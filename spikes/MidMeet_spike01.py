#!/usr/bin/env python3
"""
Spike question: can one search (2 addresses -> places near midpoint -> drive
times) finish in under 5 seconds on Google's APIs?

Setup: enable Geocoding API, Places API (New) and Routes API on your project.

Usage:
    export GOOGLE_MAPS_API_KEY=your_key
    python meetup_spike.py                 # 5 runs, default locations
    python meetup_spike.py --runs 10
    python meetup_spike.py "Addr A" "Addr B"

Billable events per run: 2 Geocoding, 1 Places Nearby Search, and
2 x N Route Matrix elements (N = candidates, default 5 -> 10 elements).
Stdlib only. Each call opens a new HTTPS connection (TLS handshake included),
so timings are slightly pessimistic vs. a server that reuses connections.
"""
import json
import math
import os
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
BUDGET_S = 5.0
N_CANDIDATES = 5
RADIUS_M = 2000
DEFAULT_A = "Addison Circle Park, Addison, TX"
DEFAULT_B = "University of Texas at Dallas, Richardson, TX"


def http(url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=data, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} from {url.split('?')[0]}:\n{e.read().decode()[:600]}\n"
                 "Check that this API is enabled on the project and the key allows it.")


def geocode(address):
    q = urllib.parse.urlencode({"address": address, "key": KEY})
    d = http(f"https://maps.googleapis.com/maps/api/geocode/json?{q}")
    if d["status"] != "OK":
        sys.exit(f"Geocoding failed for '{address}': {d['status']} {d.get('error_message', '')}")
    r = d["results"][0]
    return {"lat": r["geometry"]["location"]["lat"],
            "lng": r["geometry"]["location"]["lng"],
            "addr": r["formatted_address"]}


def midpoint(a, b):
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    dl = math.radians(b["lng"] - a["lng"])
    bx, by = math.cos(p2) * math.cos(dl), math.cos(p2) * math.sin(dl)
    lat = math.atan2(math.sin(p1) + math.sin(p2), math.hypot(math.cos(p1) + bx, by))
    lng = math.radians(a["lng"]) + math.atan2(by, math.cos(p1) + bx)
    return {"lat": math.degrees(lat), "lng": math.degrees(lng)}


def nearby_places(center):
    body = {
        "includedTypes": ["restaurant", "cafe"],
        "maxResultCount": N_CANDIDATES,
        "rankPreference": "DISTANCE",
        "locationRestriction": {"circle": {
            "center": {"latitude": center["lat"], "longitude": center["lng"]},
            "radius": RADIUS_M}},
    }
    # Keep the field mask minimal: it determines which SKU/price tier you pay for.
    h = {"X-Goog-Api-Key": KEY,
         "X-Goog-FieldMask": "places.id,places.displayName,places.location"}
    d = http("https://places.googleapis.com/v1/places:searchNearby", body, h)
    return [{"name": p["displayName"]["text"],
             "lat": p["location"]["latitude"], "lng": p["location"]["longitude"]}
            for p in d.get("places", [])]


def wp(p):
    return {"waypoint": {"location": {"latLng": {"latitude": p["lat"], "longitude": p["lng"]}}}}


def route_matrix(origins, dests):
    body = {"origins": [wp(o) for o in origins],
            "destinations": [wp(d) for d in dests],
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_UNAWARE"}  # TRAFFIC_AWARE is a pricier SKU
    h = {"X-Goog-Api-Key": KEY,
         "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters,condition"}
    d = http("https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix", body, h)
    out = {}
    for e in d:
        if e.get("condition") == "ROUTE_EXISTS":
            out[(e["originIndex"], e["destinationIndex"])] = (
                int(e["duration"].rstrip("s")), e.get("distanceMeters", 0))
    return out


def run_once(addr_a, addr_b):
    t = {}
    t0 = time.perf_counter()

    s = time.perf_counter()
    with ThreadPoolExecutor(2) as ex:  # geocode both addresses in parallel
        fa, fb = ex.submit(geocode, addr_a), ex.submit(geocode, addr_b)
        a, b = fa.result(), fb.result()
    t["geocode"] = time.perf_counter() - s

    mid = midpoint(a, b)

    s = time.perf_counter()
    places = nearby_places(mid)
    t["places"] = time.perf_counter() - s
    if not places:
        sys.exit("No places found near the midpoint; widen RADIUS_M.")

    s = time.perf_counter()
    m = route_matrix([a, b], places)
    t["matrix"] = time.perf_counter() - s

    t["total"] = time.perf_counter() - t0

    results = []
    for i, p in enumerate(places):
        if (0, i) in m and (1, i) in m:
            ta, tb = m[(0, i)][0], m[(1, i)][0]
            results.append({"name": p["name"], "from_a_min": ta / 60, "from_b_min": tb / 60,
                            "diff_min": abs(ta - tb) / 60,
                            "a_km": m[(0, i)][1] / 1000, "b_km": m[(1, i)][1] / 1000})
    results.sort(key=lambda r: r["diff_min"])
    return a, b, mid, results, t


def main():
    if not KEY:
        sys.exit("Set GOOGLE_MAPS_API_KEY first.")
    args = sys.argv[1:]
    runs = 5
    if "--runs" in args:
        i = args.index("--runs")
        runs = int(args[i + 1])
        del args[i:i + 2]
    addr_a, addr_b = (args + [DEFAULT_A, DEFAULT_B])[:2] if len(args) < 2 else args[:2]

    all_t = []
    for i in range(runs):
        a, b, mid, results, t = run_once(addr_a, addr_b)
        all_t.append(t)
        if i == 0:
            print(f"A: {a['addr']}\nB: {b['addr']}")
            print(f"Midpoint: ({mid['lat']:.5f}, {mid['lng']:.5f}), radius {RADIUS_M} m\n")
            print(f"{'Place':38} {'A min':>6} {'B min':>6} {'Diff':>6}")
            for r in results:
                print(f"{r['name'][:38]:38} {r['from_a_min']:6.1f} {r['from_b_min']:6.1f} {r['diff_min']:6.1f}")
            print()
        print(f"run {i + 1}: geocode {t['geocode']*1000:5.0f} ms | places {t['places']*1000:5.0f} ms | "
              f"matrix {t['matrix']*1000:5.0f} ms | total {t['total']*1000:5.0f} ms")

    tot = sorted(x["total"] for x in all_t)
    p50 = statistics.median(tot)
    p95 = tot[min(len(tot) - 1, math.ceil(0.95 * len(tot)) - 1)]
    print(f"\ntotal p50 {p50*1000:.0f} ms, p95 {p95*1000:.0f} ms, max {tot[-1]*1000:.0f} ms "
          f"(budget {BUDGET_S*1000:.0f} ms) -> {'PASS' if tot[-1] < BUDGET_S else 'FAIL'}")
    print(f"Billable per run: 2 Geocoding, 1 Nearby Search, {2 * N_CANDIDATES} matrix elements")


if __name__ == "__main__":
    main()

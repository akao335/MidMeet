# 7  Design Rationale

## 7.1  Architecture decision records

### ADR-01  Client-server: our server sits between the browser and Google

| Field | Content |
|---|---|
| Status | Accepted |
| Date and owner | 11/8/26, Vedanshi Sreeramoju |
| Context (drivers) | QAS-02 (no address may be kept), QAS-04 (only one part talks to the provider), QAS-01 (results in 5 s), CON-02 (free tier only, so the API key must not leak), UC-01, UC-02 |
| Options considered | (1) The browser calls Google directly, with no server. (2) Client-server: the browser sends the search to our server, which calls Google. (3) Layered with our own database that saves searches and results. |
| Decision | Option 2. The React web app runs on the User's device, and the Request Handler, Search Controller, Search Area Planner, Fairness Ranker and Google Connector run on a Vercel server. |
| Consequences | Favors security and privacy (QAS-02, CON-02) and modifiability (QAS-04). The key never reaches a browser, so nobody can copy it and use up our free tier. The move is putting all provider calls on a server we control. Cost: every search takes one extra network trip, which eats into the 5-second budget of QAS-01, and the team has to build and deploy server code as well as the web app. |
| Evidence | None yet. Spike S-01 (Section 8) is to measure whether a full search through our server fits in 5 seconds. |
| Related | QAS-01, QAS-02, QAS-04, CON-02, R1, ADR-02, ADR-03 |

### ADR-02  All location data goes through one Google Connector

| Field | Content |
|---|---|
| Status | Accepted |
| Date and owner | 11/8/26, Vedanshi Sreeramoju |
| Context (drivers) | CON-01 (data must come from a third party), CON-02 (free tier only), QAS-04 (switching provider changes one component), assumption A1, the P1 pricing estimate of about 250 searches a month (2.6) |
| Options considered | (1) Each server component calls Google wherever it needs data. (2) One Google Connector behind a LocationData interface, with OpenStreetMap (Nominatim, OSRM, Overpass) as the planned fallback. (3) Use OpenStreetMap from the start. |
| Decision | Option 2. Only the Google Connector talks to Google. The other components ask LocationData for locations, places and driving figures and never see which provider answered. |
| Consequences | Favors modifiability (QAS-04). If we run out of free usage or lose access (A1), we replace one component. The move is hiding the provider behind an interface. Cost: one more component to write, and LocationData can only offer what both Google and OpenStreetMap can supply, so we give up Google-only features. We chose Google over option 3 because its place data and drive times are more complete, at the risk of the usage limit. |
| Evidence | P1 economic feasibility (2.6): Route Matrix limits us to about 250 searches a month, above the about 200 we need for testing and demos. |
| Related | QAS-04, CON-01, CON-02, CON-03, A1, R1, ADR-01 |

### ADR-03  Addresses live in memory only

| Field | Content |
|---|---|
| Status | Accepted |
| Date and owner | 11/8/26, Vedanshi Sreeramoju |
| Context (drivers) | QR-02 and QAS-02 (zero addresses retained after the session), CON-03 (limits on storing provider results), stakeholder need: the other participant's address is entered without them present (2.2, 2.3) |
| Options considered | (1) Save searches and results in a database or cache so repeat searches are faster. (2) Keep the last search in browser storage so it survives a page refresh. (3) Keep addresses only in memory for the length of the request and session, and never write them to storage, logs or URLs. |
| Decision | Option 3. Search Session holds the search in browser memory, and the server forgets it when the request ends. Addresses are sent in the request body, never in a URL, and server logs record no addresses. |
| Consequences | Favors privacy (QAS-02) and keeps us within the provider's terms (CON-03). The move is having no persistent store at all. Cost: no caching, so every search pays for its full set of provider calls, which uses free-tier quota (CON-02) and time (QAS-01). If the User refreshes the page, they retype both addresses. We also lose address logs for debugging. |
| Evidence | None yet. QAS-02 will be verified by inspecting browser storage, server logs and network requests after 10 sessions. |
| Related | QAS-02, QR-02, CON-03, ADR-01 |

### ADR-04  A provider failure ends the search with a "try again" message

| Field | Content |
|---|---|
| Status | Accepted |
| Date and owner | 11/8/26, Vedanshi Sreeramoju |
| Context (drivers) | QAS-03 (message within 6 s, all inputs kept, no partial ranking), QAS-05 (ranking must be correct), UC-01 A4, UC-02 A2 |
| Options considered | (1) Retry the failed provider call automatically before giving up. (2) Show a partial ranking from whichever places returned figures. (3) Stop each provider call after 4 seconds and show a "try again" message with the User's entries kept. |
| Decision | Option 3. The Search Controller gives each provider call a 4-second limit, does not retry, and never ranks places with missing figures. |
| Consequences | Favors availability as the User sees it (QAS-03) and correctness (QAS-05). The User gets a clear answer quickly instead of a long wait or a ranking that looks fair but is built on incomplete data. The move is failing fast. Cost: a brief provider hiccup ends the search, and the User has to ask again, even when a retry would have succeeded. |
| Evidence | None yet. QAS-03 will be tested with 20 forced provider failures. |
| Related | QAS-03, QAS-05, UC-01 A4, UC-02 A2, R1 |


## 7.2  Trade-off summary

| Quality favored | Architectural move | Cost accepted | Recorded in |
|---|---|---|---|
| Security, privacy | Server between the browser and Google, holding the key | Extra network trip per search; server code to build | ADR-01 |
| Modifiability | One Google Connector behind LocationData | Extra component; no Google-only features | ADR-02 |
| Privacy | No persistent storage; addresses in memory only | No caching, so more provider calls and quota; entries lost on refresh | ADR-03 |
| Availability, correctness | 4-second timeout, no retry, no partial results | A brief provider hiccup fails the whole search | ADR-04 |













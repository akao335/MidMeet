# P2 Section 9: Traceability

## 9.1 Extended traceability matrix

| Requirement | Use case | Analysis classes | Component(s) | QAS / ADR | Evidence |
|---|---|---|---|---|---|
| FR-01 | UC-01 | Participant, StartLocation | Search Form, Search Session, Google Connector | QAS-02, ADR-03 | Acceptance test in 3.1; planned for P3 |
| FR-02 | UC-01 (A1) | StartLocation | Search Form, Request Handler, Google Connector | — | Acceptance test in 3.1; planned for P3 |
| FR-03 | UC-01, UC-02 | MeetingSearch, MeetingOption | Search Form, Search Session, Fairness Ranker | QAS-05 | 10-pair miles/minutes test (3.1) |
| FR-04 | UC-01, UC-02 | MeetingOption, Place | Search Controller, Search Area Planner, Google Connector, Results View | QAS-05, ADR-02 | 10-pair result-count test (3.1) |
| FR-05 | UC-01, UC-02 | MeetingSearch, Place | Search Form, Search Controller, Google Connector | ADR-02 | Category filter test (3.1) |
| FR-06 | UC-01, UC-02 | TravelEstimate, MeetingOption | Google Connector, Fairness Ranker, Results View | QAS-05, ADR-04 | 30-row value check (3.1) |
| FR-07 | UC-01, UC-02 | StartLocation, Place | Map View | — | Marker check (3.1) |
| FR-08 | UC-01 (A3), UC-02 (A1) | MeetingSearch | Search Controller, Results View | — | Empty-result test (3.1); Q3 answer (11) |
| FR-09 | UC-03 | DirectionsRequest, Place | Place Actions | — | Link test (3.1) |
| FR-10 | — (WON'T) | — | — | — | Search Form offers only 2 address entries |
| FR-11 | — (WON'T) | — | Google Connector (driving only) | — | No travel-mode option in UI |
| QR-01 | UC-01, UC-02 | — | Search Session, Search Controller, Google Connector | QAS-01, ADR-01, ADR-04 | Spike S-01 blocked ($30 prepayment); timing deferred to P3 |
| QR-02 | UC-01 | StartLocation | Search Session, Request Handler | QAS-02, ADR-03 | 10-session storage/log inspection planned |
| QR-03 | UC-01, UC-02 | — | Search Form, Results View, Map View | — | 5-tester usability session planned |
| QR-04 | UC-01, UC-02 | TravelEstimate, MeetingOption | Fairness Ranker, Google Connector | QAS-05, ADR-04 | 20-pair DFW test planned |
| CON-01 | UC-01, UC-02 | Place, TravelEstimate | Google Connector | QAS-04, ADR-02 | Component view (6.3) |
| CON-02 | All | — | Google Connector, server key | QAS-04, ADR-01, ADR-02 | Spike S-01 found $30 prepayment; under review (10.2) |
| CON-03 | UC-01 | Place | Google Connector, Search Session | ADR-03 | No persistent store (6.2, ADR-03) |
| CON-04 | — | — | — (project process) | — | GitHub repo, tag `p2` |

## 9.2 Gap analysis

| Gap | Items | What we did about it |
|---|---|---|
| Requirements with no component | FR-10, FR-11, CON-04 | FR-10 and FR-11 are WON'T items, so having no component is intended. CON-04 is a process constraint met by the repo and milestones, not by runtime code. QR-03 has components but no QAS or ADR; it will be verified by the usability session in P3. |
| Components with no requirement, QAS or ADR | Place Actions (share message, UC-04) | The sharing behavior has no FR. Propose adding FR-12 (COULD: share the chosen place) as a 0.2 change in P3, or drop sharing from Place Actions. |
| Use cases not analyzed (and why that is acceptable) | UC-04 Share the chosen place | UC-04 is an optional extension of UC-02. It only formats data already on screen, adds no provider calls, and carries no requirements yet, so it has no non-trivial steps to analyze. |

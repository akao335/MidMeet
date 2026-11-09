# 4 Use-Case Analysis

Nov 8, 2026 · @ak

## 4.1 Use cases selected for analysis

We analyze UC-01, UC-02 and UC-03: the two use cases written out in full at P1, plus the one that hands the User to a system outside MidMeet. Together they realize every MUST and COULD functional requirement (FR-01 to FR-09).

| Use case | Name | Why it was selected | Non-trivial steps |
| --- | --- | --- | --- |
| UC-01 | Find Fair Meeting Places | Carries the core promise of the product and touches most of our requirements (FR-01 to FR-08, QR-01, QR-02, QR-04). It depends on outside data and has four failures the User can see: an address that cannot be found, two addresses at one location, too few places, and an unavailable provider. | (10): locating both addresses, finding places near the middle, getting both participants' travel figures, ranking the places and showing them. Steps (1) to (9) only record or acknowledge the User's input. |
| UC-02 | Compare and Select a Place | This is where fairness is judged. Changing the category or the measure re-ranks the places, and QR-04 holds only if the ranking is right in both measures. | (2): finding and ranking places for a new category. (4): re-sorting by the other measure. Step (6) only shows details already held, so it is trivial. |
| UC-03 | Get Directions to the Chosen Place | The only use case that leaves MidMeet for an external system, and the hand-over can fail in a way the User sees. We are least sure how this hand-over behaves. | (2): handing the chosen place to the directions app. |

UC-04 (Share the chosen place) is not analyzed here. It extends UC-02 and no requirement traces to it yet (see 9.2).

## 4.2 Expanded use cases

### UC-01 Find Fair Meeting Places

| Field | Content |
| --- | --- |
| Primary actor | User |
| Supporting actors and external systems | Location data provider (supplies address lookup, place data and travel figures; outside MidMeet, R1) |
| TUCBW (this use case begins when) | The User asks MidMeet for a fair place for two participants to meet. |
| TUCEW (this use case ends when) | The User sees the ranked places, each with both participants' travel figures, on a list and on a map. |
| Preconditions | MidMeet is open on the User's device. |
| Postconditions | The User has seen 3 to 10 real, named places ranked by fairness gap, each with both participants' driving miles and minutes. Both start locations and all listed places are on the map. No start address is kept after the session ends (QR-02). |
| Traces to requirements | FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, QR-01, QR-02, QR-03, QR-04, CON-01 |

| Actor input / action | System response |
| --- | --- |
|  | (0) The system shows an entry for each participant's start address, a choice of fairness measure with minutes selected, a choice of place category, and no results. |
| (1) The User enters the first participant's start address. | (2) The system shows the address as entered, beside participant 1. |
| (3) The User enters the second participant's start address. | (4) The system shows the address as entered, beside participant 2. |
| (5) The User chooses to measure fairness in miles or in minutes. | (6) The system shows the chosen measure as selected. |
| (7) The User chooses a place category, such as coffee, restaurant or park. | (8) The system shows the chosen category as selected. |
| (9) The User asks for results. | (10) The system shows both start locations and 3 to 10 places of the chosen category on a map and in a list ranked by smallest fairness gap. Each place shows its name, street address, both participants' driving miles and minutes, and the fairness gap in the chosen measure, labelled with its unit. |

Steps (5) and (6) are skipped when the User keeps the default of minutes.

| Alternate flow | At step | Condition | What happens | Ends or rejoins at |
| --- | --- | --- | --- | --- |
| A1 | (10) | A start address is empty or cannot be found. | The system shows an error beside that address and keeps everything else the User entered (FR-02). The User corrects the address. | Rejoins at (1) or (3), for the participant concerned, then continues to (9). |
| A2 | (10) | Both addresses refer to the same location. | The system tells the User and asks them to check the addresses. Entries are kept. | Rejoins at (1). |
| A3 | (10) | Fewer than 3 places of the chosen category are found, even after the search area is widened. | The system tells the User too few places were found, stating that none were found when there are none (FR-08), and keeps all entries. The User may choose another category. | Rejoins at (7). |
| A4 | (10) | The provider does not answer in time or fails. | The system shows a "try again" message and keeps everything the User entered. | Rejoins at (9). |

### UC-02 Compare and Select a Place

| Field | Content |
| --- | --- |
| Primary actor | User |
| Supporting actors and external systems | Location data provider (supplies place data for a new category; outside MidMeet, R1) |
| TUCBW (this use case begins when) | The User, looking at the ranked places, wants to compare the options and settle on one. |
| TUCEW (this use case ends when) | The User sees the selected place highlighted on the map with its details. |
| Preconditions | UC-01 has finished and a ranked list of places is on screen. |
| Postconditions | One place is selected. The User can see its name, street address, both participants' driving miles and minutes, and the fairness gap. |
| Traces to requirements | FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, QR-03, QR-04, CON-01 |

| Actor input / action | System response |
| --- | --- |
|  | (0) The system shows the ranked places in a list and on the map with both start locations, and the category and fairness measure currently in use. |
| (1) The User changes the place category, for example from coffee to park. | (2) The system shows 3 to 10 places of the new category, ranked by smallest fairness gap in the current measure, on the list and on the map. |
| (3) The User switches the fairness measure between minutes and miles. | (4) The system shows every place with its gap in the new measure and unit, sorted by smallest gap. |
| (5) The User selects one place. | (6) The system highlights that place on the map and shows its name, street address, both participants' driving miles and minutes, and the fairness gap. |

Steps (1) to (4) are optional and may be repeated in any order. The User may go straight from (0) to (5).

| Alternate flow | At step | Condition | What happens | Ends or rejoins at |
| --- | --- | --- | --- | --- |
| A1 | (2) | No place of the new category exists near the middle. | The system tells the User and keeps the previous category and results on screen. | Rejoins at (1). |
| A2 | (2) | The provider does not answer in time or fails. | The system shows a "try again" message and keeps the previous results on screen. | Rejoins at (1). |
| A3 | (4) | The fairest place in the new measure is not the fairest in the old one. | The system shows the new order and tells the User the order changed because the measure changed. | Rejoins at (5). |
| A4 | (6) | The User wants directions to the selected place. | The system offers directions; UC-03 begins. | Ends here; UC-03 begins. |
| A5 | (6) | The User wants to send the result to the other participant. | UC-04 (Share the chosen place) begins. | Ends here; UC-04 begins. |

### UC-03 Get Directions to the Chosen Place

| Field | Content |
| --- | --- |
| Primary actor | User |
| Supporting actors and external systems | Directions app (a separate application on the User's device that shows routes; outside MidMeet) |
| TUCBW (this use case begins when) | The User, having selected a place, asks for directions to it. |
| TUCEW (this use case ends when) | The User sees the directions app showing the selected place as the destination. |
| Preconditions | UC-02 has finished: one place is selected and its details are on screen. |
| Postconditions | The directions app is showing the selected place's name and address as the destination. The selected place is still selected in MidMeet. |
| Traces to requirements | FR-09 |

| Actor input / action | System response |
| --- | --- |
|  | (0) The system shows the selected place's name, street address and details, with the option to get directions to it. |
| (1) The User asks for directions to the selected place. | (2) The system opens the directions app with the selected place as the destination, showing its name and address. |

| Alternate flow | At step | Condition | What happens | Ends or rejoins at |
| --- | --- | --- | --- | --- |
| A1 | (2) | The directions app cannot be opened or does not accept the place. | The system tells the User that directions could not be opened and shows the place's full street address so it can be copied. The selected place stays selected. | Ends; the User may rejoin UC-02 at (5). |

## 4.3 Self-review log

Reviewing the P1 use cases turn by turn found seven defects, all fixed in 4.2. The last row lists what section 5.1 must contain.

| Use case | Check | Defect found | How it was fixed |
| --- | --- | --- | --- |
| UC-01 | Step (0) present | P1 had no starting screen, so nothing said what the User sees before acting. | Added (0): both address entries, the measure choice with minutes selected, the category choice and no results. |
| UC-01 | One turn per row | P1 steps 1 to 4 were all User input with no system response between them, and steps 5 to 7 were system work the User only waits for. | Split the input into separate turns, each with a response, and merged the waiting steps into response (10). |
| UC-01 | Ends with a perceivable acknowledgment | P1 steps 2 and 3 (choosing the measure and category) were never acknowledged. | Added responses (6) and (8) that show the choice as selected. |
| UC-01 | Precondition or alternate flow | P1 listed "internet connection and provider services reachable" as a precondition, but a provider failure can happen while MidMeet works normally. It is already flow 6b. | Reduced the precondition to "MidMeet is open on the User's device" and kept the failure as A4. |
| UC-01, UC-02 | No technology | P1 named "Geocoding service, Routes service, Places service (Google Maps Platform)" and said the system "geocodes" addresses. | Replaced them with "Location data provider" and "locates". The provider is named only in the references. |
| UC-02 | Real alternate flows | P1 left open whether the User is told the order changed when the measure changes (its flow 5a). P1 also gave no failure for a category change. | Decided that the system tells the User (A3), and added A1 and A2 for the category change. A switch of measure needs no new provider request, because both miles and minutes are already held from UC-01. |
| UC-03 | Step (0) and acknowledgment | P1 gave UC-03 no turn-by-turn form, so the hand-over to the directions app had no visible end. | Wrote (0) to (2), ending when the directions app shows the destination, and added A1 for a hand-over that fails. |
| All | Actor items are in the domain model | The actor columns name these items: a start address for each participant, the fairness measure, the place category, the selected place, and the directions request. | These become required attributes in the domain model (5.1), and check K1 in 5.3 confirms them. |

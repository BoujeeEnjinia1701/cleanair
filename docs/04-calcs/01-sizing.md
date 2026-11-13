---
doc_id: CAR-CAL-001
title: CleanAir Retrofit Kit sizing and first-principles checks
project: CleanAir Retrofit Kit
doc_type: Calculation
version: "0.2"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First sizing note for options CA1 to CA3; fan curve against media, CADR, eACH, bypass, UV-C dose, mass, cost
  - version: "0.2"
    date: 2026-11-12
    author: Amish Chadha
    change: After the independent STEM review, both shut-off pressures carried, four-panel measured CADR as the design basis, worst-case bypass with the tray seam, 7.3 times loading, low speed
---

# CleanAir Retrofit Kit sizing and first-principles checks

Result: a box fan develops only about 27 to 55 Pa, so the face area of media decides the airflow. Four MERV-13 panels (CA2, 0.98 m2) let the fan run near its free air; one panel (CA1, 0.25 m2) does not. The design basis is the measured CADR of four-panel cubes, **398 to 459 m3/h on high**; two cubes give a 150 m3 ward 5.3 to 6.1 eACH and one gives a 60 m3 room 6.6 to 7.6 eACH. Kit parts cost USD 111.83 against the USD 150 value-engineering target, fan excluded. All figures are estimates from `docs/04-calcs/sizing.py` (results in `sizing_results.json`), which reads `cad/src/model.py` and `bom/bom.csv`. Sources are listed in CAR-STM-001, checked 2026-11-12.

## 1. Assumptions

| # | Assumption | Basis | Effect if wrong |
| --- | --- | --- | --- |
| A1 | Fan curve is quadratic, dP = Pmax (1 - (Q/Q0)^2) | Common first-order shape; no stall dip | Flows near shut-off (CA1) are optimistic |
| A2 | Shut-off 27.5 Pa (low-speed fit) to 55 Pa (fan laws with the 1.42 CADR ratio as speed ratio) | Dal Porto et al. 2022: 12 % flow loss at 6.2 Pa | Brackets every flow |
| A3 | Media drop is linear in face velocity, k 38.2 to 62.1 Pa per m/s | Parker and Global Industrial data sheets at 500 and 300 fpm | Overstates drop at low velocity (UC Davis 5 to 7.5 Pa estimated) |
| A4 | Smaller round fans keep the same shut-off; free air scales with swept area | Assumed; fan laws give less for small fans | CA1 small-fan flows optimistic |
| A5 | Leak discharge coefficient 0.6 | Sharp-edged orifice | Conservative for a 1 mm slot |
| A6 | Rooms well mixed | eACH = CADR / V | Placement matters (S27) |
| A7 | Panel set changed every 6 months at 24 h use, for cost only | To set from the loaded-flow test V4 | Yearly cost |
| A8 | Low-cost UV-C strip: 6 LEDs at 10 mW, mean path 0.10 m; dose = P l / Q | Assumed for a strip at the fan face | X4 |
| A9 | Actinic weighting S(275 nm) about 0.96 | ACGIH spectrum | Eye limit time |
| A10 | 4 mm twin-wall PP sheet 0.75 kg/m2 | Assumed, to weigh | Mass |
| A11 | 20 x 20 x 2 in MERV-13 panel 0.68 kg | Assumed, to weigh | Mass |
| A12 | Times from step counts: assembly 8 to 12 min, set change 4 to 6 min, one panel 1.5 to 2.5 min | Estimate | PR-007, PR-008 |

## 2. Geometry (from the model)

Four bought panels, 495 x 495 x 44 mm actual (20 x 20 x 2 in nominal), stand in a pinwheel: cube 539 mm outside, 0.98 m2 of face. Tray and deck 549 mm, 30 mm flaps, from 610 x 914 mm sheets. Deck opening 480 mm. Gasket 510 mm square. Overall 576 mm across the buckles and 639 mm high with a 20 in box fan.

## 3. Fan curve

Pmax 27.5 to 55 Pa. Free delivery 3,058 m3/h (1,800 cfm, the Lasko 3733 rating, an upper bound) or 965 m3/h (568 cfm, derived from UC Davis: 500 cfm through a four-filter cube at about 6.2 Pa). These are the same class of fan; the spread is model uncertainty (S24).

## 4. Operating points

Table 1. Clean panels, high speed (model).

| Option | Airflow (m3/h) | Media drop (Pa) | Face velocity (m/s) | CADR at E1 50 % (m3/h) |
| --- | --- | --- | --- | --- |
| CA1, one panel | 341 to 1,110 | 21 to 52 | 0.39 to 1.26 | 171 to 555 |
| CA2, four panels | 712 to 2,277 | 9 to 34 | 0.20 to 0.65 | 356 to 1,139 |

A flat panel at the fan's free-air velocity (3.47 m/s) would need 133 to 215 Pa, 2.4 to 7.8 times the shut-off; the fan slows to 13 to 71 % of free air instead. Measured on box fans, one filter gave 142 to 154 cfm against 443 to 500 cfm on a four-filter cube (29 to 35 %). The model brackets the measurements and runs high; design figures use measured CADR.

## 5. Clean air delivery rate (design basis)

Four-panel cubes on high: 398 m3/h (EPA, MS2 virus aerosol) to 459 m3/h (UC Davis, from a 54 % rating). Low speed: 277 to 280 m3/h. A five-panel cube on a stronger fan gave 1,020 to 1,450 m3/h (Dal Porto), a reference only. CA1 analogue (one filter on a box fan): 131 to 141 m3/h. PR-001 (400 m3/h) is at risk at the low end; PR-005 is a bought rating.

## 6. Air changes per hour

Table 2. eACH from measured CADR, clean panels, high speed.

| Room | Volume (m3) | 5 ACH needs (m3/h) | One CA2 cube | Two CA2 cubes | One CA1 kit |
| --- | --- | --- | --- | --- | --- |
| Ward 50 m2 x 3 m | 150 | 750 | 2.7 to 3.1 | 5.3 to 6.1 | 0.9 |
| Clinic room 20 m2 x 3 m | 60 | 300 | 6.6 to 7.6 | not needed | 2.2 to 2.4 |

Lancet "better" 6 ACHe needs 900 m3/h in the ward (2 to 3 cubes) and 360 m3/h in the clinic room (one cube). Two cubes give 10 L/s per person for about 22 occupants; PR-002 states 20. On low speed one cube gives the clinic room 4.6 eACH. PR-002 and PR-003 are met on paper; CA1 needs 6 kits for the ward on measured data.

## 7. Bypass

Worst case over both fans, both shut-off pressures and both media. CA2 seams total 6.2 m (deck gasket 2.0 m, four corner seams 2.0 m, tray seam 2.2 m): 0.5 mm 1.9 to 4.2 %, 1 mm 3.7 to 8.2 %, 2 mm 7.2 to 15.5 %. CA1 on a 16 in rim (1.44 m): 1 mm 2.5 to 5.5 %, 5 mm 11 to 23 %; round a box fan face (2.15 m) 5 mm reaches 31 %. PR-006 (10 %) is met on paper at 1 mm.

## 8. Loading

At the final resistance (2.6 times initial) CA2 keeps 467 to 1,509 m3/h and CA1 149 to 486 m3/h; at UL's dust-loaded 7.3 times, CA2 204 to 667 and CA1 53 to 175 m3/h. PR-021 sets the change point at 60 % of clean airflow, to measure (V4).

## 9. Mass, stability and envelope

Kit about 4.4 kg, with a 3.3 kg box fan 7.7 kg (PR-022). Centre of gravity about 0.42 m up; tipping angle 28 deg on the feet (PR-012, 10 deg needed); a 27 N push at the top tips it, so floor use only and away from walkways. Flat pack: two sheet blanks and four panels, about 0.05 m3 (PR-016).

## 10. Power, energy and cost

Box fans draw 52.8 to 103 W on high (UL, UC Davis), 70 W on low (PR-019). Running 24 h a day, 587 to 858 kWh a year. Clean air per watt: about 3.9 m3/h per W for four panels (14.8 for the five-panel reference). Kit parts USD 111.83 (PR-015): panels USD 54.00 (48 %), sheet USD 21.28, straps USD 16.00, feet USD 11.40, gasket USD 6.75, bolts and label USD 2.40. Panels recur at about USD 108 a year (A7). Cost per m3/h of CADR: USD 0.24 to 0.28.

## 11. UV-C (team concept, removed)

Low-cost strip at the fan face: 0.003 mJ/cm2, 1 % single pass for an estimated SARS-CoV-2 D90 of 0.5 mJ/cm2, +0.07 eACH in the ward. High-power strip (8 x 65 mW, about 18 W), 0.30 m path: 0.16 mJ/cm2, 53 % at best, +1.2 eACH; one LED of 40 to 65 mW reaches the ACGIH limit (3 mJ/cm2 effective) in 7 to 11 minutes at 1 m. Removed (CAR-DEC-001 F2; PR-009).

## 12. CA3 return grille

A 2 in panel on a 508 mm grille: 0.77 to 1.54 m/s at 400 to 800 cfm, 29 to 96 Pa against the 25 Pa DOE optimum; CADR 340 to 680 m3/h only while the air handler runs.

## 13. Results against the requirements

Table 3. Results by product requirement.

| PR | Result on paper | Section |
| --- | --- | --- |
| PR-001 | 398 to 459 m3/h measured against 400: at risk | 5 |
| PR-002 | Two cubes 5.3 to 6.1 eACH; 22 occupants at 10 L/s each | 6 |
| PR-003 | 6.6 to 7.6 eACH | 6 |
| PR-004 | 480 mm opening fits a 20 in box fan; 280 and 380 mm cut lines for round fans, fit to test | 2 |
| PR-005 | Bought MERV-13 rating | 5 |
| PR-006 | 3.7 to 8.2 % at 1 mm | 7 |
| PR-007 | 8 to 12 min estimate | 1 (A12) |
| PR-008 | Set 4 to 6 min, one panel 1.5 to 2.5 min: at risk | 1 (A12) |
| PR-009 | No active stage | 11 |
| PR-010 | No electrical part; listed fan | 10 |
| PR-011 | Straps on the fan frame, outside the guard | 2 |
| PR-012 | 28 deg | 9 |
| PR-013 | Label (BOM 9) | 10 |
| PR-014 | To test | not calculated |
| PR-015 | USD 111.83 | 10 |
| PR-016 | About 0.05 m3 | 9 |
| PR-017 | To test | not calculated |
| PR-018 | To test | not calculated |
| PR-019 | 98 to 103 W measured | 10 |
| PR-020 | Wording checked by `render.py --check` | not calculated |
| PR-021 | 60 % change point; loaded flows in section 8 | 8 |
| PR-022 | 7.7 kg, 576 mm | 9 |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.

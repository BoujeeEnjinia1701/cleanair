---
doc_id: CAR-PRS-001
title: CleanAir Retrofit Kit product requirements and specifications
project: CleanAir Retrofit Kit
doc_type: Product requirements
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First product requirements for the carried option CA2, traced to CAR-URS-001, with targets, tolerances and planned verification
---

# CleanAir Retrofit Kit product requirements and specifications

Requirements for the carried option CA2 (filter cube on an existing box fan); the choice between CA2 and CA1 is awaiting Amish (CAR-DEC-001 D1). Status "met on paper" means CAR-CAL-001 or a cited measurement shows it; nothing is tested at TRL 3. Verification families are in CAR-VER-001.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-003 | Performance | CADR per cube | One cube on its fan, high speed, clean panels, shall deliver a CADR for 0.3 to 1 um particles of at least the target | 400 | minimum | m3/h | Test V2 at TRL 4 (chamber decay, AHAM AC-1 method as benchmark) | At risk (measured four-panel cubes 398 to 459) |
| PR-002 | UR-001 | Performance | Ward air changes | Two cubes shall give at least 5 eACH in a 150 m3 ward and at least 10 L/s per person for up to 20 occupants | 5 | minimum | 1/h | Analysis CAR-CAL-001 section 6; test V3 at TRL 4 | Met on paper (5.3 to 6.1) |
| PR-003 | UR-001 | Performance | Clinic room air changes | One cube shall give at least 5 eACH in a 60 m3 room | 5 | minimum | 1/h | Analysis CAR-CAL-001 section 6; test V3 at TRL 4 | Met on paper (6.6 to 7.6 on high) |
| PR-004 | UR-002, UR-016 | Deployment and assembly | Fans it fits | The kit shall fit an existing 20 in box fan; the deck shall carry cut lines for 12 and 16 in shrouded fans | 20 | 12 to 20 | in | Inspection and fit test V7 on 5 fan models | Met by design for box fans; at risk for round fans |
| PR-005 | UR-003 | Performance | Media rating | Panels shall be bought with a MERV-13 rating to ASHRAE 52.2 (E1 at least 50 %, E2 at least 85 %) on the supplier's report | 13 | minimum | MERV | Inspection of supplier report | Met by design (bought rating) |
| PR-006 | UR-001 | Performance | Bypass | Air bypassing the media at the gasket and seams shall not exceed the target | 10 | maximum | % | Analysis CAR-CAL-001 section 7; smoke and pressure test V4 | Met on paper (3.7 to 8.2 at 1 mm) |
| PR-007 | UR-004 | Deployment and assembly | Assembly | First assembly shall need no tools and take no longer than the target | 15 | maximum | min | Timed demonstration V6 with the personas | To verify at TRL 4 (estimate 8 to 12) |
| PR-008 | UR-005 | Maintenance | Filter change | A filter change shall take no longer than the target (the deck's 2 minutes; per panel or per set to decide, CAR-DEC-001 D3) | 2 | maximum | min | Timed demonstration V6 | At risk (set 4 to 6, one panel 1.5 to 2.5) |
| PR-009 | UR-006, UR-014 | Safety | No ozone source | The kit shall contain no UV lamp, ioniser or electrostatic stage; ozone benchmark UL 2998 under 0.005 ppm | 0.005 | maximum | ppm | Inspection; ozone test only if any active stage is added | Met by design |
| PR-010 | UR-006 | Safety | Listed fan only | The kit shall be used only on a fan listed to UL 507 or IEC 60335-2-80 with guards on both faces; the kit adds no electrical part | 0 | none | electrical parts | Inspection; motor temperature test V5 | Met by design; listing coverage to assess |
| PR-011 | UR-006 | Safety | Guards untouched | No kit part shall remove, open or press on a fan guard | 0 | none | parts on guard | Inspection | Met by design (straps on the fan frame, F3) |
| PR-012 | UR-007 | Safety | Stability | The cube with its fan shall not tip on a 10 deg incline; floor use only | 10 | minimum | deg | Analysis CAR-CAL-001 section 9; tilt test V6 | Met on paper (28 deg) |
| PR-013 | UR-008 | Usability | Change prompt | The label shall show the airflow direction, a change interval and a ribbon check at the outlet | 1 | none | label | Inspection | Met by design (label) |
| PR-014 | UR-009 | Maintenance | Wipe clean | Sheet parts shall withstand 70 % alcohol and 0.5 % sodium hypochlorite wipes | 50 | minimum | wipe cycles | Test V8 | To verify at TRL 4 |
| PR-015 | UR-010 | Cost | Kit cost | Kit parts at prototype quantities shall be within the value-engineering target | 150 | maximum | USD | BOM | Met on paper (USD 111.83) |
| PR-016 | UR-011 | Logistics | Standard parts, flat pack | Panels shall be the 20 x 20 x 2 in nominal size; the kit shall pack flat within the target | 0.06 | maximum | m3 | Inspection | Met by design |
| PR-017 | UR-012 | Environment and durability | Humidity | The cube shall hold its shape after 7 days at 35 C and 90 % RH | 7 | minimum | days | Test V8 | To verify at TRL 4 |
| PR-018 | UR-013 | Usability | Noise | Sound level on the speed used at night shall not exceed the target at 1 m | 50 | maximum | dBA | Test V8 | To verify at TRL 4 (target to set with the partner) |
| PR-019 | UR-015 | Performance | Power | Power on high shall not exceed the target | 110 | maximum | W | Measurement V5 | Met on paper (98 to 103 W measured on box fans) |
| PR-020 | UR-014 | Regulatory | Claims | All wording shall follow CAR-CLM-001 | 0 | none | banned claims | Inspection; `render.py --check` | Met by design |
| PR-021 | UR-001, UR-005 | Maintenance | Change point | Panels shall be changed before the airflow falls below the target share of its clean value | 60 | minimum | % | Loaded-flow test V4 | To verify at TRL 4 |
| PR-022 | UR-004, UR-007 | Deployment and assembly | Mass and size | The cube with its fan shall weigh under 10 kg and pass a 700 mm door | 10 | maximum | kg | Analysis CAR-CAL-001 section 9; weighing | Met on paper (7.7 kg, 576 mm) |

## Assumptions

Assumptions A1 to A12 are listed in CAR-CAL-001 section 1. Targets remain proposals for review with a co-design partner.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.

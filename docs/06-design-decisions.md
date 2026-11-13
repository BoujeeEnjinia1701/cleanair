---
doc_id: CAR-DEC-001
title: CleanAir Retrofit Kit design decisions register
project: CleanAir Retrofit Kit
doc_type: Design decisions register
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First register; D1 to D7 proposed, awaiting Amish; F1 to F3 made under the standing instruction of 2026-10-23
---

# CleanAir Retrofit Kit design decisions register

Every design decision for this repo, in one place. Nothing below is recorded as Amish's decision unless he made it: the open decisions are **proposed, awaiting Amish**. The STEM fixes F1 to F3 were made under his standing instruction of 2026-10-23 (STANDARDS section 20) and he can reverse them.

## Open decisions (proposed, awaiting Amish)

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| D1 | Concept choice | CA1 collar and flat cassette (170 of 245); CA2 filter cube (185); CA3 return-grille cassette (166) | CA2 and CA1 are within 10 %, so both come to Amish without a pick. Engineering view: CA2 meets UR-001 with 2 units per ward against 6 for CA1 on measured data; CA1 fits more of the fans on site. CA2 is carried in the drawings, BOM and build plan so a constructable design exists | Everything | CAR-OPT-001, CAR-DDR-001 |
| D2 | Round fans on CA2 (runner-up's best idea) | (a) box fans only; (b) deck cut lines for 12 and 16 in fans with a foam ring; (c) the team's silicone collar as an adaptor ring on the deck | (b) for the prototype as modelled, (c) designed after a fit test on five fan models (V7) | Deck; possibly a collar part | CAR-OPT-001 |
| D3 | Filter-change target (CAR-STM-001 S18) | (a) keep "under 2 minutes" for the whole set (not met on paper: 4 to 6 min); (b) under 2 minutes per panel and under 6 for the set; (c) change panels in pairs | (b) | PR-008; label | Team deck; CAR-CAL-001 A12 |
| D4 | Number of panels | (a) four sides, solid tray (as modelled); (b) a fifth panel as the floor, as in the Dal Porto cube (adds USD 13.50 and 25 % more media area) | (a) now; (b) tested side by side in V2 | Tray, BOM | CAR-CAL-001 section 5 |
| D5 | Air treatment beyond filtration | (a) none (as fixed under F2); (b) an enclosed, interlocked UV-C module as a separate product with its own STEM check, exposure test (IEC 62471) and ozone test | (a) | None now | CAR-STM-001 X4 |
| D6 | Fan supply | (a) the facility's own box fan; (b) a listed box fan bought with the kit (USD 23.49, Lasko 3733 listing) | (a), with (b) offered where none exists | MKT, BOM | CAR-MKT-001 |
| D7 | Speed used in wards at night | (a) high (398 to 459 m3/h); (b) low (about 280 m3/h, quieter) with a third cube in the ward | Set with the field partner after the noise test V8 | Units per room | CAR-STM-001 S26 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| C1 | Actual panel size (expected 495 x 495 x 44 mm) and a supplier MERV-13 report to ASHRAE 52.2 | Tray and deck sizes; PR-005 | BOM 1 |
| C2 | UL 900 or equivalent fire classification of the panels; a flame-retardant grade of PP sheet | Combustible materials (S16) | CAR-STM-001 S16 |
| C3 | Whether the fan maker allows the fan to run lying flat with filters (listing coverage) | S10, S25 | CAR-REG-001 |
| C4 | Chemical resistance of the bought PP sheet to 70 % alcohol and 0.5 % sodium hypochlorite | PR-014 | CAR-STM-001 S21 |
| C5 | Freedom to operate against US 12,582,929 B2 (3M) by a patent attorney | Desk reading only | CAR-FTO-001 |
| C6 | Mass of a panel and of the sheet (assumed 0.68 kg and 0.75 kg/m2) | Mass and stability | CAR-CAL-001 A10, A11 |

## Value engineering

Value-engineering target: USD 150 per complete kit (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 111.83 (USD 38.17 under the target), fan excluded. With a new box fan the kit would be USD 135.32. The stretch target of under USD 80 at volume is not met on paper. Main cost drivers: the four MERV-13 panels (USD 54.00, 48 %), the two PP sheets (USD 21.28) and the four straps (USD 16.00). Savings worth trying: panels by the case at volume; tray and deck cut from one 1,220 x 2,440 mm sheet; two straps instead of four with the fan held by deck tabs; feet moulded or cut from sheet offcuts.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-11-12 | Repo shape (one public repo), licences as Helpful Water (CERN-OHL-P-2.0, Apache-2.0, CC-BY-4.0), no archive, the credits list | Amish | `project.yaml`, STANDARDS 25 |
| 2026-11-12 | F1: scope is shrouded fans (box, pedestal, wall) and duct openings; ceiling fans removed (a collar cannot seal to an unshrouded 29 to 54 in rotor) | Under Amish's standing instruction of 2026-10-23 | CAR-DDR-003 |
| 2026-11-12 | F2: UV-C LED strip removed from every option (0.003 mJ/cm2, 1 % single pass; eye limit in 7 to 11 min at 1 m) | Under the standing instruction | CAR-DDR-003 |
| 2026-11-12 | F3: hold-down straps cross the solid fan frame 261 mm from the centre, not the outlet guard | Under the standing instruction | CAR-DDR-003 |
| 2026-11-12 | Design for construction of CA2 (tray and deck instead of tape, deck gasket, feet) | Under STANDARDS section 18 (Amish, 2026-09-30) | CAR-DDR-002 |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.

---
doc_id: CAR-PRC-001
title: CleanAir Retrofit Kit design precis
project: CleanAir Retrofit Kit
doc_type: Precis
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First precis for the carried option CA2 (filter cube), with the team's CA1 as the alternative awaiting Amish
---

# CleanAir Retrofit Kit design precis

The kit turns a fan a facility already has into a room air cleaner designed to reduce airborne particles. The carried design (option CA2) stands four standard 20 x 20 x 2 in MERV-13 panels in a folded polypropylene tray, closes the top with a fan deck and a foam gasket, and puts an existing 20 in box fan on the deck to draw room air in through all four panels. It is tool-free, costs USD 111.83 in parts against the USD 150 target (fan excluded), and is designed to give one 60 m3 clinic room about 6.6 to 7.6 eACH, or a 150 m3 ward 5.3 to 6.1 eACH with two cubes, on measured data for four-panel cubes (CAR-CAL-001). The choice between CA2 and the team's collar and cassette (CA1) is **proposed, awaiting Amish**: their scores are within 10 % (CAR-OPT-001, CAR-DEC-001 D1). CONCEPT, NOT FOR FABRICATION.

## How it works

The box fan sits on the deck blowing up. It lowers the pressure inside the cube by 9 to 34 Pa; room air enters through the four panel faces at 0.20 to 0.65 m/s, leaves its particles on the pleated media, rises through the open cube and the 480 mm deck opening, and leaves upward through the fan. Spreading the flow over 0.98 m2 of media keeps the drop within the 27 to 55 Pa a box fan can develop, which a single flat panel on the fan face does not (CAR-STM-001 X1). A foam gasket seals the fan frame to the deck; the tray and deck flaps cap the panel edges, and corner angles held by two straps close the vertical seams. Two more straps pass over the solid fan frame and under the tray.

## Main components

| # | Component | Made or bought | Material |
| --- | --- | --- | --- |
| 1 | MERV-13 panel, 20 x 20 x 2 in nominal (4) | Bought | Synthetic pleated media, card frame |
| 2 | Base tray | Made: cut, scored, folded | 4 mm corrugated PP |
| 3 | Fan deck with 480 mm opening and 280, 380 mm cut lines | Made: cut, scored, folded | 4 mm corrugated PP |
| 4 | Corner angle (4) | Made from offcuts | 4 mm corrugated PP |
| 5 | Cam strap with buckle (4) | Bought | Polyester webbing |
| 6 | Deck gasket | Bought | EPDM foam weatherstrip |
| 7 | Foot (4) | Made: printed | PP |
| 8 | M5 bolt set (4) | Bought | Zinc-plated steel |
| 9 | Instruction and warning label | Bought | Vinyl |
| none | Box fan, 20 in | The facility's own | Not in the kit |

## Changes from the team concept (iteration 2)

- Option CA1 (silicone collar, PP snap ring, one flat MERV-13 cassette) is kept as an option, modelled at D3 and scored; it is not dropped. Its weakness is airflow through one panel (X1, X2).
- Ceiling fans are out of scope (fix F1); the UV-C strip is removed (fix F2). Both decided under Amish's standing instruction of 2026-10-23.
- The runner-up's best idea is grafted onto CA2: the deck carries cut lines for 12 and 16 in round fans, and the team's silicone collar is the proposed adaptor for them (CAR-DEC-001 D2).
- HEPA-grade media (an EN 1822 class such as H13), named in the deck as optional, is not used in the prototype: its resistance is higher than MERV-13 media and a box fan develops only 27 to 55 Pa, so its delivered airflow on this fan is to assess before it is offered; MERV-13 remains the bought rating.

## First-order numbers (CAR-CAL-001)

- Measured CADR of four-panel cubes: 398 to 459 m3/h on high, about 280 m3/h on low.
- Model airflow 712 to 2,277 m3/h; drop 9 to 34 Pa; bypass 3.7 to 8.2 % with 1 mm gaps.
- Mass 4.4 kg (7.7 kg with the fan); 576 mm across the buckles, 639 mm high; tips at 28 deg.
- Power 52.8 to 103 W on high (the fan's); 587 to 858 kWh a year at 24 h.
- Kit parts USD 111.83; panels about USD 108 a year.

## Safety

> **Safety:** The kit is used only with a fan listed to UL 507 or IEC 60335-2-80 with guards on both faces, on the floor, with its cord routed away from walkways. Never remove a guard, never run the fan with a strap or anything else touching the blades, and unplug before changing panels. The cube is combustible: keep it 1 m from heaters, flames and oxygen outlets. Change panels with gloves and bag them at the cube. The kit has no UV-C, ioniser or ozone source. It does not replace ventilation, masks or other infection prevention and control measures.

## Release limitation

No prototype is used to protect occupants until its delivered airflow, seal and filtration efficiency are measured by a qualified laboratory (STANDARDS 25.5a; CAR-CLM-001).

## Open questions

Decisions and items to confirm are in the design decisions register (CAR-DEC-001).

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.

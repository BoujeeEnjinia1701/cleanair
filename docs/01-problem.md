---
doc_id: CAR-PRB-001
title: CleanAir Retrofit Kit problem statement
project: CleanAir Retrofit Kit
doc_type: Problem statement
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First problem statement from the Helpful Engineering project update (iteration 2), with cited burning platform, users, personas, constraints and kill criteria
---

# CleanAir Retrofit Kit problem statement

Field hospitals, emergency shelters, clinics and communal spaces often have fans and duct openings but no filtration, and replacing their ventilation is rarely feasible in cost, time or logistics. Facility managers need a low-cost way to add clean air delivery, counted in air changes per hour, from what is already on site. This statement draws on the Helpful Engineering project update for the CleanAir Retrofit Kit (concept iteration 2) and is a proposal for review with a co-design partner.

## Burning platform

- CDC asks building operators to "aim for 5 or more air changes per hour (ACH) of clean air", counting ventilation and filtration (equivalent ACH) together, as a goal rather than a hard rule ([CDC, Aim for 5](https://cdc.gov/niosh/ventilation/prevention/Aim-for-5.html), checked 2026-11-12).
- The Lancet COVID-19 Commission proposed non-infectious air delivery rates of 4 ACHe (good), 6 ACHe (better) and above 6 (best), or 10, 14 and above 14 L/s per person ([Lancet Commission task force, November 2022](https://healthybuildings.hsph.harvard.edu/wp-content/uploads/2024/09/LANCET-November-2022-Proposed-Non-infectious-Air-Delivery-Rates-for-Reducing-Exposure-to-Airborne-Respiratory-Infectious-Diseases-3.pdf), checked 2026-11-12).
- For a 50 m2 ward 3 m high (150 m3), 5 ACH means 750 m3/h of clean air; for a 20 m2 clinic room (60 m3), 300 m3/h (CAR-CAL-001).
- A box fan with four MERV-13 panels (a Corsi-Rosenthal type cube) cut airborne MS2 virus in a 3,000 ft3 EPA chamber by 97 % in 30 minutes and 99.4 % in 60 minutes, with a CADR of 234 cfm ([EPA ORD results summary](https://today.uconn.edu/wp-content/uploads/2023/10/EPA-ORD-CR-Box-Bioaerosol-Results-embargoed-10-30-23-11am-est.pdf), checked 2026-11-12): low-cost filtration is measurable and meaningful, but it has to be built well.
- A single filter taped to a box fan delivered only 142 to 154 cfm against 443 to 500 cfm for the same fan on a four-filter cube ([UC Davis WCEC case study, 2021](https://energy.ucdavis.edu/wp-content/uploads/Case-Study_DIY-Portable-Air-Cleaners-083121.pdf), checked 2026-11-12): how the filter meets the fan decides most of the result.

## Users and context

Table 1. Users and needs.

| User | Context | Need | Persona |
| --- | --- | --- | --- |
| Facility manager | Field hospital, shelter or clinic with existing fans or ducts | Raise clean air delivery to a stated ACH with parts they can buy locally, without new HVAC | P1 |
| Healthcare worker | Ward or clinic room, busy, gloved | Kit that stands where put, does not tip, needs no attention between filter changes | P2 |
| Humanitarian operator (logistics) | Ships kits with other relief items | Flat pack, standard consumables, low cost per unit and per year | P3 |
| Occupants (patients, staff, displaced people) | Crowded, enclosed rooms for long hours | Lower airborne particle exposure; tolerable noise; no new hazard | P4 |
| Maintenance volunteer | Local, minimal training | Assemble and change filters without tools, with pictures | P5 |

### Personas

- **P1 Amara, shelter manager.** Runs a school gym used as a shelter for 120 people; six 20 in box fans on site; no ducts. Wants one figure: how many kits per room.
- **P2 Jonas, ward nurse.** Works 12 hour shifts in a tented field ward of about 50 m2; carts and beds move constantly. Will not tolerate anything that tips or rattles.
- **P3 Lina, logistics officer.** Packs relief kits by volume and weight; resupply of consumables is the usual failure point.
- **P4 Mr. Okafor, patient.** Sleeps in the ward; noise at night matters.
- **P5 Sam, volunteer.** Handy, no tools beyond a knife; reads pictures before words.

### Stakeholders

Table 2. Stakeholders.

| Stakeholder | Interest | How they shape the design |
| --- | --- | --- |
| Helpful Engineering (project team) | Open, low-cost hardware for crisis settings | Source deck, decision gate, volunteer support |
| Design Molecule Labs | Constructable open design at TRL 3 | Kit standards, documentation |
| Field partners (for example UNHCR, MSF, named in the deck as partners to explore) | Fan inventories, deployment rules | Fan types and rooms to design for (to engage) |
| FEMA (named in the deck) | Viability input | Review of deployment cases (to engage) |
| Filtration test laboratory | Measured CADR | Verification at TRL 4 (CAR-VER-001) |
| Funders (the deck cites rural health funding) | Cost per unit and per year | Value-engineering target |

## Constraints

- Uses fans and duct openings already on site; adds no permanent infrastructure (team deck).
- Value-engineering target USD 150 per complete kit, stretch under USD 80 at volume (team deck).
- Standard, locally available filter media (MERV-13 cassettes, HEPA-grade optional per the deck).
- Tool-free assembly in under 15 minutes; cassette swap under 2 minutes (team deck).
- Wipe-clean with standard disinfectants (team deck).
- Fans from 12 to 24 in (305 to 610 mm) across (team deck).

## Out of scope

- Replacing ventilation: the kit complements outdoor air, never replaces it.
- Ceiling fans: unshrouded rotors cannot be sealed to (CAR-STM-001 X3, CAR-DEC-001 F1).
- UV-C, ionisers or any other air treatment (CAR-DEC-001 F2).
- Any clinical or infection outcome claim (CAR-CLM-001).

## Prior work

- Corsi-Rosenthal boxes: measured by Dal Porto et al. (2022), UC Davis (2021), UL Chemical Insights (2021) and EPA ORD (CAR-CAL-001).
- Commercial portable air cleaners and kits (CAR-MKT-001).
- Team iteration 1 (bespoke housing for HEPA-class media, aluminium ring), dropped on cost; iteration 2 (silicone collar, PP snap ring, MERV-13 cassette, optional UV-C strip), option CA1 here.

## Kill criteria (project stop rules, not a product claim)

The project stops or changes course if any of these holds at TRL 4:

- A measured CADR below 300 m3/h for one kit on a typical site fan (half the ward's need for two units).
- Bypass at the seals above 15 % of airflow that cannot be fixed without tools.
- Fan motor temperature above its listing limit with the kit fitted.
- Kit parts above USD 150 with no route to the target.
- Field partners report that filter resupply cannot be met.

## User research and co-design

Every target here is a proposal until tested with a field partner: rooms, fans on site, noise tolerance, filter change interval and who pays for filters.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.

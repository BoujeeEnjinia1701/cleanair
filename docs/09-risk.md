---
doc_id: CAR-RSK-001
title: CleanAir Retrofit Kit risk register and hazard analysis
project: CleanAir Retrofit Kit
doc_type: Risk register
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis and design FMEA for option CA2
---

# CleanAir Retrofit Kit risk register and hazard analysis

The largest risks are a kit that delivers less clean air than people believe (silent loss of performance from loading, bypass or low speed) and a false sense of protection. Controls are honest claims, a change point, a label and laboratory measurement before use. Likelihood and impact 1 (low) to 5 (high).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Measured CADR below 400 m3/h | Weak local fans, low in-use efficiency | More cubes per room; PR-001 not met | 3 | 3 | Test lead | Measure (V2); plan by measured CADR; D4 fifth panel |
| P2 | Filters not replaced | Resupply, cost, busy staff | Flow falls by a half or more unnoticed | 4 | 4 | Field partner | Label with change interval, ribbon check, panels bought by the case |
| P3 | Fan listing does not cover the use | Fan run flat with filters | Liability, withdrawal | 3 | 4 | Safety lead | Ask fan makers (C3); motor temperature test (V5) |
| P4 | Patent conflict | US 12,582,929 B2 | Redesign or licence | 2 | 3 | Project lead | Attorney opinion (C5); keep no hinged tabs |
| P5 | Overclaiming by users or partners | Air cleaners are often sold with health claims | Misuse, regulatory exposure | 3 | 4 | Project lead | CAR-CLM-001 wording on the label and materials |
| P6 | Decision on D1 delayed | Scores within 10 % | Schedule | 3 | 2 | Project lead | Decision request in CAR-PLN-001 |

## Preliminary hazard analysis

Table 2. Hazards. Severity and likelihood 1 to 5.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Fan blade contact | Guard removed or pressed in | Finger injury | 3 | 1 | Guards untouched; straps on the frame (F3); label | Low |
| H2 | Electrical shock or fire from the fan | Damaged cord, overheating | Burns, fire | 5 | 1 | Listed fan only; cord check; motor temperature test V5 | Low |
| H3 | Fire spread | Combustible panels and PP near a heat source | Fire | 5 | 2 | 1 m from heaters, flames and oxygen outlets; UL 900 panels and FR sheet asked for (C2) | Medium |
| H4 | Tip-over | Bumped by a cart (27 N tips it) | Bruising, trip, fan damage | 2 | 3 | Floor only, out of walkways, against a wall where possible | Medium |
| H5 | Trip over the cord or straps | Cord across a walkway | Fall | 3 | 2 | Cord routed to the back, along walls | Low |
| H6 | False sense of protection | Kit seen as a substitute for ventilation or masks | Higher exposure | 4 | 3 | Claims register; label "not a substitute for ventilation" | Medium |
| H7 | Exposure during a filter change | Dust release from loaded panels | Inhaled particles | 3 | 2 | Gloves, bag at the cube, fan off | Low |
| H8 | UV-C exposure or ozone | Optional module of the team concept | Eye injury, ozone | 4 | 1 | Module removed (F2); no active stage | None |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection (each 1 to 10).

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | MERV-13 panels | Capture particles | Loaded beyond the change point | CADR falls 40 to 70 % silently | No change interval kept | 7 | 6 | 7 | 294 | Ribbon check, dated label, PR-021 change point from V4 |
| F2 | Deck gasket | Seal fan to deck | Gap after a knock | Bypass 5 to 15 % | Fan slid on the foam | 5 | 4 | 6 | 120 | Hold-down straps; tissue check at each change |
| F3 | Corner strips and straps | Close vertical seams | Strap slack | Seam bypass | Strap creep | 5 | 4 | 5 | 100 | Re-tension at each change; mark strap position |
| F4 | Panel card frames | Hold shape | Sag in humidity | Seam gaps, panel collapse | Damp card | 5 | 4 | 4 | 80 | Check at each change; moisture-resistant frames asked for |
| F5 | Fan | Move air | Run on low or stopped | CADR 280 m3/h or none | Noise, switch-off | 6 | 5 | 6 | 180 | Label; D7 speed rule; plan units for the speed used |
| F6 | Fan motor | Run continuously | Overheating flat | Fire risk | Orientation not covered by listing | 9 | 2 | 6 | 108 | V5 motor test; C3 maker's statement |
| F7 | Tray | Hold panels | Score cracks through | Flap loss, seam gap | Score too deep | 4 | 3 | 3 | 36 | Score depth 1 mm, top skin only; replace tray |
| F8 | Feet bolts | Hold feet | Bolt pulls through sheet | Foot loss, rocking | Overtightening | 3 | 3 | 3 | 27 | Washer under the head; hand tight plus a quarter turn |
| F9 | Label | Instruct | Missing or unread | Misuse | Label removed | 5 | 4 | 5 | 100 | Print the key rules on the deck flap itself at scale |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.

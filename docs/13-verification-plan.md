---
doc_id: CAR-VER-001
title: CleanAir Retrofit Kit verification plan
project: CleanAir Retrofit Kit
doc_type: Verification plan
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First verification plan, TRL 4 test families on paper only
---

# CleanAir Retrofit Kit verification plan

Planned TRL 4 verification on paper. Nothing here is run at TRL 3. Method: STANDARDS section 25.7. The team's decision gate (evidence that the seal and filtration meet minimum thresholds) is passed by V2, V4 and V5 together.

Table 1. Test families.

| Family | Method and observations | Evidence needed for the gate | Solutions | Requirements |
| --- | --- | --- | --- | --- |
| V1 Airflow | Flow hood or velocity traverse at the fan outlet, clean panels, low and high speed, three fans | Airflow in m3/h against the CAR-CAL-001 bracket | CA2 (CA1 if chosen) | PR-001, PR-019 |
| V2 CADR | Chamber decay to the AHAM AC-1 method as a benchmark, with an optical particle counter in size bins 0.3 to 1, 1 to 3 and 3 to 10 um; four and five panels side by side (D4) | CADR at least 400 m3/h for 0.3 to 1 um on high | CA2 | PR-001, PR-005 |
| V3 Room | Two cubes in a 150 m3 room and one in a 60 m3 room; decay of a particle challenge at three points | eACH against 5; mixing | CA2 | PR-002, PR-003 |
| V4 Seal and loading | Smoke pencil and tissue at every seam; pressure inside the cube; flow with panels loaded to 2.6 and 7.3 times initial resistance | Bypass 10 % or less; the change point at 60 % of clean flow | CA2 | PR-006, PR-021 |
| V5 Motor | Motor and winding temperature with thermocouples, fan flat, 8 h, clean and loaded panels, at 120 V and 230 V fans | Below the fan's listing limits | CA2 | PR-010, PR-019 |
| V6 People | Timed assembly and panel change by the personas; 10 deg tilt | 15 min assembly; filter change against D3; no tip | CA2 | PR-007, PR-008, PR-012, PR-022 |
| V7 Fit | Fit on five fan models (box, pedestal, wall), including the round-fan cut lines and the collar adaptor (D2) | Gaps under 1 mm | CA2, CA1 | PR-004 |
| V8 Environment and noise | 7 days at 35 C and 90 % RH; 50 wipe cycles with 70 % alcohol and 0.5 % hypochlorite; sound level at 1 m on each speed | Shape held; no cracking; dBA recorded against PR-018 | CA2 | PR-014, PR-017, PR-018 |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.

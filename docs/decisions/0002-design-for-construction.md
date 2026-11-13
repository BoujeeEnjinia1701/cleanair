---
doc_id: CAR-DDR-002
title: "0002: Design for construction"
project: CleanAir Retrofit Kit
doc_type: Decision record
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: Constructability changes to CA2 under STANDARDS section 18
---

# 0002: Design for construction

Status: made under STANDARDS section 18 (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). These changes keep what the concept does.

## Changes

| Concept | Constructable design | Why |
| --- | --- | --- |
| Panels taped into a cube | A tray and deck of scored and folded 4 mm corrugated PP that cap the panel edges; four folded corner strips over the vertical seams; two horizontal straps | Tool-free panel change; seams stay closed; no tape residue on reusable parts |
| Fan resting on the panel edges | Deck with a 480 mm opening and an EPDM foam square under the fan frame | The panel tops are not flat and the fan frame corners leak |
| No way to hold the fan | Two straps over the solid fan frame and under the tray | The fan must not slide off when the cube is bumped |
| Tray on the floor | Four printed 15 mm feet, bolted with M5 x 20 bolts | Path for the straps under the tray |
| Deck for one fan size | Cut lines at 280, 380 and 480 mm | Round fans (D2) |

Every part is cut, scored and folded by hand, printed, or bought; no part needs tooling at prototype scale. The model (`cad/src/model.py`) passes the D3 fidelity check with no interference.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.

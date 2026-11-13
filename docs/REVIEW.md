# CleanAir Retrofit Kit review note

**Media completed, 2026-11-12.** The Blender Cycles renders queued by this session were rendered on Amish's Mac: `media/options.png`, `media/render-hero.png`, `render-studio.png`, `render-cutaway.png` and `render-exploded.png` were composed and captioned, `media/card.png` and `media/social-preview.png` were made with `cards.py`, and `image_qc.py` passes. `render.py --check` passes. `release_gate.py` fails only on `stem_check: open` (Plausible rows wait on TRL 4 evidence; design decisions await Amish). Amish approved the repo as public on 2026-11-12.

## Session 2026-11-12: P0 to P3 (TRL 3) under kit 1.9.1-he

### What was done

- STEM check first ([docs/01b-stem-check.md](01b-stem-check.md), `docs/04-calcs/stem_check.py`, `stem_results.csv`, `stem_results_options.csv`) with the air checks of STANDARDS 25.6a, then an independent review by a separate agent (its own process, given only the claims, sources and assumptions).
- Three concept options at D3 in `cad/src/model.py` (CA1 36 parts, CA2 44, CA3 26; `cad/fidelity.json` passes D3, no interference); STEP per part for CA2 in `cad/step/CA2/` and an assembly STEP per option (11 MB in all).
- Pipeline documents: PRB, STM, PRC, OPT, URS, PRS, RTM (generated, 0 gaps), CAL with `sizing.py`, BLD with pictures, DEC with DDR 0001 to 0003, REG, FEA, RSK (PHA and design FMEA), MKT, PLN (HE process content), CLM, VER, FTO.
- Drawings CAR-DWG-001 (GA) and 002 (half section); making sketches CAR-DWG-101 to 104; STL in `cad/stl/`; concept media in `media/` (hero, cutaway, exploded, flow, viewer, blueprint).
- `cad/src/product_model.py`; render queue in `/home/claude/he5/renderq/cleanair` (`cleanair__options_jobs.json` and three option scenes) and `/home/claude/he5/renderq/cleanair/views` (`cleanair__jobs.json`, four views).
- `project.yaml` filled to P3, TRL 3, `stem_check: open`, `design_state: constructable`.

### Key results (CAR-CAL-001)

- Box fan shut-off 27 to 55 Pa. CA2 (four panels, 0.98 m2): 9 to 34 Pa, 0.20 to 0.65 m/s. CA1 (one panel): would need 133 to 215 Pa at free-air velocity; settles at 13 to 71 % of free air.
- Measured design basis: four-panel cubes 398 to 459 m3/h CADR on high, about 280 on low; one filter on a box fan 131 to 141 m3/h.
- Ward 150 m3: two cubes 5.3 to 6.1 eACH (CA1 would need six kits). Clinic room 60 m3: one cube 6.6 to 7.6 eACH.
- Bypass at 1 mm gaps: CA2 3.7 to 8.2 %; CA1 up to 31 % at 5 mm round a box fan face.
- UV-C: low-cost strip 0.003 mJ/cm2 (1 % single pass); removed.
- Kit 4.4 kg, 7.7 kg with the fan; tips at 28 deg; 576 mm across, 639 mm high.
- Value-engineering target USD 150; estimated cost of the constructable design USD 111.83 (USD 38.17 under), fan excluded; USD 135.32 with a new box fan. Stretch target under USD 80 at volume not met on paper (panels alone USD 54).

### Requirements not met or at risk

- PR-001 CADR at least 400 m3/h: at risk (measured four-panel cubes 398 to 459).
- PR-008 filter change under 2 minutes: not met on paper for the whole set (4 to 6 min); target to Amish (D3).
- PR-004 round fans: at risk until the fit test.
- PR-007, PR-014, PR-017, PR-018, PR-021: to verify at TRL 4.

### STEM check

CA2: 16 within, 15 plausible (need TRL 4 evidence), 1 fails with a fix that goes to Amish (S18). Options: 7 within, 6 plausible, 1 fails with a fix noted (X12, CA3, not carried). Fixes under the standing instruction of 2026-10-23: F1 ceiling fans out of scope, F2 UV-C strip removed, F3 hold-down straps on the fan frame. Independent review: of 24 rows marked within, 9 held, 14 weak, 1 refuted (S19, clean air per watt); 12 missed claims, added as S25 to S32; all findings recorded in CAR-STM-001.

### Decisions proposed and awaiting Amish (CAR-DEC-001)

- D1 concept: CA2 185, CA1 170, CA3 166 of 245; CA2 and CA1 within 10 %, both to Amish without a pick. CA2 carried in the drawings, BOM and build plan only so a constructable design exists. Choosing CA2 changes the pitch from "clip-on collar" to "filter cube kit".
- D2 round fans on CA2 (cut lines now; collar adaptor after a fit test).
- D3 filter-change target per panel or per set.
- D4 four or five panels. D5 no air treatment beyond filtration (a UV-C module would be a separate product). D6 fan supply. D7 speed at night.
- On-product wording in CAR-CLM-001.

### Build plan findings (design for construction, CAR-DDR-002)

Tape replaced by a folded tray and deck that cap the panel edges, corner strips and straps; deck gasket under the fan frame; feet so the hold-down straps pass under the tray; straps moved onto the fan frame (F3).

### Safety concerns

False sense of protection (claims and label); filters left to load (FMEA RPN 294, the top item); fan listing coverage when run flat with filters (C3); combustible panels and sheet (C2); tip-over at 27 N (floor only). No UV-C or ozone source remains.

### Appearance model

`product_model.py` uses the CA2 parts as modelled plus a standing 1.75 m mannequin and a half-cut copy; no appearance deviations from `model.py`. The box fan is a simplified context model of a 20.5 x 21.75 x 4.25 in fan (listing dimensions), not a specific product. Proposed, awaiting Amish: none.

### Checks that do not pass, and kit notes

- `python .kit/render.py --check` fails only on `media/options.png`, which needs the Blender renders of the exported option scenes; the storefront warning lists `media/render-hero.png`, `media/card.png` and `media/social-preview.png`, also Blender-dependent. After the Mac renders: `python .kit/options.py --compose=<dir>`, caption the views with `.kit/photo_caption.py`, then `python .kit/cards.py .` and `python .kit/image_qc.py`.
- Corrugated twin-wall PP is modelled as solid 4 mm sheet with the flute direction noted (mass corrected in CAL with an assumed 0.75 kg/m2); the foam gasket uses solid EPDM density.
- The fan curve is fitted, not a published curve: no measured box fan pressure-flow curve was found; it is built from two measured operating points and the fan laws, and every flow is shown as a range.

### Recommended next step

Amish decides D1 (and D3). The design is ready for TRL 4 on paper: three kits, a five-fan fit test, laboratory CADR and bypass, and a flat-running motor temperature test (CAR-VER-001), once the portfolio cap allows.

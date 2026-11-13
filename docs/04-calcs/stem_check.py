"""CleanAir Retrofit Kit: STEM check calculations (CAR-STM-001, STANDARDS sections 20 and 25.6a).

Run from the repo root:  python docs/04-calcs/sizing.py      (writes sizing_results.json)
                         python docs/04-calcs/stem_check.py  (writes stem_results.csv, stem_results_options.csv and
                                                              refreshes the two tables in docs/01b-stem-check.md)
Rows S1 to S24 check the recommended option CA2 (filter cube on a box fan). Rows X1 to X14 check the other options,
CA1 (the team's collar and cassette, iteration 2) and CA3 (return-grille cassette), including the two details of the
team concept that failed and were fixed under Amish's standing instruction of 2026-10-23 (CAR-DEC-001 F1, F2).
Sources and dates checked (2026-11-12) are listed in CAR-STM-001 and CAR-CAL-001.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
from stem_check import Check, WITHIN, PLAUSIBLE, FIX, FAILS  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
R = json.loads((ROOT / "docs/04-calcs/sizing_results.json").read_text())
CAL = "CAR-CAL-001"
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
x = Check(ROOT / "docs/04-calcs/stem_results_options.csv")
A = R["ach"]
LK = R["leak"]

# ---- Physics: fluid mechanics (fan curve against media, STANDARDS 25.6a) -------------------------------------------
REV = "independent review 2026-11-12"
c.cited("S1", f"A 20 in box fan develops only about {R['PMAX_range'][0]:.0f} to {R['PMAX_range'][1]:.0f} Pa at shut-off",
        "Physics", "Fluid mechanics", "Quadratic fan curve fitted to Dal Porto et al. 2022 (12 % flow loss at 6.2 Pa, low speed); fan laws "
        "(pressure scales with speed squared) with the 1.42 high-to-low CADR ratio as the speed ratio (A2)",
        "27.5 Pa at low speed, about 55 Pa at high speed; a quadratic curve has no stall dip, so flows near shut-off are optimistic "
        f"({REV}: S1 weak, low-speed point applied to high-speed flows; fixed by carrying both)", WITHIN, closed_by=f"{CAL} section 3")
cs = R["cases"]
c.cited("S2", f"Four panels (0.98 m2 of face) let a box fan deliver {R['CA2_Q'][0]:.0f} to {R['CA2_Q'][1]:.0f} m3/h (model, clean) at "
        f"{R['CA2_dP'][0]:.0f} to {R['CA2_dP'][1]:.0f} Pa and {R['CA2_v'][0]:.2f} to {R['CA2_v'][1]:.2f} m/s face velocity",
        "Physics", "Fluid mechanics", "Fan curve against linear media resistance (Parker 38.2, Global Industrial 62.1 Pa per m/s; A3); "
        "UC Davis measured 443 to 500 cfm (753 to 850 m3/h) through a four-filter cube",
        "The measured airflow sits at the model's low end; linear extrapolation overstates media resistance at low velocity (UC Davis "
        f"estimate 5 to 7.5 Pa against 9 to 15 Pa modelled) and the upper end exceeds every measurement ({REV}). Design figures use "
        "measured CADR (S3), the model only brackets", PLAUSIBLE)
c.cited("S3", f"One four-panel cube on high gives a clean air delivery rate of about {R['CA2_meas_CADR_m3h'][0]:.0f} to {R['CA2_meas_CADR_m3h'][1]:.0f} m3/h",
        "Physics", "Fluid mechanics", "Four-panel CR boxes: EPA ORD MS2 virus aerosol CADR 234 cfm (398 m3/h); UC Davis 239 to 270 cfm "
        "(406 to 459 m3/h, from a 54 % efficiency rating); Dal Porto et al. 2022 five-panel cube 1,020 to 1,450 m3/h as a reference only",
        f"PR-001 targets at least 400 m3/h, which the lowest four-panel measurement (398) just misses; no measured size-resolved 0.3 to 3 um "
        f"CADR exists for a four-panel cube, so V2 is the gate ({REV}: S3 weak, five-panel data removed from the CA2 range)", PLAUSIBLE)
c.cited("S4", "MERV-13 media keeps about 40 to 50 % single-pass efficiency for 0.3 to 1 um at the cube's low face velocity",
        "Physics", "Fluid mechanics", "ASHRAE 52.2 MERV-13 minimums E1 50 %, E2 85 %, E3 90 % (NAFA guide); in use Dal Porto et al. 2022 "
        "found an effective 41 to 58 % and EPA's CADR of 234 cfm on 560 to 605 cfm implies 39 to 42 %",
        f"Face velocity {R['CA2_v'][0]:.2f} to {R['CA2_v'][1]:.2f} m/s, below the 1.5 to 2.5 m/s at which panels are rated; humidity can "
        "discharge electret media; in-situ efficiency is measured, not assumed", PLAUSIBLE)
c.cited("S5", f"In a 50 m2 x 3 m ward (150 m3) one cube gives {A['CA2 measured | ward 50 m2 x 3 m']['ACH'][0]:.1f} to "
        f"{A['CA2 measured | ward 50 m2 x 3 m']['ACH'][1]:.1f} eACH, so CDC's 5 ACH needs 2 cubes and Lancet 'better' 6 ACHe 2 to 3",
        "Mathematics", "Units and dimensional analysis", "eACH = CADR / room volume (well mixed); CDC aim for 5 ACH of clean air, adding "
        "ventilation and filtration; Lancet Commission NADR good 4, better 6 ACHe",
        f"750 m3/h for 5 ACH; two cubes give 795 to 917 m3/h (5.3 to 6.1 eACH) clean; existing ventilation adds to it ({REV}: corrected "
        "from 1 to 2 cubes)", WITHIN, closed_by=f"{CAL} section 6; PR-002")
c.cited("S6", f"In a 20 m2 x 3 m clinic room (60 m3) one clean cube on high gives {A['CA2 measured | clinic room 20 m2 x 3 m']['ACH'][0]:.1f} to "
        f"{A['CA2 measured | clinic room 20 m2 x 3 m']['ACH'][1]:.1f} eACH, above CDC 5 ACH and Lancet 6 ACHe",
        "Mathematics", "Units and dimensional analysis", "eACH = CADR / room volume", f"300 m3/h for 5 ACH; 360 m3/h for 6. On low speed "
        f"(UC Davis 163 to 165 cfm) {R['CA2_low_speed_CADR_m3h'][0] / 60:.1f} eACH, and with loaded panels 5 ACH is not assured, so the change "
        f"point is set by PR-021 ({REV})", WITHIN, closed_by=f"{CAL} section 6; PR-003, PR-021")
c.claim("S7", "A 1 mm gap at the deck gasket, the four corner seams and the tray seam lets less than 10 % of the air bypass the media",
        "Physics", "Fluid mechanics", "Orifice leak Q = 0.6 A sqrt(2 dP / rho) in parallel with the media; 6.2 m of seam; worst case over both "
        "fans, both shut-off pressures and both media", round(LK["CA2 gap 1.0 mm"]["bypass_share"] * 100, 1), 10.0, "%",
        closed_by=f"{CAL} section 7 (best case {LK['CA2 gap 1.0 mm']['bypass_min'] * 100:.1f} %; 2 mm worst {LK['CA2 gap 2.0 mm']['bypass_share'] * 100:.0f} %); "
                  f"smoke-pencil check at TRL 4; {REV} added the tray seam")
c.cited("S8", f"Loaded panels cut the airflow to {R['CA2_loaded_Q'][0]:.0f} to {R['CA2_loaded_Q'][1]:.0f} m3/h at 2.6 times initial resistance, "
        f"and to {R['CA2_heavy_Q'][0]:.0f} to {R['CA2_heavy_Q'][1]:.0f} m3/h at 7.3 times", "Physics", "Fluid mechanics",
        "Parker final resistance 1.0 in w.g. against 0.39 initial; UL Chemical Insights dust-loaded filters 2.0 in w.g. against 0.274 clean",
        "The fan's low pressure makes the cube sensitive to loading; a change interval is set from a loaded-flow test, not assumed (A7)", PLAUSIBLE)
c.cited("S9", "The added filter load does not raise motor current, and winding temperature stays below the insulation rating",
        "Engineering and technology", "Power and link budgets", "UL Chemical Insights report 200 (2021): five box fans, 0.4 to 0.9 A, "
        "52.8 to 97.8 W, current unaffected by filter condition; highest winding 92 C against 105 C (Class A); no ignition in 7 h blocked",
        f"Listing standards set measured limits below the 105 C class rating, so 92 C may sit near a limit; the tests had the fan upright, "
        f"the cube lays it flat (S25). Use only fans listed to UL 507 or IEC 60335-2-80 with thermal protection; check per model (V5; {REV})",
        PLAUSIBLE)
c.cited("S10", "The kit adds no electrical part; the fan's own listing (UL 507 or IEC 60335-2-80) carries the electrical safety case",
        "Engineering and technology", "Standards practice", "UL 507 (electric fans); IEC 60335-2-80:2024 (fans)",
        "Whether a listing still covers a fan run with filters strapped to it is to assess with a listing body; the UL report found "
        "no hazard in 7 h fully blocked", PLAUSIBLE)
c.cited("S11", "The cube emits no ozone: it has no UV lamp, ioniser or electrostatic stage",
        "Chemistry", "Environmental and atmospheric chemistry", "Ozone forms from oxygen below about 240 nm (Luminus note) or in corona "
        "discharge; UL 2998 benchmark under 0.005 ppm; CARB limit 0.050 ppm (UL 867 method)",
        "Mechanical filtration only; UL 2998 is a benchmark to cite, not a pass, until tested", WITHIN, closed_by="CAR-DEC-001 F2; PR-009")
c.cited("S12", "Filtration lowers the airborne particle concentration that carries respiratory viruses; it does not by itself prevent infection, so only CADR is claimed",
        "Biology", "Epidemiology", "EPA ORD chamber test: CR boxes cut airborne MS2 by 97 % in 30 min and 99.4 % in 60 min in 3,000 ft3; "
        "CDC presents ACH as one layer of risk reduction, a goal not a hard rule",
        "Claims limited to particle CADR and eACH (CAR-CLM-001); no infection outcome is claimed", WITHIN, closed_by="CAR-CLM-001")
m = R["ca2_mass"]
c.cited("S13", f"The cube with its fan ({m['total_kg']:.1f} kg) stands on a 10 deg incline and needs about {m['push_at_top_N']:.0f} N at the top to tip",
        "Physics", "Mechanics and statics", "Tipping about the feet: tan(angle) = half base / centre of gravity height; 10 deg incline as in household "
        "appliance stability tests (IEC 60335-1 clause 20.1, to confirm against the current edition)",
        f"Tip angle {m['tip_angle_deg']:.0f} deg against 10; {m['push_at_top_N']:.0f} N is a bump, not a lean, so it stands on the floor, "
        "never on a table, away from walkways or tied to a fixed object (PR-012)", PLAUSIBLE)
c.claim("S14", "The cube with its fan weighs under 10 kg, a one-person carry", "Mathematics", "Units and dimensional analysis",
        "Model volumes x densities; panels 0.68 kg (A11); twin-wall sheet 0.75 kg/m2 (A10); fan 7.25 lb (listing)",
        round(m["total_kg"], 1), 10.0, "kg", closed_by=f"{CAL} section 9")
c.claim("S15", "The assembled cube passes a 700 mm door and the kit packs flat", "Engineering and technology", "Standards practice",
        "Model envelope; two 610 x 914 mm sheets and four 44 mm panels", R["ca2_envelope_mm"]["width"], 700.0, "mm",
        closed_by=f"{CAL} section 9 (640 mm tall; flat pack about 0.05 m3)")
c.cited("S16", "The cube is combustible (card frames, synthetic media, PP sheet) but adds no ignition source; fire behaviour is to rate",
        "Chemistry", "Materials and polymer chemistry", "UL Chemical Insights report 200: no ignition with clean, smoke- or dust-loaded "
        "filters, motor housing 54 C at most; polypropylene burns",
        "Panels with a UL 900 classification from the supplier and flame-retardant sheet are asked for; keep 1 m from heaters and flames",
        PLAUSIBLE)
t = R["time_min"]
c.cited("S17", f"First assembly takes under 15 minutes (estimate {t['ca2_first_assembly'][0]} to {t['ca2_first_assembly'][1]} min)",
        "Biology", "Ergonomics", "Step count from the build plan: tray, four panels, four angles, two straps, deck, gasket, fan, two straps (A12)",
        "No tape, no tools; to time with the personas at TRL 4 (V6)", PLAUSIBLE)
c.cited("S18", f"A filter change takes under 2 minutes (the deck's cassette-swap target)", "Biology", "Ergonomics",
        "Step count (A12): release four straps, lift the fan and deck, swap four panels, refit",
        f"Whole set {t['ca2_filter_set_swap'][0]} to {t['ca2_filter_set_swap'][1]} min; one panel {t['ca2_one_panel'][0]} to "
        f"{t['ca2_one_panel'][1]} min. Not met on paper for the whole set; changing the target to read per panel changes a user-facing "
        "requirement, so it goes to Amish", FIX, closed_by="Proposed, awaiting Amish: CAR-DEC-001 D3")
e = R["energy_kwh_year"]
c.cited("S19", "A four-panel cube on a box fan gives about 4 m3/h of clean air per watt; a five-panel cube on a stronger fan about 15",
        "Mathematics", "Orders of magnitude", f"UC Davis four-filter: 239 to 270 cfm CADR on 102 to 103 W; EPA 234 cfm; Dal Porto five-panel 8.7 to "
        f"8.9 cfm per W; running 24 h a day {e[0]:.0f} to {e[1]:.0f} kWh a year",
        f"{R['CADR_per_W_CA2'][0]:.1f} to {R['CADR_per_W_CA2'][1]:.1f} m3/h per W ({REV}: the earlier 15 m3/h per W was refuted for four panels "
        "and corrected)", WITHIN, closed_by=f"{CAL} section 10")
c.claim("S20", "Kit parts cost no more than the USD 150 value-engineering target", "Mathematics", "Units and dimensional analysis",
        "Priced BOM (bom/bom.csv), cited prices checked 2026-11-12; the fan is excluded (the facility's own; a new box fan adds USD 23.49); "
        "filters recur at USD 54 a set (CAR-MKT-001)", round(R["bom_total"], 2), 150.0, "USD", closed_by="bom/bom.csv")
c.cited("S21", "The PP tray, deck and angles wipe clean with 70 % alcohol or 0.5 % sodium hypochlorite; the panels are replaced, not wiped",
        "Chemistry", "Materials and polymer chemistry", "Polypropylene resists dilute hypochlorite and alcohols (supplier chemical-resistance "
        "tables, to confirm for the bought sheet); pleated media and card are not cleanable",
        "Panels are consumables; wiping only the sheet parts; disinfectant contact time per the facility's IPC procedure", PLAUSIBLE)
c.cited("S22", "Card frames hold their shape in a humid field site", "Chemistry", "Materials and polymer chemistry",
        "Card loses stiffness when damp; synthetic media does not absorb water", "Corner angles and straps carry the panels; at high "
        "humidity check sag at each change; a moisture-resistant frame is asked of the supplier", PLAUSIBLE)
c.cited("S23", "The fan's own guards stay in place; the kit adds no pinch point at the blades", "Biology", "Human physiology and biomechanics",
        "Box fans have guards both sides; the deck and straps sit outside them", f"The two hold-down straps now cross the solid fan frame "
        f"at 261 mm from the centre, outside the 484 mm guard, so strap tension cannot push the guard into the blades ({REV}, fixed F3)", WITHIN,
        closed_by="CAR-DEC-001 F3; PR-011")
c.cited("S24", "CADR and eACH are first-order estimates; the fan-curve uncertainty on one box fan (rating against measurement) is a factor of about 3",
        "Mathematics", "Statistics and uncertainty", "Rated 1,800 cfm against 568 cfm derived from a measured cube", "Every flow is shown as "
        "a range with both fans and both media resistances; a unit is accepted only on a measured CADR", WITHIN, closed_by=f"{CAL} section 4")

# ---- claims the independent review found missing (2026-11-12) --------------------------------------------------------
c.cited("S25", "A box fan may run lying flat, blowing up", "Engineering and technology", "Standards practice",
        "Neither the UL report nor a fan listing covers this orientation (bearing load, motor cooling, controls on top)",
        "Most published CR boxes run this way; ask the fan maker and test motor temperature flat (V5)", PLAUSIBLE)
c.cited("S26", "On low speed, for quiet, a four-panel cube gives about 280 m3/h", "Physics", "Acoustics and vibration",
        "UC Davis four-filter cube speed 1: 163 to 165 cfm CADR, 70 to 71 W; noise not measured in the sources",
        f"Clinic room {R['CA2_low_speed_CADR_m3h'][0] / 60:.1f} eACH on low; noise in dBA at 1 m to measure (V8, PR-018)", PLAUSIBLE)
c.cited("S27", "eACH figures assume the room air is well mixed", "Physics", "Fluid mechanics", "CADR / V is a well-mixed estimate; short-circuit "
        "from the outlet back to the inlets lowers it", "Place the cube with the outlet jet free and the inlet sides 300 mm clear; mixing to check "
        "in a room test (V3)", PLAUSIBLE)
c.cited("S28", f"Two cubes meet the Lancet 'good' 10 L/s per person for up to about {R['lancet_people_two_cubes']:.0f} ward occupants",
        "Mathematics", "Units and dimensional analysis", "Lancet Commission NADR good 10 L/s (36 m3/h) per person, better 14 L/s",
        "795 m3/h / 36 m3/h per person; with more occupants the per-person criterion governs and a third cube is planned", WITHIN,
        closed_by=f"{CAL} section 6; PR-002")
c.cited("S29", "Used panels hold captured particles and are bagged and disposed of as the facility's waste rules require", "Biology", "Microbiology",
        "Captured particles stay on the media; handling a loaded filter can release dust", "Change with gloves, bag at the cube, follow the "
        "facility's IPC procedure; disposal route to agree with the partner (UR-005)", WITHIN, closed_by="CAR-CLM-001; label (BOM 9)")
c.cited("S30", "Fans sold for 230 V, 50 Hz at field sites have different curves from the 120 V data", "Engineering and technology",
        "Power and link budgets", "All cited measurements used 120 V US box fans", "Use the local listed fan and measure its CADR in the cube (V2)",
        PLAUSIBLE)
c.cited("S31", "The cube's eACH adds to the room's ventilation; it does not replace it", "Biology", "Epidemiology",
        "CDC: ACH and eACH from filtration can be added for comparison with the 5 ACH goal", "Stated in the claims and on the label", WITHIN,
        closed_by="CAR-CLM-001")
c.cited("S32", "The fan frame seals to the deck on the foam square", "Physics", "Fluid mechanics", "Gasket 510 mm square lies inside the "
        "521 x 552 mm fan frame and outside the 480 mm opening", "Leak counted in S7; the frame's own corner gaps outside the blades to check", WITHIN,
        closed_by=f"{CAL} section 7")

# ---- other options: CA1 (team concept) and CA3 -----------------------------------------------------------------------
x.cited("X1", "CA1: a flat MERV-13 panel at the fan's free-air face velocity would need 130 to 215 Pa, 2.4 to 7.8 times what the fan "
        "develops; the fan slows instead", "Physics", "Fluid mechanics", "Media resistance at 3.5 m/s against the 27.5 to 55 Pa shut-off",
        f"Operating point {R['CA1_Q'][0]:.0f} to {R['CA1_Q'][1]:.0f} m3/h at {R['CA1_dP'][0]:.0f} to {R['CA1_dP'][1]:.0f} Pa ({R['CA1_share'][0] * 100:.0f} to {R['CA1_share'][1] * 100:.0f} % of free "
        "air); UC Davis measured 142 to 154 cfm (241 to 262 m3/h) with one filter on a box fan, 29 to 35 % of the same fan with four", WITHIN,
        closed_by=f"{CAL} section 4")
x.cited("X2", f"CA1: one kit gives a measured CADR of {R['CA1_meas_CADR_m3h'][0]:.0f} to {R['CA1_meas_CADR_m3h'][1]:.0f} m3/h (model "
        f"{R['CA1_CADR_E1'][0]:.0f} to {R['CA1_CADR_E1'][1]:.0f}), so a 150 m3 ward gets {A['CA1 measured | ward 50 m2 x 3 m']['ACH'][0]:.1f} eACH measured "
        f"({A['CA1 model | ward 50 m2 x 3 m']['ACH'][0]:.1f} to {A['CA1 model | ward 50 m2 x 3 m']['ACH'][1]:.1f} model) and needs "
        f"{A['CA1 model | ward 50 m2 x 3 m']['units_for_5ACH'][0]} to {A['CA1 measured | ward 50 m2 x 3 m']['units_for_5ACH'][1]} kits for 5 ACH", "Mathematics", "Units and dimensional analysis", "eACH = CADR / volume; UC Davis "
        "1-filter CADR 77 to 83 cfm", "The principle holds; measured, one panel gives 29 to 35 % of the four-panel CADR on the same fan; scored in CAR-OPT-001", WITHIN)
x.cited("X3", "CA1: a collar fits 'ceiling fans' (scope in the team deck)", "Physics", "Fluid mechanics",
        "Ceiling fans have no shroud and spans of 29 to 54 in (ENERGY STAR); they develop almost no static pressure",
        "The 12 to 24 in collar cannot reach a 29 to 54 in rotor, and a rotor with no shroud has nothing to seal to; a panel under it would be "
        "bypassed. Fixed: scope is shrouded fans (box, pedestal, wall) and duct openings; ceiling fans are excluded", WITHIN,
        closed_by="CAR-DEC-001 F1 (standing instruction, 2026-10-23)")
lo, hi = R["uv_low"], R["uv_high"]
x.cited("X4", "CA1: the optional clip-on UV-C LED strip adds pathogen reduction", "Physics", "Optics and radiation",
        "Dose = mean fluence rate x residence time ~ P l / Q; D90 in air about 0.5 mJ/cm2 for SARS-CoV-2 (estimate) and 1 mJ/cm2 for typical "
        "viruses at 254 nm (Allen, Benner and Bahnfleth 2021)",
        f"Low-cost strip (6 x 10 mW): {lo['dose_mJcm2']:.4f} mJ/cm2, {lo['sp_sars'] * 100:.0f} % single pass, +{lo['eACH_ward_add']:.2f} eACH in "
        f"the ward. High-power strip (8 x 65 mW, {hi['electric_W']:.0f} W): {hi['dose_mJcm2']:.2f} mJ/cm2, {hi['sp_sars'] * 100:.0f} % at best, and one "
        f"LED of 40 to 65 mW reaches the ACGIH limit in {R['uv_eye']['t_limit_s_1m_65mW'] / 60:.0f} to {R['uv_eye']['t_limit_s_1m'] / 60:.0f} min at 1 m. "
        "Mean path 0.10 m for the strip at the fan face, 0.30 m (generous) for the high-power case. Fixed: UV-C module removed from the kit", WITHIN,
        closed_by="CAR-DEC-001 F2 (standing instruction, 2026-10-23)")
x.cited("X5", "CA1: a 270 to 285 nm LED module would make no ozone", "Chemistry", "Environmental and atmospheric chemistry",
        "Ozone forms below about 240 nm, peak near 185 nm; Luminus UVC LEDs emit nothing below 240 nm", "Holds, but the module is removed (X4)",
        WITHIN, closed_by="CAR-DEC-001 F2")
x.claim("X6", "CA1: a 1 mm gap at the collar lets under 10 % of the air bypass the panel", "Physics", "Fluid mechanics",
        "Orifice leak in parallel with the panel; 1.44 m round a 16 in rim; worst case over fans and media",
        round(LK["CA1 gap 1 mm"]["bypass_share"] * 100, 1), 10.0, "%",
        closed_by=f"{CAL} section 7 (round a 20 in box fan face, 2.15 m: 1 mm {LK['CA1 box fan gap 1 mm']['bypass_share'] * 100:.0f} %, "
                  f"5 mm {LK['CA1 box fan gap 5 mm']['bypass_share'] * 100:.0f} %)")
x.cited("X7", "CA1: the silicone collar seals guards of different profiles (wire rims, moulded rims, clips)", "Engineering and technology",
        "Manufacturing tolerances", "Team risk list: 'collar seal integrity across non-standard fan blade profiles'",
        "A stretched sleeve seals a round rim; flats, clips and oscillation heads leave gaps of several mm (X6). Test fit on 5 fan models (V7)",
        PLAUSIBLE)
x.cited("X8", "CA1: silicone holds its properties in heat and humidity", "Chemistry", "Materials and polymer chemistry",
        "Silicone sheet rated -80 to 500 F (-62 to 260 C), Zoro listing", "Far above room conditions for temperature; humidity, compression "
        "set, tear when stretched and disinfectant resistance are not in the listing and are to test (V7)", PLAUSIBLE)
x.cited("X9", f"CA1: loaded, the airflow falls to {R['CA1_loaded_Q'][0]:.0f} to {R['CA1_loaded_Q'][1]:.0f} m3/h (2.6 times) and "
        f"{R['CA1_heavy_Q'][0]:.0f} to {R['CA1_heavy_Q'][1]:.0f} m3/h (7.3 times)", "Physics", "Fluid mechanics",
        "Parker final resistance; UL dust-loaded filters 7.3 times clean", "The flat panel runs near shut-off, so loading costs it more than CA2",
        PLAUSIBLE)
x.cited("X10", "CA1: running near shut-off does not overheat the motor", "Engineering and technology", "Power and link budgets",
        "UL Chemical Insights report 200: single-filter box fans, winding at most 92 C, no ignition", "Covers box fans; pedestal and wall fans "
        "to check", PLAUSIBLE)
x.cited("X11", "CA1: a smaller 12 in fan gives at most about as much filtered air as a 20 in fan through one panel", "Physics", "Fluid mechanics",
        "Free delivery scaled with swept area, same shut-off pressure (A4)", f"12 in {R['ca1_sizes']['12 in']['Q_m3h']:.0f}, 20 in "
        f"{R['ca1_sizes']['20 in']['Q_m3h']:.0f} m3/h: the panel, not the fan, sets the flow", PLAUSIBLE)
c3 = R["ca3"]
x.cited("X12", "CA3: a 2 in MERV-13 panel on a return grille stays near the 25 Pa (0.1 in w.g.) filter drop US DOE gives as optimum",
        "Physics", "Fluid mechanics", "US DOE Building America: filter drop about 0.1 in w.c. optimum; total external static 0.4 to 0.5 in",
        f"400 cfm: {c3['400 cfm']['dP_low']:.0f} to {c3['400 cfm']['dP_high']:.0f} Pa; 800 cfm: {c3['800 cfm']['dP_low']:.0f} to "
        f"{c3['800 cfm']['dP_high']:.0f} Pa. Above the DOE optimum of about 25 Pa at every flow checked; it cuts system airflow and risks coil "
        "icing; a 4 in panel or a second grille would be needed. Option not carried", FIX, closed_by="Fix noted in CAR-OPT-001; option not carried")
x.cited("X13", f"CA3: a return-grille cassette gives {c3['400 cfm']['CADR_E1_m3h']:.0f} to {c3['800 cfm']['CADR_E1_m3h']:.0f} m3/h only while the air "
        "handler runs", "Mathematics", "Units and dimensional analysis", "CADR = E1 x return flow x duty", "Most target sites (tents, "
        "shelters) have no ducts; the added drop (X12) lowers the return flow, so the upper value is optimistic", WITHIN)
x.cited("X14", "CA3: four 16 mm magnet cups hold the cassette on a steel grille", "Physics", "Electromagnetism and circuits",
        "Pull force of the bought cup to its data sheet (to assess); cassette mass about 1 kg", "Not on aluminium or plastic grilles; "
        "screw clips needed there", PLAUSIBLE)


def table(rows):
    out = ["| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
           "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(rows, key=lambda r: int(r["id"][1:])):
        out.append(f"| {r['id']} | {r['claim']} | {r['field']} | {r['branch']} | {r['law']} | {r['check']} | {r['verdict']} | {r['closed_by'] or 'Open'} |")
    return "\n".join(out)


def inject(doc, tag, text):
    s = doc.read_text(encoding="utf-8")
    a, b = f"<!-- {tag} -->", f"<!-- /{tag} -->"
    if a in s and b in s:
        i, j = s.index(a) + len(a), s.index(b)
        doc.write_text(s[:i] + "\n" + text + "\n" + s[j:], encoding="utf-8")


if __name__ == "__main__":
    state = c.write()
    x.write()
    doc = ROOT / "docs/01b-stem-check.md"
    if doc.exists():
        inject(doc, "STM_TABLE", table(c.rows))
        inject(doc, "STM_OPTIONS", table(x.rows))
        print("refreshed tables in docs/01b-stem-check.md")
    print("CA2 state:", state)

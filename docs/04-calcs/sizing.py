"""CleanAir Retrofit Kit: sizing and first-principles checks (CAR-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py   (writes docs/04-calcs/sizing_results.json)
Reads cad/src/model.py PARAMS and bom/bom.csv. Every input is cited in CAR-CAL-001 (docs/04-calcs/01-sizing.md)
with its source and the date checked (2026-11-12), or marked as an assumption (A1 to A12).

Method
  Fan curve: quadratic  dP = Pmax (1 - (Q/Q0)^2).  Pmax from Dal Porto et al. 2022 (a 20 in box fan lost 12 % of its
  flow at 6.2 Pa, so Pmax = 6.2 / (1 - 0.88^2) = 27.5 Pa); Q0 bounds: rated 1,800 cfm (Lasko 3733 listing, an upper
  bound) and 568 cfm derived from the UC Davis case study (Lasko B: 500 cfm through a 4-filter cube at an estimated
  5 to 7.5 Pa, taken at 6.2 Pa).
  Media: linear in face velocity (A3), dP = k v, k from the MERV-13 2 in data sheets: Parker Xtreme Plus 0.39 in w.g.
  at 500 fpm (38.3 Pa per m/s) and Global Industrial 0.38 in w.g. at 300 fpm (62.1 Pa per m/s).
  Leaks: orifice flow Q = Cd A sqrt(2 dP / rho), Cd 0.6 (A5), in parallel with the media.
  CADR = single-pass efficiency x filtered airflow; MERV-13 minimum E1 50 % (0.3 to 1 um), E2 85 % (1 to 3 um).
"""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import model as M  # noqa: E402

P = M.PARAMS
RHO = 1.20            # kg/m3 air at 20 C
CFM = 0.000471947     # m3/s per cfm
INWG = 249.089        # Pa per in w.g.
FPM = 0.00508         # m/s per fpm

# ---- fan curves (box fan, 20 in) ----------------------------------------------------------------------------------
PMAX = 6.2 / (1 - 0.88 ** 2)                       # Dal Porto 2022: 12 % flow loss at 6.2 Pa, measured at LOW speed
SPEED = 852.0 / 600.0                              # high/low CADR ratio (Dal Porto) as a proxy for the speed ratio (A2)
PMAXS = {"low-speed fit": PMAX, "fan laws to high speed": PMAX * SPEED ** 2}   # shut-off pressure scales with N^2
Q0 = {"rated": 1800 * CFM, "measured": 500 * CFM / math.sqrt(1 - 6.2 / PMAX)}
# ---- media ---------------------------------------------------------------------------------------------------------
K = {"low (Parker 2 in)": 0.39 * INWG / (500 * FPM), "high (Global Industrial 2 in)": 0.38 * INWG / (300 * FPM)}
A_PANEL = P["FILT_FACE_M2"]
E1, E2, E3 = 0.50, 0.85, 0.90                     # ASHRAE 52.2 MERV-13 minimums (NAFA guide)
LOAD = 1.00 / 0.39                                 # end-of-life multiplier: 1.0 in w.g. final over 0.39 initial (Parker)
CD = 0.6

ROOMS = {"ward 50 m2 x 3 m": 150.0, "clinic room 20 m2 x 3 m": 60.0}
TARGETS = {"CDC 5 ACH": 5.0, "Lancet good 4 ACHe": 4.0, "Lancet better 6 ACHe": 6.0}


def operating(q0, k, area, leak_m2=0.0, pmax=PMAX, extra=lambda q: 0.0):
    """Solve fan curve = media drop for the filtered flow, with a leak in parallel. Returns (Q_total, Q_filtered, dP)."""
    lo, hi = 0.0, pmax
    for _ in range(80):
        dp = (lo + hi) / 2
        qf = area * dp / k
        ql = CD * leak_m2 * math.sqrt(2 * dp / RHO)
        qt = qf + ql
        fan = pmax * (1 - (qt / q0) ** 2) - extra(qt)
        if fan > dp:
            lo = dp
        else:
            hi = dp
    return qt, qf, dp


def m3h(q):
    return q * 3600.0


R = {"PMAX_Pa": PMAX, "Q0_m3s": Q0, "K_Pa_per_mps": K, "A_panel_m2": A_PANEL}

# ---- CA1 one flat panel, CA2 four panels ---------------------------------------------------------------------------
cases = {}
for opt, area in (("CA1", A_PANEL), ("CA2", 4 * A_PANEL)):
    for fk, q00 in Q0.items():
      for pk, pm in PMAXS.items():
        q0 = 500 * CFM / math.sqrt(1 - 6.2 / pm) if fk == "measured" else q00   # the measured point fixes Q0 for each Pmax
        for mk, k in K.items():
            for state, mult in (("clean", 1.0), ("loaded", LOAD), ("heavily loaded", 2.0 / 0.274)):
                qt, qf, dp = operating(q0, k * mult, area, pmax=pm)
                cases[f"{opt} | fan {fk} | {pk} | media {mk} | {state}"] = dict(
                    Q_m3h=m3h(qt), Qf_m3h=m3h(qf), dP_Pa=dp, v_face=qf / area, share_of_free=qt / q0,
                    CADR_E1_m3h=E1 * m3h(qf), CADR_E2_m3h=E2 * m3h(qf))
R["cases"] = cases


def rng(opt, key, state="clean"):
    vals = [v[key] for n, v in cases.items() if n.startswith(opt) and n.split(" | ")[-1] == state]
    return min(vals), max(vals)


R["CA1_Q"] = rng("CA1", "Q_m3h")
R["CA2_Q"] = rng("CA2", "Q_m3h")
R["CA1_dP"] = rng("CA1", "dP_Pa")
R["CA2_dP"] = rng("CA2", "dP_Pa")
R["CA1_v"] = rng("CA1", "v_face")
R["CA1_share"] = rng("CA1", "share_of_free")
R["CA2_v"] = rng("CA2", "v_face")
R["CA1_CADR_E1"] = rng("CA1", "CADR_E1_m3h")
R["CA2_CADR_E1"] = rng("CA2", "CADR_E1_m3h")
R["CA1_CADR_E2"] = rng("CA1", "CADR_E2_m3h")
R["CA2_CADR_E2"] = rng("CA2", "CADR_E2_m3h")
R["CA1_loaded_Q"] = rng("CA1", "Q_m3h", "loaded")
R["CA2_loaded_Q"] = rng("CA2", "Q_m3h", "loaded")
R["CA1_heavy_Q"] = rng("CA1", "Q_m3h", "heavily loaded")
R["CA2_heavy_Q"] = rng("CA2", "Q_m3h", "heavily loaded")
R["PMAX_range"] = (min(PMAXS.values()), max(PMAXS.values()))
# pressure the brief quotes for a flat panel at the fan's own free-air face velocity (no fan curve): 40 to 100 Pa
v_free = Q0["rated"] / A_PANEL
R["flat_panel_at_free_air_Pa"] = [k * v_free for k in K.values()]
R["v_free_air"] = v_free

# ---- measured data, the cross-check -------------------------------------------------------------------------------
MEAS = {
    "UC Davis 1 filter on box fan, high (cfm CADR)": (77, 83), "UC Davis 1 filter airflow (cfm)": (142, 154),
    "UC Davis 4-filter cube, high (cfm CADR)": (239, 270), "UC Davis 4-filter airflow (cfm)": (443, 500),
    "Dal Porto 5-filter cube CADR (m3/h)": (1020, 1450), "EPA ORD MS2 virus CADR (cfm)": (234, 234),
}
R["measured"] = MEAS
CA1_MEAS_CADR = (77 * 1.699, 83 * 1.699)            # m3/h
CA2_MEAS_CADR = (234 * 1.699, 270 * 1.699)         # four-panel cubes on high: EPA MS2 234 cfm to UC Davis 270 cfm
R["five_panel_ref_m3h"] = (1020.0, 1450.0)          # Dal Porto five-panel cube, Air King fan (a reference, not CA2)
R["CA2_low_speed_CADR_m3h"] = (163 * 1.699, 165 * 1.699)   # UC Davis four-filter cube, speed 1, 70 to 71 W
R["CA1_meas_CADR_m3h"] = CA1_MEAS_CADR
R["CA2_meas_CADR_m3h"] = CA2_MEAS_CADR
R["one_vs_four_measured"] = (142 / 500, 154 / 443)

# ---- air changes per hour and units needed --------------------------------------------------------------------------
ach = {}
for room, vol in ROOMS.items():
    for opt, (lo, hi) in (("CA1 model", R["CA1_CADR_E1"]), ("CA1 measured", CA1_MEAS_CADR),
                          ("CA2 model", R["CA2_CADR_E1"]), ("CA2 measured", CA2_MEAS_CADR)):
        ach[f"{opt} | {room}"] = dict(ACH=(lo / vol, hi / vol), units_for_5ACH=(math.ceil(5 * vol / hi), math.ceil(5 * vol / lo)),
                                     units_for_6ACH=(math.ceil(6 * vol / hi), math.ceil(6 * vol / lo)))
R["ach"] = ach
R["CADR_needed_m3h"] = {room: {t: a * vol for t, a in TARGETS.items()} for room, vol in ROOMS.items()}

# ---- bypass leakage (worst case over both fans, both shut-off pressures and both media) --------------------------------
leak = {}
perim_ca1 = 2 * math.pi * (P["SLEEVE"][0] + P["SLEEVE"][1])  # mm, round a 16 in guard rim
perim_box = 2 * (521 + 552)                                  # mm, round the face of a 20 in box fan (independent review)
perim_ca2 = 4 * P["GASKET_SQ"] + 4 * P["FILT_W"] + 4 * P["TRAY"]   # deck gasket, four corner seams and the tray seam, mm


def worst_leak(perim, gap, area):
    out = []
    for fk, q0 in Q0.items():
        for pk, pm in PMAXS.items():
            q0_ = 500 * CFM / math.sqrt(1 - 6.2 / pm) if fk == "measured" else q0
            for k in K.values():
                qt, qf, dp = operating(q0_, k, area, perim * gap * 1e-6, pmax=pm)
                out.append((1 - qf / qt, E1 * m3h(qf), m3h(qt)))
    return dict(bypass_min=min(o[0] for o in out), bypass_share=max(o[0] for o in out))


for g in (1.0, 3.0, 5.0):
    leak[f"CA1 gap {g:.0f} mm"] = worst_leak(perim_ca1, g, A_PANEL)
    leak[f"CA1 box fan gap {g:.0f} mm"] = worst_leak(perim_box, g, A_PANEL)
for g in (0.5, 1.0, 2.0):
    leak[f"CA2 gap {g:.1f} mm"] = worst_leak(perim_ca2, g, 4 * A_PANEL)
R["leak"] = leak
R["perim_mm"] = {"CA1": perim_ca1, "CA1 box fan": perim_box, "CA2": perim_ca2}

# ---- CA3 return grille --------------------------------------------------------------------------------------------
ca3 = {}
for cfm in (400, 600, 800):
    q = cfm * CFM
    v = q / A_PANEL
    ca3[f"{cfm} cfm"] = dict(v_face=v, dP_low=K["low (Parker 2 in)"] * v, dP_high=K["high (Global Industrial 2 in)"] * v,
                             CADR_E1_m3h=E1 * m3h(q), DOE_limit_Pa=0.1 * INWG)
R["ca3"] = ca3

# ---- smaller shrouded fans for CA1 (A4: free delivery scales with swept area, same Pmax) ---------------------------------
small = {}
for d_in in (12, 16, 20, 24):
    q0 = Q0["rated"] * (d_in / 20) ** 2
    qt, qf, dp = operating(q0, K["low (Parker 2 in)"], A_PANEL)   # same shut-off pressure (A4; fan laws give less)
    small[f"{d_in} in"] = dict(Q0_m3h=m3h(q0), Q_m3h=m3h(qt), CADR_E1=E1 * m3h(qf))
R["ca1_sizes"] = small

# ---- motor (UL Chemical Insights report 200, 2021) -------------------------------------------------------------------
R["motor"] = dict(current_A=(0.4, 0.9), power_W=(52.8, 97.8), winding_max_C=92, class_A_limit_C=105, housing_max_C=54)
R["CADR_per_W_CA2"] = (CA2_MEAS_CADR[0] / 103.0, 1450.0 / 98.0)   # four-panel UC Davis/EPA on 102 to 103 W; Dal Porto five-panel
R["lancet_people_two_cubes"] = 2 * CA2_MEAS_CADR[0] / 36.0         # occupants for 10 L/s per person (36 m3/h) with two cubes

# ---- UV-C dose for the strip at the fan face (CA1 as drawn by the team) ----------------------------------------------------
# dose = mean fluence rate x residence time ~ P_uv x l_mean / Q (A8: well-mixed irradiated zone, absorbing walls)
uv = {}
for n_led, p_led in ((6, 0.010), (8, 0.040), (8, 0.065)):
    p_uv = n_led * p_led
    for l_mean in (0.10, 0.30):
        for q in (R["CA1_Q"][0] / 3600, R["CA1_Q"][1] / 3600):
            dose = p_uv * l_mean / q             # J/m2
            uv[f"{n_led} x {p_led * 1000:.0f} mW, path {l_mean:.2f} m, Q {q * 3600:.0f} m3/h"] = dict(
                dose_mJcm2=dose / 10.0, single_pass_D90_0p5=1 - 10 ** (-dose / 5.0), single_pass_D90_1=1 - 10 ** (-dose / 10.0),
                electric_W=n_led * 0.35 * 6.45)
R["uv"] = uv
best = max(v["single_pass_D90_0p5"] for v in uv.values())
R["uv_best_single_pass"] = best
R["uv_dose_range_mJcm2"] = (min(v["dose_mJcm2"] for v in uv.values()), max(v["dose_mJcm2"] for v in uv.values()))
# named scenarios: a low-cost strip (6 LEDs x 10 mW, A8) at a 0.1 m mean path and the CA1 flow; a high-power strip
# (8 Luminus XST-class LEDs x 65 mW, 18 W electrical) at a generous 0.3 m path and the lowest CA1 flow
def _uv(n, p, l, q):
    d = n * p * l / q
    return dict(dose_mJcm2=d / 10, sp_sars=1 - 10 ** (-d / 5.0), sp_virus=1 - 10 ** (-d / 10.0), electric_W=n * 0.35 * 6.45,
                eACH_ward_add=(1 - 10 ** (-d / 5.0)) * q * 3600 / 150.0)
R["uv_low"] = _uv(6, 0.010, 0.10, sum(R["CA1_Q"]) / 2 / 3600)
R["uv_high"] = _uv(8, 0.065, 0.30, R["CA1_Q"][0] / 3600)
# eye exposure: one 40 mW LED, 60 deg beam (about 0.84 sr), on axis at 1 m; ACGIH TLV 3 mJ/cm2 effective at 270 nm,
# S(275 nm) about 0.96 (A9)
i_sr = 0.040 / (2 * math.pi * (1 - math.cos(math.radians(30))))
e_1m = i_sr / 1.0 ** 2 * 1e2                       # uW/cm2 (W/m2 x 100)
R["uv_eye"] = dict(I_W_per_sr=i_sr, E_uW_cm2_1m=e_1m, t_limit_s_1m=3000.0 / (e_1m * 0.96),
                  t_limit_s_1m_65mW=3000.0 / (e_1m * 65 / 40 * 0.96))

# ---- ceiling fans ------------------------------------------------------------------------------------------------------
R["ceiling"] = dict(span_in=(29, 54), kit_in=(12, 24), static_Pa="about 0 (no shroud, free rotor)")

# ---- CA2 stability, mass and envelope ---------------------------------------------------------------------------------
import cad_parts as cp  # noqa: E402
parts = M.components("CA2")
real = [q for q in parts if q["kind"] != "context"]
SHEET_KG_M2 = 0.75                                 # A10: 4 mm twin-wall PP, areal mass assumed
sheet_parts = [q for q in real if "corrugated PP" in q["name"]]
m_sheet_model = sum(cp.mass_kg(q) for q in sheet_parts)
area_sheet = sum(q["shape"].volume / P["SHEET_T"] for q in sheet_parts) * 1e-6
m_other = sum(cp.mass_kg(q) for q in real if q not in sheet_parts)
m_filters_model = sum(cp.mass_kg(q) for q in real if "MERV-13" in q["name"])
FILTER_KG = 0.68                                    # A11: a 20 x 20 x 2 in MERV-13 panel, assumed (to weigh)
m_kit = (m_other - m_filters_model) + 4 * FILTER_KG + area_sheet * SHEET_KG_M2
FAN_KG = 7.25 * 0.4536                              # Lasko 3733 listing
z_cg = ((m_kit) * 0.30 + FAN_KG * (M.Z_FAN + P["BOXFAN"][2] / 2) / 1000) / (m_kit + FAN_KG)
half_base = P["FOOT_XY"] / 1000 + P["FOOT"][0] / 2000
R["ca2_mass"] = dict(kit_kg=m_kit, fan_kg=FAN_KG, total_kg=m_kit + FAN_KG, sheet_m2=area_sheet, z_cg_m=z_cg,
                     tip_angle_deg=math.degrees(math.atan(half_base / z_cg)),
                     push_at_top_N=(m_kit + FAN_KG) * 9.81 * half_base / ((M.Z_FAN + P["BOXFAN"][2]) / 1000))
from build123d import Compound  # noqa: E402
_bb = Compound(children=[q["shape"] for q in real]).bounding_box()
R["ca2_envelope_mm"] = dict(width=max(_bb.max.X - _bb.min.X, _bb.max.Y - _bb.min.Y), height=_bb.max.Z - _bb.min.Z,
                            cube=2 * (M.H_CUBE + P["ANGLE_GAP"] + P["SHEET_T"] + 0.5 + P["STRAP_T"]))
R["sheets_needed"] = 2

# ---- time estimates (A12; to be measured with users at TRL 4) -------------------------------------------------------------
R["time_min"] = dict(ca2_first_assembly=(8, 12), ca2_filter_set_swap=(4, 6), ca2_one_panel=(1.5, 2.5), ca1_cassette_swap=(1, 2))

# ---- BOM ----------------------------------------------------------------------------------------------------------------
tot = 0.0
for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
    tot += float(r["qty"]) * float(r["unit_cost_usd"])
R["bom_total"] = tot
R["budget"] = 150.0
R["filters_share"] = 4 * 13.50 / tot if tot else 0
R["cost_per_CADR_usd_per_m3h"] = (tot / CA2_MEAS_CADR[1], tot / CA2_MEAS_CADR[0])
# media cost per year (A7: replace the set every 6 months at 24 h use; to set from the loaded-flow test)
R["filters_per_year_usd"] = 2 * 4 * 13.50
R["energy_kwh_year"] = (67 * 24 * 365 / 1000, 98 * 24 * 365 / 1000)

(ROOT / "docs/04-calcs/sizing_results.json").write_text(json.dumps(R, indent=1, default=float))
if __name__ == "__main__":
    print(f"Pmax {PMAX:.1f} Pa; Q0 rated {m3h(Q0['rated']):.0f}, measured {m3h(Q0['measured']):.0f} m3/h; k {K}")
    for n in ("CA1_heavy_Q", "CA2_heavy_Q", "PMAX_range", "CADR_per_W_CA2", "CA2_meas_CADR_m3h", "CA2_low_speed_CADR_m3h", "CA1_Q", "CA2_Q", "CA1_dP", "CA2_dP", "CA1_v", "CA2_v", "CA1_CADR_E1", "CA2_CADR_E1", "CA1_loaded_Q", "CA2_loaded_Q"):
        print(n, [round(x, 2) for x in R[n]])
    print("flat panel at free-air velocity", [round(x) for x in R["flat_panel_at_free_air_Pa"]], "Pa at", round(v_free, 2), "m/s")
    for k_, v in ach.items():
        print(k_, [round(x, 1) for x in v["ACH"]], v["units_for_5ACH"])
    for k_, v in leak.items():
        print(k_, round(v["bypass_min"], 3), round(v["bypass_share"], 3))
    for k_, v in ca3.items():
        print("CA3", k_, round(v["v_face"], 2), round(v["dP_low"], 1), round(v["dP_high"], 1), round(v["CADR_E1_m3h"]))
    for k_, v in small.items():
        print("CA1 size", k_, {a: round(b) for a, b in v.items()})
    print("UV low", R["uv_low"]); print("UV high", R["uv_high"])
    print("UV eye", R["uv_eye"])
    print("CA2 mass", R["ca2_mass"], R["ca2_envelope_mm"])
    print("BOM total", round(tot, 2))

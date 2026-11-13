"""CleanAir Retrofit Kit: concept media from the TRL 3 model (option CA2, recommended; proposed, awaiting Amish).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything; on a small machine run one picture per process. Geometry comes from
cad/src/model.py; airflow values come from CAR-CAL-001 (docs/04-calcs/sizing_results.json) and are estimates.
Uses the pieces of .kit/concept.py render_all one at a time, with a 1.75 m person for scale.
CONCEPT, NOT FOR FABRICATION.
"""
import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as M  # noqa: E402

PROJECT, TITLE, DWG, DATE = "CleanAir Retrofit Kit", "Filter cube kit on an existing box fan (option CA2, proposed)", "CAR-DWG-010", "2026-11-12"
MD = ROOT / "media"
RES = ROOT / "docs/04-calcs/sizing_results.json"
SMALL = ("bolt", "washer", "nut", "label")


def parts(context=True, small=True):
    out = []
    for q in M.components(M.CHOSEN):
        if q["kind"] == "context" and not context:
            continue
        if not small and (q["kind"] == "fastener" or any(s in q["name"].lower() for s in SMALL)):
            continue
        out.append(Part(q["name"], q["shape"], q["color"], q["bom"], tuple(q["explode"])))
    return out


def hero():
    ps = K.with_scale_figure(parts(context=True, small=False))
    return K._render(ps, MD / "hero.png", title=PROJECT, size=(8, 7), elev=20, azim=-50,
                     note="Option CA2 (recommended; proposed, awaiting Amish). Seen from the front right and above, 20 deg "
                          "elevation. Grey: a 1.75 m person and the existing 20 in box fan (not in the kit). The cube is "
                          "576 mm across the buckles and 639 mm tall. CONCEPT, NOT FOR FABRICATION")


def cutaway():
    ps = [p for p in parts(context=True, small=False)]
    return K._render(K.cutaway_parts(ps), MD / "cutaway.png", azim=-90, elev=12, size=(8, 8), title=f"{PROJECT}: cutaway",
                     note="Front half removed; seen from the front, 12 deg elevation. Room air enters through the four MERV-13 "
                          "panels (sides), rises through the open cube and the 480 mm deck opening, and leaves upward through "
                          "the box fan. The foam gasket seals the fan to the deck. CONCEPT, NOT FOR FABRICATION")


def bom_names():
    out = {}
    for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
        n, _, rest = r["item"].partition(" ")
        out[int(n)] = rest.split(",")[0]
    return out


def exploded():
    names = bom_names()
    ps = []
    for p in parts(context=False, small=False):
        if p.bom is None:
            continue
        ps.append(Part(names.get(p.bom, p.name), p.shape, p.color, p.bom, p.explode))
    return K._render(ps, MD / "exploded.png", offsets=True, labels=True, size=(10, 9), elev=22, azim=-50,
                     title=f"{PROJECT}: exploded view",
                     note="Seen from the front right and above, 22 deg elevation; numbers match bom/bom.csv. Panels pulled "
                          "outward, deck and gasket lifted, tray and feet lowered. Box fan not shown (not in the kit)")


def flow():
    r = json.loads(RES.read_text())
    c = r["cases"]["CA2 | fan rated | low-speed fit | media low (Parker 2 in) | clean"]
    stages = [("Room air at the four panel faces", f"{c['Q_m3h']:.0f} m3/h"),
              ("Through MERV-13 media (E1 >= 50 %)", f"{c['dP_Pa']:.1f} Pa, {c['v_face']:.2f} m/s"),
              ("Inside the cube, up to the deck", "about 0 Pa"),
              ("Deck opening and gasket", "sealed, leak 1 to 3 %"),
              ("Box fan, out at the top", f"CADR {c['CADR_E1_m3h']:.0f} m3/h (0.3 to 1 um)")]
    return K.flow_diagram(stages, MD / "flow.png",
                          f"{PROJECT}: air path through the filter cube on a rated 20 in box fan, clean media (estimates, "
                          f"CAR-CAL-001); measured four-panel cubes give 398 to 459 m3/h CADR, the design basis", "")


def web():
    ps = parts(context=True, small=False)
    return K.export_web_model(ps, "media", title=f"{PROJECT}: {TITLE}")


def blueprint():
    from build123d import Compound
    from drawing import Sheet, project_views
    r = json.loads(RES.read_text())
    ps = parts(context=False, small=False)
    shown = K.with_scale_figure(parts(context=True, small=False))
    views = project_views(Compound(children=[p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(Compound(children=[p.shape for p in shown]), MD / "_views_fig")["iso"]
    a = r["ach"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P1", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Detailed TRL 3 model for concept communication",
              revisions=[("P1", "Concept sheet from the TRL 3 model", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale; grey is a 1.75 m person and the existing fan")
    s.add_notes("Key figures (estimates, CAR-CAL-001)", [
        f"576 mm across the buckles, {r['ca2_envelope_mm']['height']:.0f} mm tall with a 20 in box fan",
        "Four 20 x 20 x 2 in MERV-13 panels, 0.98 m2 of face",
        f"Airflow {r['CA2_Q'][0]:.0f} to {r['CA2_Q'][1]:.0f} m3/h (model); face {r['CA2_v'][0]:.2f} to {r['CA2_v'][1]:.2f} m/s",
        f"Measured 4-panel cubes: CADR {r['CA2_meas_CADR_m3h'][0]:.0f} to {r['CA2_meas_CADR_m3h'][1]:.0f} m3/h",
        f"50 m2 ward: {a['CA2 measured | ward 50 m2 x 3 m']['ACH'][0]:.1f} to {a['CA2 measured | ward 50 m2 x 3 m']['ACH'][1]:.1f} eACH per cube; plan 2",
        f"20 m2 room, one cube: {a['CA2 measured | clinic room 20 m2 x 3 m']['ACH'][0]:.1f} to {a['CA2 measured | clinic room 20 m2 x 3 m']['ACH'][1]:.1f} eACH",
        f"Kit parts USD {r['bom_total']:.2f} (target USD 150), fan not included",
        "No UV-C; no ozone source. Not a substitute for ventilation"], x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    shutil.rmtree(MD / "_views", ignore_errors=True)
    shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w_ in sys.argv[1:] or list(fns):
        print(w_, "->", fns[w_]())

"""CleanAir Retrofit Kit: drawing set and STL export for option CA2 (carried in the drawing set; choice awaiting Amish).

Run from the repo root:  python cad/src/sheets.py [ga|section|stl]   (no argument: all three)
    cad/drawings/CAR-DWG-001   general arrangement, filter cube assembled on a 20 in box fan (fan shown, not in the kit)
    cad/drawings/CAR-DWG-002   half section: air path, deck gasket, tray and feet
    cad/stl/*.stl              the assembly and each made part, for viewing and printing the feet
Making sketches for each made part (CAR-DWG-101 onward) are drawn by cad/src/build_plan_media.py.
Sheets are generated from cad/src/model.py and never edited by hand; figures come from CAR-CAL-001.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
from build123d import Box, Compound, Pos, export_stl  # noqa: E402
from drawing import Sheet, project_views  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
DATE = "2026-11-12"
DWG = ROOT / "cad/drawings"
R = json.loads((ROOT / "docs/04-calcs/sizing_results.json").read_text())
PROJECT = "CleanAir Retrofit Kit"
MAT = "4 mm corrugated PP (cut, scored, folded); bought MERV-13 panels, straps, EPDM foam; printed PP feet. See bom/bom.csv"


def body_parts(fan=True):
    out = [q for q in M.components("CA2") if q["kind"] in ("made", "bought", "fastener")]
    if fan:
        out += [q for q in M.components("CA2") if q["kind"] == "context" and "frame" not in q["name"].lower() and "Existing" in q["name"]]
    return out


def ga():
    parts = body_parts()
    work = DWG / "_views_ga"
    views = project_views(Compound(children=[q["shape"] for q in parts]), work)
    s = Sheet(project=PROJECT, title="Filter cube kit on an existing 20 in box fan (option CA2): general arrangement",
              dwg_no="CAR-DWG-001", rev="P1", author="Amish Chadha", date=DATE, concept=True, scale=None, material=MAT,
              revisions=[("P1", "Preliminary GA from the TRL 3 model (CAR-CAL-001)", DATE, "AC")])
    s.add_ortho(views, ["front", "top", "right"])
    s.add_svg(views["iso"], 276, 32, 140, 70, label="Isometric view", sublabel="Not to scale; box fan outline shown, not in the kit")
    s.add_notes("Key dimensions (mm) and data", [
        f"Panels 4 x {P['FILT_W']:.0f} x {P['FILT_W']:.0f} x {P['FILT_T']:.0f} (20 x 20 x 2 in nominal), pinwheel",
        f"Cube outside {P['CUBE']:.0f} square; tray and deck {P['TRAY']:.0f} square, 30 flaps",
        f"Deck opening {P['DECK_HOLE_D']:.0f} dia (cut lines 280 and 380 for smaller fans)",
        f"Gasket {P['GASKET_SQ']:.0f} square, 8 wide, 10 compressed (EPDM foam)",
        "Corner angles 40 x 40 x 425, folded from offcuts",
        "Straps 25 wide: two round the panels at 180 and 360, two over the fan",
        f"Feet 50 x 50 x 15 at +-{P['FOOT_XY']:.0f}, M5 x 20 bolts",
        f"Overall {R["ca2_envelope_mm"]["width"]:.0f} across the buckles, {R['ca2_envelope_mm']['height']:.0f} high with the fan",
        f"Airflow {R['CA2_Q'][0]:.0f} to {R['CA2_Q'][1]:.0f} m3/h (model, clean)",
        f"Kit about {R['ca2_mass']['kit_kg']:.1f} kg; parts USD {R['bom_total']:.2f}",
        "PRELIMINARY, NOT FOR FABRICATION",
    ], x=276, y=118, width=140)
    s.save(DWG / "CAR-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote cad/drawings/CAR-DWG-001.svg, .pdf, .png")


def section():
    cutter = Pos(0, 400, 400) * Box(1400, 800, 1400)       # keeps +Y half: seen from -Y the cut face shows
    parts = []
    for q in body_parts():
        if "label" in q["name"].lower():
            continue
        try:
            h = q["shape"] & cutter
            if h.volume > 1e-3:
                parts.append(h)
        except Exception:
            pass
    work = DWG / "_views_sec"
    views = project_views(Compound(children=parts), work, center_lines=False)
    s = Sheet(project=PROJECT, title="Filter cube kit (option CA2): half section through the air path, deck gasket and feet",
              dwg_no="CAR-DWG-002", rev="P1", author="Amish Chadha", date=DATE, concept=True, scale=None, material=MAT,
              revisions=[("P1", "Preliminary half section from the TRL 3 model", DATE, "AC")])
    s.add_ortho(views, ["front", "top", "right"], dims=True)
    s.add_svg(views["iso"], 276, 32, 140, 70, label="Isometric view", sublabel="Half section, front half removed; not to scale")
    s.add_notes("Air path and seals", [
        "Room air enters through the four panel faces",
        f"Face velocity {R['CA2_v'][0]:.2f} to {R['CA2_v'][1]:.2f} m/s; drop {R['CA2_dP'][0]:.0f} to {R['CA2_dP'][1]:.0f} Pa",
        "Cube interior is open; air rises to the deck",
        "Deck opening 480 dia under the fan blades",
        "Seal 1: EPDM foam square under the fan frame",
        "Seal 2: tray and deck flaps over the panel edges",
        "Seal 3: corner angles over the four vertical seams",
        f"1 mm gaps everywhere: {R['leak']['CA2 gap 1.0 mm']['bypass_share'] * 100:.1f} % bypass (estimate)",
        "Fan blows up; inlet sides need 300 clear",
        "PRELIMINARY, NOT FOR FABRICATION",
    ], x=276, y=118, width=140)
    s.save(DWG / "CAR-DWG-002")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote cad/drawings/CAR-DWG-002.svg, .pdf, .png")


def stl():
    out = ROOT / "cad/stl"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.stl"):
        old.unlink()
    parts = [q for q in body_parts(fan=False) if q["kind"] in ("made", "bought")]
    export_stl(Compound(children=[q["shape"] for q in parts]), str(out / "car-ca2-assembly.stl"), tolerance=0.2, angular_tolerance=0.3)
    seen = set()
    for q in parts:
        if q["kind"] == "made":
            base = q["name"].split(",")[0].lower().replace(" ", "-")
            base = "".join(ch for ch in base if ch.isalnum() or ch == "-")
            base = base.rstrip("-0123456789").rstrip("-") or base
            if base in seen:
                continue
            seen.add(base)
            export_stl(q["shape"], str(out / f"car-{base}.stl"), tolerance=0.1, angular_tolerance=0.2)
    print("wrote", len(list(out.glob("*.stl"))), "STL files to cad/stl/")


if __name__ == "__main__":
    fns = {"ga": ga, "section": section, "stl": stl}
    for w in sys.argv[1:] or list(fns):
        fns[w]()

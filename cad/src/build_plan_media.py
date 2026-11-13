"""CleanAir Retrofit Kit: prototype build plan pictures (CAR-BLD-001, STANDARDS section 18), option CA2.

Run from the repo root, one picture group per process on a small machine:
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
Every picture is drawn from cad/src/model.py components("CA2"), so pictures and model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CAR-DWG-101 to 104        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import functools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Box, Compound, Pos  # noqa: E402
import model as M  # noqa: E402

OUT = ROOT / "docs/05-build-plan"
DWG = ROOT / "cad/drawings"
DATE = "2026-11-12"
PROJECT = "CleanAir Retrofit Kit"
SIDES = ("north", "west", "south", "east")


@functools.lru_cache(None)
def raw():
    return {q["name"]: q for q in M.components("CA2")}


def P_(name, explode=None, color=None, label=None):
    q = raw()[name]
    return Part(name if label is None else label, q["shape"], color or q["color"], q["bom"], tuple(explode if explode is not None else q["explode"]))


def panel(side, explode=None):
    """One MERV-13 panel (frame and media) as one picture item."""
    f, m = raw()[f"MERV-13 panel frame ({side})"], raw()[f"MERV-13 pleated media ({side})"]
    ex = explode if explode is not None else f["explode"]
    return Part(f"MERV-13 panel ({side})", Compound(children=[f["shape"], m["shape"]]), f["color"], 1, tuple(ex))


def bolts(i):
    names = [n for n in raw() if n.endswith(f"foot {i}")]
    return Part(f"M5 bolt, washers and nut (foot {i})", Compound(children=[raw()[n]["shape"] for n in names]), "#9CA3AF", 8)


def fan():
    names = [n for n, q in raw().items() if q["kind"] == "context"]
    return Part("Existing 20 in box fan (not in the kit)", Compound(children=[raw()[n]["shape"] for n in names]), "#D1D5DB")


TRAY, DECK, GASKET = "Base tray, corrugated PP 4 mm, scored and folded", "Fan deck, corrugated PP 4 mm, scored and folded", "Fan deck gasket, EPDM foam weatherstrip"
ANG = [f"Corner angle {k}, corrugated PP 4 mm, scored and folded" for k in range(1, 5)]
FEET = [f"Foot {k}, printed PP" for k in range(1, 5)]
HS = ["Cam strap, 25 mm, horizontal (lower)", "Cam strap, 25 mm, horizontal (upper)"]
HB = ["Cam buckle, horizontal strap (lower)", "Cam buckle, horizontal strap (upper)"]
VS = ["Cam strap, 25 mm, fan hold-down (+Y)", "Cam strap, 25 mm, fan hold-down (-Y)"]
VB = ["Cam buckle, fan hold-down strap (+Y)", "Cam buckle, fan hold-down strap (-Y)"]
LABEL = "Instruction and warning label"


def overview():
    ps = [P_(FEET[0], (0, 0, -120), label="Foot (4), printed PP")]
    ps += [P_(n, (0, 0, -120), label="") for n in FEET[1:]]
    ps.append(bolts(1)); ps[-1].explode = (0, 0, -60); ps[-1].name = "M5 bolt set (4)"
    ps.append(P_(TRAY, (0, 0, -60), label="Base tray, folded PP sheet"))
    ps += [panel(s, ex) for s, ex in zip(SIDES, [(0, 160, 0), (-160, 0, 0), (0, -160, 0), (160, 0, 0)])]
    ps[-4].name = "MERV-13 panel (4)"
    for p in ps[-3:]:
        p.name = ""
    ps.append(P_(ANG[3], (240, -240, 0), label="Corner angle (4), folded PP"))
    ps += [P_(n, ex, label="") for n, ex in zip(ANG[:3], [(240, 240, 0), (-240, 240, 0), (-240, -240, 0)])]
    ps.append(P_(HS[0], (0, 0, 0), label="Cam strap (4), round the panels and over the fan"))
    ps.append(P_(DECK, (0, 0, 160), label="Fan deck, folded PP sheet"))
    ps.append(P_(GASKET, (0, 0, 240), label="Deck gasket, EPDM foam"))
    ps.append(P_(LABEL, (0, -120, 160), label="Label"))
    ps = [p for p in ps]
    named = [p for p in ps if p.name]
    # unnamed duplicates are merged into their named first item so the key has one line per component
    merged = []
    for p in ps:
        if p.name:
            merged.append(p)
        else:
            q = merged[-1]
            q.shape = Compound(children=[Pos(*q.explode) * q.shape, Pos(*p.explode) * p.shape])
            q.explode = (0, 0, 0)
    return bv.overview(merged, OUT / "overview.png", title=f"{PROJECT}: filter cube kit components in build order",
                       subtitle="Every component, pulled apart and numbered in build order; the box fan is the facility's own; plan, not yet built",
                       size=(11, 9), key=True, elev=22, azim=-50)


SHEETS = {
    101: (TRAY, "Base tray: making sketch",
          "4 mm twin-wall corrugated polypropylene, one 24 x 36 in sheet; cut, scored and folded by hand",
          ["Cut a 609 mm square blank; flutes running the way the flaps fold up",
           "Mark a 30 mm line in from each edge; score it on the inside face 1 mm deep",
           "Cut out the four 30 mm corner squares; fold the flaps up to 90 deg",
           "Tray is 549 mm square outside, 541 mm inside: 1 mm clear of the panels",
           "Drill four 5.5 mm holes, 200 mm from the centre each way, for the feet",
           "Fits: the four panels stand on the floor inside the flaps",
           "Check: a 539 mm square of card drops in with a finger gap all round"]),
    102: (DECK, "Fan deck: making sketch",
          "4 mm twin-wall corrugated polypropylene, one 24 x 36 in sheet; cut, scored and folded by hand",
          ["Cut a 609 mm square blank; mark the three cut circles 280, 380 and 480 mm",
           "Cut the 480 mm circle for a 20 in box fan (the smaller lines suit 12 and 16 in fans)",
           "Score and fold four 30 mm flaps down, as for the tray",
           "Cut a 110 x 16 mm hand hole in two opposite flaps",
           "Stick the foam gasket as a 510 mm square round the opening, ends butted",
           "Fits: flaps drop over the panel tops; the fan frame sits on the gasket",
           "Check: the fan's guard circle sits inside the cut circle all round"]),
    103: (ANG[0], "Corner angle: making sketch",
          "Offcut of the same 4 mm sheet, 80 x 425 mm; scored and folded",
          ["Cut an 80 mm strip 425 mm long, flutes running along it",
           "Score down the centre line on the inside face; fold to 90 deg",
           "Legs 40 + 40 mm; make four",
           "Fits: over each vertical corner where two panels meet, 2 mm clear",
           "The horizontal straps hold the angles against the panels",
           "Check: the angle closes the seam with no daylight from inside"]),
    104: (FEET[0], "Foot: making sketch",
          "Polypropylene printed flat, 4 walls, 40 % infill; moulded PP at scale",
          ["Block 50 x 50 x 15 mm, edges rounded 2 mm",
           "5.5 mm hole through the centre",
           "Pocket underneath: 12 mm across, 8 mm deep, for the nut and washer",
           "Fits under the tray, 200 mm out from the centre each way",
           "One M5 x 20 bolt from inside the tray, washer each side, nut in the pocket",
           "Check: the cube stands without rocking on a flat floor"]),
}


def sheets(which=None):
    nb_all = [TRAY, DECK, ANG[0], FEET[0]]
    for no, (name, title, mat, notes) in SHEETS.items():
        if which and str(no) not in which:
            continue
        part = P_(name)
        nb = [P_(n) for n in nb_all if n != name] + [panel("north"), panel("west")]
        print(bv.component_sheet(part, nb, PROJECT, f"CAR-DWG-{no}", title, mat, notes, DATE))


def _window(parts, lo, hi):
    win = Pos(*[(a + b) / 2 for a, b in zip(lo, hi)]) * Box(*[b - a for a, b in zip(lo, hi)])
    out = []
    for p in parts:
        try:
            s = p.shape & win
            if s.volume > 1e-3:
                out.append(Part(p.name, s, p.color, p.bom))
        except Exception:
            pass
    return out


def joints(which=None):
    J = {
        1: ("Joint 1: panel foot in the tray flap, and a foot bolted under the tray (cut open)",
            [P_(TRAY), panel("east"), panel("south"), P_(FEET[3]), bolts(4), P_(ANG[3]), P_(VS[1])], (150, -290, -5), (300, -150, 80), "+Y"),
        2: ("Joint 2: corner angle over the seam where two panels meet, held by a strap (seen from above)",
            [panel("north"), panel("east"), P_(ANG[0]), P_(HS[0]), P_(HB[0])], (180, 180, 150), (300, 300, 210), None),
        3: ("Joint 3: deck flap over the panel tops, foam gasket and the fan frame on it (cut open)",
            [panel("north"), panel("east"), P_(DECK), P_(GASKET), fan(), P_(VS[0]), P_(ANG[0])], (150, 150, 470), (300, 300, 660), "-Y"),
    }
    for k, (title, ps, lo, hi, cut) in J.items():
        if which and str(k) not in which:
            continue
        print(bv.joint(_window(ps, lo, hi), OUT / f"joint-{k:02d}.png", title,
                       subtitle="Close-up from the model; parts named", cut=cut, elev=24, azim=-55))


def steps(which=None):
    S = {
        1: ("Step 1: bolt the four feet under the tray, bolt heads inside", [P_(TRAY)], [],
            [P_(n, (0, 0, -60)) for n in FEET] + [Part(f"M5 bolt set (foot {i})", bolts(i).shape, "#9CA3AF", 8, (0, 0, 60)) for i in range(1, 5)]),
        2: ("Step 2: stand the four panels in the tray in a pinwheel, airflow arrows pointing in", [P_(TRAY)] + [P_(n) for n in FEET], [],
            [panel(s, ex) for s, ex in zip(SIDES, [(0, 0, 150)] * 4)]),
        3: ("Step 3: fit a corner angle over each vertical seam", [P_(TRAY)] + [panel(s) for s in SIDES], [],
            [P_(n, ex) for n, ex in zip(ANG, [(90, 90, 0), (-90, 90, 0), (-90, -90, 0), (90, -90, 0)])]),
        4: ("Step 4: run two straps round the panels at 180 and 360 mm and pull them snug", [P_(TRAY)] + [panel(s) for s in SIDES] + [P_(n) for n in ANG], [],
            [P_(HS[0], (0, 0, -60)), P_(HB[0], (0, 0, -60)), P_(HS[1], (0, 0, 60)), P_(HB[1], (0, 0, 60))]),
        5: ("Step 5: stick the foam gasket on the deck, then drop the deck over the panel tops", [P_(TRAY)] + [panel(s) for s in SIDES] + [P_(n) for n in ANG],
            [], [P_(DECK, (0, 0, 150)), P_(GASKET, (0, 0, 220))]),
        6: ("Step 6: set the box fan on the gasket, blowing up, cord to the back", [P_(TRAY), P_(DECK), P_(GASKET)] + [panel(s) for s in SIDES], [],
            [Part("Existing 20 in box fan (not in the kit)", fan().shape, "#9CA3AF", None, (0, 0, 200))]),
        7: ("Step 7: run the two hold-down straps over the fan frame and under the tray; fit the label", [P_(TRAY), P_(DECK)] + [panel(s) for s in SIDES],
            [fan()], [P_(VS[0], (0, 0, 120)), P_(VB[0], (0, 0, 120)), P_(VS[1], (0, 0, 120)), P_(VB[1], (0, 0, 120)), P_(LABEL, (0, -80, 0))]),
    }
    for k, (title, done, ctx, new) in S.items():
        if which and str(k) not in which:
            continue
        print(bv.step(done, new, OUT / f"step-{k:02d}.png", title, context=ctx, size=(8, 7), elev=22, azim=-50, label_done=False))


if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else "all"), sys.argv[2:]
    if cmd in ("overview", "all"):
        print(overview())
    if cmd in ("sheets", "all"):
        sheets(args)
    if cmd in ("joints", "all"):
        joints(args)
    if cmd in ("steps", "all"):
        steps(args)

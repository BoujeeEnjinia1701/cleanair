"""CleanAir Retrofit Kit: product appearance model (kit 1.9), TRL 3, option CA2 (carried; choice awaiting Amish).

Built from components("CA2") in cad/src/model.py with every part used as it is, so every main dimension comes from
the model. Only scale context is added: a standing 1.75 m mannequin from .kit/context_parts.py, on the same floor
(z = 0) as the cube's feet, and a half-cut copy of the kit for the cutaway render. The box fan is the facility's own
and is shown as context. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.
Groups: "shell" (outside), "internal" (panels' media, gasket, bolts), "context" (fan, person), "cut" (half section).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot  # noqa: E402
import model as M  # noqa: E402

TITLE = "CleanAir Retrofit Kit: filter cube on an existing box fan"
_INTERNAL = ("pleated media", "gasket", "bolt", "washer", "nut")
PERSON_X = -M.P["TRAY"] / 2 - 450.0

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 14, "az": -40, "args": ["--lens=50"],
     "note": "On a ward floor beside a 1.75 m person, seen from the front right and slightly above (about 14 deg elevation); "
             "cube 576 mm across the buckles and 639 mm high with the facility's own 20 in box fan on top"},
    {"name": "studio", "groups": ["shell", "internal"], "explode": False, "el": 24, "az": -40, "args": [],
     "note": "Studio view from the front right and above (about 24 deg elevation): four MERV-13 panels in the folded tray, "
             "corner strips and straps, fan deck and foam seal; fan not shown"},
    {"name": "cutaway", "groups": ["cut"], "explode": False, "el": 12, "az": -90, "args": [],
     "note": "Half section seen from the front (about 12 deg elevation): panels, open cube interior, deck opening and foam "
             "seal under the fan frame, tray on its feet"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 22, "az": -50, "args": [],
     "note": "Exploded view from the front right and above (about 22 deg elevation): panels pulled outward, deck and seal "
             "lifted, tray and feet lowered"},
]


def product_parts():
    import context_parts
    out = []
    cutter = Pos(0, 500, 500) * Box(1600, 1000, 1600)
    for q in M.components("CA2"):
        d = dict(q)
        if q["kind"] == "context":
            d["group"] = "context"
            out.append(d)
        else:
            d["group"] = "internal" if any(k in q["name"] for k in _INTERNAL) else "shell"
            out.append(d)
        if "label" in q["name"].lower():
            continue
        try:
            h = q["shape"] & cutter
            if h.volume > 1e-3:
                c = dict(q)
                c["shape"], c["group"], c["name"] = h, "cut", q["name"] + " (section)"
                out.append(c)
        except Exception:
            pass
    man = Pos(PERSON_X, 0, 0) * Rot(0, 0, 20) * context_parts.mannequin(1750.0, "stand")
    out.append(dict(name="Person (scale)", shape=man, material="clay", material_name="skin", color="#9C9C9E", kind="context",
                    bom=None, group="context", explode=(0, 0, 0), note=""))
    return out


if __name__ == "__main__":
    from collections import Counter
    print(Counter(p["group"] for p in product_parts()))

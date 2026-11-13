"""CleanAir Retrofit Kit. Parametric model (kit 1.9 interface, STANDARDS section 24), detail level D3.

Run from the repo root:  python .kit/cad_check.py --export
Every main dimension is in PARAMS; docs/04-calcs/sizing.py (CAR-CAL-001) and stem_check.py (CAR-STM-001) read it.

Units mm. Z up, floor at z = 0. The existing fan or grille in each option is a context part (kind "context"):
it is not part of the kit, it is not in the BOM and it is drawn only to show where the kit goes.

Options (CAR-OPT-001; the recommendation is proposed, awaiting Amish):
  CA1  Collar and cassette (team concept, iteration 2): a silicone collar sleeve stretched over the front guard rim
       of an existing shrouded fan and clamped with a tension strap, a polypropylene snap-ring adaptor, and one flat
       20 x 20 x 2 in MERV-13 cassette held in rails by two turn buttons. The UV-C strip is removed (CAR-DEC-001 F2).
  CA2  Filter cube (Corsi-Rosenthal type): four 20 x 20 x 2 in MERV-13 panels stand in a scored and folded
       corrugated polypropylene tray, closed at the top by a fan deck with a 480 mm opening and a foam gasket; an
       existing 20 in box fan sits on the deck and draws air in through all four panels. Corner angles and two
       horizontal straps hold the panels; two vertical straps hold the fan. Four printed feet lift the tray so the
       straps pass under it.
  CA3  Return-grille cassette: a polypropylene cassette with one 20 x 20 x 2 in MERV-13 panel, a foam gasket and
       four magnet cups clips onto an existing steel return grille, so the building's own air handler is the fan.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from build123d import Box, Cylinder, Location, Plane, Polygon, Pos, Rot, Torus, extrude

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "CleanAir Retrofit Kit"
OPTIONS = {"CA1": "Collar and flat cassette on a shrouded fan", "CA2": "Filter cube on a box fan (Corsi-Rosenthal type)",
           "CA3": "Return-grille cassette on a ducted system"}
PRINCIPLES = {
    "CA1": "A silicone collar seals one flat MERV-13 cassette to the front of an existing shrouded fan; all the air "
           "the fan moves must pass one 0.25 m2 panel, so the weak fan curve sets a low airflow.",
    "CA2": "An existing box fan on a deck draws air in through four MERV-13 panels (about 1 m2 of face), so the "
           "face velocity and the pressure drop stay within what a box fan can develop.",
    "CA3": "A gasketed MERV-13 cassette on a return grille uses the building air handler as the fan; clean air "
           "delivery depends on that system's airflow and run time.",
}
CHOSEN = "CA2"   # carried to the drawing, BOM and build plan. Proposed, awaiting Amish (CAR-DEC-001 D1); not decided
OPTION_VIEWS = {
    "CA1": dict(el=14, az=-35, scale="person", keep_context=True, ground_z=0.0),
    "CA2": dict(el=20, az=-40, scale="person", keep_context=True, ground_z=0.0),
    "CA3": dict(el=12, az=-35, scale="person", keep_context=True, ground_z=0.0),
}
# the silicone collar sleeve is stretched over the fan guard rim and the adaptor spigot by design; it shows as overlap
ALLOWED_CONTACTS = [("Silicone collar sleeve", "")]

PARAMS = {
    # bought MERV-13 panel: nominal 20 x 20 x 2 in; actual 495 x 495 x 44 mm (19.5 x 19.5 x 1.75 in, to confirm)
    "FILT_W": 495.0, "FILT_T": 44.0, "FILT_LIP": 15.0, "FILT_BAND_T": 1.5, "PLEATS": 24, "MEDIA_T": 0.8,
    "FILT_FACE_M2": 0.495 * 0.495,
    # CA2 filter cube
    "SHEET_T": 4.0,              # 4 mm corrugated polypropylene (twin-wall), flutes run vertical in the flaps
    "SHEET_BLANK": (610.0, 914.0),   # one 24 x 36 in sheet per tray or deck blank
    "CUBE": 539.0,               # outside of the four panels in a pinwheel: FILT_W + FILT_T
    "TRAY": 549.0, "FLAP": 30.0, "TRAY_Z": 15.0,   # tray outside, flap height, underside of the tray floor
    "DECK_HOLE_D": 480.0,        # opening under a 20 in box fan's blades
    "KNOCKOUT_D": (280.0, 380.0, 480.0),   # scored cut lines for 12, 16 and 20 in fans
    "GASKET_W": 8.0, "GASKET_H": 10.0, "GASKET_SQ": 510.0,   # 5/16 x 9/16 in EPDM weatherstrip, compressed to 10 mm
    "BOXFAN": (521.0, 552.0, 108.0),   # 20 in box fan, 20.5 x 21.75 x 4.25 in (Lasko 3733 listing), lying flat
    "ANGLE_LEG": 40.0, "ANGLE_Z": (54.0, 479.0),
    "ANGLE_GAP": 2.0, "STRAP_W": 25.0, "STRAP_T": 1.5, "STRAP_Z": (180.0, 360.0), "VSTRAP_Y": 261.0,  # over the solid fan frame outside the 484 mm guard (CAR-DEC-001 F3)
    "FOOT": (50.0, 50.0, 15.0), "FOOT_XY": 200.0, "FOOT_POCKET": (12.0, 8.0),
    # CA1 collar and cassette on a 16 in (406 mm) pedestal fan, axis at z = 1150, blowing toward -Y
    "FAN1_D": 406.0, "FAN1_Z": 1150.0, "GUARD_R": 225.0, "GUARD_Y": -75.0,
    "SLEEVE": (226.0, 3.0, -60.0, -130.0), "SPIGOT": (220.0, 225.5, -100.0, -130.0),
    "FLANGE": (600.0, 5.0), "CASSETTE": (539.0, 50.0, 22.0),
    # CA3 return-grille cassette, grille centre at z = 600 on a wall at y = 0
    "GRILLE": (560.0, 508.0, 600.0), "CAS3": (600.0, 45.0, 5.0), "MAGNET": (16.0, 6.0),
}
P = PARAMS
W, T, LIP, BT = P["FILT_W"], P["FILT_T"], P["FILT_LIP"], P["FILT_BAND_T"]
ST = P["SHEET_T"]
H_CUBE = P["CUBE"] / 2
H_TRAY = P["TRAY"] / 2
Z_FLOOR = P["TRAY_Z"] + ST           # top of the tray floor: the panels stand here
Z_TOP = Z_FLOOR + W                  # top of the panels
Z_DECK = Z_TOP + 0.5                 # underside of the deck plate
Z_FAN = Z_DECK + ST + P["GASKET_H"]  # underside of the box fan

C_PP, C_PP2, C_SIL, C_FILT, C_MEDIA = "#E9EEF0", "#2F7F86", "#C2410C", "#D8C9A0", "#F4F2EC"
C_STRAP, C_FOAM, C_FAN = "#1F2937", "#151617", "#9CA3AF"


def _p(name, shape, mat, kind="made", bom=None, explode=(0, 0, 0), color=None, group="shell", note=""):
    return part(name, shape, mat, kind=kind, bom=bom, group=group, explode=explode, color=color, note=note)


def loc(origin, x_dir, z_dir):
    return Location(Plane(origin=origin, x_dir=x_dir, z_dir=z_dir))


def ring_box(ox, oy, oz, ix, iy, iz):
    """A rectangular ring: outer box less inner box, both centred on the origin."""
    return Box(ox, oy, oz) - Box(ix, iy, iz)


def bolt_set(d, grip, location, tag, bom=None, explode=(0, 0, 0)):
    """ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut, placed by a Location (local +Z is the head side)."""
    out = []
    for n, s in cp.hex_bolt_set(d, grip):
        out.append(_p(f"{n}, {tag}", location * s, "zinc_plated", "fastener", bom, explode))
    return out


# ---------------------------------------------------------------------------------------------------------
# the bought MERV-13 panel (all options): card frame and pleated media
# ---------------------------------------------------------------------------------------------------------
def _panel_shapes():
    """Panel in local axes: face in X (0 to W) and Z (0 to W), depth in Y (0 to T)."""
    band = Pos(W / 2, T / 2, W / 2) * ring_box(W, T, W, W - 2 * BT, T + 2, W - 2 * BT)
    lip = ring_box(W, BT, W, W - 2 * LIP, BT + 2, W - 2 * LIP)
    frame = band + Pos(W / 2, BT / 2, W / 2) * lip + Pos(W / 2, T - BT / 2, W / 2) * lip
    n, mt = P["PLEATS"], P["MEDIA_T"]
    x0, x1, y0, y1 = 2.0, W - 2.0, BT + 0.3, T - BT - 0.3
    xs = [x0 + i * (x1 - x0) / (2 * n) for i in range(2 * n + 1)]
    top = [(x, y1 if i % 2 else y0 + mt) for i, x in enumerate(xs)]
    bot = [(x, y - mt) for x, y in reversed(top)]
    media = Pos(0, 0, 2.0) * extrude(Polygon(*(top + bot), align=None), W - 4.0, dir=(0, 0, 1))
    return frame, media


def panel(tag, location, bom=None, explode=(0, 0, 0)):
    frame, media = _panel_shapes()
    return [_p(f"MERV-13 panel frame{tag}", location * frame, "label", "bought", bom, explode, C_FILT),
            _p(f"MERV-13 pleated media{tag}", location * media, "insulated_white", "bought", bom, explode, C_MEDIA)]


# ---------------------------------------------------------------------------------------------------------
# option CA2: filter cube on a box fan (recommended, proposed)
# ---------------------------------------------------------------------------------------------------------
def _score(length, x, z, axis):
    """A 1 mm V score on the inside of a fold line, as cut into twin-wall sheet before folding."""
    g = Rot(0, 45, 0) * Box(1.4, length, 1.4) if axis == "y" else Rot(45, 0, 0) * Box(length, 1.4, 1.4)
    return Pos(x, 0, z) * g if axis == "y" else Pos(0, x, z) * g


def tray():
    """Base tray: one 610 mm square blank of 4 mm corrugated PP, scored and folded into a 549 mm tray with 30 mm
    flaps; four 5.5 mm holes for the feet bolts."""
    holes = [(sx * P["FOOT_XY"], sy * P["FOOT_XY"], 5.5) for sx in (-1, 1) for sy in (-1, 1)]
    s = Pos(0, 0, P["TRAY_Z"]) * cp.sheet(P["TRAY"], P["TRAY"], ST, holes=holes, r_corner=2.0, edge=0.0)
    f = P["FLAP"]
    for k in range(4):
        flap = Pos(H_TRAY - ST / 2, 0, P["TRAY_Z"] + f / 2) * Box(ST, P["TRAY"] - 2 * ST - 1.0, f)
        s = s + Rot(0, 0, 90 * k) * flap
    for k in range(4):
        s = s - Rot(0, 0, 90 * k) * Pos(H_TRAY - ST, 0, Z_FLOOR) * Rot(0, 45, 0) * Box(1.4, P["TRAY"] - 20, 1.4)
    return cp.break_edges(s, 0.3)


def deck():
    """Fan deck: the same blank folded the other way, a 480 mm opening for a 20 in box fan, 30 mm flaps down."""
    s = Pos(0, 0, Z_DECK) * cp.sheet(P["TRAY"], P["TRAY"], ST, holes=[(0, 0, P["DECK_HOLE_D"])], r_corner=2.0, edge=0.0)
    f = P["FLAP"]
    for k in range(4):
        flap = Pos(H_TRAY - ST / 2, 0, Z_DECK + ST - f / 2) * Box(ST, P["TRAY"] - 2 * ST - 1.0, f)
        s = s + Rot(0, 0, 90 * k) * flap
    for k in range(4):
        s = s - Rot(0, 0, 90 * k) * Pos(H_TRAY - ST, 0, Z_DECK) * Rot(0, 45, 0) * Box(1.4, P["TRAY"] - 20, 1.4)
    hh = Pos(0, -H_TRAY + ST / 2, Z_DECK + ST - f / 2) * Box(ST + 2, 110, 16)   # hand hole in the -Y flap
    s = s - hh - Rot(0, 0, 180) * hh
    return cp.break_edges(s, 0.3)


def corner_angle(k):
    """Corner angle: a 80 mm strip of 4 mm corrugated PP scored down its centre and folded to 90 deg."""
    a, (z0, z1) = P["ANGLE_LEG"], P["ANGLE_Z"]
    ang = cp.angle(a, a, ST, z1 - z0)
    c = H_CUBE + P["ANGLE_GAP"] + ST
    return Rot(0, 0, 90 * k) * Pos(c, c, z0) * Rot(0, 0, 180) * ang


def cube_panels(bom=1):
    out = []
    for k, side in enumerate(("north", "west", "south", "east")):
        location = Rot(0, 0, 90 * k) * Pos(-H_CUBE, H_CUBE - T, Z_FLOOR)
        ex = [(0, 120, 0), (-120, 0, 0), (0, -120, 0), (120, 0, 0)][k]
        out += panel(f" ({side})", location, bom, ex)
    return out


def h_strap(z, tag, bom_strap=5):
    o = H_CUBE + P["ANGLE_GAP"] + ST + 0.5 + P["STRAP_T"]
    s = Pos(0, 0, z) * ring_box(2 * o, 2 * o, P["STRAP_W"], 2 * (o - P["STRAP_T"]), 2 * (o - P["STRAP_T"]), P["STRAP_W"] + 2)
    buckle = Pos(0, o + 7.0, z) * (Box(40, 14, 32) - Pos(0, 0, 0) * Box(30, 4, 26.5))
    return [_p(f"Cam strap, 25 mm, horizontal{tag}", s, "rope", "bought", bom_strap, (0, 0, 0), C_STRAP),
            _p(f"Cam buckle, horizontal strap{tag}", cp.break_edges(buckle, 0.8), "zinc_plated", "bought", bom_strap, (0, 60, 0))]


def v_strap(y, tag, bom_strap=5):
    x0 = H_CUBE + P["ANGLE_GAP"] + ST + 0.5 + P["STRAP_T"] + 2.0 + P["STRAP_T"]   # outside the horizontal straps
    z_top = Z_FAN + P["BOXFAN"][2] + 0.5
    zb = P["TRAY_Z"] - P["STRAP_T"]
    zt = z_top + P["STRAP_T"]
    outer = Pos(0, y, (zb + zt) / 2) * Box(2 * x0, P["STRAP_W"], zt - zb)
    inner = Pos(0, y, (zb + zt) / 2) * Box(2 * (x0 - P["STRAP_T"]), P["STRAP_W"] + 2, zt - zb - 2 * P["STRAP_T"])
    buckle = Pos(x0 + 7.0, y, 300.0) * (Box(14, 40, 32) - Box(4, 30, 26.5))
    return [_p(f"Cam strap, 25 mm, fan hold-down{tag}", outer - inner, "rope", "bought", bom_strap, (0, 0, 80), C_STRAP),
            _p(f"Cam buckle, fan hold-down strap{tag}", cp.break_edges(buckle, 0.8), "zinc_plated", "bought", bom_strap, (60, 0, 80))]


def gasket():
    sq, w, h = P["GASKET_SQ"], P["GASKET_W"], P["GASKET_H"]
    g = Pos(0, 0, Z_DECK + ST + h / 2) * ring_box(sq, sq, h, sq - 2 * w, sq - 2 * w, h + 2)
    return _p("Fan deck gasket, EPDM foam weatherstrip", cp.break_edges(g, 1.0), "epdm", "bought", 6, (0, 0, 40), C_FOAM)


def feet_and_bolts(bom_foot=7, bom_bolt=8):
    fx, fy, fz = P["FOOT"]
    pd, ph = P["FOOT_POCKET"]
    out = []
    for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        x, y = sx * P["FOOT_XY"], sy * P["FOOT_XY"]
        f = Pos(x, y, fz / 2) * Box(fx, fy, fz)
        f = cp.break_edges(f, 2.0)
        f = f - Pos(x, y, fz / 2) * Cylinder(2.75, fz + 2) - Pos(x, y, ph / 2 - 0.5) * Cylinder(pd / 2, ph + 1)
        out.append(_p(f"Foot {i + 1}, printed PP", f, "hdpe_natural", "made", bom_foot, (0, 0, -40), C_PP2))
        out += bolt_set(5, ST + fz - ph, Location((x, y, Z_FLOOR)), f"foot {i + 1}", bom_bolt, (0, 0, 40))
    return out


def label():
    lb = Pos(0, -H_TRAY - 0.4, Z_DECK + ST - 12.0) * Rot(0, 0, 0) * Pos(160, 0, 0) * Box(150, 0.8, 18)
    return _p("Instruction and warning label", cp.break_edges(lb, 0.3), "label", "bought", 9, (0, -30, 0), "#F4F1E6")


def box_fan(z0=None, ctx_name="Existing 20 in box fan (not in the kit)"):
    """Context: a 20 in box fan lying flat, blowing up. Frame, guard rings, three blades and the motor."""
    z0 = Z_FAN if z0 is None else z0
    w, d, h = P["BOXFAN"]
    frame = Pos(0, 0, z0 + h / 2) * Box(w, d, h) - Pos(0, 0, z0 + h / 2) * Cylinder(242, h + 2)
    frame = cp.break_edges(frame, 6.0)
    parts = [part(ctx_name, frame, "hdpe_natural", kind="context", group="context", color="#E5E7EB")]
    rings = None
    for r in (80, 150, 220):
        for zz in (z0 + 3, z0 + h - 3):
            t = Pos(0, 0, zz) * Torus(r, 1.6)
            rings = t if rings is None else rings + t
    parts.append(part("Box fan guard (context)", rings, "zinc_plated", kind="context", group="context", color="#D1D5DB"))
    motor = Pos(0, 0, z0 + h / 2) * Cylinder(55, 60)
    parts.append(part("Box fan motor (context)", motor, "matte_black", kind="context", group="context"))
    for k in range(3):
        bl = Rot(0, 0, 120 * k) * Pos(140, 0, z0 + h / 2) * Rot(25, 0, 0) * Box(180, 110, 2.0)
        parts.append(part(f"Box fan blade {k + 1} (context)", bl, "hdpe_natural", kind="context", group="context", color="#CBD5E1"))
    return parts


def option_ca2():
    out = []
    out.append(_p("Base tray, corrugated PP 4 mm, scored and folded", tray(), "hdpe_natural", "made", 2, (0, 0, -80), C_PP))
    out += cube_panels(1)
    for k in range(4):
        out.append(_p(f"Corner angle {k + 1}, corrugated PP 4 mm, scored and folded", corner_angle(k), "hdpe_natural", "made", 4,
                      [(70, 70, 0), (-70, 70, 0), (-70, -70, 0), (70, -70, 0)][k], C_PP))
    out.append(_p("Fan deck, corrugated PP 4 mm, scored and folded", deck(), "hdpe_natural", "made", 3, (0, 0, 80), C_PP))
    out.append(gasket())
    out += h_strap(P["STRAP_Z"][0], " (lower)") + h_strap(P["STRAP_Z"][1], " (upper)")
    out += v_strap(P["VSTRAP_Y"], " (+Y)") + v_strap(-P["VSTRAP_Y"], " (-Y)")
    out += feet_and_bolts()
    out.append(label())
    out += box_fan()
    return out


# ---------------------------------------------------------------------------------------------------------
# option CA1: collar and flat cassette on a shrouded pedestal fan (team concept)
# ---------------------------------------------------------------------------------------------------------
def pedestal_fan(zc):
    gr, gy = P["GUARD_R"], P["GUARD_Y"]
    ps = []
    base = Pos(0, 180, 15) * Cylinder(180, 30)
    pole = Pos(0, 180, (30 + zc - 120) / 2) * Cylinder(15, zc - 150)
    neck = Pos(0, 180, zc - 100) * Box(40, 40, 120)
    motor = Pos(0, 150, zc) * Rot(90, 0, 0) * Cylinder(70, 150)
    rim_f = Pos(0, gy, zc) * Rot(90, 0, 0) * Torus(gr, 3.0)
    rim_r = Pos(0, 75, zc) * Rot(90, 0, 0) * Torus(gr, 3.0)
    band = Pos(0, 0, zc) * Rot(90, 0, 0) * (Cylinder(gr + 1.5, 150) - Cylinder(gr - 1.5, 152))
    spokes = None
    for k in range(12):
        s = Pos(0, gy, zc) * Rot(0, 30 * k, 0) * Pos(gr / 2, 0, 0) * Box(gr, 2.0, 2.0)
        spokes = s if spokes is None else spokes + s
    for n, s, m in (("Pedestal fan base (context)", base, "matte_black"), ("Pedestal fan pole (context)", pole, "stainless"),
                    ("Pedestal fan neck (context)", neck, "matte_black"), ("Pedestal fan motor (context)", motor, "hdpe_natural"),
                    ("Existing 16 in pedestal fan guard rim, front (not in the kit)", rim_f, "zinc_plated"),
                    ("Pedestal fan guard rim, rear (context)", rim_r, "zinc_plated"), ("Pedestal fan guard band (context)", band, "zinc_plated"),
                    ("Pedestal fan guard spokes (context)", spokes, "zinc_plated")):
        ps.append(part(n, s, m, kind="context", group="context"))
    for k in range(3):
        bl = Pos(0, 0, zc) * Rot(0, 120 * k, 0) * Pos(110, 0, 0) * Rot(0, 0, 20) * Box(170, 2.0, 90)
        ps.append(part(f"Pedestal fan blade {k + 1} (context)", bl, "hdpe_natural", kind="context", group="context", color="#CBD5E1"))
    return ps


def option_ca1():
    zc = P["FAN1_Z"]
    r_in, t, y0, y1 = P["SLEEVE"]
    s0, s1, sy0, sy1 = P["SPIGOT"]
    fw, ft = P["FLANGE"]
    cw, cd, cb = P["CASSETTE"]
    out = []
    ax = lambda y, z=zc: Pos(0, (y0 + y1) / 2 if y is None else y, z)
    sleeve = Pos(0, (y0 + y1) / 2, zc) * Rot(90, 0, 0) * (Cylinder(r_in + t, y0 - y1) - Cylinder(r_in, y0 - y1 + 2))
    out.append(_p("Silicone collar sleeve, 3 mm", cp.break_edges(sleeve, 0.8), "epdm", "made", None, (0, -60, 0), C_SIL))
    strap = Pos(0, -77.5, zc) * Rot(90, 0, 0) * (Cylinder(r_in + t + 2.0, 25) - Cylinder(r_in + t + 0.5, 27))
    out.append(_p("Tension strap, 25 mm, collar", strap, "rope", "bought", None, (0, -60, 0), C_STRAP))
    buckle = Pos(0, -77.5, zc + r_in + t + 9.0) * (Box(32, 40, 14) - Box(26.5, 30, 4))
    out.append(_p("Cam buckle, collar strap", cp.break_edges(buckle, 0.8), "zinc_plated", "bought", None, (0, -60, 40)))
    # snap-ring adaptor: spigot and a square flange with bolt holes for the rails and the turn buttons
    spig = Pos(0, (sy0 + sy1) / 2, zc) * Rot(90, 0, 0) * (Cylinder(s1, sy0 - sy1) - Cylinder(s0, sy0 - sy1 + 2))
    fl = Pos(0, sy1 - ft / 2, zc) * Box(fw, ft, fw) - Pos(0, sy1 - ft / 2, zc) * Rot(90, 0, 0) * Cylinder(s0, ft + 2)
    holes = [(sx * 200, zc + sz * 290) for sx in (-1, 1) for sz in (-1, 1)] + [(sx * 285, zc) for sx in (-1, 1)]
    for hx, hz in holes:
        fl = fl - Pos(hx, sy1 - ft / 2, hz) * Rot(90, 0, 0) * Cylinder(2.75, ft + 2)
    ring = cp.break_edges(spig, 0.6) + fl
    out.append(_p("Snap-ring adaptor, PP (spigot and flange)", ring, "hdpe_natural", "made", None, (0, -120, 0), C_PP2))
    y_f = sy1 - ft                  # front face of the flange
    g = Pos(0, y_f - 1.5, zc) * ring_box(cw - 4, 3, cw - 4, cw - 20, 5, cw - 20)
    out.append(_p("Cassette gasket, EPDM foam", g, "epdm", "bought", None, (0, -150, 0), C_FOAM))
    yc0 = y_f - 3.0                 # back face of the cassette
    cas = Pos(0, yc0 - cd / 2, zc) * ring_box(cw, cd, cw, W + 2, cd + 2, W + 2)
    cas = cas + Pos(0, yc0 - cd + 1.5, zc) * ring_box(cw, 3, cw, W - 30, 5, W - 30)
    out.append(_p("Cassette frame, PP", cp.break_edges(cas, 0.8), "hdpe_natural", "made", None, (0, -220, 0), C_PP))
    out += panel(" (cassette)", loc((-W / 2, yc0 - 0.5, zc - W / 2), (1, 0, 0), (0, 0, 1)) * Pos(0, -T, 0), None, (0, -220, 0))
    # rails: folded PP angles above and below the cassette, bolted to the flange
    a_up, a_fw = 40.0, cd + 4.0
    for sz, nm in ((1, "top"), (-1, "bottom")):
        ang = cp.angle(a_up, a_fw, 4.0, 560.0)
        holes_r = []
        if sz > 0:
            L = loc((-280, y_f, zc + cw / 2 + 0.5), (0, 0, 1), (1, 0, 0))
        else:
            L = loc((280, y_f, zc - cw / 2 - 0.5), (0, 0, -1), (-1, 0, 0))
        rail = L * ang
        for sx in (-1, 1):
            rail = rail - Pos(sx * 200, y_f - 2, zc + sz * 290) * Rot(90, 0, 0) * Cylinder(2.75, 8)
        out.append(_p(f"Cassette rail, {nm}, PP angle", rail, "hdpe_natural", "made", None, (0, -150, sz * 40), C_PP2))
        for sx in (-1, 1):
            out += bolt_set(5, 4.0 + ft, loc((sx * 200, y_f - 4.0, zc + sz * 290), (1, 0, 0), (0, -1, 0)), f"rail {nm} {sx:+d}")
    # turn buttons at the sides: boss to the cassette front face, lever over its edge
    y_front = yc0 - cd
    for sx in (-1, 1):
        boss = Pos(sx * 285, (y_f + y_front) / 2, zc) * Rot(90, 0, 0) * Cylinder(8, y_f - y_front)
        lever = Pos(sx * 270, y_front - 3, zc) * Box(50, 6, 20)
        tb = cp.break_edges(lever, 1.0) + boss - Pos(sx * 285, (y_f + y_front) / 2 - 3, zc) * Rot(90, 0, 0) * Cylinder(2.75, y_f - y_front + 10)
        out.append(_p(f"Turn button {'+X' if sx > 0 else '-X'}, PP", tb, "hdpe_natural", "made", None, (sx * 40, -60, 0), C_PP2))
        out += bolt_set(5, (y_f - y_front) + 6 + ft, loc((sx * 285, y_front - 6, zc), (1, 0, 0), (0, -1, 0)), f"turn button {sx:+d}")
    out += pedestal_fan(zc)
    return out


# ---------------------------------------------------------------------------------------------------------
# option CA3: return-grille cassette
# ---------------------------------------------------------------------------------------------------------
def option_ca3():
    gface, gopen, zc = P["GRILLE"]
    ow, depth, back = P["CAS3"]
    md, mt = P["MAGNET"]
    out = []
    wall = Pos(0, 6.5, 1200) * Box(1600, 13, 2400) - Pos(0, 6.5, zc) * Box(gopen, 15, gopen)
    out.append(part("Wall, plasterboard (context)", wall, "insulated_white", kind="context", group="context", color="#EDEDE8"))
    gr = Pos(0, -1.5, zc) * ring_box(gface, 3, gface, gopen - 20, 5, gopen - 20)
    for k in range(9):
        gr = gr + Pos(0, -1.5, zc - 220 + 55 * k) * Rot(30, 0, 0) * Box(gopen - 20, 1.2, 30)
    out.append(part("Existing steel return grille (not in the kit)", gr, "painted_steel", kind="context", group="context", color="#D1D5DB"))
    duct = Pos(0, 13 + 150, zc) * ring_box(gopen + 4, 300, gopen + 4, gopen, 302, gopen)
    out.append(part("Return duct (context)", duct, "galvanised", kind="context", group="context"))
    y_g = -3.0                                  # grille face
    g = Pos(0, y_g - 3.0, zc) * ring_box(500, 6, 500, 484, 8, 484)
    out.append(_p("Grille gasket, EPDM foam", g, "epdm", "bought", None, (0, -80, 0), C_FOAM))
    yb = y_g - 6.0                              # back face of the cassette
    frame = Pos(0, yb - back / 2, zc) * ring_box(ow, back, ow, W - 30, back + 2, W - 30)
    frame = frame + Pos(0, yb - back - depth / 2, zc) * ring_box(ow, depth, ow, W + 2, depth + 2, W + 2)
    for sx in (-1, 1):
        for sz in (-1, 1):
            frame = frame - Pos(sx * 262, yb - back / 2, zc + sz * 262) * Rot(90, 0, 0) * Cylinder(2.75, back + 2)
            frame = frame - Pos(sx * 262, yb - back - depth / 2, zc + sz * 262) * Rot(90, 0, 0) * Cylinder(9.0, depth + 0.02)
            frame = frame - Pos(sx * 275, yb - back - depth + 9, zc + sz * 150) * Rot(90, 0, 0) * Cylinder(2.75, 20)
    out.append(_p("Grille cassette frame, PP", cp.break_edges(frame, 0.8), "hdpe_natural", "made", None, (0, -140, 0), C_PP))
    out += panel(" (grille cassette)", loc((-W / 2, yb - back - 0.5, zc - W / 2), (1, 0, 0), (0, 0, 1)) * Pos(0, -T, 0), None, (0, -200, 0))
    y_front = yb - back - depth
    for sz in (-1, 1):
        bar = Pos(0, y_front - 2.5, zc + sz * 150) * Box(ow - 20, 5, 20)
        for sx in (-1, 1):
            bar = bar - Pos(sx * 275, y_front - 2.5, zc + sz * 150) * Rot(90, 0, 0) * Cylinder(2.75, 7)
        out.append(_p(f"Retaining bar {'upper' if sz > 0 else 'lower'}, PP", cp.break_edges(bar, 1.0), "hdpe_natural", "made", None,
                      (0, -260, 0), C_PP2))
        for sx in (-1, 1):
            Lb = loc((sx * 275, y_front - 5.0, zc + sz * 150), (1, 0, 0), (0, -1, 0))
            out.append(_p(f"M5x16 hex bolt (ISO 4017), bar {sx:+d}{sz:+d}", Lb * Pos(0, 0, 1.0) * cp.hex_bolt(5, 16), "zinc_plated", "fastener"))
            out.append(_p(f"M5 washer (ISO 7089), bar {sx:+d}{sz:+d}", Lb * cp.washer(5), "zinc_plated", "fastener"))
    for sx in (-1, 1):
        for sz in (-1, 1):
            mg = Pos(sx * 262, y_g - mt / 2, zc + sz * 262) * Rot(90, 0, 0) * (Cylinder(md / 2, mt) - Cylinder(2.6, mt + 2))
            out.append(_p(f"Magnet cup {sx:+d}{sz:+d}, 16 mm", cp.break_edges(mg, 0.4), "zinc_plated", "bought", None, (0, -60, 0)))
            Lm = loc((sx * 262, yb - back, zc + sz * 262), (1, 0, 0), (0, -1, 0))
            out.append(_p(f"M5x10 hex bolt (ISO 4017), magnet {sx:+d}{sz:+d}", Lm * Pos(0, 0, 1.0) * cp.hex_bolt(5, 10), "zinc_plated", "fastener"))
            out.append(_p(f"M5 washer (ISO 7089), magnet {sx:+d}{sz:+d}", Lm * cp.washer(5), "zinc_plated", "fastener"))
    return out


def components(option="CA2"):
    return {"CA1": option_ca1, "CA2": option_ca2, "CA3": option_ca3}[option]()


if __name__ == "__main__":
    for k in OPTIONS:
        ps = components(k)
        real = [q for q in ps if q["kind"] != "context"]
        m = sum(cp.mass_kg(q) for q in real)
        print(k, len(real), "parts", f"{m:.2f} kg")

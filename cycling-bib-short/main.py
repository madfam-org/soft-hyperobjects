"""
Cycling bib short — Fashion Cabinet Garment Cartridge
(FC-500 rank #450, active_swim, no hardware — pure pattern).

The road cyclist's bib short: a high-compression lycra short held up not by a waistband but by
BIB STRAPS over the shoulders, so nothing constricts the belly in the aero position and the
chamois stays put. A panelled short (front, back, side) at strong negative ease, a chamois pad
window, and mesh bib straps that cross at the back. No waistband, no drawcord, no hardware.

Two real decisions:

  1. THE BIB STRAP LENGTH IS SOLVED TO THE TORSO. The strap runs from the short front over the
     shoulder to the short back; its length is the measured torso rise plus the shoulder span,
     clamped positive so it always reaches. No waistband means the strap IS the suspension.

  2. NEGATIVE EASE + ONE SHARED CROTCH. Front and back share ONE crotch point and one inseam so
     the leg cannot twist; the chamois window sits over the shared crotch.

Pieces: front (cut 2), back (cut 2), strap (cut 2). Made to measure to waist, hip, thigh girths,
inseam and torso rise. FC-500 lane 6 (active).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|strap|set

waist_girth = float(PARAM(lambda: waist_girth, 820.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
thigh_girth = float(PARAM(lambda: thigh_girth, 560.0))
inseam = float(PARAM(lambda: inseam, 220.0))
torso_rise = float(PARAM(lambda: torso_rise, 520.0))       # short waist to shoulder over the bib
strap_width = float(PARAM(lambda: strap_width, 60.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 14.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1300.0))
hip_girth = max(720.0, min(hip_girth, 1500.0))
thigh_girth = max(360.0, min(thigh_girth, 800.0))
inseam = max(120.0, min(inseam, 360.0))
torso_rise = max(360.0, min(torso_rise, 720.0))
strap_width = max(30.0, min(strap_width, 120.0))
negative_ease_pct = max(6.0, min(negative_ease_pct, 26.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
HIP_FIN = hip_girth * NEG
WAIST_FIN = waist_girth * NEG
THIGH_FIN = thigh_girth * NEG
QUARTER_HIP = HIP_FIN / 4.0
THIGH_HALF = THIGH_FIN / 2.0
RISE = inseam + 60.0                          # short body rise above the crotch
CROTCH_X = -QUARTER_HIP * 0.14
CROTCH_Y = 0.0
STRAP_LEN = max(120.0, torso_rise - RISE + QUARTER_HIP)   # solved, floored positive


def build_front():
    """Short front (cut 2). Waist at top (RISE), leg hem at bottom, chamois window marking over
    the crotch."""
    top = WAIST_FIN / 4.0
    hemw = THIGH_HALF
    edges = [
        fc.Edge("waist", [fc.Line(fc.P(0.0, RISE), fc.P(top, RISE))]),
        fc.Edge("side", [fc.Line(fc.P(top, RISE), fc.P(hemw, inseam))]),
        fc.Edge("hem", [fc.Line(fc.P(hemw, inseam), fc.P(CROTCH_X, inseam))]),
        fc.Edge("inseam", [fc.Line(fc.P(CROTCH_X, inseam), fc.P(CROTCH_X, CROTCH_Y))]),
        fc.Edge("centre_front", [fc.Bezier(fc.P(CROTCH_X, CROTCH_Y),
                                           fc.P(top * 0.2, RISE * 0.4),
                                           fc.P(0.0, RISE * 0.7), fc.P(0.0, RISE))]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"hem": 12.0},
        notches=[fc.Notch("side", 0.5, "hip"), fc.Notch("inseam", 0.5, "crotch")],
        grainline=fc.Grainline(fc.P(top * 0.5, RISE * 0.3), fc.P(top * 0.5, RISE * 0.85)),
        internals=[fc.Internal("chamois-window", [fc.P(CROTCH_X * 0.5, 20.0),
                                                  fc.P(top * 0.4, 20.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Short front (chamois)")


def build_back():
    """Short back (cut 2). Same crotch/inseam so the leg matches; higher back rise."""
    top = WAIST_FIN / 4.0
    hemw = THIGH_HALF
    back_rise = RISE + 40.0
    edges = [
        fc.Edge("waist", [fc.Line(fc.P(0.0, back_rise), fc.P(top, back_rise))]),
        fc.Edge("side", [fc.Line(fc.P(top, back_rise), fc.P(hemw, inseam))]),
        fc.Edge("hem", [fc.Line(fc.P(hemw, inseam), fc.P(CROTCH_X, inseam))]),
        fc.Edge("inseam", [fc.Line(fc.P(CROTCH_X, inseam), fc.P(CROTCH_X, CROTCH_Y))]),
        fc.Edge("centre_back", [fc.Bezier(fc.P(CROTCH_X, CROTCH_Y),
                                          fc.P(top * 0.28, back_rise * 0.3),
                                          fc.P(0.0, back_rise * 0.7), fc.P(0.0, back_rise))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"hem": 12.0},
        notches=[fc.Notch("side", 0.5, "hip"), fc.Notch("inseam", 0.5, "crotch")],
        grainline=fc.Grainline(fc.P(top * 0.5, back_rise * 0.3), fc.P(top * 0.5, back_rise * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Short back (raised)")


def build_strap():
    """A bib strap (cut 2): a mesh strap from the front waist over the shoulder to the back waist,
    length STRAP_LEN, width strap_width."""
    ln, w = STRAP_LEN, strap_width
    return fc.Piece(
        "strap", [
            fc.Edge("front_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("back_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("top", 0.5, "shoulder")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Bib strap (cut 2, mesh)")


def build():
    pattern = fc.PatternSet("cycling-bib-short")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    strap = build_strap()
    picked = {"front": front, "back": back, "strap": strap}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, back, strap):
        pattern.add(piece)
    pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5,
                         ease=(front.edge("side").length() - back.edge("side").length()))
    pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "high-compression lycra (front/back) + power mesh (straps)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "the panelled short at strong negative ease; breathable power mesh for the bib "
                 "straps so nothing constricts the belly in the aero position."},
        {"item": "chamois pad", "qty": 1, "unit": "piece",
         "note": "a multi-density chamois seated in the crotch window; the whole point of a bib "
                 "short is that the pad stays put with no waistband to shift it."},
        {"item": "silicone leg gripper", "qty": round(THIGH_FIN + 40.0), "unit": "mm_length",
         "note": "a wide gripper at each leg hem holds the short down over the thigh."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock every seam so nothing chafes over hours in the saddle."},
    ]
    pattern.metadata = {
        "fc500_rank": 450, "family": "active_swim", "fabric_hint": "nylon-elastano",
        "silhouette_note": "A road cyclist's bib short: high-compression panelled short held by "
            "mesh bib straps over the shoulders, no waistband, chamois seated over the crotch.",
        "hardware": "none — the bib straps are the suspension, no buckle or drawcord.",
        "solver": {
            "strap_len_mm": round(STRAP_LEN, 1), "rise_mm": round(RISE, 1),
            "note": "the strap length is solved from the torso rise + shoulder span and floored "
                    "positive so it always reaches; the front and back share ONE crotch point so "
                    "the leg cannot twist; strong negative ease throughout.",
        },
        "active": {"use": "long road rides; the bib straps suspend the short so nothing "
                   "constricts the abdomen in the aero position and the chamois stays put."},
    }
    return pattern


result = build()

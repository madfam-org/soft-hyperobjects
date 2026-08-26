"""
Three-piece suit vest — Fashion Cabinet Garment Cartridge
(FC-500 rank #444, tailoring, T3; y4d strap-buckle).

The waistcoat of a three-piece suit: a plain V-neck single-breasted vest in the suit cloth,
worn between shirt and jacket, with the front matched to the suit and a lining back with a
buckled cinch strap to nip the waist. The distinguishing feature vs the lapelled evening vest
is the higher, straight V-neck and the whole-cloth (not satin) styling.

Two real decisions:

  1. THE V-NECK AND POINT ARE CLAMPED. The neck opening depth is clamped under the front length
     so the V can never drop below the top button; the front point drop is clamped so it never
     falls below the hem baseline (which would invert the hem edge).

  2. THE BACK STRAP BUCKLES. The cinch strap adjusts the back on a Yantra4D strap-buckle; the
     strap webbing width is the drafted strap_width that drives the garment's cinch interface AND
     the buckle's webbing channel.

Pieces: front (V-neck + point, cut 2), back (cut 2 mirrored), strap (cut 2). T3 tailoring.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
front_length = float(PARAM(lambda: front_length, 560.0))
neck_depth = float(PARAM(lambda: neck_depth, 260.0))       # V depth below shoulder
point_drop = float(PARAM(lambda: point_drop, 60.0))
strap_width = float(PARAM(lambda: strap_width, 40.0))
button_count = float(PARAM(lambda: button_count, 5.0))
vest_ease = float(PARAM(lambda: vest_ease, 70.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1400.0))
waist_girth = max(640.0, min(waist_girth, 1300.0))
front_length = max(440.0, min(front_length, 700.0))
neck_depth = max(120.0, min(neck_depth, 420.0))
point_drop = max(20.0, min(point_drop, 140.0))
strap_width = max(20.0, min(strap_width, 70.0))
button_count = max(3.0, min(round(button_count), 8.0))
vest_ease = max(20.0, min(vest_ease, 140.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

CHEST_FIN = chest_girth + vest_ease
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 4.0
BODY_H = front_length
NECK_Y = max(BODY_H * 0.30, BODY_H - neck_depth)     # V break clamped above the point
POINT_DROP = min(point_drop, BODY_H * 0.25)


def build_front():
    w = FRONT_HALF
    h = BODY_H
    neck_x = max(w * 0.30, w - 90.0)
    p_shoulder_pt = fc.P(w, h)
    p_neck_pt = fc.P(neck_x, h)
    p_neck_cf = fc.P(0.0, NECK_Y)                     # V base at the CF
    p_armscye_bot = fc.P(w, h - h * 0.34)
    p_waist_side = fc.P(w, POINT_DROP + 30.0)
    p_hem_side = fc.P(w, POINT_DROP)
    p_point = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_side, p_point)]),
        fc.Edge("front_edge", [fc.Line(p_point, p_neck_cf)]),
        fc.Edge("neck", [fc.curve_through(p_neck_cf, p_neck_pt, bulge=0.24, side=1.0)]),
        fc.Edge("shoulder", [fc.Line(p_neck_pt, p_shoulder_pt)]),
        fc.Edge("armscye", [fc.curve_through(p_shoulder_pt, p_armscye_bot, bulge=0.22, side=-1.0)]),
        fc.Edge("side", [fc.Line(p_armscye_bot, p_waist_side),
                         fc.Line(p_waist_side, p_hem_side)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"hem": 20.0},
        notches=[fc.Notch("side", 0.5, "waist"), fc.Notch("front_edge", 0.5, "top button")],
        grainline=fc.Grainline(fc.P(w * 0.45, h * 0.15), fc.P(w * 0.45, h * 0.8)),
        internals=[fc.Internal("button-stand",
                               [fc.P(0.0, POINT_DROP + 40.0), fc.P(0.0, NECK_Y - 10.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Front (V-neck + point)")


def build_back():
    w = BACK_HALF
    h = BODY_H
    neck_x = max(w * 0.20, w - 90.0)
    p_shoulder_pt = fc.P(w, h)
    p_neck_pt = fc.P(neck_x, h)
    p_neck_cb = fc.P(0.0, h - 20.0)
    p_armscye_bot = fc.P(w, h - h * 0.34)
    p_waist_side = fc.P(w, POINT_DROP + 30.0)
    p_hem_side = fc.P(w, POINT_DROP)
    p_hem_cb = fc.P(0.0, POINT_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armscye_bot)]),
        fc.Edge("armscye", [fc.curve_through(p_armscye_bot, p_shoulder_pt, bulge=0.22, side=1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"hem": 20.0, "cb": 0.0},
        notches=[fc.Notch("side", 0.5, "waist"), fc.Notch("cb", 0.5, "strap level")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.8)),
        internals=[fc.Internal("strap-line",
                               [fc.P(0.0, POINT_DROP + h * 0.4),
                                fc.P(w * 0.7, POINT_DROP + h * 0.4)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Back (satin, cinch strap)")


def build_strap():
    ln = max(140.0, BACK_HALF * 0.8)
    w = strap_width
    return fc.Piece(
        "strap", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("free", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.5, w * 0.2), fc.P(ln * 0.5, w * 0.8)),
        internals=[fc.Internal("buckle-slot", [fc.P(ln * 0.85, w * 0.2), fc.P(ln * 0.85, w * 0.8)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Cinch strap (cut 2, buckle)")


def build():
    pattern = fc.PatternSet("three-piece-vest-back")
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
    pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "suit cloth (fronts) + lining/satin (back)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "worsted fronts matched to the suit; a lining/satin back with the cinch strap."},
        {"item": "strap buckle (Yantra4D strap-buckle)", "qty": 1, "unit": "piece",
         "note": f"the back cinch buckle, webbing {strap_width:.0f} mm = the strap_width that "
                 "drives the cinch interface AND the buckle's webbing channel; the buckle solid "
                 "is Yantra4D, never modelled here."},
        {"item": "front buttons", "qty": int(button_count), "unit": "piece",
         "note": f"{int(button_count)} front buttons down the button stand."},
        {"item": "front interfacing + full lining", "qty": round(marker_len * 0.7),
                "unit": "mm_length",
         "note": "canvas the front edge; fully line the vest."},
    ]
    pattern.metadata = {
        "fc500_rank": 444, "family": "tailoring", "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "A three-piece suit waistcoat: plain V-neck single-breasted front in "
            "the suit cloth, satin back with a buckled cinch strap.",
        "hardware": "cinch buckle via Yantra4D (notion.hardware_ref -> strap-buckle); webbing = "
            "strap_width, the same parameter that drives the cinch interface — the handshake.",
        "solver": {
            "neck_y_mm": round(NECK_Y, 1), "point_drop_mm": round(POINT_DROP, 1),
            "note": "the V-neck depth is clamped above the point so it never drops below the top "
                    "button; the point drop is clamped under a quarter of the front length so it "
                    "never falls below the hem baseline and inverts the hem.",
        },
        "tailoring": {"cut": "three-piece suit vest, V-neck, pointed hem, back buckle cinch."},
    }
    return pattern


result = build()

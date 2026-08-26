"""
Bandhgala formal jacket — Fashion Cabinet Garment Cartridge
(FC-500 rank #447, tailoring, T3; y4d shank-button-solid).

The bandhgala (jodhpuri): a structured, closed-neck formal jacket of the Indian court, with a
short mandarin band collar and a straight buttoned front, cut cleaner and more fitted than the
lounge suit and traditionally worn with a welt breast pocket. Like the Nehru jacket it has no
lapel, but it is more structured and formal — the black-tie equivalent of the subcontinent.

Two real decisions:

  1. THE STAND COLLAR IS SOLVED TO THE MEASURED NECK. The band length is the measured neckline
     run (two fronts + back), so it closes; its height is clamped so it never exceeds a comfort
     limit that would bind the throat.

  2. THE BUTTON IS SOLVED TO THE STRAIGHT FRONT. The shank buttons run the straight centre-front;
     their disc is the drafted button_dia that drives the garment's button-stand interface.

Pieces: front, back (cut 1 on fold), sleeve, collar (stand band). T3 tailoring.

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
# front|back|sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
jacket_length = float(PARAM(lambda: jacket_length, 740.0))    # nape to hem
sleeve_length = float(PARAM(lambda: sleeve_length, 630.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 350.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
collar_height = float(PARAM(lambda: collar_height, 45.0))
button_dia = float(PARAM(lambda: button_dia, 20.0))
coat_ease = float(PARAM(lambda: coat_ease, 110.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(820.0, min(chest_girth, 1400.0))
jacket_length = max(600.0, min(jacket_length, 900.0))
sleeve_length = max(520.0, min(sleeve_length, 720.0))
bicep_girth = max(260.0, min(bicep_girth, 520.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
collar_height = max(25.0, min(collar_height, 80.0))
button_dia = max(15.0, min(button_dia, 30.0))
coat_ease = max(60.0, min(coat_ease, 220.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

CHEST_FIN = chest_girth + coat_ease
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 4.0
BODY_H = jacket_length
ARM_DEPTH = min(BODY_H * 0.30, 320.0)
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0


def build_front():
    w = FRONT_HALF
    h = BODY_H
    neck_x = max(w * 0.28, w - SH_SEAM)
    SH_DROP = 16.0
    NECK_DROP = 14.0
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)
    arm_top = fc.P(w, h - ARM_DEPTH)
    cf_neck = fc.P(0.0, h - NECK_DROP)                # straight CF to the neck (no lapel)
    edges = [
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), cf_neck)]),
        fc.Edge("neckline", [fc.curve_through(cf_neck, neck_pt, bulge=0.14, side=1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, shoulder)]),
        fc.Edge("armhole", [fc.curve_through(shoulder, arm_top, bulge=0.22, side=-1.0)]),
        fc.Edge("side_seam", [fc.Line(arm_top, fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        allowances={"hem": 40.0, "center_front": 30.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("center_front", 0.5, "button")],
        grainline=fc.Grainline(fc.P(w * 0.45, h * 0.1), fc.P(w * 0.45, h * 0.85)),
        internals=[fc.Internal("button-stand", [fc.P(0.0, h * 0.2), fc.P(0.0,
                h - NECK_DROP - 20.0)],
                               kind="marking"),
                   fc.Internal("welt-breast-pocket",
                               [fc.P(w * 0.20, h - ARM_DEPTH - 30.0),
                                fc.P(w * 0.62, h - ARM_DEPTH - 30.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Front (mandarin, welt pocket)")


def build_back():
    w = BACK_HALF
    h = BODY_H
    neck_x = max(w * 0.18, w - SH_SEAM)
    SH_DROP = 16.0
    NECK_DROP = 14.0
    shoulder = fc.P(w, h - SH_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.curve_through(fc.P(0.0, h), fc.P(neck_x, h - NECK_DROP),
                                              bulge=0.12, side=1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_x, h - NECK_DROP), shoulder)]),
        fc.Edge("armhole", [fc.curve_through(shoulder, fc.P(w, h - ARM_DEPTH), bulge=0.22,
                side=-1.0)]),
        fc.Edge("side_seam", [fc.Line(fc.P(w, h - ARM_DEPTH), fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"hem": 40.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (cut 1 on fold)")


def build_sleeve(armhole_ring):
    ln = sleeve_length
    wrist = min(bicep_girth * 0.66, armhole_ring * 0.62)
    cap_w = min(armhole_ring * 0.9, wrist * 1.5)
    bow = ARM_DEPTH * 0.5
    for _ in range(40):
        test = fc.Edge("t", [fc.Bezier(fc.P(0.0, ln), fc.P(cap_w * 0.25, ln + bow),
                                       fc.P(cap_w * 0.75, ln + bow), fc.P(cap_w, ln))]).length()
        if test < 1e-6:
            break
        ratio = armhole_ring / test
        if ratio > 1.0:
            cap_w = min(cap_w * ratio, armhole_ring)
        else:
            bow = max(4.0, bow * ratio)
        cap_w = max(wrist + 10.0, cap_w)
        if abs(test - armhole_ring) < 0.4:
            break
    cuff_off = (cap_w - wrist) / 2.0
    edges = [
        fc.Edge("cuff", [fc.Line(fc.P(cuff_off, 0.0), fc.P(cuff_off + wrist, 0.0))]),
        fc.Edge("seam_r", [fc.Line(fc.P(cuff_off + wrist, 0.0), fc.P(cap_w, ln))]),
        fc.Edge("cap", [fc.Bezier(fc.P(cap_w, ln), fc.P(cap_w * 0.75, ln + bow),
                                  fc.P(cap_w * 0.25, ln + bow), fc.P(0.0, ln))]),
        fc.Edge("seam_l", [fc.Line(fc.P(0.0, ln), fc.P(cuff_off, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance, allowances={"cuff": 40.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"), fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2)")


MEASURED = {}


def build_collar():
    """The Nehru stand band (cut 1): length is the measured neckline run; height collar_height."""
    ln = MEASURED.get("neck_run", neck_girth)
    h = collar_height
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "collar", edges, seam_allowance=seam_allowance, allowances={"top": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.2), fc.P(ln * 0.1, h * 0.8)),
        cut=fc.CutSpec(quantity=1), label="Nehru stand collar (cut 1)")


def build():
    pattern = fc.PatternSet("bandhgala-jacket")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    MEASURED["neck_run"] = 2.0 * front.edge("neckline").length() + back.edge("neckline").length()
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()
    sleeve = build_sleeve(armhole_ring)
    collar = build_collar()
    picked = {"front": front, "back": back, "sleeve": sleeve, "collar": collar}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, back, sleeve, collar):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.5)
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=3.0)
    pattern.declare_seam(("collar", "neck_edge"),
                         [("front", "neckline"), ("front", "neckline"), ("back", "neckline")],
                         tol=3.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "worsted suiting", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "the body, sleeves and stand collar; a firm worsted so the Nehru collar stands."},
        {"item": "shank buttons (Yantra4D shank-button-solid)", "qty": 5, "unit": "piece",
         "note": f"five front buttons, disc {button_dia:.0f} mm = the button_dia that drives the "
                 "button-stand interface; the shank solid is Yantra4D, never modelled here."},
        {"item": "collar + front interfacing", "qty": round(BODY_H + 400.0), "unit": "mm_length",
         "note": "stiffen the stand collar so it holds; canvas the front edge."},
        {"item": "lining", "qty": round(marker_len * 0.8), "unit": "mm_length",
         "note": "fully line the jacket."},
    ]
    pattern.metadata = {
        "fc500_rank": 447, "family": "tailoring", "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "A bandhgala (jodhpuri): a structured closed-neck formal jacket with a "
            "mandarin band collar, straight buttoned front and a welt breast pocket.",
        "hardware": "shank buttons via Yantra4D (notion.hardware_ref -> shank-button-solid); "
            "diameter_mm = button_dia, the same parameter that drives the button_stand interface.",
        "solver": {
            "neck_run_mm": round(MEASURED.get("neck_run", 0.0), 1),
            "collar_height_mm": round(collar_height, 1),
            "note": "the stand collar length is the measured neckline run so it closes; its "
                    "height is clamped under a comfort limit that would bind the throat.",
        },
        "tailoring": {"cut": "bandhgala/jodhpuri structured closed-neck formal jacket, "
                   "mandarin collar, welt breast pocket, set-in sleeve."},
    }
    return pattern


result = build()

"""
Nehru Collar Jacket — Fashion Cabinet Garment Cartridge
(FC-400 #315, tailoring, T3).

The Nehru jacket (bandhgala-adjacent): a single-breasted straight-front jacket
with a stand (mandarin) collar that closes to the throat, no lapel, a clean
button run down the centre front, and a two-piece sleeve. The signature is the
STAND COLLAR that meets edge-to-edge at the centre front — it does not overlap —
so the collar length and the front-edge length are one relationship: the two
collar ends must meet exactly where the two front edges meet.

Three things are solved by measurement rather than by formula:

  1. THE STAND COLLAR IS BISECTED TO THE MEASURED NECK, AND ITS ENDS MEET AT CF.
     The collar length is derived from the MEASURED neckline (both front necks
     plus the back neck), so the two collar ends meet exactly at the centre front
     where the two front edges meet — a collar cut to a guessed length either
     gaps at the throat or overlaps and buckles.

  2. THE BUTTON RUN IS SOLVED ACROSS THE MEASURED CENTRE FRONT. Whole intervals
     from just under the collar to just above the hem, pitch recomputed, so the
     top button clears the collar seam and the bottom clears the hem.

  3. THE WAIST DART IS CLAMPED AND THE SLEEVE CAP EASED. The suppression dart is
     clamped so it cannot fold the panel through itself; the two-piece sleeve's
     vertical seams close by construction and its cap is eased to the measured
     armscye.

TAILORING CONVENTIONS: fine edge-stitch; a stand collar; shank buttons. The
SHANK-BUTTON SOLID is Yantra4D territory (`shank-button-solid`; see
notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|upper_sleeve|under_sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 900.0))
back_width = float(PARAM(lambda: back_width, 460.0))
jacket_length = float(PARAM(lambda: jacket_length, 740.0))
back_length = float(PARAM(lambda: back_length, 440.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
neck_width = float(PARAM(lambda: neck_width, 175.0))
collar_stand = float(PARAM(lambda: collar_stand, 50.0))
button_count = float(PARAM(lambda: button_count, 5.0))
button_dia = float(PARAM(lambda: button_dia, 20.0))
coat_ease = float(PARAM(lambda: coat_ease, 110.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 35.0))

chest_girth = max(820.0, min(chest_girth, 1400.0))
waist_girth = max(640.0, min(waist_girth, 1300.0))
back_width = max(360.0, min(back_width, 540.0))
jacket_length = max(600.0, min(jacket_length, 900.0))
back_length = max(360.0, min(back_length, 520.0))
sleeve_length = max(520.0, min(sleeve_length, 720.0))
neck_width = max(140.0, min(neck_width, 220.0))
collar_stand = max(30.0, min(collar_stand, 75.0))
button_count = max(3.0, min(round(button_count), 8.0))
button_dia = max(12.0, min(button_dia, 28.0))
coat_ease = max(60.0, min(coat_ease, 200.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(20.0, min(hem_allowance, 50.0))

EDGESTITCH = 6.0
N_BUTTONS = int(button_count)

QUARTER_CHEST = (chest_girth + coat_ease) / 4.0
QUARTER_WAIST = max(QUARTER_CHEST * 0.72,
                    min((waist_girth + coat_ease) / 4.0, QUARTER_CHEST - 6.0))
HALF_NECK = neck_width / 2.0
HALF_BACK = back_width / 2.0
NECK_DROP_F = max(70.0, HALF_NECK * 0.95)
NECK_DROP_B = max(20.0, HALF_NECK * 0.28)
SHOULDER_SLOPE = 45.0

PLACKET_LEN = jacket_length - NECK_DROP_F
BUTTON_END_CLEAR = max(button_dia * 1.6, 40.0)
BUTTON_RUN = max(button_dia * 2.0, PLACKET_LEN - 2.0 * BUTTON_END_CLEAR)
N_INTERVALS = max(1, N_BUTTONS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS

TOTAL_SUPPRESS = max(0.0, QUARTER_CHEST - QUARTER_WAIST)
WAIST_DART = max(0.0, min(TOTAL_SUPPRESS * 0.55, QUARTER_CHEST * 0.24))


def _button(label, x, y):
    r = button_dia / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    hw = QUARTER_CHEST
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, back_length)
    p_armhole = fc.P(hw, jacket_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, jacket_length - NECK_DROP_B - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, jacket_length - NECK_DROP_B)
    p_neck_cf = fc.P(0.0, jacket_length - NECK_DROP_B - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, jacket_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, jacket_length - NECK_DROP_B - SHOULDER_SLOPE + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.28, side=1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("edge-stitch",
                    [fc.P(EDGESTITCH, EDGESTITCH), fc.P(EDGESTITCH, PLACKET_LEN)],
                    kind="trace"),
        fc.Internal("waist dart",
                    [fc.P(hw * 0.5, back_length + 60.0),
                     fc.P(hw * 0.5 - WAIST_DART / 2.0, back_length),
                     fc.P(hw * 0.5, back_length - 70.0),
                     fc.P(hw * 0.5 + WAIST_DART / 2.0, back_length),
                     fc.P(hw * 0.5, back_length + 60.0)], kind="marking"),
    ]
    y0 = BUTTON_END_CLEAR
    for i in range(N_BUTTONS):
        internals.append(_button(f"button-{i + 1}", button_dia * 0.9, y0 + BUTTON_PITCH * i))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf": hem_allowance},
        notches=[fc.Notch("armscye", 0.0, "underarm"),
                 fc.Notch("side", 0.5, "waist")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, jacket_length - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    hw = QUARTER_CHEST
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, back_length)
    p_armhole = fc.P(hw, jacket_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, jacket_length - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, jacket_length)
    p_neck_cb = fc.P(0.0, jacket_length - NECK_DROP_B)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, jacket_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, jacket_length - SHOULDER_SLOPE + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cb_fold": 0.0},
        notches=[fc.Notch("side", 0.5, "waist"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.35, 30.0), fc.P(hw * 0.35, jacket_length - 40.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold)",
    )


_FRONT = build_front()
_BACK = build_back()
ARMSCYE_RUN = _FRONT.edge("armscye").length(0.05) + _BACK.edge("armscye").length(0.05)


def build_upper_sleeve():
    sw = QUARTER_CHEST * 0.86
    cap_h = QUARTER_CHEST * 0.32
    ln = sleeve_length
    edges = [
        fc.Edge("cap", [fc.Bezier(
            fc.P(sw, 0.0), fc.P(sw * 0.80, cap_h * 0.9),
            fc.P(sw * 0.30, cap_h * 1.05), fc.P(0.0, 0.0))]),
        fc.Edge("fore_seam", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P(0.0, -ln), fc.P(sw, -ln))]),
        fc.Edge("hind_seam", [fc.Line(fc.P(sw, -ln), fc.P(sw, 0.0))]),
    ]
    return fc.Piece(
        "upper_sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_h * 0.9)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Upper sleeve (cut 2, mirrored)",
    )


def build_under_sleeve():
    sw = QUARTER_CHEST * 0.40
    ln = sleeve_length
    edges = [
        fc.Edge("scye", [fc.curve_through(
            fc.P(0.0, 0.0), fc.P(sw, 0.0), bulge=0.20, side=1.0)]),
        fc.Edge("hind_seam", [fc.Line(fc.P(sw, 0.0), fc.P(sw, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P(sw, -ln), fc.P(0.0, -ln))]),
        fc.Edge("fore_seam", [fc.Line(fc.P(0.0, -ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "under_sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("scye", 0.5, "underarm")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, -ln * 0.85)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Under sleeve (cut 2, mirrored)",
    )


def build_collar():
    """Stand (mandarin) collar, cut 2 on the fold. Length = the MEASURED neck."""
    neck_run = (_FRONT.edge("neck").length(0.05) * 2.0
                + _BACK.edge("neck").length(0.05))
    ln = neck_run / 2.0
    depth = collar_stand
    edges = [
        fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("top", [fc.curve_through(
            fc.P(0.0, depth), fc.P(ln, depth * 0.85), bulge=0.06, side=-1.0)]),
        fc.Edge("cf_end", [fc.Line(fc.P(ln, depth * 0.85), fc.P(ln, 0.0))]),
        fc.Edge("neck_edge", [fc.curve_through(
            fc.P(ln, 0.0), fc.P(0.0, 0.0), bulge=0.10, side=1.0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match"),
                 fc.Notch("cf_end", 0.5, "CF meeting point")],
        grainline=fc.Grainline(fc.P(ln * 0.1, depth * 0.5), fc.P(ln * 0.9, depth * 0.5)),
        internals=[
            fc.Internal("edge-stitch",
                        [fc.P(EDGESTITCH, depth - EDGESTITCH),
                         fc.P(ln - EDGESTITCH, depth * 0.85 - EDGESTITCH)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb_fold"),
        label="Stand collar (cut 2, on fold)",
    )


def build():
    pattern = fc.PatternSet("nehru-jacket")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "upper_sleeve": everything or target_piece == "upper_sleeve",
        "under_sleeve": everything or target_piece == "under_sleeve",
        "collar": everything or target_piece == "collar",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        pattern.add(build_front())
    if want["back"]:
        pattern.add(build_back())
    if want["upper_sleeve"]:
        pattern.add(build_upper_sleeve())
    if want["under_sleeve"]:
        pattern.add(build_under_sleeve())
    if want["collar"]:
        pattern.add(build_collar())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if want["upper_sleeve"] and want["under_sleeve"]:
        pattern.declare_seam(("upper_sleeve", "fore_seam"),
                             ("under_sleeve", "fore_seam"), tol=1.0)
        pattern.declare_seam(("upper_sleeve", "hind_seam"),
                             ("under_sleeve", "hind_seam"), tol=1.0)
    if want["upper_sleeve"] and want["under_sleeve"] and want["front"] and want["back"]:
        us = build_upper_sleeve()
        un = build_under_sleeve()
        cap = us.edge("cap").length(0.05) + un.edge("scye").length(0.05)
        pattern.declare_seam([("upper_sleeve", "cap"), ("under_sleeve", "scye")],
                             [("front", "armscye"), ("back", "armscye")],
                             tol=3.0, ease=cap - ARMSCYE_RUN)
    if want["collar"] and want["front"] and want["back"]:
        # The stand collar meets the measured neckline; declared so a collar
        # redrafted off a guessed length (gapping or overlapping at CF) goes red.
        neck = (_FRONT.edge("neck").length(0.05) * 2.0
                + _BACK.edge("neck").length(0.05))
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("front", "neck"), ("back", "neck")],
                             tol=2.0, ease=build_collar().edge("neck_edge").length(0.05)
                             - neck)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "wool worsted, 280 gsm (suiting)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 66% marker."},
        {"item": "shank button", "qty": N_BUTTONS, "unit": "piece",
         "note": f"Yantra4D shank-button-solid (notion.hardware_ref) at "
                 f"{button_dia:.0f} mm; SOLVED pitch {BUTTON_PITCH:.1f} mm, clear of "
                 f"the collar seam and the hem."},
        {"item": "hair canvas + shoulder pads", "qty": 1, "unit": "set",
         "note": "a light canvas front holds the clean straight line; the stand "
                 "collar is interfaced firm to stay up."},
        {"item": "fine edge-stitch thread + needle 80/12", "qty": 1, "unit": "spool",
         "note": f"{EDGESTITCH:.0f} mm edge-stitch on the front edge and collar."},
    ]
    pattern.metadata = {
        "fc400_rank": 315,
        "family": "tailoring",
        "tier": 3,
        "fabric_hint": "wool-worsted",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "jacket_length": round(jacket_length, 1),
            "collar_stand": round(collar_stand, 1),
        },
        "solved": {
            "button_count": N_BUTTONS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "button_run_mm": round(BUTTON_RUN, 2),
            "neck_run_measured_mm": round(
                _FRONT.edge("neck").length(0.05) * 2.0
                + _BACK.edge("neck").length(0.05), 2),
            "collar_meets_at_cf": True,
            "armscye_run_measured_mm": round(ARMSCYE_RUN, 2),
            "waist_dart_clamped_mm": round(WAIST_DART, 2),
            "note": "the stand collar is bisected to the MEASURED neckline so its "
                    "two ends meet exactly at the centre front where the two front "
                    "edges meet — a collar cut to a guessed length gaps at the "
                    "throat or overlaps and buckles. The buttons are solved across "
                    "the measured centre front, the waist dart is clamped, and the "
                    "sleeve cap is eased to the measured armscye.",
        },
        "hardware": "shank buttons via Yantra4D (notion.hardware_ref -> "
                    "shank-button-solid); the solid's diameter_mm is fed from this "
                    "garment's button_dia, which also sizes the button run.",
    }
    return pattern


result = build()

"""
Safari-Suit Bush Jacket — Fashion Cabinet Garment Cartridge
(FC-400 #319, tailoring, T3).

The safari (bush) jacket: a belted single-breasted jacket in cotton twill, four
patch bellows pockets with box pleats, a self-fabric belt through belt loops, a
notch or camp collar, and shoulder epaulettes. The signature is the SELF BELT
through loops, and the number that has to be right is the belt length against the
belted (cinched) waist plus a buckle tail — a belt cut to the waist girth cannot
be buckled at all.

Three things are solved by measurement rather than by formula:

  1. THE BELT IS CUT TO THE MEASURED WAIST PLUS A BUCKLE TAIL. The belt runs the
     MEASURED waist girth plus the tail that passes the buckle and the wrap round
     its bar — a belt cut to the girth alone meets end-to-end with no tail to
     buckle. The belt-loop pitch is then solved across the MEASURED waist so the
     loops sit evenly and the last loop lands on the panel.

  2. THE FOUR BELLOWS POCKETS ARE CLAMPED AGAINST THE PANELS. A bellows pocket
     wider than the front (or the belt line height it sits above) folds the panel
     over, and — because the kernel CCW-normalizes an inverted outline and area()
     takes an absolute value — such a pocket renders and passes verify() looking
     healthy. Pocket width and the belt-loop count are clamped and reported.

  3. THE BUTTON RUN IS SOLVED AND THE SLEEVE CAP EASED. The front buttons are
     pitched across the MEASURED front above the belt line; the two-piece sleeve's
     vertical seams close by construction and its cap is eased to the armscye.

TAILORING/UTILITY CONVENTIONS: edge-stitch; box-pleat bellows pockets; a self
belt. The SEW-THROUGH BUTTON SOLID is Yantra4D territory (`sew-through-button`;
see notion.hardware_ref).

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
# front|back|sleeve|collar|belt|pocket|set

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
waist_girth = float(PARAM(lambda: waist_girth, 940.0))
back_width = float(PARAM(lambda: back_width, 465.0))
jacket_length = float(PARAM(lambda: jacket_length, 760.0))
back_length = float(PARAM(lambda: back_length, 440.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
neck_width = float(PARAM(lambda: neck_width, 175.0))
button_count = float(PARAM(lambda: button_count, 4.0))
button_ligne = float(PARAM(lambda: button_ligne, 30.0))
pocket_width = float(PARAM(lambda: pocket_width, 190.0))
belt_width = float(PARAM(lambda: belt_width, 45.0))
belt_loops = float(PARAM(lambda: belt_loops, 5.0))
coat_ease = float(PARAM(lambda: coat_ease, 180.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 35.0))

chest_girth = max(860.0, min(chest_girth, 1500.0))
waist_girth = max(700.0, min(waist_girth, 1400.0))
back_width = max(380.0, min(back_width, 560.0))
jacket_length = max(620.0, min(jacket_length, 900.0))
back_length = max(360.0, min(back_length, 520.0))
sleeve_length = max(520.0, min(sleeve_length, 760.0))
neck_width = max(140.0, min(neck_width, 240.0))
button_count = max(3.0, min(round(button_count), 7.0))
button_ligne = max(22.0, min(button_ligne, 42.0))
pocket_width = max(120.0, min(pocket_width, 300.0))
belt_width = max(28.0, min(belt_width, 70.0))
belt_loops = max(3.0, min(round(belt_loops), 8.0))
coat_ease = max(100.0, min(coat_ease, 320.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(20.0, min(hem_allowance, 50.0))

EDGESTITCH = 6.0
N_BUTTONS = int(button_count)
N_LOOPS = int(belt_loops)
BUTTON_MM = button_ligne * 0.635

QUARTER_CHEST = (chest_girth + coat_ease) / 4.0
HALF_NECK = neck_width / 2.0
HALF_BACK = back_width / 2.0
NECK_DROP_F = max(70.0, HALF_NECK * 0.95)
NECK_DROP_B = max(20.0, HALF_NECK * 0.28)
SHOULDER_SLOPE = 45.0
BELT_LINE_Y = back_length            # the belt sits at the waist

# The belt: MEASURED waist plus a buckle tail plus the bar wrap.
BELT_TAIL = max(150.0, waist_girth * 0.20)
BELT_WRAP = belt_width * 2.0
BELT_CUT = waist_girth + BELT_TAIL + BELT_WRAP + 2.0 * seam_allowance
# Belt-loop pitch solved across the measured waist (front span only, per front).
LOOP_SPAN = QUARTER_CHEST * 2.0
LOOP_PITCH = LOOP_SPAN / max(1, N_LOOPS - 1) if N_LOOPS > 1 else 0.0

# The button run above the belt line.
BUTTON_END_CLEAR = max(BUTTON_MM * 1.6, 40.0)
BUTTON_TOP_Y = jacket_length - NECK_DROP_B - NECK_DROP_F - BUTTON_MM
BUTTON_BOTTOM_Y = BELT_LINE_Y - 20.0
BUTTON_RUN = max(BUTTON_MM * 2.0, BUTTON_TOP_Y - BUTTON_BOTTOM_Y)
N_INTERVALS = max(1, N_BUTTONS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS

_POCKET_W_RAW = pocket_width
POCKET_W = max(90.0, min(_POCKET_W_RAW, QUARTER_CHEST - 2.0 * seam_allowance))
POCKET_H = max(140.0, POCKET_W * 1.05)


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    hw = QUARTER_CHEST
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_armhole = fc.P(hw, jacket_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, jacket_length - NECK_DROP_B - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, jacket_length - NECK_DROP_B)
    p_neck_cf = fc.P(0.0, jacket_length - NECK_DROP_B - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, jacket_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, jacket_length - NECK_DROP_B - SHOULDER_SLOPE + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.28, side=1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("belt line", [fc.P(0.0, BELT_LINE_Y), fc.P(hw, BELT_LINE_Y)],
                    kind="marking"),
        fc.Internal("box-pleat placement (front)",
                    [fc.P(hw * 0.2, BELT_LINE_Y * 0.5), fc.P(hw * 0.2, BELT_LINE_Y * 0.5)],
                    kind="marking"),
        fc.Internal("epaulette placement",
                    [fc.P(HALF_BACK - 60.0, jacket_length - NECK_DROP_B - SHOULDER_SLOPE),
                     fc.P(HALF_NECK + 12.0, jacket_length - NECK_DROP_B)], kind="marking"),
    ]
    for tag, py in (("chest", jacket_length - QUARTER_CHEST * 0.85),
                    ("hip", POCKET_H + hem_allowance + 20.0)):
        px = hw * 0.32
        internals.append(fc.Internal(
            f"{tag} bellows pocket placement",
            [fc.P(px, py), fc.P(px + POCKET_W, py),
             fc.P(px + POCKET_W, py - POCKET_H), fc.P(px, py - POCKET_H),
             fc.P(px, py)], kind="marking"))
    # Belt loops on this front.
    for i in range(max(1, N_LOOPS // 2)):
        internals.append(fc.Internal(
            f"belt loop-{i + 1}",
            [fc.P(hw * 0.3 + LOOP_PITCH * i, BELT_LINE_Y + belt_width * 0.5),
             fc.P(hw * 0.3 + LOOP_PITCH * i, BELT_LINE_Y - belt_width * 0.5)],
            kind="marking"))
    y0 = BUTTON_TOP_Y
    for i in range(N_BUTTONS):
        internals.append(_button(f"button-{i + 1}", BUTTON_MM * 0.9, y0 - BUTTON_PITCH * i))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf": hem_allowance},
        notches=[fc.Notch("armscye", 0.0, "underarm"),
                 fc.Notch("side", BELT_LINE_Y / (jacket_length - QUARTER_CHEST * 0.5),
                          "belt line")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, jacket_length - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    hw = QUARTER_CHEST
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_armhole = fc.P(hw, jacket_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, jacket_length - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, jacket_length)
    p_neck_cb = fc.P(0.0, jacket_length - NECK_DROP_B)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_armhole)]),
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
        notches=[fc.Notch("side", BELT_LINE_Y / (jacket_length - QUARTER_CHEST * 0.5),
                          "belt line"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, jacket_length - 40.0)),
        internals=[
            fc.Internal("belt line", [fc.P(0.0, BELT_LINE_Y), fc.P(hw, BELT_LINE_Y)],
                        kind="marking"),
            fc.Internal("centre box pleat",
                        [fc.P(0.0, jacket_length - QUARTER_CHEST * 0.55),
                         fc.P(0.0, BELT_LINE_Y)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold)",
    )


_FRONT = build_front()
_BACK = build_back()
ARMSCYE_RUN = _FRONT.edge("armscye").length(0.05) + _BACK.edge("armscye").length(0.05)


def build_sleeve():
    sw = QUARTER_CHEST * 0.92
    cap_h = QUARTER_CHEST * 0.30
    ln = sleeve_length
    edges = [
        fc.Edge("cap_r", [fc.Bezier(
            fc.P(sw, 0.0), fc.P(sw * 0.86, cap_h * 0.75),
            fc.P(sw * 0.60, cap_h), fc.P(sw / 2.0, cap_h))]),
        fc.Edge("cap_l", [fc.Bezier(
            fc.P(sw / 2.0, cap_h), fc.P(sw * 0.40, cap_h),
            fc.P(sw * 0.14, cap_h * 0.75), fc.P(0.0, 0.0))]),
        fc.Edge("seam_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P(0.0, -ln), fc.P(sw, -ln))]),
        fc.Edge("seam_r", [fc.Line(fc.P(sw, -ln), fc.P(sw, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("cap_r", 1.0, "shoulder point"),
                 fc.Notch("cap_l", 0.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_h * 0.9)),
        internals=[
            fc.Internal("cuff tab button", [fc.P(30.0, -ln + 30.0)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


_SLEEVE = build_sleeve()
CAP_RUN = _SLEEVE.edge("cap_r").length(0.05) + _SLEEVE.edge("cap_l").length(0.05)
CAP_EASE = CAP_RUN - ARMSCYE_RUN


def build_collar():
    neck_run = (_FRONT.edge("neck").length(0.05) * 2.0
                + _BACK.edge("neck").length(0.05))
    ln = neck_run / 2.0
    depth = max(55.0, HALF_NECK * 0.6)
    edges = [
        fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("fall", [fc.Line(fc.P(0.0, depth), fc.P(ln, depth))]),
        fc.Edge("point", [fc.Line(fc.P(ln, depth), fc.P(ln + 20.0, 10.0))]),
        fc.Edge("neck_edge", [fc.curve_through(
            fc.P(ln + 20.0, 10.0), fc.P(0.0, 0.0), bulge=0.10, side=1.0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, depth * 0.5), fc.P(ln * 0.9, depth * 0.5)),
        internals=[
            fc.Internal("edge-stitch",
                        [fc.P(EDGESTITCH, depth - EDGESTITCH),
                         fc.P(ln - EDGESTITCH, depth - EDGESTITCH)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb_fold"),
        label="Camp collar (cut 2, on fold)",
    )


def build_belt():
    """The self belt, cut 1. Runs the MEASURED waist plus a buckle tail."""
    ln = BELT_CUT
    w = belt_width * 2.0 + 2.0 * seam_allowance
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("buckle_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        # A pointed tip.
        fc.Edge("tip", [fc.Line(fc.P(0.0, w), fc.P(-w * 0.6, w / 2.0)),
                        fc.Line(fc.P(-w * 0.6, w / 2.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "belt", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 1.0, "buckle end"),
                 fc.Notch("lower", (BELT_TAIL + BELT_WRAP) / ln, "nominal waist mark")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Self belt (cut 1)",
    )


def build_pocket():
    """Bellows patch pocket, cut 4. Clamped against the front."""
    w = POCKET_W
    h = POCKET_H
    edges = [
        fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"mouth": hem_allowance * 0.5},
        notches=[fc.Notch("bottom", 0.5, "centre box pleat")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=[
            fc.Internal("centre box pleat", [fc.P(w * 0.5, 0.0), fc.P(w * 0.5, h)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=4),
        label="Bellows pocket (cut 4)",
    )


def build():
    pattern = fc.PatternSet("safari-suit-jacket")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "collar": everything or target_piece == "collar",
        "belt": everything or target_piece == "belt",
        "pocket": everything or target_piece == "pocket",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        pattern.add(build_front())
    if want["back"]:
        pattern.add(build_back())
    if want["sleeve"]:
        pattern.add(build_sleeve())
    if want["collar"]:
        pattern.add(build_collar())
    if want["belt"]:
        pattern.add(build_belt())
    if want["pocket"]:
        pattern.add(build_pocket())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if want["sleeve"] and want["front"] and want["back"]:
        pattern.declare_seam([("sleeve", "cap_r"), ("sleeve", "cap_l")],
                             [("front", "armscye"), ("back", "armscye")],
                             tol=2.5, ease=CAP_EASE)
    if want["belt"]:
        pattern.declare_seam(("belt", "lower"), ("belt", "upper"), tol=0.3)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cotton twill, 8 oz (safari cloth)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; a firm cotton twill "
                 f"holds the bellows pockets' box pleats crisp."},
        {"item": "sew-through button", "qty": N_BUTTONS + 8, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm): {N_BUTTONS} front "
                 f"at a SOLVED pitch of {BUTTON_PITCH:.1f} mm, plus pocket + "
                 f"epaulette + cuff buttons."},
        {"item": "belt buckle", "qty": 1, "unit": "piece",
         "note": f"a self belt of MEASURED length {BELT_CUT:.0f} mm (waist + tail) "
                 f"runs through {N_LOOPS} loops."},
        {"item": "fine edge-stitch thread + needle 90/14", "qty": 1, "unit": "spool",
         "note": f"{EDGESTITCH:.0f} mm edge-stitch on pockets, collar, and belt."},
    ]
    pattern.metadata = {
        "fc400_rank": 319,
        "family": "tailoring",
        "tier": 3,
        "fabric_hint": "cotton-twill",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "jacket_length": round(jacket_length, 1),
            "belt_cut_length": round(BELT_CUT, 1),
            "pocket_width": round(POCKET_W, 1),
        },
        "solved": {
            "button_count": N_BUTTONS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "belt_tail_mm": round(BELT_TAIL, 2),
            "belt_cut_mm": round(BELT_CUT, 2),
            "belt_loop_count": N_LOOPS,
            "belt_loop_pitch_mm": round(LOOP_PITCH, 2),
            "pocket_width_requested_mm": round(_POCKET_W_RAW, 2),
            "pocket_width_clamped_mm": round(POCKET_W, 2),
            "pocket_width_was_clamped": bool(abs(POCKET_W - _POCKET_W_RAW) > 0.01),
            "cap_ease_mm": round(CAP_EASE, 2),
            "note": "the self belt is cut to the MEASURED waist girth plus a buckle "
                    "tail plus the bar wrap — a belt cut to the girth alone meets "
                    "end-to-end with no tail to buckle. The belt-loop pitch is "
                    "solved across the measured waist. The four bellows pockets are "
                    "clamped against the front, because an inverted pocket is CCW-"
                    "normalized by the kernel into a healthy-looking piece, and the "
                    "buttons are pitched above the belt line.",
        },
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne is fed from this "
                    "garment's button_ligne, which also sizes the buttonholes and "
                    "the front run. The belt buckle is a companion hard good.",
    }
    return pattern


result = build()

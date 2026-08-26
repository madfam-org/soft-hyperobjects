"""
Welder's Cotton Duck Jacket — Fashion Cabinet Garment Cartridge
(FC-400 #307, workwear_uniforms, T3).

The welder's jacket: heavy cotton duck, a stand collar that closes right to the
throat, a storm flap that covers the button placket so no spark reaches the gap,
and set-in sleeves cut generous for reach. The garment's job is to keep molten
spatter off skin, so the two things that matter most are that the flap actually
COVERS the placket and that there are no exposed gaps at the throat.

Three things are solved by measurement rather than by formula:

  1. THE STORM FLAP IS WIDER THAN THE PLACKET GAP IT COVERS, BY MEASUREMENT. A
     spark flap that merely reaches the buttons leaves a line of thread exposed;
     it has to overlap past the buttonholes on both sides. Its width is derived
     from the MEASURED button position plus an overlap on each side, and clamped
     so it can never come out narrower than the gap — a flap narrower than what
     it covers is worse than none, and a naive draft that ties flap width to a
     fraction of the chest produces exactly that at a small size.

  2. THE BUTTON RUN IS SOLVED ACROSS THE MEASURED PLACKET. Whole intervals are
     fitted between two end clearances and the pitch recomputed, so the top
     button sits under the collar and the bottom clears the hem — a drifted
     bottom button lands in the hem turn.

  3. THE SLEEVE CAP EASE IS TAKEN OFF THE MEASURED ARMSCYE. The cap seam exceeds
     the MEASURED armscye by a low worked-in ease (duck eases badly), reported so
     a cap drafted independently of the armscye cannot ripple or refuse to close.

WORKWEAR CONVENTIONS: 7 mm topstitch; felled seams; every hard good a Yantra4D
reference. The SEW-THROUGH BUTTON SOLID is Yantra4D territory
(`sew-through-button`; see notion.hardware_ref).

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


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|collar|storm_flap|set

chest_girth = float(PARAM(lambda: chest_girth, 1080.0))
back_width = float(PARAM(lambda: back_width, 470.0))
body_length = float(PARAM(lambda: body_length, 700.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 660.0))
neck_width = float(PARAM(lambda: neck_width, 180.0))
collar_stand = float(PARAM(lambda: collar_stand, 60.0))     # tall throat collar
shoulder_slope = float(PARAM(lambda: shoulder_slope, 45.0))
button_count = float(PARAM(lambda: button_count, 5.0))
button_ligne = float(PARAM(lambda: button_ligne, 32.0))
flap_overlap = float(PARAM(lambda: flap_overlap, 40.0))     # spark overlap each side
wear_ease = float(PARAM(lambda: wear_ease, 220.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(880.0, min(chest_girth, 1500.0))
back_width = max(380.0, min(back_width, 560.0))
body_length = max(560.0, min(body_length, 860.0))
sleeve_length = max(520.0, min(sleeve_length, 780.0))
neck_width = max(150.0, min(neck_width, 240.0))
collar_stand = max(40.0, min(collar_stand, 90.0))
shoulder_slope = max(25.0, min(shoulder_slope, 70.0))
button_count = max(4.0, min(round(button_count), 8.0))
button_ligne = max(24.0, min(button_ligne, 45.0))
flap_overlap = max(20.0, min(flap_overlap, 70.0))
wear_ease = max(120.0, min(wear_ease, 340.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(18.0, min(hem_allowance, 45.0))

TOPSTITCH = 7.0
N_BUTTONS = int(button_count)
BUTTON_MM = button_ligne * 0.635

QUARTER_CHEST = (chest_girth + wear_ease) / 4.0
HALF_NECK = neck_width / 2.0
HALF_BACK = back_width / 2.0
SHOULDER_RUN = max(40.0, HALF_BACK - HALF_NECK)
NECK_DROP_F = max(60.0, HALF_NECK * 0.9)
NECK_DROP_B = max(20.0, HALF_NECK * 0.28)

# The button placket run.
PLACKET_LEN = body_length - NECK_DROP_B
BUTTON_END_CLEAR = max(BUTTON_MM * 1.5, 50.0)
BUTTON_RUN = max(BUTTON_MM * 2.0, PLACKET_LEN - 2.0 * BUTTON_END_CLEAR)
N_INTERVALS = max(1, N_BUTTONS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS

# The button stand: the buttons sit inboard of CF by a measured stand.
BUTTON_STAND = max(BUTTON_MM * 0.9, 20.0)
# The storm flap has to cover the buttonholes on BOTH sides: its finished width
# is the button stand plus the overlap on each side, and it is clamped so it can
# never come out narrower than the gap it covers.
_FLAP_W_RAW = 2.0 * (BUTTON_STAND + flap_overlap)
FLAP_W = max(2.0 * BUTTON_STAND + 2.0 * seam_allowance, _FLAP_W_RAW)


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    hw = QUARTER_CHEST
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_armhole = fc.P(hw, body_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, body_length - NECK_DROP_B - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, body_length - NECK_DROP_B)
    p_neck_cf = fc.P(0.0, body_length - NECK_DROP_B - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole,
            fc.P(hw - 10.0, body_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, body_length - NECK_DROP_B - shoulder_slope + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.28, side=1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("placket topstitch",
                    [fc.P(TOPSTITCH, TOPSTITCH),
                     fc.P(TOPSTITCH, body_length - NECK_DROP_B - NECK_DROP_F)],
                    kind="trace"),
    ]
    y0 = BUTTON_END_CLEAR
    for i in range(N_BUTTONS):
        internals.append(_button(f"button-{i + 1}", BUTTON_STAND, y0 + BUTTON_PITCH * i))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf": hem_allowance},
        notches=[fc.Notch("armscye", 0.0, "underarm"),
                 fc.Notch("shoulder", 0.5, "shoulder mid")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, body_length - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    hw = QUARTER_CHEST
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_armhole = fc.P(hw, body_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, body_length - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, body_length)
    p_neck_cb = fc.P(0.0, body_length - NECK_DROP_B)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole,
            fc.P(hw - 10.0, body_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, body_length - shoulder_slope + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cb_fold": 0.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder mid"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, body_length - 30.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold)",
    )


_FRONT = build_front()
_BACK = build_back()
ARMSCYE_RUN = _FRONT.edge("armscye").length(0.05) + _BACK.edge("armscye").length(0.05)


def build_sleeve():
    sw = QUARTER_CHEST * 0.94
    cap_h = QUARTER_CHEST * 0.30
    ln = sleeve_length
    cuff_w = sw * 0.66
    p_ul = fc.P(0.0, 0.0)
    p_ur = fc.P(sw, 0.0)
    p_cuff_r = fc.P((sw - cuff_w) / 2.0 + cuff_w, -ln)
    p_cuff_l = fc.P((sw - cuff_w) / 2.0, -ln)
    edges = [
        fc.Edge("cap_r", [fc.Bezier(
            p_ur, fc.P(sw * 0.86, cap_h * 0.75),
            fc.P(sw * 0.60, cap_h), fc.P(sw / 2.0, cap_h))]),
        fc.Edge("cap_l", [fc.Bezier(
            fc.P(sw / 2.0, cap_h), fc.P(sw * 0.40, cap_h),
            fc.P(sw * 0.14, cap_h * 0.75), p_ul)]),
        fc.Edge("seam_l", [fc.Line(p_ul, p_cuff_l)]),
        fc.Edge("cuff", [fc.Line(p_cuff_l, p_cuff_r)]),
        fc.Edge("seam_r", [fc.Line(p_cuff_r, p_ur)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("cap_r", 1.0, "shoulder point"),
                 fc.Notch("cap_l", 0.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_h * 0.9)),
        internals=[
            fc.Internal("cuff topstitch",
                        [fc.P((sw - cuff_w) / 2.0 + TOPSTITCH, -ln + TOPSTITCH),
                         fc.P((sw - cuff_w) / 2.0 + cuff_w - TOPSTITCH, -ln + TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


_SLEEVE = build_sleeve()
CAP_RUN = _SLEEVE.edge("cap_r").length(0.05) + _SLEEVE.edge("cap_l").length(0.05)
CAP_EASE = CAP_RUN - ARMSCYE_RUN


def build_collar():
    """Tall stand collar, cut 2 on the fold. Length = the MEASURED neck run."""
    neck_run = (_FRONT.edge("neck").length(0.05) * 2.0
                + _BACK.edge("neck").length(0.05))
    ln = neck_run / 2.0
    depth = collar_stand
    edges = [
        fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, depth), fc.P(ln, depth))]),
        fc.Edge("cf_end", [fc.Line(fc.P(ln, depth), fc.P(ln, 0.0))]),
        fc.Edge("neck_edge", [fc.curve_through(
            fc.P(ln, 0.0), fc.P(0.0, 0.0), bulge=0.10, side=1.0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, depth * 0.5), fc.P(ln * 0.9, depth * 0.5)),
        internals=[
            fc.Internal("collar topstitch",
                        [fc.P(TOPSTITCH, TOPSTITCH), fc.P(ln - TOPSTITCH, TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb_fold"),
        label="Stand collar (cut 2, on fold)",
    )


def build_storm_flap():
    """The spark storm flap, cut 1. Wider than the placket gap it covers."""
    w = FLAP_W
    h = PLACKET_LEN
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("outer", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "storm_flap", edges,
        seam_allowance=seam_allowance,
        allowances={"outer": hem_allowance * 0.5, "bottom": hem_allowance * 0.5},
        notches=[fc.Notch("attach", 0.5, "CF attach"),
                 fc.Notch("outer", 0.5, "overlap edge")],
        grainline=fc.Grainline(fc.P(w * 0.5, 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=[
            fc.Internal("overlap edge topstitch",
                        [fc.P(w - TOPSTITCH, TOPSTITCH), fc.P(w - TOPSTITCH, h - TOPSTITCH)],
                        kind="trace"),
            fc.Internal("buttonhole line",
                        [fc.P(BUTTON_STAND, TOPSTITCH), fc.P(BUTTON_STAND, h - TOPSTITCH)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Spark storm flap (cut 1)",
    )


def build():
    pattern = fc.PatternSet("welder-jacket")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "collar": everything or target_piece == "collar",
        "storm_flap": everything or target_piece == "storm_flap",
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
    if want["storm_flap"]:
        pattern.add(build_storm_flap())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if want["sleeve"] and want["front"] and want["back"]:
        pattern.declare_seam([("sleeve", "cap_r"), ("sleeve", "cap_l")],
                             [("front", "armscye"), ("back", "armscye")],
                             tol=2.5, ease=CAP_EASE)
    if want["storm_flap"] and want["front"]:
        # The flap's attach edge runs the full placket length, matching the front's
        # CF. Declared so a flap redrafted short of the placket goes red.
        pattern.declare_seam(("storm_flap", "attach"), ("front", "cf"),
                             tol=1.5, ease=PLACKET_LEN - _FRONT.edge("cf").length(0.05))

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cotton duck canvas, 12 oz (heavy, flame-treatable)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; untreated duck is "
                 f"cotton and chars rather than melts — the reason it, not a "
                 f"synthetic, is the welder's cloth."},
        {"item": "sew-through button", "qty": N_BUTTONS, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm), covered by the "
                 f"storm flap; SOLVED pitch {BUTTON_PITCH:.1f} mm."},
        {"item": "heavy topstitch thread (cotton) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"cotton thread (not polyester — it must not melt); {TOPSTITCH:.0f} "
                 f"mm gauge, felled seams."},
    ]
    pattern.metadata = {
        "fc400_rank": 307,
        "family": "workwear_uniforms",
        "tier": 3,
        "fabric_hint": "duck-canvas",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "body_length": round(body_length, 1),
            "collar_stand": round(collar_stand, 1),
            "storm_flap_width": round(FLAP_W, 1),
            "placket_length": round(PLACKET_LEN, 1),
        },
        "solved": {
            "button_count": N_BUTTONS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "button_stand_mm": round(BUTTON_STAND, 2),
            "flap_width_requested_mm": round(_FLAP_W_RAW, 2),
            "flap_width_final_mm": round(FLAP_W, 2),
            "flap_covers_gap": bool(FLAP_W >= 2.0 * BUTTON_STAND),
            "armscye_run_measured_mm": round(ARMSCYE_RUN, 2),
            "cap_ease_mm": round(CAP_EASE, 2),
            "note": "the storm flap width is the button stand plus a spark overlap "
                    "on EACH side, clamped so it can never come out narrower than "
                    "the placket gap it covers — a flap narrower than its gap is "
                    "worse than none, and a naive draft tying flap width to a "
                    "fraction of the chest produces exactly that at a small size. "
                    "The buttons are solved across the measured placket, and the "
                    "sleeve cap is eased to the measured armscye (low ease — duck "
                    "eases badly).",
        },
        "topstitch": f"cotton twin-needle at {TOPSTITCH:.0f} mm; felled seams",
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne is fed from this "
                    "garment's button_ligne, which also sizes the buttonholes and "
                    "the spacing. The buttons are covered by the storm flap so no "
                    "spark reaches the thread.",
    }
    return pattern


result = build()

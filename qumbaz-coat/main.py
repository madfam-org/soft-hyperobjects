"""
Qumbaz linen robe (قمباز) — Fashion Cabinet Heritage Cartridge (FC-500 #494,
heritage_global; Levant — Palestine, Syria, Jordan, Lebanon).

The qumbaz (also kumbaz / qombaz) is the long men's coat-robe of the Levant: ankle-length,
opening all the way down the centre front, crossed right-over-left and held with a long sash
(and, in many regions, a row of small buttons and loops up the chest), with long straight
sleeves and side slits for walking and riding. It is worn over a shirt (and sometimes under a
short jacket or the abaya cloak), in linen or striped silk-cotton, and it is everyday and
festive dress across the Levant.

Two facts govern the draft:

  1. THE FRONT WRAPS AND THE OVERLAP IS REAL. The qumbaz is not an edge-to-edge coat: the right
     front crosses PAST centre front and the left front sits under it, so each front is drafted
     with an overlap beyond centre front, and the buttons/loops run up the crossing edge. The
     overlap is a real parameter, checked so the two fronts always meet with a genuine cross.

  2. THE STAND COLLAR IS CUT TO THE MEASURED NECKLINE. The low stand collar is cut to the
     MEASURED neck run (both fronts including their overlaps + both back quarters), so it sits
     without gaping.

Pieces:
  - front  : one front (cut 2), with the centre-front overlap and the button run.
  - back   : the back (cut on fold), side slits.
  - sleeve : the long straight sleeve (cut 2), gathered lightly at the shoulder.
  - collar : the low stand collar, cut to the MEASURED neckline.

Hardware: front buttons — Yantra4D sew-through-button, LINKED (small ball or cloth buttons).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
robe_length = float(PARAM(lambda: robe_length, 1360.0))
neck_girth = float(PARAM(lambda: neck_girth, 410.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
sleeve_width = float(PARAM(lambda: sleeve_width, 380.0))     # flat sleeve width
armhole_depth = float(PARAM(lambda: armhole_depth, 260.0))
collar_height = float(PARAM(lambda: collar_height, 40.0))
front_overlap = float(PARAM(lambda: front_overlap, 140.0))  # how far the right front crosses
side_slit = float(PARAM(lambda: side_slit, 420.0))
ease = float(PARAM(lambda: ease, 160.0))
button_ligne = float(PARAM(lambda: button_ligne, 16.0))
button_count = int(PARAM(lambda: button_count, 8))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(820.0, min(chest_girth, 1300.0))
robe_length = max(1100.0, min(robe_length, 1600.0))
neck_girth = max(340.0, min(neck_girth, 480.0))
shoulder_width = max(400.0, min(shoulder_width, 540.0))
sleeve_length = max(480.0, min(sleeve_length, 700.0))
sleeve_width = max(300.0, min(sleeve_width, 480.0))
armhole_depth = max(220.0, min(armhole_depth, 340.0))
collar_height = max(25.0, min(collar_height, 60.0))
front_overlap = max(60.0, min(front_overlap, 260.0))
side_slit = max(150.0, min(side_slit, 700.0))
ease = max(100.0, min(ease, 300.0))
button_ligne = max(12.0, min(button_ligne, 26.0))
button_count = max(4, min(button_count, 14))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(15.0, min(hem_allowance, 80.0))

# ── Body geometry ────────────────────────────────────────────────────────────
CHEST_Q = (chest_girth + ease) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_HALF = min((neck_girth + 28.0) / 4.0, HALF_SHOULDER - 30.0)
FRONT_NECK_DROP = NECK_HALF * 0.85 + 14.0
BACK_NECK_DROP = 24.0
side_slit = min(side_slit, (robe_length - armhole_depth) * 0.7)
SHOULDER_Y = robe_length
UNDERARM_Y = robe_length - armhole_depth


def _armscye(x_side, y_underarm, x_shoulder, y_shoulder, front):
    bias = 0.42 if front else 0.30
    run = x_side - x_shoulder
    rise = y_shoulder - y_underarm
    return fc.Bezier(
        fc.P(x_side, y_underarm),
        fc.P(x_side - run * 0.10, y_underarm + rise * 0.42),
        fc.P(x_shoulder + run * bias, y_shoulder - rise * 0.12),
        fc.P(x_shoulder, y_shoulder))


def build_front():
    """One front (cut 2): the body quarter plus the centre-front overlap. x = 0 is the crossing
    edge (past centre front); x = CHEST_Q + overlap is the side."""
    overlap = front_overlap
    x_cross = 0.0
    x_side = CHEST_Q + overlap
    x_shoulder = overlap + HALF_SHOULDER
    x_neck = overlap + NECK_HALF
    p_hem_cross = fc.P(x_cross, 0.0)
    p_hem_side = fc.P(x_side, 0.0)
    p_underarm = fc.P(x_side, UNDERARM_Y)
    p_shoulder_tip = fc.P(x_shoulder, SHOULDER_Y)
    p_neck_shoulder = fc.P(x_neck, SHOULDER_Y)
    p_neck_cross = fc.P(x_cross, SHOULDER_Y - FRONT_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cross, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [_armscye(x_side, UNDERARM_Y, x_shoulder, SHOULDER_Y, True)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(x_neck * 0.7 + x_cross * 0.3, SHOULDER_Y - 6.0),
                                   fc.P(x_cross + (x_neck - x_cross) * 0.3, p_neck_cross.y + 10.0),
                                   p_neck_cross)]),
        # the crossing edge, straight down centre-front-plus-overlap.
        fc.Edge("cross_edge", [fc.Line(p_neck_cross, p_hem_cross)]),
    ]
    internals = [
        fc.Internal("centre-front", [fc.P(overlap, SHOULDER_Y - FRONT_NECK_DROP),
                                     fc.P(overlap, 30.0)], kind="marking"),
        fc.Internal("slit-head", [fc.P(x_side, side_slit), fc.P(x_side - 24.0, side_slit)],
                    kind="marking"),
    ]
    span = (SHOULDER_Y - FRONT_NECK_DROP) - 40.0
    for i in range(button_count):
        t = (i + 0.5) / button_count
        y = 40.0 + span * t
        bx = 12.0 + button_ligne * 0.635
        internals.append(fc.Internal(f"button-{i + 1}", [fc.P(12.0, y), fc.P(bx, y)],
                                     kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", side_slit / max(UNDERARM_Y, 1.0), "slit head")],
        grainline=fc.Grainline(fc.P(x_side * 0.5, hem_allowance + 30.0),
                               fc.P(x_side * 0.5, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (centre-front overlap, button run)",
    )


def build_back():
    top = SHOULDER_Y
    x_side = CHEST_Q
    x_shoulder = HALF_SHOULDER
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side, 0.0)
    p_underarm = fc.P(x_side, UNDERARM_Y)
    p_shoulder_tip = fc.P(x_shoulder, top)
    p_neck_shoulder = fc.P(NECK_HALF, top)
    p_neck_cb = fc.P(0.0, top - BACK_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [_armscye(x_side, UNDERARM_Y, x_shoulder, top, False)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.55, top - 3.0),
                                   fc.P(NECK_HALF * 0.25, p_neck_cb.y + 3.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    internals = [
        fc.Internal("slit-head", [fc.P(x_side, side_slit), fc.P(x_side - 24.0, side_slit)],
                    kind="marking"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", side_slit / max(UNDERARM_Y, 1.0), "slit head")],
        grainline=fc.Grainline(fc.P(x_side * 0.3, hem_allowance + 30.0),
                               fc.P(x_side * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back (side slits), cut on fold",
    )


# ── Measure armscyes + neckline ──────────────────────────────────────────────
_FRONT = build_front()
_BACK = build_back()
FRONT_SCYE = _FRONT.edge("armhole").length(0.2)
BACK_SCYE = _BACK.edge("armhole").length(0.2)
ARMSCYE = FRONT_SCYE + BACK_SCYE
CAP_EASE = 16.0            # a light shoulder gather
CAP_TARGET = ARMSCYE + CAP_EASE
FRONT_NECK = _FRONT.edge("neck").length(0.2)
BACK_NECK = _BACK.edge("neck").length(0.2)
NECK_RUN = 2.0 * FRONT_NECK + 2.0 * BACK_NECK
NECK_NAIVE = neck_girth + 28.0


def _cap_curve(x_right, x_left, y_base, cap_height):
    span = x_right - x_left
    return fc.Bezier(
        fc.P(x_right, y_base),
        fc.P(x_right - span * 0.14, y_base + cap_height * 1.32),
        fc.P(x_left + span * 0.14, y_base + cap_height * 1.32),
        fc.P(x_left, y_base))


def build_sleeve():
    """The long straight sleeve (cut 2): a wide cap solved to the measured armscye, straight
    sides to the wrist. sleeve_width sets the cuff width; the cap is solved above it."""
    cap_height = armhole_depth * 0.5
    y_cap = cap_height
    cap_span = CAP_TARGET * 0.72
    for _ in range(8):
        xr = cap_span / 2.0
        got = fc.Edge("probe", [_cap_curve(xr, -xr, 0.0, cap_height)]).length(0.2)
        if got <= 1e-6:
            break
        cap_span *= CAP_TARGET / got
    total_w = cap_span
    # The cuff can be no wider than the solved cap span, or the cap curve would be stretched
    # past its measured target — clamp it so the sleeve stays a valid taper.
    cuff_open = min(sleeve_width, total_w * 0.95)
    p_bl = fc.P((total_w - cuff_open) / 2.0, -sleeve_length)
    p_br = fc.P((total_w + cuff_open) / 2.0, -sleeve_length)
    p_cap_r = fc.P(total_w, y_cap)
    p_cap_l = fc.P(0.0, y_cap)
    edges = [
        fc.Edge("cuff_edge", [fc.Line(p_bl, p_br)]),
        fc.Edge("under_r", [fc.Line(p_br, p_cap_r)]),
        fc.Edge("cap", [_cap_curve(total_w, 0.0, y_cap, cap_height)]),
        fc.Edge("under_l", [fc.Line(p_cap_l, p_bl)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff_edge": hem_allowance * 0.5},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(total_w / 2.0, y_cap),
                               fc.P(total_w / 2.0, -sleeve_length + 20.0)),
        internals=[fc.Internal("cap-notch",
                               [fc.P(total_w / 2.0, y_cap + cap_height * 0.9),
                                fc.P(total_w / 2.0, y_cap + cap_height * 0.9 - 12.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Long straight sleeve (cap measured to the armscye)",
    )


def build_collar():
    ln = NECK_RUN
    h = collar_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", FRONT_NECK / ln, "left shoulder"),
                 fc.Notch("neck_edge", (FRONT_NECK + BACK_NECK) / ln, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, collar_height + 2.0),
                                        fc.P(ln, collar_height + 2.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Low stand collar (cut to the measured neckline)",
    )


def build():
    pattern = fc.PatternSet("qumbaz-coat")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_FRONT)
    if everything or target_piece == "back":
        pattern.add(_BACK)
    sleeve = build_sleeve()
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    cap_measured = sleeve.edge("cap").length(0.2)
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=2.0, ease=CAP_EASE)
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    pattern.bom = [
        {"item": "washed linen or striped silk-cotton", "qty": round(
            (robe_length + hem_allowance) * 2.6 / 10.0) * 10, "unit": "mm_length",
         "note": "the long coat-robe; linen for everyday, striped atlas silk-cotton for dress."},
        {"item": "front buttons (with loops)", "qty": button_count, "unit": "count",
         "note": f"{button_ligne:.0f}-ligne small buttons up the crossing edge; the Yantra4D "
                 f"sew-through-button solid, linked. Held also by the sash."},
        {"item": "sash / belt", "qty": 1, "unit": "length",
         "note": "a long sash wraps the waist; the front crosses right-over-left beneath it."},
        {"item": "collar interlining", "qty": round(NECK_RUN), "unit": "mm_length", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 494,
        "family": "heritage_global",
        "fabric_hint": "lino-lavado",
        "finished_mm": {
            "chest_girth": round(chest_girth, 1),
            "robe_length": round(robe_length, 1),
            "front_overlap": round(front_overlap, 1),
            "side_slit": round(side_slit, 1),
        },
        "solved": {
            "chest_quarter_mm": round(CHEST_Q, 2),
            "front_overlap_mm": round(front_overlap, 2),
            "front_scye_mm": round(FRONT_SCYE, 3),
            "back_scye_mm": round(BACK_SCYE, 3),
            "armscye_total_mm": round(ARMSCYE, 3),
            "sleeve_cap_target_mm": round(CAP_TARGET, 3),
            "sleeve_cap_measured_mm": round(cap_measured, 3),
            "collar_run_mm": round(NECK_RUN, 3),
            "collar_vs_neck_estimate_mm": round(NECK_RUN - NECK_NAIVE, 3),
            "side_slit_ceiling_mm": round((robe_length - armhole_depth) * 0.7, 2),
            "note": "the qumbaz WRAPS: each front is drafted with a real centre-front overlap "
                    "so the right front crosses past centre and the left sits under it, and "
                    "the buttons/loops run up the crossing edge. The set-in sleeve cap is "
                    "SOLVED to the measured armscye plus a light gather. The low stand collar "
                    "is cut to the MEASURED neckline (both fronts with their overlaps + both "
                    "back quarters), off the naive estimate by collar_vs_neck_estimate_mm.",
        },
        "heritage": {
            "garment": "qumbaz / kumbaz — the Levantine men's long coat-robe",
            "worn": "ankle-length over a shirt, crossed right-over-left and held with a sash "
                    "(and buttons), with side slits; everyday and festive dress across "
                    "Palestine, Syria, Jordan and Lebanon",
            "construction": "wrapped front with a real overlap and a button run, set-in "
                            "sleeves, a low stand collar, side slits",
            "excluded": "no woven stripe (atlas) colourway or regional trim is drawn — the "
                        "cloth is the maker's",
        },
        "hardware": "front buttons with loops: Yantra4D sew-through-button, linked, sized in "
                    "lignes; the robe is also held by the sash.",
    }
    return pattern


result = build()

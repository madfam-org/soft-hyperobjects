"""
Baju Melayu set — Fashion Cabinet Heritage Cartridge (FC-500 #498, heritage_global;
Malay — Malaysia, Brunei, Singapore, southern Thailand, Indonesia).

The baju melayu is the Malay men's outfit: a loose, long-sleeved shirt (the baju) with a raised
stand collar (the cekak musang, "civet's grip") and a short buttoned front placket, worn with
matching trousers (seluar) and — the piece that completes it — the SAMPING, a short cloth
(often songket) wrapped over the trousers at the waist and folded to hang in front. It is the
national dress worn to the mosque, at weddings, and at Hari Raya. This cartridge drafts the
baju shirt, its cekak musang collar, and the samping wrap.

Two facts govern the draft:

  1. THE CEKAK MUSANG COLLAR IS CUT TO THE MEASURED NECKLINE. The raised stand collar is the
     signature of the baju melayu; it is cut to the MEASURED neck run (both fronts + both back
     quarters), not to a neck girth, so it stands cleanly at the throat.

  2. THE SLEEVE IS SET IN, TO THE MEASURED ARMSCYE, AND THE SAMPING IS SOLVED FROM THE WAIST.
     The sleeve cap is solved to the measured armhole so it hangs; the samping wrap length is
     solved from the waist plus the front-fold overlap, so the fold sits right rather than being
     guessed.

Pieces:
  - front  : the baju front (cut 2), short buttoned placket.
  - back   : the baju back (cut on fold).
  - sleeve : the long sleeve, cap MEASURED to the armscye, cut 2.
  - collar : the cekak musang stand collar, cut to the MEASURED neckline.
  - samping: the samping wrap cloth (a marked, solved rectangle).

Hardware: front-placket buttons — Yantra4D sew-through-button, LINKED.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|collar|samping|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
baju_length = float(PARAM(lambda: baju_length, 760.0))
neck_girth = float(PARAM(lambda: neck_girth, 410.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 470.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
armhole_depth = float(PARAM(lambda: armhole_depth, 260.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 230.0))
collar_height = float(PARAM(lambda: collar_height, 45.0))   # the cekak musang stand
placket_length = float(PARAM(lambda: placket_length, 200.0))  # short front opening
ease = float(PARAM(lambda: ease, 160.0))
waist_girth = float(PARAM(lambda: waist_girth, 900.0))       # for the samping
samping_drop = float(PARAM(lambda: samping_drop, 480.0))     # samping length
button_ligne = float(PARAM(lambda: button_ligne, 20.0))
button_count = int(PARAM(lambda: button_count, 3))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(820.0, min(chest_girth, 1300.0))
baju_length = max(640.0, min(baju_length, 900.0))
neck_girth = max(340.0, min(neck_girth, 480.0))
shoulder_width = max(400.0, min(shoulder_width, 540.0))
sleeve_length = max(500.0, min(sleeve_length, 720.0))
armhole_depth = max(220.0, min(armhole_depth, 320.0))
wrist_girth = max(190.0, min(wrist_girth, 280.0))
collar_height = max(30.0, min(collar_height, 65.0))
placket_length = max(120.0, min(placket_length, 320.0))
ease = max(100.0, min(ease, 280.0))
waist_girth = max(700.0, min(waist_girth, 1250.0))
samping_drop = max(360.0, min(samping_drop, 640.0))
button_ligne = max(14.0, min(button_ligne, 30.0))
button_count = max(2, min(button_count, 5))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 45.0))

# ── Body geometry ────────────────────────────────────────────────────────────
CHEST_Q = (chest_girth + ease) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_HALF = min((neck_girth + 28.0) / 4.0, HALF_SHOULDER - 30.0)
FRONT_NECK_DROP = NECK_HALF * 0.8 + 16.0
BACK_NECK_DROP = 24.0
placket_length = min(placket_length, baju_length * 0.5)

# ── The samping solve ────────────────────────────────────────────────────────
SAMPING_WRAP = waist_girth + waist_girth * 0.55   # once round plus a front-fold overlap


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
    top = baju_length
    x_side = CHEST_Q
    x_shoulder = HALF_SHOULDER
    y_underarm = top - armhole_depth
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side, 0.0)
    p_underarm = fc.P(x_side, y_underarm)
    p_shoulder_tip = fc.P(x_shoulder, top)
    p_neck_shoulder = fc.P(NECK_HALF, top)
    p_neck_cf = fc.P(0.0, top - FRONT_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [_armscye(x_side, y_underarm, x_shoulder, top, True)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.6, top - 6.0),
                                   fc.P(NECK_HALF * 0.28, p_neck_cf.y + 10.0),
                                   p_neck_cf)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("placket", [fc.P(12.0, top - FRONT_NECK_DROP),
                                fc.P(12.0, top - FRONT_NECK_DROP - placket_length)],
                    kind="marking"),
    ]
    span = placket_length - 20.0
    for i in range(button_count):
        t = (i + 0.5) / button_count
        y = (top - FRONT_NECK_DROP) - 10.0 - span * t
        bx = 12.0 + button_ligne * 0.635
        internals.append(fc.Internal(f"button-{i + 1}", [fc.P(12.0, y), fc.P(bx, y)],
                                     kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 0.5, "front notch")],
        grainline=fc.Grainline(fc.P(x_side * 0.3, hem_allowance + 30.0),
                               fc.P(x_side * 0.3, y_underarm - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Baju front (short buttoned placket)",
    )


def build_back():
    top = baju_length
    x_side = CHEST_Q
    x_shoulder = HALF_SHOULDER
    y_underarm = top - armhole_depth
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side, 0.0)
    p_underarm = fc.P(x_side, y_underarm)
    p_shoulder_tip = fc.P(x_shoulder, top)
    p_neck_shoulder = fc.P(NECK_HALF, top)
    p_neck_cb = fc.P(0.0, top - BACK_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [_armscye(x_side, y_underarm, x_shoulder, top, False)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.55, top - 3.0),
                                   fc.P(NECK_HALF * 0.25, p_neck_cb.y + 3.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "side mid")],
        grainline=fc.Grainline(fc.P(x_side * 0.3, hem_allowance + 30.0),
                               fc.P(x_side * 0.3, y_underarm - 30.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Baju back (cut on fold)",
    )


# ── Measure armscyes + neckline ──────────────────────────────────────────────
_FRONT = build_front()
_BACK = build_back()
FRONT_SCYE = _FRONT.edge("armhole").length(0.2)
BACK_SCYE = _BACK.edge("armhole").length(0.2)
ARMSCYE = FRONT_SCYE + BACK_SCYE
CAP_EASE = 12.0
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
    cuff_open = wrist_girth + 40.0
    cap_height = armhole_depth * 0.55
    y_cap = cap_height
    cap_span = CAP_TARGET * 0.72
    for _ in range(8):
        xr = cap_span / 2.0
        got = fc.Edge("probe", [_cap_curve(xr, -xr, 0.0, cap_height)]).length(0.2)
        if got <= 1e-6:
            break
        cap_span *= CAP_TARGET / got
    cap_span = max(cap_span, cuff_open * 1.02)
    total_w = cap_span
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
        label="Long sleeve (cap measured to the armscye)",
    )


def build_collar():
    """The cekak musang stand collar, cut to the MEASURED neckline run."""
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
        label="Cekak musang stand collar (cut to the measured neckline)",
    )


def build_samping():
    """The samping wrap cloth: a solved rectangle wrapped over the trousers and folded in front.
    Its width is the wrap (once round the waist plus the front-fold overlap); its drop is the
    samping length."""
    w = SAMPING_WRAP
    h = samping_drop
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("hem", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("waist", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("front-fold", [fc.P(w - waist_girth * 0.55, 0.0),
                                   fc.P(w - waist_girth * 0.55, h)], kind="marking"),
        fc.Internal("songket-band", [fc.P(0.0, hem_allowance + 40.0),
                                     fc.P(w, hem_allowance + 40.0)], kind="marking"),
    ]
    return fc.Piece(
        "samping", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "waist": 0.0, "end_r": 0.0, "end_l": 0.0},
        notches=[fc.Notch("waist", 0.5, "centre"),
                 fc.Notch("waist", (w - waist_girth * 0.55) / w, "front-fold start")],
        grainline=fc.Grainline(fc.P(w * 0.5, hem_allowance + 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Samping wrap cloth (songket)",
    )


def build():
    pattern = fc.PatternSet("baju-melayu-set")
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
    if everything or target_piece == "samping":
        pattern.add(build_samping())

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
        {"item": "cotton, linen, or songket-blend (baju)", "qty": round(
            (baju_length + sleeve_length + hem_allowance) * 2.4 / 10.0) * 10,
         "unit": "mm_length", "note": "the loose baju shirt."},
        {"item": "front-placket buttons", "qty": button_count, "unit": "count",
         "note": f"{button_ligne:.0f}-ligne buttons on the short placket; the Yantra4D "
                 f"sew-through-button solid, linked."},
        {"item": "samping cloth (songket / plaid)", "qty": round(SAMPING_WRAP), "unit": "mm_length",
         "note": f"the samping wraps once round the waist ({waist_girth:.0f} mm) plus a "
                 f"front-fold overlap — {SAMPING_WRAP:.0f} mm total. The songket weave is the "
                 f"weaver's; none is drawn."},
        {"item": "collar interlining", "qty": round(NECK_RUN), "unit": "mm_length",
         "note": "the cekak musang stand is interfaced to stand at the throat."},
    ]
    pattern.metadata = {
        "fc500_rank": 498,
        "family": "heritage_global",
        "fabric_hint": "algodon-tejido",
        "finished_mm": {
            "chest_girth": round(chest_girth, 1),
            "baju_length": round(baju_length, 1),
            "collar_height": round(collar_height, 1),
            "samping_wrap": round(SAMPING_WRAP, 1),
        },
        "solved": {
            "chest_quarter_mm": round(CHEST_Q, 2),
            "front_scye_mm": round(FRONT_SCYE, 3),
            "back_scye_mm": round(BACK_SCYE, 3),
            "armscye_total_mm": round(ARMSCYE, 3),
            "sleeve_cap_target_mm": round(CAP_TARGET, 3),
            "sleeve_cap_measured_mm": round(cap_measured, 3),
            "collar_run_mm": round(NECK_RUN, 3),
            "collar_naive_estimate_mm": round(NECK_NAIVE, 3),
            "collar_vs_neck_estimate_mm": round(NECK_RUN - NECK_NAIVE, 3),
            "samping_wrap_mm": round(SAMPING_WRAP, 2),
            "note": "the cekak musang stand collar is cut to the MEASURED neckline (both "
                    "fronts + both back quarters), off the naive neck_girth estimate by "
                    "collar_vs_neck_estimate_mm, so it stands cleanly. The set-in sleeve cap "
                    "is SOLVED to the measured armscye plus ease. The samping wrap is solved "
                    "from the waist plus a front-fold overlap so the fold sits right.",
        },
        "heritage": {
            "garment": "baju melayu — the Malay men's outfit",
            "worn": "the baju shirt with the cekak musang collar, seluar trousers, and the "
                    "samping wrapped over at the waist; the national dress for the mosque, "
                    "weddings and Hari Raya across Malaysia, Brunei, Singapore and beyond",
            "construction": "loose set-in-sleeve shirt, cekak musang stand collar, short "
                            "buttoned placket, samping wrap cloth",
            "excluded": "no songket weave, tekat embroidery, or state-specific motif is drawn "
                        "— those are the weaver's and the region's",
        },
        "hardware": "front-placket buttons: Yantra4D sew-through-button, linked, sized in "
                    "lignes.",
    }
    return pattern


result = build()

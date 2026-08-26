"""
Hanbok magoja overjacket (마고자) — Fashion Cabinet Heritage Cartridge (FC-500 #488,
heritage_global; Korean).

The magoja is the Korean overjacket worn over the jeogori (저고리): a hip-length jacket,
straight down the centre front (NOT wrapped and tied like the jeogori), fastened with a small
number of buttons — traditionally amber or knotted — with the same soft raglan-free one-piece
sleeve carrying the gentle 배래 (baerae) curved underarm, and short side vents. It was adopted
into Korean dress in the late 19th century (from a Manchu jacket) and became a standard warm
outer layer of the hanbok for both men and women.

Two facts govern the draft:

  1. THE SLEEVE IS CUT IN ONE, WITH THE 배래 CURVE. There is no set-in armscye: the sleeve runs
     straight out from the shoulder, and the underarm is the soft 배래 curve, not a right angle
     and not a Western scye. The seam that closes it — the sleeve underseam continuing into the
     side seam — is declared and MEASURED so front and back agree.

  2. THE FRONT IS STRAIGHT AND BUTTONED, NOT WRAPPED. Unlike the jeogori, the magoja meets
     edge-to-edge (or with a small overlap) at centre front and buttons; there are no goreum
     ties. The 깃 (git) collar band frames the neck and is cut to the MEASURED neckline; the
     white 동정 (dongjeong) collar strip sits on top of it (a marked strip, applied in make-up).

Pieces:
  - back   : the back, cut on fold, one-piece sleeve with 배래 curve.
  - front  : the front (cut 2), straight buttoned centre front, one-piece sleeve.
  - git    : the 깃 collar band, cut to the MEASURED neckline; 동정 strip marked.

Hardware: front buttons — Yantra4D sew-through-button, LINKED (amber/shell traditional).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # back|front|git|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
magoja_length = float(PARAM(lambda: magoja_length, 620.0))  # nape to hem
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
back_neck_width = float(PARAM(lambda: back_neck_width, 180.0))  # half back neck
sleeve_length = float(PARAM(lambda: sleeve_length, 560.0))  # neck to cuff (one-piece)
sleeve_depth = float(PARAM(lambda: sleeve_depth, 280.0))    # armhole depth at the body
cuff_opening = float(PARAM(lambda: cuff_opening, 260.0))    # sleeve mouth
baerae_curve = float(PARAM(lambda: baerae_curve, 40.0))     # depth of the 배래 curve
git_width = float(PARAM(lambda: git_width, 55.0))           # 깃 collar band width
wrap_ease = float(PARAM(lambda: wrap_ease, 120.0))
side_vent = float(PARAM(lambda: side_vent, 90.0))
button_ligne = float(PARAM(lambda: button_ligne, 26.0))
button_count = int(PARAM(lambda: button_count, 3))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(780.0, min(chest_girth, 1200.0))
magoja_length = max(520.0, min(magoja_length, 780.0))
neck_girth = max(340.0, min(neck_girth, 480.0))
back_neck_width = max(130.0, min(back_neck_width, 240.0))
sleeve_length = max(420.0, min(sleeve_length, 680.0))
sleeve_depth = max(220.0, min(sleeve_depth, 360.0))
cuff_opening = max(180.0, min(cuff_opening, 360.0))
baerae_curve = max(10.0, min(baerae_curve, 90.0))
git_width = max(35.0, min(git_width, 85.0))
wrap_ease = max(60.0, min(wrap_ease, 220.0))
side_vent = max(0.0, min(side_vent, 220.0))
button_ligne = max(16.0, min(button_ligne, 40.0))
button_count = max(2, min(button_count, 5))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 50.0))

# ── Derived geometry ─────────────────────────────────────────────────────────
HALF_BODY = (chest_girth + wrap_ease) / 4.0
NECK_HALF_BACK = min(back_neck_width, HALF_BODY - 30.0)
FRONT_NECK_DROP = min((neck_girth + 30.0) / 4.0 * 0.9, sleeve_depth * 0.55)
BACK_NECK_DROP = 22.0
side_vent = min(side_vent, (magoja_length - sleeve_depth) * 0.8)
SHOULDER_Y = magoja_length
UNDERARM_Y = magoja_length - sleeve_depth
cuff_half = cuff_opening / 2.0


def _baerae(x_underarm, y_underarm, x_cuff, y_cuff, depth):
    """The 배래 underarm curve: from the body underarm out and down to the cuff, dipping by
    `depth` — the soft Korean sleeve underseam, not a straight line and not a scye."""
    return fc.Bezier(
        fc.P(x_underarm, y_underarm),
        fc.P(x_underarm + (x_cuff - x_underarm) * 0.4, y_underarm - depth),
        fc.P(x_cuff - (x_cuff - x_underarm) * 0.2, y_cuff - depth * 0.3),
        fc.P(x_cuff, y_cuff))


def build_back():
    """The back, cut on the CB fold: straight body, one-piece sleeve with 배래 curve."""
    hb = HALF_BODY
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hb, 0.0)
    p_underarm = fc.P(hb, UNDERARM_Y)
    p_cuff_low = fc.P(hb + sleeve_length, UNDERARM_Y + (sleeve_depth - cuff_opening) * 0.5
                      if sleeve_depth > cuff_opening else UNDERARM_Y + 20.0)
    p_cuff_high = fc.P(hb + sleeve_length, SHOULDER_Y - 20.0)
    p_neck_shoulder = fc.P(NECK_HALF_BACK, SHOULDER_Y)
    p_neck_cb = fc.P(0.0, SHOULDER_Y - BACK_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("baerae", [_baerae(hb, UNDERARM_Y, hb + sleeve_length, p_cuff_low.y,
                                   baerae_curve)]),
        fc.Edge("cuff", [fc.Line(p_cuff_low, p_cuff_high)]),
        fc.Edge("shoulder", [fc.Line(p_cuff_high, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF_BACK * 0.55, SHOULDER_Y - 3.0),
                                   fc.P(NECK_HALF_BACK * 0.25, p_neck_cb.y + 3.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    internals = [
        fc.Internal("vent", [fc.P(hb, side_vent), fc.P(hb - 20.0, side_vent)], kind="marking"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.5, "sleeve mid"),
                 fc.Notch("side", side_vent / max(UNDERARM_Y, 1.0), "vent head")],
        grainline=fc.Grainline(fc.P(hb * 0.3, hem_allowance + 20.0),
                               fc.P(hb * 0.3, UNDERARM_Y - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back (one-piece sleeve, 배래 curve), cut on fold",
    )


def build_front():
    """The front (cut 2): straight buttoned centre front, one-piece sleeve with 배래 curve."""
    hb = HALF_BODY
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hb, 0.0)
    p_underarm = fc.P(hb, UNDERARM_Y)
    p_cuff_low = fc.P(hb + sleeve_length, UNDERARM_Y + (sleeve_depth - cuff_opening) * 0.5
                      if sleeve_depth > cuff_opening else UNDERARM_Y + 20.0)
    p_cuff_high = fc.P(hb + sleeve_length, SHOULDER_Y - 20.0)
    p_neck_shoulder = fc.P(NECK_HALF_BACK, SHOULDER_Y)
    p_neck_cf = fc.P(0.0, SHOULDER_Y - FRONT_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("baerae", [_baerae(hb, UNDERARM_Y, hb + sleeve_length, p_cuff_low.y,
                                   baerae_curve)]),
        fc.Edge("cuff", [fc.Line(p_cuff_low, p_cuff_high)]),
        fc.Edge("shoulder", [fc.Line(p_cuff_high, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF_BACK * 0.6, SHOULDER_Y - 6.0),
                                   fc.P(NECK_HALF_BACK * 0.28, p_neck_cf.y + 10.0),
                                   p_neck_cf)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("vent", [fc.P(hb, side_vent), fc.P(hb - 20.0, side_vent)], kind="marking"),
    ]
    span = (SHOULDER_Y - FRONT_NECK_DROP) - 40.0
    for i in range(button_count):
        t = (i + 0.5) / button_count
        y = 40.0 + span * t
        bx = 10.0 + button_ligne * 0.635
        internals.append(fc.Internal(f"button-{i + 1}", [fc.P(10.0, y), fc.P(bx, y)],
                                     kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.5, "sleeve mid"),
                 fc.Notch("side", side_vent / max(UNDERARM_Y, 1.0), "vent head")],
        grainline=fc.Grainline(fc.P(hb * 0.3, hem_allowance + 20.0),
                               fc.P(hb * 0.3, UNDERARM_Y - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (straight buttoned CF, one-piece sleeve)",
    )


# ── The git collar, cut to the MEASURED neckline ─────────────────────────────
_BACK = build_back()
_FRONT = build_front()
BACK_NECK = _BACK.edge("neck").length(0.2)
FRONT_NECK = _FRONT.edge("neck").length(0.2)
NECK_RUN = 2.0 * BACK_NECK + 2.0 * FRONT_NECK
NECK_NAIVE = neck_girth + 30.0


def build_git():
    """The 깃 collar band, cut to the MEASURED neckline; the white 동정 strip is marked."""
    ln = NECK_RUN
    h = git_width * 2.0 + 4.0
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
        "git", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", FRONT_NECK / ln, "left shoulder"),
                 fc.Notch("neck_edge", (FRONT_NECK + BACK_NECK) / ln, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, git_width + 2.0),
                                        fc.P(ln, git_width + 2.0)], kind="marking"),
                   fc.Internal("dongjeong-strip",
                               [fc.P(0.0, git_width + 2.0 + git_width * 0.4),
                                fc.P(ln, git_width + 2.0 + git_width * 0.4)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="깃 collar band (cut to the measured neckline; 동정 strip marked)",
    )


def build():
    pattern = fc.PatternSet("hanbok-magoja")
    everything = target_piece == "set"
    if everything or target_piece == "back":
        pattern.add(_BACK)
    if everything or target_piece == "front":
        pattern.add(_FRONT)
    if everything or target_piece == "git":
        pattern.add(build_git())

    if everything:
        # The side seam and sleeve underseam (배래) match front to back.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "baerae"), ("back", "baerae"), tol=1.0)
        pattern.declare_seam(("front", "cuff"), ("back", "cuff"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # THE seam that solves: the 깃 collar band against the MEASURED neckline.
        pattern.declare_seam(("git", "neck_edge"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    pattern.bom = [
        {"item": "silk or ramie (magoja shell) + lining", "qty": round(
            (magoja_length + hem_allowance) * 2.2 / 10.0) * 10, "unit": "mm_length",
         "note": "the magoja is usually lined and often lightly padded for warmth."},
        {"item": "front buttons (단추)", "qty": button_count, "unit": "count",
         "note": f"{button_ligne:.0f}-ligne buttons; amber or shell traditional. The Yantra4D "
                 f"sew-through-button solid, linked. There are NO goreum ties — the magoja "
                 f"buttons straight, unlike the jeogori."},
        {"item": "동정 (dongjeong) white collar strip", "qty": round(NECK_RUN), "unit": "mm_length",
         "note": "the removable white strip applied over the 깃 collar band."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 488,
        "family": "heritage_global",
        "fabric_hint": "seda-satinada",
        "finished_mm": {
            "chest_girth": round(chest_girth, 1),
            "magoja_length": round(magoja_length, 1),
            "sleeve_length": round(sleeve_length, 1),
            "git_width": round(git_width, 1),
        },
        "solved": {
            "half_body_mm": round(HALF_BODY, 2),
            "front_neck_quarter_mm": round(FRONT_NECK, 3),
            "back_neck_quarter_mm": round(BACK_NECK, 3),
            "git_run_mm": round(NECK_RUN, 3),
            "git_naive_estimate_mm": round(NECK_NAIVE, 3),
            "git_vs_neck_estimate_mm": round(NECK_RUN - NECK_NAIVE, 3),
            "baerae_curve_mm": round(baerae_curve, 2),
            "side_vent_mm": round(side_vent, 2),
            "note": "the magoja sleeve is CUT IN ONE with the body, its underseam the soft "
                    "배래 (baerae) curve rather than a set-in scye; front and back are declared "
                    "equal along it. The front is STRAIGHT and BUTTONED (no goreum ties, unlike "
                    "the jeogori). The 깃 (git) collar band is cut to the MEASURED neckline "
                    "(both fronts + both backs), off the naive neck_girth estimate by "
                    "git_vs_neck_estimate_mm; the white 동정 (dongjeong) strip is marked, "
                    "applied over it in make-up.",
        },
        "heritage": {
            "garment": "마고자 magoja — the Korean hanbok overjacket",
            "worn": "over the jeogori as a warm outer layer; adopted into hanbok in the late "
                    "19th century, worn by men and women",
            "construction": "one-piece sleeve with the 배래 curve, straight buttoned front "
                            "(no goreum ties), 깃 collar band with the 동정 strip, side vents",
            "excluded": "no woven or embroidered motif is drafted — the cloth is the maker's",
        },
        "hardware": "front buttons: Yantra4D sew-through-button, linked, sized in lignes "
                    "(amber or shell traditional).",
    }
    return pattern


result = build()

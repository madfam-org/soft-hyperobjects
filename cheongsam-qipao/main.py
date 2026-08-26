"""
Cheongsam (qipao 旗袍) — Fashion Cabinet Heritage Cartridge (FC-500 #489,
heritage_global; Chinese women's fitted dress).

The cheongsam (Cantonese 長衫 chèuhngsāam) or qipao (Mandarin 旗袍) is the fitted women's
Chinese dress that evolved in 1920s Shanghai from the looser Manchu banner gown: a
body-skimming sheath with a stand collar (立領), the curved 大襟 (dàjīn) diagonal opening
from the throat across the chest to the right underarm, knotted-frog and hook-and-eye
closures along that curve, and high side slits. Unlike the men's changpao (a panel garment),
the qipao is SHAPED — it has bust and waist darts and follows the body — so the draft is a
fitted block, but the 大襟 is still the seam that must solve.

Two facts govern the draft:

  1. THE BODY IS FITTED, THROUGH THE WAIST. The front and back carry waist suppression
     (darts) sized from the bust-to-waist and hip-to-waist differences, so the sheath follows
     the figure. The waist is SOLVED from the three girths (bust, waist, hip), not guessed.

  2. THE 大襟 IS DRAFTED ONCE AND MEASURED. The curved overlap that carries the closure runs
     from the throat to the right underarm; the panel beneath it must carry an edge of exactly
     that length or the front twists. The curve is drawn once, MEASURED, and the collar and
     the closure spacing read that measurement. The hook-and-eye is real hardware, sized from
     the closure, spaced along the MEASURED curve.

Pieces:
  - front  : the fitted front (cut on fold), with waist dart and the marked 大襟 seat.
  - dajin  : the 大襟 overlap panel (cut 2), its curved edge the MEASURED curve.
  - back   : the fitted back (cut on fold), with waist dart, high side slit.
  - collar : the stand collar (立領), cut to the MEASURED neckline.

Hardware: hook-and-eye along the dajin — Yantra4D hook-and-eye, LINKED.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|dajin|back|collar|set

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
waist_girth = float(PARAM(lambda: waist_girth, 720.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
qipao_length = float(PARAM(lambda: qipao_length, 1200.0))    # shoulder to hem
neck_girth = float(PARAM(lambda: neck_girth, 360.0))
collar_height = float(PARAM(lambda: collar_height, 45.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 380.0))  # tip to tip
armhole_depth = float(PARAM(lambda: armhole_depth, 220.0))    # shoulder to underarm
bust_to_waist = float(PARAM(lambda: bust_to_waist, 360.0))    # shoulder line to waist
dajin_drop = float(PARAM(lambda: dajin_drop, 260.0))         # throat to underarm on the curve
slit_height = float(PARAM(lambda: slit_height, 380.0))       # side slit from hem
bust_ease = float(PARAM(lambda: bust_ease, 80.0))
closure_span = float(PARAM(lambda: closure_span, 22.0))      # hook-and-eye size (mm)
closure_count = int(PARAM(lambda: closure_count, 4))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
bust_girth = max(760.0, min(bust_girth, 1200.0))
waist_girth = max(580.0, min(waist_girth, 1080.0))
hip_girth = max(820.0, min(hip_girth, 1300.0))
qipao_length = max(900.0, min(qipao_length, 1500.0))
neck_girth = max(300.0, min(neck_girth, 440.0))
collar_height = max(28.0, min(collar_height, 70.0))
shoulder_width = max(320.0, min(shoulder_width, 460.0))
armhole_depth = max(180.0, min(armhole_depth, 290.0))
bust_to_waist = max(300.0, min(bust_to_waist, 440.0))
dajin_drop = max(160.0, min(dajin_drop, 380.0))
slit_height = max(0.0, min(slit_height, 700.0))
bust_ease = max(40.0, min(bust_ease, 160.0))
closure_span = max(12.0, min(closure_span, 40.0))
closure_count = max(3, min(closure_count, 8))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(15.0, min(hem_allowance, 80.0))

# ── The fit solve — the waist is SOLVED from the three girths ────────────────
BUST_Q = (bust_girth + bust_ease) / 4.0
WAIST_Q = (waist_girth + bust_ease * 0.5) / 4.0
HIP_Q = (hip_girth + bust_ease * 0.75) / 4.0
# The waist dart take-up per panel is the difference between the bust quarter and the waist
# quarter, split between the side seam and a vertical dart. Clamp so the dart is never
# negative (a waist wider than the bust just means no dart, not a reversed one).
WAIST_SUPPRESSION = max(BUST_Q - WAIST_Q, 0.0)
SIDE_TAKE = WAIST_SUPPRESSION * 0.45          # taken at the side seam
DART_TAKE = WAIST_SUPPRESSION - SIDE_TAKE     # taken as a vertical dart
HALF_SHOULDER = shoulder_width / 2.0
NECK_HALF = (neck_girth + 24.0) / 4.0
FRONT_NECK_DROP = min(NECK_HALF * 0.7 + 12.0, dajin_drop * 0.35)
BACK_NECK_DROP = 20.0
# The dajin horizontal reach across the front: clear of the neck, short of the side.
DAJIN_X = min(max(BUST_Q * 0.72, NECK_HALF + 40.0), BUST_Q - 20.0)
armhole_depth = min(armhole_depth, bust_to_waist - 40.0)
slit_height = min(slit_height, (qipao_length - bust_to_waist) * 0.85)

SHOULDER_Y = qipao_length
WAIST_Y = qipao_length - bust_to_waist
UNDERARM_Y = qipao_length - armhole_depth


def _dajin_curve(x_neck, y_neck, x_arm, y_arm):
    """The 大襟 curve: out from the neck, then down to the underarm — biased outward near the
    neck and downward near the underarm, the shape of a real dajin."""
    return fc.Bezier(
        fc.P(x_neck, y_neck),
        fc.P(x_neck + (x_arm - x_neck) * 0.6, y_neck - (y_neck - y_arm) * 0.10),
        fc.P(x_arm, y_arm + (y_neck - y_arm) * 0.42),
        fc.P(x_arm, y_arm))


def _side_seam(y_hem, y_waist, y_underarm, x_hip, x_waist, x_bust):
    """The fitted side seam: hip out at the hem, drawn in at the waist, out again to the
    underarm — one smooth curve through the three widths."""
    return [
        fc.Bezier(fc.P(x_hip, y_hem),
                  fc.P(x_hip, y_hem + (y_waist - y_hem) * 0.45),
                  fc.P(x_waist, y_waist - (y_waist - y_hem) * 0.18),
                  fc.P(x_waist, y_waist)),
        fc.Bezier(fc.P(x_waist, y_waist),
                  fc.P(x_waist, y_waist + (y_underarm - y_waist) * 0.30),
                  fc.P(x_bust, y_underarm - (y_underarm - y_waist) * 0.35),
                  fc.P(x_bust, y_underarm)),
    ]


def build_front():
    """The fitted FRONT, cut on the CF fold: waist-shaped, with the marked 大襟 seat."""
    x_hip = HIP_Q
    x_waist = WAIST_Q + SIDE_TAKE
    x_bust = BUST_Q
    x_shoulder = HALF_SHOULDER
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_hip, 0.0)
    p_underarm = fc.P(x_bust, UNDERARM_Y)
    p_shoulder_tip = fc.P(x_shoulder, SHOULDER_Y)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y)
    p_neck_cf = fc.P(0.0, SHOULDER_Y - FRONT_NECK_DROP)
    side = _side_seam(0.0, WAIST_Y, UNDERARM_Y, x_hip, x_waist, x_bust)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", side),
        fc.Edge("armhole", [fc.Bezier(p_underarm,
                                      fc.P(x_bust, UNDERARM_Y + (SHOULDER_Y - UNDERARM_Y) * 0.4),
                                      fc.P(x_shoulder + (x_bust - x_shoulder) * 0.4,
                                           SHOULDER_Y - (SHOULDER_Y - UNDERARM_Y) * 0.1),
                                      p_shoulder_tip)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.6, SHOULDER_Y - 6.0),
                                   fc.P(NECK_HALF * 0.28, p_neck_cf.y + 10.0),
                                   p_neck_cf)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("dajin-seat",
                    [fc.P(NECK_HALF, SHOULDER_Y - FRONT_NECK_DROP),
                     fc.P(DAJIN_X * 0.7, SHOULDER_Y - FRONT_NECK_DROP - dajin_drop * 0.18),
                     fc.P(DAJIN_X, UNDERARM_Y + dajin_drop * 0.30),
                     fc.P(DAJIN_X, UNDERARM_Y)], kind="marking"),
        # the waist dart: a vertical fold taking DART_TAKE at the waist.
        fc.Internal("waist-dart",
                    [fc.P(BUST_Q * 0.5, WAIST_Y - 90.0),
                     fc.P(BUST_Q * 0.5 - DART_TAKE * 0.5, WAIST_Y),
                     fc.P(BUST_Q * 0.5, WAIST_Y + 110.0)], kind="dart"),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "waist"),
                 fc.Notch("hem", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(x_bust * 0.3, hem_allowance + 30.0),
                               fc.P(x_bust * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Fitted front (waist dart + 大襟 seat), cut on fold",
    )


def build_back():
    """The fitted BACK, cut on the CB fold: waist-shaped, high side slit."""
    x_hip = HIP_Q
    x_waist = WAIST_Q + SIDE_TAKE
    x_bust = BUST_Q
    x_shoulder = HALF_SHOULDER
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_hip, 0.0)
    p_underarm = fc.P(x_bust, UNDERARM_Y)
    p_shoulder_tip = fc.P(x_shoulder, SHOULDER_Y)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y)
    p_neck_cb = fc.P(0.0, SHOULDER_Y - BACK_NECK_DROP)
    side = _side_seam(0.0, WAIST_Y, UNDERARM_Y, x_hip, x_waist, x_bust)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", side),
        fc.Edge("armhole", [fc.Bezier(p_underarm,
                                      fc.P(x_bust, UNDERARM_Y + (SHOULDER_Y - UNDERARM_Y) * 0.4),
                                      fc.P(x_shoulder + (x_bust - x_shoulder) * 0.4,
                                           SHOULDER_Y - (SHOULDER_Y - UNDERARM_Y) * 0.1),
                                      p_shoulder_tip)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.55, SHOULDER_Y - 3.0),
                                   fc.P(NECK_HALF * 0.25, p_neck_cb.y + 3.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    internals = [
        fc.Internal("slit-head", [fc.P(x_hip, slit_height), fc.P(x_hip - 24.0, slit_height)],
                    kind="marking"),
        fc.Internal("waist-dart",
                    [fc.P(BUST_Q * 0.5, WAIST_Y - 100.0),
                     fc.P(BUST_Q * 0.5 - DART_TAKE * 0.5, WAIST_Y),
                     fc.P(BUST_Q * 0.5, WAIST_Y + 120.0)], kind="dart"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "waist"),
                 fc.Notch("side", slit_height / max(UNDERARM_Y, 1.0), "slit head")],
        grainline=fc.Grainline(fc.P(x_bust * 0.3, hem_allowance + 30.0),
                               fc.P(x_bust * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Fitted back (waist dart, high slit), cut on fold",
    )


# ── The dajin curve, MEASURED ────────────────────────────────────────────────
_NECK_PT = (NECK_HALF, SHOULDER_Y - FRONT_NECK_DROP)
_ARM_PT = (DAJIN_X, UNDERARM_Y)
_CURVE = _dajin_curve(_NECK_PT[0], _NECK_PT[1], _ARM_PT[0], _ARM_PT[1])
DAJIN_LEN = _CURVE.length(0.2)
DAJIN_CHORD = math.hypot(_ARM_PT[0] - _NECK_PT[0], _NECK_PT[1] - _ARM_PT[1])
CHORD_SHORTFALL = DAJIN_LEN - DAJIN_CHORD


def build_dajin():
    """The 大襟 overlap panel (cut 2 — face and facing). Its curved edge IS the drafted curve,
    the same curve the front marks as `dajin-seat`."""
    x0 = 0.0
    top = SHOULDER_Y
    p_bl = fc.P(x0, UNDERARM_Y)
    p_br = fc.P(DAJIN_X, UNDERARM_Y)
    p_neck = fc.P(NECK_HALF, top - FRONT_NECK_DROP)
    p_shoulder = fc.P(NECK_HALF, top)
    p_tl = fc.P(x0, top)
    edges = [
        fc.Edge("under_edge", [fc.Line(p_bl, p_br)]),
        fc.Edge("dajin", [_dajin_curve(DAJIN_X, UNDERARM_Y, NECK_HALF, top - FRONT_NECK_DROP)]),
        fc.Edge("neck", [fc.Line(p_neck, p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_tl)]),
        fc.Edge("cf", [fc.Line(p_tl, p_bl)]),
    ]
    internals = []
    dajin_edge = fc.Edge("probe",
                         [_dajin_curve(DAJIN_X, UNDERARM_Y, NECK_HALF, top - FRONT_NECK_DROP)])
    for i in range(closure_count):
        t = (i + 0.5) / closure_count
        pt, tangent = dajin_edge.point_at_fraction(t, 0.2)
        nx, ny = -tangent.y, tangent.x
        internals.append(fc.Internal(
            f"closure-{i + 1}",
            [fc.P(pt.x - nx * closure_span * 0.5, pt.y - ny * closure_span * 0.5),
             fc.P(pt.x + nx * closure_span * 0.5, pt.y + ny * closure_span * 0.5)],
            kind="marking"))
    return fc.Piece(
        "dajin", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("dajin", 0.5, "dajin midpoint")],
        grainline=fc.Grainline(fc.P(DAJIN_X * 0.35, UNDERARM_Y + 40.0),
                               fc.P(DAJIN_X * 0.35, top - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Dajin overlap panel (大襟)",
    )


# ── The collar, cut to the MEASURED neckline ─────────────────────────────────
_FRONT = build_front()
_BACK = build_back()
_DAJIN = build_dajin()
FRONT_NECK = _FRONT.edge("neck").length(0.2)
BACK_NECK = _BACK.edge("neck").length(0.2)
DAJIN_NECK = _DAJIN.edge("neck").length(0.2)
DAJIN_MEASURED = _DAJIN.edge("dajin").length(0.2)
# The stand collar runs the whole neckline: the left front quarter (on the fold, so ×2 minus
# the dajin overlap on the right), the two back quarters, and the dajin's own neck run.
COLLAR_RUN = FRONT_NECK + 2.0 * BACK_NECK + DAJIN_NECK
COLLAR_NAIVE = neck_girth + 24.0


def build_collar():
    """The 立領 stand collar, cut to the MEASURED neckline run."""
    ln = COLLAR_RUN
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
                                        fc.P(ln, collar_height + 2.0)], kind="marking"),
                   fc.Internal("throat-hook", [fc.P(ln - closure_span, collar_height * 0.5),
                                               fc.P(ln - 6.0, collar_height * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Stand collar (立領)",
    )


def build():
    pattern = fc.PatternSet("cheongsam-qipao")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_FRONT)
    if everything or target_piece == "dajin":
        pattern.add(_DAJIN)
    if everything or target_piece == "back":
        pattern.add(_BACK)
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        # The side seams: fitted front side to fitted back side (same three widths).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        # The shoulder seams and armscye edges match front to back.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "armhole"), ("back", "armhole"), tol=2.0)
        # THE seam that had to solve: the stand collar against the MEASURED neckline —
        # left front, both backs, and the dajin's own neck edge.
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("back", "neck"), ("back", "neck"),
                              ("dajin", "neck")], tol=1.5)

    pattern.bom = [
        {"item": "brocade silk, satin, or printed silk", "qty": round(
            (qipao_length + hem_allowance) * 1.6 / 10.0) * 10, "unit": "mm_length",
         "note": "the fitted sheath; a firmly woven brocade or satin holds the fit."},
        {"item": "hook-and-eye closures (along the dajin)", "qty": closure_count,
         "unit": "count",
         "note": f"{closure_span:.0f} mm hook-and-eye sets spaced along the MEASURED 大襟 "
                 f"curve; the Yantra4D hook-and-eye solid, linked. Knotted 盤扣 frogs are "
                 f"traditional alongside; those are hand-made cloth, not drafted here."},
        {"item": "collar & body interlining", "qty": round(COLLAR_RUN), "unit": "mm_length",
         "note": "the 立領 stand and the fitted body are interfaced to hold the shape."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 489,
        "family": "heritage_global",
        "fabric_hint": "brocado-seda",
        "finished_mm": {
            "bust_girth": round(bust_girth, 1),
            "waist_girth": round(waist_girth, 1),
            "hip_girth": round(hip_girth, 1),
            "qipao_length": round(qipao_length, 1),
            "collar_height": round(collar_height, 1),
            "slit_height": round(slit_height, 1),
        },
        "solved": {
            "bust_quarter_mm": round(BUST_Q, 2),
            "waist_quarter_mm": round(WAIST_Q, 2),
            "hip_quarter_mm": round(HIP_Q, 2),
            "waist_suppression_mm": round(WAIST_SUPPRESSION, 2),
            "side_take_mm": round(SIDE_TAKE, 2),
            "dart_take_mm": round(DART_TAKE, 2),
            "dajin_length_measured_mm": round(DAJIN_MEASURED, 3),
            "dajin_length_drafted_mm": round(DAJIN_LEN, 3),
            "dajin_chord_mm": round(DAJIN_CHORD, 3),
            "chord_shortfall_mm": round(CHORD_SHORTFALL, 3),
            "front_neck_quarter_mm": round(FRONT_NECK, 3),
            "back_neck_quarter_mm": round(BACK_NECK, 3),
            "dajin_neck_measured_mm": round(DAJIN_NECK, 3),
            "collar_run_mm": round(COLLAR_RUN, 3),
            "collar_naive_estimate_mm": round(COLLAR_NAIVE, 3),
            "collar_vs_neck_estimate_mm": round(COLLAR_RUN - COLLAR_NAIVE, 3),
            "closure_spacing_arc_mm": round(DAJIN_MEASURED / closure_count, 3),
            "note": "unlike the men's changpao, the qipao is FITTED: the waist is solved "
                    "from the three girths and suppressed with a side take-in plus a vertical "
                    "dart. The 大襟 (dàjīn) curve is still the seam that must solve — drafted "
                    "once, MEASURED, and the panel's seat is the same curve. The 立領 stand "
                    "collar is cut to the MEASURED neckline (left front + both backs + the "
                    "dajin's own neck run), not to neck_girth + ease. Hook-and-eye closures "
                    "are spaced along the measured curve.",
        },
        "heritage": {
            "garment": "旗袍 qípáo / 長衫 cheongsam — the fitted Chinese women's dress",
            "construction": "fitted sheath with bust/waist shaping, 立領 stand collar, 大襟 "
                            "curved right-over-left overlap, high side slits",
            "closure": "hook-and-eye and knotted 盤扣 frogs along the dajin curve",
            "excluded": "no dragon roundel, embroidery motif or clan mark is drafted — those "
                        "are the maker's cloth and choice",
        },
        "hardware": "hook-and-eye along the dajin: Yantra4D hook-and-eye, linked, sized from "
                    "the closure span and spaced along the measured curve.",
    }
    return pattern


result = build()

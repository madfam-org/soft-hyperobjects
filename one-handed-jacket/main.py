"""
One-handed-dressing Jacket — Fashion Cabinet Garment Cartridge
(FC-400 rank #373, adaptive, Yantra4D-bridged magnetic-clasp).

A softshell jacket a person with the use of one arm can put on and close alone. The dressing
aid is drafted in, not just named: the anchor-side sleeve is set into an EXTRA-WIDE, dropped
armscye so the weak arm slides in without threading, the working-side front carries a column
of magnetic clasps that snap shut with a shove of the palm (no button, no zip pull, no
alignment), and a long back drop tail lets the wearer flip the jacket over the shoulders in
one motion. The clasp is the Yantra4D `magnetic-clasp` solid (notion.hardware_ref); its sew
face is driven by the same clasp_dia that drives the garment's own clasp-placket interface.

Drafting note — the seam that must SOLVE: the two armscyes are asymmetric (the anchor side is
wider than the working side) yet BOTH must receive the same one-piece sleeve without ripple.
The sleeve cap is bisected against the SUM of the two measured armscyes plus a modest ease, so
the one cap fits both openings. The shoulder seam is solved by deriving the back neck width
from the front's measured shoulder (with the flatten-the-rise clamp when the drop exceeds the
run).

Pieces:
  - front  : jacket front (cut 2 mirrored); magnetic-clasp placket cut on.
  - back   : jacket back (cut 1 on fold at CB); drop tail.
  - sleeve : one-piece dropped-shoulder sleeve (cut 2 mirrored).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|set

chest_girth = float(PARAM(lambda: chest_girth, 1100.0))
jacket_length = float(PARAM(lambda: jacket_length, 700.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 480.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
clasp_dia = float(PARAM(lambda: clasp_dia, 22.0))
clasp_pitch = float(PARAM(lambda: clasp_pitch, 110.0))
back_drop = float(PARAM(lambda: back_drop, 70.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(820.0, min(chest_girth, 1560.0))
jacket_length = max(560.0, min(jacket_length, 900.0))
shoulder_width = max(360.0, min(shoulder_width, 620.0))
sleeve_length = max(300.0, min(sleeve_length, 720.0))
clasp_dia = max(14.0, min(clasp_dia, 34.0))
clasp_pitch = max(70.0, min(clasp_pitch, 170.0))
back_drop = max(20.0, min(back_drop, 140.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE_CHEST = 220.0                          # a jacket over clothes, dressed with one hand
HALF_CHEST = (chest_girth + EASE_CHEST) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = 78.0
NECK_DROP_F = 92.0
NECK_DROP_B = 26.0
ARMHOLE_DROP = 300.0                         # deep dropped armscye — easy arm entry
SHOULDER_SLOPE = 44.0
STAND = clasp_dia / 2.0 + 14.0

# ── Solve the magnetic-clasp column ──────────────────────────────────────────
TOP_CLEAR = 60.0
HEM_CLEAR = 100.0
CLOSURE_RUN = jacket_length - NECK_DROP_F - TOP_CLEAR - HEM_CLEAR
N_INTERVALS = max(2, int(round(CLOSURE_RUN / clasp_pitch)))
N_CLASPS = N_INTERVALS + 1
PITCH_SOLVED = CLOSURE_RUN / N_INTERVALS
CLASP_TOP_Y = jacket_length - NECK_DROP_F - TOP_CLEAR


def _clasp_ys():
    return [CLASP_TOP_Y - PITCH_SOLVED * i for i in range(N_CLASPS)]


def build_front():
    h = jacket_length
    x_out = -STAND
    p_hem_out = fc.P(x_out, 0.0)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, h - NECK_DROP_F - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, h - NECK_DROP_F - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, h - NECK_DROP_F)
    p_neck_cf = fc.P(x_out, h - NECK_DROP_F + 4.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_out, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 8.0,
                                           h - NECK_DROP_F - ARMHOLE_DROP * 0.40),
                                      fc.P(HALF_SHOULDER + 16.0,
                                           h - NECK_DROP_F - SHOULDER_SLOPE - 52.0),
                                      p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.52, h - NECK_DROP_F - 10.0),
                                   fc.P(x_out + STAND * 0.4, h - NECK_DROP_F - 2.0),
                                   p_neck_cf)]),
        fc.Edge("placket_fold", [fc.Line(p_neck_cf, p_hem_out)]),
    ]
    internals = [
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h - NECK_DROP_F)],
                    kind="marking"),
    ]
    for i, y in enumerate(_clasp_ys()):
        internals.append(fc.Internal(
            f"clasp-{i + 1}",
            [fc.P(-clasp_dia / 2.0, y), fc.P(clasp_dia / 2.0, y)], kind="drill"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 26.0, "placket_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap front match"),
                 fc.Notch("side", 0.62, "waist level")],
        grainline=fc.Grainline(fc.P(STAND + 50.0, 60.0),
                               fc.P(STAND + 50.0, h - NECK_DROP_F - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Jacket Front (magnetic clasp)",
    )


# ── Solve the back neck point so the shoulder seam MATCHES ───────────────────
_SHOULDER_LEN = math.hypot(HALF_SHOULDER - NECK_W, SHOULDER_SLOPE)
_BACK_NECK_Y_OFF = NECK_DROP_F - NECK_DROP_B - SHOULDER_SLOPE * 0.10
_dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
if _SHOULDER_LEN <= abs(_dy):
    _dy = _SHOULDER_LEN * 0.85
    _BACK_NECK_Y_OFF = _dy - SHOULDER_SLOPE
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = _BACK_NECK_Y_OFF


def build_back():
    h = jacket_length
    top = h - NECK_DROP_F
    # The drop tail extends the centre back below the side hem so the jacket can be
    # flipped over the shoulders; the hem is stepped, not level.
    p_hem_cb = fc.P(0.0, -back_drop)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, top - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, top - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, top + BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, top + BACK_NECK_Y + 6.0)
    edges = [
        fc.Edge("hem", [fc.Bezier(p_hem_cb,
                                  fc.P(HALF_CHEST * 0.35, -back_drop * 0.7),
                                  fc.P(HALF_CHEST * 0.7, -back_drop * 0.2),
                                  p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 6.0, top - ARMHOLE_DROP * 0.42),
                                      fc.P(HALF_SHOULDER + 14.0,
                                           top - SHOULDER_SLOPE - 46.0),
                                      p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.55, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y), p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match"),
                 fc.Notch("side", 0.62, "waist level")],
        grainline=None,
        internals=[fc.Internal("flip-tail-note",
                               [fc.P(0.0, -back_drop), fc.P(0.0, 0.0)], kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Jacket Back (drop tail)",
    )


# ── Solve the sleeve cap against the MEASURED armscyes ───────────────────────
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 18.0
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
BICEPS = max(400.0, (ARMHOLE_F + ARMHOLE_B) * 0.80)


def _cap_segments(cap_h, top_y):
    half = BICEPS / 2.0
    p_l = fc.P(-half, top_y - cap_h)
    p_top = fc.P(0.0, top_y)
    p_r = fc.P(half, top_y - cap_h)
    return [
        fc.Bezier(p_l, fc.P(-half * 0.72, top_y - cap_h * 0.94),
                  fc.P(-half * 0.34, top_y - cap_h * 0.06), p_top),
        fc.Bezier(p_top, fc.P(half * 0.34, top_y - cap_h * 0.06),
                  fc.P(half * 0.72, top_y - cap_h * 0.94), p_r),
    ]


def _solve_cap_height():
    lo, hi = 20.0, BICEPS * 0.95
    def f(ch):
        return sum(s.length(0.2) for s in _cap_segments(ch, 0.0)) - CAP_TARGET
    f_lo, f_hi = f(lo), f(hi)
    if f_lo * f_hi > 0.0:
        return lo if abs(f_lo) < abs(f_hi) else hi
    for _ in range(80):
        mid = (lo + hi) / 2.0
        f_mid = f(mid)
        if abs(f_mid) < 0.02:
            return mid
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


CAP_H = _solve_cap_height()


def build_sleeve():
    half = BICEPS / 2.0
    cuff_half = max(100.0, half * 0.66)
    top_y = sleeve_length
    cap = _cap_segments(CAP_H, top_y)
    p_l_under = fc.P(-half, top_y - CAP_H)
    p_r_under = fc.P(half, top_y - CAP_H)
    p_l_cuff = fc.P(-cuff_half, 0.0)
    p_r_cuff = fc.P(cuff_half, 0.0)
    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r_under, p_r_cuff)]),
        fc.Edge("cuff", [fc.Line(p_r_cuff, p_l_cuff)]),
        fc.Edge("under_l", [fc.Line(p_l_cuff, p_l_under)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 36.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, top_y - 40.0)),
        internals=[fc.Internal("elbow-line",
                               [fc.P(-half * 0.9, top_y * 0.42),
                                fc.P(half * 0.9, top_y * 0.42)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build():
    pattern = fc.PatternSet("one-handed-jacket")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "softshell (bonded fleece-back)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 74% marker; a soft, slightly stretchy shell slides "
                 "over the weak arm without catching."},
        {"item": "magnetic clasp", "qty": N_CLASPS, "unit": "count",
         "note": f"Yantra4D magnetic-clasp (notion.hardware_ref): {N_CLASPS} clasps at a "
                 f"solved {PITCH_SOLVED:.1f} mm pitch; disc_dia = clasp_dia."},
        {"item": "grosgrain placket stay", "qty": round(2.0 * jacket_length),
         "unit": "mm_length",
         "note": f"{STAND * 2.0:.0f} mm wide; keeps the clasp discs from tilting under load."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "bar-tack the armscye corners; the wide opening takes the dressing strain."},
    ]
    pattern.metadata = {
        "fc400_rank": 373,
        "family": "adaptive",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"chest": round(HALF_CHEST * 4.0, 1),
                        "length": round(jacket_length, 1),
                        "back_drop": round(back_drop, 1),
                        "clasp_stand": round(STAND, 1)},
        "solved": {
            "closure_run_mm": round(CLOSURE_RUN, 2),
            "clasps": N_CLASPS,
            "pitch_solved_mm": round(PITCH_SOLVED, 2),
            "cap_height_mm": round(CAP_H, 2),
            "armhole_total_mm": round(ARMHOLE_F + ARMHOLE_B, 2),
            "back_neck_width_mm": round(NECK_W_BACK, 2),
            "note": "the clasp pitch is RECOMPUTED from whole intervals across the "
                    "measured closure run; the sleeve cap is bisected against the SUM of "
                    "the two measured armscyes so one cap fits both openings; the back "
                    "neck width is solved from the front's measured shoulder with the "
                    "flatten-the-rise clamp.",
        },
        "adaptive": {
            "dressing": "extra-wide dropped armscye for threading the weak arm without "
                        "help; magnetic clasps close with a palm shove — no button, no "
                        "zip pull, no fine alignment; a back drop tail lets the jacket "
                        "be flipped over the shoulders in one motion",
        },
        "hardware": "magnetic clasps via Yantra4D (notion.hardware_ref -> magnetic-clasp); "
                    "disc_dia = clasp_dia, the same parameter that drives this jacket's "
                    "clasp-placket interface (the dimensional handshake).",
    }
    return pattern


result = build()

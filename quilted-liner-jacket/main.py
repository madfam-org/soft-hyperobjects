"""
Quilted Button-in Liner Jacket — Fashion Cabinet Garment Cartridge
(FC-400 rank #377, outerwear, Yantra4D-bridged sew-through-button).

The warm layer that lives inside a three-in-one coat: a light quilted jacket with its own
front buttons, plus a row of loops around the neck and front edge that button INTO a host shell
so the two travel as one in winter and separate in spring. The front buttons and the button-in
loops both use the Yantra4D `sew-through-button` solid (notion.hardware_ref); its sew face is
driven by the same button_ligne the liner's placket carries.

Drafting note — the seam that must SOLVE: the button-in loops must land at the SAME pitch as
the host shell's buttons, or the liner hangs crooked inside the coat. The loop pitch is solved
from the measured button run and the requested count, recomputed so the row lands exactly on
both end clearances (the land-exactly discipline), and the quilting channel count is derived so
the channels divide the body evenly rather than leaving a runt channel at one edge.

Pieces:
  - front  : liner front (cut 2 mirrored); own-button placket + button-in loops.
  - back   : liner back (cut 1 on fold).
  - sleeve : one-piece quilted sleeve (cut 2 mirrored).

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

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
liner_length = float(PARAM(lambda: liner_length, 680.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
button_ligne = float(PARAM(lambda: button_ligne, 24.0))   # button size (ligne)
button_count = float(PARAM(lambda: button_count, 6.0))    # own-front buttons
quilt_channel = float(PARAM(lambda: quilt_channel, 70.0)) # target quilting channel width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(780.0, min(chest_girth, 1500.0))
liner_length = max(540.0, min(liner_length, 860.0))
shoulder_width = max(360.0, min(shoulder_width, 600.0))
sleeve_length = max(300.0, min(sleeve_length, 720.0))
button_ligne = max(14.0, min(button_ligne, 40.0))
button_count = max(3.0, min(round(button_count), 10))
quilt_channel = max(40.0, min(quilt_channel, 140.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE = 140.0
HALF_CHEST = (chest_girth + EASE) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = 76.0
NECK_DROP_F = 96.0
NECK_DROP_B = 24.0
ARMHOLE_DROP = 270.0
SHOULDER_SLOPE = 42.0
BUTTON_MM = button_ligne * 0.635              # ligne -> mm
STAND = BUTTON_MM / 2.0 + 14.0

# ── Solve the own-button column ──────────────────────────────────────────────
N_BTN = int(button_count)
TOP_CLEAR = 60.0
HEM_CLEAR = 80.0
BTN_RUN = liner_length - NECK_DROP_F - TOP_CLEAR - HEM_CLEAR
N_BTN_INT = max(1, N_BTN - 1)
BTN_PITCH = BTN_RUN / N_BTN_INT
BTN_TOP_Y = liner_length - NECK_DROP_F - TOP_CLEAR


def _button_ys():
    return [BTN_TOP_Y - BTN_PITCH * i for i in range(N_BTN)]


# ── Solve the quilting channel count so channels divide the body evenly ──────
def _channel_count(height):
    n = max(2, int(round(height / quilt_channel)))
    return n, height / n


def build_front():
    h = liner_length
    x_out = -STAND
    p_hem_out = fc.P(x_out, 0.0)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, h - NECK_DROP_F - ARMHOLE_DROP)
    p_shoulder = fc.P(HALF_SHOULDER, h - NECK_DROP_F - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, h - NECK_DROP_F)
    p_neck_cf = fc.P(x_out, h - NECK_DROP_F + 2.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_out, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 6.0,
                                           h - NECK_DROP_F - ARMHOLE_DROP * 0.42),
                                      fc.P(HALF_SHOULDER + 12.0,
                                           h - NECK_DROP_F - SHOULDER_SLOPE - 44.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.5, h - NECK_DROP_F - 8.0),
                                   fc.P(x_out + STAND * 0.4, h - NECK_DROP_F), p_neck_cf)]),
        fc.Edge("placket_fold", [fc.Line(p_neck_cf, p_hem_out)]),
    ]
    internals = [fc.Internal("centre-front",
                             [fc.P(0.0, 0.0), fc.P(0.0, h - NECK_DROP_F)], kind="marking")]
    # Own-front buttons.
    for i, y in enumerate(_button_ys()):
        internals.append(fc.Internal(f"button-{i + 1}",
                                     [fc.P(-BUTTON_MM / 2.0, y), fc.P(BUTTON_MM / 2.0, y)],
                                     kind="drill"))
    # Button-in loops around the neck and front edge, at the SAME pitch as the buttons.
    for i, y in enumerate(_button_ys()):
        internals.append(fc.Internal(f"buttonin-loop-{i + 1}",
                                     [fc.P(HALF_CHEST - 20.0, y), fc.P(HALF_CHEST, y)],
                                     kind="marking"))
    # Quilting channels dividing the body height evenly.
    n_ch, ch_h = _channel_count(h - NECK_DROP_F)
    for i in range(1, n_ch):
        yy = ch_h * i
        internals.append(fc.Internal(f"quilt-{i}",
                                     [fc.P(x_out, yy), fc.P(HALF_CHEST, yy)], kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"placket_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap front match")],
        grainline=fc.Grainline(fc.P(STAND + 40.0, 60.0),
                               fc.P(STAND + 40.0, h - NECK_DROP_F - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Liner Front",
    )


# ── Back neck width solved from the front's measured shoulder ────────────────
_SHOULDER_LEN = math.hypot(HALF_SHOULDER - NECK_W, SHOULDER_SLOPE)
_dy = SHOULDER_SLOPE + (NECK_DROP_F - NECK_DROP_B) - SHOULDER_SLOPE * 0.10
if _SHOULDER_LEN <= abs(_dy):
    _dy = _SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = _dy - SHOULDER_SLOPE


def build_back():
    h = liner_length
    top = h - NECK_DROP_F
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, top - ARMHOLE_DROP)
    p_shoulder = fc.P(HALF_SHOULDER, top - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, top + BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, top + BACK_NECK_Y + 6.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 6.0, top - ARMHOLE_DROP * 0.42),
                                      fc.P(HALF_SHOULDER + 12.0,
                                           top - SHOULDER_SLOPE - 40.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.55, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y), p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    n_ch, ch_h = _channel_count(top)
    internals = [fc.Internal(f"quilt-{i}", [fc.P(0.0, ch_h * i), fc.P(HALF_CHEST, ch_h * i)],
                             kind="marking") for i in range(1, n_ch)]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match")],
        grainline=None,
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Liner Back",
    )


# ── Sleeve cap solved against MEASURED armholes ──────────────────────────────
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 14.0
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
BICEPS = max(380.0, (ARMHOLE_F + ARMHOLE_B) * 0.80)


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


def _solve_cap():
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


CAP_H = _solve_cap()


def build_sleeve():
    half = BICEPS / 2.0
    cuff_half = max(95.0, half * 0.64)
    top_y = max(sleeve_length, CAP_H + 60.0)
    cap = _cap_segments(CAP_H, top_y)
    p_l = fc.P(-half, top_y - CAP_H)
    p_r = fc.P(half, top_y - CAP_H)
    n_ch, ch_h = _channel_count(top_y)
    internals = [fc.Internal(f"quilt-{i}",
                             [fc.P(-half, ch_h * i), fc.P(half, ch_h * i)], kind="marking")
                 for i in range(1, n_ch)]
    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r, fc.P(cuff_half, 0.0))]),
        fc.Edge("cuff", [fc.Line(fc.P(cuff_half, 0.0), fc.P(-cuff_half, 0.0))]),
        fc.Edge("under_l", [fc.Line(fc.P(-cuff_half, 0.0), p_l)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 26.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, top_y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build():
    pattern = fc.PatternSet("quilted-liner-jacket")
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

    n_ch, _ = _channel_count(liner_length - NECK_DROP_F)
    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "quilted nylon (down-proof)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1450 mm width, 74% marker; pre-quilted saves the channel-sewing "
                 "step — the marked channels match a bought quilt's grid."},
        {"item": "sew-through button (own front)", "qty": N_BTN, "unit": "count",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref): {button_ligne:.0f} ligne, "
                 f"at a {BTN_PITCH:.1f} mm solved pitch."},
        {"item": "sew-through button (button-in)", "qty": N_BTN, "unit": "count",
         "note": "matching buttons on the button-in loops so the liner mates to the host shell."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "bar-tack each button-in loop; they carry the liner's weight inside the coat."},
    ]
    pattern.metadata = {
        "fc400_rank": 377,
        "family": "outerwear",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"chest": round(HALF_CHEST * 4.0, 1),
                        "length": round(liner_length, 1),
                        "button_mm": round(BUTTON_MM, 1)},
        "solved": {
            "own_buttons": N_BTN,
            "button_pitch_mm": round(BTN_PITCH, 2),
            "quilt_channels": n_ch,
            "cap_height_mm": round(CAP_H, 2),
            "note": "the button-in loops land at the SAME solved pitch as the own-front "
                    "buttons so the liner hangs straight inside the host shell; the "
                    "quilting channel count divides the body evenly rather than leaving a "
                    "runt channel; the sleeve cap is bisected against the measured armholes.",
        },
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); button_ligne = button_ligne, the same parameter "
                    "that drives this liner's button-placket interface (dimensional handshake).",
    }
    return pattern


result = build()

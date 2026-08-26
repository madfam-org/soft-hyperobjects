"""
Toggle Duffle Coat — Fashion Cabinet Garment Cartridge
(FC-400 rank #380, outerwear, Yantra4D-bridged toggle).

The classic duffle: a straight wool-melton coat closed by the signature horn-toggle-and-rope
fastenings across the front, with a deep buttoned HOOD, patch POCKETS, and set SLEEVES. Unlike
the sleeveless A-line cape (rank #378), this is a proper sleeved coat — the toggles are the
face of it. The toggle is the Yantra4D `toggle` solid (notion.hardware_ref); its barrel length
is driven by the same toggle_len the coat's rope loops are cut for.

Drafting note — the seam that must SOLVE: the toggle-and-rope closures sit on a BUTTON STAND
that extends past centre front, mirror-equal on both fronts so the toggles meet their loops
when closed — and the toggle row must divide the closure run into whole intervals with the top
toggle clear of the collar seam and the bottom clear of the hem. The pitch is SOLVED and
recomputed so the row lands exactly (the land-exactly discipline). The hood is cut to the
measured neckline, and the sleeve cap bisected against the measured armholes.

Pieces:
  - front  : coat front (cut 2 mirrored); toggle stand, patch-pocket line marked.
  - back   : coat back (cut 1 on fold); back yoke marked.
  - sleeve : two-piece look one-piece sleeve (cut 2 mirrored).
  - hood   : deep hood half (cut 2 mirrored).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|hood|set

chest_girth = float(PARAM(lambda: chest_girth, 1060.0))
coat_length = float(PARAM(lambda: coat_length, 860.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 480.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 650.0))
neck_girth = float(PARAM(lambda: neck_girth, 430.0))
toggle_len = float(PARAM(lambda: toggle_len, 70.0))
toggle_count = float(PARAM(lambda: toggle_count, 4.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(840.0, min(chest_girth, 1560.0))
coat_length = max(680.0, min(coat_length, 1100.0))
shoulder_width = max(380.0, min(shoulder_width, 620.0))
sleeve_length = max(360.0, min(sleeve_length, 720.0))
neck_girth = max(340.0, min(neck_girth, 560.0))
toggle_len = max(40.0, min(toggle_len, 100.0))
toggle_count = max(3.0, min(round(toggle_count), 6))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

EASE = 260.0                                 # a coat over a jacket
HALF_CHEST = (chest_girth + EASE) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = neck_girth / 6.0 + 12.0
NECK_DROP_F = neck_girth / 6.0 + 22.0
NECK_DROP_B = 26.0
ARMHOLE_DROP = 300.0
SHOULDER_SLOPE = 46.0
# The toggle stand extends past centre front, mirror-equal both fronts.
STAND = max(30.0, toggle_len * 0.5)

# ── Solve the toggle column ──────────────────────────────────────────────────
N_TOG = int(toggle_count)
TOP_CLEAR = 80.0
HEM_CLEAR = 140.0
TOG_RUN = coat_length - NECK_DROP_F - TOP_CLEAR - HEM_CLEAR
N_TOG_INT = max(1, N_TOG - 1)
TOG_PITCH = TOG_RUN / N_TOG_INT
TOG_TOP_Y = coat_length - NECK_DROP_F - TOP_CLEAR


def _toggle_ys():
    return [TOG_TOP_Y - TOG_PITCH * i for i in range(N_TOG)]


def build_front():
    h = coat_length
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
                                      fc.P(HALF_CHEST - 8.0,
                                           h - NECK_DROP_F - ARMHOLE_DROP * 0.42),
                                      fc.P(HALF_SHOULDER + 14.0,
                                           h - NECK_DROP_F - SHOULDER_SLOPE - 48.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.5, h - NECK_DROP_F - 8.0),
                                   fc.P(x_out + STAND * 0.4, h - NECK_DROP_F), p_neck_cf)]),
        fc.Edge("stand_fold", [fc.Line(p_neck_cf, p_hem_out)]),
    ]
    internals = [fc.Internal("centre-front",
                             [fc.P(0.0, 0.0), fc.P(0.0, h - NECK_DROP_F)], kind="marking")]
    for i, y in enumerate(_toggle_ys()):
        internals.append(fc.Internal(f"toggle-{i + 1}",
                                     [fc.P(0.0, y), fc.P(toggle_len, y)], kind="marking"))
    # Patch pocket, sized from the front width.
    pk_w = max(160.0, HALF_CHEST * 0.6)
    pk_h = max(160.0, coat_length * 0.22)
    pk_x = STAND + 40.0
    pk_y = h - NECK_DROP_F - ARMHOLE_DROP - 60.0
    pk_y = max(pk_y, HEM_CLEAR)
    internals.append(fc.Internal("patch-pocket",
                                 [fc.P(pk_x, pk_y), fc.P(pk_x + pk_w, pk_y),
                                  fc.P(pk_x + pk_w, pk_y + pk_h), fc.P(pk_x, pk_y + pk_h),
                                  fc.P(pk_x, pk_y)], kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0, "stand_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap front match")],
        grainline=fc.Grainline(fc.P(STAND + 50.0, 60.0),
                               fc.P(STAND + 50.0, h - NECK_DROP_F - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Duffle Front",
    )


# ── Back neck width solved from front's measured shoulder ────────────────────
_SHOULDER_LEN = math.hypot(HALF_SHOULDER - NECK_W, SHOULDER_SLOPE)
_dy = SHOULDER_SLOPE + (NECK_DROP_F - NECK_DROP_B) - SHOULDER_SLOPE * 0.10
if _SHOULDER_LEN <= abs(_dy):
    _dy = _SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = _dy - SHOULDER_SLOPE


def build_back():
    h = coat_length
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
                                           top - SHOULDER_SLOPE - 44.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.55, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y), p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0, "cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match")],
        grainline=None,
        internals=[fc.Internal("yoke-line",
                               [fc.P(0.0, top - 140.0), fc.P(HALF_SHOULDER, top - 140.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Duffle Back",
    )


# ── Sleeve cap solved against MEASURED armholes ──────────────────────────────
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 20.0
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
    cuff_half = max(105.0, half * 0.66)
    top_y = max(sleeve_length, CAP_H + 60.0)
    cap = _cap_segments(CAP_H, top_y)
    p_l = fc.P(-half, top_y - CAP_H)
    p_r = fc.P(half, top_y - CAP_H)
    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r, fc.P(cuff_half, 0.0))]),
        fc.Edge("cuff", [fc.Line(fc.P(cuff_half, 0.0), fc.P(-cuff_half, 0.0))]),
        fc.Edge("under_l", [fc.Line(fc.P(-cuff_half, 0.0), p_l)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 40.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, top_y - 30.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


# ── Deep hood, neck edge = MEASURED half neckline ────────────────────────────
_NECK_HALF_RUN = _F.edge("neck").length(0.2) + _B.edge("neck").length(0.2)


def build_hood():
    neck_run = _NECK_HALF_RUN
    hood_h = max(340.0, neck_run * 1.55)       # a duffle hood is deep
    hood_w = max(260.0, neck_run * 1.1)
    p_neck_front = fc.P(0.0, 0.0)
    p_neck_back = fc.P(neck_run, 0.0)
    p_crown = fc.P(neck_run + 24.0, hood_h)
    p_face_top = fc.P(-hood_w * 0.18, hood_h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p_neck_front, p_neck_back)]),
        fc.Edge("centre_back", [fc.Bezier(p_neck_back,
                                          fc.P(neck_run + hood_w * 0.32, hood_h * 0.5),
                                          fc.P(neck_run + hood_w * 0.12, hood_h * 0.9),
                                          p_crown)]),
        fc.Edge("crown", [fc.Line(p_crown, p_face_top)]),
        fc.Edge("face", [fc.Bezier(p_face_top,
                                   fc.P(-hood_w * 0.22, hood_h * 0.55),
                                   fc.P(-hood_w * 0.06, hood_h * 0.2), p_neck_front)]),
    ]
    return fc.Piece(
        "hood", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(neck_run * 0.5, 20.0), fc.P(neck_run * 0.5, hood_h - 20.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Deep hood half",
    )


def build():
    pattern = fc.PatternSet("duffle-coat")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "hood":
        pattern.add(build_hood())

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)
        pattern.declare_seam(("hood", "centre_back"), ("hood", "centre_back"), tol=1.0)
        pattern.declare_seam([("hood", "neck_edge"), ("hood", "neck_edge")],
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "wool melton (heavy)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker; a heavy melton is the duffle's whole "
                 "point — it does not fray, so seams can be raw-bound."},
        {"item": "horn or wood toggle", "qty": N_TOG, "unit": "count",
         "note": f"Yantra4D toggle (notion.hardware_ref): {N_TOG} at a {TOG_PITCH:.1f} mm "
                 f"solved pitch; barrel_len = toggle_len ({toggle_len:.0f} mm)."},
        {"item": "leather rope loops", "qty": N_TOG * 2, "unit": "count",
         "note": "each toggle rides a rope loop on one side and passes through a loop on the "
                 "other; cut to the same toggle_len."},
        {"item": "check-flannel lining", "qty": round(marker_len * 0.9), "unit": "mm_length",
         "note": "the traditional tartan body lining; not structural but expected."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "bar-tack the toggle loops; they take the full closing strain."},
    ]
    pattern.metadata = {
        "fc400_rank": 380,
        "family": "outerwear",
        "fabric_hint": "lana-melton-abrigo",
        "finished_mm": {"chest": round(HALF_CHEST * 4.0, 1),
                        "length": round(coat_length, 1),
                        "toggle_stand": round(STAND, 1)},
        "solved": {
            "toggles": N_TOG,
            "toggle_pitch_mm": round(TOG_PITCH, 2),
            "cap_height_mm": round(CAP_H, 2),
            "neck_half_run_mm": round(_NECK_HALF_RUN, 2),
            "back_neck_width_mm": round(NECK_W_BACK, 2),
            "note": "the toggle stand extends past centre front, mirror-equal on both "
                    "fronts so the toggles meet their loops when closed; the toggle pitch "
                    "is RECOMPUTED so the row lands exactly on both end clearances; the "
                    "deep hood is cut to the measured neckline; the sleeve cap is bisected "
                    "against the measured armholes; the back neck is solved with the "
                    "flatten clamp.",
        },
        "hardware": "horn toggle-and-rope closure via Yantra4D (notion.hardware_ref -> "
                    "toggle); barrel_len = toggle_len, the same parameter that drives this "
                    "coat's toggle-placket interface (the dimensional handshake).",
    }
    return pattern


result = build()

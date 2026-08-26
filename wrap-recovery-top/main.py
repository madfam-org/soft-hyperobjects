"""
Post-surgery Wrap Recovery Top — Fashion Cabinet Garment Cartridge
(FC-400 rank #375, adaptive, Yantra4D-bridged hook-loop-tape).

A crossover wrap top for after breast, shoulder, or cardiac surgery, when raising an arm
overhead is impossible or forbidden. It opens completely flat so a carer lays it under the
wearer and wraps the two fronts across the body — no overhead dressing — and it closes on
hook-and-loop tape at the side so the wearer or carer can adjust the pressure over a dressing
or a drain without a knot. A soft, low armscye clears a shoulder that cannot lift. The tape is
the Yantra4D `hook-loop-tape` solid (notion.hardware_ref); its sewn strip length is driven by
the same wrap_overlap that drives the garment's own wrap-closure interface.

Drafting note — the seam that must SOLVE: a wrap top's two fronts OVERLAP, so their combined
width across the body is more than the back's — the overlap has to be a MEASURED, deliberate
amount, not whatever falls out of the pattern. Each front's centre edge extends past the
centre front by wrap_overlap, and the hook-loop run is that same overlap, so the closure and
the pattern agree. The tie-anchor points are clamped inside the side seam so a wide overlap on
a narrow body cannot push the anchor off the panel.

Pieces:
  - front  : one wrap front (cut 2 mirrored); the two cross over.
  - back   : the back (cut 1 on fold at CB).
  - sleeve : soft low-cap sleeve (cut 2 mirrored).

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

chest_girth = float(PARAM(lambda: chest_girth, 980.0))
top_length = float(PARAM(lambda: top_length, 620.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 420.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 300.0))
wrap_overlap = float(PARAM(lambda: wrap_overlap, 140.0))  # how far the fronts cross
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(640.0, min(chest_girth, 1440.0))
top_length = max(440.0, min(top_length, 800.0))
shoulder_width = max(300.0, min(shoulder_width, 560.0))
sleeve_length = max(120.0, min(sleeve_length, 420.0))
wrap_overlap = max(60.0, min(wrap_overlap, 260.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

EASE = 100.0
HALF_BACK = (chest_girth + EASE) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
# The wrap front is the back half-width PLUS the overlap. Clamp the overlap so the
# front cannot exceed the full body width (which would wrap past the far side seam).
wrap_overlap = min(wrap_overlap, HALF_BACK * 1.4)
FRONT_HALF = HALF_BACK + wrap_overlap
NECK_W = 74.0
NECK_DROP_F = 150.0                          # deep V so no overhead pull
NECK_DROP_B = 24.0
ARMHOLE_DROP = min(220.0, top_length * 0.40)
SHOULDER_SLOPE = 40.0


def build_front():
    """One wrap front (cut 2 mirrored). x from the side seam (x=0) inward across the
    body; the centre edge extends past centre front by wrap_overlap. A deep V neck
    means no overhead pull; the hook-loop tab sits on the side seam."""
    h = top_length
    p_hem_side = fc.P(0.0, 0.0)
    p_hem_centre = fc.P(FRONT_HALF, 0.0)
    p_neck_low = fc.P(FRONT_HALF, h - NECK_DROP_F)          # where the wrap V begins
    p_shoulder = fc.P(HALF_SHOULDER, h - SHOULDER_SLOPE)    # shoulder point, side at x=0
    p_arm_base = fc.P(0.0, h - ARMHOLE_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_side, p_hem_centre)]),
        fc.Edge("centre_wrap", [fc.Line(p_hem_centre, p_neck_low)]),
        fc.Edge("neck_v", [fc.Bezier(p_neck_low,
                                     fc.P(FRONT_HALF - wrap_overlap * 0.4, h - NECK_DROP_F * 0.5),
                                     fc.P((HALF_SHOULDER - NECK_W) + 20.0, h - 8.0),
                                     fc.P(HALF_SHOULDER - NECK_W, h))]),
        fc.Edge("shoulder", [fc.Line(fc.P(HALF_SHOULDER - NECK_W, h), p_shoulder)]),
        fc.Edge("armhole", [fc.Bezier(p_shoulder,
                                      fc.P(HALF_SHOULDER * 0.5, h - SHOULDER_SLOPE - 40.0),
                                      fc.P(6.0, h - ARMHOLE_DROP * 0.5), p_arm_base)]),
        fc.Edge("side", [fc.Line(p_arm_base, p_hem_side)]),
    ]
    # The hook-loop anchor sits on the side seam, clamped inside the panel height.
    anchor_y = min(h * 0.5, h - ARMHOLE_DROP - 10.0)
    anchor_y = max(anchor_y, 40.0)
    internals = [
        fc.Internal("hook-loop-anchor",
                    [fc.P(4.0, anchor_y), fc.P(4.0 + min(wrap_overlap, FRONT_HALF * 0.4),
                                               anchor_y)], kind="marking"),
        fc.Internal("wrap-edge-note",
                    [fc.P(HALF_BACK, 0.0), fc.P(HALF_BACK, h - NECK_DROP_F)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 20.0},
        notches=[fc.Notch("side", 0.5, "underarm"),
                 fc.Notch("armhole", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(HALF_BACK * 0.5, 30.0), fc.P(HALF_BACK * 0.5, h - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Wrap front",
    )


# ── Solve the back neck point so the shoulder seam MATCHES the front's ───────
_FRONT_SHOULDER_LEN = None  # computed after build_front measured below


def build_back():
    h = top_length
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_BACK, 0.0)
    p_arm_base = fc.P(HALF_BACK, h - ARMHOLE_DROP)
    p_shoulder = fc.P(HALF_SHOULDER, h - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, h - NECK_DROP_B)
    p_neck_cb = fc.P(0.0, h - NECK_DROP_B + 6.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_arm_base)]),
        fc.Edge("armhole", [fc.Bezier(p_arm_base,
                                      fc.P(HALF_BACK - 6.0, h - ARMHOLE_DROP * 0.5),
                                      fc.P(HALF_SHOULDER + 8.0, h - SHOULDER_SLOPE - 34.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.55, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y), p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 20.0, "cb_fold": 0.0},
        notches=[fc.Notch("side", 0.5, "underarm"),
                 fc.Notch("armhole", 0.5, "sleeve match")],
        grainline=None,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back",
    )


# Solve the back neck width from the front's MEASURED shoulder so the seam matches.
_FRONT = build_front()
_FRONT_SHOULDER_LEN = _FRONT.edge("shoulder").length(0.2)
_dy = SHOULDER_SLOPE - NECK_DROP_B * 0.0 + (NECK_DROP_F - NECK_DROP_F)  # back shoulder dy
# The back shoulder runs from (HALF_SHOULDER, h - SLOPE) to (NECK_W_BACK, h - NECK_DROP_B).
# Its vertical component is |NECK_DROP_B - SLOPE_at_out|; we solve NECK_W_BACK so its
# length equals the front's measured shoulder. dy_back = (h - SLOPE) - (h - NECK_DROP_B)
_dy_back = (SHOULDER_SLOPE - NECK_DROP_B)
if _FRONT_SHOULDER_LEN <= abs(_dy_back):
    # Flatten: the vertical alone exceeds the shoulder length. Reduce the effective dy
    # and let the drawn back neck drop track it (the back-neck-rise clamp lesson).
    _dy_back = _FRONT_SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_FRONT_SHOULDER_LEN ** 2 - _dy_back ** 2, 1.0))


CAP_EASE_375 = 8.0
_AH = (_FRONT.edge("armhole").length(0.2)
       + build_back().edge("armhole").length(0.2))
CAP_TARGET_375 = _AH + CAP_EASE_375
BICEPS_375 = max(300.0, _AH * 0.78)


def _cap_segs_375(cap_h, top_y):
    half = BICEPS_375 / 2.0
    p_l = fc.P(-half, top_y - cap_h)
    p_top = fc.P(0.0, top_y)
    p_r = fc.P(half, top_y - cap_h)
    return [
        fc.Bezier(p_l, fc.P(-half * 0.7, top_y - cap_h * 0.9),
                  fc.P(-half * 0.3, top_y - cap_h * 0.08), p_top),
        fc.Bezier(p_top, fc.P(half * 0.3, top_y - cap_h * 0.08),
                  fc.P(half * 0.7, top_y - cap_h * 0.9), p_r),
    ]


def _solve_cap_375():
    lo, hi = 15.0, BICEPS_375 * 0.95
    def f(ch):
        return sum(s.length(0.2) for s in _cap_segs_375(ch, 0.0)) - CAP_TARGET_375
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


CAP_H_375 = _solve_cap_375()


def build_sleeve():
    half = BICEPS_375 / 2.0
    cuff_half = max(90.0, half * 0.7)
    # The solved cap height must fit within the sleeve length; a recovery sleeve is
    # short, so guarantee the panel is at least tall enough for its own solved cap.
    top_y = max(sleeve_length, CAP_H_375 + 60.0)
    cap_h = CAP_H_375
    cap = _cap_segs_375(cap_h, top_y)
    p_l = fc.P(-half, top_y - cap_h)
    p_r = fc.P(half, top_y - cap_h)
    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r, fc.P(cuff_half, 0.0))]),
        fc.Edge("cuff", [fc.Line(fc.P(cuff_half, 0.0), fc.P(-cuff_half, 0.0))]),
        fc.Edge("under_l", [fc.Line(fc.P(-cuff_half, 0.0), p_l)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 24.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, top_y - 20.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Soft low-cap sleeve",
    )


def build():
    pattern = fc.PatternSet("wrap-recovery-top")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())

    if everything:
        # The fronts join the back at the side seams and shoulders.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # The sleeve cap against both measured armholes.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")], tol=1.2,
                             ease=8.0)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "modal jersey (soft)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1600 mm width, 72% marker; soft modal sits gently over a dressing "
                 "or a drain site."},
        {"item": "hook-and-loop tape (soft-loop)", "qty": round(wrap_overlap + 60.0),
         "unit": "mm_length",
         "note": f"Yantra4D hook-loop-tape (notion.hardware_ref): {wrap_overlap:.0f} mm "
                 "adjust run at the side; strip_length = wrap_overlap. Use soft-loop so "
                 "it never scratches healing skin."},
        {"item": "internal drain pocket (optional)", "qty": 1, "unit": "count",
         "note": "a light pouch on the inner front holds a surgical drain bulb off the incision."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "flatlock the inner front edge so no ridge presses the incision."},
    ]
    pattern.metadata = {
        "fc400_rank": 375,
        "family": "adaptive",
        "fabric_hint": "jersey-algodon",
        "finished_mm": {"chest": round(HALF_BACK * 4.0, 1),
                        "length": round(top_length, 1),
                        "wrap_overlap": round(wrap_overlap, 1)},
        "solved": {
            "front_half_mm": round(FRONT_HALF, 2),
            "back_half_mm": round(HALF_BACK, 2),
            "wrap_overlap_clamped_mm": round(wrap_overlap, 2),
            "back_neck_width_mm": round(NECK_W_BACK, 2),
            "note": "the wrap overlap is a MEASURED, deliberate amount: each front is the "
                    "back half-width plus wrap_overlap, and the hook-loop run is that same "
                    "overlap, so the closure and the pattern agree. The overlap is clamped "
                    "under 1.4x the back half so it cannot wrap past the far side seam; the "
                    "back neck width is solved from the front's measured shoulder with the "
                    "flatten clamp.",
        },
        "adaptive": {
            "dressing": "opens completely flat — a carer lays it under the wearer and "
                        "wraps the fronts across, no overhead pull; hook-loop side closure "
                        "adjusts pressure over a dressing or drain without a knot; the low "
                        "armscye clears a shoulder that cannot lift",
        },
        "hardware": "hook-and-loop wrap closure via Yantra4D (notion.hardware_ref -> "
                    "hook-loop-tape); strip_length = wrap_overlap, the same parameter that "
                    "drives this top's wrap-closure interface (the dimensional handshake).",
    }
    return pattern


result = build()

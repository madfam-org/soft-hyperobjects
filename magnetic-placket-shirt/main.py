"""
Magnetic-Placket Shirt — Fashion Cabinet Garment Cartridge (FC-300 #246, adaptive II).

A button-front shirt that never asks a hand to pinch. Real buttons are sewn to the
outside of the placket as decoration; the closure underneath is a column of magnetic
button covers, so the shirt reads as an ordinary dress shirt and closes with a nudge
of a knuckle. The cover SOLID is Yantra4D territory (`magnetic-button-cover`; see the
manifest's notion.hardware_ref) — its snap lip grips a conventional shank button, so
the wearer's own shirts can be converted, not only ones cut from this pattern.

The drafting problem the placket poses: a magnetic pair only holds if the two magnet
CENTRES land on top of each other when the shirt is closed. That means the button
stand and the buttonhole stand must be mirror-equal about the centre front, and the
magnet pitch must divide the closure run into a whole number of intervals with the
first and last magnet clear of the collar seam and the hem. Both are SOLVED here:
`n_magnets` is derived from the measured closure run and the requested pitch, then the
pitch is recomputed so the column lands exactly, rather than accumulating drift.

Pieces:
  - front  : shirt front (cut 2 mirrored), with the placket extension cut on.
  - back   : shirt back (cut 1 on fold at CB), with a shoulder yoke line marked.
  - sleeve : one-piece sleeve (cut 2 mirrored), open-cuff, drop shoulder.
  - collar : a single-piece convertible collar (cut 2 on fold at the stand edge).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
shirt_length = float(PARAM(lambda: shirt_length, 720.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
button_diameter = float(PARAM(lambda: button_diameter, 18.0))
magnet_pitch = float(PARAM(lambda: magnet_pitch, 95.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1500.0))
shirt_length = max(560.0, min(shirt_length, 900.0))
shoulder_width = max(340.0, min(shoulder_width, 580.0))
sleeve_length = max(200.0, min(sleeve_length, 700.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
button_diameter = max(11.0, min(button_diameter, 25.0))
magnet_pitch = max(60.0, min(magnet_pitch, 140.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE_CHEST = 160.0                      # a dressing-friendly shirt is a loose shirt
HALF_CHEST = (chest_girth + EASE_CHEST) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = neck_girth / 6.0 + 8.0         # half front neck width
NECK_DROP_F = neck_girth / 6.0 + 18.0
NECK_DROP_B = 24.0
ARMHOLE_DROP = 250.0                    # deep, dropped armhole — easy to get an arm in
SHOULDER_SLOPE = 42.0

# The placket stand: half the button diameter plus a fixed margin, mirrored either
# side of centre front. Equal stands are what put the magnet centres in register.
STAND = button_diameter / 2.0 + 12.0

# ── Solve the magnet column ──────────────────────────────────────────────────
# The closure runs from below the collar seam to above the hem. Both ends are held
# clear so the first and last magnet never fight a seam.
TOP_CLEAR = 55.0
HEM_CLEAR = 90.0
CLOSURE_RUN = shirt_length - NECK_DROP_F - TOP_CLEAR - HEM_CLEAR
# Whole intervals at (or just under) the requested pitch, then the pitch RECOMPUTED
# so the column lands exactly on both clearances instead of drifting.
N_INTERVALS = max(2, int(round(CLOSURE_RUN / magnet_pitch)))
N_MAGNETS = N_INTERVALS + 1
PITCH_SOLVED = CLOSURE_RUN / N_INTERVALS
MAGNET_TOP_Y = shirt_length - NECK_DROP_F - TOP_CLEAR


def _magnet_ys():
    """y of every magnet centre, top-down along the solved column."""
    return [MAGNET_TOP_Y - PITCH_SOLVED * i for i in range(N_MAGNETS)]


def build_front():
    """Shirt front (cut 2 mirrored) with the placket extension cut on.

    x runs from the placket's outer fold (x = -STAND) out to the side seam. Centre
    front is x = 0, so the stand is symmetric about it by construction: mirror the
    piece for the other front and every magnet centre falls on its partner.
    """
    h = shirt_length
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
        # Dropped armhole: shallow scoop, generous for a seated or assisted dressing.
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 6.0,
                                           h - NECK_DROP_F - ARMHOLE_DROP * 0.42),
                                      fc.P(HALF_SHOULDER + 14.0,
                                           h - NECK_DROP_F - SHOULDER_SLOPE - 46.0),
                                      p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.52, h - NECK_DROP_F - 10.0),
                                   fc.P(x_out + STAND * 0.4, h - NECK_DROP_F - 2.0),
                                   p_neck_cf)]),
        fc.Edge("placket_fold", [fc.Line(p_neck_cf, p_hem_out)]),
    ]

    internals = [
        # Centre front — the line the two magnet columns must meet on.
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h - NECK_DROP_F)],
                    kind="marking"),
        # The placket topstitch line, one stand's width in from the fold.
        fc.Internal("placket-stitch",
                    [fc.P(STAND, 0.0), fc.P(STAND, h - NECK_DROP_F)],
                    kind="marking"),
    ]
    # Every magnet centre, as a drill mark on centre front.
    for i, y in enumerate(_magnet_ys()):
        internals.append(fc.Internal(
            f"magnet-{i + 1}",
            [fc.P(-button_diameter / 2.0, y), fc.P(button_diameter / 2.0, y)],
            kind="drill"))
    # The chest pocket is placed clear of the magnet column so a card or a phone
    # never sits on a magnet.
    pk_x, pk_y, pk_w, pk_h = STAND + 60.0, h - NECK_DROP_F - 290.0, 120.0, 140.0
    internals.append(fc.Internal(
        "chest-pocket",
        [fc.P(pk_x, pk_y), fc.P(pk_x + pk_w, pk_y),
         fc.P(pk_x + pk_w, pk_y + pk_h), fc.P(pk_x, pk_y + pk_h), fc.P(pk_x, pk_y)],
        kind="marking"))

    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 22.0, "placket_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap front match"),
                 fc.Notch("side", 0.62, "waist level")],
        grainline=fc.Grainline(fc.P(STAND + 40.0, 60.0),
                               fc.P(STAND + 40.0, h - NECK_DROP_F - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shirt Front (magnetic placket)",
    )


# ── Solve the back neck point so the shoulder seam MATCHES ───────────────────
# The front's shoulder runs from (HALF_SHOULDER, top - SHOULDER_SLOPE) to
# (NECK_W, top). The back's shoulder shares the outer point but its neck point
# sits higher (a back neck is shallower than a front neck), so a back neck width
# of NECK_W would give a LONGER shoulder. Solve the back neck width from the
# front's measured shoulder length instead — the seam is then equal by
# construction rather than by hoping the two formulas agree.
_SHOULDER_LEN = math.hypot(HALF_SHOULDER - NECK_W, SHOULDER_SLOPE)
_BACK_NECK_Y_OFF = NECK_DROP_F - NECK_DROP_B - SHOULDER_SLOPE * 0.10  # back neck is higher
_dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
if _SHOULDER_LEN <= abs(_dy):
    # Degenerate: the vertical drop alone exceeds the shoulder length. Flatten the
    # back neck rise until a real horizontal run remains.
    _dy = _SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = _BACK_NECK_Y_OFF   # y above the front's neck level


def build_back():
    """Shirt back, cut 1 on fold at centre back. A yoke line is marked, not cut,
    so a maker can split it for a shoulder yoke without a second piece.

    The back neck WIDTH is solved (see NECK_W_BACK) so this shoulder measures
    exactly the front's, despite the back neck sitting higher.
    """
    h = shirt_length
    top = h - NECK_DROP_F
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, top - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, top - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, top + BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, top + BACK_NECK_Y + 6.0)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 4.0,
                                           top - ARMHOLE_DROP * 0.44),
                                      fc.P(HALF_SHOULDER + 12.0,
                                           top - SHOULDER_SLOPE - 40.0),
                                      p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.55, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y),
                                   p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 22.0, "cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match"),
                 fc.Notch("side", 0.62, "waist level")],
        grainline=None,
        internals=[fc.Internal("yoke-line",
                               [fc.P(0.0, top - 120.0),
                                fc.P(HALF_SHOULDER, top - 120.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Shirt Back",
    )


# ── Solve the sleeve cap against the MEASURED armholes ───────────────────────
# The cap is a symmetric curve whose height is bisected until its measured length
# equals the two armholes plus a modest ease. A dropped shoulder takes little
# ease — too much and the cap ripples, which a wearer dressing by feel will catch
# on. Measure both armholes from the built pieces rather than reconstructing them.
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 14.0
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
# Cap width = the flat biceps line; generous, because a dropped-shoulder adaptive
# sleeve is meant to admit an arm that cannot be lifted far.
BICEPS = max(360.0, (ARMHOLE_F + ARMHOLE_B) * 0.78)


def _cap_segments(cap_h, top_y):
    """A symmetric two-Bézier sleeve cap of height cap_h, left underarm to right."""
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
    """Bisect the cap height until the cap measures CAP_TARGET.

    Cap length grows monotonically with cap height at fixed biceps width, so a
    bracket from a nearly flat cap to a tall one always contains the root.
    """
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
    """One-piece sleeve (cut 2 mirrored): solved cap, straight taper, open cuff."""
    half = BICEPS / 2.0
    cuff_half = max(90.0, half * 0.62)
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
        allowances={"cuff": 30.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, top_y - 40.0)),
        internals=[fc.Internal("elbow-line",
                               [fc.P(-half * 0.9, top_y * 0.42),
                                fc.P(half * 0.9, top_y * 0.42)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_collar():
    """Convertible collar, cut 2 on fold at the roll line.

    Its neck edge is drafted to the MEASURED neckline (front neck x2 + back neck x2,
    the back being on fold), so the collar cannot come up short — the usual failure
    when a collar is cut to a neck-girth formula.
    """
    neck_run = 2.0 * _F.edge("neck").length(0.2) + 2.0 * _B.edge("neck").length(0.2)
    half = neck_run / 2.0
    stand_h = 38.0
    point_drop = 16.0
    p_l_neck = fc.P(-half, 0.0)
    p_r_neck = fc.P(half, 0.0)
    p_r_point = fc.P(half + 10.0, stand_h + point_drop)
    p_l_point = fc.P(-half - 10.0, stand_h + point_drop)

    edges = [
        fc.Edge("neck_edge", [fc.Line(p_l_neck, p_r_neck)]),
        fc.Edge("point_r", [fc.Line(p_r_neck, p_r_point)]),
        fc.Edge("outer", [fc.Bezier(p_r_point,
                                    fc.P(half * 0.45, stand_h + point_drop + 6.0),
                                    fc.P(-half * 0.45, stand_h + point_drop + 6.0),
                                    p_l_point)]),
        fc.Edge("point_l", [fc.Line(p_l_point, p_l_neck)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", 0.5, "centre back"),
                 fc.Notch("neck_edge", 0.25, "shoulder match"),
                 fc.Notch("neck_edge", 0.75, "shoulder match")],
        grainline=fc.Grainline(fc.P(-half * 0.5, 4.0), fc.P(half * 0.5, 4.0)),
        internals=[fc.Internal("roll-line",
                               [fc.P(-half, stand_h * 0.55),
                                fc.P(half, stand_h * 0.55)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Convertible Collar",
    )


def build():
    pattern = fc.PatternSet("magnetic-placket-shirt")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # The solved cap against both measured armholes, with its declared ease.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)
        # The collar against the measured neckline (front x2, back x2 = on fold).
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")],
                             tol=1.0)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "cotton poplin", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 76% marker; poplin presses a crisp placket, "
                 "which is what keeps the magnet pairs parallel."},
        {"item": "magnetic button cover", "qty": N_MAGNETS * 2, "unit": "count",
         "note": f"Yantra4D magnetic-button-cover (notion.hardware_ref): {N_MAGNETS} pairs "
                 f"at a solved {PITCH_SOLVED:.1f} mm pitch; the cover's snap lip takes a "
                 f"{button_diameter:.0f} mm shank button."},
        {"item": "shank buttons", "qty": N_MAGNETS, "unit": "count",
         "note": f"{button_diameter:.0f} mm, sewn to the OUTER placket as the visible face; "
                 "they never pass through a hole."},
        {"item": "fusible placket interfacing", "qty": round(2.0 * shirt_length),
         "unit": "mm_length",
         "note": f"{STAND * 2.0:.0f} mm wide; an unfused placket lets the magnets tilt."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": "topstitch both placket edges."},
    ]
    pattern.metadata = {
        "fc300_rank": 246,
        "family": "adaptive",
        "fabric_hint": "popelina-algodon",
        "finished_mm": {
            "chest": round(HALF_CHEST * 4.0, 1),
            "length": round(shirt_length, 1),
            "sleeve": round(sleeve_length, 1),
            "placket_stand": round(STAND, 1),
        },
        "solved": {
            "closure_run_mm": round(CLOSURE_RUN, 2),
            "magnets": N_MAGNETS,
            "pitch_requested_mm": round(magnet_pitch, 2),
            "pitch_solved_mm": round(PITCH_SOLVED, 2),
            "cap_height_mm": round(CAP_H, 2),
            "cap_length_mm": round(sum(s.length(0.2) for s in _cap_segments(CAP_H, 0.0)), 2),
            "armhole_total_mm": round(ARMHOLE_F + ARMHOLE_B, 2),
            "note": "the magnet pitch is RECOMPUTED from whole intervals across the "
                    "measured closure run, so the column lands exactly on both end "
                    "clearances instead of drifting; the sleeve cap height is bisected "
                    "against the MEASURED armholes.",
        },
        "adaptive": {
            "dressing": "closes with a knuckle nudge — no pinch, no fine motor control, "
                        "no buttonhole; the visible buttons are decorative",
            "conversion": "the cover's snap lip grips a conventional shank button, so an "
                          "existing shirt can be converted with the same hardware",
        },
        "hardware": "magnetic button covers via Yantra4D (notion.hardware_ref -> "
                    "magnetic-button-cover); the cover's sew ring is driven by this "
                    "shirt's button_diameter",
    }
    return pattern


result = build()

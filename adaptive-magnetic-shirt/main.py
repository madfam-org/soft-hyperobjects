"""
Magnetic-close Dress Shirt (adaptive) — Fashion Cabinet Garment Cartridge
(FC-400 rank #371, adaptive, Yantra4D-bridged magnetic-button-cover).

A proper dress shirt that closes without a pinch: decorative shank buttons sit on the outer
placket for looks, and underneath, a column of magnetic button covers snaps the shirt shut
with a knuckle nudge. The cover SOLID is Yantra4D territory (`magnetic-button-cover`;
notion.hardware_ref) — its snap lip grips a conventional shank button, so a wearer's own
shirts can be converted, not only ones cut from this pattern. A separating cuff placket and a
front bib pocket clear of the magnet column round out the office-ready look.

The drafting problem the placket poses: a magnetic pair only holds if the two magnet CENTRES
land on top of each other when the shirt is closed. So the button stand and buttonhole stand
must be mirror-equal about the centre front, and the magnet pitch must divide the closure run
into a whole number of intervals with the first and last magnet clear of the collar seam and
the hem. Both are SOLVED: n_magnets is derived from the measured closure run and the requested
pitch, then the pitch is RECOMPUTED so the column lands exactly, rather than accumulating
drift. The back neck width is SOLVED from the front's measured shoulder so the shoulder seam
matches, and the sleeve cap is bisected against the MEASURED armholes.

Pieces:
  - front  : shirt front (cut 2 mirrored), placket cut on.
  - back   : shirt back (cut 1 on fold at CB), yoke line marked.
  - sleeve : one-piece dropped-shoulder sleeve (cut 2 mirrored).
  - collar : convertible collar (cut 2 on fold).

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

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
shirt_length = float(PARAM(lambda: shirt_length, 740.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 470.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 630.0))
neck_girth = float(PARAM(lambda: neck_girth, 410.0))
button_diameter = float(PARAM(lambda: button_diameter, 18.0))
magnet_pitch = float(PARAM(lambda: magnet_pitch, 90.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1520.0))
shirt_length = max(560.0, min(shirt_length, 920.0))
shoulder_width = max(340.0, min(shoulder_width, 600.0))
sleeve_length = max(200.0, min(sleeve_length, 720.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
button_diameter = max(11.0, min(button_diameter, 25.0))
magnet_pitch = max(60.0, min(magnet_pitch, 140.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE_CHEST = 170.0
HALF_CHEST = (chest_girth + EASE_CHEST) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = neck_girth / 6.0 + 8.0
NECK_DROP_F = neck_girth / 6.0 + 18.0
NECK_DROP_B = 24.0
ARMHOLE_DROP = 250.0
SHOULDER_SLOPE = 42.0
STAND = button_diameter / 2.0 + 12.0

# ── Solve the magnet column ──────────────────────────────────────────────────
TOP_CLEAR = 55.0
HEM_CLEAR = 90.0
CLOSURE_RUN = shirt_length - NECK_DROP_F - TOP_CLEAR - HEM_CLEAR
N_INTERVALS = max(2, int(round(CLOSURE_RUN / magnet_pitch)))
N_MAGNETS = N_INTERVALS + 1
PITCH_SOLVED = CLOSURE_RUN / N_INTERVALS
MAGNET_TOP_Y = shirt_length - NECK_DROP_F - TOP_CLEAR


def _magnet_ys():
    return [MAGNET_TOP_Y - PITCH_SOLVED * i for i in range(N_MAGNETS)]


def build_front():
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
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h - NECK_DROP_F)],
                    kind="marking"),
        fc.Internal("placket-stitch",
                    [fc.P(STAND, 0.0), fc.P(STAND, h - NECK_DROP_F)], kind="marking"),
    ]
    for i, y in enumerate(_magnet_ys()):
        internals.append(fc.Internal(
            f"magnet-{i + 1}",
            [fc.P(-button_diameter / 2.0, y), fc.P(button_diameter / 2.0, y)],
            kind="drill"))
    pk_x, pk_y, pk_w, pk_h = STAND + 60.0, h - NECK_DROP_F - 300.0, 120.0, 140.0
    internals.append(fc.Internal(
        "bib-pocket",
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
_SHOULDER_LEN = math.hypot(HALF_SHOULDER - NECK_W, SHOULDER_SLOPE)
_BACK_NECK_Y_OFF = NECK_DROP_F - NECK_DROP_B - SHOULDER_SLOPE * 0.10
_dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
if _SHOULDER_LEN <= abs(_dy):
    # Degenerate: the vertical drop alone exceeds the shoulder length. Flatten the
    # back neck rise until a real horizontal run remains — the drawn rise MUST track
    # the flattened run (the back-neck-rise clamp lesson).
    _dy = _SHOULDER_LEN * 0.85
    _BACK_NECK_Y_OFF = _dy - SHOULDER_SLOPE
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = _BACK_NECK_Y_OFF


def build_back():
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
                                      fc.P(HALF_CHEST - 4.0, top - ARMHOLE_DROP * 0.44),
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
                               [fc.P(0.0, top - 120.0), fc.P(HALF_SHOULDER, top - 120.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Shirt Back",
    )


# ── Solve the sleeve cap against the MEASURED armholes ───────────────────────
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 14.0
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
BICEPS = max(360.0, (ARMHOLE_F + ARMHOLE_B) * 0.78)


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
                                fc.P(half * 0.9, top_y * 0.42)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_collar():
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
                               [fc.P(-half, stand_h * 0.55), fc.P(half, stand_h * 0.55)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Convertible Collar",
    )


def build():
    pattern = fc.PatternSet("adaptive-magnetic-shirt")
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
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.0)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "cotton poplin", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 76% marker; poplin presses a crisp placket, which "
                 "keeps the magnet pairs parallel."},
        {"item": "magnetic button cover", "qty": N_MAGNETS * 2, "unit": "count",
         "note": f"Yantra4D magnetic-button-cover (notion.hardware_ref): {N_MAGNETS} pairs "
                 f"at a solved {PITCH_SOLVED:.1f} mm pitch; the cover's snap lip takes a "
                 f"{button_diameter:.0f} mm shank button."},
        {"item": "shank buttons", "qty": N_MAGNETS, "unit": "count",
         "note": f"{button_diameter:.0f} mm, sewn to the OUTER placket as the visible face."},
        {"item": "fusible placket interfacing", "qty": round(2.0 * shirt_length),
         "unit": "mm_length",
         "note": f"{STAND * 2.0:.0f} mm wide; an unfused placket lets the magnets tilt."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": "topstitch both placket edges."},
    ]
    pattern.metadata = {
        "fc400_rank": 371,
        "family": "adaptive",
        "fabric_hint": "popelina-algodon",
        "finished_mm": {"chest": round(HALF_CHEST * 4.0, 1),
                        "length": round(shirt_length, 1),
                        "sleeve": round(sleeve_length, 1),
                        "placket_stand": round(STAND, 1)},
        "solved": {
            "closure_run_mm": round(CLOSURE_RUN, 2),
            "magnets": N_MAGNETS,
            "pitch_requested_mm": round(magnet_pitch, 2),
            "pitch_solved_mm": round(PITCH_SOLVED, 2),
            "cap_height_mm": round(CAP_H, 2),
            "armhole_total_mm": round(ARMHOLE_F + ARMHOLE_B, 2),
            "back_neck_width_mm": round(NECK_W_BACK, 2),
            "note": "the magnet pitch is RECOMPUTED from whole intervals across the "
                    "measured closure run so the column lands exactly on both end "
                    "clearances; the back neck width is solved from the front's measured "
                    "shoulder (with the flatten-the-rise clamp when the drop exceeds the "
                    "run); the sleeve cap is bisected against the MEASURED armholes.",
        },
        "adaptive": {
            "dressing": "closes with a knuckle nudge — no pinch, no fine motor control, no "
                        "buttonhole; the visible buttons are decorative",
            "conversion": "the cover's snap lip grips a conventional shank button, so an "
                          "existing shirt can be converted with the same hardware",
        },
        "hardware": "magnetic button covers via Yantra4D (notion.hardware_ref -> "
                    "magnetic-button-cover); the cover's sew ring is driven by this "
                    "shirt's button_diameter.",
    }
    return pattern


result = build()

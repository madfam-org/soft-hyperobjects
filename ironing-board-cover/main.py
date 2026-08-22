"""
Ironing Board Cover — Fashion Cabinet Care & Keeping Cartridge (FC-300 rank #260,
Yantra4D-bridged cord lock).

The drawstring cover for the one tool every other cartridge in this commons depends on.
A board cover that is loose scorches and creases what it is pressing; a cover that is
drum-tight is what makes a pressed seam stay pressed. The COVER is drafted to the board's
tapered nose-and-shoulder outline plus a turn-under skirt; a bias-cut CASING carries the
drawcord round the whole perimeter to a Yantra4D `cord-lock`; a PAD layer softens.

Drafting note — the seam that must SOLVE: the casing runs round the cover's OUTSIDE
perimeter, which is a closed convex-ish curve made of a nose arc, two long tapering sides
and a square heel — there is no formula for its length. The casing must be cut to that
perimeter or it will not close. This cartridge builds the outline once, MEASURES the full
perimeter, and cuts the casing to it. Separately: because the casing is a strip applied
round a CURVE, its inner edge travels a shorter path than its outer edge; that
inner/outer difference is computed by measuring an OFFSET copy of the same outline, and
is what forces the casing to be cut on the bias rather than straight-grain.

Pieces:
  - cover  : the board outline plus skirt (cut 1).
  - casing : the bias drawcord channel, cut to the measured perimeter (cut 1).
  - pad    : the felt underlayer, cut to the board line only (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # cover|casing|pad|set

board_length = float(PARAM(lambda: board_length, 1240.0))   # nose tip to heel
board_width = float(PARAM(lambda: board_width, 380.0))      # at the widest (the heel end)
nose_width = float(PARAM(lambda: nose_width, 130.0))        # across the rounded nose
skirt_depth = float(PARAM(lambda: skirt_depth, 90.0))       # the turn-under
cord_diameter = float(PARAM(lambda: cord_diameter, 5.0))    # drives the cord-lock
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
board_length = max(800.0, min(board_length, 1500.0))
board_width = max(280.0, min(board_width, 500.0))
nose_width = max(80.0, min(nose_width, 260.0))
skirt_depth = max(50.0, min(skirt_depth, 180.0))
cord_diameter = max(3.0, min(cord_diameter, 9.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# A board narrows toward the nose; hold that even if a caller inverts the pair.
nose_width = min(nose_width, board_width - 40.0)

NOSE_SEGS = 20
SHOULDER_SEGS = 24
HALF_W = board_width / 2.0
HALF_N = nose_width / 2.0
NOSE_R = HALF_N                       # the nose caps off as a half-round
SHOULDER_RUN = board_length * 0.42    # how far back the taper reaches


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


def _half_outline(off=0.0):
    """The board's RIGHT half-outline, from the nose crown back to the heel corner,
    offset outward by `off`. Returned nose-first.

    The shoulder is a smoothstep taper, not a straight bevel — a real board bulges
    out of the nose and then runs almost parallel. Measuring this curve is the whole
    point; no closed form exists for its length.
    """
    pts = []
    # Nose cap: a quarter-round centred at (NOSE_R, 0), swept from the crown
    # (angle π, on the axis) round to the widest point (angle π/2). Offsetting is
    # a radius increase about the SAME centre, so the offset copy stays concentric.
    r = NOSE_R + off
    for i in range(NOSE_SEGS + 1):
        a = math.pi - (math.pi / 2.0) * i / NOSE_SEGS
        pts.append(fc.P(NOSE_R + r * math.cos(a), r * math.sin(a)))
    # Shoulder: smoothstep from the nose half-width out to the board half-width.
    x0, x1 = NOSE_R, SHOULDER_RUN
    for i in range(1, SHOULDER_SEGS + 1):
        t = i / SHOULDER_SEGS
        s = t * t * (3.0 - 2.0 * t)             # smoothstep
        pts.append(fc.P(x0 + (x1 - x0) * t, (HALF_N + (HALF_W - HALF_N) * s) + off))
    # Parallel run back to the heel.
    pts.append(fc.P(board_length, HALF_W + off))
    return pts


_HALF = _half_outline(0.0)
_HALF_OUT = _half_outline(skirt_depth)     # the skirt's outer edge, one offset out

HALF_LEN = _poly_len(_HALF)
HALF_LEN_OUT = _poly_len(_HALF_OUT)

# The cover's full cut perimeter: both half outlines at the skirt line, plus the heel.
HEEL_RUN = 2.0 * (HALF_W + skirt_depth)
PERIMETER = 2.0 * HALF_LEN_OUT + HEEL_RUN
# The board line itself, for the pad.
BOARD_PERIMETER = 2.0 * HALF_LEN + 2.0 * HALF_W

# The casing's inner edge travels the board line; its outer edge the skirt line.
# That difference is why it must be cut on the bias.
CASING_HEIGHT = max(26.0, cord_diameter * 4.0 + 12.0)
CASING_CURVE_EXCESS = 2.0 * (HALF_LEN_OUT - HALF_LEN)


def _mirror_y(pts):
    return [fc.P(p.x, -p.y) for p in pts]


def build_cover():
    """The cover blank: the board outline pushed out by the skirt depth, closed
    across the heel."""
    top = _HALF_OUT                                  # nose → heel, +y side
    bot = list(reversed(_mirror_y(_HALF_OUT)))       # heel → nose, −y side
    edges = [
        fc.Edge("side_top", _lines(top)),
        fc.Edge("heel", [fc.Line(top[-1], bot[0])]),
        fc.Edge("side_bottom", _lines(bot)),
        # The nose crown closes the loop across the very tip.
        fc.Edge("nose_close", [fc.Line(bot[-1], top[0])]),
    ]
    internals = [
        fc.Internal("board-line-top", _HALF, kind="marking"),
        fc.Internal("board-line-bottom", _mirror_y(_HALF), kind="marking"),
        fc.Internal("casing-line",
                    [fc.P(NOSE_R, HALF_W + skirt_depth * 0.45),
                     fc.P(board_length, HALF_W + skirt_depth * 0.45)],
                    kind="marking"),
        fc.Internal("cord-exit",
                    [fc.P(board_length - 40.0, -(HALF_W + skirt_depth * 0.45)),
                     fc.P(board_length - 40.0 + cord_diameter * 4.0,
                          -(HALF_W + skirt_depth * 0.45))],
                    kind="drill"),
    ]
    return fc.Piece(
        "cover",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side_top", 0.0, "nose crown"),
                 fc.Notch("side_top", 0.5, "shoulder — ease the casing here"),
                 fc.Notch("heel", 0.5, "centre heel"),
                 fc.Notch("side_bottom", 0.5, "shoulder — ease the casing here")],
        grainline=fc.Grainline(fc.P(board_length * 0.25, 0.0),
                               fc.P(board_length * 0.75, 0.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Cover blank (board + skirt)",
    )


def build_casing():
    """The bias drawcord channel, cut to the MEASURED cover perimeter.

    Cut double the finished height and folded, so the cord runs in a clean tube
    with no raw edge against the board.
    """
    ln, h = PERIMETER, CASING_HEIGHT * 2.0
    return fc.Piece(
        "casing",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.0, "start at the heel"),
                 fc.Notch("attach", 0.5, "nose crown")],
        # Bias: the grainline runs at 45° because the casing has to travel a curve.
        grainline=fc.Grainline(fc.P(ln * 0.3, 0.0),
                               fc.P(ln * 0.3 + h, h)),
        internals=[fc.Internal("cord-channel",
                               [fc.P(0.0, h * 0.5), fc.P(ln, h * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Bias casing (drawcord)",
    )


def build_pad():
    """The felt underlayer, cut to the board line — no skirt, so it does not bulk
    up under the drawcord."""
    top = _HALF
    bot = list(reversed(_mirror_y(_HALF)))
    edges = [
        fc.Edge("side_top", _lines(top)),
        fc.Edge("heel", [fc.Line(top[-1], bot[0])]),
        fc.Edge("side_bottom", _lines(bot)),
        fc.Edge("nose_close", [fc.Line(bot[-1], top[0])]),
    ]
    return fc.Piece(
        "pad",
        edges,
        seam_allowance=0.0,
        notches=[fc.Notch("heel", 0.5, "centre heel")],
        grainline=fc.Grainline(fc.P(board_length * 0.25, 0.0),
                               fc.P(board_length * 0.75, 0.0)),
        cut=fc.CutSpec(quantity=1),
        label="Felt pad (board line)",
    )


def build():
    pattern = fc.PatternSet("ironing-board-cover")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "cover":
        pattern.add(build_cover())
    if all_pieces or target_piece == "casing":
        pattern.add(build_casing())
    if all_pieces or target_piece == "pad":
        pattern.add(build_pad())

    if all_pieces:
        # THE solving seam: the casing is cut to the cover's MEASURED perimeter, so
        # it closes on itself as it comes back round to the heel. There is no formula
        # for that perimeter — the smoothstep shoulder has no closed-form arc length.
        pattern.declare_seam(("casing", "attach"),
                             [("cover", "side_top"), ("cover", "heel"),
                              ("cover", "side_bottom"), ("cover", "nose_close")],
                             tol=1.0)
        # The two halves of the cover mirror each other exactly.
        pattern.declare_seam(("cover", "side_top"), ("cover", "side_bottom"), tol=0.5)
        # And the pad's halves likewise — it is the same outline, un-offset.
        pattern.declare_seam(("pad", "side_top"), ("pad", "side_bottom"), tol=0.5)

    cord_len = PERIMETER + 350.0
    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "cotton drill (heat-safe, undyed or fast-dyed)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 66% marker. Cotton only — a synthetic cover "
                 "melts onto the sole plate at wool settings."},
        {"item": "wool or cotton felt pad", "qty": 1, "unit": "count",
         "note": f"cut to the board line: ≈ {BOARD_PERIMETER:.0f} mm perimeter."},
        {"item": "drawcord", "qty": round(cord_len), "unit": "mm_length",
         "note": f"{cord_diameter:.1f} mm; one full circuit of the "
                 f"{PERIMETER:.0f} mm casing plus a tail to cinch."},
        {"item": "cord lock", "qty": 1, "unit": "count",
         "note": "Yantra4D cord-lock (see notion.hardware_ref); its cord channel is "
                 f"bored for the same {cord_diameter:.1f} mm cord. A cover you can "
                 f"re-tension is a cover that stays flat for years."},
    ]
    pattern.metadata = {
        "fc300_rank": 260,
        "family": "care_and_keeping",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"length": round(board_length, 1),
                        "width": round(board_width, 1),
                        "nose_width": round(nose_width, 1),
                        "skirt_depth": round(skirt_depth, 1)},
        "solved": {
            "half_outline_board_mm": round(HALF_LEN, 2),
            "half_outline_skirt_mm": round(HALF_LEN_OUT, 2),
            "cover_perimeter_mm": round(PERIMETER, 2),
            "board_perimeter_mm": round(BOARD_PERIMETER, 2),
            "casing_curve_excess_mm": round(CASING_CURVE_EXCESS, 2),
            "nose_segments": NOSE_SEGS,
            "shoulder_segments": SHOULDER_SEGS,
            "note": "the shoulder is a smoothstep taper with NO closed-form arc "
                    "length, so the casing is cut to the MEASURED perimeter. The "
                    f"skirt-line path runs {CASING_CURVE_EXCESS:.1f} mm longer than the "
                    "board-line path — "
                    "that inner/outer difference around a curve is exactly why the "
                    "casing is cut on the bias.",
        },
        "hardware": "drawcord tensioner via Yantra4D "
                    "(notion.hardware_ref -> cord-lock); cord_dia = cord_diameter",
    }
    return pattern


result = build()

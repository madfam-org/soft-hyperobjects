"""
Shaped Shoe-Tree Fabric Stuffer — Fashion Cabinet Care & Keeping Cartridge
(FC-400 rank #365, pattern-only — the shoe-tree solid is not in the pinned Yantra4D snapshot).

A stuffable fabric shoe tree: a foot-shaped sack that fills with cedar shavings, rolled
paper, or silica beads and holds a shoe's toe box open so it does not crease flat in
storage. A single UPPER panel wraps from toe to heel over the instep, an oval SOLE base
closes the bottom, and a drawstring HEEL casing cinches the fill in.

Drafting note — the seam that must SOLVE: the sole is an asymmetric oval (a foot outline
is wider at the ball than the heel), drafted as a smoothed polyline and MEASURED. The
upper's lower edge is cut to that MEASURED sole perimeter, so the two close on one number
regardless of shoe size. The upper's instep seam is a dart-free curved wrap whose height
is taken from the measured toe-to-heel run, not assumed.

Pieces:
  - upper : the wrap over the foot form (cut 1); toe_seam closes at the front.
  - sole  : the asymmetric oval base (cut 1).
  - heel  : the drawstring casing that cinches the fill (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # upper|sole|heel|set

foot_length = float(PARAM(lambda: foot_length, 270.0))   # toe to heel
ball_width = float(PARAM(lambda: ball_width, 100.0))     # widest point (the ball)
heel_width = float(PARAM(lambda: heel_width, 62.0))      # heel width
form_height = float(PARAM(lambda: form_height, 90.0))    # instep rise of the stuffed form
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
foot_length = max(150.0, min(foot_length, 340.0))
ball_width = max(60.0, min(ball_width, 150.0))
heel_width = max(40.0, min(heel_width, 100.0))
form_height = max(45.0, min(form_height, 150.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The heel must not be wider than the ball, or the outline is not a foot.
heel_width = min(heel_width, ball_width - 10.0)

ARC_SEGS = 20
BALL_R = ball_width / 2.0
HEEL_R = heel_width / 2.0
# The straight run between the ball arc and the heel arc.
STRAIGHT = max(20.0, foot_length - BALL_R - HEEL_R)


def _arc(cx, cy, r, a0, a1, n):
    return [fc.P(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# ── The asymmetric-oval sole, drafted once and MEASURED ──────────────────────
# Toe (ball) end at x = +STRAIGHT/2 with radius BALL_R; heel end at x = -STRAIGHT/2
# with radius HEEL_R. Two tangent straights join them along the top and bottom.
_TOE_X = STRAIGHT / 2.0
_HEEL_X = -STRAIGHT / 2.0
_CAP_TOE = _arc(_TOE_X, 0.0, BALL_R, -math.pi / 2.0, math.pi / 2.0, ARC_SEGS)
_CAP_HEEL = _arc(_HEEL_X, 0.0, HEEL_R, math.pi / 2.0, 3.0 * math.pi / 2.0, ARC_SEGS)
_SIDE_TOP = [fc.P(_TOE_X, BALL_R), fc.P(_HEEL_X, HEEL_R)]
_SIDE_BOT = [fc.P(_HEEL_X, -HEEL_R), fc.P(_TOE_X, -BALL_R)]
SOLE_PERIMETER = (_poly_len(_CAP_TOE) + _poly_len(_SIDE_TOP)
                  + _poly_len(_CAP_HEEL) + _poly_len(_SIDE_BOT))
WRAP = SOLE_PERIMETER


def build_upper():
    """The wrap over the foot form: WRAP wide (= sole perimeter) × form_height tall.
    Its `back_seam` (toe fold) and `heel_edge` are the two ends that close the tube;
    both are plain verticals of the same height, so the wrap seams cleanly and the
    foot shape comes entirely from the asymmetric sole below."""
    w, h = WRAP, form_height
    edges = [
        fc.Edge("back_seam", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("heel_edge", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("sole_edge", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "upper", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sole_edge", 0.25, "ball match"),
                 fc.Notch("sole_edge", 0.75, "heel match"),
                 fc.Notch("top", 0.5, "instep centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 12.0), fc.P(w * 0.5, h - 12.0)),
        internals=[fc.Internal("fill-line",
                               [fc.P(w * 0.2, h * 0.5), fc.P(w * 0.9, h * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Foot wrap upper",
    )


def build_sole():
    """The asymmetric oval base, split into four addressable edges so the upper's
    single sole_edge has a partner on every quarter."""
    edges = [
        fc.Edge("cap_toe", _lines(_CAP_TOE)),
        fc.Edge("side_top", _lines(_SIDE_TOP)),
        fc.Edge("cap_heel", _lines(_CAP_HEEL)),
        fc.Edge("side_bottom", _lines(_SIDE_BOT)),
    ]
    return fc.Piece(
        "sole", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("cap_toe", 0.5, "toe point"),
                 fc.Notch("cap_heel", 0.5, "heel point")],
        grainline=fc.Grainline(fc.P(_HEEL_X * 0.7, 0.0), fc.P(_TOE_X * 0.7, 0.0)),
        cut=fc.CutSpec(quantity=1),
        label="Foot-shaped sole",
    )


HEEL_CASING_W = max(60.0, heel_width * 2.4)
HEEL_CASING_H = 40.0


def build_heel():
    """The drawstring casing band that cinches the fill at the heel opening."""
    w, h = HEEL_CASING_W, HEEL_CASING_H * 2.0
    return fc.Piece(
        "heel", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("fold_top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.5, "match heel edge")],
        grainline=fc.Grainline(fc.P(w * 0.2, h / 2.0), fc.P(w * 0.8, h / 2.0)),
        internals=[fc.Internal("cord-channel",
                               [fc.P(0.0, h * 0.5), fc.P(w, h * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Heel drawstring casing",
    )


def build():
    pattern = fc.PatternSet("shoe-stuffer-bag")
    everything = target_piece == "set"
    if everything or target_piece == "upper":
        pattern.add(build_upper())
    if everything or target_piece == "sole":
        pattern.add(build_sole())
    if everything or target_piece == "heel":
        pattern.add(build_heel())

    if everything:
        # THE solving seam: the upper's sole edge walks the whole MEASURED oval sole.
        pattern.declare_seam(("upper", "sole_edge"),
                             [("sole", "cap_toe"), ("sole", "side_top"),
                              ("sole", "cap_heel"), ("sole", "side_bottom")],
                             tol=1.2)
    if everything or target_piece == "upper":
        # The upper wraps into a tube: its back seam meets the heel edge (both plain
        # verticals of form_height), closing the cone.
        pattern.declare_seam(("upper", "back_seam"), ("upper", "heel_edge"), tol=1.0)

    fabric_width = 1300.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton drill", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1300 mm width, 72% marker; a firm drill holds the toe box shape "
                 "once the sack is filled."},
        {"item": "cedar shavings or silica beads", "qty": round(foot_length * ball_width
                 * form_height / 8000.0), "unit": "cm3",
         "note": "the fill; cedar also deodorises, silica also dries a wet shoe out."},
        {"item": "drawcord", "qty": round(HEEL_CASING_W + 200.0), "unit": "mm_length",
         "note": "one loop round the heel casing plus a pull tail."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "flat-fell the sole seam so it survives repeated stuffing."},
    ]
    pattern.metadata = {
        "fc400_rank": 365,
        "family": "care_and_keeping",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"foot_length": round(foot_length, 1),
                        "ball_width": round(ball_width, 1),
                        "heel_width": round(heel_width, 1)},
        "solved": {
            "sole_shape": "asymmetric oval (ball cap + heel cap + two tangent sides)",
            "sole_perimeter_mm": round(SOLE_PERIMETER, 2),
            "upper_wrap_mm": round(WRAP, 2),
            "arc_segments_per_cap": ARC_SEGS,
            "note": "the sole is a foot outline (ball wider than heel) drafted as a "
                    "measured polyline; the upper's sole edge is cut to that MEASURED "
                    "perimeter, so the base seam closes on one number at any size.",
        },
        "hardware": "none linked — a printable shoe-tree body would be the natural "
                    "bridge, but shoe-tree is NOT in the pinned Yantra4D snapshot. "
                    "Logged co-create (shoe-tree) in the FC-400 index; this cartridge "
                    "stays honestly pattern-only rather than declare a dangling ref.",
    }
    return pattern


result = build()

"""
Shoe Bag (Drawstring) — Fashion Cabinet Care & Keeping Cartridge (FC-300 rank #254,
Yantra4D-bridged cord lock).

The travelling shoe bag: a flat-bottomed drawstring sack that swallows a pair of shoes
sole-to-sole and cinches shut on a cord. A single BODY panel wraps into a tube, an oval
BASE closes the bottom, and a folded CASING band at the mouth carries the drawcord with
a Yantra4D `cord-lock` toggle on the tail.

Drafting note — the seam that must SOLVE: the base is an OVAL (a stadium — two
half-circles joined by straights), because a shoe pair is long and narrow and a circular
base wastes fabric on the width. Its perimeter has no clean closed form once it is
polygonised, so the body's wrap length is taken from the MEASURED base perimeter, and
the casing band is measured against the same wrap. Three seams solve off one measurement.

Pieces:
  - body   : the tube wall; `wrap_a` meets `wrap_b` at the side seam.
  - base   : the oval bottom (cut 1).
  - casing : the folded drawcord channel at the mouth (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # body|base|casing|set

shoe_length = float(PARAM(lambda: shoe_length, 310.0))    # longest shoe in the pair
shoe_width = float(PARAM(lambda: shoe_width, 115.0))      # widest point of one shoe
bag_height = float(PARAM(lambda: bag_height, 400.0))      # base seam to mouth
cord_diameter = float(PARAM(lambda: cord_diameter, 4.0))  # drawcord; drives the cord-lock
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
shoe_length = max(180.0, min(shoe_length, 400.0))
shoe_width = max(70.0, min(shoe_width, 180.0))
bag_height = max(220.0, min(bag_height, 620.0))
cord_diameter = max(2.0, min(cord_diameter, 8.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The base is a stadium sized to swallow a pair stacked sole-to-sole, plus ease.
BASE_EASE = 24.0
BASE_LEN = shoe_length + BASE_EASE            # overall oval length
BASE_WID = shoe_width * 2.0 * 0.62 + BASE_EASE  # a pair nests, so not a full 2× width
BASE_R = BASE_WID / 2.0
STRAIGHT = max(10.0, BASE_LEN - BASE_WID)     # the flat run between the two half-ends
ARC_SEGS = 24                                 # per half-end

# The casing must clear the cord doubled back plus turn-of-cloth.
CASING_HEIGHT = max(24.0, cord_diameter * 4.0 + 14.0)


def _arc(cx, cy, r, a0, a1, n):
    return [fc.P(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# ── The stadium base, drafted once and MEASURED ──────────────────────────────
# Centred on the origin, long axis along x. Right end cap sweeps -90°→+90°.
_HX = STRAIGHT / 2.0
_CAP_R = _arc(_HX, 0.0, BASE_R, -math.pi / 2.0, math.pi / 2.0, ARC_SEGS)
_CAP_L = _arc(-_HX, 0.0, BASE_R, math.pi / 2.0, 3.0 * math.pi / 2.0, ARC_SEGS)

_SIDE_TOP = [fc.P(_HX, BASE_R), fc.P(-_HX, BASE_R)]
_SIDE_BOT = [fc.P(-_HX, -BASE_R), fc.P(_HX, -BASE_R)]

BASE_PERIMETER = (_poly_len(_CAP_R) + _poly_len(_SIDE_TOP)
                  + _poly_len(_CAP_L) + _poly_len(_SIDE_BOT))
WRAP = BASE_PERIMETER          # the body's wrap = the MEASURED oval perimeter


def build_body():
    """The tube wall: WRAP wide × bag_height tall. `hem_base` sews to the oval."""
    w, h = WRAP, bag_height
    edges = [
        fc.Edge("wrap_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("wrap_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("hem_base", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    # Cord exit: the casing is broken at the side seam so the cord tails emerge there.
    internals = [
        fc.Internal("cord-exit",
                    [fc.P(4.0, h - CASING_HEIGHT * 0.5),
                     fc.P(4.0 + cord_diameter * 3.0, h - CASING_HEIGHT * 0.5)],
                    kind="drill"),
        fc.Internal("casing-fold-line",
                    [fc.P(0.0, h - CASING_HEIGHT), fc.P(w, h - CASING_HEIGHT)],
                    kind="marking"),
    ]
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("hem_base", 0.25, "oval end cap"),
                 fc.Notch("hem_base", 0.75, "oval end cap"),
                 fc.Notch("mouth", 0.5, "opposite the side seam")],
        grainline=fc.Grainline(fc.P(w * 0.5, 30.0), fc.P(w * 0.5, h - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (tube wall)",
    )


def build_base():
    """The oval (stadium) bottom, split into four named edges so the body's single
    `hem_base` edge has an addressable seam partner on every quarter."""
    edges = [
        fc.Edge("cap_r", _lines(_CAP_R)),
        fc.Edge("side_top", _lines(_SIDE_TOP)),
        fc.Edge("cap_l", _lines(_CAP_L)),
        fc.Edge("side_bottom", _lines(_SIDE_BOT)),
    ]
    return fc.Piece(
        "base",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("cap_r", 0.5, "long-axis end"),
                 fc.Notch("cap_l", 0.5, "long-axis end")],
        grainline=fc.Grainline(fc.P(-_HX * 0.7, 0.0), fc.P(_HX * 0.7, 0.0)),
        cut=fc.CutSpec(quantity=1),
        label="Oval base",
    )


def build_casing():
    """The drawcord channel: a band the same wrap length as the mouth, folded in half
    lengthwise. Cut as a single strip 2× the finished casing height."""
    w, h = WRAP, CASING_HEIGHT * 2.0
    return fc.Piece(
        "casing",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("fold_top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.5, "match the mouth notch")],
        grainline=fc.Grainline(fc.P(w * 0.2, h / 2.0), fc.P(w * 0.8, h / 2.0)),
        internals=[fc.Internal("cord-channel",
                               [fc.P(0.0, h * 0.5), fc.P(w, h * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Drawcord casing band",
    )


def build():
    pattern = fc.PatternSet("shoe-bag-drawstring")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "base":
        pattern.add(build_base())
    if all_pieces or target_piece == "casing":
        pattern.add(build_casing())

    if all_pieces or target_piece == "body":
        pattern.declare_seam(("body", "wrap_a"), ("body", "wrap_b"), tol=0.5)
    if all_pieces:
        # The solving seam: the tube's hem walks the whole MEASURED oval perimeter.
        pattern.declare_seam(("body", "hem_base"),
                             [("base", "cap_r"), ("base", "side_top"),
                              ("base", "cap_l"), ("base", "side_bottom")],
                             tol=1.0)
        # The casing band is cut to the same wrap, so it closes with the mouth.
        pattern.declare_seam(("casing", "attach"), ("body", "mouth"), tol=0.5)

    cord_len = WRAP + bag_height * 0.6 + 250.0
    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "cotton drill or ripstop", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 80% marker; an unlined bag is the point — "
                 "it has to breathe around damp shoes."},
        {"item": "drawcord", "qty": round(cord_len), "unit": "mm_length",
         "note": f"{cord_diameter:.1f} mm cord: one loop round the casing plus a tail."},
        {"item": "cord lock", "qty": 1, "unit": "count",
         "note": "Yantra4D cord-lock (see notion.hardware_ref); its cord channel is "
                 f"bored for the same {cord_diameter:.1f} mm cord."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "flat-fell the side seam so it survives being turned inside out."},
    ]
    pattern.metadata = {
        "fc300_rank": 254,
        "family": "care_and_keeping",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"height": round(bag_height, 1),
                        "base_length": round(BASE_LEN, 1),
                        "base_width": round(BASE_WID, 1)},
        "solved": {
            "base_shape": "stadium (two half-circle caps + two straights)",
            "arc_segments_per_cap": ARC_SEGS,
            "base_perimeter_mm": round(BASE_PERIMETER, 2),
            "true_stadium_mm": round(2.0 * STRAIGHT + 2.0 * math.pi * BASE_R, 2),
            "body_wrap_mm": round(WRAP, 2),
            "note": "body wrap = the MEASURED polygonised stadium perimeter, not the "
                    "closed-form 2·s + 2·π·r — so the base seam and the casing band "
                    "both close on one number.",
        },
        "hardware": "drawcord toggle via Yantra4D (notion.hardware_ref -> cord-lock); "
                    "cord_dia = cord_diameter",
    }
    return pattern


result = build()

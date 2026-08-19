"""
Belt Bag / Fanny Pack — Fashion Cabinet Accessory Cartridge (FC-200 rank #129, y4d zip).

A curved-front belt bag: a body panel (front + base + back folded at the base), a top zip,
and a webbing belt threaded through two loops. The zip solid bridges to the Yantra4D
`zipper`; the adjustable belt bridges (via the same webbing width) to the strap-buckle
family. Fashion Cabinet owns the bag; Yantra4D owns the zip + buckle.

Pieces:
  - body      : front + base + back as one fold-at-base panel; top edges take the zip.
  - belt_loop : two short webbing loops the belt threads through.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|belt_loop|set

bag_width   = float(PARAM(lambda: bag_width, 260.0))    # width (zip runs along this)
bag_height  = float(PARAM(lambda: bag_height, 150.0))   # front-face height
bag_depth   = float(PARAM(lambda: bag_depth, 70.0))     # box depth
belt_width  = float(PARAM(lambda: belt_width, 38.0))    # webbing belt width (loop size)
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_width  = max(140.0, min(bag_width, 420.0))
bag_height = max(80.0, min(bag_height, 260.0))
bag_depth  = max(30.0, min(bag_depth, 160.0))
belt_width = max(20.0, min(belt_width, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

BW = bag_width
BH = 2.0 * bag_height + bag_depth


def build_body():
    """Front + base + back, folded at the base; the front face curves gently at the top
    toward the zip (the belt bag's soft crescent front)."""
    top_front_l = fc.P(0.0, 0.0)
    top_front_r = fc.P(BW, 0.0)
    edges = [
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))]),
        fc.Edge("zip_back", [fc.Line(fc.P(0.0, BH), fc.P(BW, BH))]),
        fc.Edge("right", [fc.Line(fc.P(BW, BH), fc.P(BW, 0.0))]),
        fc.Edge("zip_front", [fc.curve_through(top_front_r, top_front_l, bulge=0.06, side=1.0)]),
    ]
    y_fb = bag_height
    y_bb = bag_height + bag_depth
    internals = [
        fc.Internal("fold-front-base", [fc.P(0.0, y_fb), fc.P(BW, y_fb)], kind="marking"),
        fc.Internal("fold-base-back", [fc.P(0.0, y_bb), fc.P(BW, y_bb)], kind="marking"),
    ]
    # Belt-loop attachment marks on the back panel.
    for x in (BW * 0.30, BW * 0.70):
        internals.append(fc.Internal("loop-mark",
                                     [fc.P(x - 4.0, y_bb + 20.0), fc.P(x + 4.0, y_bb + 20.0)],
                                     kind="drill"))
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("left", y_fb / BH, "front base fold"),
                 fc.Notch("left", y_bb / BH, "back base fold")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 40.0), fc.P(BW * 0.5, BH - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (front + base + back)",
    )


def build_belt_loop():
    """A short webbing loop the belt threads through (cut 2). Width slightly over the
    belt width so the belt slides."""
    w = belt_width + 10.0
    ln = 90.0
    return fc.Piece(
        "belt_loop",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Belt Loop",
    )


def build():
    pattern = fc.PatternSet("belt-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "belt_loop":
        pattern.add(build_belt_loop())

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "cordura or ripstop nylon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length", "note": "≈ at 1400 mm width, 80% marker; light lining advised."},
        {"item": "top zip", "qty": 1, "unit": "count",
         "note": f"Yantra4D zipper (see notion.hardware_ref), ≈ {bag_width:.0f} mm long."},
        {"item": "webbing belt + buckle", "qty": 1, "unit": "set",
         "note": "the belt threads the loops; pair with the Yantra4D strap-buckle for adjust."},
    ]
    pattern.metadata = {
        "fc200_rank": 129,
        "family": "accessories",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"width": round(bag_width, 1), "height": round(bag_height, 1),
                        "depth": round(bag_depth, 1)},
        "hardware": "top zip via Yantra4D (notion.hardware_ref -> zipper); belt via strap-buckle",
    }
    return pattern


result = build()

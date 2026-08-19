"""
Dopp Kit — Fashion Cabinet Accessory Cartridge (FC-200 rank #130, Yantra4D-bridged zip).

A boxed toiletry / wash bag: a wrap body (front + base + back folded at the base), two
end gussets that give it its rigid box shape, and a top zip. The zip solid is Yantra4D
territory (`zipper`; see the manifest's notion.hardware_ref). Fashion Cabinet owns the
bag — dimensions, boxed shape, zip length.

Pieces:
  - body     : front + base + back as one fold-at-base rectangle, top edges take the zip.
  - end      : two end gussets (rectangles the height+depth of the box).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|end|set

kit_length  = float(PARAM(lambda: kit_length, 240.0))   # length (zip runs along this)
kit_height  = float(PARAM(lambda: kit_height, 130.0))   # front-face height
kit_depth   = float(PARAM(lambda: kit_depth, 120.0))    # box depth (end-gusset width)
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
kit_length = max(120.0, min(kit_length, 450.0))
kit_height = max(80.0, min(kit_height, 300.0))
kit_depth  = max(60.0, min(kit_depth, 250.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

BW = kit_length
BH = 2.0 * kit_height + kit_depth                   # front + base + back flat panel


def build_body():
    edges = [
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))]),
        fc.Edge("zip_back", [fc.Line(fc.P(0.0, BH), fc.P(BW, BH))]),    # back top (zip tape)
        fc.Edge("right", [fc.Line(fc.P(BW, BH), fc.P(BW, 0.0))]),
        fc.Edge("zip_front", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),  # front top (zip tape)
    ]
    y_fb = kit_height
    y_bb = kit_height + kit_depth
    internals = [
        fc.Internal("fold-front-base", [fc.P(0.0, y_fb), fc.P(BW, y_fb)], kind="marking"),
        fc.Internal("fold-base-back", [fc.P(0.0, y_bb), fc.P(BW, y_bb)], kind="marking"),
    ]
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


def build_end():
    """One end gusset: a rectangle depth wide x height tall, with the top corners softly
    rounded toward the zip. Cut 2."""
    w, h = kit_depth, kit_height
    top_l = fc.P(0.0, h)
    top_r = fc.P(w, h)
    return fc.Piece(
        "end",
        [
            fc.Edge("attach_l", [fc.Line(fc.P(0.0, 0.0), top_l)]),
            fc.Edge("top", [fc.curve_through(top_l, top_r, bulge=0.10, side=1.0)]),  # toward zip
            fc.Edge("attach_r", [fc.Line(top_r, fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "base centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="End Gusset",
    )


def build():
    pattern = fc.PatternSet("dopp-kit")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "end":
        pattern.add(build_end())

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "coated / laminated cotton or waxed canvas",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 75% marker; a wipe-clean lining recommended."},
        {"item": "top zip", "qty": 1, "unit": "count",
         "note": f"Yantra4D zipper (see notion.hardware_ref), ≈ {kit_length:.0f} mm long."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "box the ends to the body; a boxed bag holds its shape."},
    ]
    pattern.metadata = {
        "fc200_rank": 130,
        "family": "accessories",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"length": round(kit_length, 1), "height": round(kit_height, 1),
                        "depth": round(kit_depth, 1)},
        "hardware": "top zip via Yantra4D (notion.hardware_ref -> zipper)",
    }
    return pattern


result = build()

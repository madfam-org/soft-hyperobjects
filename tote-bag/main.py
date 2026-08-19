"""
Tote Bag — Fashion Cabinet Accessory Cartridge (FC-200 rank #127, Yantra4D-bridged strap).

A classic boxed-bottom tote: one wrap body panel (front + back cut as one, folded at the
base) that boxes at the lower corners for a flat bottom, plus two carry straps. The
optional adjustable strap hardware is Yantra4D territory (`strap-buckle`; see the
manifest's notion.hardware_ref). Fashion Cabinet owns the bag — dimensions, boxed-corner
depth, strap length. Made-to-order homeware/carry, not a body garment.

Pieces:
  - body   : one panel = front + base + back as a single fold-at-base rectangle, with
             lower corners boxed (a square notch cut at each bottom corner).
  - strap  : two carry straps (self fabric or webbing).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|strap|set

bag_width   = float(PARAM(lambda: bag_width, 380.0))    # finished width across the front
bag_height  = float(PARAM(lambda: bag_height, 400.0))   # finished height (front face)
bag_depth   = float(PARAM(lambda: bag_depth, 120.0))    # boxed-bottom depth (gusset)
strap_width = float(PARAM(lambda: strap_width, 40.0))   # carry-strap width
strap_length = float(PARAM(lambda: strap_length, 600.0))  # carry-strap length
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))  # top-hem turn-under
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_width   = max(200.0, min(bag_width, 600.0))
bag_height  = max(200.0, min(bag_height, 600.0))
bag_depth   = max(0.0, min(bag_depth, 250.0))
strap_width = max(20.0, min(strap_width, 60.0))
strap_length = max(300.0, min(strap_length, 900.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

box = bag_depth / 2.0                                # corner-notch half-depth
# The body is front + base + back stacked: total height = height + depth + height,
# width = bag_width. The lower corners of front and back box for the flat bottom.
BW = bag_width
BH = 2.0 * bag_height + bag_depth                   # full flat panel height (front+base+back)


def build_body():
    """The wrap body: a tall rectangle (front + base + back), folded at the base. The two
    corners at the base fold line box out (a square notch) so the bag has a flat bottom.
    We draft the flat panel with the corner notches marked as internal box lines; the
    outline stays a simple rectangle (the notch is sewn, not cut away, to keep one piece).
    """
    edges = [
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))]),
        fc.Edge("top_back", [fc.Line(fc.P(0.0, BH), fc.P(BW, BH))]),   # back top opening
        fc.Edge("right", [fc.Line(fc.P(BW, BH), fc.P(BW, 0.0))]),
        fc.Edge("top_front", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),  # front top opening
    ]
    internals = []
    # Base fold lines (front↔base and base↔back).
    y_front_base = bag_height
    y_base_back = bag_height + bag_depth
    internals.append(fc.Internal("fold-front-base",
                                 [fc.P(0.0, y_front_base), fc.P(BW, y_front_base)], kind="marking"))
    internals.append(fc.Internal("fold-base-back",
                                 [fc.P(0.0, y_base_back), fc.P(BW, y_base_back)], kind="marking"))
    if bag_depth > 0.0:
        # Boxed-corner stitch lines at the four base corners.
        for (cx, cy) in [(0.0, y_front_base), (BW, y_front_base),
                         (0.0, y_base_back), (BW, y_base_back)]:
            sx = box if cx == 0.0 else -box
            internals.append(fc.Internal("box-corner",
                                         [fc.P(cx, cy - (box if cy == y_front_base else -box)),
                                          fc.P(cx + sx, cy)], kind="marking"))
    # Strap attachment marks on the front and back top edges.
    for y in (10.0, BH - 10.0):
        for x in (BW * 0.28, BW * 0.72):
            internals.append(fc.Internal("strap-mark",
                                         [fc.P(x - 4.0, y), fc.P(x + 4.0, y)], kind="drill"))
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        allowances={"top_front": hem_allowance, "top_back": hem_allowance},
        notches=[fc.Notch("left", bag_height / BH, "front base fold"),
                 fc.Notch("left", (bag_height + bag_depth) / BH, "back base fold")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 60.0), fc.P(BW * 0.5, BH - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (front + base + back)",
    )


def _strap():
    return fc.Piece(
        "strap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(strap_length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(strap_length, 0.0), fc.P(strap_length, strap_width))]),
            fc.Edge("top", [fc.Line(fc.P(strap_length, strap_width), fc.P(0.0, strap_width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, strap_width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(strap_length * 0.2, strap_width / 2.0),
                               fc.P(strap_length * 0.8, strap_width / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Carry Strap",
    )


def build():
    pattern = fc.PatternSet("tote-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "strap":
        pattern.add(_strap())

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "canvas or heavy cotton", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length", "note": "≈ at 1400 mm width, 80% marker; line for a stiffer tote."},
        {"item": "adjustable strap buckle (optional)", "qty": 1, "unit": "count",
         "note": "Yantra4D strap-buckle (see notion.hardware_ref) for a length-adjustable strap."},
        {"item": "all-purpose / upholstery thread", "qty": 1, "unit": "spool",
         "note": "topstitch the straps and hem; box the corners for a flat bottom."},
    ]
    pattern.metadata = {
        "fc200_rank": 127,
        "family": "accessories",
        "fabric_hint": "manta-cruda",
        "boxed_bottom": f"depth {bag_depth:.0f} mm; corners boxed at the base fold for a "
                        "flat bottom.",
        "finished_mm": {"width": round(bag_width, 1), "height": round(bag_height, 1),
                        "depth": round(bag_depth, 1)},
        "hardware": "optional adjustable strap via Yantra4D (notion.hardware_ref -> strap-buckle)",
    }
    return pattern


result = build()

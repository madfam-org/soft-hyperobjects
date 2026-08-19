"""
Backpack (Panelled) — Fashion Cabinet Accessory Cartridge (FC-200 rank #128, y4d buckle).

A simple panelled rucksack: a wrap body (front + base + back folded at the base), two
side/base gussets, a top flap that buckles shut, and two shoulder straps. The adjustable
strap + flap buckle hardware bridges to the Yantra4D `strap-buckle`. Fashion Cabinet owns
the pack — dimensions, gusset depth, strap length.

Pieces:
  - body   : front + base + back as one fold-at-base panel.
  - gusset : one long side gusset wrapping both sides + the base (cut 1 or 2).
  - flap   : the top flap that folds over and buckles.
  - strap  : two padded shoulder straps.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|gusset|flap|strap|set

pack_width  = float(PARAM(lambda: pack_width, 300.0))   # front width
pack_height = float(PARAM(lambda: pack_height, 440.0))  # front-face height
pack_depth  = float(PARAM(lambda: pack_depth, 160.0))   # gusset depth
flap_drop   = float(PARAM(lambda: flap_drop, 220.0))    # how far the flap covers the front
strap_width = float(PARAM(lambda: strap_width, 45.0))   # shoulder-strap width
strap_length = float(PARAM(lambda: strap_length, 700.0))  # shoulder-strap length
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
pack_width  = max(220.0, min(pack_width, 480.0))
pack_height = max(300.0, min(pack_height, 620.0))
pack_depth  = max(80.0, min(pack_depth, 260.0))
flap_drop   = max(120.0, min(flap_drop, pack_height * 0.7))
strap_width = max(25.0, min(strap_width, 70.0))
strap_length = max(450.0, min(strap_length, 900.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

BW = pack_width
BH = 2.0 * pack_height + pack_depth


def build_body():
    edges = [
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))]),
        fc.Edge("top_back", [fc.Line(fc.P(0.0, BH), fc.P(BW, BH))]),
        fc.Edge("right", [fc.Line(fc.P(BW, BH), fc.P(BW, 0.0))]),
        fc.Edge("top_front", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
    ]
    y_fb = pack_height
    y_bb = pack_height + pack_depth
    internals = [
        fc.Internal("fold-front-base", [fc.P(0.0, y_fb), fc.P(BW, y_fb)], kind="marking"),
        fc.Internal("fold-base-back", [fc.P(0.0, y_bb), fc.P(BW, y_bb)], kind="marking"),
    ]
    # Shoulder-strap anchor marks (top of back + base of back).
    for (x, y) in [(BW * 0.35, BH - 15.0), (BW * 0.65, BH - 15.0),
                   (BW * 0.30, y_bb + 15.0), (BW * 0.70, y_bb + 15.0)]:
        internals.append(fc.Internal("strap-anchor",
                                     [fc.P(x - 5.0, y), fc.P(x + 5.0, y)], kind="drill"))
    return fc.Piece(
        "body", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("left", y_fb / BH, "front base fold"),
                 fc.Notch("left", y_bb / BH, "back base fold")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 60.0), fc.P(BW * 0.5, BH - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (front + base + back)",
    )


def build_gusset():
    """A long side gusset that wraps up one side, across the base, and up the other side.
    Length = height + depth + height; width = depth. Cut 1 (or split into 2)."""
    w = pack_depth
    ln = 2.0 * pack_height + pack_depth
    return fc.Piece(
        "gusset",
        [
            fc.Edge("attach_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, ln))]),
            fc.Edge("top_a", [fc.Line(fc.P(0.0, ln), fc.P(w, ln))]),
            fc.Edge("attach_b", [fc.Line(fc.P(w, ln), fc.P(w, 0.0))]),
            fc.Edge("top_b", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach_a", pack_height / ln, "base corner"),
                 fc.Notch("attach_a", (pack_height + pack_depth) / ln, "base corner")],
        grainline=fc.Grainline(fc.P(w * 0.5, 60.0), fc.P(w * 0.5, ln - 60.0)),
        cut=fc.CutSpec(quantity=1),
        label="Side/Base Gusset",
    )


def build_flap():
    """The top flap: a rounded rectangle that folds over the front and buckles."""
    w = pack_width + 20.0
    h = flap_drop
    edges = [
        fc.Edge("hinge", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),      # sews to the back top
        fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 40.0))]),
        fc.Edge("front", [fc.curve_through(fc.P(w, 40.0), fc.P(0.0, 40.0), bulge=0.10, side=-1.0)]),
        fc.Edge("left", [fc.Line(fc.P(0.0, 40.0), fc.P(0.0, h))]),
    ]
    internals = [fc.Internal("buckle-mark",
                             [fc.P(w / 2.0 - 5.0, 60.0), fc.P(w / 2.0 + 5.0, 60.0)], kind="drill")]
    return fc.Piece(
        "flap", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(w * 0.5, 60.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Top Flap",
    )


def build_strap():
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
        label="Shoulder Strap",
    )


def build():
    pattern = fc.PatternSet("backpack-panel")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "gusset":
        pattern.add(build_gusset())
    if all_pieces or target_piece == "flap":
        pattern.add(build_flap())
    if all_pieces or target_piece == "strap":
        pattern.add(build_strap())

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "cordura / waxed canvas", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length", "note": "≈ at 1400 mm width, 78% marker; foam-back the straps."},
        {"item": "flap + strap buckles", "qty": 3, "unit": "count",
         "note": "Yantra4D strap-buckle (notion.hardware_ref): one flap + two strap adjusters."},
        {"item": "webbing + thread", "qty": 1, "unit": "set",
         "note": "topstitch the anchors well — a pack takes load."},
    ]
    pattern.metadata = {
        "fc200_rank": 128,
        "family": "accessories",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"width": round(pack_width, 1), "height": round(pack_height, 1),
                        "depth": round(pack_depth, 1)},
        "hardware": "flap + strap buckles via Yantra4D (notion.hardware_ref -> strap-buckle)",
    }
    return pattern


result = build()

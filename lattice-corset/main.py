"""
Printed lattice corset — FC-400 rank #350, Lane 5 (am_fashion). Fashion Cabinet Cartridge.

A corset built from printed TPU lattice panels — an open tile-and-bridge lattice that is
rigid enough to shape the waist yet flexes at the bridges to breathe, printed instead of
boned. The lattice is Yantra4D territory (notion.hardware_ref → tpu-lattice-panel); Fashion
Cabinet owns the corset FASHION: the shaped waist-cinching panel (bust over waist to hip)
and the lattice field (rows × cols) DERIVED from the panel so the tiling clads the shape.

What this cartridge owns:
  - THE CORSET panel placement guide: an hourglass panel (cut 2, mirrored) from the
    under-bust down over the waist to the hip, sized from bust, waist and hip girths and
    the torso length.
  - THE LATTICE FIELD: cols/rows DERIVED from the panel and the tile+gap pitch.

Solving and clamps. The bust, waist and hip half-widths are DERIVED and FLOORED; the waist
half is clamped BELOW both the bust and the hip so the hourglass never bulges out at the
waist (an inverted cinch). The field cols/rows are floored at 1.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # placement-guide|set

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
waist_girth = float(PARAM(lambda: waist_girth, 720.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
torso_length = float(PARAM(lambda: torso_length, 340.0))    # under-bust to hip
waist_position = float(PARAM(lambda: waist_position, 0.5))  # waist level as fraction of length
cinch = float(PARAM(lambda: cinch, 60.0))                  # extra waist reduction
tile_size = float(PARAM(lambda: tile_size, 22.0))
tile_gap = float(PARAM(lambda: tile_gap, 7.0))
wall = float(PARAM(lambda: wall, 1.6))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

bust_girth = max(600.0, min(bust_girth, 1500.0))
waist_girth = max(500.0, min(waist_girth, 1300.0))
hip_girth = max(600.0, min(hip_girth, 1500.0))
torso_length = max(180.0, min(torso_length, 520.0))
waist_position = max(0.25, min(waist_position, 0.75))
cinch = max(0.0, min(cinch, 200.0))
tile_size = max(10.0, min(tile_size, 70.0))
tile_gap = max(2.0, min(tile_gap, 30.0))
wall = max(0.6, min(wall, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

BUST_Q = max(90.0, bust_girth / 4.0)
HIP_Q = max(90.0, hip_girth / 4.0)
# Waist half is the girth quarter less the cinch, floored, and clamped BELOW bust and hip.
_waist_raw = waist_girth / 4.0 - cinch / 2.0
WAIST_Q = max(60.0, min(_waist_raw, BUST_Q - 15.0, HIP_Q - 15.0))
WAIST_CLAMPED = _waist_raw != WAIST_Q
H = max(150.0, torso_length)
WAIST_Y = H * (1.0 - max(0.25, min(waist_position, 0.75)))   # from the hem up
W = (BUST_Q + WAIST_Q + HIP_Q) / 3.0                     # average width for the field
pitch = tile_size + tile_gap
cols = max(1, round(W / pitch))
rows = max(1, round(H / pitch))


def build():
    # Hourglass panel: bust edge (top), side curves in to the waist then out to hip, hem.
    cf_bottom = fc.P(0.0, 0.0)                   # centre-front hem (hip level)
    cf_top = fc.P(0.0, H)                        # centre-front under-bust
    bust_side = fc.P(BUST_Q, H)
    waist_side = fc.P(WAIST_Q, WAIST_Y)
    hip_side = fc.P(HIP_Q, 0.0)
    edges = [
        fc.Edge("guide", [fc.Line(cf_bottom, cf_top)]),        # centre front (sewn/busk)
        fc.Edge("top", [fc.Line(cf_top, bust_side)]),          # under-bust edge
        fc.Edge("side", [fc.curve_through(bust_side, waist_side, bulge=0.10, side=-1.0),
                         fc.curve_through(waist_side, hip_side, bulge=0.10, side=1.0)]),
        fc.Edge("hem", [fc.Line(hip_side, cf_bottom)]),
    ]
    internals = [
        fc.Internal("waist line", [fc.P(0.0, WAIST_Y), fc.P(max(BUST_Q, HIP_Q), WAIST_Y)],
                    kind="marking"),
    ]
    for r in range(1, rows):
        y = H * r / rows
        internals.append(fc.Internal(f"lattice-row-{r}", [fc.P(0.0, y), fc.P(W, y)],
                                     kind="marking"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.4, H * 0.12), fc.P(W * 0.4, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Lattice Corset Placement Guide",
    )
    pattern = fc.PatternSet("lattice-corset")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 350, "family": "am_fashion", "lane": 5,
        "panel_width_mm": round(W, 1), "panel_height_mm": round(H, 1),
        "bust_q_mm": round(BUST_Q, 1), "waist_q_mm": round(WAIST_Q, 1),
        "hip_q_mm": round(HIP_Q, 1), "waist_clamped": WAIST_CLAMPED,
        "tile_size_mm": tile_size, "tile_gap_mm": tile_gap, "wall_mm": wall,
        "field_cols": cols, "field_rows": rows,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "lattice field delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-lattice-panel)",
        "note": "the waist half is clamped below both the bust and hip so the hourglass "
                "never bulges out at the waist (an inverted cinch)",
    }
    return pattern


result = build()

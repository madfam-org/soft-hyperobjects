"""
Printed lattice-panel skirt — FC-400 rank #342, Lane 5 (am_fashion). Fashion Cabinet Cartridge.

A made-to-measure A-line skirt built from printed TPU lattice panels — an open tile-and-
bridge lattice that is rigid across the tile and flexes at the bridges, so the skirt holds
a sculptural bell while it moves. The lattice is Yantra4D territory (notion.hardware_ref →
tpu-lattice-panel); Fashion Cabinet owns the fashion: the skirt panel dimensions and the
lattice field (rows × cols) DERIVED from the panel so the tiling exactly fills the shape.

What this cartridge owns:
  - THE SKIRT PANEL placement guide: an A-line front/back panel (cut on the fold) sized
    from waist girth, hip girth, skirt length and the hem flare.
  - THE LATTICE FIELD: cols/rows derived from the panel and the tile+gap pitch — the exact
    numbers the tpu-lattice-panel solid tiles.

Solving and clamps. The waist and hip half-widths are DERIVED and FLOORED; the hem half is
the larger of the hip half and the waist half so the skirt never narrows below the hip.
The field cols/rows are floored at 1. Match the manifest params_map exactly.

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

waist_girth = float(PARAM(lambda: waist_girth, 780.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
skirt_length = float(PARAM(lambda: skirt_length, 560.0))
hem_flare = float(PARAM(lambda: hem_flare, 140.0))       # each side release at hem
tile_size = float(PARAM(lambda: tile_size, 26.0))
tile_gap = float(PARAM(lambda: tile_gap, 8.0))
wall = float(PARAM(lambda: wall, 1.4))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

waist_girth = max(560.0, min(waist_girth, 1400.0))
hip_girth = max(600.0, min(hip_girth, 1600.0))
skirt_length = max(300.0, min(skirt_length, 1100.0))
hem_flare = max(0.0, min(hem_flare, 360.0))
tile_size = max(10.0, min(tile_size, 70.0))
tile_gap = max(2.0, min(tile_gap, 30.0))
wall = max(0.6, min(wall, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

# Panel = the skirt front quarter (cut on fold, mirrored).
WAIST_HALF = max(80.0, waist_girth / 4.0)
HIP_HALF = max(WAIST_HALF, hip_girth / 4.0)             # never below the waist
HEM_HALF = HIP_HALF + hem_flare
H = max(200.0, skirt_length)
HIP_Y = H * 0.75                                        # hip level below the waist
# Panel width for the lattice field is the average width.
W = (WAIST_HALF + HEM_HALF) / 2.0
pitch = tile_size + tile_gap
cols = max(1, round(W / pitch))
rows = max(1, round(H / pitch))


def build():
    # A-line panel: waist top, side (waist->hip->hem), hem, centre fold.
    origin = fc.P(0.0, 0.0)                     # centre-front hem
    cf_top = fc.P(0.0, H)                       # centre-front waist
    waist_side = fc.P(WAIST_HALF, H)
    hip_side = fc.P(HIP_HALF, HIP_Y)
    hem_side = fc.P(HEM_HALF, 0.0)
    edges = [
        fc.Edge("guide", [fc.Line(origin, cf_top)]),       # sewn edge (centre front)
        fc.Edge("waist", [fc.Line(cf_top, waist_side)]),
        fc.Edge("side", [fc.Line(waist_side, hip_side), fc.Line(hip_side, hem_side)]),
        fc.Edge("hem", [fc.Line(hem_side, origin)]),
    ]
    internals = []
    for r in range(1, rows):
        y = H * r / rows
        internals.append(fc.Internal(f"lattice-row-{r}", [fc.P(0.0, y), fc.P(W, y)],
                                     kind="marking"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.4, H * 0.12), fc.P(W * 0.4, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="guide", mirror=True),
        label="Lattice-Panel Skirt Placement Guide",
    )
    pattern = fc.PatternSet("lattice-panel-skirt")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 342, "family": "am_fashion", "lane": 5,
        "panel_width_mm": round(W, 1), "panel_height_mm": round(H, 1),
        "tile_size_mm": tile_size, "tile_gap_mm": tile_gap, "wall_mm": wall,
        "field_cols": cols, "field_rows": rows,
        "waist_half_mm": round(WAIST_HALF, 1), "hip_half_mm": round(HIP_HALF, 1),
        "hem_half_mm": round(HEM_HALF, 1),
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "lattice field delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-lattice-panel)",
        "note": "cols/rows DERIVED from the panel and tile+gap pitch; the hem half is the "
                "larger of hip and waist so the skirt never narrows below the hip",
    }
    return pattern


result = build()

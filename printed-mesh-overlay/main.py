"""
Printed structural mesh overlay — FC-400 rank #352, Lane 5 (am_fashion). Fashion Cabinet.

A structural mesh overlay — a printed TPU lattice sheet laid over a base garment to add a
sculptural, semi-rigid second skin that catches light and holds a silhouette while the base
cloth moves underneath. The lattice mesh is Yantra4D territory (notion.hardware_ref →
tpu-lattice-panel); Fashion Cabinet owns the overlay FASHION: the overlay panel dimensions
(sized to the body region it covers) and the mesh field (rows × cols) DERIVED from the panel.

What this cartridge owns:
  - THE OVERLAY panel placement guide: a rectangular sheet sized from cover width and
    cover height (the body region it overlays), with a sewn perimeter edge.
  - THE MESH FIELD: cols/rows DERIVED from the panel and the tile+gap pitch.

Solving and clamps. The cover width and height are FLOORED; the field cols/rows are floored
at 1 so the mesh is never empty. Match the manifest params_map exactly.

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

cover_width = float(PARAM(lambda: cover_width, 420.0))    # width of the covered region
cover_height = float(PARAM(lambda: cover_height, 560.0))  # height of the covered region
corner_radius = float(PARAM(lambda: corner_radius, 60.0))  # rounded overlay corners
tile_size = float(PARAM(lambda: tile_size, 30.0))
tile_gap = float(PARAM(lambda: tile_gap, 10.0))
wall = float(PARAM(lambda: wall, 1.2))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

cover_width = max(150.0, min(cover_width, 900.0))
cover_height = max(150.0, min(cover_height, 1100.0))
corner_radius = max(0.0, min(corner_radius, 200.0))
tile_size = max(10.0, min(tile_size, 80.0))
tile_gap = max(2.0, min(tile_gap, 40.0))
wall = max(0.6, min(wall, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

W = max(120.0, cover_width)
H = max(120.0, cover_height)
# Corner radius clamped below half the smaller dimension so corners never cross.
R = max(0.0, min(corner_radius, min(W, H) / 2.0 - 10.0))
pitch = tile_size + tile_gap
cols = max(1, round(W / pitch))
rows = max(1, round(H / pitch))


def build():
    # Rounded rectangle overlay. Frame: x in [0,W], y in [0,H]. One perimeter edge (guide)
    # plus rounded corners as short arcs.
    if R > 1.0:
        edges = [
            fc.Edge("guide", [
                fc.Line(fc.P(R, 0.0), fc.P(W - R, 0.0)),
                fc.curve_through(fc.P(W - R, 0.0), fc.P(W, R), bulge=0.12, side=-1.0),
                fc.Line(fc.P(W, R), fc.P(W, H - R)),
                fc.curve_through(fc.P(W, H - R), fc.P(W - R, H), bulge=0.12, side=-1.0),
                fc.Line(fc.P(W - R, H), fc.P(R, H)),
                fc.curve_through(fc.P(R, H), fc.P(0.0, H - R), bulge=0.12, side=-1.0),
                fc.Line(fc.P(0.0, H - R), fc.P(0.0, R)),
                fc.curve_through(fc.P(0.0, R), fc.P(R, 0.0), bulge=0.12, side=-1.0),
            ]),
        ]
    else:
        edges = [
            fc.Edge("guide", [
                fc.Line(fc.P(0.0, 0.0), fc.P(W, 0.0)),
                fc.Line(fc.P(W, 0.0), fc.P(W, H)),
                fc.Line(fc.P(W, H), fc.P(0.0, H)),
                fc.Line(fc.P(0.0, H), fc.P(0.0, 0.0)),
            ]),
        ]
    internals = []
    for r in range(1, rows):
        y = H * r / rows
        internals.append(fc.Internal(f"mesh-row-{r}", [fc.P(0.0, y), fc.P(W, y)],
                                     kind="marking"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.5, H * 0.12), fc.P(W * 0.5, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Structural Mesh Overlay Placement Guide",
    )
    pattern = fc.PatternSet("printed-mesh-overlay")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 352, "family": "am_fashion", "lane": 5,
        "panel_width_mm": round(W, 1), "panel_height_mm": round(H, 1),
        "corner_radius_mm": round(R, 1),
        "tile_size_mm": tile_size, "tile_gap_mm": tile_gap, "wall_mm": wall,
        "field_cols": cols, "field_rows": rows,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "structural mesh delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-lattice-panel)",
        "note": "cols/rows DERIVED from the panel and tile+gap pitch, floored at 1; the "
                "corner radius is clamped below half the smaller dimension so corners never "
                "cross",
    }
    return pattern


result = build()

"""
Lattice Armor Panel — Fashion Cabinet Notion Cartridge (Yantra4D-bridged printed textile).

The tile-and-bridge lattice itself is Yantra4D territory (CadQuery; see the manifest's
notion.hardware_ref → tpu-lattice-panel). What Fashion Cabinet owns is the fashion — the
finished panel dimensions, the tile grid derived from the panel size, and the 2-D
placement guide for the sewn edge where the printed panel joins the garment.

One material identity — Bambu TPU 95A (`tpu-panel-impreso` class) — spans this notion and
that solid, so the same panel is a Fashion Cabinet fabric and a Yantra4D object at once.

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
panel_width_mm  = float(PARAM(lambda: panel_width_mm, 180.0))
panel_height_mm = float(PARAM(lambda: panel_height_mm, 260.0))
tile_size       = float(PARAM(lambda: tile_size, 18.0))
tile_gap        = float(PARAM(lambda: tile_gap, 3.0))
seam_allowance  = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest ranges) ──────────────────────────────────────
panel_width_mm  = max(40.0, min(panel_width_mm, 300.0))
panel_height_mm = max(40.0, min(panel_height_mm, 700.0))
tile_size       = max(6.0, min(tile_size, 60.0))
tile_gap        = max(1.0, min(tile_gap, 12.0))
seam_allowance  = max(0.0, min(seam_allowance, 25.0))

# The tile grid the printed panel will fill (must match the manifest params_map:
# cols = round(panel_width_mm / (tile_size + tile_gap)), rows likewise for height).
pitch = tile_size + tile_gap
cols = max(1, round(panel_width_mm / pitch))
rows = max(1, round(panel_height_mm / pitch))

W = panel_width_mm
H = panel_height_mm


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, H)
    top_right    = fc.P(W, H)
    bottom_right = fc.P(W, 0.0)

    edges = [
        fc.Edge("guide",  [fc.Line(origin, top_left)]),   # sewn panel edge
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("side",   [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    # Faint tile-grid markings (orientation only; the printed panel carries the tiles).
    internals = []
    for c in range(1, cols):
        x = W * c / cols
        internals.append(fc.Internal(f"tile-col-{c}", [fc.P(x, 0.0), fc.P(x, H)], kind="marking"))
    for r in range(1, rows):
        y = H * r / rows
        internals.append(fc.Internal(f"tile-row-{r}", [fc.P(0.0, y), fc.P(W, y)], kind="marking"))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.5, H * 0.12), fc.P(W * 0.5, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Lattice Panel Placement Guide",
    )

    pattern = fc.PatternSet("lattice-armor-panel")
    pattern.add(piece)
    pattern.metadata = {
        "panel_width_mm": round(W, 1),
        "panel_height_mm": round(H, 1),
        "tile_size_mm": tile_size,
        "tile_gap_mm": tile_gap,
        "grid_cols": cols,
        "grid_rows": rows,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "tile-and-bridge lattice delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-lattice-panel)",
    }
    return pattern


result = build()

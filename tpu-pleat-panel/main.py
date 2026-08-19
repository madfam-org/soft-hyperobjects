"""
TPU Pleat Panel — Fashion Cabinet Notion Cartridge (Yantra4D-bridged printed textile).

The pleated wall itself is Yantra4D territory (CadQuery; see the manifest's
notion.hardware_ref → tpu-pleat-panel). What Fashion Cabinet owns is the fashion — the
finished panel dimensions, the pleat count derived from the panel height, and the 2-D
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
panel_width_mm  = float(PARAM(lambda: panel_width_mm, 200.0))
panel_height_mm = float(PARAM(lambda: panel_height_mm, 320.0))
pleat_depth     = float(PARAM(lambda: pleat_depth, 12.0))
wall            = float(PARAM(lambda: wall, 1.2))
seam_allowance  = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest ranges) ──────────────────────────────────────
panel_width_mm  = max(40.0, min(panel_width_mm, 300.0))
panel_height_mm = max(40.0, min(panel_height_mm, 800.0))
pleat_depth     = max(3.0, min(pleat_depth, 40.0))
wall            = max(0.6, min(wall, 4.0))
seam_allowance  = max(0.0, min(seam_allowance, 25.0))

# Pleat count the printed panel will fill (must match the manifest params_map:
# pleats = round(panel_height_mm / (2 * pleat_depth))).
pleats = max(1, round(panel_height_mm / (2.0 * pleat_depth)))

W = panel_width_mm
H = panel_height_mm


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, H)
    top_right    = fc.P(W, H)
    bottom_right = fc.P(W, 0.0)

    edges = [
        # The guide edge is the sewn panel edge (where the printed panel meets the garment).
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("side",   [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    # Horizontal marking lines at each pleat crease (orientation only; the printed
    # panel carries the real folds).
    internals = []
    for i in range(1, pleats):
        y = H * i / pleats
        internals.append(fc.Internal(
            f"pleat-crease-{i}", [fc.P(0.0, y), fc.P(W, y)], kind="marking"))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.5, H * 0.12), fc.P(W * 0.5, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Pleat Panel Placement Guide",
    )

    pattern = fc.PatternSet("tpu-pleat-panel")
    pattern.add(piece)
    pattern.metadata = {
        "panel_width_mm": round(W, 1),
        "panel_height_mm": round(H, 1),
        "pleat_depth_mm": pleat_depth,
        "wall_mm": wall,
        "pleats": pleats,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "pleated wall delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-pleat-panel)",
    }
    return pattern


result = build()

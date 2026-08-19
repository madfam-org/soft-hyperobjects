"""
Articulated Scale Mail — Fashion Cabinet Notion Cartridge (Yantra4D-bridged printed textile).

The scale-and-neck field itself is Yantra4D territory (CadQuery; see the manifest's
notion.hardware_ref → tpu-scale-mail). What Fashion Cabinet owns is the fashion — the
finished panel dimensions, the scale field derived from the panel size, and the 2-D
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
panel_height_mm = float(PARAM(lambda: panel_height_mm, 280.0))
scale_size      = float(PARAM(lambda: scale_size, 22.0))
overlap         = float(PARAM(lambda: overlap, 0.45))
seam_allowance  = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest ranges) ──────────────────────────────────────
panel_width_mm  = max(40.0, min(panel_width_mm, 300.0))
panel_height_mm = max(40.0, min(panel_height_mm, 700.0))
scale_size      = max(8.0, min(scale_size, 60.0))
overlap         = max(0.0, min(overlap, 0.7))
seam_allowance  = max(0.0, min(seam_allowance, 25.0))

# The scale field the printed panel will fill (must match the manifest params_map:
# cols = round(panel_width_mm / scale_size),
# rows = round(panel_height_mm / (scale_size * 1.3 * (1 - overlap)))).
scale_h_mm = scale_size * 1.3
cols = max(1, round(panel_width_mm / scale_size))
rows = max(1, round(panel_height_mm / (scale_h_mm * (1.0 - overlap))))

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

    # Faint scale-row markings (orientation only; the printed panel carries the scales).
    internals = []
    for r in range(1, rows):
        y = H * r / rows
        internals.append(fc.Internal(f"scale-row-{r}", [fc.P(0.0, y), fc.P(W, y)], kind="marking"))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.5, H * 0.12), fc.P(W * 0.5, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Scale Mail Placement Guide",
    )

    pattern = fc.PatternSet("articulated-scale-mail")
    pattern.add(piece)
    pattern.metadata = {
        "panel_width_mm": round(W, 1),
        "panel_height_mm": round(H, 1),
        "scale_size_mm": scale_size,
        "overlap": overlap,
        "field_cols": cols,
        "field_rows": rows,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "scale-and-neck field delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-scale-mail)",
    }
    return pattern


result = build()

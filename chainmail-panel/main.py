"""
Chainmail Panel — Fashion Cabinet Notion Cartridge (Yantra4D-bridged printed textile).

The flexible ring lattice itself is Yantra4D territory (CadQuery; see the manifest's
`notion.hardware_ref` → `tpu-chainmail-panel`). What Fashion Cabinet owns is the
fashion semantics — the finished panel's dimensions, the sewable-edge placement guide,
and the cut planning against the printed panel's bed-bound width — and the 2D
fabrication output: a PANEL PLACEMENT GUIDE that shows the finished panel outline, its
tape-bound sew edge (the `panel_edge` interface), and the ring grid the print will fill
so the maker can size the Yantra4D panel to the garment.

One material identity — Bambu TPU 95A (`tpu-panel-impreso`) — spans this card and that
solid, so the same panel is a Fashion Cabinet fabric and a Yantra4D object at once.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `panel_width_mm`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr —
    they are not in the sandbox's allowed builtins.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
panel_width_mm  = float(PARAM(lambda: panel_width_mm, 200.0))   # finished width (≤ bed)
panel_height_mm = float(PARAM(lambda: panel_height_mm, 300.0))  # finished height
ring_id         = float(PARAM(lambda: ring_id, 9.0))            # ring inner diameter
wire_d          = float(PARAM(lambda: wire_d, 2.4))             # ring wire cross-section
seam_allowance  = float(PARAM(lambda: seam_allowance, 10.0))    # tape-bound sew edge

# ── Clamps (mirror the manifest ranges) ──────────────────────────────────────
panel_width_mm  = max(60.0, min(panel_width_mm, 250.0))
panel_height_mm = max(60.0, min(panel_height_mm, 600.0))
ring_id         = max(4.0, min(ring_id, 30.0))
wire_d          = max(1.2, min(wire_d, 6.0))
seam_allowance  = max(0.0, min(seam_allowance, 25.0))

# ── Weave grid the printed panel will fill (must match tpu-chainmail-panel's
# params_map: cols = round(width / (ring_id + wire_d)),
#             rows = round(height / ((ring_id + 2*wire_d) * 0.62))) ────────────
ring_od  = ring_id + 2.0 * wire_d
cols     = max(1, round(panel_width_mm / (ring_id + wire_d)))
rows     = max(1, round(panel_height_mm / (ring_od * 0.62)))


def _grid_markings():
    """Faint marking lines showing the ring-grid the print fills — orientation only,
    so the maker can see how the weave lands on the panel. Not cut lines."""
    marks = []
    # Vertical column guides.
    for c in range(1, cols):
        x = panel_width_mm * c / cols
        marks.append(fc.Internal(
            f"weave-col-{c}",
            [fc.P(x, 0.0), fc.P(x, panel_height_mm)],
            kind="marking",
        ))
    # Horizontal row guides.
    for r in range(1, rows):
        y = panel_height_mm * r / rows
        marks.append(fc.Internal(
            f"weave-row-{r}",
            [fc.P(0.0, y), fc.P(panel_width_mm, y)],
            kind="marking",
        ))
    return marks


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, panel_height_mm)
    top_right    = fc.P(panel_width_mm, panel_height_mm)
    bottom_right = fc.P(panel_width_mm, 0.0)

    edges = [
        # The whole perimeter is the sewable panel edge (`panel_edge` interface):
        # a tape-bound seam where the printed panel joins the garment.
        fc.Edge("left",   [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("right",  [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(
            fc.P(panel_width_mm * 0.5, panel_height_mm * 0.12),
            fc.P(panel_width_mm * 0.5, panel_height_mm * 0.88),
        ),
        internals=_grid_markings(),
        cut=fc.CutSpec(quantity=1),
        label="Chainmail Panel Placement Guide",
    )

    pattern = fc.PatternSet("chainmail-panel")
    pattern.add(piece)
    pattern.metadata = {
        "panel_width_mm": round(panel_width_mm, 1),
        "panel_height_mm": round(panel_height_mm, 1),
        "ring_id_mm": ring_id,
        "wire_d_mm": wire_d,
        "weave_cols": cols,
        "weave_rows": rows,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "flexible ring lattice delegated to Yantra4D "
                    "(see manifest notion.hardware_ref → tpu-chainmail-panel)",
    }
    return pattern


result = build()

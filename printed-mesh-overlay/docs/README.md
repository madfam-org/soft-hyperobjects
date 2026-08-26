# Printed Structural Mesh Overlay

A structural mesh overlay — a printed TPU **lattice sheet** laid over a base garment to add
a sculptural, semi-rigid second skin that catches light and holds a silhouette while the
base cloth moves underneath.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The lattice mesh is Yantra4D territory (`notion.hardware_ref → tpu-lattice-panel`). Fashion
Cabinet owns the overlay panel (sized from cover width and height) and the **mesh field
derived from it**.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 1 | Rounded-rectangle overlay sheet; mesh rows marked; perimeter is the sewn edge. |

## Solving and clamps

The cover width and height are floored; the corner radius is clamped **below half the
smaller dimension** so the corners never cross. The field `cols`/`rows` are derived and
floored at 1.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-lattice-panel`**, mapping `tile`, `gap`, `cols`, `rows`. The
flange params are driven by garment params in the `panel_edge` interface, so the
**dimensional handshake** holds.

## Parameters

`cover_width`, `cover_height`, `corner_radius`, `tile_size`, `tile_gap`, `wall`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

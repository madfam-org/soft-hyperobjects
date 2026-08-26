# AM Printed-Panel Tee

A T-shirt whose front carries a printed TPU lattice panel — a tile-and-bridge lattice (rigid
across the tile, flexing at the bridges) set as a structured window into a soft jersey tee.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, am_fashion).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 1 | Carries the clamped lattice window and the tile-field guide. |
| `back` | 1 | Plain jersey back. |
| `sleeve` | 2 mirrored | Solved cap. |

## Solving and clamps

The lattice **field** (cols × rows) is derived from the window and the tile+gap pitch,
**floored at 1** so a large tile against a small window never yields a zero count. The
sleeve cap is a **solved bow** to the measured armhole. The lattice window is **clamped**
inside the front panel so an over-large window never runs off the edge and folds the piece.
Verified at defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

The two `shoulder`s and the two `side`s (front ↔ back). The sleeve cap sets into the measured
armscye (declared as an interface).

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-lattice-panel`**, mapping `tile → tile_size`, `gap →
tile_gap`, and `cols` / `rows` derived from the window and pitch. These are the panel's
**flange** (sewn-edge) params, so the `lattice_panel` interface lists every driving param
(`panel_width`, `panel_height`, `tile_size`, `tile_gap`) — the dimensional handshake holds.

## Parameters

`chest_girth`, `body_length`, `shoulder_width`, `armhole_depth`, `sleeve_length`,
`neck_width`, `panel_width`, `panel_height`, `tile_size`, `tile_gap`, `ease`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

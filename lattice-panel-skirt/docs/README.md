# Printed Lattice-Panel Skirt

A made-to-measure A-line skirt built from printed TPU **lattice panels** — an open
tile-and-bridge lattice, rigid across the tile and flexing at the bridges, so the skirt
holds a sculptural bell while it moves.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The lattice field is Yantra4D territory (`notion.hardware_ref → tpu-lattice-panel`). Fashion
Cabinet owns the A-line skirt panel (sized from waist, hip, length and hem flare) and the
**lattice field derived from the panel**. One material — **Bambu TPU 95A** — is both fabric
and solid.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 1 on fold | A-line front/back panel; lattice rows marked. |

## Solving and clamps

The hip half-width is floored at the waist half; the hem half is `hip_half + flare`, so the
skirt **never narrows below the hip**. The field is `cols = round(avg_width / (tile+gap))`,
`rows = round(length / (tile+gap))`, each floored at 1 — the exact `params_map` expressions.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-lattice-panel`**, mapping `tile`, `gap`, `cols`, `rows`. All
four are `flange` params of the solid, and the garment's `panel_edge` interface is driven
by the same garment params (`waist_girth`, `hip_girth`, `skirt_length`, `hem_flare`,
`tile_size`, `tile_gap`), so the **dimensional handshake** holds.

## Parameters

`waist_girth`, `hip_girth`, `skirt_length`, `hem_flare`, `tile_size`, `tile_gap`, `wall`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

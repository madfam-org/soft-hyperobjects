# Printed Lattice Corset

A corset built from printed TPU **lattice panels** — an open tile-and-bridge lattice rigid
enough to shape the waist yet flexing at the bridges to breathe, printed instead of boned.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The lattice field is Yantra4D territory (`notion.hardware_ref → tpu-lattice-panel`). Fashion
Cabinet owns the hourglass panel (sized from bust/waist/hip girths, torso length, waist
position and cinch) and the **lattice field derived from it**.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 2 mirrored | Hourglass panel (under-bust → waist → hip); lattice rows and waist line marked. |

## Solving and clamps

The waist half-width is derived (`waist_girth/4 − cinch/2`) and **clamped below both the
bust and hip halves** so the hourglass never bulges out at the waist (an inverted cinch).
The field `cols`/`rows` are derived and floored at 1.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-lattice-panel`**, mapping `tile`, `gap`, `cols`, `rows`. The
flange params are driven by garment params in the `panel_edge` interface, so the
**dimensional handshake** holds.

## Parameters

`bust_girth`, `waist_girth`, `hip_girth`, `torso_length`, `waist_position`, `cinch`,
`tile_size`, `tile_gap`, `wall`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

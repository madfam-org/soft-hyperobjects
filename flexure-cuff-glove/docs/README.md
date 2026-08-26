# Printed Flexure-Cuff Glove

A glove whose wrist is a printed TPU **flexure cuff** — a slotted living-hinge band that
flexes with the wrist and springs back, printed rather than elasticated.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The flexure cuff is Yantra4D territory (`notion.hardware_ref → tpu-flexure-cuff`). Fashion
Cabinet owns the glove-back panel (sized from hand length and width) and the cuff
circumference **derived from the wrist girth + ease** so the printed cuff matches the sewn
wrist opening.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 2 mirrored | Hand-back panel; wrist edge is the sewn cuff seam; rounded finger top. |

## Solving and clamps

The hand width and length are floored; the cuff circumference (`wrist_girth + cuff_ease`) is
floored at 120 mm; the wrist edge is drafted at half the cuff circumference. The outline
stays closed even at the wide-wrist / narrow-hand extreme.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-flexure-cuff`**, mapping `cuff_circum → wrist_girth +
cuff_ease`, `cuff_height`, `wall`. All three are flange params driven by garment params in
the `wrist_seam` interface, so the **dimensional handshake** holds.

## Parameters

`hand_length`, `hand_width`, `wrist_girth`, `cuff_ease`, `cuff_height`, `wall`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

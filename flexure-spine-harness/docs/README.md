# Flexure-Spine Fashion Harness

A body harness whose back is a printed TPU **flexure band** running down the spine — a
slotted living-hinge strip that curves with the back and springs back.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The flexure band is Yantra4D territory (`notion.hardware_ref → tpu-flexure-cuff`, used here
as a **straight spine band** rather than a wrap). Fashion Cabinet owns the strap panel
(sized from shoulder width, back length and strap width) and the spine band length derived
from the back length.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 2 mirrored | Back panel with a central spine channel (the sewn band edge) and a shoulder strap. |

## Solving and clamps

The strap width is floored **below half the shoulder width** so the two straps clear the
centre spine; the spine half-width is floored. The spine band length is derived from the
back length.

## Declared seams

`placement-guide.guide ↔ placement-guide.guide` — the two mirrored halves join at the centre
spine channel, where the printed band bridges.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-flexure-cuff`**, mapping `cuff_circum → back_length`,
`cuff_height → spine_width`, `wall`. All three are flange params driven by garment params in
the `spine_seam` interface, so the **dimensional handshake** holds.

## Parameters

`shoulder_width`, `back_length`, `strap_width`, `spine_width`, `wall`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

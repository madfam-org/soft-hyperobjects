# Articulated Hinge-Collar Capelet

A short shoulder cape that stands on an articulated printed TPU **hinge collar** — a
living-hinge band at the neck that folds crisply where a sewn collar would only crease.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The hinge collar is Yantra4D territory (`notion.hardware_ref → tpu-hinge-collar`). Fashion
Cabinet owns the cape drafted as a **half-annulus** (inner ring = neckline, outer ring =
hem sweep) and the collar length derived from the neckline.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `cape` | 2 on fold | Half-annulus; inner ring is the neck seam, outer is the hem sweep; joined at centre back. |

## Solving and clamps

Both rings use the **corrected polygon radius** (`r = C/(2n·sin(π/n))`) so drafted
perimeters equal circumferences. The inner (neck) radius is floored below the outer (hem)
radius so the annulus never inverts; the cape length and collar length are floored.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-hinge-collar`**, mapping `collar_len → neck_girth +
collar_ease`, `band_h`, `wall`. All three are flange params driven by garment params in the
`neck_seam` interface, so the **dimensional handshake** holds.

## Parameters

`neck_girth`, `collar_ease`, `cape_length`, `band_h`, `wall`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

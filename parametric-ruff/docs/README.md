# Parametric Printed Ruff Collar

The Elizabethan ruff, reimagined as a printed TPU **pleat panel** — a long figure-of-eight
pleated band that holds its cartwheel and folds flat to pack.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The pleat field is Yantra4D territory (`notion.hardware_ref → tpu-pleat-panel`). Fashion
Cabinet owns the ruff band length (the outer run = `neck_girth × fullness`) and the **pleat
count derived from it**.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 1 | Long pleated band; lower edge is the gathered neck seam; pleat lines marked. |

## Solving and clamps

The band length is derived (`neck_girth × fullness`) and floored at 600 mm; the pleat count
`= round(band_len / pleat_pitch)` is floored at **2** so it is genuinely a ruff; the depth is
floored.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-pleat-panel`**, mapping `pleats`, `pleat_depth`,
`pleat_pitch`, `panel_width`, `wall`. The flange params are driven by garment params in the
`neck_seam` interface, so the **dimensional handshake** holds.

## Parameters

`neck_girth`, `fullness`, `ruff_depth`, `pleat_pitch`, `pleat_depth`, `wall`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

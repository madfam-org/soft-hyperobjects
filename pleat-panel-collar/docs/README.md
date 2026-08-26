# Printed Pleat-Panel Collar

A standing collar built from a printed TPU **pleat panel** — accordion pleats printed into
the flat panel that spring the collar up around the neck and let it fold flat.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The pleat field is Yantra4D territory (`notion.hardware_ref → tpu-pleat-panel`). Fashion
Cabinet owns the collar band (sized from neck girth + ease and the stand height) and the
**pleat count derived from the collar length and pitch**. One material — **Bambu TPU 95A** —
is both fabric and solid.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 1 | Collar band; pleat lines marked; lower edge is the neck seam. |

## Solving and clamps

The collar length is derived (`neck_girth + collar_ease`) and floored at 200 mm; the pleat
count `= round(collar_len / pleat_pitch)` is floored at 1 so the panel is never flat.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-pleat-panel`**, mapping `pleats`, `pleat_depth`,
`pleat_pitch`, `panel_width`, `wall`. The flange params (`pleats`, `pleat_pitch`,
`panel_width`, `wall`) are driven by garment params in the `neck_seam` interface, so the
**dimensional handshake** holds.

## Parameters

`neck_girth`, `collar_ease`, `stand_height`, `pleat_pitch`, `pleat_depth`, `wall`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Printed Chainmail Drape Top

A draped top made of printed TPU **chainmail** — interlocked printed rings that fall and
pool like woven maille but come off the print bed already linked.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The chainmail field is Yantra4D territory (`notion.hardware_ref → tpu-chainmail-panel`).
Fashion Cabinet owns the drape panel (sized from bust girth, top length and drape ease) and
the **ring field derived from the panel and the ring pitch** (`ring_id + wire_d`).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 1 on fold | Wide front panel from shoulder to low hem; ring rows marked. |

## Solving and clamps

Panel width `= bust_girth/4 + drape_ease/2` (includes the pooling drape), floored; height
floored. The field is `cols = round(W / (ring_id+wire_d))`, `rows = round(H /
(ring_id+wire_d))`, each floored at 1.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-chainmail-panel`**, mapping `cols`, `rows`, `ring_id`,
`wire_d`, `clearance`. The flange params (`rows`, `cols`, `ring_id`, `wire_d`) are driven by
garment params in the `panel_edge` interface, so the **dimensional handshake** holds.

## Parameters

`bust_girth`, `top_length`, `drape_ease`, `ring_id`, `wire_d`, `clearance`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

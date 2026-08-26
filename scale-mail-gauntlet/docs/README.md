# Printed Scale-Mail Gauntlet

An armoured gauntlet — forearm to knuckles — clad in a printed TPU **scale-mail** field,
the scales articulating over the wrist and the back of the hand.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The scale field is Yantra4D territory (`notion.hardware_ref → tpu-scale-mail`). Fashion
Cabinet owns the tapered forearm-to-hand panel (sized from forearm length, elbow girth and
hand width) and the **scale field derived from it**.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 2 mirrored | Tapered forearm→knuckle panel; scale rows marked; left edge is the sewn seam. |

## Solving and clamps

The knuckle half-width is clamped **never wider than the elbow half** so the taper never
inverts. The scale field `cols`/`rows` are derived from the panel size and floored at 1.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-scale-mail`**, mapping `scale_w`, `scale_h`, `overlap`,
`cols`, `rows`. The flange params are driven by garment params in the `panel_edge`
interface, so the **dimensional handshake** holds.

## Parameters

`forearm_length`, `elbow_girth`, `hand_width`, `scale_size`, `overlap`, `wall`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

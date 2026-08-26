# Printed Scale-Mail Bodice

A made-to-measure bodice whose whole face is a **printed TPU scale-mail field** —
independently articulating scales that protect and move.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion, the printed-textile
shelf). Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The scale field is Yantra4D territory (`notion.hardware_ref → tpu-scale-mail`). Fashion
Cabinet owns the **fashion**: the bodice-front placement guide (sized from bust girth,
bodice length and the neck/armhole scoops) and the **scale field derived from the panel**
so the print exactly fills the sewn shape. One material — **Bambu TPU 95A**
(`tpu-panel-impreso`) — is both a Fashion Cabinet fabric and a Yantra4D solid.

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 1 on fold | Shaped bodice front (neck, armhole, side, waist, CF); scale rows marked. |

## Solving and clamps

Panel width `= bust_girth/4` and height `= bodice_length`, both floored at 120 mm. The
neck and armhole scoops are clamped inside the panel so no corner inverts. The scale field
is `cols = round(W / scale_size)`, `rows = round(H / (scale_size·1.3·(1−overlap)))`, each
floored at 1 so the print is never empty — the exact expressions the `params_map` feeds
the solid.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-scale-mail`**, mapping `scale_w`, `scale_h`, `overlap`,
`cols`, `rows`. `tpu-scale-mail` declares a `flange` sewn edge driven by those params; the
garment's `panel_edge` interface is driven by `bust_girth`, `bodice_length`, `scale_size`,
`overlap`, so the **dimensional handshake** holds — the same dimensions size both the
garment's sewn edge and the printed panel's.

## Parameters

`bust_girth`, `bodice_length`, `neck_scoop`, `armhole_scoop`, `scale_size`, `overlap`,
`wall`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

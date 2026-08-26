# Brushed Mohair Cardigan

A soft, boxy brushed-mohair cardigan: a **round-neck drop-shoulder** body that opens down
the centre front with a button band and a ribbed round neckband.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 2 mirrored | Opens; button band outside centre front; drop-shoulder armhole; buttonholes marked. |
| `back` | 1 on fold | Drop-shoulder armhole. |
| `sleeve` | 2 | Straight head solved to the armhole length. |
| `neckband` / `cuff` / `hem_band` | 1 / 2 / 1 | Rib bands, double-height, folded. |

## Solving and clamps

Shoulder run derived and **floored at 45 mm**; shoulder slope capped at `0.45 ×
armhole_depth` (back-neck-rise clamp lesson). Sleeve head solved to the armhole length,
biceps widened so the crown is never degenerate. Neckband length solved from the measured
neckline and floored. Buttonhole slit sized from `button_ligne` (1 ligne ≈ 0.635 mm).
Signed knit ease, **positive** default.

## Declared seams

Armholes ↔ sleeve head edges, `front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`,
sleeve underarm to itself.

## Cross-commons bridge

`notion.hardware_ref` → **`sew-through-button`**, mapping `button_ligne → button_ligne` and
`thickness → max(3, seam_allowance)`. `sew-through-button` declares a `flange` interface
driven by `button_ligne`; the garment's `front_placket` interface is also driven by
`button_ligne`, so the **dimensional handshake** is satisfied — the same size flows to both
the garment's placket and the button. The buttonholes appear as `drill`-kind internals.

## Parameters

`chest_girth`, `body_length`, `neck_girth`, `sleeve_length`, `knit_ease`, `armhole_depth`,
`front_neck_drop`, `shoulder_slope`, `band_width`, `button_count`, `button_ligne`,
`neckband_ratio`, `neckband_width`, `cuff_ratio`, `hemband_ratio`, `rib_height`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

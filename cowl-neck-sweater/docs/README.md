# Cowl-Neck Sweater

A drop-shoulder knit pullover whose feature is a deep draped **cowl** — a wide, soft tube
much longer than the neckline it sews to, falling in folds at the front.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` / `back` | 1 on fold each | Drop-shoulder body, scooped neck. |
| `sleeve` | 2 | Straight head solved to the armhole length. |
| `cowl` | 1 | Trapezoid: sewn edge = neckline, flared top folds into the drape. |
| `cuff` / `hem_band` | 2 / 1 | Rib bands, double-height, folded. |

## Solving and clamps

The shoulder run is derived (quarter width less half neck) and **floored at 45 mm**; the
shoulder slope is capped at `0.45 × armhole_depth` so the neck point can never dip below
the underarm (the back-neck-rise clamp lesson). The sleeve head is solved to the armhole
length, biceps widened when needed so the crown is never degenerate. The cowl's sewn edge
is solved from the measured neckline (`2×front.neck + 2×back.neck`), floored so it never
goes negative; its flared top is `cowl_flare ×` that. Signed negative knit ease with a
floored draft girth.

## Declared seams

Armholes ↔ sleeve head edges, `front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`,
sleeve underarm to itself, and `cowl.neck_seam ↔` the full neckline.

## Hardware

**None** — a cowl pullover has no closure.

## Parameters

`chest_girth`, `body_length`, `neck_girth`, `sleeve_length`, `knit_ease`, `armhole_depth`,
`front_neck_drop`, `shoulder_slope`, `cowl_drop`, `cowl_flare`, `cuff_ratio`,
`hemband_ratio`, `rib_height`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

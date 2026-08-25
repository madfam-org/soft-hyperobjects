# House Slipper

A soft indoor slipper in the classic **three-part cut**: a **vamp** over the toes, a
**sole-line upper** — the quarters, cut on the fold at centre back and running round past
the heel — and a folded **collar band** binding the foot opening.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 4 — footwear soft goods). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Curved toe edge, two sides, a curved `join` the quarters sew to. |
| `sole_upper` | 1 **on fold** (centre back), mirrored | Sole line below, collar line above, a solved `join` at the front. |
| `collar` | 1 | Flat strip, twice the finished width, folded lengthwise when sewn. |

Cut all three again for the second slipper.

## Sizing — sized, not measured

ISO 8559, as vendored in `packages/schemas/body-measurements.schema.json`, declares **no
foot landmark codes**. Rather than invent one, this cartridge is honestly **sized**: a
discrete `size` select (S/M/L/XL) maps to a foot length and ball girth in millimetres
inside the script. No parameter carries a `measurement` block.

## Solving, and why the quarters take their height from the join

The quarters are cut **on the fold**, so their two mirrored `join` edges together sew to
the vamp's single `join`. Each is therefore solved to **half** the vamp join by bisecting
a Bézier bulge until the arc length matches.

A solved arc must always be **longer than its own chord**. The quarter panel height *is*
that chord, so the height is capped by the join budget (`half_join * 0.86`) rather than
set independently — the first draft set it from `collar_width` and a short-vamp,
wide-collar combination made the chord outrun the target, which the solver correctly
refused to draft. Clamping instead of raising keeps every slider combination buildable: a
short vamp simply yields shallower quarters. The effective height is reported in
`metadata.solved.quarter_height_mm`.

## Declared seams

| Side A | Side B | Note |
| :-- | :-- | :-- |
| `vamp.join` | `sole_upper.join` + `sole_upper.join` | The on-fold piece contributes both mirrored edges. |
| `collar.attach` | `sole_upper.collar_line` ×2 | Ease = `2 × seam_allowance`, the band's own joins. |

## Cross-commons bridge

**None.** The index row for rank 228 asks for `pattern` only — a house slipper is
all-soft-goods, with no hardware to bridge.

## Parameters

`size`, `vamp_length`, `collar_width`, `foot_ease`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

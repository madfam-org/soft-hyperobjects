# Denim Chore Jacket

The boxy denim work jacket (chore coat / *bleu de travail*): a straight front with a button
placket and patch pockets, a straight back, a set-in sleeve and a band collar, with felled
seams and 7 mm twin-needle gold topstitch throughout.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, denim).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 2 mirrored | Placket extension, button run, patch-pocket placement, rivet. |
| `back` | 1 | Straight box, higher round CB neck, yoke line. |
| `sleeve` | 2 mirrored | Solved cap; plain cuff. |
| `collar` | 1 | Band cut to the measured neckline. |
| `patch_pocket` | 2 | Rivets at the top corners. |

## Solving and clamps

The sleeve cap is a **solved bow** whose length equals the measured front + back armhole, so
it sets in without easing a mismatch. The band collar is cut to the **measured** neckline.
The shoulder tip and quarter-chest are clamped so a big-ease or small-body request never
draws a negative-width piece the kernel would CCW-normalize into a healthy-looking sliver.
Verified at defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

`front.shoulder ↔ back.shoulder`, `front.side ↔ back.side`, and `collar.lower` against the
four summed neck edges (declared as ease). The sleeve cap sets into the measured armscye
(declared as an interface).

## Cross-commons bridge

`notion.hardware_ref` → **`rivet`**, mapping the cap height, bore and burr from `rivet_cap`.
The rivet's sewn-edge params (`cap_dia`, `post_dia`, `post_h`) are **left unmapped** — a
rivet is set through a drilled hole, no sewn seam, so no dimensional handshake is owed.

## Parameters

`chest_girth`, `body_length`, `shoulder_width`, `armhole_depth`, `sleeve_length`,
`neck_width`, `back_neck_rise`, `placket_width`, `rivet_cap`, `ease`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

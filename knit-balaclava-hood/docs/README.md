# Knit Balaclava Hood

A close-fitting knit balaclava: two side panels wrapping from the face opening over the ear
to the centre back, plus a crown-to-nape gore, with ribbed face and neck bands.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, knitwear).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `side` | 2 mirrored | Face-opening scoop, ear ease, centre-back seam. |
| `gore` | 1 | Symmetric solved lens; sews to both crown edges. |
| `face_band` | 1 | Ribbed rectangle cut to the measured face opening. |

## Solving and clamps

The gore is a **symmetric lens centred on x=0** — never a hairline sliver — whose chord is
**bisected** so each bowed edge measures the side panel's crown edge, and it sews in flush.
The face opening height is **clamped** under the head-arc so an over-tall request never eats
past the crown and collapses the side panel above the opening into a self-crossing outline.
Panel widths carry a **floored** stretch factor (negative ease). Verified at defaults,
all-min, all-max, and every parameter swung to each bound.

## Declared seams

`side.crown ↔ gore.side_a` (solved to a near-zero ease), and the two side panels join at
`side.cb ↔ side.cb` (centre back).

## Cross-commons bridge

None — a pull-on knit balaclava.

## Parameters

`head_girth`, `head_height`, `neck_depth`, `face_width`, `face_height`, `stretch_factor`,
`band_depth`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

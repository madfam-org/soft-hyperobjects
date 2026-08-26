# Welt-Pocket Dress Trouser

A tailored dress trouser in worsted wool: a shaped front with a slant pocket and a front
pleat, a shaped back with a bound welt pocket, a straight waistband closed at centre front
with a hidden trouser hook-and-bar, and the welt strip.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, tailoring).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front_leg` | 2 mirrored | Front crease + pleat, slant pocket mouth. |
| `back_leg` | 2 mirrored | Back dart, bound welt mouth (clamped). |
| `waistband` | 1 | Cut to the measured waist plus the hook-bar underlap. |
| `welt` | 2 | The upper/lower welt strips. |

## Solving and clamps

The two inseams are **bisected** to equal length so the crease hangs plumb (the bisection
ceiling grows so the front can reach the back at the short-rise extreme). The waistband is
cut to the **measured** waist plus the hook-bar underlap. The **welt mouth is clamped**
inside the back panel waist run so an over-wide welt never runs off the panel into a
self-crossing outline. The waist quarter is held under the hip quarter (a big waist cannot
invert the side seam), and the half-knee is clamped to at least the half-hem. Verified at
defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

`front_leg.inseam ↔ back_leg.inseam`, the two `side`s, the two `hem`s, and `waistband.lower`
against the four summed panel waist runs (declared as ease).

## Cross-commons bridge

`notion.hardware_ref` → **`trouser-hook-bar`**, mapping `plate_len → hook_plate` (and the
wire diameter / gap proportionally). The sewn-plate params (`hook_width`, `plate_t`,
`sew_holes`) are **left unmapped** — the hook-bar is set on the band underlap, no sewn seam,
so no dimensional handshake is owed.

## Parameters

`waist_girth`, `hip_girth`, `inside_leg`, `front_rise`, `hem_width`, `knee_width`,
`band_depth`, `welt_width`, `hook_plate`, `wear_ease`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

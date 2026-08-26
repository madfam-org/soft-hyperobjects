# Raw-Hem Denim Short

The cut-off denim short with a **raw** (unfinished) hem — the leg chopped short and left to
fray, no turn-up. The raw edge is drawn at its finished length and the fray depth is marked
as a distress zone, not sewn.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, denim).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front_leg` | 2 mirrored | Front pocket rivet; raw fray zone marked. |
| `back_leg` | 2 mirrored | Deeper back rise; hem on the same hemline as the front. |
| `waistband` | 1 | Cut to the measured waist; jeans button seated on cloth. |
| `fly` | 2 | Shield / facing. |
| `coin_pocket` | 1 | Watch pocket. |
| `pocket_bag` | 4 | Front pocket lining. |

## Solving and clamps

The two inseams are **bisected** to equal length (a short leg twists too); the waistband is
cut to the **measured** panel waist runs. Clamps: the waist quarter is held under the hip
quarter (a big waist cannot invert the side seam), and the thigh opening is clamped to the
hip quarter so a raw hem set high never folds the leg into the crotch curve. The front and
back share one hemline so the side seams sew flush. The bisection ceiling grows until the
front inseam can reach the back's length at the short-rise extreme. Verified at defaults,
all-min, all-max, and every parameter swung to each bound.

## Declared seams

`front_leg.inseam ↔ back_leg.inseam`, the two `side`s, the two `hem`s, and `waistband.lower`
against the four summed panel waist runs (declared as ease).

## Cross-commons bridge

`notion.hardware_ref` → **`jeans-button`**, mapping `head_dia → button_head`. `button_head`
drives the garment's `buttoned_waistband` interface, so the set face is dimensionally
coupled. The raw hem carries **no** turn-up allowance.

## Parameters

`waist_girth`, `hip_girth`, `short_length`, `front_rise`, `hem_width`, `band_depth`,
`button_head`, `wear_ease`, `fray_depth`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Cable-Knit Vest

A sleeveless pullover vest in a cabled wool knit: a V-neck front, a higher round-neck back,
joined at the shoulders and sides, with ribbed neck / armhole / hem bands.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, knitwear).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 1 | V-neck across CF; cable panel centre marked. |
| `back` | 1 | Round neck scooped `back_neck_rise` below the shoulder line. |
| `armhole_band` | 2 | Ribbed rectangle cut to the measured front + back opening. |

## Solving and clamps

A cabled knit draws in across its width, so the body carries a modest positive ease
**floored** at the chest quarter. The front and back share one shoulder point and slope so
the shoulder seams sew flush. The **V-neck depth is clamped** above the armhole depth so a
deep-V request never crosses the front outline into a self-intersecting neckline the kernel
would still close and pass. The shoulder tip is clamped inside the body quarter, and the
ribbed armhole band is cut to the **measured** opening. Verified at defaults, all-min,
all-max, and every parameter swung to each bound (including deep-V / shallow-armhole and
shoulder-wider-than-chest).

## Declared seams

`front.shoulder ↔ back.shoulder`, `front.side ↔ back.side`. The armhole band attaches to the
measured `front.armhole + back.armhole` opening (declared as an interface).

## Cross-commons bridge

None — a pull-on cabled vest.

## Parameters

`chest_girth`, `body_length`, `shoulder_width`, `armhole_depth`, `neck_width`, `v_depth`,
`back_neck_rise`, `ease`, `band_depth`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

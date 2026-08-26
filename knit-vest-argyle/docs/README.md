# Argyle Knit Vest

A sleeveless V-neck pullover vest in the classic **argyle** intarsia — the diamond
lattice marked on the front so the pattern carries the colourwork.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 1 on fold | V-neck, shaped armhole, argyle diamonds marked. |
| `back` | 1 on fold | Crew back neck, shaped armhole. |
| `vneck_band` / `armhole_band` / `hem_band` | 1 / 2 / 1 | Rib bindings and hem, double-height, folded. |

## Solving and clamps

The shoulder point x is `shoulder_width/2`, capped at the body quarter. The shoulder run
is derived and **floored at 40 mm**. The V-neck point is clamped to sit at least 20 mm
**above the underarm** so the neck never inverts the front. The armhole cut-in is floored
above the neck width. The rib band lengths are solved from the measured openings and
floored. Signed negative knit ease with a floored draft girth.

## Declared seams

`front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`. The armholes and V-neck are
**bound**, not seamed to another panel, so they are declared as **interfaces**.

## Hardware

**None** — a pullover vest has no closure.

## Parameters

`chest_girth`, `body_length`, `neck_girth`, `shoulder_width`, `knit_ease`, `armhole_depth`,
`armhole_scoop`, `vneck_depth`, `shoulder_slope`, `diamond_rows`, `diamond_cols`,
`band_width`, `hemband_ratio`, `rib_height`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

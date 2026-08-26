# Knit Tank Dress

A pull-on sleeveless jersey dress: a scoop-neck tank body run down to dress length, with a
gentle **A-line release** from the waist to a flared hem.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 1 on fold | Deep scoop neck, scooped armhole, A-line side. |
| `back` | 1 on fold | Shallow scoop, matching side. |
| `neck_band` / `armhole_band` | 1 / 2 | Rib or self-binding, double-height, folded. |

## Solving and clamps

The neck scoop half-width is **floored below the chest quarter** so a wide scoop can never
eat the whole shoulder and invert the strap. Both scoop depths are clamped to sit **above
the underarm**. The waist release point is clamped below the underarm. The hem half-width
is `max(quarter hip, quarter chest) + flare`, so the dress **never narrows below the body**
at the hem. Signed negative knit ease with floored draft girths.

## Declared seams

`front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`. Neck and armholes are **bound**,
declared as interfaces.

## Hardware

**None** — a pull-on tank dress has no closure.

## Parameters

`chest_girth`, `hip_girth`, `dress_length`, `waist_drop`, `neck_girth`, `knit_ease`,
`armhole_depth`, `front_scoop`, `back_scoop`, `scoop_half`, `armhole_scoop`, `hem_flare`,
`band_width`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

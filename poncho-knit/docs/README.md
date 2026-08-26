# Knit Ruana Poncho

The **ruana**: an open-front poncho — a soft-knit rectangle split up the centre front so
it falls as two panels off the shoulders, shaped at the neckline so it sits rather than
slides.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `panel` | 2 mirrored | Rectangular panel with a shaped shoulder run and neckline scoop; joined at centre back, open at the front, optionally fringed. |

## Solving and clamps

The shoulder run is **floored below `panel_width − neck_quarter`** so the top corner never
inverts when the neck is wide on a narrow panel. The neck scoop is clamped inside the panel
(`≤ 0.4 × panel_length`). The panel width is floored so the poncho always covers the
shoulder.

## Declared seams

`panel.centre_back ↔ panel.centre_back` — the two mirrored panels join at the centre back.
The front stays open (declared as an interface).

## Hardware

**None** — a ruana is open and unfastened.

## Parameters

`panel_width`, `panel_length`, `neck_girth`, `neck_scoop`, `shoulder_run`, `fringe_depth`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

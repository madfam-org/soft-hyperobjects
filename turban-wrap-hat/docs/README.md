# Draped Turban Hat

A soft draped **turban** in stretch jersey: a fitted cap that covers the head plus a long
wrap band gathered into a knot at the centre front.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — millinery depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `cap` | 2 mirrored | Fitted head cap; two dome halves seamed at the crown. |
| `wrap` | 1 | Long drape band; length = head circ × turns. |
| `knot` | 1 | Gathered front knot panel. |

## Solving and clamps

The turban pulls on, so the cap draft girth is `head_girth + knit_ease` (signed negative)
and **floored** so it stays wearable at maximum stretch. The wrap length is derived
(`draft_girth × wrap_turns`) and floored so it can never go negative.

## Declared seams

`cap.crown_seam ↔ cap.crown_seam` — the two mirrored cap halves join at the crown.

## Hardware

**None** — a draped turban pulls on and has no closure.

## Parameters

`head_girth`, `head_height`, `knit_ease`, `wrap_turns`, `wrap_h`, `knot_width`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

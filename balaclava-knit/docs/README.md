# Knit Balaclava Hood

A close-fitting knit hood covering the head and neck with an opening for the face — two
mirrored side halves joined by a crown-and-back seam, a ribbed face-opening edge, and a
neck tube.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `hood` | 2 mirrored | Head profile from forehead over crown to nape, down the neck tube; face-opening curve. |
| `face_band` | 1 | Ribbed face-opening binding, double-height, folded. |

## Solving and clamps

The draft is smaller than the head and stretches on (**signed negative knit ease**, floored
draft girth). The face opening is **clamped inside the head profile** — `face_width ≤
half_head − 40`, `face_height ≤ head_height − 40` — so the crown and chin runs never go
negative and invert the hood after CCW normalization. The neck-tube half-width is floored
and capped at the head half.

## Declared seams

`hood.crown_seam ↔ hood.crown_seam` — the two mirrored halves join at the crown-and-back
seam. The face opening and neck hem are declared as interfaces.

## Hardware

**None** — a balaclava pulls on and has no closure.

## Parameters

`head_girth`, `head_height`, `neck_girth`, `neck_tube`, `face_width`, `face_height`,
`knit_ease`, `band_width`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

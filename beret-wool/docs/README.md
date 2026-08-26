# Wool Beret

The classic soft wool beret: a full circular **top**, an annular **under**, and a soft
inner **band**.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — millinery depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `top` | 1 | Full circular crown. |
| `under` | 2 on fold | Half-annulus; outer ring matches the top, inner hole is the head opening. |
| `band` | 1 | Soft inner band finishing the head opening. |

## Solving and clamps

Circular runs are drafted on the **corrected polygon radius** (`r = C/(2n·sin(π/n))`) so
drafted perimeters equal the intended circumferences. The **overhang is floored at 20 mm**
so the top ring is always larger than the head ring and the annulus can never invert. The
under is a half-annulus cut on the fold, so its outer and inner edges each measure half
their rings and are declared against their mirror listed twice.

## Declared seams

`top.rim ↔ under.outer` (both halves), `under.inner ↔ band.under_edge`, and the band closes
into a ring (`band.join_a ↔ band.join_b`).

## Hardware

**None** — a soft wool beret has no sizing hardware.

## Parameters

`head_girth`, `overhang`, `band_height`, `ease`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

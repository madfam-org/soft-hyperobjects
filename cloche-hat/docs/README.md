# Cloche Hat

The 1920s **cloche**: a deep bell crown that hugs the head down to the brow, with a small
downturned brim.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — millinery depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `tip` | 1 | Circular crown top. |
| `band` | 1 | Side crown (trapezoid: top = tip circ, bottom = head opening, height = crown depth). |
| `brim` | 2 on fold | Half-annulus downturned brim; inner ring = head opening. |

## Solving and clamps

Every ring is drafted on the **corrected polygon radius** so drafted perimeters equal
circumferences. The tip circumference is **floored above zero** and the brim inner radius is
**floored below the outer** so no ring inverts. The tip circ == the band top, the band
bottom == the head opening == the brim inner ring — each seam balances by construction.

## Declared seams

`tip.rim ↔ band.top`, `band.bottom ↔ brim.inner` (both halves).

## Cross-commons bridge

`notion.hardware_ref` → **`hat-size-reducer`**, mapping `head_circ → head_girth + ease` and
`strip_length → head_girth + ease`. `hat-size-reducer` declares no `flange` interface, so
it is **point/slot hardware** and no dimensional handshake is owed — it clips inside the
crown band, not sewn to an edge.

## Parameters

`head_girth`, `ease`, `crown_depth`, `tip_dome`, `brim_width`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Straw Boater Hat

The straw **boater**: a stiff flat-top cylindrical crown and a stiff flat wide brim — the
summer-regatta hat.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — millinery depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `tip` | 1 | Flat circular crown top, sized to the head ring (a true cylinder). |
| `band` | 1 | Straight side crown (a rectangle: head circ × crown height). |
| `brim` | 2 on fold | Flat half-annulus; inner ring = head opening. |

## Solving and clamps

A boater crown is a **true cylinder**, so the tip and band-top rings are both the head ring
and the band is a plain rectangle. Every ring is on the **corrected polygon radius**; the
brim inner radius is floored below the outer so the annulus never inverts.

## Declared seams

`tip.rim ↔ band.top`, `band.bottom ↔ brim.inner` (both halves).

## Cross-commons bridge

`notion.hardware_ref` → **`hat-size-reducer`** (point/slot hardware, no dimensional
handshake): `head_circ → head_girth + ease`, `strip_length → head_girth + ease`.

## Parameters

`head_girth`, `ease`, `crown_height`, `brim_width`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

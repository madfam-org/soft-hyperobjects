# Sewn Fedora Crown-and-Brim

A sewn (cut-and-sew, not blocked-from-a-cone) **fedora**: a tapered crown that narrows
toward a domed tip and a medium snap brim, with the pinch-and-dent crease marked on the
crown.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — millinery depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `tip` | 1 | Domed crown top, smaller than the head ring (the taper). |
| `band` | 1 | Tapered side crown (trapezoid: tip circ → head circ); crease marked. |
| `brim` | 2 on fold | Snap brim half-annulus; inner ring = head opening. |

## Solving and clamps

Every ring is on the **corrected polygon radius**. The tip circumference is **floored above
zero** so a large taper can never invert the tip; the brim inner radius is floored below the
outer. The band top == tip circ and band bottom == head opening, so the crown seams balance
by construction. The pinch-and-dent crease is marked as `marking` internals on the band.

## Declared seams

`tip.rim ↔ band.top`, `band.bottom ↔ brim.inner` (both halves).

## Cross-commons bridge

`notion.hardware_ref` → **`hat-size-reducer`** (point/slot hardware, no dimensional
handshake): `head_circ → head_girth + ease`, `strip_length → head_girth + ease`.

## Parameters

`head_girth`, `ease`, `crown_height`, `crown_taper`, `brim_width`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

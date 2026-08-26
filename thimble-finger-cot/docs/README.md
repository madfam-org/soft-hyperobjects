# Quilter's Thimble Cot

A padded fabric finger cot worn over a quilter's thimble — a soft tapered sleeve for the
pushing finger, quilted at the tip where the needle bears.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `side` | 1 | Trapezoid that rolls into a cone; quilted tip. |
| `cap` | 1 | Polygonised tip cap, cut to the measured tip. |

## Solving and clamps

The side panel is a trapezoid whose base and tip edges are the **measured** base and tip
circumferences, so rolled it is a true cone. The tip cap radius is the tip circumference over
2·π so the cone closes exactly. The taper is **clamped** so the tip is smaller than the base
but never a hairline — and the tip cap is **floored** so it is never a degenerate sliver at
the slim-finger extreme. Verified at defaults, all-min, all-max, and every parameter swung to
each bound (including tip-larger-than-base).

## Declared seams

`side.seam_r ↔ side.seam_l` (the back seam of the rolled cone). The cap seams to the tip edge
at the measured tip circumference.

## Cross-commons bridge

`notion.hardware_ref` → **`thimble`**, mapping `finger_girth`, `thimble_h` and `wall_t` from
the finger and cot dimensions. The thimble declares no flange interface — the cot wears over
it, so no dimensional handshake is owed.

## Parameters

`finger_girth`, `tip_girth`, `cot_length`, `wall`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

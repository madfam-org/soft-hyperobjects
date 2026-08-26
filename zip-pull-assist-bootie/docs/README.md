# Zip-Pull-Assist Bootie

An adaptive neoprene bootie with a full side zip and a printed pull-assist lever for
one-handed closing — for people with limited grip or reach.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 3 — footwear soft goods III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Toe + instep; solved lasting arc. |
| `quarter` | 2 mirrored | Ankle wrap; the side zip runs the `zip_edge`. |
| `guard` | 1 | Zip guard behind the side zip. |
| `lever` | 1 | Lever tab carrying the printed pull-assist body and finger loop. |

## Sizing — no invented landmark codes

ISO 8559 declares **no foot landmark codes**. This cartridge drafts from **plain sized
parameters** (`foot_length`, `foot_girth`, `ankle_height`); nothing is claimed the schema
cannot back.

## Solving and clamps

The vamp lasting edge is a **solved bow over its own chord** — proportionate, never a share
of the whole sole perimeter, which degenerates. The zip length is the **measured** quarter
side so it runs the full opening; the lever tab is cut to the printed assist body plus a
clearance; and the ankle rise is **clamped** under 4× the quarter half-width so the quarter
never folds through the lasting edge. Verified at defaults, all-min, all-max, and every
parameter swung to each bound.

## Declared seams

`vamp.throat_r ↔ quarter.zip_edge` and the two quarters at the centre back. The lasting edge
stitches to the sole (declared as an interface).

## Cross-commons bridge

`notion.hardware_ref` → **`zipper-pull-assist`**, mapping `body_l`, `lever_len` and `lever_w`
from the assist body and lever. The zipper-pull-assist declares no flange interface — the
assist clips to the zip pull, so no dimensional handshake is owed.

## Parameters

`foot_length`, `foot_girth`, `vamp_depth`, `ankle_height`, `assist_body`, `lever_len`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

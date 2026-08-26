# Point-Turner Tool Sleeve

A slim padded sleeve for a point turner: an open-top pocket with a fold-over flap and a
closure tab, cut to the exact tool length.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `back` | 1 | Back with the fold-over flap and closure tab. |
| `front` | 1 | Shorter front pocket. |
| `flap` | 1 | Reinforcing flap facing. |

## Solving and clamps

The sleeve is cut to the **measured** tool length plus a seat and the flap. The **front is
clamped shorter than the back** so the mouth is always open (a front as tall as the back
would seal the pocket). The closure tab is stepped in off the flap end so it seats on cloth.
Verified at defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

`front.bottom ↔ back.bottom` and `front.left ↔ back.left` (the shorter front declared with
the measured height ease).

## Cross-commons bridge

`notion.hardware_ref` → **`point-turner`**, mapping `tool_len`, `presser_w` and `tool_t`
from the tool dimensions. The point-turner declares no flange interface — the sleeve holds
the tool, so no dimensional handshake is owed.

## Parameters

`tool_length`, `tool_width`, `tool_thick`, `seat`, `flap_fold`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

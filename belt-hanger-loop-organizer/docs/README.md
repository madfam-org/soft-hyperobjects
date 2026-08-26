# Belt-Hanger Loop Organizer

A hanging spine sleeve with a row of soft belt loops, the loop count matching the printed
belt-hanger hooks so each belt is cradled without buckles knocking.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `spine` | 1 | Sleeves over the hanger bar; loop-attach lines. |
| `loop` | per hook | A strap folded into a belt loop. |

## Solving and clamps

The loop count equals the hanger hook count and the loops are spaced down the spine at the
**measured** spine length over the count, so a loop sits at each hook. Each loop length is
**clamped** to clear a belt width plus a turn (never a hairline a belt cannot pass), and the
spine sleeve is floored to sleeve on. Verified at defaults, all-min, all-max, and every
parameter swung to each bound.

## Declared seams

`loop.attach ↔ spine.top` (declared with the loop-vs-spine width ease).

## Cross-commons bridge

`notion.hardware_ref` → **`belt-hanger`**, mapping `hook_count`, `strap_w` and `hook_reach`
from the hook count, belt width and loop reach. The belt-hanger declares no flange interface
— the sleeve wraps the hanger, so no dimensional handshake is owed.

## Parameters

`hook_count`, `belt_width`, `hanger_length`, `bar_width`, `loop_reach`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

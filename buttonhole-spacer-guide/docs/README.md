# Buttonhole-Spacer Guide Roll

A roll-up guide that stores the buttonhole-spacer rail and prints its own measuring scale, so
the rail and the guide it needs live together.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `body` | 1 | Body with the rail-pocket outline and the derived scale ticks. |
| `pocket` | 1 | The long rail pocket. |
| `tie` | 1 | The wrap tie. |

## Solving and clamps

The rail pocket is cut to the **measured** rail plus a seat (declared to the body length).
The scale tick count is **derived** from the rail length over the pitch, floored at 2 so a
coarse pitch never yields a single tick. The pocket width is **clamped** inside the body so
it never runs off the panel edge. Verified at defaults, all-min, all-max, and every parameter
swung to each bound.

## Declared seams

`pocket.left ↔ body.left` (declared with the pocket-vs-body length ease).

## Cross-commons bridge

`notion.hardware_ref` → **`buttonhole-spacer`**, mapping `rail_len`, `rail_w` and `pitch`
from the rail. The buttonhole-spacer declares no flange interface — the guide holds the rail,
so no dimensional handshake is owed.

## Parameters

`rail_length`, `rail_width`, `rail_pitch`, `seat`, `margin`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

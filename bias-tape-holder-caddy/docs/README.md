# Bias-Tape Maker Caddy

A roll-up fabric caddy that holds a graduated set of bias-tape makers, its pockets sized to
the tools, with a tie that wraps the roll closed.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `body` | 1 | The caddy body with the pocket-attach line and dividers. |
| `pocket` | 1 | The pocket strip, pleated at each divider. |
| `tie` | 1 | The wrap tie. |

## Solving and clamps

Each pocket width is the tool throat plus a clearance, and the row width is their sum
(declared as the pocket-attach seam ease). The pocket depth is **clamped** under the body
height so a deep pocket never runs past the fold and inverts the flap. The tie is **floored**
to wrap the rolled caddy at least once plus a bow. Verified at defaults, all-min, all-max,
and every parameter swung to each bound.

## Declared seams

`pocket.attach ↔ body.top` (declared with the row-vs-body ease).

## Cross-commons bridge

`notion.hardware_ref` → **`bias-tape-maker`**, mapping `tape_width`, `tool_len` and
`throat_len` from the tool dimensions. The bias-tape-maker declares no flange interface —
the caddy holds the tool, it does not sew to it, so no dimensional handshake is owed.

## Parameters

`tool_count`, `tool_width`, `tool_length`, `pocket_clear`, `body_margin`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

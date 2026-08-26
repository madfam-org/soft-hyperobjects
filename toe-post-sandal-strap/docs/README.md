# Toe-Post Sandal Strap Set

The strap set for a toe-post sandal (the leather flip-flop / huarache toe-post): a Y toe post
that splits into two instep straps, and a heel strap, all riveted through the sole.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 3 — footwear soft goods III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `toe_post` | 1 | Y toe post + two instep straps; toe and instep rivets. |
| `heel` | 1 | Back heel strap with a rivet lap at each end. |

## Sizing — no invented landmark codes

ISO 8559 declares **no foot landmark codes**. This cartridge drafts from **plain sized
parameters** (`foot_length`, `foot_width`, `instep_girth`); nothing is claimed the schema
cannot back.

## Solving and clamps

The instep straps are half the **measured** instep girth plus a rivet lap each, and the heel
strap is the back-of-heel run plus laps. Each rivet is stepped in off the strap end by its own
cap plus a margin so it seats on leather and grips. The toe-post split is **clamped** so the Y
never crosses itself — the split point stays below the instep join. Verified at defaults,
all-min, all-max, and every parameter swung to each bound.

## Declared seams

None between pieces — each strap is riveted independently to the sole.

## Cross-commons bridge

`notion.hardware_ref` → **`rivet`**, mapping the cap height, bore and burr from `rivet_cap`.
The rivet's sewn-edge params (`cap_dia`, `post_dia`, `post_h`) are **left unmapped** — a rivet
is set through a drilled hole, no sewn seam, so no dimensional handshake is owed.

## Parameters

`foot_length`, `foot_width`, `instep_girth`, `strap_width`, `rivet_cap`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

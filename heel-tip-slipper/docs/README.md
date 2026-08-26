# Heel-Tip-Blank Slipper

A felted-wool slipper with a replaceable printed heel-tip blank seated in the heel counter,
so the one part that wears through — the heel — swaps out instead of the whole slipper.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 3 — footwear soft goods III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Toe + instep; solved lasting arc. |
| `sole` | 2 | Foot-shaped felt sole; heel-tip seat marked. |
| `counter` | 1 | Heel counter with the tip-blank pocket. |

## Sizing — no invented landmark codes

ISO 8559 declares **no foot landmark codes**. This cartridge drafts from **plain sized
parameters** (`foot_length`, `foot_girth`); nothing is claimed the schema cannot back.

## Solving and clamps

The vamp lasting edge is a **solved bow over its own chord** — proportionate, never a share
of the whole sole perimeter, which degenerates. The tip pocket is cut to the **measured** tip
blank plus a clearance, and its depth is **clamped** under the counter height so it never runs
through the topline. The vamp and counter are both lasted independently to the sole — no
inter-piece seam. Verified at defaults, all-min, all-max, and every parameter swung to each
bound.

## Declared seams

None between pieces — the vamp and counter each stitch to the sole (declared as the lasting
interface); the slipper has an open collar between them.

## Cross-commons bridge

`notion.hardware_ref` → **`heel-tip-blank`**, mapping `tip_w`, `tip_l` and `tip_h` from the
tip and counter. The heel-tip-blank declares no flange interface — the blank seats in the
counter pocket, so no dimensional handshake is owed.

## Parameters

`foot_length`, `foot_girth`, `vamp_depth`, `counter_height`, `tip_width`, `tip_length`,
`tip_clear`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

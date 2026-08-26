# Espadrille Upper Wrap

A canvas espadrille upper: a vamp with an ankle-wrap eyelet tie and a heel sling, stitched to
a jute sole.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 3 — footwear soft goods III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Toe + instep; solved lasting arc; ankle-tie eyelet pair. |
| `heel` | 1 | Heel sling; side edges drafted to the vamp side. |

## Sizing — no invented landmark codes

ISO 8559 declares **no foot landmark codes**. This cartridge drafts from **plain sized
parameters** (`foot_length`, `foot_girth`); nothing is claimed the schema cannot back.

## Solving and clamps

Both lasting edges are **solved arcs** whose length is a **proportionate bow over the piece's
own chord** — never a share of the whole sole perimeter, which degenerates into a sliver at
the extreme. The heel sling's top is drafted to the vamp side so the side seams sew flush, and
the eyelet pair is stepped in off the throat edge so it never tears out the finished edge.
Verified at defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

`vamp.side_r ↔ heel.side_r` and `vamp.side_l ↔ heel.side_l`. The lasting edge stitches to the
jute sole (declared as an interface).

## Cross-commons bridge

`notion.hardware_ref` → **`garment-eyelet`**, mapping `inner_dia → eyelet_dia`, `barrel_h`
and `wall`. The eyelet is point hardware set through a drilled hole; neither mapped key is a
`flange` param, so no dimensional handshake is owed.

## Parameters

`foot_length`, `foot_girth`, `vamp_depth`, `heel_height`, `eyelet_dia`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

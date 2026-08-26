# Driving-Moccasin Upper

A driving-moccasin upper: a soft sole-wrap gathered to a raised apron plug, with rubber
driving pebbles marked underfoot and a throat eyelet pair.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 3 — footwear soft goods III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `wrap` | 2 mirrored | Sole wrap; lasting arc; heel seam; underfoot pebbles. |
| `plug` | 1 | Raised apron; solved lens gathering the wrap throats. |

## Sizing — no invented landmark codes

ISO 8559 declares **no foot landmark codes**. This cartridge drafts from **plain sized
parameters** (`foot_length`, `foot_girth`); nothing is claimed the schema cannot back.

## Solving and clamps

The wrap's lasting edge is a **solved bow over its own chord** — proportionate, never a share
of the whole sole perimeter, which degenerates. The plug is a **solved lens** drafted to the
wrap's gathered throat so the apron sews in as a real gather (declared as the gather ease).
The wrap rise is **clamped** under 4× the wrap half-width so the wrap never folds through the
lasting edge. Verified at defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

`wrap.throat ↔ plug.side_a` (declared with the gather ease) and `wrap.heel_seam ↔
wrap.heel_seam` (the two wraps at the heel). The lasting edge is hand-lasted (declared as an
interface).

## Cross-commons bridge

`notion.hardware_ref` → **`garment-eyelet`**, mapping `inner_dia → eyelet_dia`, `barrel_h` and
`wall`. The eyelet is point hardware set through a drilled hole; neither mapped key is a
`flange` param, so no dimensional handshake is owed.

## Parameters

`foot_length`, `foot_girth`, `wrap_rise`, `plug_length`, `gather_ratio`, `eyelet_dia`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

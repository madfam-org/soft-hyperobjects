# Balconette Underwire Bra

A **balconette** (balcony) underwire bra: a wired cup whose horizontal seam sits **low and straight** so the cup lifts from below like a shelf, with **wide-set** straps that drop near-vertically from the outer cup edge. Made to measure to underbust and bust girths. FC-500 lane 7 (intimates & loungewear III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 7 — intimates & loungewear III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The balconette is the cut people reach for under a wide or square neckline, and off the rack it is graded to a size table that decides where the horizontal seam and the straps land — the two things that make a balconette read as a shelf. This cartridge makes both a number, over a wire solved to the wearer's own measured cup.

## Distinct from `underwire-bra`

The commons already carries a three-piece `underwire-bra` (a full/demi cup with a diagonal seam and near-centred straps). The balconette is a different object, and the difference is two explicit parameters:

| Parameter | Role |
| :-- | :-- |
| `cup_seam_drop` | how low the horizontal cup seam sits (higher = more shelf) |
| `strap_set_frac` | how wide the straps are set along the cup top |

## The wire handshake

The underwire is the Yantra4D solid [`bra-underwire`](https://yantra4d.com), referenced via `notion.hardware_ref`. The cradle's `wire_line` edge is **solved** to the wire's own arc:

| Quantity | Source |
| :-- | :-- |
| Wire chord | `cup_width` → hardware `cup_width` |
| Wire sweep | `sweep_deg` → hardware `sweep_deg` |
| Arc radius | `R = cup_width / (2 sin θ/2)` (solved) |
| Channel run | `L = R θ` (the drafted `wire_line`) |

Both parameters drive the garment's `wire_line` interface **and** the hardware's `cradle_seam` flange, so `wire_run == cradle.wire_line == cup mouths` — one dimension, checked by `declare_seam`, at every extreme.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `cup_lower_inner` | 2 pairs | lower cup, inner — half the solved mouth |
| `cup_lower_outer` | 2 pairs | lower cup, outer — the other half + side rise |
| `cup_upper` | 2 pairs | balconette upper band (the low seam, wide strap) |
| `cradle` | 2 pairs | wired frame; `wire_line` carries the channel |
| `band` | 2 pairs | negative-ease underband |
| `back` | 2 pairs | back wing to the centre-back hook |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un brasier balconette con varilla: una copa con varilla cuya costura horizontal se coloca baja y recta para que levante desde abajo como una repisa, con tirantes muy separados que caen casi verticales. Hecho a medida al contorno bajo el busto y al busto. Carril 7 de FC-500 (lencería y ropa de descanso III).

## Français
Un soutien-gorge balconnet à armatures : un bonnet armé dont la couture horizontale est placée bas et droite pour soutenir par le bas comme une tablette, avec des bretelles très écartées. Fait sur mesure aux tours de dessous de poitrine et de poitrine. Couloir 7 de FC-500 (lingerie et vêtements d'intérieur III).

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

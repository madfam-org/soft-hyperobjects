# Balconette Bra

A balconette bra: one horizontal cup seam carries all the shaping, the top edge runs low and nearly level across the bust (the "balcony"), straps sit wide, and the wire sweeps shallower than a full cup. Made to measure to underbust and bust girths. FC-300 lane 3 (structured intimates).

Part of the **Fashion Cabinet Commons** (FC-300, lane 3 — structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A balconette's shape comes from easing a longer curve into a shorter one, a step commercial patterns describe only as "ease to fit" and leave the sewist to guess. Here the surplus is computed, declared on the seam, and verified — the shaping is a stated number in millimetres, spread evenly from a marked apex notch.

## The shaping is a declared number

There is no vertical seam through the apex on a balconette, so the single horizontal
seam does all the work. The lower cup is drafted **longer** than the upper cup by
`seam_ease_pct`, and that surplus is eased in at the machine:

```
lower.cup_seam = 152.8 mm      upper.cup_seam = 142.8 mm      ease = 10.0 mm
```

The seam is declared with that `ease`, so the verifier checks the *intended* surplus
rather than tolerating an accidental mismatch. Spread it evenly either side of the
apex notch and press over a ham.

## The wire handshake

Shared with [`underwire-bra`](../../underwire-bra/docs/README.md). The underwire is the
Yantra4D solid `bra-underwire`, referenced via `notion.hardware_ref` and never modelled
here; the cradle's `wire_line` edge is built as exactly that wire's arc:

| Quantity | Value at defaults |
| :-- | --: |
| Wire chord (`cup_width`) | 140.0 mm |
| Wire sweep (`sweep_deg`) | 180° |
| Solved arc run | 219.91 mm |
| `cradle.wire_line` | 219.90 mm |
| `cup_lower.mouth` | 219.90 mm |

A balconette deliberately runs a **shallower sweep** than a full cup — that is what
lets the top edge sit low and horizontal.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `cup_lower` | 2 pairs | lower section; mouth = solved arc, top edge carries the ease |
| `cup_upper` | 2 pairs | the balcony; low level neckline, wide strap tab |
| `cradle` | 2 pairs | the wired frame; `wire_line` carries the channel |
| `band` | 2 pairs | negative-ease underband (the load path) |
| `back` | 2 pairs | back wing to the centre-back hook |

## Español
Un sostén balconette: una sola costura horizontal de copa lleva todo el moldeado, el canto superior corre bajo y casi a nivel sobre el busto (el "balcón"), los tirantes van separados, y la varilla barre menos que una copa completa. Hecho a medida al contorno bajo el busto y al busto. Carril 3 de FC-300 (lencería estructurada).

> La forma de un balconette viene de embeber una curva más larga en una más corta, un paso que los patrones comerciales describen sólo como "embeber al ajustar" y dejan a quien cose adivinar. Aquí el excedente se calcula, se declara en la costura y se verifica.

## Français
Un soutien-gorge balconnet : une seule couture horizontale de bonnet porte toute la mise en forme, le bord supérieur court bas et presque à l'horizontale sur la poitrine (le « balcon »), les bretelles sont écartées, et l'armature balaie moins qu'un bonnet complet. Fait sur mesure aux tours de dessous de poitrine et de poitrine. Couloir 3 de FC-300 (lingerie structurée).

> La forme d'un balconnet vient de l'embu d'une courbe plus longue dans une plus courte, une étape que les patrons commerciaux décrivent seulement par « embuer pour ajuster ». Ici l'excédent est calculé, déclaré sur la couture et vérifié.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

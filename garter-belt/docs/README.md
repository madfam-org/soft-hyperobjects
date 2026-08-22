# Garter Belt

A shaped suspender belt that sits between waist and high hip and hangs four straps to stocking clips. The belt is drafted as a flattened truncated cone — its top edge sums to the waist ring and its hem to the high-hip ring — which is why it stays put where a straight strip rides up or falls down. FC-300 lane 3 (structured intimates).

Part of the **Fashion Cabinet Commons** (FC-300, lane 3 — structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Two failures make cheap garter belts unwearable, and both are dimensional. A straight strip of elastic cannot sit between a waist and a hip, so it rides up or falls down; and a strap cut to whatever webbing was on hand either will not thread its clip or twists inside an oversized slot.

## The belt is a cone, and it closes

The ring is walked as `front(on fold) + side + back(on fold)`, mirrored. Every panel
gets the **same** flare — not a flare proportional to its width — so all six slanted
seams are congruent and meet exactly:

| Ring | Target | Drafted |
| :-- | --: | --: |
| Waist (top edges) | 658.0 mm | 658.0 mm |
| High hip (hems) | 902.4 mm | 902.4 mm |

Giving each panel a *proportional* flare instead makes the wide panels slant harder
than the narrow ones and the seams cannot meet — the verifier caught exactly that
during drafting, which is the argument for declaring every seam.

## The clip handshake

The clips are the Yantra4D solid `garter-clip`, referenced via `notion.hardware_ref`
and never modelled here. Its sewn mating feature is a `strap_slot` **flange** driven by
`strap_w` and `strap_t` — the slot the strap threads through:

```
strap_w  ->  the drafted strap's cut width (the strap_edge interface)
         ->  the clip's slot width
strap_t  ->  the clip's slot clearance for the folded webbing
```

One number reaches both objects, so the strap threads its hardware by construction
rather than by luck.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front_panel` | 1 on fold | shaped front, 2 strap positions marked |
| `side_panel` | 2 pairs | shaped side |
| `back_panel` | 1 on fold | shaped back, 2 strap positions, hook closure |
| `strap` | 4 | suspender strap, cut to `strap_w` |

## Español
Un liguero moldeado que se asienta entre la cintura y la cadera alta y cuelga cuatro tirantes hacia broches de media. El cinturón se traza como un cono truncado desplegado — su canto superior suma el anillo de cintura y su ruedo el de cadera alta. Carril 3 de FC-300 (lencería estructurada).

> Dos fallas hacen impracticables los ligueros baratos, y ambas son dimensionales: una tira recta no puede asentarse entre cintura y cadera, y un tirante cortado a ojo o no enhebra su broche o se tuerce en una ranura holgada.

## Français
Un porte-jarretelles mis en forme qui se place entre la taille et la hanche haute et suspend quatre jarretelles vers des pinces à bas. La ceinture est tracée comme un cône tronqué déplié — son bord supérieur totalise l'anneau de taille et son ourlet celui de la hanche haute. Couloir 3 de FC-300 (lingerie structurée).

> Deux défauts rendent les porte-jarretelles bon marché inutilisables, et tous deux sont dimensionnels : une bande droite ne peut se placer entre taille et hanche, et une jarretelle coupée à vue soit n'enfile pas sa pince, soit vrille dans une fente trop large.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

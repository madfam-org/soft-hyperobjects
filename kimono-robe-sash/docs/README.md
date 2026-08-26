# Sashed Kimono Robe

A wrap dressing-robe on **kimono logic**: body and sleeve in one continuous panel (no set-in armscye), a self band running unbroken up both fronts and around the back neck, and a self sash that ties at the waist. It closes by wrapping, so it carries **no hardware** — the honest pure-pattern case the FC-500 plan reserves for wrap robes. Made to measure to chest/bust, hip and lengths. FC-500 lane 7 (intimates & loungewear III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 7 — intimates & loungewear III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The dressing robe is one of the few garments almost everyone owns and almost nobody has fitted, sold in three lengths that ignore height entirely. A kimono robe is also the most forgiving garment to draft to measure — the cross construction has no armscye to fit — which makes it the ideal object for a first parametric make.

## The kimono cross

Body and sleeve are one panel, so the only construction seams are:

| Seam | Declared as |
| :-- | :-- |
| underarm + side | `front.side + front.sleeve_under` ↔ `back.side + back.sleeve_under` |
| shoulder / sleeve-top fold | `front.sleeve_top` ↔ `back.sleeve_top` |
| self band | `band.attach` ↔ two `front.front_neck` + two `back.neck` |

## The band solve

A self band that runs up both fronts and around the back neck must be exactly as long as the edge it finishes. The band is drafted to the **measured** front-edge + back-neck run and declared against it, so it is never cut short — the classic error that makes a robe band ripple or fall short at the hem.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `back` | 1 on fold | kimono back half |
| `front` | 2 mirror | kimono front (the wrap V) |
| `band` | 1 folded | self band, front + back neck |
| `sash` | 1 folded | waist tie (waist girth × 1.5 + bow) |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Una bata cruzada de kimono: cuerpo y manga en un solo panel continuo, sin sisa montada, una tira de la misma tela por ambos delanteros y el escote trasero, y un cinto que anuda a la cintura. Cierra al cruzarse, sin herrajes. Hecha a medida a busto, cadera y largos. Carril 7 de FC-500.

## Français
Un peignoir croisé kimono : corps et manche en un seul panneau continu, sans emmanchure montée, une bande de même tissu sur les deux devants et l'encolure dos, et une ceinture nouée à la taille. Il se ferme en croisant, sans accessoire. Fait sur mesure à la poitrine, aux hanches et aux longueurs. Couloir 7 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

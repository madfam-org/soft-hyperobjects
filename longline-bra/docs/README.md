# Longline Bra

A bra continued down over the ribs into a boned midriff panel — the bridge between lingerie and foundationwear. The load is carried by a broad gripping panel rather than a narrow band, and light boning at every vertical seam stops that panel rolling and collapsing. Made to measure to underbust, bust and waist girths. FC-300 lane 3 (structured intimates).

Part of the **Fashion Cabinet Commons** (FC-300, lane 3 — structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Boning is where home foundationwear usually goes wrong: stays are bought by the packet in fixed lengths, cut down with tin snips, and end up either punching through a hem or leaving the panel to fold above them. This cartridge derives the stay length from the panel the wearer actually drafted.

## The boning handshake

The stays and their channels are the Yantra4D solid `boning-stay`, referenced through
`notion.hardware_ref` and never modelled here. The channel length is **derived**, not
chosen:

```
stay_length = midriff_depth - 2 * bone_clearance
            = 130 mm - 2 * 8 mm  =  114.0 mm     (at defaults)
```

That expression is what the manifest maps to the hardware's `stay_length`, and the
drafted channel internals are drawn at that same literal length — what is chalked is
what is printed. Because `midriff_depth` also drives the garment's own
`boning_channels` and `midriff_seam` interfaces, the same dimension reaches both sides
of the joint, which is what makes it a *coupled* handshake rather than a slug that
happens to resolve.

Eight stays at defaults: two in each front panel, one in each side panel, one either
side of the centre-back hook tape.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `cup_lower` / `cup_upper` | 2 pairs each | two-piece cup over the wired cradle |
| `cradle` | 2 pairs | `wire_line` solved to the underwire arc |
| `midriff_front` | 2 pairs | the boned heart of the longline |
| `midriff_side` | 2 pairs | boned side panel, seam-matched to the front |
| `back` | 2 pairs | full-depth wing, boned centre back, 4-row hook tape |

Two hardware families meet here: `boning-stay` (the bridged, coupled one) and
`bra-underwire` for the cup, referenced in the BOM.

## Español
Un sostén que continúa sobre las costillas hasta un panel de cintura con ballenas — el puente entre lencería y prenda base. La carga la lleva un panel amplio que agarra, no una banda angosta. Hecho a medida al contorno bajo el busto, al busto y a la cintura. Carril 3 de FC-300 (lencería estructurada).

> Las ballenas son donde suele fallar la prenda base casera: se compran en largos fijos, se recortan y acaban o atravesando el ruedo o dejando que el panel se doble. Este cartucho deriva el largo de la ballena del panel que realmente se trazó.

## Français
Un soutien-gorge prolongé sur les côtes en un panneau de taille baleiné — le pont entre lingerie et vêtement de base. La charge est portée par un large panneau qui adhère plutôt que par une bande étroite. Fait sur mesure aux tours de dessous de poitrine, de poitrine et de taille. Couloir 3 de FC-300 (lingerie structurée).

> Les baleines sont l'endroit où le vêtement de base fait maison échoue : achetées en longueurs fixes, recoupées, elles finissent par percer un ourlet ou laisser le panneau se plier. Ce cartouche dérive la longueur de baleine du panneau réellement tracé.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

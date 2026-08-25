# Nursing Bra

A drop-cup nursing bra built around the one requirement that drives every decision: the cup must open one-handed and come back, repeatedly, without the band ever slackening. Made to measure to underbust and bust girths. FC-300 lane 3 (structured intimates).

Part of the **Fashion Cabinet Commons** (FC-300, lane 3 — structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A nursing bra is medical equipment sold as underwear: it is operated one-handed, dozens of times a day, for months, usually while exhausted and holding an infant. The two things that decide whether it works are never printed on the label.

## Three consequences of "the cup must open"

1. **The cup splits horizontally.** A fixed **sling** (lower) plus a **drop cup**
   (upper). The sling is not decorative — it is what still holds the breast when the
   cup is open, and it is why a nursing bra is not just a bra with a clip on it.
2. **The strap is the hinge.** The drop cup hangs from a **ring** at its apex tab.
   Cup and strap are joined by *hardware*, not by a seam — the point/slot case.
3. **The band is untouched by the opening.** Band and cradle run continuously under
   both cup sections; the drop happens entirely above the wire line.

`drop_cup.lower` and `sling.upper` are both **free finished edges** and are deliberately
never declared as a seam — sewing them together would defeat the entire garment.

## The support number nobody prints

```
sling_hold_pct = 42.0 %     (sling 39.9 mm of a 95 mm cup rise)
```

With the drop cup released, the sling still spans this share of the cup height. Raise
`sling_frac` for more hold when open, lower it for easier access.

## The ring handshake

The rings and sliders are the Yantra4D solid `bra-ring-slider` — a point/slot fitting
whose loop grips the strap, with no sewn flange. One number reaches every joint:

```
strap_w = 19 mm  ->  strap cut width
                 ->  drop_cup.ring_tab, sling.strap_tab, back.strap_tab
                 ->  the printed ring's loop width
```

A strap wider than the ring will not thread; narrower and the clip slips under load —
which on a nursing bra means it opens when it should not. All three tab seams verify at
19.0 mm exactly.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `sling` | 2 pairs | fixed lower cup; mouth = solved wire arc |
| `drop_cup` | 2 pairs | falls away; free lower edge, ring tab |
| `cradle` | 2 pairs | wire channel, continuous under both sections |
| `band` | 2 pairs | underband, 4×3 hook tape for a changing ribcage |
| `back` | 2 pairs | back wing |
| `strap` | 2 | cut to `strap_w`; ring at the cup end |

## Español
Un sostén de lactancia de copa abatible construido alrededor del único requisito que rige todo: la copa debe abrirse con una mano y volver, una y otra vez, sin que la banda pierda su agarre. Hecho a medida al contorno bajo el busto y al busto. Carril 3 de FC-300 (lencería estructurada).

> Un sostén de lactancia es equipo médico vendido como ropa interior: se opera con una mano, decenas de veces al día, durante meses. Las dos cosas que deciden si funciona nunca se imprimen en la etiqueta.

## Français
Un soutien-gorge d'allaitement à bonnet abattant construit autour de la seule exigence qui commande tout : le bonnet doit s'ouvrir d'une main et revenir, encore et encore, sans que la bande ne se relâche. Fait sur mesure aux tours de dessous de poitrine et de poitrine. Couloir 3 de FC-300 (lingerie structurée).

> Un soutien-gorge d'allaitement est un équipement médical vendu comme de la lingerie : il s'actionne d'une main, des dizaines de fois par jour, pendant des mois. Les deux choses qui décident s'il fonctionne ne sont jamais imprimées sur l'étiquette.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

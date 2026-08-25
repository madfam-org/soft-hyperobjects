# Waspie

A short six-panel waist cincher spanning the lower ribs to the upper hip, nipped at the waist with an explicit reduction, boned at every seam, closing on hooks at the front and lacing at the back. Made to measure to underbust, waist and hip girths. FC-300 lane 3 (structured intimates).

Part of the **Fashion Cabinet Commons** (FC-300, lane 3 — structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Waist reduction is the one corsetry number that must never be a guess, and commercial cinchers hide it entirely behind a size label. Here it is a stated parameter in millimetres, bounded by a safety constraint.

## Short changes the engineering twice

1. **More boning per millimetre.** A short garment has less area to spread the
   compression over, so it wants a bone at *every* seam — six panels, six seams,
   twelve channels — or it rolls at the top and bottom edges instead of holding
   the waist.
2. **It can skip the busk.** A full corset opens on a rigid steel busk because it is
   long enough that hooks alone would gap between them. A waspie closes on a
   **hook-and-eye front** instead, which is why this cartridge does not reference
   `corset-busk` — see [`structured-corset`](../../structured-corset/docs/README.md)
   for that lineage. Hooks and eyes are point/slot: no sewn flange, so no edge coupling.

## Three rings, closed exactly

Six equal panels, every one sharing the same top/waist/bottom half-widths — so every
vertical seam edge is congruent and paired seams balance to the micron:

| Ring | Source | Drafted |
| :-- | :-- | --: |
| Top | `underbust_girth` | 780.0 mm |
| Waist | `waist_girth − waist_reduction` | 670.0 mm |
| Bottom | `hip_girth` | 960.0 mm |

## The boning handshake

```
stay_length = waspie_len - 2 * bone_clearance
            = 200 mm - 2 * 10 mm  =  180.0 mm     (at defaults)
```

That expression is mapped to the Yantra4D `boning-stay` hardware, and the drafted
channel internals are marked at that same literal length. `waspie_len` also drives the
garment's own `boning_channels` and `panel_seams` interfaces, making the handshake
dimensionally coupled.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `cf_panel` | 2 pairs | centre front, hook-and-eye line, 2 channels |
| `side_panel` | 2 pairs | side, 2 channels |
| `back_panel` | 2 pairs | back, lacing, 2 channels |

## Español
Una cinturilla corsé corta de seis paneles que abarca de las costillas bajas a la cadera alta, ceñida con una reducción explícita, con ballenas en cada costura, que cierra con broches al frente y cordón atrás. Hecha a medida al contorno bajo el busto, a la cintura y a la cadera. Carril 3 de FC-300 (lencería estructurada).

> La reducción de cintura es el número de la corsetería que jamás debe adivinarse, y los ceñidores comerciales lo esconden tras una etiqueta de talla. Aquí es un parámetro declarado en milímetros, acotado por una restricción de seguridad.

## Français
Une guêpière courte à six panneaux allant des côtes basses à la hanche haute, resserrée avec une réduction explicite, baleinée à chaque couture, fermée par des agrafes devant et un laçage dos. Faite sur mesure aux tours de dessous de poitrine, de taille et de hanches. Couloir 3 de FC-300 (lingerie structurée).

> La réduction de taille est le nombre de la corsetterie qui ne doit jamais être deviné, et les serre-tailles commerciaux le cachent derrière une étiquette. Ici c'est un paramètre énoncé en millimètres, borné par une contrainte de sécurité.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

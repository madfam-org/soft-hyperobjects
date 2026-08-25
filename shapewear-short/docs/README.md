# Shapewear Short

A high-waisted pull-on compression short in powernet, waist to mid-thigh, with graduated compression stated as an explicit percentage per zone rather than hidden behind a size letter. Made to measure to waist, hip and thigh girths plus body rise. FC-300 lane 3 (structured intimates).

Part of the **Fashion Cabinet Commons** (FC-300, lane 3 — structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Shapewear sells compression as a size letter and an adjective — "firm control" — which tells a wearer nothing, cannot be reproduced, and hides the one decision that determines whether the garment is comfortable or a tourniquet.

## Compression is a number, per zone

Each zone gets its own negative ease, and the output prints every finished ring beside
the body measurement it came from:

| Zone | Compression | Body | Finished |
| :-- | --: | --: | --: |
| Waist | 18 % | 760.0 mm | 623.2 mm |
| Hip | 12 % | 990.0 mm | 871.2 mm |
| Thigh | 7 % | 580.0 mm | 539.4 mm |

The gradient is deliberate. The thigh takes **least**, because a leg opening cut too
tight rolls up and cuts in — the failure mode of cheap shapewear, and a drafting
decision rather than a fabric problem. A manifest constraint warns if thigh compression
is ever set above hip compression.

## Seat room goes in the crotch curve, not the side seam

The back needs more cloth than the front through the seat or the short drags itself
down. That room is added as extra **depth in the back crotch curve**, never as extra
width at the side seam — which keeps both side seams straight, vertical and balanced
(`front_leg.side_seam = back_leg.side_seam = 340.0 mm`). An earlier draft put the room
in the side seam and the verifier rejected it at a 34.5 mm mismatch.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front_leg` | 2 pairs | front leg, straight side seam |
| `back_leg` | 2 pairs | back leg, deeper seat curve |
| `waistband` | 2 pairs | high band, tapered so it does not roll down |
| `gusset` | 1 | cotton jersey — not optional in a compression garment |

No hardware: a pull-on garment has no closure, and this cartridge does not invent one.

## Español
Un short de compresión de tiro alto en powernet, de la cintura al medio muslo, con compresión graduada declarada como un porcentaje explícito por zona en vez de esconderse tras una letra de talla. Hecho a medida a cintura, cadera y muslo más el tiro. Carril 3 de FC-300 (lencería estructurada).

> La faja vende la compresión como una letra de talla y un adjetivo — "control firme" — que no dice nada, no puede reproducirse y esconde la única decisión que determina si la prenda es cómoda o un torniquete.

## Français
Un short de compression taille haute en powernet, de la taille à mi-cuisse, avec une compression graduée énoncée en pourcentage explicite par zone plutôt que cachée derrière une lettre de taille. Fait sur mesure aux tours de taille, de hanches et de cuisse plus la hauteur d'enfourchure. Couloir 3 de FC-300 (lingerie structurée).

> La gaine vend la compression comme une lettre de taille et un adjectif — « maintien ferme » — qui ne dit rien, ne peut être reproduit, et masque la seule décision qui détermine si le vêtement est confortable ou un garrot.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

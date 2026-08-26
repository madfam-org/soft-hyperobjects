# Princess-Seam Dance Leotard

A dance leotard shaped by **princess seams** — curved vertical seams running from the shoulder over the bust apex to the waist, so the garment is fitted by seam rather than dart (the convention of stage and competition dancewear, where a dart would break the line the audience reads). Made to measure to bust, waist and hip girths. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Dancewear is one of the most size-hostile garment categories, and a poorly fitted leotard is visible from the back row, because the princess seam either sits on the bust apex or it does not. This cartridge draws the fit to a real body and guarantees the seam that decides the whole look balances by construction.

## The princess seam solve

A princess seam is one physical seam sewn from two curves on two panels; the centre-panel curve and the side-panel curve **must be equal length** or the bust puckers. Both are built from **identical curve math** (the side panel's is the centre's, translated sideways — translation preserves length), so the seam balances by construction, not by a fitting.

The side seam is drafted **vertical** with matched y-spans front and back, so all the shaping lives in the princess seam and the side seam always balances.

## The snap handshake

The gusset closes on the Yantra4D [`sew-on-snap`](https://yantra4d.com). `snap_dia` drives the snap's `sew_face` flange **and** the drafted gusset seat **and** the garment's `gusset_snap` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front_centre` | 1 on fold | front centre panel (CF, princess seam) |
| `front_side` | 2 mirror | front side panel (princess seam, armhole) |
| `back` | 1 on fold | scooped back |
| `gusset` | 2 | crotch gusset with the sew-on-snap |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un leotardo de danza formado por costuras princesa — costuras verticales curvas del hombro sobre el ápice del busto a la cintura — ajustado por costura y no por pinza. Cierra en una entrepierna con broche `sew-on-snap`. Hecho a medida a busto, cintura y cadera. Carril 9 de FC-500.

## Français
Un justaucorps de danse façonné par des coutures princesse — des coutures verticales courbes de l'épaule par l'apex de la poitrine à la taille — ajusté par couture et non par pince. Ferme sur un gousset à bouton-pression `sew-on-snap`. Fait sur mesure aux tours de poitrine, de taille et de hanches. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

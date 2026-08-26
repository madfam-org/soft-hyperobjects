# Marching-Band Tunic

The high-collared, structured tunic of the marching band and drum corps: a fitted military coat with a standing collar, a chest of horizontal braid (*frogging*), and rigid **epaulettes** (shoulder boards) — the boards are Yantra4D `epaulette-board` solids, and this cartridge drafts the tunic and the seat the board sits on. Made to measure to chest, waist and lengths. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> School and community marching bands wear uniforms that cost hundreds per player and are ordered from a size chart, so a growing teenager wears a coat that fits for one season. Drafting it to a real player with epaulette boards clamped to the actual shoulder, and the boards a printable commons part, gives a band a sharp, reproducible uniform it can make and mend itself.

## Provenance

The marching-band / drum-corps tunic descends from 18th–19th century military full dress: standing collar, braided chest, rigid epaulettes. It is worn by school and community bands worldwide as a uniform that must read sharp on a field from a distance.

## The epaulette handshake

An epaulette board is a rigid trapezoid on a curved shoulder, so its length is **clamped to the drafted shoulder seam** (it never hangs off the arm) and its ends are placed **wide at the shoulder point, narrow at the neck** (the military convention). The board is the Yantra4D [`epaulette-board`](https://yantra4d.com); `board_len` drives the board's `shoulder_edge` flange **and** the drafted seat **and** the `epaulette_seat` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `tunic_front` | 2 mirror | front (braided chest, buttons) |
| `tunic_back` | 1 on fold | back |
| `sleeve` | 2 mirror | set-in sleeve (cap solved to armscye) |
| `collar` | 1 | standing collar (cut to the neck) |
| `epaulette` | 2 mirror | epaulette board seat |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
La túnica estructurada de cuello alto de la banda de guerra: abrigo militar entallado con cuello de tira, pecho de alamares y charreteras rígidas (`epaulette-board`). Hecho a medida a pecho, cintura y largos. Carril 9 de FC-500.

## Français
La tunique structurée à col haut de la fanfare : veste militaire ajustée à col officier, poitrine à galon et épaulettes rigides (`epaulette-board`). Fait sur mesure à la poitrine, à la taille et aux longueurs. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

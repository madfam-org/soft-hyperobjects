# Harlequin Diamond Suit

The **Arlecchino** (Harlequin) suit of the commedia dell'arte: a close-fitting jacket and tapered trouser marked all over with a regular diamond lattice (*losanges*), buttoned down the front with a column of Yantra4D `sew-through-button`. Made to measure to chest, waist, hip and lengths. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Commedia dell'arte is a living theatre tradition taught worldwide, and the Arlecchino suit is its most recognisable costume — yet one of the hardest to make well, because a badly tiled diamond lattice reads as a mistake from the stalls. Encoding the lattice as a parametric object gives a suit whose diamonds meet at the seams by construction.

## Provenance

Arlecchino's motley began as the patched rags of a poor servant and formalised into the regular *losange* lattice by the 17th–18th century. The suit is jacket + trouser, buttoned front, all-over diamonds.

## The lattice solve

A regular diamond lattice must tile each panel without a broken diamond at a seam, so the pitch is **snapped** to an integer number of diamonds across each panel width:

```
columns    = round(panel_width / diamond_pitch)
pitch_used = panel_width / columns
```

## The button handshake

The jacket buttons on the Yantra4D [`sew-through-button`](https://yantra4d.com); `button_ligne` drives the button seats **and** the hardware's `sew_face` flange **and** the `button_stand` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `jacket_front` | 2 mirror | jacket front (button column, lattice) |
| `jacket_back` | 1 on fold | jacket back (lattice) |
| `trouser` | 2 mirror | tapered trouser (lattice) |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
El traje de Arlecchino de la commedia dell'arte: chaqueta ceñida y pantalón entallado con retícula regular de rombos, abotonados al frente con `sew-through-button`. Hecho a medida a pecho, cintura, cadera y largos. Carril 9 de FC-500.

## Français
Le costume d'Arlecchino de la commedia dell'arte : veste ajustée et pantalon fuselé à réseau régulier de losanges, boutonnés devant par des `sew-through-button`. Fait sur mesure à la poitrine, à la taille, aux hanches et aux longueurs. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Quick-Change Stage Gown

The quick-change stage gown of the illusion act and the musical: a fitted gown whose centre-back runs unbroken from collar to hem as a **magnetic breakaway seam** held by a column of Yantra4D `magnetic-clasp` clasps, so a dresser or the performer can rip the whole gown off in one motion for a reveal or a wing change in seconds. Made to measure to bust, waist, hip and lengths. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The quick-change is one of the oldest crafts in live performance, normally engineered by hand for one production and one performer. A gown whose breakaway seam is drafted to a real body with a solved clasp count, and printable commons clasps, democratises a piece of theatre-craft that has always lived in a few specialists' hands.

## Provenance

The quick-change gown is the working garment of the illusion act, the quick-change variety turn, and the musical with fast on-stage transformations: the whole engineering is the breakaway seam — historically hooks or Velcro, here a magnetic seam that closes clean and releases in one motion.

## The clasp-count solve

A breakaway seam holds only if the clasps are close enough that no gap sags open under movement, but each adds pull-apart force, so the count is solved from the seam length:

```
clasps = round(breakaway_length / clasp_pitch)
```

so the holding force per unit length stays constant whatever the size. The seam allowance is floored to hold the clasp with margin.

## The clasp handshake

The clasps are the Yantra4D [`magnetic-clasp`](https://yantra4d.com); `clasp_dia` drives the clasp's `disc_dia` (its `sew_face` flange) **and** the drafted seat **and** the `breakaway_seam` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `bodice_front` | 1 on fold | fitted front |
| `bodice_back` | 2 mirror | back (breakaway CB clasps) |
| `skirt` | 1 | gathered skirt (breakaway CB clasps) |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
El vestido escénico de cambio rápido: un vestido entallado cuya espalda es una costura magnética desprendible del cuello al ruedo con broches `magnetic-clasp`, que se arranca de un movimiento. Hecho a medida a busto, cintura, cadera y largos. Carril 9 de FC-500.

## Français
La robe de scène à changement rapide : une robe ajustée dont le dos est une couture magnétique détachable du col à l'ourlet avec des fermoirs `magnetic-clasp`, arrachée d'un geste. Faite sur mesure à la poitrine, à la taille, aux hanches et aux longueurs. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

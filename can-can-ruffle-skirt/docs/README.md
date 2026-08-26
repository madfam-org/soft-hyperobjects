# Can-Can Ruffle Skirt

The high-kick **can-can** skirt: a full gathered skirt on a fitted waistband, faced underneath with tier upon tier of net ruffles (the *froufrou*) that flash when the hem goes overhead, closing at a Yantra4D `hook-and-eye`. Made to measure to waist and hip girths. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The can-can skirt is a chorus-line staple almost always improvised from a bought skirt with net safety-pinned underneath, which sags on the first kick because the tiers were cut flat. Drafting it with a solved ruffle stack gives a small company a reproducible, fitted, launderable garment for the cost of the net.

## Provenance

The can-can skirt is the costume of the 1890s Parisian dance-hall chorus (Moulin Rouge, Folies Bergère): the point is the *froufrou* — a wall of white net ruffles revealed on the high kick and the grand écart.

## The tier solve

Each ruffle tier is cut to the skirt's circumference **at its own level** times the fullness:

```
tier_len(level) = skirt_circ_at(level) · ruffle_fullness
```

A lower tier is longer than an upper one because the skirt is a cone. Cutting them all equal (the naive error) strains the low tiers and droops the high ones.

## The closure handshake

The waistband closes on the Yantra4D [`hook-and-eye`](https://yantra4d.com); `closure_rows` drives the hook columns and `waistband_height` drives the drafted placket and the `wb_closure` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `skirt` | 1 | flared skirt body (CB closure) |
| `ruffle` | 1 (per schedule) | net ruffle tier (widest drafted) |
| `waistband` | 1 folded | fitted waistband with the hook closure |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
La falda de can-can de patada alta: una falda amplia sobre una pretina, forrada con capas de olanes de tul (el froufrou), cerrando con un `hook-and-eye`. Hecha a medida a cintura y cadera. Carril 9 de FC-500.

## Français
La jupe de french cancan : une jupe ample sur une ceinture, doublée de volants de tulle (le froufrou), fermant par une agrafe `hook-and-eye`. Faite sur mesure aux tours de taille et de hanches. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

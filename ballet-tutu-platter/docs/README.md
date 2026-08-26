# Platter Tutu

The classical **platter** (pancake) tutu: a short, stiff, near-horizontal disc of gathered net standing straight out from the hip, built on a boned **basque** hip yoke and closing at a centre-back Yantra4D `hook-and-eye`. Made to measure to waist and hip girths. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A classical tutu is one of the most expensive and least reproducible garments a ballet company owns — each built by hand from tacit workroom knowledge, in a fixed size. Encoding the platter's real construction as a parametric object lets a company draft it to a specific dancer and reproduce it, preserving endangered making-knowledge.

## Provenance

The platter (pancake) tutu is the Petipa-era classical form (*Sleeping Beauty*, *Swan Lake*): a short stiff horizontal disc on a boned basque, held rigid by a covered steel hoop — distinct from the softer Romantic bell tutu. The construction here follows that workroom tradition: a firm basque, tiered net at high fullness, a hoop near the plate edge.

## The gather solve

Each net tier is a full ring gathered onto the basque hem; its flat cut length is the basque hem times a **fullness** ratio, and the ratio is what makes the net stand:

```
tier_flat = basque_hem · fullness   (fullness 2×–6×; a platter wants a lot)
```

declared against the basque hem with the fullness as gathered ease — the net's standing power is proven arithmetic.

## The closure handshake

The centre back closes on the Yantra4D [`hook-and-eye`](https://yantra4d.com); `closure_rows` drives the hook columns and `basque_depth` drives the drafted CB placket (built to the measured slanted basque CB) and the `cb_closure` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `basque` | 2 mirror | boned hip yoke |
| `tier` | per schedule | net tier (gathered onto the basque) |
| `placket` | 2 | CB hook-and-eye placket |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
El tutú de plato clásico: un disco corto, rígido y casi horizontal de tul fruncido sobre un canesú con ballenas, que cierra al centro de la espalda con un `hook-and-eye`. Hecho a medida a cintura y cadera. Carril 9 de FC-500.

## Français
Le tutu plateau classique : un disque court, rigide et quasi horizontal de tulle froncé sur un basque baleiné, fermant au milieu du dos par une agrafe `hook-and-eye`. Fait sur mesure aux tours de taille et de hanches. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

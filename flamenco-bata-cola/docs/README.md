# Flamenco Bata de Cola

The **bata de cola**: the trained flamenco dress whose skirt sweeps into a long ruffled tail (the *cola*) that the dancer throws and controls with the legs. A fitted bodice over a gored skirt that grows from a front hem to a floor-plus train at the back, edged with a cascade of ruffles (*volantes*), closing at a centre-back Yantra4D `hook-and-eye`. Made to measure to bust, waist, hip and length. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The bata de cola is the single most technique-defining garment in flamenco, and it cannot be bought off a rack: its weight and sweep are what the dancer moves against. Encoding its construction as a parametric object keeps a living dance tradition affordable and its endangered making-knowledge documented.

## Provenance

The bata de cola is the trained dress of the *escuela bolera* and the danced *soleá* / *alegrías*: the cola is not decoration but an instrument moved with the legs. It is **always** made to measure — the weight and sweep must match the body, which is why a stock-size bata de cola does not exist.

## The tail solve

The skirt is a set of gores whose length grows from the front to `front_length + tail_length` at the back — a drafted sweep, not a level hem. Gores share **equal side seams** so they sew together whatever the flare, and the ruffle is gathered onto the swept hem at `ruffle_fullness`, declared as gathered ease so the cascade length is proven.

## The closure handshake

The centre back closes on the Yantra4D [`hook-and-eye`](https://yantra4d.com); `closure_rows` drives the hook columns and `bodice_length` drives the drafted placket and the `cb_closure` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `bodice_front` | 1 on fold | fitted front |
| `bodice_back` | 2 mirror | fitted back (CB hook) |
| `gore` | N | skirt gores (the sweep) |
| `ruffle` | 1 | volante (gathered onto the hem) |
| `placket` | 2 | CB hook-and-eye placket |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
La bata de cola: el vestido flamenco de cola, corpiño ajustado sobre falda de nesgas que barre en una larga cola de volantes, cerrando al centro de la espalda con un `hook-and-eye`. Siempre a medida. Carril 9 de FC-500.

## Français
La bata de cola : la robe flamenca à traîne, corsage ajusté sur jupe à lés balayant en une longue traîne à volants, fermant au milieu du dos par une agrafe `hook-and-eye`. Toujours sur mesure. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

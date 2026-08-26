# ECG-Electrode Monitoring Vest

A close-fitting compression vest that holds ECG electrodes at measured positions against the torso and routes their leads, between a **shell** and a **lining**, to a single recorder pocket. Made to measure to chest/bust girth. FC-500 lane 8 (e-textile & smart garments III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 8 — e-textile & smart garments III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> **This is a garment pattern, not a medical device.** It positions electrodes and routes leads. It does not measure, monitor, or diagnose anything, and makes no clinical claim.

> Ambulatory monitoring is done with adhesive electrodes that itch, peel, and fail within a day. A washable vest holding reusable, printable electrode carriers at measured positions turns a two-day consumable into a garment a clinic or family can repair.

## The dead-length solve

A monitoring vest works only if the electrodes stay put, so the shell **compresses**. But an electrode carrier is rigid and cannot stretch. Its footprint plus margin is a **dead length** that takes no stretch, so the compression comes out of the *live* remainder only:

```
dead  = electrode_count · (electrode_dia + 2·electrode_margin)
live  = chest_ring − dead
shell = dead + live · (1 − compression)
```

Drafted naively as `chest·(1−compression)` the shell is short by `dead·compression` and the electrodes rock on a ring stretched across them — motion artefact, not signal. The dead island is capped at 55% of the ring (at the extremes it exceeds the ring entirely). The lining eases gentler than the shell (clamped), so it never pulls the electrodes off their marks.

## The electrode handshake

The carrier is the Yantra4D [`snap-electrode-carrier`](https://yantra4d.com). `electrode_dia` drives the carrier's `disc_dia` (its `sew_face` flange) **and** the drafted seat window **and** the garment's `electrode_seat` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `shell` | 1 on fold | compression shell (holds the electrodes still) |
| `lining` | 1 on fold | electrode seats + channel routing |
| `pocket` | 1 | recorder pocket where traces converge |

Electrode seats, sew rings, channel traces and the pocket entry are **marked**; no electrode, conductor, recorder, or circuit is drafted. Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un chaleco de compresión que sostiene electrodos ECG en posiciones medidas y encamina sus cables entre capa y forro hasta una bolsa de grabador. Es un patrón de prenda, no un dispositivo médico. Hecho a medida al contorno de pecho. Carril 8 de FC-500.

## Français
Un gilet de compression tenant des électrodes ECG à des positions mesurées et acheminant leurs fils entre coque et doublure vers une poche d'enregistreur. C'est un patron de vêtement, non un dispositif médical. Fait sur mesure au tour de poitrine. Couloir 8 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

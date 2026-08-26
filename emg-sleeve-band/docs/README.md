# EMG-Electrode Sleeve Band

A tapered compression band worn on the forearm or bicep that clamps a pair of EMG electrodes to a muscle belly at a measured spacing and routes their leads to a connector tab. The standalone sibling of the ECG vest. Made to measure to two limb girths. FC-500 lane 8 (e-textile & smart garments III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 8 — e-textile & smart garments III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> **This is a garment pattern, not a medical device.** It positions and clamps electrodes and routes leads. It does not measure, monitor, or diagnose, and makes no clinical claim.

> Surface EMG electrodes taped to a moving limb slide, and a sliding electrode gives motion artefact, not muscle signal. A band cut to a real, tapered limb at a solved grip holds two electrodes at a chosen spacing over a chosen muscle — cleaner signal from a repairable band.

## The dead-length grip solve

The band grips by negative ease, but the two electrode carriers are rigid and cannot stretch. Their combined footprint plus margins is a **dead length** that takes no stretch, so the grip comes out of the *live* remainder only, computed per girth:

```
dead = 2 · (electrode_dia + 2·electrode_margin)
live = limb_girth − dead
band = dead + live · (1 − grip)
```

Drafted naively as `limb·(1−grip)` the band is short by `dead·grip` and the electrodes rock. The dead island is capped at 55% of the girth (at the extremes two big electrodes on a thin limb make `dead` exceed the girth). The band is a **trapezoid** — a limb is a cone — solved proximal-to-distal.

## The electrode handshake

The carrier is the Yantra4D [`snap-electrode-carrier`](https://yantra4d.com). `electrode_dia` drives the carrier's `disc_dia` (its `sew_face` flange), the drafted seat, and the band's `electrode_seat` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `band` | 1 | tapered band with two electrode seats + channel |
| `tab` | 1 | connector tab where the leads exit |

The electrode seats, sew points, channel, dead-length markers and the tab lead-path are **marked**; no electrode, conductor, or circuit is drafted. Every piece verifies watertight at defaults and at every parameter min/max.

## Español
Una banda de compresión cónica que sujeta un par de electrodos EMG a un vientre muscular con separación medida y encamina sus cables a una lengüeta. Es un patrón de prenda, no un dispositivo médico. Hecho a medida a dos contornos del miembro. Carril 8 de FC-500.

## Français
Une bande de compression conique qui plaque une paire d'électrodes EMG sur un ventre musculaire à un écartement mesuré et achemine leurs fils vers une patte. C'est un patron de vêtement, non un dispositif médical. Fait sur mesure à deux tours du membre. Couloir 8 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

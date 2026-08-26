# Sensor-Mount Cycling Jersey

An aero-fit cycling jersey with a **rigid sensor seat**: a Yantra4D `sensor-mount-plate` sits on a stabilised non-stretch island at the lower back, its lead routed between the layers to the standard three rear cargo pockets. A real racing cut — long tail hem, forward sleeves, full-length zip front. Made to measure to chest/bust and waist girths. FC-500 lane 8 (e-textile & smart garments III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 8 — e-textile & smart garments III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> **This is a garment pattern, not a device.** It seats a mount plate and routes a lead. It contains no sensor, battery, or circuit and makes no measurement claim.

> Cycling telemetry is sold as sensors that clip to the bike or stick to the skin, and the jersey stays dumb. This cartridge makes the jersey the instrument mount: a printable plate on a stabilised island, fitted to a real body, with a lead routed to the pockets a rider already uses.

## The stabilised seat

A sensor plate is rigid and screws down flat, but the jersey is a stretch knit at negative ease. If the plate is sewn onto stretching cloth it rocks and the reading drifts. So the plate sits on a **fused non-stretch island** (`plate + margin`) — a dead length that takes none of the negative ease. `plate_w`/`plate_d` drive the carrier's `base_w`/`base_d`, the drafted island and seat, and the garment's `sensor_seat` interface.

## The racing tail

The tail drops the **centre-back hem** below the side hem, so the side seam and the whole upper structure exactly match the front — the tail is length added only at centre back, never on the side, so the side seam always balances.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front` | 2 mirror | front (CF zip) |
| `back` | 1 on fold | back with the sensor island + racing tail |
| `sleeve` | 2 mirror | short sleeve (cap solved to armscye) |
| `pocket_band` | 1 | rear cargo pocket band |

The sensor island, the plate seat, its four screw points, the lead trace and the pocket band are **marked**; no sensor, conductor, battery, or circuit is drafted. Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un jersey de ciclismo aero con asiento rígido de sensor: una `sensor-mount-plate` sobre una isla estabilizada en la espalda baja, con su cable a los tres bolsillos traseros. Es un patrón de prenda, no un dispositivo. Hecho a medida a pecho y cintura. Carril 8 de FC-500.

## Français
Un maillot de cyclisme aéro avec assise rigide de capteur : une `sensor-mount-plate` sur un îlot stabilisé dans le bas du dos, son fil vers les trois poches arrière. C'est un patron de vêtement, non un dispositif. Fait sur mesure aux tours de poitrine et de taille. Couloir 8 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

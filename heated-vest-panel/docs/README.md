# Heated Vest Panel

A vest whose front and back carry **heating panels**: serpentine channels routing a flexible heating element across the chest and kidneys, housed in a Yantra4D `led-channel` extrusion so the element sits protected rather than loose against the body, fed from a battery/controller pocket at the hem. Made to measure to chest/bust girth. FC-500 lane 8 (e-textile & smart garments III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 8 — e-textile & smart garments III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> **This is a garment pattern, not an appliance.** It routes and houses a heating element in a channel. It contains no heater, battery, or controller and makes no thermal claim.

> Heated apparel is sold as a sealed product with the element sewn permanently into a fixed-size shell. This cartridge separates the garment from the electronics: the routing is a channel the element slides into, the carrier is a printable commons part, and the pass count is solved so the heat is even.

## The routing solve

A heating panel covers an *area*, but a strip element has a *length*, so the serpentine run must cover the panel at the strip's own pitch:

```
passes = panel_h // strip_pitch
run    = passes·panel_w + (passes − 1)·strip_pitch
```

`strip_pitch` is floored at `strip_w + 12 mm` so passes never overlap the element. Under-route and cold stripes appear; over-route and the element bunches at the turns — the solve avoids both.

## The channel handshake

The channel carrier is the Yantra4D [`led-channel`](https://yantra4d.com) extrusion. `strip_w` drives the carrier's `strip_width` **and** the drafted channel width **and** the garment's `heat_channel` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front` | 2 mirror | front panel with the chest heat channel |
| `back` | 2 mirror | back panel with the kidney heat channel |
| `battery_pocket` | 1 | battery/controller pocket at the hem |

The heat panel, the serpentine channel centre-line, the lead exit and the pocket entry are **marked**; no heater, conductor, battery, or circuit is drafted. Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un chaleco cuyo frente y espalda llevan paneles calefactables en serpentina, alojados en una extrusión `led-channel`, alimentados desde una bolsa de batería. Es un patrón de prenda, no un electrodoméstico. Hecho a medida al contorno de pecho. Carril 8 de FC-500.

## Français
Un gilet dont le devant et le dos portent des panneaux chauffants en serpentin, logés dans une extrusion `led-channel`, alimentés depuis une poche de batterie. C'est un patron de vêtement, non un appareil. Fait sur mesure au tour de poitrine. Couloir 8 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

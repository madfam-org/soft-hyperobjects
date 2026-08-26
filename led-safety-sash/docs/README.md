# LED Safety Sash

A high-visibility sash worn diagonally across the torso, carrying a lit LED strip along its whole length in a Yantra4D `led-channel` extrusion so the strip is protected and diffused rather than loose, with a small battery pocket at the lower end and a side-release loop so it goes on over any jacket. Made to measure to chest/bust girth and torso height. FC-500 lane 8 (e-textile & smart garments III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 8 — e-textile & smart garments III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> **This is a garment pattern, not a light.** It houses and routes an LED strip in a channel. It contains no LED, battery, or circuit and makes no lighting or certification claim.

## The diagonal-span solve

A shoulder-to-hip sash is longer than a horizontal band: it is the **hypotenuse** of the torso drop and the cross-body reach.

```
cross_reach = chest_bust_girth · 0.5
diagonal    = hypot(torso_height, cross_reach)
sash_len    = diagonal · overlap
```

Cut to a horizontal girth the sash rides up over the shoulder and the light points at the sky. Cut to the diagonal, it actually crosses the body — and the LED channel is cut to that measured run.

## The channel handshake

The channel carrier is the Yantra4D [`led-channel`](https://yantra4d.com) extrusion. `strip_w` drives the carrier's `strip_width` **and** the drafted channel width **and** the sash's `led_channel` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `sash` | 1 | the sash body with the LED channel down its centre |
| `loop` | 2 | shoulder loop tabs (bar-tacked around the buckle) |
| `battery_pocket` | 1 | battery pocket at the lower end |

The LED channel centre-line, its two stitch lines, the battery lead and the pocket entry are **marked**; no LED, conductor, battery, or circuit is drafted. The sash is a single continuous piece with attached tabs; every drafted piece verifies watertight at defaults and at every parameter min/max.

## Español
Una banda de alta visibilidad en diagonal por el torso, con una tira LED a todo su largo en una extrusión `led-channel`, una bolsa de batería y un lazo lateral. Es un patrón de prenda, no una lámpara. Hecha a medida al contorno de pecho y a la altura del torso. Carril 8 de FC-500.

## Français
Une écharpe de haute visibilité en diagonale sur le torse, avec une bande LED sur toute sa longueur dans une extrusion `led-channel`, une poche de batterie et une boucle latérale. C'est un patron de vêtement, non une lampe. Faite sur mesure au tour de poitrine et à la hauteur du torse. Couloir 8 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

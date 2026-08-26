# Cable-Conduit Harness Tee

A wearable cable harness in the form of a tee: cable bundles run **along the seams** — the strongest, least-flexing lines of a garment — held off the skin in Yantra4D `seam-conduit-clip` bundles clipped into the seam allowances, converging at a junction pocket. Made to measure to chest/bust and waist girths. FC-500 lane 8 (e-textile & smart garments III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 8 — e-textile & smart garments III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> **This is a garment pattern, not a wiring loom.** It routes and clips cable bundles along the seams. It contains no cable, connector, or circuit and makes no electrical claim.

> Everyone who builds wearable electronics hits the same wall: the wiring has nowhere to live, so it gets taped or hot-glued to the inside of a garment where it snags and can never be washed. This tee makes the seam a cable race by design — the infrastructure the field lacks.

## The clip-count solve

A conduit clip holds the bundle at intervals; too few and it sags, too many and the seam stiffens. The clip count on each seam is solved from the seam's **measured** length:

```
clips = round(seam_length / clip_pitch)
```

so spacing stays constant whatever the body size. The seam allowance is floored to hold the clip tab plus the bundle.

## The conduit handshake

The clips are the Yantra4D solid [`seam-conduit-clip`](https://yantra4d.com). `tab_w` drives the clip's `seam_tabs` flange **and** the drafted clip footprint **and** the tee's `seam_conduit` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front` | 2 mirror | front (side-seam cable race) |
| `back` | 1 on fold | back (side-seam cable race) |
| `sleeve` | 2 mirror | sleeve (underseam cable race) |
| `junction` | 1 | junction pocket where bundles converge |

The conduit clip positions, the in-seam cable traces and the junction entry are **marked**; no cable, connector, or circuit is drafted. Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un arnés de cable ponible con forma de playera: los haces corren por las costuras en clips imprimibles `seam-conduit-clip`, convergiendo en una bolsa de unión. Es un patrón de prenda, no un mazo de cables. Hecho a medida a pecho y cintura. Carril 8 de FC-500.

## Français
Un harnais de câble portable en forme de tee : les faisceaux courent le long des coutures dans des clips imprimables `seam-conduit-clip`, convergeant vers une poche de jonction. C'est un patron de vêtement, non un faisceau électrique. Fait sur mesure aux tours de poitrine et de taille. Couloir 8 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

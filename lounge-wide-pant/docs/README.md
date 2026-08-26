# Wide-Leg Lounge Pant

A pull-on **wide-leg** lounge trouser: generous front and back legs, an **elastic-casing waistband** (no fly, no button), inseam and outseam, and deep patch pockets. It closes with a waist elastic, so it carries **no hardware** — the honest pure-pattern case the FC-500 plan reserves for pull-on lounge wear. Made to measure to waist, hip and inseam length. FC-500 lane 7 (intimates & loungewear III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 7 — intimates & loungewear III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The pull-on wide-leg trouser is the most-worn garment in a lounge, maternity, or accessibility wardrobe, sold in a grid that fixes the leg width and the rise together. This cartridge separates them — rise, leg ease and hem sweep are three independent numbers — which matters most for the bodies the size grid serves worst.

## Width is three independent numbers

| Parameter | Controls |
| :-- | :-- |
| `rise` | how high the crotch sits below the waist |
| `leg_ease` | positive ease at the hip, carried down the whole leg |
| `hem_width` | the ankle sweep — straight column or flare |

## The seam that must match

The inseam point is a **shared x** for front and back, so the two inseams are the same length and sew together without twisting the leg (the classic wide-trouser error). The front/back difference lives entirely in the rise curve — a scooped front, a fuller back seat — which are the CF/CB seams, not shared. The inseam and outseam are declared front-to-back and verify at every extreme.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front_leg` | 2 mirror | front leg (scooped rise) |
| `back_leg` | 2 mirror | back leg (seat room) |
| `waistband` | 1 | elastic-casing waistband |
| `pocket` | 2 | deep patch pockets |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un pantalón amplio de descanso que se pone sin cierre: piernas generosas, una pretina de jareta con elástico (sin bragueta ni botón), entrepierna y costado, y bolsas de parche profundas. Hecho a medida a cintura, cadera y largo de entrepierna. Carril 7 de FC-500.

## Français
Un pantalon large d'intérieur à enfiler : jambes généreuses, une ceinture à coulisse élastique (sans braguette ni bouton), entrejambe et côté, et poches plaquées profondes. Fait sur mesure aux tours de taille, de hanches et à l'entrejambe. Couloir 7 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

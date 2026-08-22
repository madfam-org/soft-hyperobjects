# Underwire Bra

A three-piece-cup underwire bra: two lower cup sections and one upper section build projection out of stable cloth with two cones at right angles, seated in a cradle whose upper edge carries the wire channel, on a negative-ease band closing at a centre-back hook-and-eye. Made to measure to underbust and bust girths. FC-300 lane 3 (structured intimates).

Part of the **Fashion Cabinet Commons** (FC-300, lane 3 — structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Underwire fit is the hardest problem in ready-to-wear lingerie, and the industry solves it by rounding bodies to a size grid. This cartridge solves it dimensionally instead: the cup is computed from a wearer's own underbust and bust, and the cradle's wire channel is solved to the exact arc of the printable wire that will be threaded through it, so the wire, the channel and the cup mouth are one number rather than three approximations.

## The wire handshake

The underwire itself is **not** modelled here — it is the Yantra4D solid
[`bra-underwire`](https://yantra4d.com), referenced through the manifest's
`notion.hardware_ref`. Fashion Cabinet draws the *channel* the wire lives in, and
that channel is **solved** to the wire's own arc rather than drawn near it:

| Quantity | Symbol | Source |
| :-- | :-- | :-- |
| Wire chord (tip to tip) | `cup_width` | garment parameter → hardware `cup_width` |
| Wire sweep | `sweep_deg` | garment parameter → hardware `sweep_deg` |
| Arc radius | `R = cup_width / (2 sin(θ/2))` | solved |
| Channel run | `L = R θ` | solved — the drafted `wire_line` edge |

Both mapped parameters drive the hardware's `cradle_seam` **flange** interface *and*
the garment's own `wire_line` interface, which is what makes this a dimensionally
coupled handshake rather than a slug that merely resolves. At defaults the chain is
`wire_run 246.64 mm = cradle.wire_line 246.62 mm = cup mouths 246.62 mm` — one
dimension, checked by `declare_seam`, not three approximations.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `cup_lower_inner` | 2 pairs | lower cup, inner section — half the solved mouth |
| `cup_lower_outer` | 2 pairs | lower cup, outer section — the other half + side rise |
| `cup_upper` | 2 pairs | upper section, elastic neckline, strap tab |
| `cradle` | 2 pairs | the wired frame; `wire_line` carries the channel |
| `band` | 2 pairs | negative-ease underband (the load path) |
| `back` | 2 pairs | back wing to the centre-back hook |

Every sewn relationship is declared and verifies at delta `+0.00`.

## Español
Un sostén con varilla de copa en tres piezas: dos secciones inferiores y una superior construyen la proyección a partir de tela estable con dos conos en ángulo recto, asentadas en una base cuyo canto superior lleva el canal de la varilla, sobre una banda de holgura negativa que cierra con broches al centro de la espalda. Hecho a medida al contorno bajo el busto y al busto. Carril 3 de FC-300 (lencería estructurada).

> El ajuste con varilla es el problema más difícil de la lencería industrial, y la industria lo resuelve redondeando los cuerpos a una tabla de tallas. Este cartucho lo resuelve dimensionalmente: la copa se calcula desde el bajo busto y el busto propios de quien la viste, y el canal de varilla de la base se resuelve al arco exacto de la varilla imprimible que se enhebrará en él.

## Français
Un soutien-gorge à armatures au bonnet en trois pièces : deux sections inférieures et une section supérieure construisent la projection à partir d'un tissu stable par deux cônes à angle droit, assises dans un berceau dont le bord supérieur porte la coulisse d'armature, sur une bande à aisance négative fermée par une agrafe au milieu dos. Fait sur mesure aux tours de dessous de poitrine et de poitrine. Couloir 3 de FC-300 (lingerie structurée).

> L'ajustement à armatures est le problème le plus difficile de la lingerie industrielle, et l'industrie le résout en arrondissant les corps à une grille de tailles. Ce cartouche le résout dimensionnellement : le bonnet est calculé à partir du dessous de poitrine et de la poitrine propres à la personne, et la coulisse d'armature du berceau est résolue sur l'arc exact de l'armature imprimable qui y sera enfilée.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

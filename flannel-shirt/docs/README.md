# Flannel Shirt · Camisa de Franela

**FC-100 rank #76.** The classic brushed-cotton casual flannel button-up — a
relaxed woven shirt whose signature is that the cloth is **plaid** and the craft
is **matching the pattern across every seam**. Structurally it is the
[dress-shirt](../../dress-shirt/) family solved for a soft, roomy flannel:
a CF button-stand front with a curved shirttail hem, a back that ends at a yoke
seam, a yoke carrying the back neck and shoulders, a set-in sleeve with a barrel
cuff, and a two-piece turndown collar (stand + fall).

*La clásica camisa casual de franela de algodón cepillado — una camisa de tejido
plano holgada cuya firma es que la tela es **de cuadros** y el oficio es **casar
el patrón en cada costura**. Estructuralmente es la familia de la camisa de
vestir resuelta para una franela suave y amplia.*

## Pieces · Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front | Delantero | 2, mirrored — CF button stand, curved tail, pocket trace |
| `back` | Back | Espalda | 1 on fold — ends at the yoke seam, deeper curved tail |
| `yoke` | Yoke (doubled) | Canesú (doble) | 1 on fold — back neck + both shoulders |
| `sleeve` | Sleeve | Manga | 2, mirrored — cap solved to the armholes, placket slit |
| `cuff` | Cuff | Puño | 2 — barrel cuff, folded double at mid |
| `stand` | Collar Stand | Pie de Cuello | 2 on fold — solved to the neckline + overlap |
| `fall` | Collar Fall | Cuello | 2 on fold — chained to the stand's top edge |
| `pocket` | Chest Patch Pocket | Bolsa de Parche al Pecho | 1 — chamfered pouch, plaid-snapped |
| `flap` | Pocket Flap | Tapa de Bolsa | 1 — echoes the pocket, buttoned |

## The plaid-matching model (the signature) · El modelo de casado de cuadros

Flannel is a **tartan grid** of repeat `plaid_repeat` (default 40 mm). True
pattern matching is a fabric-and-cutting craft; this cartridge carries it three
ways so the draft stays honest:

1. **Match-point notches.** The front and back share **one** side-seam
   construction (`front.side == back.side`, verified), so whole-`plaid_repeat`
   notches placed down that seam land on the **same physical points** on both
   pieces — align the notches and the plaid lines meet. Repeat-spaced match
   notches also sit on the `yoke.bottom ↔ back.top` seam and the `sleeve.cap`.
2. **Grid-snapped pocket + flap.** The chest pocket's top-left corner is
   **snapped to whole plaid repeats** (measured from the body origin), so when
   the pocket is cut on-grain on the *same* grid its tartan reads continuous
   with the body behind it. The flap echoes the pocket, 2 mm wider each side.
3. **A yardage matching allowance.** Plaid matching wastes cloth. The BOM adds
   **one plaid repeat of length per matched seam** (side ×2, yoke/back,
   armholes ×2, collar → 6 seams) on top of the marker length, and reports the
   uplift as a percentage. `plaid_repeat` drives the notch spacing *and* this
   allowance, so a bigger check honestly costs more cloth.

*La franela es una retícula de tartán con repetición `plaid_repeat`. El casado
se lleva con piquetes de coincidencia sobre la costura lateral compartida, una
bolsa ajustada a la retícula del cuadro, y una tolerancia de metraje de una
repetición por costura casada (reportada como porcentaje).*

## Construction order · Orden de construcción

1. Cut every piece **on-grain on the same plaid grid**; transfer all notches.
2. Make the chest pocket (turn the hem facing, press) and topstitch it to the
   front at the snapped placement; attach the flap above it.
3. Sew the **yoke to the back** (`yoke.bottom ↔ back.top`), matching notches;
   the yoke is doubled and encloses the seam.
4. Join **fronts to yoke at the shoulders** (`front.shoulder ↔ yoke.shoulder`).
5. Build the collar: solve/sew the **fall to the stand's top edge**, then the
   **stand to the neckline** (`stand.neck ↔ front.neck + yoke.neck`, ease = the
   15 mm button overlap). Set the collar to the neck.
6. Set the **sleeves** into the armholes (`sleeve.cap ↔ front.armhole +
   back.armhole`, zero ease), matching the shoulder notch and the plaid notch.
7. Close each **underarm + side** in one run
   (`sleeve.underarm_front ↔ sleeve.underarm_back`, `front.side ↔ back.side`),
   matching every plaid notch down the side.
8. Mark and sew the **sleeve placket**, attach the **barrel cuffs**.
9. Hem the **curved shirttail**; work the buttonholes and sew the buttons.

## Honest simplifications (teaching-grade) · Simplificaciones honestas

- The **full back armhole is drafted on the back piece**; real shirts split the
  armhole across the back and the yoke. The shoulder point still meets the front.
- The **pocket, flap, and collar fall are single-layer** in v0 (the real garment
  doubles them). The barrel cuff is cut double and folded at mid.
- The **curved shirttail is a symmetric bézier**, not a drafted sweep; set
  `shirttail_drop = 0` for a straight hip-length hem.
- **Plaid matching is expressed as notches, a grid-snapped placement, and a
  yardage allowance** — the tartan itself is a fabric/render property, not
  drafted thread-by-thread here. Matching still depends on cutting every piece
  on the same grid, which the notches and the pocket snap make checkable.
- **Hardware federates to [Yantra4D](https://yantra4d.madfam.io)** (shank-button
  family): buttons are a notion reference in the BOM, never re-implemented here.

## Fabric · Tela

`felpa-algodon` — soft brushed cotton (the flannel). Napped, so it sheds while
sewing; match the thread to the dominant plaid ground.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

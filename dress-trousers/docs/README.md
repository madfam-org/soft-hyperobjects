# Dress Trousers — FC-100 rank #36

The **chinos block refined for tailoring** (`projects/chinos`, trouser block
family): front/back legs (cut 2 each) with the front inseam bowed by the same
solved bisection to match the deeper back fork, equal side seams by
construction, and the grown-on fly extension with fly J-topstitch guide and
fly-stop notch carried over unchanged. What the refinement changes:

- **Pleated front** — the flat chino front gains two pleat markings per leg:
  the main pleat on the crease line (two fold lines `pleat_depth` = 25 mm
  apart meeting the waist, bridged by a depth rung) and a secondary pleat
  40 mm toward the side, 15 mm wide.
- **Straight side-entry pockets** — the diagonal slash opening is replaced by
  a straight 150 mm opening span marked on the side seam, with a pair of
  pocket notches on the side edge.
- **Sharper taper** — hem half-width 95 mm (chinos: 105), back +12 as usual.
- **Full-length creases** — front and back creases run hem → waist and carry
  the grainline (grain on the crease, tailoring convention).
- **Back double-besom pockets** — two parallel welt lines 130 mm long and
  12 mm apart, drawn as a closed welt window below the two back waist darts.
- **Extended waistband with crossover tab** — the band is cut as two halves:
  the tab half extends +60 mm into a crossover tab with a button cross-mark
  and a tab line, and its bottom edge is verified against front + back waists
  with the tab (60 mm + 2 × seam allowance) declared as seam ease; the plain
  half eases only its end seam allowances.
- **Blind hem** — 40 mm hem allowance for a blind-stitched finish.

v0 simplifications: pleats and besom pockets are **markings only** — no pleat
intake is added to the waist edge and no welt, jet, or pocket-bag pieces are
drafted; a construction guide (pleat fold order, besom welting, tab underlay
and buttonhole) is future work. The fly zipper federates to a Yantra4D notion
via the `fly` (zipper_tape) interface rather than being drafted here.
Fabrics: `materials/popelina-algodon` as stand-in — the suiting-wool card is
pending.

```bash
python apps/api/services/engine/fc_runner.py projects/dress-trousers/main.py dress-trousers.svg '{}' svg
```

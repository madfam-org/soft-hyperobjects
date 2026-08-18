# Suit Trousers — FC-100 rank #68

The **dress-trousers block finished as the trouser half of a suit**, cut in
worsted wool suiting (`materials/lana-peinada-traje`). It carries over from
`projects/dress-trousers` (and, underneath it, `projects/chinos`): front/back
legs (cut 2 each) with the front inseam bowed by a solved bisection to match
the deeper back fork, equal side seams by construction, the grown-on fly
extension with a fly J-topstitch guide and a fly-stop notch, full-length front
and back creases carrying the grainline, and the two-half tab waistband. What
the suit finish adds:

*El bloque del pantalón de vestir terminado como la mitad inferior de un traje,
cortado en lana peinada de sastrería.*

## The suit-trouser signature: pleats cut into the waist

The dress-trousers block drew its pleats as **markings only** and explicitly did
*not* add pleat intake to the waist edge. A proper suit trouser does the
opposite, and this cartridge makes it honest:

- The front leg is drafted **wider at the waist by the total pleat intake**
  (`pleat_count × pleat_depth`, default 2 × 30 = 60 mm). The forward pleats fold
  that surplus toward centre front so the waist reads to the measured waist.
- The two waistband halves are drafted to the **pleated-flat waist**
  (`measured front.waist + back.waist − total pleat intake`), so the pleat
  intake is genuinely eased into the band. It is **declared as waistband seam
  ease**: with defaults the tab half's ease is `TAB(60) + 2×SA(20) − intake(60)
  = +20 mm` and the plain half's is `2×SA(20) − intake(60) = −40 mm`. Both seams
  verify to delta ≈ 0 — the waist stays balanced whether you pick one pleat or
  two, at any girth.

## Pieces

| id | piece | cut |
|----|-------|-----|
| `front` | Front Leg — pleated waist, grown-on fly, slant pocket, full-length crease, cuff line | 2, mirror |
| `back` | Back Leg — two waist darts, single-welt back pocket, full-length crease, cuff line | 2, mirror |
| `waistband_tab` | Waistband half with the +60 mm crossover tab and hook-and-bar mark | 1 |
| `waistband_plain` | Plain waistband half | 1 |

## What the finish adds beyond dress-trousers

- **Forward pleats declared as ease** (above) — one or two, `pleat_count`.
- **Full-length front *and* back creases** — both run hem → waist; the front
  crease carries the grainline (grain on the crease, tailoring convention).
- **Single-welt back pocket** — one closed welt window below the darts (a suit
  trouser welts singly where the chino patch-pocketed and the dress trouser
  double-besomed).
- **Slant side-entry pockets** — a 155 mm opening on the side seam with a pair
  of pocket notches.
- **Cuffed or plain hem** — `cuff_depth` (default 40 mm). A cuff is a turn-up:
  above 0 it draws a cuff turn-up line and a cuff notch, and the hem allowance
  is automatically raised to clear a full turn-up (`2 × cuff_depth + 10`).
  Set `cuff_depth = 0` for a plain, blind-hemmed bottom.
- **Optional knee-length front lining** — the `lined` checkbox adds a lining
  line to the BOM (silesia/bemberg fronts lined to the knee to stop the wool
  bagging). The lining is **noted, not drafted** in v0.
- **Hook-and-bar + tab button** waist closure at the tab half.

## Construction order (teaching-grade)

1. Interface the waistband stay and the fly shield; press.
2. Sew and press the back darts; work the single back welt pocket at its mark.
3. Fold and press the forward pleats toward centre front; baste at the waist.
4. Set the slant side pockets; join the fronts to the backs at the side and
   inseam (equal by construction), press seams open.
5. Insert the fly on the grown-on extension (zipper to the fly stop, J-topstitch
   to the guide).
6. Join the two waistband halves to the waist, easing the pleat intake in;
   finish the crossover tab with the hook-and-bar and the tab button.
7. Hem: plain blind hem, or turn up and secure the cuff at the cuff line.
8. **Press the creases hard** — set the full-length front and back creases with
   steam. A sharp crease is the suit trouser.

## Honest simplifications (v0)

- Pleats, welt, and pocket openings are **markings** — no welt/jet, pocket-bag,
  fly-shield, or cuff pieces are drafted; the pleat *intake* is handled as waist
  width + declared ease, but the fold construction is a guide, not geometry.
- The waistband is a folded rectangle, not a curtained/canvassed waistband.
- The lining is noted in the BOM, not drafted.
- **Hardware federates to Yantra4D**: the fly zipper (via the `fly` /
  `zipper_tape` interface), the trouser hook-and-bar, and the tab button are
  Yantra4D notion cartridges referenced in the BOM notes, never re-implemented
  here.
- Worsted wool tailors true to pattern (no stretch compensation) but must be
  pre-shrunk (steam / London-shrink) before cutting — see the fabric card.

```bash
python apps/api/services/engine/fc_runner.py projects/suit-trousers/main.py suit-trousers.svg '{}' svg
# one pleat, plain hem, unlined, larger block:
python apps/api/services/engine/fc_runner.py projects/suit-trousers/main.py alt.svg '{"pleat_count": 1, "cuff_depth": 0, "lined": false, "hip_girth": 1160}' svg
```

Official visualizer and configurator: Fashion Cabinet.

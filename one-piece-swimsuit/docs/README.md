# One-piece Swimsuit — FC-100 rank #54

The commons' hardest swim garment: a continuous full-torso **maillot** — a
leotard with legs — drafted on negative ease so the four-way-stretch tricot
grips the whole body when wet. The front runs from the neckline down through
the bust and torso to the crotch; the back runs from the shoulders down to the
crotch; they meet at a **crotch gusset** and at the shoulder and side seams.

_El enterizo de baño: torso continuo con holgura negativa. El delantero baja
del escote a la entrepierna; el trasero baja de los hombros a la entrepierna;
se encuentran en un refuerzo de entrepierna y en las costuras de hombro y
costado._

## The fit-critical dimension — the torso loop

A swimsuit fails or fits on its **vertical torso length**, not its width. The
loop that runs from the shoulder down the front, through the crotch, and up the
back is drafted **shorter than the body** (a length negative ease — "the suit
stretches to fit torso length"). This cartridge derives the front centre run,
the back centre run and the gusset span from `torso_girth × (1 − torso_neg_ease)`
and **checks the loop closes** at render time (drafted = target, delta ≈ 0). The
width negative ease (`negative_ease_pct`) separately grips bust and hip. Both are
sliders and both are reported in the metadata — the numbers swimwear makers keep
on private spec sheets.

## Pieces

- **Front (self)** — fold-cut half (CF on the fold): crotch, high-cut leg, side,
  armhole, shoulder/strap, deep-scoop neckline, CF centre. Elastic-finished leg,
  armhole and neck (zero allowance, marked zones).
- **Back (scoop / racer)** — fold-cut half (CB on the fold): same topology,
  fuller-coverage leg, and a `back_style` that digs the armhole in for a racer.
- **Front lining** — mirrors the front outline, cut in shell or mesh; swimsuits
  are front-lined.
- **Gusset (self + lining)** — half-trapezoid on the fold, cut twice. Its front
  edge (width = gusset front) and back edge (width = gusset back) equal the body
  crotch edges **by construction** — the same proven-at-render trick as the
  bikini panty.

## Seams (all declared, all balanced at render time)

| Seam | Balances by |
| --- | --- |
| gusset front_edge ↔ front crotch | construction (equal half-widths) |
| gusset back_edge ↔ back crotch | construction (equal half-widths) |
| front shoulder ↔ back shoulder | shared strap landmarks |
| front side ↔ back side | shared underarm + hip landmarks |

Front and back share the underarm height, the hip corner and the high-point
shoulder, so the shoulder and side seams close with delta 0. The torso loop
closes because each centre edge runs the full crotch→neckline height and the two
runs plus the gusset span are derived from the reduced torso girth.

## Construction order

1. Front to front lining: baste wrong-sides together at neckline, armholes and
   legs; from here they behave as one layer.
2. Front(+lining) to back at the **side seams** (stretch/overlock).
3. Close the **crotch**: gusset (self + lining) sandwiches the front and back
   crotch edges; the front is caught between the two gusset layers, the back
   topstitched or burrito-rolled.
4. Join the **shoulders / straps**.
5. Elastic-finish neckline, armholes and legs: cut each elastic to the exact
   length in the BOM, join in a ring, quarter-mark, zigzag into the marked zone,
   then coverstitch. Pull-on — **no hardware**.

## Honest simplifications (teaching-grade, documented not hidden)

- **No bust or waist darts.** The 4-way-stretch tricot molds shaping out; a woven
  or a structured cup version would need them. Bust support here is the front
  lining, not a shelf bra or cups.
- The **front lining** shares the full front outline (including the leg) rather
  than a partial bust-to-hip lining panel; trim the lining leg back in production
  if a lighter finish is wanted.
- The **strap** is grown onto both front and back (no separate strap piece); the
  shoulder seam is the join. Adjustable/back-crossed straps are a later variant.
- Front and back share one underarm depth and hip line so the side seam is a
  straight balanced segment; a contoured side-seam panel is a refinement.
- The gusset side (leg) edge is caught flat under the leg elastic, as on the
  bikini panty.

```bash
python apps/api/services/engine/fc_runner.py projects/one-piece-swimsuit/main.py one-piece.svg '{}' svg
# racer back, larger frame:
python apps/api/services/engine/fc_runner.py projects/one-piece-swimsuit/main.py racer.svg '{"back_style":"racer","torso_girth":1650}' svg
```

Official visualizer and configurator: Fashion Cabinet.

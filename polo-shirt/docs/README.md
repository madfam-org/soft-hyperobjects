# Polo Shirt — FC-100 rank #3

The tee knit block grown into tier 2: six pieces, two solvers, one marked
placket. What this cartridge adds over the crew-neck tee:

1. **The collar is solved, not drawn.** `build_collar` bisects the flat neck
   length of a half collar (cut 2 on fold at CB) until its curved neck edge
   equals half the measured neck opening — zero overlap, the placket carries
   the closure. A halves-on-both-sides seam check (`collar.neck` vs
   `front.neck + back.neck`) enforces it at render time. The pointed front
   edge angles 20 mm outward from the solved flat length.
2. **The placket is marked, not guessed.** Two vertical placement lines run
   from the CF neck point down `placket_length` (the CF-side line rides the
   fold, the second sits `placket_width` away), with three buttonhole drill
   crosses evenly spaced on the box centerline. A separate backing strip —
   (`placket_length` + 30) × (2 × `placket_width`), cut 1 — faces the slash.
3. **The sleeve cap is solved** with the tee's exact bisection against the
   front + back armholes, and the hem is finished with a derived rib cuff:
   sleeve hem × 0.85 + two seam allowances, 2 × 25 mm high, cut 2.

Suggested fabric: [`materials/jersey-algodon`](../../../materials/jersey-algodon/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/polo-shirt/main.py polo.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/polo-shirt/main.py polo.json '{"chest_girth": 1140}' json
```

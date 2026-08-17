# Turtleneck Sweater — FC-100 rank #40

Slim cut-and-sew knit turtleneck (tier 4, knitwear family). Reuses rank #6's
solved sleeve cap on a slimmer block (ease 90, front neck drop 55 / back 15 so
the funnel sits close) and extends the derived-rib rule to a tall funnel
collar:

- **collar length** = neck opening × `collar_ratio` (0.75 — turtlenecks need
  strong negative ease to hug) + 2 × seam allowance
- **collar piece height** = 2 × `collar_height` + 2 × seam allowance
  (≈ 236 mm at defaults). The tube folds double when sewn and is worn folded:
  **finished height = `collar_height`** (110 mm). The piece is cut at 2× the
  finished height — do not "fix" the rectangle to 110.

Cuffs run deeper than the crew (ratio 0.72, finished 70 mm); the hem band is
short (0.88, 45 mm). Shoulder seams carry stabilizer-tape placement traces.
Quarter notches on the collar's bottom edge distribute the negative ease onto
the neckline. Suggested fabric: `materials/felpa-algodon` or
`materials/jersey-algodon` (body) + 1x1 rib for collar and bands.

```bash
python apps/api/services/engine/fc_runner.py projects/turtleneck-sweater/main.py turtle.svg '{}' svg
```

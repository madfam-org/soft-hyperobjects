# Scrubs Top (Filipina Médica) — FC-100 rank #85

Boxy woven medical top: front/back on fold, straight-line V-neck, set-flat
short sleeve, derived V-neck facing, chest patch pocket. Three things this
cartridge encodes:

1. **Woven ease.** The same drop-shoulder block family as the tee, but poplin
   does not stretch: 160 mm total ease (vs the tee's 60) is what produces the
   boxy scrubs fit. `knit_negative_ease` is off — this block never compresses.
2. **The sleeve cap is solved, not drawn.** `build_sleeve` bisects the
   half-biceps width until the cap curve's measured length equals the front +
   back armhole lengths at zero cap ease (drop-shoulder wovens sew flat); a
   multi-edge seam check enforces it at render time.
3. **The V-neck facing is derived.** Strip length = measured front + back neck
   opening × 2 + two joining allowances, cut 70 mm tall for a 35 mm finished
   facing — the construction rule, not a fixed number. The pocket placement is
   traced on the front as an internal marking.

Suggested fabric: [`materials/popelina-algodon`](../../../materials/popelina-algodon/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/scrubs-top/main.py scrubs.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/scrubs-top/main.py scrubs.json '{"chest_girth": 1140}' json
```

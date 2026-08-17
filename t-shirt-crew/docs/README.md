# T-shirt (Crew Neck) — FC-100 rank #1

Relaxed drop-shoulder knit tee: front/back on fold, set-flat sleeve, rib
neckband. Two things make this cartridge the FC-100's teaching example:

1. **The sleeve cap is solved, not drawn.** `build_sleeve` bisects the
   half-biceps width until the cap curve's measured length equals the front +
   back armhole lengths (a multi-edge seam check enforces it at render time).
   Change any body measurement and the sleeve re-solves.
2. **The neckband is derived.** Band length = measured neck opening ×
   rib ratio (default 0.85) — the pattern encodes the construction rule, not
   a fixed number.

Suggested fabric: [`materials/jersey-algodon`](../../../materials/jersey-algodon/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/t-shirt-crew/main.py tee.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/t-shirt-crew/main.py tee.json '{"chest_girth": 1100}' json
```

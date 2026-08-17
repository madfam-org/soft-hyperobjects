# T-shirt (V-neck) — FC-100 rank #27

Rank #1's relaxed drop-shoulder knit block with a V front neckline and a
mitered V-neckband. Three things distinguish this cartridge from
[`t-shirt-crew`](../../t-shirt-crew/docs/README.md), whose block family it
belongs to:

1. **The V is a true V.** The front neck is one straight stitch line from the
   centre front at `v_depth` (default 140 mm below HPS) up to the shoulder
   neck point — a single `fc.Line`, not a flattened curve — with a "V point"
   notch at the CF end. A manifest **error** constraint keeps
   `v_depth < body_length / 4`.
2. **The band is derived AND mitered.** Band length = measured neck opening ×
   0.82 (V-bands need more negative ease than crews) + two seam allowances.
   The centre-V miter is marked twice: a notch on the band's bottom edge at
   its midpoint and a "miter fold" cross at the band centre, where the band
   folds and stitches into the V.
3. **Back and sleeve are rank #1's, exactly.** The sleeve cap is still solved
   by bisection until its measured length matches the front + back armholes
   (multi-edge seam check, tol 2.0 mm).

Suggested fabric: [`materials/jersey-algodon`](../../../materials/jersey-algodon/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/t-shirt-v-neck/main.py vee.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/t-shirt-v-neck/main.py vee.json '{"v_depth": 170}' json
```

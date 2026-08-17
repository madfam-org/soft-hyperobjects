# Camisole — FC-100 rank #44

Strappy knit camisole with a slight A-line flare, front/back on fold. The
front top edge is a straight-ish neckline rising to a narrow strap attachment
point (notched); the back top edge is nearly straight. Both top edges carry
**zero seam allowance** — they are finished with one binding strip derived
from the measured openings × the stretch ratio (default 0.92) + 2 seam
allowances. Straps are two separate 24 mm strips sewn into 8 mm spaghetti
(`strap_length` is the cut length, tuck-in included); no fabric strap is
drafted on the body pieces. Underarm edges are turned under the regular seam
allowance and stitched. v0 drafts a straight-grain knit; a bias-cut woven
variant is a preset concern. Suggested fabric: `materials/jersey-algodon`.

```bash
python apps/api/services/engine/fc_runner.py projects/camisole/main.py cami.svg '{}' svg
```

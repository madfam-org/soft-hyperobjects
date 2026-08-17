# Blouse (Blusa) — FC-100 rank #21

Darted woven top: front/back on fold with scoop and shallow necks, side bust
darts + back waist darts as internals, gathered-cap short sleeve, derived neck
facing, CB button-loop keyhole. Three things this cartridge encodes:

1. **Darts stay internal; the side seam is common.** The side bust dart
   (intake 25, length 110) and the back waist dart pair (intake 12, length
   100 — one internal on the fold half, mirrored into the pair) are classic
   triangle polylines. Both pieces share one fitted side-seam curve
   (skirt-block's shared-point trick), so `front.side ↔ back.side` matches by
   construction and the waist shaping absorbs the dart differences.
2. **The gathered cap is solved WITH its ease.** `build_sleeve` bisects the
   half-biceps width until the cap measures front + back armholes **plus**
   `gather_ease` (default 30 mm); the multi-edge seam check carries
   `ease=gather_ease`, so verification proves the extra length is intentional.
   Gather start/stop notches sit at t = 0.35/0.65 with a gather-zone bar
   marked under the crown.
3. **Closure and facing are derived, not drawn.** The neck facing strip is
   the measured opening × 2 + two joining allowances, cut 60 mm tall; the CB
   keyhole is a half-U internal on the fold (the mirror completes it) with a
   button cross-mark — the button itself is a hard notion, federated out
   (Yantra4D ref), never redrafted here.

Suggested fabric: [`materials/popelina-algodon`](../../../materials/popelina-algodon/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/blouse/main.py blouse.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/blouse/main.py blouse.json '{"bust_girth": 1060}' json
```

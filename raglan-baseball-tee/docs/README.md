# Raglan Baseball Tee — FC-100 rank #74

The commons' **first raglan geometry**. A raglan has no shoulder seam: the
sleeve runs all the way to the neckline, so the body pieces lose their
shoulder edge and the neck opening is shared by *three* pieces.

## How the raglan is drafted

**Body (front/back, cut 1 on fold each).** Edges are `center, neck, raglan,
side, hem` — no shoulder. The neckline is shortened: it spans only the CF/CB
portion, from the fold to the raglan point `RP` at `x = raglan_neck_w`
(default 45 mm). From `RP` a long, gently hollowed bezier — the `raglan`
edge — runs down to the underarm at `(W, underarm_y)`. The back `RP` sits
higher than the front one because the back neck drop is shallower, so the
back raglan measures slightly longer than the front raglan.

**Sleeve (cut 2, mirrored).** Drafted flat: its top is a short `sleeve_neck`
arc (length = `sleeve_neck_len`, default 70 mm — the remaining neckline arc
bridging the two raglan points) flanked by `front_raglan` and `back_raglan`
edges that descend to the underarm corners, then tapered `underarm_front` /
`underarm_back` seams to a 3/4-length baseball wrist. **Both raglan edges are
solved, not drawn**: with endpoints fixed, a control-point bulge is bisected
until each sleeve raglan's measured length equals its measured body raglan
(one solve per side; the back solves to a fuller curve because its target is
longer). Seam checks enforce the match at render time with 2 mm tolerance.

## Neckline accounting

Per half-garment the opening is three arcs: `front.neck + back.neck +
sleeve_neck`. Two mirrored halves and two sleeves give

```
total = 2*(front.neck + back.neck) + 2*sleeve_neck
band  = total * neckband_ratio + 2*seam_allowance
```

At defaults that is a ~400 mm opening and a ~354 mm contrast rib band.

## Baseball styling

Classic colourway: body in one colour, **sleeves and neckband in contrast**
(the BOM splits fabric consumption accordingly). Notches differ by side —
single notch on the front raglan, double on the back — so the near-symmetric
cut pieces cannot be confused at the machine.

Suggested fabric: [`materials/jersey-algodon`](../../../materials/jersey-algodon/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/raglan-baseball-tee/main.py raglan.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/raglan-baseball-tee/main.py raglan.json '{"chest_girth": 1100}' json
```

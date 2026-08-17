# Casual Button-Down Shirt (Camisa Casual) — FC-100 rank #20

Relaxed drop-shoulder woven shirt, deliberately simpler than a dress shirt:
**no yoke, no collar fall**. Front cut 2, back cut 1 on fold, set-flat sleeve,
one-piece band collar. Four things this cartridge encodes:

1. **The button stand is geometry, not decoration.** The front's center edge
   is extended `button_stand` (30 mm) past CF; six buttonhole cross-marks sit
   on the CF line itself and the `button_stand` interface exposes the placket
   edge. The stand's cut edge folds back (`center` carries a hem-width
   allowance) and the chest patch-pocket placement is traced as an internal —
   the pocket piece itself federates to the `patch-pocket` enabler.
2. **The band collar is solved per half, overlap included.** Exactly the
   collar-band enabler rule: the half-collar (cut on fold at CB) has its neck
   edge bisected until it equals one front neck + half the back neck. The
   front neck edge deliberately starts 15 mm past CF (the `OVERLAP` — the
   band's button line, mid-stand), so the per-half seam check
   `collar.neck == front.neck + back.neck` closes at delta ≈ 0 with no
   bookkeeping: front cut 2 means its neck appears once per garment half; the
   on-fold back and collar each contribute their half.
3. **The sleeve cap is solved, not drawn.** Rank #85's bisection: half-biceps
   grows until the cap curve equals front + back armhole lengths at zero cap
   ease (drop-shoulder wovens sew flat). Short 240 mm by default; the
   long-sleeve preset (600 mm) reuses the same solve. Plain hem, no cuff.
4. **The box pleat is a marking in v0.** Two internal fold lines 30 mm apart
   at CB top, 120 mm long, on the half-draft (mirrored across the fold at cut
   time). It documents the pleat position without adding pleat intake — the
   fullness comes from the relaxed 180 mm ease.

Suggested fabrics:
[`materials/popelina-algodon`](../../../materials/popelina-algodon/material.json),
[`materials/manta-cruda`](../../../materials/manta-cruda/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/casual-button-down/main.py shirt.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/casual-button-down/main.py shirt.json \
  '{"chest_girth": 1180, "sleeve_length": 600}' json
```

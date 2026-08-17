# Shirt Dress (Vestido Camisero) — FC-100 rank #26

The casual button-down ([rank #20](../../casual-button-down/)) lengthened into
a dress: same drop-shoulder woven block, **no yoke, no collar fall**, carried
to mid-calf (`body_length` 1050) with a gentle A-flare. Front cut 2, back cut
1 on fold, set-flat sleeve, one-piece band collar, tie belt with loops, and
in-seam pocket bags. What this cartridge encodes:

1. **The A-flare starts at the waist, in one shared side edge.** The side runs
   straight from the underarm to the waist line (nape-to-waist 410 on the
   block), then a G1 Bezier flares to a hem half-width of chest quarter +
   `flare_mm` (70). Front and back use the SAME construction, so the declared
   `front.side == back.side` check closes exactly even through the curve.
2. **The nine-button stand is the parent's placket, extended.** The center
   edge is extended `button_stand` (30 mm) past CF for the full dress length;
   nine buttonhole cross-marks sit on the CF line from 60 mm below the neck to
   150 mm above the hem (~97 mm pitch at defaults), and the `button_stand`
   interface exposes the placket edge. The chest patch-pocket trace of the
   parent is dropped — this dress pockets at the seams instead.
3. **The band collar and sleeve cap are solved, not drawn — verbatim from the
   parent.** The half-collar (cut on fold at CB) has its neck edge bisected
   until it equals one front neck + half the back neck, with the front neck
   deliberately starting 15 mm past CF (the band's button line), so
   `collar.neck == front.neck + back.neck` closes at delta ≈ 0. The sleeve cap
   is bisection-solved to the measured front + back armholes at zero cap ease
   (short 220 mm default; the winter preset reuses the solve at 600 mm).
4. **In-seam pockets are notches plus one bag silhouette.** Both side seams
   carry `pocket opening top/bottom` notches spanning 160 mm centered at hip
   level (200 mm below the waist), with the notch fractions computed from the
   actual side-edge arc length — they stay put when the flare or length
   changes. The bag is ONE symmetric rounded pouch (~160×180) with a straight
   `opening` edge, cut 2 mirrored (one per side) in v0; production doubles the
   layers from the same pattern piece. A single piece needs no opening seam
   check — both layers are cut from it, so the lengths match by construction.
5. **The tie belt is self-fabric and pieced.** A 60 mm strip 2.4× the chest
   girth (waist proxy, robe rule) cut 1 with a center-back piecing notch —
   poplin is 1450 mm wide, so the belt joins at CB by design. Two 50×12
   loop strips hang it at the `waist / belt loop` side notches.

Suggested fabric:
[`materials/popelina-algodon`](../../../materials/popelina-algodon/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/shirt-dress/main.py dress.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/shirt-dress/main.py dress.json \
  '{"chest_girth": 1120, "sleeve_length": 600}' json
```

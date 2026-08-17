# Pajama Set (Pijama, conjunto) — FC-100 rank #41

The commons' first **TWO-GARMENT cartridge**: one object drafts a complete
sleep set — a button-front pajama top and a relaxed pull-on pajama pant.
Five things this cartridge encodes:

1. **One cartridge, two garments, three modes.** `target_piece` selects
   `"top"`, `"pants"`, or `"set"` (both; the default and the fallback for
   unknown values), and the manifest exposes the same three as modes. Piece
   names are namespaced per garment (`top_front` vs `pant_front`, …) so the
   full set coexists in one `PatternSet` with no collisions, and every seam
   check is declared only among the pieces actually rendered — a top-only
   render never references a pant edge and vice versa.
2. **The top is the casual-button-down block, softened for sleep.** Same
   drop-shoulder woven geometry at lounge ease (180 mm total): front cut 2
   with the center edge extended `button_stand` (28 mm) past CF — four
   buttonhole cross-marks on the CF line, chest patch-pocket trace — and a
   plain on-fold back (no box pleat; the ease is the fullness). The classic
   pajama notched collar is deliberately **simplified to the solved band
   collar** inherited from casual-button-down: half on fold at CB, neck edge
   bisected until it equals one front neck (15 mm overlap included) + half
   back neck, so `collar.neck == top_front.neck + top_back.neck` closes at
   delta ≈ 0. Neck girth is derived from chest (250 + 0.15 × chest, clamped
   300–520) — one slider fewer on a garment nobody measures a collar for.
3. **The sleeve is long and its cap is solved, not drawn.** The rank #85
   bisection at zero cap ease, defaulting to 580 mm (pajama-length), plain
   hem, no cuff.
4. **The pants are the sweatpants block at lounge ease.** Separate front and
   back legs cut 2 each, deeper back fork with the front inseam bowed outward
   by a solved amount to match it, equal side seams by construction, straight
   open hems with a 25 mm allowance.
5. **The casing carries elastic AND a drawstring; the BOM totals both
   garments.** The waistband strip is cut to the measured waist, folds at
   half height around `elastic_width` + seam allowance, and carries two
   drawstring-exit crosses 40 mm apart straddling the middle of its length —
   center front, since the band-end seam is worn at CB. The BOM is computed
   over all seven pieces regardless of the rendered mode (`set_note`:
   "two garments, one cartridge; BOM totals both"): one popelina marker at
   1450 mm width and 65% efficiency, elastic, drawstring cord, buttons
   (hard goods federate to Yantra4D), interfacing, thread.

Suggested fabrics:
[`materials/popelina-algodon`](../../../materials/popelina-algodon/material.json),
[`materials/manta-cruda`](../../../materials/manta-cruda/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/pajama-set/main.py set.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/pajama-set/main.py top.json \
  '{"target_piece": "top", "sleeve_length": 600}' json
python apps/api/services/engine/fc_runner.py projects/pajama-set/main.py pants.svg \
  '{"target_piece": "pants", "hip_girth": 1120}' svg
```

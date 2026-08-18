# Camp-Collar Shirt (Camisa de Cuello Camp) — FC-100 rank #77

The relaxed, open-collar resort shirt — the **camp collar** (also *Cuban* or
*convertible* collar), the family of the guayabera and the short-sleeve
warm-weather shirt. A woven-tops sibling of the casual button-down (rank #20):
the same drop-shoulder block and the same one-piece-per-half collar solve, but
the collar lies **flat and open** instead of standing as a band. Pieces: front
(cut 2), back (cut 1 on fold), short sleeve (cut 2), camp collar (cut 2 on
fold — upper + under), chest pocket (cut 1). Five things this cartridge encodes:

1. **The camp collar is one flat piece, solved to the neckline.** The half
   collar (cut on fold at CB) has its neck edge bisected until it equals one
   front neck + half the back neck — the collar-band enabler rule. But where a
   band *stands* narrow and tall, this collar body is **wide and flat**
   (`collar_width`, 85 mm default): it extends outward from the neck seam and
   folds open over the shoulders. Its front edge breaks to a forward **collar
   point** (`collar_point`, 55 mm); the gap between the two mirrored collar
   fronts, over the open placket, is the camp **"V" notch** at CF. The neck
   seam `collar.neck == front.neck + back.neck` closes at delta ≈ 0.1 mm.
2. **The neckline is drafted open.** A camp collar rolls open at the throat
   rather than buttoning up, so the front neck drop is deeper (100 mm) than a
   dress neckline. The front neck edge still starts 15 mm past CF (the
   `OVERLAP`, the placket button line), so the per-half seam check closes with
   no bookkeeping: the front is cut 2 (its neck appears once per garment half);
   the on-fold back and collar each contribute their half.
3. **The button placket leaves the top open.** The front's center edge is
   extended `button_stand` (30 mm) past CF as a folded-edge placket; six
   buttonhole cross-marks sit on the CF line. Camp convention wears the **top
   button open** (the collar rolls over it), so the topmost mark is a reference
   point — sew five or six as you like.
4. **The sleeve is short and set flat.** Rank #85's bisection: half-biceps
   grows until the cap curve equals front + back armhole at zero cap ease
   (drop-shoulder wovens sew flat). Short 230 mm by default, with a turn-up
   cuff-fold marking; the long-sleeve preset (600 mm) reuses the same solve.
5. **Boxy body, side vents, real pocket.** Straight relaxed hem (200 mm ease);
   a side-vent slit is marked on both side seams above the hem; the chest patch
   pocket is both traced on the front (placement) and drafted as its own cut
   piece with an angled bottom point and a top-facing fold line.

### Honest simplifications (teaching-grade)

- The camp collar is a **single flat piece**. Some industrial camp/Cuban
  collars carry a tiny separate under-stand at CB to lift the back neck; here
  the one-piece flat draft is the teaching form (upper + under cut from the
  same piece on fold).
- The **side vent and pocket placement are markings**, not cut-away detail; the
  straight hem is v0 (no shirttail curve).
- The sleeve **turn-up cuff is a fold line**, not a separate banded cuff.
- Buttons are **hardware**: they federate to the Yantra4D button family via the
  BOM note and are never re-implemented in this kernel.

Suggested fabrics:
[`materials/popelina-algodon`](../../../materials/popelina-algodon/material.json)
(crisp cotton poplin) or
[`materials/manta-cruda`](../../../materials/manta-cruda/material.json)
(cotton muslin/canvas, a linen-look camp shirt).

```bash
python apps/api/services/engine/fc_runner.py projects/camp-collar-shirt/main.py shirt.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/camp-collar-shirt/main.py shirt.json \
  '{"chest_girth": 1200, "collar_width": 110}' json
```

Official visualizer and configurator: **Fashion Cabinet**.

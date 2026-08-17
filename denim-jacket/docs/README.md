# Denim Jacket — FC-100 rank #28

Trucker-style denim jacket ("chamarra de mezclilla") in `materials/mezclilla-denim`,
built on the dress-shirt architecture but cropped and boxy (`body_length` 620,
`woven_ease` 200). Front AND back split at the chest line: front yokes (cut 2)
over button-stand front bodies with six buttonhole cross-marks and chest
flap-pocket markings; back yoke and back body each cut on fold. A long sleeve
with buttoned rectangular cuffs, a solved band collar, and a two-half hem
waistband with a crossover tab.

Three solves, all declared and verified: the sleeve cap is bisected to the
measured front + back body armholes; the collar neck edge is bisected to the
measured half neckline (front yoke + back yoke) plus a 15 mm button overlap
(the collar-band enabler's method, carried as declared ease); and each
waistband half is verified against `front_body.hem + back_body.hem` with the
tab extension + end allowances as declared ease. Nine seam relationships are
checked in the full set.

**v0 honesty notes:**

- **Flap pockets are markings.** The chest flap + pocket rectangles and the
  attach line are internal markings only; real flap, welt/bag, and lower
  hand-pocket construction pieces are future work.
- **Armholes live on the body pieces.** Both armholes start at the yoke-seam
  corner and are drafted fully on the bodies; the yokes keep straight side
  edges clear of the armhole (the dress-shirt back-armhole precedent, applied
  to both sides). The drafted armhole depth is clamped to
  `chest_line + 70` so the yoke seam never crosses it — that is why the
  default `chest_line` is 150 rather than a lower-chest 180.
- **Band accounting.** The bodies end at the band seam (the band supplies the
  finished 45 mm hem height). Front is cut 2, back on fold, so each band half
  covers one front hem + the half back hem; the tab half extends +50 mm with a
  button cross-mark and both halves carry their end seam allowances in the
  declared ease (dress-trousers method).
- **One-piece collar.** A single band collar (height 70, folds in wear) solved
  to the neckline; a true two-piece trucker collar with a separate stand is
  future work.
- **Buttonhole distribution.** The six CF buttonholes are assigned to the
  front yoke or front body automatically by each mark's height relative to
  the chest seam.
- **Cuff opening** is a slit marking with a drill stop, not a bound placket.
- **Topstitching** (metadata note): double-needle heavy contrast thread on
  yoke seams, button stand, flap and pocket edges, band, and cuffs.
- **Buttons are hardware** — a Yantra4D cartridge (`shank-button` guide in
  this commons), referenced from the BOM, never re-implemented here.

```bash
python apps/api/services/engine/fc_runner.py projects/denim-jacket/main.py jacket.svg '{}' svg
```

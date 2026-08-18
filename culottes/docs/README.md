# Culottes — FC-100 rank #80

**Falda pantalón.** Culottes read as a **divided skirt**: the tailored trouser
block (`projects/dress-trousers`, trouser leg family) drawn **wide and cropped**
so the legs drape like a skirt rather than a pant. Front and back legs are cut
2 mirror each and join at the inseam and outseam; the straight cut-1 waistband
closes the top. Half-hem is flat ~300 mm (front) / 312 mm (back) and the inseam
is short (~380 mm default, knee-to-midcalf), the two proportions that make a
culotte a culotte instead of trousers or palazzo.

## What the block borrows and what it changes

- **Shared outer construction → matching outseam.** Front and back use the
  identical straight outseam (x = 0, hem → a common side-waist point), so the
  outseam matches by construction (delta 0). Both side seams reach the same
  height; the deeper back rise is taken up at the centre back, never at the
  side (trouser/skirt convention).
- **Solved front inseam.** The back fork is deeper (crotch ≈ 461 mm vs the
  front's 282 mm), so the front inseam is bowed by a bisection-solved bulge
  until front and back inseams are equal length (delta 0) — the same solver the
  dress-trousers front inseam uses.
- **Front knife pleats as verified ease.** Two knife pleats per front half fold
  toward centre front, each hiding 2× `pleat_depth`. The intake is drafted into
  the front waist edge (so the leg is wide) and then declared back to the band
  as seam **ease**, so the band still balances to the four unpleated waist edges
  at delta 0.
- **Centre-back invisible zip.** The back opens at centre back: the back
  `crotch` edge is a straight CB rise (hosting the zipper) into the fork bezier,
  with a **zipper-stop notch** at `zipper_length` down from the waist and a
  **hook-and-bar** drill cross above it at the CB waist.

## Pieces

| id | piece | cut |
|----|-------|-----|
| `front` | Front Leg | cut 2, mirror |
| `back` | Back Leg | cut 2, mirror |
| `waistband` | Waistband | cut 1 |

Each leg's named edges (CCW): `side` (outseam) · `waist` · `crotch` (front:
plain fork; back: CB rise + fork) · `inseam` · `hem`.

## Construction order

1. Press the two knife pleats on each front toward centre front; baste across
   the waist so each front waist presses down to its finished quarter.
2. Sew the centre-back rise seam and set the **invisible zipper** into it,
   closing at the zipper-stop notch.
3. Sew inseams (front↔back) and outseams (front↔back).
4. Attach the straight cut-1 **waistband** to the pleated-down waist, matching
   the side-seam and CF notches; the overlap carries the **hook-and-bar**.
5. Blind-hem each leg (40 mm allowance).

## Honest, teaching-grade simplifications

- The crotch fork is a **plain bezier** — no separate gusset piece.
- The back has **no waist darts**: a wide culotte's seat drape is carried by the
  fork and the side curve, so the only waist suppression is the front pleat
  intake (which keeps the band accounting to a single clean ease term).
- The outseam is **straight** (no hip-curve bulge); fullness lives in the wide
  hem and the inner extension. A hip-line notch still marks the balance point.
- The hem is a straight **blind-hem allowance**; no faced or cuffed hem.
- Hardware federates to **Yantra4D**: the CB invisible zipper (`cb_zip`,
  `zipper_tape` interface) and the hook-and-bar are Yantra4D cartridges
  referenced from the BOM, never drafted here.

Fabric: `materials/popelina-algodon` (cotton poplin). Parameter contract:
`project.json` + the `main.py` docstring.

Official visualizer and configurator: Fashion Cabinet.

```bash
python apps/api/services/engine/fc_runner.py projects/culottes/main.py culottes.svg '{}' svg
```

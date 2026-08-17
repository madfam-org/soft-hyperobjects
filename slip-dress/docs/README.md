# Slip Dress — FC-100 rank #46

The nightgown refined into outerwear ("vestido lencero"): a woven slip drafted
for **true-bias cutting**. Construction stays in the camisole family — front
and back drafted on the center fold, top edges carrying **zero seam
allowance** and finished with one binding strip derived from the measured
openings × 0.95 (woven bias binding barely stretches) + 2 seam allowances,
plus two 18 mm strap strips sewn into 6 mm spaghetti. What changes from the
gown:

- **45° grainline** — drawn with equal run and rise on both panels, so the
  printed diagonal *is* the straight grain when the piece lies on the bias.
- **Cowl-ish front neck** — a gentle inward sag toward CF (`front_drop`,
  default 115 mm) instead of a straight edge; on the bias it drapes soft.
- **Back V dip** — the back top edge is nearly straight; mirrored across the
  CB fold it leaves a small V dipping `back_drop` (default 55 mm).
- **Shaped side seam** — two tangent-continuous beziers through a gentle
  waist suppression computed from `bust_girth − waist_girth` (capped at
  25 mm per quarter) so the dress skims; a waist notch is placed at the same
  computed arc fraction on front and back. No slits, no gather zone.

## Bias-cutting guidance

- Trace the **full piece** (mirror across the center line) and cut **single
  layer**, face up, on a flat table — never on the fold and never doubled;
  bias layers creep against each other.
- Lay the pattern so the drawn 45° grainline runs parallel to the selvage.
  Weight, don't pin; cut with the fabric fully relaxed and unstretched.
- Handle cut panels flat. Stitch with a slight stretch on the seam, or
  stabilize the seamline with tissue, to keep bias seams from popping.
- **Let the dress hang 24 h** before marking and sewing the hem — bias drops
  unevenly, then re-true the hem line.
- The 12 mm allowance is a **French seam**: sew wrong sides together at 6 mm,
  trim, press, then right sides together at 6 mm, enclosing the raw edge —
  the right finish for fray-prone popelina.

Suggested fabrics: `materials/popelina-algodon` (crisp, casual) or
`materials/jersey-algodon` (drapes closer to a charmeuse slip; the bias note
still applies but jersey may also be cut on grain).

```bash
python apps/api/services/engine/fc_runner.py projects/slip-dress/main.py slip.svg '{}' svg
```

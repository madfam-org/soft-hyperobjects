# Bomber Jacket — FC-100 rank #29

The zip-hoodie (rank #14) architecture with the hood swapped for a **ribbed
stand collar**. The front is **cut 2 mirrored** — never on fold: its center
edge is the zipper seam, with a 15 mm tape allowance, top/bottom stop notches,
and a 7 mm stitch line (zipper-notion's installation convention). Each front
carries a **diagonal welt-pocket marking**: an exact 150 mm opening trace
(3-4-5 slope — upper end toward the side seam, lower end toward center front)
inside its welt construction surround box. The long sleeve cap is solved by
bisection against the measured armhole pair and seam-checked (tol 2.0), along
with sides, shoulders and underarms.

All three ribs are **derived — no solver, no seam check needed**:

- `collar_rib` (cut 1): full neck opening × `collar_ratio` (0.80) +
  2 × `seam_allowance`, cut 2 × `collar_height` tall and folded.
- `cuff_rib` (cut 2): sleeve opening × `cuff_ratio` (0.75), 2 × `cuff_height`.
- `hem_rib` (cut 1, **split for the zipper**): hem circumference ×
  `hem_ratio` (0.82) + 2 sa, with a center notch (= center back when worn)
  marking the open ends at the zipper.

Metadata derives `zipper_length_mm` (measured front center edge + hem rib
height, rounded to 10) with the ordering note, plus the optional MA-1 sleeve
utility-zip **zipper-garage** note; slider/pull hardware is a Yantra4D solid
federated through `projects/zipper-notion`. Fabric: `materials/felpa-algodon`
as the stand-in until the nylon-shell fabric card lands (`shell_note`).

```bash
python apps/api/services/engine/fc_runner.py projects/bomber-jacket/main.py bomber.svg '{}' svg
```

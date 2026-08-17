# Zip Hoodie — FC-100 rank #14

The pullover hoodie (rank #5) transformed for a full front zipper. The front
is **cut 2 mirrored** — never on fold: its center edge is the zipper seam,
with a 15 mm tape allowance, top/bottom stop notches, and a 7 mm stitch line
(zipper-notion's installation convention). The kangaroo pocket splits into
two mirrored halves with a faced hand opening, and the rib hem band is cut
split for the zipper — hem circumference × 0.85 + 2 sa, with a center notch
(center back when worn) marking the gap at the ends. The sleeve cap and the
two-panel hood remain solved by bisection against the measured armhole pair
and half neck opening — both seam-checked.

Metadata derives `zipper_length_mm` (measured front center edge + hem band
height, rounded to 10) with the ordering note; slider/pull hardware is a
Yantra4D solid federated through `projects/zipper-notion`. Fabric:
`materials/felpa-algodon`.

```bash
python apps/api/services/engine/fc_runner.py projects/zip-hoodie/main.py zip-hoodie.svg '{}' svg
```

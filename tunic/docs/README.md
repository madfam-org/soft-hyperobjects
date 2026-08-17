# Tunic — FC-100 rank #78

Flowing woven tunic, front and back cut on fold with the sleeve **integrated
into the body** (kimono/dolman cut): the shoulder line extends from the high
point of shoulder out to a wide short sleeve end, then the underarm curves
down and in to the side seam. No separate sleeve piece, no cap solver.

- **Side slits**: the side seam is sewn only from the underarm down to the
  slit top; a notch on each side edge marks it (default 180 mm above the hem).
- **Neck**: round bound neckline (front drop 90 mm, back 25 mm). The bias
  binding strip is derived: measured opening × 0.95 + 2 seam allowances.
- **Bound edge**: the neck carries zero seam allowance; hem and sleeve ends
  use the hem allowance. Suggested fabrics: `materials/popelina-algodon`,
  `materials/manta-cruda`.

Construction order: shoulder/sleeve-top seams → underarm + side seams down to
the slit notches → press slit allowances back and edgestitch → bind neck →
hem sleeve ends and bottom.

```bash
python apps/api/services/engine/fc_runner.py projects/tunic/main.py tunic.svg '{}' svg
```

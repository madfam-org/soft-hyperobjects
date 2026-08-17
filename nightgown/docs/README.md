# Nightgown — FC-100 rank #43

The camisole lengthened into a below-knee gown (`gown_length`, default
1150 mm) with a gentle A-flare (default 120 mm per quarter). Construction is
the camisole family's: front/back on fold, top edges carry **zero seam
allowance** and are finished with one binding strip derived from the measured
openings × the stretch ratio (default 0.92) + 2 seam allowances; straps are
two separate 24 mm strips sewn into 8 mm spaghetti. New to the gown:

- **Side slits** — the side seam is sewn from the underarm down to the
  slit-top notches, placed at the same computed arc fraction on the front and
  back side edges (`slit_height` above the hem, default 200 mm, clamped to a
  quarter of the gown); below the notches the seam allowances turn back as
  the slit facings.
- **Empire gather zone** (optional, `empire_gather`) — a horizontal "gather
  zone" marking line on the front, `bodice_line` (default 260 mm) below the
  strap point, for elastic or shirring under the bust.

Default fit carries +20 mm knit ease for lounge wear. Suggested fabrics:
`materials/jersey-algodon` (knit) or, with positive ease, woven
`materials/popelina-algodon`.

```bash
python apps/api/services/engine/fc_runner.py projects/nightgown/main.py gown.svg '{}' svg
```

# Henley — FC-100 rank #73

The collarless placket shirt: five pieces, one solver, one marked placket.
What this cartridge combines from its family:

1. **The rank #1 knit block, unchanged.** Front and back cut on fold with the
   crew tee's relaxed drop-shoulder draft; sides, shoulders and the multi-edge
   cap seam are declared and verified at render time.
2. **The polo's placket, without the collar.** Two vertical placement lines run
   from the CF neck point down `placket_length` — the CF-side line rides the
   fold (the slash opens on center), the second sits `placket_width` away —
   with three buttonhole drill crosses evenly spaced on the box centerline.
   The placket bottom is marked with an internal bar instead of an edge notch:
   the box bottom ends mid-piece at the fold, where an edge notch would be
   ambiguous. A separate backing strip — (`placket_length` + 30) ×
   (2 × `placket_width`), cut 1 — faces the slash.
3. **The band is the finish.** No collar: a rib neckband derived from the
   measured opening (full opening × `neckband_ratio` + two seam allowances,
   2 × `neckband_width` high) runs the FULL neckline, riding across the
   placket top, so the top button closes band against band.
4. **The sleeve is long, tapered and solved** — the tee's exact bisection
   against the front + back armholes, tapering to `wrist_opening` flat at the
   hemmed wrist.

Suggested fabric: [`materials/jersey-algodon`](../../../materials/jersey-algodon/material.json).

```bash
python apps/api/services/engine/fc_runner.py projects/henley/main.py henley.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/henley/main.py henley.json '{"chest_girth": 1120}' json
```

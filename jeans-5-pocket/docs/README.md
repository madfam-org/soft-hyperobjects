# Jeans (5-pocket) — FC-100 rank #2

The canonical **five-pocket jean** on the side-seamed trouser block (the same
frame as the chinos cartridge), graded by measurement and cut in denim.

## Pieces

- **Front Leg** (cut 2, mirror) — grown-on fly extension on the upper crotch
  that rejoins the fork curve with tangent continuity, a fly **J-topstitch**
  trace, a **fly-stop notch**, a curved **coin-pocket** (scoop) opening
  marking, and a pressed centre crease.
- **Back Leg** (cut 2, mirror) — its **top edge IS the yoke seam** (side→CB),
  the defining five-pocket feature. The straight back inseam hem is solved
  analytically so it matches the front inseam exactly. Carries a pentagon
  back-pocket placement marking and a centre crease.
- **Back Yoke** (cut 2, mirror) — the shaped wedge that removes waist
  suppression. Its **lower edge is built from the same two endpoints** as the
  back-leg yoke seam, so the two match by construction (seam delta ≈ 0).
- **Back Patch Pocket** (cut 2, mirror) — the classic pentagon pocket, with a
  topstitched upper-hem trace.
- **Fly Shield** (cut 1) — the rounded facing behind the fly.
- **Waistband (half)** (cut 2, mirror) — a straight band; the bottom edge is
  verified against the whole waist (2 fronts + 2 yokes) with the 40 mm
  button-stand overlap declared as seam ease.
- **Belt Loop** (cut 5) — 55 × 12 mm strips.

## Construction order (garment)

1. Serge/finish edges. Topstitch coin pocket to a front; set front pocket bags.
2. Sew the **back yoke** to each back leg (yoke seam), press up, topstitch.
3. Topstitch and set the **back patch pockets** on the yoked backs.
4. Join **inseams** and **out-seams** (front side ↔ back-leg side + yoke side).
5. Assemble the **fly** with the shield; insert zipper or work the button fly;
   topstitch the **J**.
6. Join the crotch seam; attach the **waistband**, add **belt loops**.
7. Set the **tack button** and **rivets**; hem; bar-tack the loops.

## Honest simplifications (teaching-grade)

- The coin pocket, back pocket and front slant pockets are **placement
  markings**; the pocket bags/facings (beyond the fly shield) are not drafted.
- Topstitching is represented as **guide traces**, not offset stitch lines.
- **Hardware is never modelled here**: the jeans **tack button**, the **copper
  rivets** and the **zipper** are Yantra4D hardware-cartridge references in the
  BOM (per the federation contract). The `fly_type` selector only switches the
  closure **note** (zipper vs button fly); the fork/fly geometry is identical.

## Seams (all verified, delta ≈ 0)

| Seam | side A | side B | ease |
|---|---|---|---|
| out-seam | front.side | back.side + yoke.side | 0 |
| inseam | front.inseam | back.inseam | 0 (solved hem) |
| **yoke** | yoke.lower | back.yoke_seam | 0 (shared endpoints) |
| waistband | waistband.bottom | 2×front.waist + 2×yoke.waist | 60 mm overlap |

Fabric: `materials/mezclilla-denim`.

```bash
python apps/api/services/engine/fc_runner.py projects/jeans-5-pocket/main.py jeans-5-pocket.svg '{}' svg
```

Official visualizer and configurator: Fashion Cabinet.

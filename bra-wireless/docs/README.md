# Wireless Bra (soft bralette) — FC-100 rank #11

A wire-free bra that shapes with **seams and stretch, never boning**. The support
is honest and in the open:

- **The underband is the primary support.** Its finished length is the underbust
  girth taken to a stated negative ease (`underbust_girth × (1 − negative_ease/100)`),
  so the band tensions around the ribcage and carries the load — not the straps.
  Bras run a high negative ease (default 18%, band elastic runs firmer still).
- **The bust is shaped by a curved cup seam.** Two cup halves (`cup_inner` +
  `cup_outer`) meet at a vertical seam that bows outward: sewing two curved edges
  cones the flat cloth into projection the way a dart would — the wire-free
  shaping trick. Both seam edges are the *same* curve, so they match to the
  micron.
- **Center-back hook closure.** The back wings wrap to a `hook-and-eye bra back
  (3×2)` at the marked center-back notch. Hardware is a **Yantra4D cartridge
  reference** (`notion.hardware_ref: yantra4d/hook-and-eye-3x2`), never modelled
  here. A pullover (no-hook) variant simply omits the closure and pulls on.
- **Adjustable straps.** Two straps run cup → over-shoulder → back on sliders and
  rings (also a Yantra4D reference); the strap `outer` length is a measured span,
  trimmed to fit after the slider is set.

## Pieces (Piezas)

| id | EN | ES | cut |
|----|----|----|-----|
| `cup_inner` | Cup — inner half | Copa — mitad interior | cut 2 pairs (mirror) |
| `cup_outer` | Cup — outer half | Copa — mitad exterior | cut 2 pairs (mirror) |
| `underband` | Underband | Banda inferior | cut 2 (mirror), CF seam → CB hook |
| `back` | Back wing | Ala trasera | cut 2 (mirror), CB hook |
| `strap` | Strap | Tirante | cut 2, adjustable |

## Construction order (Orden de construcción)

1. Sew each **cup seam** (`cup_inner.cup_seam` ↔ `cup_outer.cup_seam`) to cone the
   cups; press the seam toward the side.
2. Join the two cup bottoms to the **underband** front span (`underband.top_cup`);
   the notch marks cup centre.
3. Sew the **back wing** bottom to the underband back span (`underband.top_back`).
4. Close the **side seam** (`cup_outer.side` ↔ `back.side`) at the underarm.
5. Apply **elastic**: band elastic into the underband's lower zone (the primary
   support — join in a ring at CF, quarter-mark), then picot elastic into the
   neckline and armhole zones. Cut lengths come exact-mm from the BOM.
6. Attach **straps** with slider + rings; set length, trim.
7. Sew the **hook-and-eye** back to the center-back edges at the marked notch
   (skip for the pullover variant).

Every structural seam is a **declared seam check** (delta ≈ 0 at render time):
cup seam, both cup↔band spans, back↔band, side seam, and both strap tabs.

## Honest v0 simplifications (documented, not hidden)

- The cup is a **two-panel** wireless cup (inner + outer). It gives real seam-based
  shape but is not a full three-part balconette; there is no separate cradle/frame
  piece or wire channel — by design, this is a *soft* bralette.
- The underband and back wing are drafted as clean tapered panels; the band is one
  height around (no separately lowered back band).
- Strap ends are matched to short tabs by width; final strap length is set by the
  **slider hardware**, so the strap is declared as a hardware span rather than sewn
  to a fixed seam length.
- Support scales with the fabric: the default cotton/elastane jersey suits a light
  soft bra; for firmer wire-free support, add a **power-mesh lining** cut of the two
  cup pieces (noted in the BOM).

```bash
python apps/api/services/engine/fc_runner.py projects/bra-wireless/main.py bra.svg '{}' svg
```

Official visualizer and configurator: **Fashion Cabinet**.

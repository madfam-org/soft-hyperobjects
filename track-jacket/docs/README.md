# Track Jacket — FC-100 rank #51

The classic zip-up athletic jacket, drafted on the **zip-hoodie / bomber**
block and finished with a **solved stand collar**. The front is cut as **two
mirrored halves** (never on fold) whose center edge is the **zipper seam**: a
15 mm tape allowance, a 7 mm stitch line, and top/bottom stop notches, exactly
as the zip-hoodie established. The sleeve is **set-in**, its cap **solved by
bisection** against the measured armhole pair (with a small cap ease carried on
the seam). The cuff and the **split** hem band are rectangles derived from the
measured openings.

What makes it a track jacket rather than a bomber is the **stand collar**. It
is a funnel / mock-neck collar cut on fold at center-back whose **neck (inner)
edge is bisection-solved** — the collar-band method — to the **half** neck
opening, so the collar↔neckline seam balances to delta ≈ 0. Its center-front
edge carries the **same 15 mm zipper tape allowance** as the front center,
because the **separating zipper runs up through the collar**.

Fit is **relaxed**: a small **positive** ease (`relaxed_ease`) is added to the
chest girth. This is *not* a compression cut; the power-stretch interlock only
lends comfort give, so the fabric card's `cut_scale < 1.0` (negative ease) is
deliberately **not** applied — the metadata says so explicitly.

La chamarra deportiva con cierre clásica: el bloque de la sudadera con cierre /
bomber con un cuello alto **resuelto**. Delantero en dos mitades espejadas con
la costura del cierre al centro (margen de cinta de 15 mm, línea de pespunte a
7 mm, piquetes de tope), manga montada con copa **resuelta** a la sisa medida, y
puños + pretina dividida derivados de las aberturas. El cuello funnel/mao se
corta al doblez y su borde de cuello se **resuelve** a la mitad de la abertura;
su borde delantero lleva el margen de cinta porque el cierre separable sube a
través del cuello. Ajuste **holgado** (holgura positiva, no compresión).

## Pieces

- **Front (zip half)** (`front`) — cut 2 mirror, never on fold. Center edge is
  the zip seam (tape allowance + stitch line + stop notches). Optional front
  zip-pocket markings.
- **Back** (`back`) — cut 1 on fold at center-back.
- **Sleeve (set-in)** (`sleeve`) — cut 2 mirror. Cap solved to the armhole pair.
- **Stand Collar (funnel)** (`collar`) — cut 1 on fold at CB. Neck edge solved
  to the half opening; CF edge carries the zip tape allowance.
- **Cuff** (`cuff`) — cut 2, rib/elastic, length = sleeve hem × `cuff_ratio`.
- **Hem Band (split)** (`hem_band`) — cut 1, ends open at CF for the zipper;
  center-back notch marks the gap. Length = hem circumference × `hemband_ratio`.

## Construction order

1. If pockets are on, install the two front zip pockets at the marked openings
   **before** closing the fronts.
2. Sew shoulders (front↔back) and side seams (front↔back). Both balance to
   delta ≈ 0.
3. Set the sleeves: ease the solved cap into each armhole (one front + one back
   armhole per physical sleeve), then close each underarm seam.
4. Close each cuff into a ring and coverstitch to the sleeve hem (the cuff is
   drafted smaller — the rib recovers).
5. Join the collar into its stand: sew the solved neck edge to the neckline all
   the way round; the CF ends align with the front center edges.
6. Attach the split hem band across the whole hem, ends open at center front.
7. Install the **separating** zipper up the center front and through the
   collar; the derived `zipper_length_mm` is the length to order.

## Honest v0 simplifications (documented, not hidden)

- **Relaxed fit via positive ease, no negative-ease scaling.** Unlike the
  compression garments in this cluster (leggings, sports bra), a track jacket is
  relaxed, so fit is driven by `relaxed_ease` added to the chest — not by
  cutting under the body. The fabric card's `cut_scale < 1.0` is *not* applied.
- **Set-in cap ease** is carried as an exact `ease` on the cap↔armhole seam, so
  the cap is genuinely longer than the armhole pair and still balances to
  delta ≈ 0 — a real set-in cap, not a zero-ease knit shortcut.
- **Stand collar solved, not guessed.** The neck edge is bisection-solved to the
  half opening (collar-band method) rather than a rib rectangle × ratio (the
  bomber's approach); the collar↔neckline seam is declared and verified.
- **Cuff/hem band are rectangles** sized from the measured openings; their join
  allowance and rib recovery are carried as an exact `ease` on the declared
  seam so lengths still balance to delta ≈ 0 (the band is deliberately smaller
  than its opening — the rib/elastic recovers).
- **Front pockets are placement markings** (opening trace + surround box), not
  cut-in bag pieces; the common ready-to-wear construction.
- **Zippers are hardware**: the separating body zipper and the pocket zips are
  referenced as Yantra4D cartridges (zipper-notion) in the BOM notes, never
  re-drafted here (per the federation contract).

```bash
python apps/api/services/engine/fc_runner.py projects/track-jacket/main.py track-jacket.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/track-jacket/main.py big.svg '{"chest_girth": 1400, "neck_girth": 480}' svg
```

Official visualizer and configurator: Fashion Cabinet.

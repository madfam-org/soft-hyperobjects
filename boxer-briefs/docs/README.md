# Boxer Briefs — FC-100 #10 / Bóxer ajustado — FC-100 #10

A fitted mid-thigh men's/unisex boxer brief: essentially **leggings cut very
short**, drafted with the intimates cluster's **exact elastic accounting**. Knit,
pull-on, negative ease — no hardware.

Un bóxer ajustado a media pierna para hombre/unisex: en esencia **mallas
cortadas muy cortas**, trazado con la **matemática exacta de elástico** del grupo
de ropa interior. De punto, sin cierre, con holgura negativa — sin herrajes.

## Pieces / Piezas

- **front** — Front (pouch). Fold-cut on the centre-front line, cut 1 on fold →
  full front. Carries the narrower pouch fork and a short leg.
- **back** — Back (full seat). Fold-cut on the centre-back line, cut 1 on fold →
  full back. Wider fork, raised seat (back rise extra), short leg.
- **gusset** — Pouch gusset, cut 2 on fold (self + liner). A half-trapezoid whose
  **front edge = the front fork half-width** and **back edge = the back fork
  half-width**, so the crotch seams close by construction.
- **waistband** — The signature wide **fold-over casing**. Its attach (bottom)
  edge equals the **full measured waist opening**; the branded gripper elastic
  rides inside the fold, cut to `waist × ratio`.

## Construction order / Orden de construcción

1. Close the crotch: sew **gusset.front_edge → front.gusset_edge** and
   **gusset.back_edge → back.gusset_edge** (self and liner treated as one).
2. Sew the **inner-leg seam**: front.inseam → back.inseam (the shorter inseam was
   bowed to the longer, so they match exactly).
3. Sew the **side seam**: front.outseam → back.outseam.
4. Finish the **leg openings**: elastic-finished (soft elastic zig-zagged into the
   marked zone) or a turned-and-coverstitched hem — set by the `leg_hem_elastic`
   checkbox.
5. Apply the **waistband casing** around the full waist opening; join the gripper
   elastic in a ring, quarter-mark, and enclose it in the fold.
6. Coverstitch / overlock. Ballpoint needle, stretch thread on every seam.

## Honest simplifications (teaching-grade)

- **Flat front, no functional fly.** The pouch is shaped by the front fork and the
  gusset only; a real fly opening is a later refinement. / **Frente plano, sin
  bragueta funcional.**
- **Symmetric leg tube.** Front and back share one snug thigh half-width, so the
  side seam (outseam) balances without a separate side-shaping solve. Real boxer
  briefs shape the outer thigh slightly. / **Tubo de pierna simétrico.**
- **Solved inseam.** Front and back forks differ, so the two straight inseams
  differ; the shorter one is bowed outward by a bisection-solved amount until the
  inner-leg seam closes (delta ≈ 0) — the same technique the leggings cartridge
  uses. / **Entrepierna resuelta.**
- **Waistband as a fold-over casing.** The attach edge is sewn 1:1 to the waist
  opening (so the declared seam balances); the negative pull lives in the gripper
  **elastic cut length** (`waist × ratio`), not in the seam. You may instead expose
  a branded jacquard elastic band — same cut length. / **Pretina como funda
  doblada.**
- **Negative ease** is applied in the draft (girth × `1 − ease%`), never by asking
  for a smaller measurement. Cut with the greatest stretch (weft) running around
  the body. / **La holgura negativa** se aplica en el trazo.

## Notions / Insumos

No hardware. Elastics and thread only; every elastic **cut length is emitted in
the BOM in exact mm**, derived from the measured pattern openings (waist opening ×
waistband ratio; leg opening × leg-elastic ratio, per leg). Hard goods, if ever
added (e.g. a branded metal tag), would be a **Yantra4D** cartridge referenced via
the manifest, never re-implemented here.

Sin herrajes. Solo elásticos e hilo; cada **largo de corte de elástico se emite en
la lista de materiales en mm exactos**, derivado de las aberturas medidas del
patrón.

## Fabric / Tela

`jersey-algodon` (cotton/elastane single jersey, ~10% comfortable negative ease,
stretch in the weft). See `materials/jersey-algodon`.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

# Parka — FC-100 rank #59

A long, roomy, insulated hooded technical coat (thigh/knee length). Built on
the **zip-hoodie block** (rank #14) grown into a coat, then dressed with the
parka signatures as verified, regenerating pieces.

*Un abrigo técnico largo, holgado y aislado con capucha (a la altura de
muslo/rodilla), sobre el bloque de la sudadera con cierre crecido a abrigo.*

## Pieces / Piezas

| Piece | Cut | What it is |
|-------|-----|-----------|
| `front` | cut 2 mirror | Half front; the **center edge is the separating-zipper seam** (15 mm tape allowance, top/bottom stop notches, 7 mm stitch line). Carries the drawcord waist + hem channels and the pocket placement. |
| `back` | cut 1 on fold | One-piece back with the same drawcord channels. |
| `sleeve` | cut 2 mirror | Long set-in coat sleeve; the **cap is solved by bisection** to the measured armholes + a small declared ease. |
| `hood` | cut 2 mirror | Two-panel hood; the **neck edge is solved by bisection** to the measured half neck opening (the hoodie method). Face edge carries a drawcord channel + fur-trim line. |
| `storm_flap` | cut 1 | A placket strip that snaps over the zipper; its **`attach` edge is solved to the front center length** and caught in the CF seam (the trench gun-flap method at center front). |
| `pocket` | cut 2 mirror | Big **bellows cargo pocket** — a chamfered patch pocket with a 3D bellows-gusset fold trace and a cut-and-fold flap. Topstitched appliqué. |
| `cuff` | cut 2 | Rib **storm cuff** inside the shell sleeve (sleeve opening × `cuff_ratio`, folded). |

## Construction order / Orden de construcción

1. Topstitch the **bellows pockets** to the fronts (fold the gusset, set the flap).
2. Sew the **storm flap** into the left **center-front** seam; install the **separating zipper** into both center-front edges (tape allowance = 15 mm; stops at the notches). Snap the storm flap over the closed zipper.
3. Join **shoulders** and **side seams** (front ↔ back).
4. **Set the sleeves** into the armholes (cap eased in), then close the **underarm** seams; ring the **rib storm cuffs** to the sleeve hems.
5. Sew the two **hood panels** at the crown, then the **hood neck** to the body neckline (front + back). Thread the **hood face drawcord**; snap on the fur ruff.
6. Form the **waist** and **hem drawcord channels**; thread the cords out through the front eyelets and cap them with cord stops.
7. **Bag the shell to the insulated lining** over the fill; finish the hem.

## Honest simplifications (teaching-grade)

- The geometry is a **normal long jacket**; the parka-ness lives in the storm
  flap, the hood, the bellows pockets, the drawcord channels, the rib cuffs and
  the **BOM** — the same rule as the blazer's pockets. No 3D loft is modeled.
- **Lining and insulation are noted-not-drafted** in v0: BOM lines for a full
  insulated lining and synthetic fill (by garment area). A real down parka uses
  **baffled down** instead — synthetic keeps loft when wet, which suits the
  ripstop shell. Lining pieces cut from the shell fronts/back/sleeves/hood.
- **Bellows depth** is drawn as a fold trace, not a separate gusset strip; the
  pocket is an appliqué, so it is **not** a length-balanced seam (no declare).
- **Waterproofing:** the ripstop shell is wind/water-resistant; seam-sealing
  tape over the needle holes is what makes it waterproof — add it (and taped
  seams) if a hardshell build is wanted (see the BOM thread note).
- **Hardware is federated to Yantra4D**, never re-implemented here: the zipper
  slider/pull (`projects/zipper-notion`), the storm-flap **snaps**, and the
  waist/hem/hood **cord stops** are all Yantra4D notion references. Fill, cord,
  elastic, lining and the fur ruff are purchased components noted in the BOM.

## Verified seams / Costuras verificadas (delta ≈ 0)

- `front.side` ↔ `back.side`, `front.shoulder` ↔ `back.shoulder`
- `sleeve.cap` ↔ `front.armhole + back.armhole` (with the declared cap ease)
- `sleeve.underarm_front` ↔ `sleeve.underarm_back`
- `hood.neck` ↔ `front.neck + back.neck` (solved)
- `storm_flap.attach` ↔ `front.center` (solved)

Fabric: `materials/nylon-ripstop-shell` (lightweight ripstop nylon shell, 95 gsm).

Official visualizer and configurator: **Fashion Cabinet**.
*Visualizador y configurador oficial: **Fashion Cabinet**.*

```bash
python apps/api/services/engine/fc_runner.py projects/parka/main.py parka.svg '{}' svg
```

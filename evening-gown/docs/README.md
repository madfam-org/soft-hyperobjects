# Evening Gown · Vestido de Noche

**FC-100 rank #72.** A woven, floor-length formal gown cut on the **true bias**,
with a fitted torso, a low back, an invisible zipper, a full lining, and an
optional **train**. The formal-wear peak of the FC-100.

Un vestido de noche largo en tela plana cortado al **bies verdadero**, con torso
entallado, espalda baja, cierre invisible, forro completo y **cola** opcional.

---

## What it is · Qué es

The gown extends the **a-line-dress** lineage to the floor and cuts it on the
bias. The front is cut on the fold; the back is cut 2 with a center-back seam
that carries the closure. Two things turn a long shift into a gown:

1. **True bias.** The grainline is drawn at an exact **45°** on both body
   panels (the **slip-dress** trick). Cutting on the bias is what lets a gown
   hang liquid and skim the body — the reason real evening gowns are bias-cut in
   silk crepe or satin. Here the poplin stand-in shows the geometry; swap in a
   drapey silk for the real hand.
2. **A train.** `train_length` extends the **CB back hem below the floor line**
   into a sweep, while the front hem stays level at the floor. Because hems are
   faced/finished (never sewn to each other), the train changes only the back
   hem and the CB seam's start point — the side seam is untouched, so the front
   and back side seams still match exactly.

A **silhouette** select swaps the sweep: `bias_column` skims the hip with a
light flare (the classic bias column); `a_line_train` opens the hem well past
the hip for a dramatic A-line. A **zip_placement** select puts the invisible
zipper at center back (default) or at the side seam — a bias gown often prefers
a side zip so the CB drape is unbroken.

## Honest simplifications (teaching-grade) · Simplificaciones honestas

- **Darts stay internal.** The side-bust dart and back fisheye waist darts are
  drawn as internal markings, not rotated/slashed into the outline. Real bias
  gowns often mould with the bias itself and minimal darting; the darts here are
  a legible shaping guide.
- **Bias behaviour is drawn, not draped.** The 45° grainline is placed
  correctly, but the kernel does not simulate bias stretch or drape. The
  fabric-hang settling is a construction note (**hang 24 h before hemming**),
  not a solved deformation.
- **The lining reuses the body pieces.** The gown is fully lined; the lining is
  cut from the same front + back pieces (noted in the BOM), not re-drafted with
  its own ease. An underlining vs. free-hanging lining choice is left to the
  maker.
- **The train is a hem sweep, not a separate panel.** It drops the back hem in
  one continuous curve rather than adding a seamed train section.
- **One woven ease** (70 mm) is folded into every width; grading rules and
  dart rotation are future kernel work.

## Pieces · Piezas

| id | piece | cut |
|----|-------|-----|
| `front` | Gown Front (bias, on fold) | 1 on fold, mirrored |
| `back` | Gown Back (bias, CB seam + zip) | 2, mirrored |
| `neck_facing` | Neck Facing | 1 (derived from measured neck opening) |
| `armhole_facing` | Armhole Facing | 2 (derived from measured armhole) |

Plus a full **lining** cut from `front` + `back` (see BOM).

## Construction order · Orden de confección

1. Cut every body panel **single layer on the true bias** (45° grainline). Cut
   the lining the same way. Let the bias panels **hang 24 h** before truing the
   hem.
2. Staystitch the neck and armhole curves; mark and sew the internal darts
   (side-bust on the front, fisheye on each back panel).
3. Join front to back at the **shoulder** seams, then the **side** seams
   (`front.side` = `back.side` by construction).
4. Install the **invisible zipper** in the marked seam — center-back by default,
   or the left side seam when `zip_placement = side`. Close the seam above the
   top stop with a **hook & eye**. (Zipper hardware is a Yantra4D cartridge
   reference — see BOM.)
5. Face the neck and armholes with the derived facing strips; understitch.
6. Assemble the lining the same way, bag or hand-finish it to the facings.
7. **Hem** the shell and lining level at the floor; carry the **train** sweep at
   CB. A narrow bias hem (the default 20 mm allowance) hangs best.

## Declared seams · Costuras declaradas

- `front.shoulder` ↔ `back.shoulder` — shared geometry, delta ≈ 0.
- `front.side` ↔ `back.side` — one shaped run used on both panels, delta ≈ 0.

(The hems are finished/faced, not sewn to each other, so the train may lengthen
the back hem without any seam mismatch. The CB seam is a single-piece self-seam
carrying the zipper.)

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

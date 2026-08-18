# Kaftan / Caftán — FC-100 #99

**EN** — The kaftan is a loose, wide, T-shaped tunic-robe worn across North
Africa, West Africa, the Middle East, and South Asia. It is pulled on over the
head (no buttons or zips) through a narrow, deep **keyhole** neckline finished
with a **neck facing**. Length runs from below-knee to ankle. Historically it is
cut with great economy from rectangular panels, and its fabric spans humble
cotton to fine silk. This cartridge drafts it respectfully as a teaching-grade
parametric block.

**ES** — El caftán es una túnica-bata amplia y holgada en forma de T, usada en
el norte de África, África occidental, Medio Oriente y el sur de Asia. Se viste
por la cabeza (sin botones ni cierres) a través de un escote estrecho y profundo
de **ojo de cerradura**, rematado con una **vista de escote**. El largo va de
bajo la rodilla al tobillo. Tradicionalmente se corta con gran economía a partir
de paneles rectangulares, y su tela abarca del algodón sencillo a la seda fina.
Este cartucho lo traza con respeto como bloque didáctico paramétrico.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front (keyhole) | Delantero (ojo de cerradura) | 1 on fold at CF |
| `back` | Back | Trasero | 1 on fold at CB |
| `sleeve` | Sleeve | Manga | 2 (mirrored) |
| `facing` | Neck facing | Vista de escote | 1 |
| `belt` | Tie belt (sash) | Faja | 1 |

## Construction order / Orden de confección

1. Stay-stitch and finish the **keyhole neckline** with the **neck facing**:
   the facing `inner` edge sews to the full neck opening (front neck ×2 + back
   neck ×2), then it is turned and understitched. Interface the facing to keep
   the keyhole crisp.
2. Sew **shoulder** seams (front ↔ back).
3. Set the **sleeves**: the sleeve `cap` eases into the front + back armholes
   (zero ease — a dropped, near-horizontal shoulder sews flat), then close each
   sleeve underarm seam (`underarm_front` ↔ `underarm_back`).
4. Sew the **side** seams from the underarm down to the notched **slit top**;
   below the notch the seam stays open as a side slit. Hem the slit edges.
5. Hem the **sleeve openings** and the **bottom hem**.
6. Optional: roll-hem the **tie sash** and add belt carriers if wanted.

## Declared seams (all verified, delta ≈ 0)

- `front.shoulder` ↔ `back.shoulder`
- `front.side` ↔ `back.side` (sewn to the slit top only)
- `sleeve.cap` ↔ `front.armhole` + `back.armhole` (ease 0)
- `sleeve.underarm_front` ↔ `sleeve.underarm_back`
- `facing.inner` ↔ `front.neck` ×2 + `back.neck` ×2 (ease = 2 × seam allowance,
  the facing's two centre-back-break ends)

## Honest simplifications (teaching-grade)

- **The keyhole** is drafted as a narrow, deep centre-front neck opening: the
  front neck curve hugs the fold near its base (the throat) and flares out to
  the high point of shoulder. The rounded throat and any hand-worked slit
  finish are a machine detail, not separate pattern geometry.
- **The sleeve** is a simple wide **dropped set-in** sleeve, with its cap length
  solved numerically to the measured armhole. The classic kaftan is often cut
  with a **grown-on / T-cut** sleeve (a nearly straight shoulder line and no
  armhole seam); that is the traditional alternative, chosen here as a set-in
  for a clearer, verifiable draft.
- **The neck facing** is topologically a ring. A single pattern piece cannot
  carry a hole, so — following the commons convention — the facing is cut open
  (broken at centre back) and laid flat as a shaped band. Its `inner` edge is
  the edge that sews to the neckline; it is exactly the opening length plus one
  seam allowance at each centre-back end.
- **Hardware** (a decorative tassel or tie at the keyhole throat) is a Yantra4D
  cartridge reference in the BOM (`notion.hardware_ref`), never re-implemented
  in the fashion kernel.

Units are millimetres; girths are full-body measurements.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

# Swim Trunks — FC-100 #53

**EN** — Board-short-style men's swim trunks: a relaxed **outer trunk**
(mid-thigh, woven-like fit even in 4-way-stretch swim tricot, so **no negative
ease** on the outer) with an elastic **waistband casing** and an internal
**drawcord**, worn over a fitted **mesh brief liner**. One waistband casing
catches both layers; the mesh liner attaches only at the waist and hangs free at
the leg. The outer carries a **curved, split side hem** (the board-short side
vent) and a patch **back pocket** with a **drain eyelet**.

**ES** — Traje de baño (short) estilo board-short para hombre: un **short
exterior holgado** (a media pierna, con caída plana aun en tricot de baño de
estiramiento en cuatro direcciones, por lo que el exterior **no lleva holgura
negativa**) con **pretina elástica** y **cordón** interno, sobre un **forro
interior de malla tipo brief** ajustado. Una sola pretina atrapa ambas capas; el
forro de malla se une solo en la cintura y cuelga libre en la pierna. El exterior
lleva un **bajo lateral curvo y abierto** (la abertura lateral del board-short) y
un **bolsillo trasero** de parche con **ojal de drenaje**.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `outer_front` | Outer Front | Delantero exterior | cut 2, mirror |
| `outer_back` | Outer Back | Trasero exterior | cut 2, mirror |
| `liner_front` | Mesh Liner Front (brief) | Forro de malla delantero (brief) | cut 2, mirror |
| `liner_back` | Mesh Liner Back (brief) | Forro de malla trasero (brief) | cut 2, mirror |
| `waistband` | Waistband Casing | Pretina (casing) | cut 1 |
| `back_pocket` | Back Patch Pocket | Bolsillo trasero de parche | cut 1 |

## Construction order / Orden de construcción

1. **Topstitch the back pocket** onto the outer back at the marked placement:
   hem the pocket top, turn the three sides, set the **drain eyelet** at the base
   centre, and edgestitch + bar-tack the corners.
2. Sew each layer's **inseams** (outer front↔back, liner front↔back) and **side
   seams** (outer front↔back, liner front↔back). Flatlock or overlock.
3. **Elastic-finish the mesh liner leg openings** — coverstitch clear/knit leg
   elastic into the marked leg zone (exact cut length in the BOM, per leg).
4. **Stack the mesh liner inside the outer at the waist** (wrong sides together);
   the two waist edges match by construction.
5. Enclose the joined waist stack in the **waistband casing**, leaving a small
   opening; insert the joined waist **elastic**, thread the **drawcord** through
   the channel and out the two **center-front eyelets**; close the opening.
6. **Hem the outer split side hem** (turn the curved hem allowance and
   topstitch).

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **Relaxed outer, no negative ease** — a swim trunk hangs like a woven short,
  so the **outer trunk is drafted at hip girth + ease** (not reduced), even
  though the swim tricot stretches. The stretch here is comfort, not fit. Only
  the **mesh liner** carries negative ease (`liner_neg_ease`), applied in the
  draft, not by asking for a smaller measurement.
- **Curved / split side hem** — the outer hem is modelled as a single cubic
  bezier that sweeps up `side_scoop` mm at the side seam. A production board
  short often has a separate bound or faced split; here the scoop is drawn into
  the one hem edge. The outer hem is a **finished** edge, not a seam, so front
  and back hems differ in length by design and are not length-matched.
- **Both back hems solved analytically** — the outer back hem width and the mesh
  liner back hem width are each solved so the straight back inseam equals the
  straight front inseam exactly (the athletic-shorts idiom, applied twice). The
  inseam seams verify at delta ≈ 0.
- **Liner waist pinned to the outer waist** — the mesh liner is a **brief**
  drafted with mild negative ease at the hip and leg, but its **waist width is
  pinned to the outer waist width** so both layers meet the one waistband at the
  same length. The waist-stack seams (liner↔outer, band↔outer) verify at
  delta ≈ 0. In wear the mesh brief tensions to the body below the waist.
- **Elastic and drawcord under tension are not length-matched** — the waistband
  fabric length equals the waist opening; the shorter **elastic** and the longer
  **drawcord** live in the BOM as exact-mm cut lengths (opening × ratio), the
  numbers factories keep on private spec sheets. They are applied under tension,
  not sewn edge-to-edge, so they are not declared as length-matched seams.
- **Back pocket is a topstitched patch, not a seam** — the pocket attaches by
  topstitching onto the outer back at the marked placement rectangle, so its
  attach is a placement guide (like the bermuda/jeans back pockets), not a
  length-balanced declared seam.
- **No hardware modelled** — the drawcord cord-stops/tips and the **eyelets**
  (2 center-front drawcord eyelets + 1 pocket drain eyelet) are **Yantra4D**
  notion references (`notion.kind = eyelet`, `hardware_ref → yantra4d`, noted in
  the BOM), never re-implemented in this cartridge.

## Fabrics / Telas

- Outer shell: **tricot-nylon-elastano** (swim tricot, chlorine-resistant grade;
  greatest stretch runs weft, around the body).
- Mesh liner: the **lighter open-mesh grade of the same swim tricot** — a
  quick-drain inner brief. The commons carries one swim card; the liner is that
  card's lighter mesh variant (noted in the BOM).

The `tricot-nylon-elastano` card carries `cut_scale < 1.0` (it encodes the
swimwear negative-ease reduction). Here that reduction is applied to the **mesh
liner only** via `liner_neg_ease`; the **relaxed outer takes none**.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

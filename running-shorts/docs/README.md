# Running Shorts — FC-100 #52

**EN** — A runner's short: a relaxed **outer short** with a scooped, split
**curved side hem** worn over a fitted **compression liner** brief. One elastic
**waistband casing** catches both layers; the liner attaches only at the waist
and hangs free at the leg.

**ES** — Un short para correr: un short exterior holgado con **bajo lateral
curvo y abierto** sobre un **forro de compresión** ajustado. Una sola **pretina
elástica** atrapa ambas capas; el forro se une solo en la cintura y cuelga libre
en la pierna.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `outer_front` | Outer Front | Delantero exterior | cut 2, mirror |
| `outer_back` | Outer Back | Trasero exterior | cut 2, mirror |
| `liner_front` | Liner Front (compression) | Forro delantero (compresión) | cut 2, mirror |
| `liner_back` | Liner Back (compression) | Forro trasero (compresión) | cut 2, mirror |
| `waistband` | Waistband Casing | Pretina (casing) | cut 1 |

## Construction order / Orden de construcción

1. Sew each layer's **inseams** (outer front↔back, liner front↔back) and
   **side seams** (outer front↔back, liner front↔back). Flatlock or overlock.
2. **Elastic-finish the liner leg openings** — coverstitch clear/knit leg
   elastic into the marked leg zone (exact cut length in the BOM, per leg).
3. **Stack the liner inside the outer at the waist** (wrong sides together);
   the two waist edges match by construction.
4. Enclose the joined waist stack in the **waistband casing**, leaving a small
   opening; insert the joined waist **elastic** and, if wanted, the **drawcord**
   through the casing's drawcord channel; close the opening.
5. **Hem the outer split hem** (turn the curved hem allowance and topstitch).

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **Curved hem** — the outer hem is modelled as a single cubic bezier that
  sweeps up `side_scoop` mm at the side seam. A production split short often has
  a separate bound or faced split; here the scoop is drawn into the one hem
  edge. The outer hem is a **finished** edge, not a seam, so front and back hems
  differ in length by design and are not length-matched.
- **Both back hems solved analytically** — the outer back hem width and the
  liner back hem width are each solved so the straight back inseam equals the
  straight front inseam exactly (the athletic-shorts idiom, applied twice). The
  inseam seams verify at delta ≈ 0.
- **Liner waist pinned to the outer waist** — the liner is drafted with negative
  ease at the hip and leg (compression), but its **waist width is pinned to the
  outer waist width** so both layers meet the one waistband at the same length.
  The waist-stack seams (liner↔outer, band↔outer) verify at delta ≈ 0. In wear
  the compression liner tensions to the body below the waist.
- **Elastic under tension is not length-matched** — the waistband fabric length
  equals the waist opening; the shorter **elastic** and the longer **drawcord**
  live in the BOM as exact-mm cut lengths (opening × ratio), the numbers
  factories keep on private spec sheets. They are applied under tension, not
  sewn edge-to-edge, so they are not declared as length-matched seams.
- **No hardware** — cord stops/tips for the drawcord are a **Yantra4D** notion
  reference (noted in the BOM), never re-implemented in this cartridge.

## Fabrics / Telas

- Outer shell: **poliester-elastano-compresion** (athletic power-stretch).
- Liner: **tricot-nylon-elastano** (lighter compression tricot).

Both cards carry `cut_scale < 1.0`; the negative ease for the liner is applied
in the draft (`liner_neg_ease`), not by asking for a smaller measurement.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

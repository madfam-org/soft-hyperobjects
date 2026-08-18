# Kurta — FC-100 #97

**EN** — The kurta is a long, straight, loose tunic of South Asia, worn by men
and women across India, Pakistan, Bangladesh, Nepal, Sri Lanka and the wider
diaspora. It reaches from mid-thigh to knee, closes with a short **centre-front
placket** (small buttons or a neck tie), and finishes at the neck with a
standing **mandarin band collar**. Its lower side seams open into **side slits
(chaak)** for movement. Its cloth spans humble cotton and khadi to fine silk.
This cartridge drafts it respectfully as a teaching-grade parametric block; it
is a garment of real cultural significance and is offered here with care.

**ES** — El kurta es una túnica larga, recta y holgada del sur de Asia, usada
por hombres y mujeres en India, Pakistán, Bangladés, Nepal, Sri Lanka y la
diáspora. Llega de medio muslo a la rodilla, cierra con una **tapeta central
delantera** corta (botones pequeños o un lazo al cuello) y remata en el cuello
con un **cuello banda mandarín** de tira alta. Sus costuras laterales inferiores
se abren en **aberturas laterales (chaak)** para dar movimiento. Su tela abarca
del algodón y el khadi humildes a la seda fina. Este cartucho lo traza con
respeto como bloque didáctico paramétrico; es una prenda de verdadera
significación cultural y se ofrece aquí con cuidado.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front (placket) | Delantero (tapeta) | 1 on fold at CF |
| `back` | Back | Trasero | 1 on fold at CB |
| `sleeve` | Sleeve (long or short) | Manga (larga o corta) | 2 (mirrored) |
| `collar` | Band collar (mandarin) | Cuello banda (mandarín) | 2 on fold at CB |
| `placket` | Placket facing | Vista de tapeta | 2 |
| `pocket` | Chest pocket | Bolsillo de pecho | 1 |

## Construction order / Orden de confección

1. Mark the **CF placket slash** on the front (it opens on the fold at centre)
   and finish it with the **placket facing** strip (interfaced): slash, turn the
   two placket edges, topstitch, and bar-tack the bottom. Add the placket
   buttons or a neck tie (hardware federates to Yantra4D).
2. Optional: hem the top edge of the **chest pocket** and topstitch it to the
   traced placement on the front.
3. Sew the **shoulder** seams (front ↔ back).
4. Build and attach the **band collar**: the collar `neck` edge sews to the full
   neckline (front `neck` + back `neck`, each side of the fold), meeting at the
   CF closure line; understitch and edgestitch the mandarin band.
5. Set the **sleeves**: the sleeve `cap` eases into the front + back armholes
   (zero ease), then close each sleeve underarm seam (`underarm_front` ↔
   `underarm_back`).
6. Sew the **side** seams from the underarm down to the notched **chaak slit
   top**; below the notch the seam stays open as the side slit. Finish the slit
   edges.
7. Hem the **sleeve openings** and the straight **bottom hem**.

## Declared seams (all verified, delta ≈ 0)

- `front.shoulder` ↔ `back.shoulder`
- `front.side` ↔ `back.side` (sewn to the chaak slit top only; open below)
- `sleeve.cap` ↔ `front.armhole` + `back.armhole` (ease 0, solved by bisection)
- `sleeve.underarm_front` ↔ `sleeve.underarm_back`
- `collar.neck` ↔ `front.neck` + `back.neck` (ease = collar closure overlap;
  the mandarin band solved to the measured neckline by bisection)

## Honest simplifications (teaching-grade)

- **The neckline** where the band attaches is a plain round neckline. The
  **placket** is a partial centre-front slash, opened on the fold and finished
  by the facing strip. The slash's two cut edges are a construction detail
  marked as internals on the fold-cut front (like the henley / polo placket),
  not separate outline geometry; the facing strip's size is derived from the
  placket length and width.
- **The band collar** is a single standing mandarin band (no fall). Its neck
  edge length is solved numerically to half the measured neckline plus the
  centre-front closure overlap, so the neck seam matches to floating-point
  precision — the collar-band method, shared with the dress shirt and the
  collar-band enabler.
- **The sleeve** is a simple **set-in** sleeve, with its cap length solved to
  the measured armhole. The traditional kurta is often cut with a **grown-on or
  gusseted** sleeve (a nearly straight shoulder line with an underarm gusset);
  that is the authentic alternative, chosen here as a set-in for a clearer,
  verifiable draft. A `sleeve_style` select offers long or short.
- **The side slit (chaak)** is placed by a notch at the slit top on each side
  seam; below it the seam is left open. A straight hem is drafted, with an
  optional gentle A-line **side flare**.
- **Hardware** (placket buttons or a neck tie) is a Yantra4D cartridge reference
  in the BOM (`notion.hardware_ref`), never re-implemented in the fashion
  kernel. Real kurtas span cotton poplin and khadi to fine silk; the draft uses
  a light cotton (`popelina-algodon`, with `manta-cruda` as the muslin-look
  alternative).

Units are millimetres; girths are full-body measurements.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

# Chef Coat · Filipina de chef — FC-100 #87

**EN.** The classic **double-breasted chef's jacket**. Its signature is the
**wide crossover front**: each front is cut twice and its center edge runs a
generous *crossover* (default 110 mm) past the center-front line, so the right
front wraps well over the left. Two columns of **knotted cloth (china) buttons**
are marked on the front — an outer column near the wrap edge (the functional
closure) and an inner column near CF (the reversible / under-wrap side),
about two columns × five. A **stand / mandarin band collar**, long roomy
sleeves with a **turn-back cuff**, **side vents**, a **chest thermometer
pocket**, a **sleeve pocket**, and a straight hem complete the coat. The whole
draft regenerates parametrically and every seam is length-checked.

**ES.** La clásica **filipina de chef cruzada** (doble botonadura). Su firma es
el **cruce ancho del delantero**: cada delantero se corta dos veces y su canto
central corre un *cruce* generoso (110 mm por defecto) más allá del centro
frente, de modo que el delantero derecho envuelve sobre el izquierdo. Se marcan
dos columnas de **botones de nudo de tela (china)** — una exterior junto al
borde del cruce (el cierre funcional) y una interior junto al centro frente (el
lado reversible), unas dos columnas × cinco. Un **cuello mao (banda de pie)**,
mangas holgadas con **puño vuelto**, **aberturas laterales**, una **bolsa de
termómetro** al pecho, una **bolsa de manga** y bajo recto completan la prenda.
Todo el trazo se regenera de forma paramétrica y cada costura se verifica en
longitud.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front (double-breasted) | Delantero (cruzado) | cut 2, mirror |
| `back` | Back | Espalda | cut 1 on fold |
| `sleeve` | Sleeve | Manga | cut 2, mirror |
| `collar` | Band collar | Cuello mao | cut 2 on fold (CB) |
| `facing` | Crossover front facing | Vista delantera del cruce | cut 2, mirror |

## Construction order / Orden de construcción

1. Mark both fronts (they are identical — reversible). Trace the CF line, the
   crossover edge, both **cloth-button columns**, the thermometer pocket, and
   the side-vent stop. Fuse the front stands / facings.
2. Attach the **crossover front facings** to the center + neck edge of each
   front (the facing length is verified against `front.center + front.neck`).
3. Sew **shoulder** seams (front ↔ back) and **side** seams (front ↔ back),
   stopping the side seam at the marked **vent** height.
4. Solve and set the **one-piece sleeves**: the cap is bisected to the
   front + back armholes plus the small declared **cap ease**; sew the
   **underarm** seam; press up the **turn-back cuff** at its fold line.
5. Build the **band collar** on the fold at CB and sew it to the neckline
   (`collar.neck == front.neck + back.neck`, per half).
6. Hem straight. Hand-knot or set the **cloth knot buttons** in two columns on
   each front; work buttonholes / loops on the wrap.

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **Reversible note.** Both fronts are cut identical so the coat can be built
  reversible (either front can wrap on top). The two button columns support
  that; a fully finished reversible build (double buttonholes / removable
  studs) is a construction detail, not separate geometry.
- **Collar.** A single-piece **stand / mandarin** band, solved to the neckline
  at zero ease. A small **turndown** variant is a construction note, not a
  separate piece in v0.
- **Facing** is a straight strip verified against the measured front run; a
  shaped facing that mirrors the crossover curve is future work.
- **Vents, cuff, and pockets** (side vents, turn-back cuff, thermometer pocket,
  sleeve pocket) are **markings/traces** in v0 — placement is drafted and
  checked, the finished welts/facings are construction steps.
- **Sleeve** is one-piece and comfort-first (a small eased cap, not a shaped
  tailored two-piece cap).
- **Hardware is federated.** The **cloth knot / china buttons** are a Yantra4D
  cartridge reference in the BOM (knotted-button family), traditionally
  hand-knotted from cloth cord or purchased — never re-implemented here.

Units are millimetres; girths are full-body measurements.

---

Official visualizer and configurator: **Fashion Cabinet**
Visualizador y configurador oficial: **Fashion Cabinet**

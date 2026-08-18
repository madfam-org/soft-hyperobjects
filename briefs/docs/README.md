# Briefs — FC-100 #9 · Trusa

Full-coverage classic briefs (men's / unisex) — the higher-coverage sibling of
the bikini panty (#45). Same intimates architecture, drafted for real coverage.

*Trusa clásica de cobertura completa (hombre / unisex) — la hermana de mayor
cobertura de la pantaleta bikini (#45). Misma arquitectura de ropa interior,
trazada para cobertura real.*

## What it is / Qué es

A close-fitting knit brief cut with **negative ease** so the elastane jersey
tensions to the body. Three pieces: a fold-cut **flat front**, a fold-cut
**full-seat back**, and a **trapezoid gusset** cut twice (self + liner). Front
and back are sewn up a real **side seam**; the gusset closes the crotch. Waist
and both leg openings are **elastic-finished**.

## Pieces / Piezas

| id       | piece                         | cut                         |
|----------|-------------------------------|-----------------------------|
| `front`  | Flat front, full coverage     | 1× on fold (mirror) → whole |
| `back`   | Full seat                     | 1× on fold (mirror) → whole |
| `gusset` | Gusset (self + liner)         | 2× on fold (mirror)         |

## Construction order / Orden de construcción

1. Sandwich the crotch between gusset **self and liner**; sew the gusset
   `front_edge` to the front `gusset_edge` and the gusset `back_edge` to the
   back `gusset_edge` (burrito method encloses both raw edges).
2. Sew the **side seams**: front `side` to back `side` (4-thread overlock).
3. Apply **waist elastic** in a ring into the marked waist zone, then
   **leg elastic** to each leg opening; coverstitch or zigzag down.

*1. Encierra la entrepierna entre tela y forro del refuerzo; une los bordes
delantero/trasero del refuerzo a los cuerpos. 2. Cierra las costuras laterales.
3. Aplica elástico de cintura en anillo y elástico en cada pierna.*

## Honest simplifications / Simplificaciones honestas (teaching-grade)

- **One hip girth drives every width.** A single `hip_girth` sets the front/back
  half-widths; there are no separate seat/thigh measures yet. Real graded briefs
  shape the seat independently. *Una sola medida de cadera define los anchos.*
- **Flat front, no pouch.** Chosen for clarity; a shaped/pouch front is a future
  variant. *Delantero plano, sin bolsa anatómica.*
- **The gusset matches by construction, not by fudging.** Because the gusset
  drafts on the same fold as the bodies, its front/back edges equal the body
  gusset edges exactly — the declared seams prove `delta ≈ 0` at render.
- **Side seam is identical by construction.** Front and back leg curves both end
  at the same side point and height, so the two side seams are equal straight
  segments (`delta = 0`).
- **Elastic lengths are exact, not guessed.** Waist and leg elastic cut lengths
  are `measured opening × ratio`, rounded to the millimetre, and reported in the
  BOM and metadata. *Los largos de elástico son exactos: abertura medida ×
  proporción.*

## Fabric / Tela

`jersey-algodon` (cotton/elastane single jersey). Cut with the greatest stretch
(**weft**) running horizontally, around the body. No hardware.

## Parameters / Parámetros

`hip_girth`, `rise_height`, `side_seam_h`, `negative_ease_pct` (default 10),
plus advanced gusset dims and the two elastic ratios. Girths are full-body
measurements; the negative ease is applied in the draft, not by entering a
smaller number.

---

Official visualizer and configurator: **Fashion Cabinet**.
*Visualizador y configurador oficial: **Fashion Cabinet**.*

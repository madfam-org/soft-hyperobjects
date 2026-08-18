# Raincoat — Impermeable

**FC-100 rank #61 · family: outerwear · tier T4 · fabric: technical shell**

A hooded, knee-length **waterproof shell coat**, cut roomy over layers. It takes
the zip-front architecture of the zip-hoodie / track-jacket and lengthens it into
a coat, then dresses it with the details that make a coat shed rain — a storm flap
over the zip, a solved rain hood, and, above all, **heat-taped seams**.

*Un impermeable con capucha, largo a la rodilla, holgado para usarse sobre capas.
Toma la arquitectura de frente con cierre de la sudadera con cierre / chamarra
deportiva y la alarga a abrigo, con los detalles que hacen que un abrigo escurra
la lluvia — una tapeta sobre el cierre, una capucha resuelta, y sobre todo
**costuras termoselladas**.*

## The waterproofing is construction, not a special shape

The one honest idea a raincoat teaches: **the fabric is only half the story.** A
laminated or DWR-finished shell resists water on its face, but every seam is a
line of needle holes, and water walks straight through them. What makes a
raincoat actually waterproof is **seam-sealing tape** — a heat-activated film
pressed over every seam on the inside.

So this cartridge models the waterproofing exactly the way the blazer models its
pockets — as **BOM + a note**, not a new outline:

- the BOM line **`seam-sealing tape`** is quantified at **~the total sewn seam
  length** (summed from the real seams: both side seams, both shoulders, both
  set-in armhole rings, both sleeve underarms, the hood-to-neck ring, the CF
  zipper tape seam, and the storm-flap attach);
- the metadata `waterproofing_note` names the taped-seam step as the thing that
  keeps the wearer dry;
- the thread/needle BOM line calls for a **fine microtex needle** so the holes
  stay small enough for the tape to bridge.

*La impermeabilidad es construcción, no una forma especial: el shell resiste el
agua, pero cada costura es una línea de orificios de aguja. La cinta selladora
termoactivada sobre cada costura es lo que de verdad impermeabiliza. Se modela
como BOM + nota (cinta ≈ longitud total de costura), igual que las bolsas del
saco.*

## Pieces

| id | qty | what it is |
|----|-----|-----------|
| `front` | cut 2, mirror | half front; the center edge is the separating-zipper seam (15 mm tape allowance, 7 mm stitch line, top/bottom stop notches). Storm-flap placement + big flap hip pocket are marked. |
| `back` | cut 1 on fold | knee-length back; a back storm-cape / vent-yoke line is a ventilation marking. |
| `sleeve` | cut 2, mirror | set-in sleeve; the cap is **solved by bisection** to the measured armhole pair **plus the declared cap ease**. Two underarm ventilation eyelets are marked. |
| `hood` | cut 2, mirror | two-panel rain hood; the neck edge is **solved by bisection** to the half neck opening. A brim-wire channel + a face drawcord run the face edge. |
| `storm_flap` | cut 1 | placket over the CF zip; its `attach` edge is **solved to the front center edge** so it sews on with delta ≈ 0. Snap crosses mark the closure. |

## Construction order (teaching-grade)

1. Mark and set the **flap hip pockets** on each front (welt/jetting is future work).
2. Join **shoulder** seams (front ↔ back), then **side** seams. Tape both.
3. Sew the two **hood** panels together at the crown; solve/attach the hood to the
   neckline (`hood.neck ↔ front.neck + back.neck`). Thread the **brim wire** and
   **face drawcord**; fit **cord locks**. Tape the neck seam.
4. Set each **sleeve**: sew the underarm seam, ease the **cap** into the armhole
   pair, tape both. Punch the **underarm ventilation eyelets** (grommets).
5. Install the **separating zipper** on the two front center edges (Yantra4D
   hardware). Attach the **storm flap** over the right front so it laps the closed
   zip; add **snaps**. Tape the CF and flap seams.
6. Hem the coat with the generous coat hem allowance; optionally cord the hem.
7. **Heat-tape every seam on the inside** — this is the step that makes it
   waterproof — then re-proof the DWR as needed.

## Honest simplifications

- **Waterproofing is modeled, not simulated.** The geometry is a normal roomy
  coat; the "waterproof" property lives in the BOM (tape at ~total seam length)
  and the notes. No hydrostatic-head or breathability physics here.
- **Storm flap is a straight placket**, cut 1, solved in length to the front
  center. A shaped/curved flap and a separate under-flap are future work.
- **Ventilation is marked, not cut**: the back storm-cape / vent-yoke line and the
  underarm eyelets are traces/drill marks; a functional cape panel and pit-zips
  are future work (pit-zip hardware would be a Yantra4D reference).
- **Hood is two panels** solved to the neck; a three-panel hood with a center
  gusset, or a detachable snap-off hood, is future work.
- **Lining / mesh** is not drafted; a mesh-lined shell hangs the mesh off the same
  body pieces.
- **Hardware is federated, never drafted:** the separating zipper, the storm-flap
  snaps, the drawcord **cord stops**, and the ventilation **eyelets** are all
  Yantra4D cartridge references in the BOM, per the federation contract.

## Fabric

`nylon-ripstop-shell` — a lightweight (95 gsm) wind/water-resistant ripstop.
It cuts true (no stretch compensation); a DWR finish or a PU/PTFE laminate grade
takes it from water-resistant to waterproof. Slippery hand — pin inside the
allowance and sew with a fine microtex needle so the holes stay small for the
tape to seal.

## Verified seams (all delta ≈ 0 at the default size)

- `front.side ↔ back.side`
- `front.shoulder ↔ back.shoulder`
- `sleeve.cap ↔ front.armhole + back.armhole` (ease = `cap_ease`)
- `sleeve.underarm_front ↔ sleeve.underarm_back`
- `hood.neck ↔ front.neck + back.neck`
- `storm_flap.attach ↔ front.center`

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

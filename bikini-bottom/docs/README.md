# Bikini bottom — FC-100 rank #56

The swimwear sibling of the [panties-bikini](../../panties-bikini/) underwear
draft — the **same** fold-cut topology, rebuilt honestly for the pool. Three
fold-cut pieces: a front with an adjustable leg line, a fuller-seat back, and
a waisted trapezoid gusset cut twice (**self + mesh liner**). All three draft
as half-pieces on the fold, so the gusset's front and back edges equal the
bodies' gusset edges **by construction**, and — with `side_style: fixed` — the
front and back side seams are identical by construction too. Three declared
seam checks (tol 1.0 mm) prove all of it at render time.

Cortada en tricot de baño (nylon/elastano, grado resistente al cloro) con
holgura negativa de baño; los cantos se rematan con elástico de baño.

## What makes it swimwear (not a relabel)

- **Swim fabric**: `tricot-nylon-elastano` — a chlorine-grade nylon/elastane
  warp-knit, cut with the greatest stretch running weft (around the body).
- **Swim elastic**: leg and waist edges are finished with **clear/rubber swim
  elastic** (polyurethane or rubber), which survives chlorine and does not
  water-log — a different notion from the soft picot/plush *underwear* elastic
  the panties draft uses. The BOM says so explicitly.
- **Swim negative ease**: ~13% by default (swimwear runs 10–15% so the suit
  holds when wet); `NEG = 1 − negative_ease_pct/100` scales the girth-derived
  widths in the draft. Body girths stay full-body measurements.
- **Adjustable coverage**: one `leg_line` slider sweeps the leg from **high-cut**
  (short side seam, leg scooped near the waist) to **full/boyshort** (long side
  seam, leg dropped low). `back_coverage` fills or bares the seat.
- **Side-tie option**: `side_style: tie` separates the sides and joins them with
  two knotted self-fabric ties (the classic side-tie bikini), added to the BOM;
  in that mode no side seam is declared because there isn't one. Default is
  `fixed` (seamed) for teaching clarity.

## The elastic accounting (the point of the cartridge)

Waist and leg edges carry **zero seam allowance** (elastic finish, with marked
application zones as internal traces) and the BOM emits **exact-mm swim-elastic
cut lengths**, recomputed from the measured pattern for any body size:

- waist swim elastic = full waist opening × `elastic_ratio` (default 0.92)
- per-leg swim elastic = (front + back leg curves) × `leg_elastic_ratio` (0.88)

## Pieces

| Piece  | Cut                     | Notes                                   |
|--------|-------------------------|-----------------------------------------|
| front  | 1 on fold (mirror)      | high-cut → boyshort via `leg_line`      |
| back   | 1 on fold (mirror)      | seat fullness via `back_coverage`       |
| gusset | 2 on fold (self + mesh) | front/back edges match bodies by build  |

## Construction order

1. Sandwich the gusset self + mesh liner to the **front** at the front match
   notch (gusset `front_edge` ↔ front `gusset_edge`), then to the **back**
   (gusset `back_edge` ↔ back `gusset_edge`); the gusset side edge is caught
   flat, later trapped under the leg elastic.
2. **Sides**: `fixed` → seam front `side` ↔ back `side` (they match by build);
   `tie` → bind each side edge and anchor a self-fabric tie front and back so
   the halves knot at the hip.
3. Apply **swim leg elastic** to each leg opening (quarter-marked), then the
   **swim waist elastic** as a joined ring — both zigzagged / coverstitched into
   the marked zones. Ballpoint 75/11 needle; stretch overlock every seam.

## Known v0 simplifications (documented, not hidden)

- Front and back share one rise height (no separate back rise).
- The side seam is a straight vertical segment at the outer hip; hip flare is
  not modelled, so the seam matches front-to-back exactly.
- Leg beziers are smooth teaching curves; the leg-elastic formula spans the
  front and back leg curves only, with the gusset side edges caught underneath.
- Swim tricot ages faster than a woven in the digital twin (chlorine/salt on
  elastane) — this draft does not model that ageing, only the cut and the BOM.

```bash
python apps/api/services/engine/fc_runner.py projects/bikini-bottom/main.py bikini-bottom.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/bikini-bottom/main.py tie.svg '{"side_style":"tie","leg_line":90}' svg
```

Official visualizer and configurator: Fashion Cabinet.

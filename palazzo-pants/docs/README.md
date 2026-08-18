# Palazzo Pants — FC-100 rank #79

**EN** — A dramatically wide-leg pull-on trouser on the **sweatpants
side-seamed woven block**. Separate front and back legs (cut 2 each) flare from
the hip to a very wide hem on **both** the outseam and the inseam: the outseam
kicks out to `side_flare` at the hem and both legs share one flared side curve,
so the side seams match by construction. The front inseam is bowed by a solved
bisection to match the deeper back fork (delta ≈ 0). The waist finish is a
select — `elastic` (default, no opening) or `side_zip` (a left-side zip-stop
notch on the outseam plus a zipper BOM line). An elastic waistband **casing**
(two mirror halves joined at the sides, folded on its centre line to a channel)
carries the elastic, which is cut shorter than the body to gather the pull-on
waist. Fabric: `materials/popelina-algodon` (a soft, flowing plain weave).

**ES** — Pantalón palazzo de tiro sin bragueta sobre el **bloque de tela con
costura lateral del pants**. Piernas delantera y trasera separadas (cortar 2 de
cada una) que se ensanchan desde la cadera hasta un bajo muy amplio tanto en el
**costado** como en la **entrepierna**: el costado sale hasta `side_flare` en el
bajo y ambas piernas comparten la misma curva de costado, de modo que los
costados coinciden por construcción. La entrepierna delantera se curva por
bisección hasta igualar el tiro trasero más profundo (delta ≈ 0). El acabado de
cintura es seleccionable: `elastic` (por defecto, sin abertura) o `side_zip`
(piquete de tope de cierre en el costado izquierdo más una línea de cierre en el
BOM). La pretina de **casing** con elástico (dos mitades espejo unidas en los
costados, dobladas sobre su línea central formando un canal) lleva el elástico,
cortado más corto que el cuerpo para fruncir la cintura de tiro.

## Pieces / Piezas

- **front** — Front Leg / Pierna Delantera (cut 2, mirror). Edges: `side`,
  `waist`, `crotch`, `inseam`, `hem`.
- **back** — Back Leg / Pierna Trasera (cut 2, mirror). Deeper crotch fork and
  a touch wider hem; same edge names.
- **waistband** — Waistband Casing half / Pretina (casing) mitad (cut 2,
  mirror). A straight strip folded on its centre `fold line` into the elastic
  channel.

## Declared seams / Costuras declaradas

- `front.side ↔ back.side` (equal by construction, delta 0).
- `front.inseam ↔ back.inseam` (front bow solved, delta ≈ 0).
- `waistband.bottom ↔ front.waist + back.waist`, with the join/overlap
  allowance carried as declared seam **ease**.

## Construction order / Orden de construcción

1. Sew the front and back legs together at the **inseams**.
2. Sew the **outseams** (side seams). For `side_zip`, leave the LEFT side open
   above the zip-stop notch and insert the zipper (see BOM).
3. Join the two casing halves into a loop, fold on the centre line, and sew the
   casing to the assembled waist; leave a gap to thread the **elastic**.
4. Thread the elastic (cut to ~0.9× waist), overlap and secure, close the gap.
5. Turn and topstitch the **hem** allowance.

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- No shaped/contour waistband and no pockets — a clean pull-on draft.
- The elastic cut length is approximated from the hip girth (palazzos are
  drafted to the hip); tune it to the wearer's relaxed waist.
- The zipper is a **hard good**: it federates to a Yantra4D notion cartridge via
  the `side_closure` (zipper_tape) interface / BOM note, not drafted here.
- Single-layer yardage in the BOM is a rough estimate at ~1500 mm fabric width.

```bash
python apps/api/services/engine/fc_runner.py projects/palazzo-pants/main.py palazzo-pants.svg '{}' svg
```

Official visualizer and configurator: Fashion Cabinet

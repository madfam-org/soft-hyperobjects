# Bermuda Shorts — FC-100 rank #83

Tailored woven shorts on the **chino trouser block**, cropped to
just-above-the-knee (inseam ~180–320 mm, default 230 mm). Bermudas are
essentially chinos cut short, so the block, the grown-on fly, the two-piece
waistband, the slash pockets and the belt loops are carried straight over from
the `chinos` cartridge; the short hem length and the optional turn-up cuff
follow the `denim-shorts` cartridge.

Las bermudas son básicamente un chino cortado a la altura de la rodilla: el
bloque, la aletilla unida, la pretina en dos piezas, los bolsillos sesgados y
las trabillas vienen del cartucho `chinos`; el largo corto y la vuelta opcional
siguen al cartucho `denim-shorts`.

## Pieces / Piezas

- **Front Leg / Pierna Delantera** — cut 2, mirrored. Grown-on fly extension on
  the upper crotch edge (a line down the extension, then a bezier rejoining the
  fork with tangent continuity), a **fly J-topstitch** guide, a **fly-stop
  notch**, a ~150 mm diagonal **slash-pocket opening** from waist to side, a
  pressed **front crease**, and (when enabled) a **turn-up cuff fold line**.
- **Back Leg / Pierna Trasera** — cut 2, mirrored. Two **back waist darts**
  (intake 12 mm, length 80 mm), a **back-pocket placement** rectangle, a pressed
  **back crease**, and (when enabled) a **cuff fold line**. The back hem width is
  **solved by bisection** so the back inseam matches the front inseam exactly.
- **Waistband (half) / Pretina (mitad)** — cut 2, mirrored. Two straight halves
  that meet at centre-front; the bottom edge is verified against front + back
  waists with the 40 mm closure overlap declared as seam ease. Carries a fold
  line for the folded (doubled) finish.
- **Belt Loop / Trabilla** — cut 5. A 55 × 12 mm strip.

## Construction order / Orden de confección

1. Mark darts, creases, pockets, the fly J and (if used) the cuff fold on each
   leg. Sew and press the two back darts.
2. Assemble the fly: sew the front crotch below the fly-stop notch, then finish
   the grown-on fly extension around the zipper (the extension folds back as the
   fly facing — it is not sewn to the back fork).
3. Join front to back at the inseams and the outseams (both balanced by
   construction; the side seams are equal, the inseams matched by the solved
   back hem).
4. Attach the two-piece waistband to the assembled waist, closing with a
   hook-and-bar plus a button on the overlap. Bar-tack the five belt loops.
5. Hem the legs — a plain turned hem, or fold the turn-up cuff along the marked
   fold line when `cuff_depth > 0`.

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- The **fly shield / French bearer** is simplified out; the fly zipper (or fly
  button) federates to a **Yantra4D** notion via the `fly` (zipper_tape)
  interface rather than being drafted here. Same for the trouser hook-and-bar
  and the waist button — all hardware lives as Yantra4D cartridge references in
  the BOM, per the federation contract.
- Darts, pockets, creases and the cuff fold are **placement markings**, not cut
  geometry — pocket bags and the cuff turn-back are left to the maker.
- The front/back **fork seam is not declared as a single balanced edge**: the
  front crotch edge includes the fly extension (which folds back as facing), so
  a whole-edge length check would assert a false balance. The fork joins below
  the fly-stop notch, which is marked on the front leg.

## Verified relationships / Relaciones verificadas

- `front.side ↔ back.side` — delta 0.0 mm (equal by construction).
- `front.inseam ↔ back.inseam` — delta 0.0 mm (back hem solved to match).
- `waistband.bottom ↔ front.waist + back.waist` — delta 0.0 mm with a 60 mm ease
  (40 mm closure overlap + 2 × seam allowance).

Fabrics: `materials/popelina-algodon` (cotton poplin) or `materials/manta-cruda`
(raw canvas, for a chino-canvas look).

```bash
python apps/api/services/engine/fc_runner.py projects/bermuda-shorts/main.py bermuda-shorts.svg '{}' svg
```

Official visualizer and configurator: Fashion Cabinet
Visualizador y configurador oficial: Fashion Cabinet

# Puffer Vest / Chaleco acolchado — FC-100 #64

**EN** — A roomy, sleeveless insulated zip vest (a *gilet* / puffer body vest) —
the puffer jacket with the sleeves removed, drafted teaching-grade. The front is
cut as **two mirrored halves** whose center edge is a **full separating zipper**
seam; with no sleeve, each **armhole is a finished/bound edge** (the waistcoat's
bound-armscye method). The signature is the **quilting**: horizontal **quilt
channels** are drawn as sew-through *traces* on the shell of the front and back
at a `channel_spacing` parameter, and the garment is **shell + lining quilted
over the insulation** (down or synthetic fill) between them. A **stand / funnel
collar** is solved by bisection to the neck opening, and the **hem is a
bound / elastic-cased** finished edge. Every sewn seam is declared and
length-checked by the kernel, so the geometry regenerates as you change
measurements.

**ES** — Un chaleco acolchado con cierre, holgado y sin mangas (un *gilet* /
cuerpo de puffer) — la chamarra puffer sin las mangas, con trazo de grado
didáctico. El delantero se corta en **dos mitades espejadas** cuyo borde central
es la costura de un **cierre separable completo**; al no haber manga, cada
**sisa es un borde terminado/ribeteado** (el método de sisa ribeteada del chaleco
de vestir). La firma es el **acolchado**: los **canales** horizontales se trazan
como líneas de pespunte pasante sobre el shell del delantero y el trasero según
un parámetro `channel_spacing`, y la prenda es **shell + forro acolchados sobre
el aislante** (relleno de pluma o sintético) en medio. Un **cuello alto / tipo
embudo** se resuelve por bisección contra la abertura de cuello, y el
**dobladillo es un borde terminado con elástico/jareta**. Cada costura cosida
está declarada y verificada por el kernel, así que la geometría se regenera al
cambiar las medidas.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front (zip half, quilted) | Delantero (mitad del cierre, acolchado) | cut 2, mirror |
| `back` | Back (quilted) | Trasero (acolchado) | cut 1 on fold |
| `collar` | Stand collar (funnel) | Cuello alto (embudo) | cut 1 on fold |

The armhole and the hem are **finished edges, not pieces**: the armscye is bound
(strip or elastic) and the hem is an elastic-cased casing. The insulation fill,
the lining, and the separating zipper are **BOM**, not drafted geometry. / La
sisa y el dobladillo son **cantos terminados, no piezas**: la sisa se ribetea
(tira o elástico) y el dobladillo es una jareta con elástico. El relleno, el
forro y el cierre separable son **BOM**, no geometría trazada.

## Construction order / Orden de confección

1. Cut the shell (2 fronts, 1 back on fold, 1 collar on fold) and the lining to
   match; cut the insulation batt to the body panels. Mark the **quilt channels**
   on the shell. *Corte el shell (2 delanteros, 1 trasero al doblez, 1 cuello al
   doblez) y el forro igual; corte el aislante a los paneles del cuerpo. Marque
   los **canales de acolchado** sobre el shell.*
2. **Quilt** each body panel: sandwich shell + fill + lining and sew through
   along the channel traces so the loft is held in place. *Acolche cada panel:
   una shell + relleno + forro y pespuntee sobre los canales para fijar el loft.*
3. Join front to back at the **shoulder** and **side** seams (right sides
   together, through all layers). *Una delantero con trasero en **hombro** y
   **costado** (derechos juntos, por todas las capas).*
4. Install the **separating zipper** down the two front center edges (15 mm tape
   allowance, top/bottom stops at the notches, stitch line at 7 mm). The
   slider/pull is a Yantra4D part — see the `zipper-notion` cartridge.
   *Instale el **cierre separable** en los dos bordes centrales (margen de cinta
   15 mm, topes en los piquetes, pespunte a 7 mm). El deslizador es una pieza de
   Yantra4D — vea el cartucho `zipper-notion`.*
5. Solve and attach the **stand/funnel collar**: its neckline edge equals the
   full neck opening; sew it around the neckline, catching the zipper tape ends
   at center front. *Resuelva y monte el **cuello alto**: su borde de escote
   iguala la abertura de cuello; cósalo al escote atrapando los extremos de la
   cinta del cierre al centro delantero.*
6. **Bind the two armscyes** — there is no sleeve; each armhole is a finished
   edge (bias binding or a folded elastic). *Ribetee las dos **sisas** — no hay
   manga; cada sisa es un canto terminado (bies o elástico doblado).*
7. Finish the **hem** as an elastic/drawcord casing at the hem-draw ratio; feed
   the elastic and secure the ends. *Termine el **dobladillo** como jareta con
   elástico/cordón a la proporción de ajuste; pase el elástico y fije los
   extremos.*
8. If enabled, make the **zip hand-warmer pockets** at the marked openings (welt
   method; the pocket zips are another `zipper-notion` reference). *Si están
   activadas, haga las **bolsas con cierre** en las aberturas marcadas (método de
   vista; los cierres de bolsa son otra referencia `zipper-notion`).*

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **The loft is BOM, not geometry.** The pattern draws a normal roomy vest; the
  puffer volume comes from the insulation batt between shell and lining. The
  quilt channels are *traces* (sew-through markings), exactly like the blazer's
  pocket markings. Real production would also add a few millimetres of "loft
  take-up" per channel — omitted here. *El loft es BOM, no geometría: el patrón
  traza un chaleco holgado normal; el volumen viene del aislante entre shell y
  forro. Los canales son trazos. La producción real sumaría unos milímetros de
  "consumo por loft" por canal — omitido aquí.*
- **Sleeveless = bound armscye.** The armhole is a clean, slightly scooped curve
  finished by binding — never a declared seam (there is no sleeve to check it
  against). *Sin mangas = sisa ribeteada. La sisa es una curva limpia terminada
  con ribete — nunca una costura declarada.*
- **The collar is a single solved band.** A stand/funnel collar cut 1 on fold at
  center back, its neckline length bisection-solved to the half neck opening
  (delta ≈ 0). A separate under-collar / two-piece topstitched funnel is future
  work. *El cuello es una banda única resuelta. Un cuello alto al doblez en el
  centro trasero, con su escote resuelto por bisección a la media abertura
  (delta ≈ 0). Un cuello de dos piezas es trabajo futuro.*
- **Zipper hardware is federated.** The separating-zipper slider and pull are
  Yantra4D solids referenced through the `zipper-notion` cartridge, never
  re-implemented here. *El herraje del cierre está federado: deslizador y tirador
  son sólidos de Yantra4D vía `zipper-notion`.*

## Parameters / Parámetros

`chest_girth`, `body_length`, `neck_girth`, `puffer_ease` (roomy ease over
layers), `channel_spacing` (quilt channel pitch), `collar_height`, `loft_mm`
(insulation loft), `hem_elastic` (hem draw ratio), `pockets` (zip hand-warmer
markings on/off), `seam_allowance`, `hem_allowance`. Presets: **size-m**,
**size-l**.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

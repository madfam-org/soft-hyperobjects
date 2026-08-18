# Hi-Vis Safety Vest / Chaleco de alta visibilidad — FC-100 #89

**EN** — The classic economy **high-visibility safety vest**, drafted
teaching-grade — the simplest workwear garment in the commons. A **boxy,
sleeveless over-vest** worn over street clothes: a straight **front** cut as
**two mirrored halves** that close at center front with **hook-and-loop**
(Velcro), and a **back** cut **on fold**. Every canonical edge — **neck, both
armscyes, hem and the two front closing edges** — is a **bias-bound finished
edge** (no sleeve, no folded hem). The signature is the **retroreflective tape**
in the **EN ISO 20471** configuration: horizontal band(s) that **encircle the
torso** plus vertical **shoulder braces**, drawn as placement *traces* whose
total run is **summed off the geometry** into the BOM. Every sewn seam is
declared and length-checked by the kernel, so the geometry regenerates as you
change measurements.

**ES** — El clásico **chaleco económico de alta visibilidad**, con trazo de
grado didáctico — la prenda de ropa de trabajo más simple del commons. Un
**chaleco cuadrado, sin mangas**, que se lleva sobre la ropa: un **delantero**
recto cortado en **dos mitades espejadas** que cierran al centro con **velcro**,
y un **trasero** al **doblez**. Cada canto canónico — **escote, ambas sisas,
dobladillo y los dos bordes de cierre del delantero** — es un **canto terminado
con bies** (sin manga, sin dobladillo doblado). La firma es la **cinta
retrorreflejante** en la configuración de la **EN ISO 20471**: banda(s)
horizontal(es) que **rodean el torso** más **tirantes** verticales sobre los
hombros, trazados como líneas de colocación cuyo recorrido total se **suma a
partir de la geometría** hacia el BOM. Cada costura cosida está declarada y
verificada por el kernel, así que la geometría se regenera al cambiar las
medidas.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front (hook-loop, taped) | Delantero (velcro, con cinta) | cut 2, mirror |
| `back` | Back (taped) | Trasero (con cinta) | cut 1 on fold |
| `neck_binding` | Neck Binding (bias) | Vivo de Escote (bies) | strip |
| `armhole_binding` | Armhole Binding (bias) | Vivo de Sisa (bies) | strip |
| `hem_binding` | Hem Binding (bias) | Vivo de Dobladillo (bies) | strip |
| `front_binding` | Front Edge Binding (bias) | Vivo de Borde Delantero (bies) | strip |

The neck, both armscyes, the hem and the two front closing edges are **finished
by binding, not pieces of the body**; the binding strips are drafted cut-ready,
their length = the measured opening × the binding ratio. The **reflective tape**
and the **hook-and-loop tape** are **BOM/notions**, not drafted geometry. / El
escote, las dos sisas, el dobladillo y los dos bordes de cierre se **terminan con
vivo, no son piezas del cuerpo**; las tiras de vivo se trazan listas para cortar,
su largo = la abertura medida × la proporción de vivo. La **cinta reflejante** y
el **velcro** son **BOM/insumos**, no geometría trazada.

## Reflective-tape layout / Colocación de la cinta (EN ISO 20471)

The tape is placed as `fc.Internal(kind="trace")` lines — **band centres** and
**brace columns** — topstitched onto the panels:

- **Horizontal bands** (default 2) span each panel at **shared front↔back
  levels**, so at every side seam a front band meets its back band exactly and
  the band **encircles the torso**. Band width is `tape_width` (default 50 mm —
  the EN ISO 20471 minimum), centred on the trace.
- **Vertical braces** run **shoulder-to-hem** at matching front/back columns, so
  they read as one continuous stripe over the shoulder seam: one brace per front
  half (×2) + one per back half (×2 mirrored) = **4 braces**.
- The **total tape run** (exact mm) is summed off the trace geometry and written
  to the BOM and metadata — it is derived, never guessed.

*La cinta se coloca como líneas `fc.Internal(kind="trace")` — centros de banda y
columnas de tirante — pespunteadas sobre los paneles: bandas horizontales (2 por
defecto) a niveles compartidos delantero↔trasero para que rodeen el torso, y
tirantes verticales de hombro a dobladillo en columnas coincidentes. El recorrido
total se suma a partir de la geometría hacia el BOM.*

## Construction order / Orden de confección

1. Cut 2 fronts + 1 back on fold in the fluorescent hi-vis fabric; cut the four
   bias-binding strips. Mark the **reflective bands + braces** and the
   **hook/loop strips** on the panels. *Corte 2 delanteros + 1 trasero al doblez
   en la tela fluorescente; corte las cuatro tiras de bies. Marque las **bandas +
   tirantes** reflejantes y las **tiras de velcro**.*
2. **Topstitch the retroreflective tape** along the marked band centres and brace
   columns (bands first, then braces so the vertical crosses on top). *Pespuntee
   la **cinta retrorreflejante** sobre los centros de banda y las columnas de
   tirante marcados.*
3. Join front to back at the **shoulder** and **side** seams (right sides
   together). *Una delantero con trasero en **hombro** y **costado**.*
4. **Bind** the neck, both armscyes and the hem with bias binding (folded double);
   there is no sleeve and no folded hem. *Ribetee escote, ambas sisas y
   dobladillo con bies (doblado doble); no hay manga ni dobladillo doblado.*
5. **Bind the two front closing edges**, then sew the **hook-and-loop** strips —
   a hook strip on one front, a loop strip on the other, at the ~overlap width.
   Make it a **breakaway / tear-away** closure. The tape hardware is a Yantra4D
   part — see the `hook-loop-tape` cartridge. *Ribetee los dos bordes delanteros
   y cosa el **velcro** — gancho en un delantero, felpa en el otro. Hágalo
   **desprendible**. El herraje es una pieza de Yantra4D — vea `hook-loop-tape`.*
6. If enabled, make the **ID/badge + phone pocket** at the marked boxes (markings;
   bag pieces are future work). *Si están activadas, haga la **bolsa de gafete +
   teléfono** en los recuadros marcados.*

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **The reflective tape is a placement layout + a BOM run, not a sewn seam.** The
  cartridge draws the band centres and brace columns as traces and sums the total
  tape length; the tape itself is a purchased retroreflective ribbon topstitched
  on. *La cinta reflejante es una colocación + un recorrido en BOM, no una costura
  cosida.*
- **Compliance is a step beyond geometry.** EN ISO 20471 visibility **class**
  depends on certified **fluorescent background area** + **retroreflective band
  area** + placement; this cartridge draws the placement and computes the tape
  run, but the certified fabric and the area minimums are a compliance
  requirement, not something the geometry can assert. Keep `tape_width ≥ 50 mm`
  and use a **certified fluorescent background**. *El cumplimiento es un paso más
  allá de la geometría: la clase EN ISO 20471 depende del área de fondo
  fluorescente certificado + el área de banda + la colocación.*
- **Fabric is the closest technical card.** Real hi-vis is a **fluorescent
  polyester knit/mesh** for breathability; the `nylon-ripstop-shell` card is the
  closest technical base in the commons, and **mesh is a fabric swap** (noted in
  the BOM). *La tela real es un tejido/malla de poliéster fluorescente; la ficha
  ripstop es la base técnica más cercana y la malla es un cambio de tela.*
- **Sleeveless = bound armscye.** The armhole is a clean, slightly scooped curve
  finished by binding — never a declared seam (there is no sleeve to check it
  against). *Sin mangas = sisa ribeteada.*
- **Hook-and-loop hardware is federated.** The hook-and-loop tape is a purchased
  notion referenced through a Yantra4D cartridge, never re-implemented here. *El
  velcro es un insumo referenciado vía un cartucho de Yantra4D.*

## Parameters / Parámetros

`chest_girth` (over clothes), `body_length` (nape to hem), `neck_girth`,
`vest_ease` (roomy ease over layers), `overlap` (CF hook-loop overlap),
`tape_width` (reflective band width), `band_count` (1–3 horizontal bands),
`binding_ratio`, `binding_width`, `pockets` (ID + phone pocket markings on/off),
`seam_allowance`, `hem_allowance` (0 = bound). Presets: **size-m**, **size-l**.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

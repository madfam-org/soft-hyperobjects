# Abaya — FC-100 #98

A long, loose, floor-length overgarment, offered here as a **teaching-grade
parametric draft, respectfully**. The abaya is a cultural garment; this
cartridge supplies an honest pattern block, not an identity. The wearer chooses
the fabric, the length, and any embellishment.

Prenda exterior larga, holgada y hasta el suelo, ofrecida aquí como **trazo
paramétrico didáctico, con respeto**. La abaya es una prenda cultural; este
cartucho aporta un bloque de patrón honesto, no una identidad. Quien la viste
elige la tela, el largo y cualquier adorno.

## The cut we modelled / El corte que modelamos

The classic **front-open ("open abaya")** style — the most common
made-to-measure cut. The two fronts meet at centre front but are not joined;
the garment is worn open or with one discreet neck closure. The **closed
overhead** style is a different draft and is not modelled here.

El estilo clásico **abierto al frente ("abaya abierta")**, el corte a medida más
común. Los dos delanteros se encuentran en el centro delantero pero no se unen;
se lleva abierta o con un solo cierre discreto de escote. El estilo **cerrado
por la cabeza** es otro trazo y no se modela aquí.

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **Dropped shoulder.** The shoulder is low and wide, so the armhole is a short,
  shallow curve and the sleeve cap is drafted **flat to it (cap ease 0)** — no
  set-in cap ease, which is realistic for a loose overgarment and keeps the seam
  balance exact.
- **Minimal body shaping.** Straight side seams with an optional hem flare. There
  is no bust dart, no waist suppression — the drape is the point.
- **Fabric stand-in.** The default fabric card is `popelina-algodon` (cotton
  poplin), a crisp woven chosen because it is in the commons and drapes for
  teaching. **Production abaya is commonly crepe or nidha**; substitute a fluid,
  drapey woven for a garment that hangs like the real thing.
- **One continuous binding.** A single straight binding strip finishes the whole
  opening — back neckline + both front necklines + both centre-front edges — in
  one run. Its length is derived from the measured edges, so it always matches.

## Pieces / Piezas

| id | piece | cut |
|----|-------|-----|
| `back` | Back panel | cut 1 on fold at centre back |
| `front` | Front panel (open at CF) | cut 2 mirrored |
| `sleeve` | Long wide sleeve | cut 2 mirrored |
| `binding` | Neck & front binding strip | cut 1 |

## Construction order / Orden de construcción

1. Stitch **front shoulders to back shoulders** (front ↔ back shoulder seam).
2. Set each **sleeve** into the armscye — one cap sews to one front armhole plus
   one back armhole (cap ease 0); match at the shoulder notch.
3. Close each **sleeve underarm** and continue down the **side seams**
   (front ↔ back), in one line from wrist to hem.
4. Apply the **binding** around the neckline and down both centre-front edges in
   a single pass; it is cut doubled and pressed to the finished width.
5. Narrow-hem the **centre-front opening** and the **floor hem**; hem the sleeve
   wrists.
6. Optional: add one discreet neck closure — a hidden snap or a fabric self-tie.
   Snap/hook **hard goods federate to Yantra4D** (snap-fastener family) and are
   never modelled in this cartridge.

## Parameters / Parámetros

`chest_girth`, `abaya_length` (nape to floor), `neck_girth`, `sleeve_length`
(shoulder to wrist), `drape_ease` (very generous total ease), `hem_flare` (per
side), `sleeve_width` (half wrist opening), `seam_allowance`, `hem_allowance`.
Dispatch a single piece with `target_piece` = `back` | `front` | `sleeve` |
`binding` | `set`.

## Seams (all verified, delta ≈ 0) / Costuras (todas verificadas)

- front.shoulder ↔ back.shoulder
- front.side ↔ back.side
- sleeve.cap ↔ (front.armhole + back.armhole), ease 0
- sleeve.underarm_front ↔ sleeve.underarm_back
- binding.bottom ↔ (back.neck + 2× front.neck + 2× front.center_front)

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

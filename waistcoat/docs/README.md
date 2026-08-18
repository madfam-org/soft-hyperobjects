# Waistcoat / Chaleco de vestir — FC-100 #69

**EN** — A classic single-breasted, five-button suit waistcoat (vest), drafted
teaching-grade. It is *sleeveless tailoring*: a shaped front panel with a **deep
V-neck** to the top button, the signature **pointed front hem**, a **fisheye
waist dart**, welt-pocket markings, and a **cinched, lined back** pulled in by an
adjustable **cinch belt**. Every sewn seam is declared and length-checked by the
kernel, so the geometry regenerates as you change measurements.

**ES** — Un chaleco de vestir clásico de un solo pecho y cinco botones, con trazo
de grado didáctico. Es *sastrería sin manga*: un delantero formado con **escote
en V profundo** hasta el botón superior, la **punta delantera** característica,
una **pinza de pez** en la cintura, marcas de bolsillo de vista y una **espalda
entallada y forrada** ceñida por un **cinturón de ajuste**. Cada costura cosida
está declarada y verificada por el kernel, así que la geometría se regenera al
cambiar las medidas.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front (worsted wool) | Delantero (lana peinada) | cut 2, mirror |
| `back` | Back (lining/satin) | Espalda (forro/satén) | cut 2, mirror — CB seam |
| `facing` | Front facing | Vista delantera | cut 2, mirror |
| `cinch_strap` | Cinch strap (buckle + tongue) | Tira de ajuste (hebilla + lengüeta) | cut 2 |

## Construction order / Orden de confección

1. Interface the fronts and facings; mark the CF, the five buttonholes, the
   fisheye dart, and the welt pockets. *Entretele delanteros y vistas; marque el
   CF, los cinco ojales, la pinza de pez y los bolsillos de vista.*
2. Sew the front fisheye dart; make the welt pockets (v0 = markings only, jetting
   is future work). *Cosa la pinza de pez; haga los bolsillos de vista (v0 = solo
   marcas; el vivo/jetting es trabajo futuro).*
3. Join front to back at the **shoulder** and **side** seams. *Una delantero con
   espalda en **hombro** y **costado**.*
4. Sew the shaped **center-back seam** (the cinch shaping) on the lining back.
   *Cosa la **costura central** formada (el entalle) en la espalda de forro.*
5. Attach the **facing** to the CF + V-neck run (right sides together), turn and
   press. *Monte la **vista** al recorrido de CF + escote en V, voltee y planche.*
6. **Bind or face the armscyes and the V-neck** — there is no sleeve; the armhole
   is a finished edge. *Ribetee o forre las sisas y el escote — no hay manga; la
   sisa es un canto terminado.*
7. Make the two **cinch straps**, fit the **buckle + slider**, and anchor them at
   the back cinch marks. *Arme las dos **tiras de ajuste**, coloque la **hebilla +
   corredera** y fíjelas en las marcas traseras.*
8. Line the fronts, finish the pointed hem, and sew on the five front buttons.
   *Forre los delanteros, termine la punta del bajo y cosa los cinco botones.*

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **Sleeveless — bound armscye.** The armhole is drafted as a finished/bound edge
  (a clean armscye curve). No sleeve piece; bind or face it in construction. *La
  sisa se traza como canto terminado; ribetéela o fórrela.*
- **Straight facing.** The facing is a straight strip whose length is verified
  against the measured center + V-neck run (`facing.long_edge` vs
  `front.center + front.neck`, with 2×seam-allowance declared as ease). A shaped
  facing that mirrors the point and V is future work. *Vista recta verificada
  contra el recorrido medido; una vista formada es trabajo futuro.*
- **Lining noted, not fully drafted.** The back is drafted in lining; the front
  lining and welt-bag pieces are called out in the BOM but not separately
  drafted in v0. *El forro delantero y las bolsas de welt se anotan en la BOM,
  no se trazan por separado en v0.*
- **Welt pockets are markings.** The two lower welts and the breast welt are
  drilled placement markings; jetting/welting is a future construction guide.
  *Los welts son marcas; el vivo es guía futura.*
- **No tailored canvas.** Fusible interfacing stands in for a full canvassed
  front. *Entretela fusionable en lugar de crin/entretela de sastre.*

## Hardware / Herraje

Buttons, the **cinch buckle**, and the **slider** are **Yantra4D** cartridges,
referenced in the BOM — never re-implemented in this kernel (Fashion Cabinet is
soft goods; hard goods federate to Yantra4D). *Los botones, la hebilla y la
corredera son cartuchos de Yantra4D, referenciados en la BOM.*

## Fabric / Tela

`lana-peinada-traje` — worsted wool suiting (260 gsm) for the fronts; the back
and full lining are cut in lining/satin. Pre-shrink, interface the fronts and
facings, and press hard — pressing is half the tailoring. *Lana peinada para los
delanteros; espalda y forro en satén.*

Official visualizer and configurator: Fashion Cabinet ·
Visualizador y configurador oficial: Fashion Cabinet

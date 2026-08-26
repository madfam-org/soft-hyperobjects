# Dirndl laced bodice (Mieder)

The fitted, lightly-boned upper of the Alpine dirndl (**Mieder**) — a shaped corselet closed at
the centre front by a lace crossed through two columns of metal eyelets, worn over a blouse.

Part of the **Fashion Cabinet Commons** (FC-400, lane 10 — heritage). Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A laced bodice is the garment where the fastener and the pattern have to be designed together:
> draft the fronts to meet, punch eyelets afterward, and there is no gap for the lace.

## Provenance

The dirndl is **Alpine regional dress** (Bavaria/Austria), with strong regional and
class-historical associations. This cartridge drafts a plain everyday laced **Mieder**. It
carries no regional trim or apron and invents no ornament.

## Why it earns its rank

**The eyelet columns are spaced, and the lace gap is real cloth.** A laced bodice does **not**
meet edge-to-edge; it is drafted with a deliberate **lacing gap** between the two front edges,
spanned by the crossed lace. So the two fronts together are cut **narrower** than the finished
chest by the gap (`fronts + gap = finished bust`), the front width is solved **around** the gap,
and the eyelets are placed in even columns whose count is solved from the front edge length and
pitch.

**The eyelets are hardware, and one number sizes them.** Each eyelet is the Yantra4D
`garment-eyelet` solid; `eyelet_dia` drives **both** the drafted punch mark **and** the printed
eyelet's inner diameter, so the lace, the punched hole and the eyelet agree. The bodice is shaped
by princess/side seams and lightly boned at the front edges so the lacing pulls a smooth line
rather than crushing the cloth.

## Construction notes

Pieces: **front** (cut 2, laced edge + eyelet column), **side_front** (cut 2), **side_back**
(cut 2), **back** (cut 1 on fold).

1. Join the panels around the ring: front → side_front → side_back → back (the back is on the
   fold at centre back). The front is longer than the side panels (it rises over the bust); the
   princess seam eases the difference.
2. Interline and bone the front edges; press the seams open.
3. Set the eyelets down each front edge at the solved pitch, sizing them to `eyelet_dia`.
4. Lace the two fronts across the gap; the lace does the final fit.

## Hardware

The eyelets are **Yantra4D solids** (`notion.hardware_ref → garment-eyelet`, linked):
`inner_dia → eyelet_dia`, `flange_dia = 2.1 × eyelet_dia`, `barrel_h = 3.0 mm`.

## Made to measure

Drafted to **bust**, **underbust** and **waist** girths plus **bodice** and **front** lengths.
The front is drafted to bust-minus-gap and the eyelet count is solved to the edge; every slider
extreme renders watertight.

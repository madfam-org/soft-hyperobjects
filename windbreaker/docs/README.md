# Windbreaker — FC-100 rank #62

A lightweight, **unlined** hooded shell jacket — the **simplest Wave-J
technical piece**: no insulation, no quilting. It is drafted on the same
**zip-hoodie / track-jacket** full-zip block and topped with the
**hoodie-pullover** two-panel hood. The front is cut as **two mirrored halves**
(never on fold) whose center edge is the **separating-zipper seam**: a 15 mm
tape allowance, a 7 mm stitch line, and top/bottom stop notches. The sleeve is
**set-in**, its cap **solved by bisection** against the measured armhole pair
(a small cap ease is carried on the seam). The hood is **two panels** whose
**neck edge is bisection-solved** to the **half** neck opening, so the
hood↔neckline seam balances to delta ≈ 0.

What makes it a windbreaker is the **elastic / drawcord finish**, drafted as
**self-fabric casings** on the shell edges rather than separate rib bands (a
windbreaker is unlined shell, not a sweatshirt):

- **Body hem** → a deep **drawcord casing** (fold line marked) with a drawcord
  threaded through and a **cord stop** at each center-front exit.
- **Sleeve hems** → deep **elastic cuff casings** (fold line marked); each cuff
  elastic is cut to a recovered circumference (`sleeve hem × cuff_ratio`).
- **Hood face** → a **drawcord channel** (marked) with a drawcord + two cord
  stops.

Every cord and elastic length is derived to the **millimetre** in the BOM. The
shell is **DWR-treated ripstop nylon** — wind- and water-resistant (this is
*not* a seam-sealed raincoat; the seams are not taped). Fit is **relaxed**
(`shell_ease` positive, added to the chest). The soft hood **rolls and stows**
into the neckline/collar area (a small CB-neck stow pocket is added at assembly,
not drafted as a separate piece).

Una chamarra shell ligera con capucha **sin forro** — la pieza técnica más
sencilla de la Ola J: sin aislante ni acolchado. Se traza sobre el mismo bloque
de frente con cierre de la sudadera con cierre / track jacket, rematada con la
capucha de dos paneles de la sudadera. Delantero en **dos mitades espejadas**
(nunca al doblez) con la **costura del cierre separable** al centro (margen de
cinta de 15 mm, línea de pespunte a 7 mm, piquetes de tope). Manga **montada**
con copa **resuelta por bisección** a la sisa medida; capucha de **dos paneles**
cuyo borde de cuello se **resuelve** a la mitad de la abertura (delta ≈ 0). El
sello es el **acabado de elástico/jareta** trazado como **jaretas de tela
propia**: jareta de dobladillo con jareta, puños con elástico y canal de jareta
en la cara — cada largo de cordón y elástico derivado **al milímetro** en el
BOM. Shell de **ripstop con DWR**, resistente al viento y al agua (no es un
impermeable con costuras selladas). Ajuste **holgado**; la capucha suave se
enrolla y guarda en el escote.

## Pieces

- **Front (zip half)** (`front`) — cut 2 mirror, never on fold. Center edge is
  the zip seam (15 mm tape allowance + 7 mm stitch line + stop notches). Deep
  hem casing for the drawcord; hand + chest zip-pocket markings.
- **Back** (`back`) — cut 1 on fold at center-back; deep hem casing.
- **Sleeve (set-in)** (`sleeve`) — cut 2 mirror. Cap solved to the armhole pair;
  deep elastic cuff casing at the hem.
- **Hood (side panel)** (`hood`) — cut 2 mirror. Neck edge solved to the half
  opening; face edge carries the drawcord channel.

## Construction order

1. If pockets are on, install the chest zip and the two hand-pocket zips at the
   marked openings **before** closing the fronts.
2. Sew shoulders (front↔back) and side seams (front↔back). Both balance to
   delta ≈ 0.
3. Set the sleeves: ease each solved cap into its armhole (one front + one back
   armhole per physical sleeve), then close each underarm seam.
4. Assemble the hood: join the two panels along the crown and face edges, form
   the **face drawcord channel**, then sew the solved hood neck edge to the
   neckline all the way round (the CF ends align with the front center edges).
5. Turn and topstitch the **body-hem casing** on the marked fold line, leaving
   the two center-front ends open as drawcord exits.
6. Turn and topstitch each **sleeve-hem cuff casing** on its marked fold line,
   leaving a small gap; thread the cut-to-length **cuff elastic** into a ring.
7. Thread the **hem drawcord** and the **hood drawcord**; add a **cord stop** at
   each of the four exits (hardware via Yantra4D).
8. Install the **separating** zipper up the center front; the derived
   `zipper_length_mm` is the length to order.

## Honest v0 simplifications (documented, not hidden)

- **Teaching-grade elastic/drawcord finish.** The signature finish is modelled
  as **self-fabric casings** — a deep per-edge cut **allowance** plus a marked
  interior **fold line** — with the drawcord/elastic lengths carried as
  **exact-mm BOM** numbers. It is genuine unlined-shell construction, but the
  casing depth is an allowance and a trace, not a second drafted panel. There
  are **no separate cuff/hem band pieces** (unlike the sweatshirt cluster); the
  shell edge folds back on itself.
- **Set-in cap ease** is carried as an exact `ease` on the cap↔armhole seam, so
  the cap is genuinely longer than the armhole pair and still balances to
  delta ≈ 0 — a real set-in cap, not a zero-ease shortcut.
- **Two-panel hood solved, not guessed.** The neck edge is bisection-solved to
  the half opening (the hoodie-pullover method); the hood↔neckline seam is
  declared and verified to delta ≈ 0.
- **Relaxed fit via positive ease.** Fit is driven by `shell_ease` added to the
  chest, and the crisp ripstop cuts true — the fabric card's `cut_scale` is
  `1.0`, so no stretch compensation is applied.
- **Pockets are placement markings** (opening trace + bag box), not cut-in bag
  pieces — the common ready-to-wear convention.
- **Not a raincoat.** DWR ripstop is wind/water-*resistant*; the seams are not
  seam-sealed (that is the raincoat's job, on the same shell card).
- **Hardware is federated**: the separating body zipper, the pocket zips, and
  the four cord stops / cord locks are referenced as **Yantra4D** cartridges
  (`zipper-notion`, `drawcord-stop`) in the BOM notes, never re-drafted here
  (per the federation contract).

```bash
python apps/api/services/engine/fc_runner.py projects/windbreaker/main.py windbreaker.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/windbreaker/main.py big.svg '{"chest_girth": 1500, "cuff_ratio": 0.6, "hood_depth": 320}' svg
```

Official visualizer and configurator: Fashion Cabinet.

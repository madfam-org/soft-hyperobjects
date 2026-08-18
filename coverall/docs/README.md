# Coverall — Overol (enterizo) · FC-100 #84

The classic mechanic's / worker's **one-piece coverall** (boilersuit): a
sleeved, collared woven **bodice** joined to a straight-leg **trouser** at a
single declared **waist seam**. It reuses the jumpsuit's verified top-to-bottom
join, the casual-button-down's solved sleeve cap and band collar, and the
chinos leg block — recombined into workwear with a full-length front zip, a
bi-swing action back, and real utility patch pockets.

El **overol industrial de una pieza** (enterizo): un talle de tela plana con
mangas y cuello unido a un pantalón de pierna recta en una sola costura de
cintura declarada. Reutiliza la unión verificada del jumpsuit, la copa de manga
y el cuello mao resueltos de la camisa casual, y el bloque de pierna de los
chinos — recombinados en ropa de trabajo con cierre frontal completo, espalda de
acción bi-swing y bolsas de parche de trabajo reales.

## What makes it a coverall (the three needs)

- **Zip front (`zipper`)** — a full **center-front separating zipper** runs from
  the collar top straight down the whole center front to the waist. Each front
  half is cut with the center edge as the zip seam (15 mm tape allowance, an
  8 mm topstitch guide, top/bottom stop notches). The zip continues up through
  the collar, so the collar's `front_edge` carries the same tape allowance. The
  zipper itself is a **Yantra4D** solid (`zipper-notion`, subtype *separating*) —
  referenced through the manifest `notion`, never re-drafted here.
- **Action back (`action_back`)** — the signature bi-swing. The back is cut on
  fold at CB; its **shoulder edge is drafted longer than the front** by the
  pleat intake (`action_pleat`, default 45 mm per shoulder blade). That extra
  length is folded into an inverted pleat at the shoulder seam, letting the
  wearer reach forward without the back binding. The pleat is a *verified*
  feature: the shoulder seam is declared with the measured intake as **ease**
  (back is the long side), and the three pleat fold lines are traced on the
  back. Set `action_pleat = 0` for a plain back.
- **Patch pockets (`patch_pockets`)** — three **real pocket pieces**, drafted
  with the patch-pocket hexagon idiom (45° bottom chamfers, a hem-facing on the
  opening, a topstitch attach guide): a **chest bib pocket** (cut 2), a **hip
  pocket** (cut 2), and a **thigh tool pocket** (cut 1). Their placement is also
  traced on the bodice front and front leg so the sewer knows where they land.

## The waist seam (the jumpsuit join)

The one thing a one-piece must get right: the bodice and trouser meet at the
waist with no gap. Both sides are driven by the **same waist formulas** —
`WAIST_F = (waist + ease)/4 − quarter_shift`, `WAIST_B = (waist + ease)/4 +
quarter_shift`. The bodice front/back hems and the leg front/back waists are all
set from those two numbers, so the declared **eight-reference** waist seam
(bodice front ×2 + bodice back ×2 ↔ leg front ×2 + leg back ×2, one edge per
physical cut) closes at **delta ≈ 0** by construction. The slanted back-leg
waist edge is solved analytically so its *length* equals the back quarter even
though it rises for the deeper back rise.

## Pieces

| id | label | cut | notes |
|----|-------|-----|-------|
| `bodice_front` | Bodice Front | 2 | CF edge = separating-zip seam; chest-pocket + zip-stitch traces |
| `bodice_back` | Bodice Back (action pleat) | 1 on fold (CB) | shoulder drafted +intake; bi-swing pleat fold lines |
| `sleeve` | Sleeve | 2 | long; cap solved by bisection to front+back armholes (ease 0) |
| `cuff` | Cuff | 2 | buttoned band; length solved to the sleeve-hem opening + overlap |
| `collar` | Band Collar | 2 on fold (CB) | neck edge solved to the neckline; CF carries the zip tape |
| `leg_front` | Leg Front | 2 | side-seamed block; solved inseam bow; thigh-pocket trace |
| `leg_back` | Leg Back | 2 | deeper fork; analytically-solved slanted waist |
| `chest_pocket` | Chest Bib Pocket | 2 | 130 × 150 mm patch |
| `hip_pocket` | Hip Pocket | 2 | 150 × 165 mm patch |
| `thigh_pocket` | Thigh Tool Pocket | 1 | 150 × 175 mm patch |

## Construction order (teaching sketch)

1. Make up the three patch-pocket kinds; press the chamfers and opening facings.
2. Topstitch the chest pocket to a bodice front, the hip pockets to the legs (or
   backs, to taste), and the thigh tool pocket to the front leg — on the traces.
3. Fold and stitch the bodice-back **action pleats** at the shoulder line;
   bar-tack the pleat ends.
4. Join bodice fronts to back at the **shoulder** (easing the pleat intake) and
   the **side** seams. Do the same for the legs (side + inseam), then close each
   leg's **crotch**.
5. Sew the **waist seam**: bodice hems to leg waists all the way round.
6. Solve-and-sew the **collar** to the neckline; set the **sleeves** into the
   armholes; close the **underarm** seams; attach the **cuffs**.
7. Set the **center-front separating zipper** from the collar top down to the
   waist; add snaps at the cuffs and pocket flaps.
8. Hem the legs (plain open hem).

## Honest simplifications (teaching-grade)

- **No fly, no waistband** — the coverall zips at the front and is continuous
  through the waist, so there is deliberately no separate trouser waistband or
  fly; the leg upper crotch is a plain fork edge, and no belt loops are drawn.
- **Bi-swing as shoulder ease** — the action back is modelled as extra shoulder
  length folded at the seam (a real inverted-pleat intake) rather than a
  separately-cut gusset or yoke; the pleat depth below the shoulder is shown as
  traced fold lines, not a shaped seam. This keeps the back a single verified
  piece that still balances the front.
- **Straight legs, plain hem** — no tapering shaping beyond the block, no cuff
  turn-ups on the legs (only the sleeves are cuffed).
- **Placement traces, not seams** — pocket and zip-stitch guides are internal
  markings; only sewn edges are declared as seams and length-verified.
- **Sanforized denim assumed** — the BOM marker length assumes stable cloth;
  raw denim needs larger allowances (see the `mezclilla-denim` card).

## Bill of materials

Heavy 12 oz **denim** (`mezclilla-denim`, 1500 mm width) — or cotton canvas
(`manta-cruda`) for a lighter coverall — plus a **separating CF zipper**, **snap
fasteners** for the cuffs and pocket flaps, **heavy topstitch/bar-tack thread**,
and a jeans needle. All hardware (zipper, snaps) is a **Yantra4D** reference,
not drafted here.

---

Official visualizer and configurator: **Fashion Cabinet** ·
Visualizador y configurador oficial: **Fashion Cabinet**.

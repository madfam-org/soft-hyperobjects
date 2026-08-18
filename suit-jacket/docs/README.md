# Suit Jacket — FC-100 rank #67

Teaching-grade two-button single-breasted **suit jacket** ("saco de traje") in
`materials/lana-peinada-traje` (worsted wool suiting) — the blazer's refined
sibling. Seven pieces: front (cut 2), **side body** (cut 2), back (cut 2 with a
shaped CB seam + vent), a proper **two-piece sleeve** (upper + under, cut 2
each), upper collar (half on fold), and a straight front facing.

## How it differs from the blazer (drafted, not just noted)

The blazer is the gateway; the suit jacket is the refined garment. Three
tailored refinements are drafted here, not deferred:

1. **Three-panel body.** Instead of front + back with a plain side seam, the
   body is split into **front + side body + back**. The side body is the panel
   that straddles the underarm; the armhole is carved across all three panels
   (`front.armhole` + `side_body.armhole` + `back.armhole`). This is how a real
   suit gets chest and waist shape without a visible princess line on the front,
   and it moves the side seams off the body's widest point. Two vertical body
   seams are declared and balanced: `front.side_seam ↔ side_body.front_seam`
   and `side_body.back_seam ↔ back.side_seam` (both delta 0.0).
2. **Two-piece sleeve.** Instead of one eased tube, the sleeve is **upper +
   under**. The **upper sleeve** carries the full eased cap; the **under
   sleeve** is the inner panel that joins along matched **forearm** (front) and
   **hindarm** (back) seams. Both pieces share the same solved seam curves, so
   `upper_sleeve.forearm ↔ under_sleeve.forearm` and the two hindarm seams
   balance exactly (delta 0.0). Four cuff buttons are marked at the hindarm hem
   for a working (or mock) vent.
3. **Structured shoulder + full lining + chest canvas.** The shoulder is
   lightly extended (`shoulder_ext`, default 10 mm) and carries a shoulder-pad +
   floating-chest-canvas placement note; the jacket is drafted to be **fully
   lined** (lining yardage is BOM-costed).

## The lapel, the roll line, and the notch (as in the blazer)

The center edge climbs the 20 mm button stand only as far as the **roll point**
at waist level (`roll_line_y` 300 above the hem) — the top button sits there.
Above it the front **breaks open**: the **lapel** runs as a straight diagonal
out to the lapel point (90 mm past CF at chest level) and the **gorge** runs
back in to the neck point. The **roll line** — an internal from the roll point
to the neck point — is the crease the lapel folds along, which is why the
**facing** (not the front) becomes the public face of the lapel.

In construction the upper collar sews along the gorge and back neck and meets
the lapel at the **notch** — the classic V-gap between collar and lapel point.
Convention holds that gap around **10 mm**; in this v0 the notch is a
construction note, not drafted geometry.

## Three solves, all declared and verified

- **Sleeve cap** — the upper-sleeve cap is bisected to the measured *whole*
  armhole (`front + side_body + back`) **plus the declared cap ease** (default
  28 mm), `declare_seam(..., ease=cap_ease, tol=2.5)`. A tailored cap is longer
  than its armhole on purpose and is shrunk in with steam.
- **Upper collar** — the neck edge is bisected to the measured
  `front.gorge + back.neck` per half (overlap 0, collar-band method).
- **Facing** — the straight facing length is derived from the measured
  `center + lapel + gorge` run plus end allowances, verified with the
  allowances as declared seam ease.

## Pieces & construction order

1. **Front** (cut 2 mirror) — lapel/roll-line front, fisheye waist dart, breast
   welt + jetted-flap hip-pocket markings.
2. **Side body** (cut 2 mirror) — sew to the front along the front side seam.
3. **Back** (cut 2 mirror) — join the CB seam (inlay 15) with the vent; sew the
   side body to the back along the back side seam; close the shoulders.
4. **Two-piece sleeve** — join the upper and under sleeve at the forearm and
   hindarm seams; set the eased cap into the armhole, shrinking the ease with
   steam; mark the cuff buttons.
5. **Upper collar** (half on fold) — sew to the gorge + back neck.
6. **Front facing** (cut 2 mirror) — face the front edge along the center +
   lapel + gorge run.
7. Set shoulder pads and the floating chest canvas; bag the lining; hem; press
   hard at every stage.

## v0 simplifications (honesty notes)

- **Lining is noted, not drafted.** The jacket is fully lined and the lining
  yardage is BOM-costed, but the lining pieces are not drafted in v0 — they
  mirror the shells, less the facing at the front. Drafted lining pieces are
  future work.
- **Fusible + floating chest canvas, not a full pad-stitched canvas.** The BOM
  carries a fusible front + a floating chest-canvas panel and a note; a full
  hand-padded canvas is future work.
- **Two-piece sleeve, honest split.** The **whole** cap↔armhole seam lives on
  the upper sleeve; the under sleeve's shallow scye scoop is the inner underarm
  and is **not** part of the declared cap seam (in a bespoke sleeve a small
  piece of the underarm crosses onto the undersleeve). The two vertical sleeve
  seams are matched exactly. This keeps the seams verifiable while staying an
  honest two-piece.
- **Straight facing.** A shaped facing that mirrors the lapel blade is future
  work; wide lapels get a manifest warning.
- **CB vent is markings.** Two internal lines (underlap 48, stop at
  `vent_height` 260) on the shaped CB seam; the vent's cut extension is future
  work.
- **Pockets are markings.** Breast welt + two jetted-flap hip pockets are marked
  only; jetted-pocket and flap construction pieces are future work.
- **Fisheye dart.** The front waist dart is a marked internal diamond; the
  kernel's dart-rotation pass is a roadmap item, so the dart is marked, not
  rotated.
- **Buttons are hardware** — a Yantra4D cartridge (`shank-button` guide in this
  commons) referenced from the BOM (2 front, 4 per sleeve), never
  re-implemented here.

```bash
python apps/api/services/engine/fc_runner.py projects/suit-jacket/main.py suit-jacket.svg '{}' svg
```

Official visualizer and configurator: Fashion Cabinet.

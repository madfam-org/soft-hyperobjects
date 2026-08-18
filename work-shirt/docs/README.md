# Work Shirt — FC-100 rank #90

The classic two-pocket utility / uniform work shirt ("camisa de trabajo") in
`materials/mezclilla-denim` (chambray-weight denim, 1500 mm width): a slightly
relaxed woven shirt (`body_length` 760, `woven_ease` 200) with a wide
topstitched CF button placket, a **proper two-piece turndown collar**
(stand + fall), a doubled back yoke over a back with a marked CB box pleat, a
set-in sleeve with a placket and a barrel cuff, and — the signature — **two
chest flap pockets drafted as real cut pieces** (a chamfered patch body plus a
button-through flap each).

It reuses the `dress-shirt` (rank #4) architecture — the yoke split, the
sleeve-cap bisection, and the **chained collar solve** (stand → neckline, fall
→ stand top) — and the `casual-button-down` / `chore-coat` button-placket +
patch-pocket idioms, but wears a **wider work placket**, a **relaxed utility
fit**, and carries the pocket **flap as its own real piece** (the `cargo-pants`
flap method) so the flap width is verified against the pocket opening.

## Pieces (9)

| Piece | Cut | Role |
|-------|-----|------|
| `front` | 2, mirrored | one-piece button-placket front; 7 buttonhole crosses, wide topstitched placket box, both chest flap-pocket placements, full front armhole |
| `back` | 1, on fold at CB | top edge ends at the yoke seam; CB box pleat marked; full back armhole below the yoke |
| `yoke` | 1, on fold at CB | doubled; carries the back neck + both shoulders; straight lower edge at the yoke seam |
| `sleeve` | 2, mirrored | set-in sleeve; cap solved to the summed armholes + cap ease; sleeve placket marked |
| `cuff` | 2 | barrel cuff, cut doubled and folded at mid; buttonhole + button |
| `stand` | 2, on fold at CB | collar stand, neck edge solved to the half neckline + button overlap |
| `fall` | 2, on fold at CB | collar fall, neck edge solved to the stand's measured top edge (chained) |
| `chest_pocket` | 2 | breast patch-pocket body — chamfered pouch, hem-faced opening, topstitch guide |
| `pocket_flap` | 2 | button-through flap — angled lower corners, flap buttonhole; opening matches the pocket mouth |

## Solves — all declared and verified (delta ≈ 0)

- **Sleeve cap** is bisected to the measured `front.armhole + back.armhole`
  plus a 14 mm set-in **cap ease** (carried as declared ease).
- **Collar stand** neck edge is bisected to the measured half neckline
  (`front.neck + yoke.neck`) plus a 15 mm button **overlap** (collar-band
  method, declared ease).
- **Collar fall** neck edge is bisected to the stand's **measured top edge** —
  the second solve chained off the first (`fall.neck ↔ stand.top`).
- **Yoke seam**: `yoke.bottom` against `back.top`; the shoulder
  (`front.shoulder ↔ yoke.shoulder`) and side (`front.side ↔ back.side`) seams
  are straight matches; the sleeve underarm closes on itself.
- **Flap ↔ pocket opening**: `pocket_flap.attach` is verified against
  `chest_pocket.top` so the flap covers the mouth exactly.

Eight seam relationships are checked in the full set.

The **flap pockets are topstitched appliqué**, not balance seams: the pocket
body and the flap are each their own closed piece, and the two chest
**placements + flap attach lines are internal traces** on the front. That is
why the pockets appear as pieces and as markings, but their appliqué edges are
never a declared seam — only the flap-to-mouth match is.

## Construction order (teaching-grade)

1. Fuse the CF placket, the collar stand + fall, and the cuffs; mark the
   buttonholes and the two chest-pocket placements.
2. Fold the pocket hem facings; **topstitch the two chest pockets** to their
   placements along the topstitch guide (leave the tops open).
3. Make the two flaps, then set each flap to the front along its attach line
   just above its pocket; topstitch; work the flap buttonhole.
4. Set the yoke to the back (yoke seam, over the box pleat); topstitch.
5. Join shoulders (front ↔ yoke), then the side seams; flat-fell both.
6. Assemble the two-piece collar (stand + fall, each half on fold at CB); set
   it to the neckline, matching the CF / button-line notch.
7. Set the sleeves into the armholes (ease the cap), close the underarm seams,
   then attach the barrel cuffs; topstitch.
8. Hem the shirt; edge-finish and topstitch the front placket.
9. Sew the buttons (placket, cuffs, flaps); work the buttonholes.

## v0 honesty notes

- **Full back armhole on the back piece.** Real work shirts split the armhole
  across the back and the yoke; here the yoke's side edge is straight and the
  whole back armhole is drafted on the back, so the sleeve caps still meet at
  the shoulder point. The yoke seam height is clamped clear of the back neck
  and the underarm.
- **Two-piece turndown collar.** The stand is solved to the neckline and the
  fall is chained to the stand's top edge; both are cut doubled on fold at CB.
  A separate under-collar and a bias band are future work.
- **Flap pockets are single-layer.** The pocket body is one chamfered pouch
  with a hem-faced opening and a topstitch attach guide; the flap is a single
  layer with an angled lower edge and a buttonhole. A lined pocket or a lined
  flap is future work. The bottom corners are 45° clips (the `patch-pocket`
  enabler shape).
- **Set-in sleeve.** The cap is a true set-in cap solved to the summed
  armholes **plus 14 mm ease**; the wrist is a slit placket marking with a
  drill stop, closed by the separate barrel cuff.
- **Box pleat is marked.** The CB box pleat is two internal fold lines at the
  yoke seam; the back is still cut on fold at CB (the pleat is folded in, not
  cut as a separate extension in v0).
- **Cuff** is a rectangle cut doubled in height and folded at mid, with a
  buttonhole + button cross-mark; its length already includes both seam
  allowances.
- **Topstitching** (metadata note): heavy contrast thread, 3 mm gauge, on the
  CF placket, back yoke, collar, cuffs, every pocket + flap edge, and the
  felled structural seams — the workwear look and the durability in one pass.
- **Buttons are hardware** — a Yantra4D cartridge (the `shank-button` guide in
  this commons), referenced from the BOM, never re-implemented here.

## Run

```bash
python apps/api/services/engine/fc_runner.py projects/work-shirt/main.py shirt.svg '{}' svg
```

Single pieces render on their own via `target_piece`, e.g.
`'{"target_piece": "pocket_flap"}'` or `'{"target_piece": "fall"}'`.

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

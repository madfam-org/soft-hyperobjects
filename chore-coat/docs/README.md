# Chore Coat — FC-100 rank #65

The classic French workwear chore coat ("chamarra de trabajo") in
`materials/mezclilla-denim` (12 oz denim, 1500 mm width): boxy and hip-length
(`body_length` 720, `woven_ease` 220), a CF button placket, a flat spread
collar, a set-in sleeve with a buttoned cuff, and — the signature — three big
patch pockets (two hip + one chest).

It reuses the `denim-jacket` (rank #28) workwear architecture — a button-stand
front, buttonhole cross-marks, a back yoke split, a buttoned cuff, and the
solved collar + solved sleeve-cap solves — but keeps a **one-piece front** (a
chore coat has no front yoke), runs **longer to the hip**, wears a **flat
spread collar** instead of a band, and carries **real patch-pocket pieces**
from the `patch-pocket` enabler rather than pocket markings.

## Pieces (8)

| Piece | Cut | Role |
|-------|-----|------|
| `front` | 2, mirrored | one-piece button-stand front; 4 buttonhole crosses, chest + hip pocket placements, full front armhole |
| `back_yoke` | 1, on fold at CB | back neck + both shoulders; straight lower edge at the yoke seam |
| `back_body` | 1, on fold at CB | yoke seam at top, full back armhole below it, straight side + hem |
| `sleeve` | 2, mirrored | set-in sleeve; cap solved to the summed armholes + cap ease; wrist placket marked |
| `cuff` | 2 | rectangular buttoned cuff, cut doubled and folded at mid |
| `collar` | 2, on fold at CB | flat spread collar, neck edge solved to the half neckline + overlap |
| `patch_chest` | 1 | breast patch pocket — chamfered pouch, hem-faced opening, topstitch guide |
| `patch_hip` | 2 | hip patch pockets — the same pouch, one per side |

## Three solves, all declared and verified

- **Sleeve cap** is bisected to the measured `front.armhole + back_body.armhole`
  plus an 18 mm set-in **cap ease** (carried as declared ease), delta ≈ 0.
- **Spread collar** neck edge is bisected to the measured half neckline
  (`front.neck + back_yoke.neck`) plus a 15 mm button **overlap**
  (collar-band method, carried as declared ease), delta ≈ 0.
- **Yoke seam**: `back_yoke.bottom` is verified against `back_body.top`; the
  shoulder (`front.shoulder ↔ back_yoke.shoulder`) and side
  (`front.side ↔ back_body.side`) seams are straight matches; the sleeve
  underarm closes on itself. Six seam relationships are checked in the full set.

The **patch pockets are topstitched appliqué**, not balance seams: each pocket
outline is its own closed piece, and the chest + hip **placements are internal
traces** on the front. That is why the pockets appear as pieces and as
markings, but never as a declared seam.

## Construction order (teaching-grade)

1. Fuse the CF button stand and the collar; mark the buttonholes.
2. Set the back yoke to the back body (yoke seam); topstitch.
3. Join shoulders (front ↔ back yoke), then the side seams; flat-fell both.
4. Solve + assemble the spread collar (half on fold at CB); set it to the
   neckline, matching the CF / button-line notch.
5. Set the sleeves into the armholes (ease the cap), close the underarm seams,
   then attach the buttoned cuffs; topstitch.
6. Hem the coat; edge-finish the front placket.
7. Fold the pocket hem facings, then **topstitch the three patch pockets** to
   their marked placements along the topstitch guide (leave the tops open).
8. Sew the buttons; work the buttonholes.

## v0 honesty notes

- **Patch pockets are single-layer.** The pocket bag is one chamfered pouch
  with a hem-faced opening and a topstitch attach guide; a lined pocket, a
  flap, or a pleated bellows pocket is future work. The bottom corners are cut
  by 45° chamfers (the `patch-pocket` enabler shape).
- **Flat spread collar, one piece.** A single collar (default fall 75 mm)
  solved to the neckline and cut doubled on fold; a two-piece collar with a
  separate stand is future work. The forward `COLLAR_POINT` gives the spread.
- **Back yoke only.** The workwear yoke split is on the **back** (yoke over
  body); the front stays one piece, as a chore coat is cut. The yoke seam
  height is clamped clear of the back neck and the underarm.
- **Set-in sleeve.** The cap is a true set-in cap solved to the summed
  armholes **plus 18 mm ease** (not a flat drop shoulder); the wrist is a slit
  placket marking with a drill stop, closed by the separate cuff.
- **Cuff** is a rectangle cut doubled in height and folded at mid, with a
  buttonhole + button cross-mark; its length already includes both seam
  allowances.
- **Topstitching** (metadata note): heavy contrast thread, 3 mm gauge, on the
  placket, back yoke, collar, every patch-pocket edge, and the felled
  structural seams — the workwear look and the durability in one pass.
- **Buttons are hardware** — a Yantra4D cartridge (the `tack-button` /
  `shank-button` guide in this commons), referenced from the BOM, never
  re-implemented here.

## Run

```bash
python apps/api/services/engine/fc_runner.py projects/chore-coat/main.py coat.svg '{}' svg
```

Single pieces render on their own via `target_piece`, e.g.
`'{"target_piece": "patch_hip"}'` or `'{"target_piece": "collar"}'`.

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

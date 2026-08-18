# Lab Coat — FC-100 rank #88

The classic knee-length white lab coat ("bata de laboratorio") in
`materials/popelina-algodon` (115 gsm cotton poplin, 1450 mm width; a heavier
`materials/manta-cruda` is listed as the alternative): a relaxed single-breasted
coat (`body_length` 1050, `coat_ease` 220) cut to layer over street clothes,
with a modest notch lapel, a set-in sleeve, a center-back vent and half-belt
marking, and — the signature — three big patch pockets (two hip + one chest with
a **pen slot**).

It is the `overcoat` (rank #63) coat frame simplified to a workwear staple. The
center→lapel→gorge front break, the shaped CB seam with a vent + half-belt
marking, the upper collar solved to the gorge + back neck, and the straight
front facing verified against the measured front-edge run are the overcoat's
techniques; the modest **notch lapel** and the **one-piece eased set-in sleeve**
are the `blazer`'s (rank #30); the **three real patch pockets** are the
`chore-coat`'s (rank #65), from the `patch-pocket` enabler.

## Pieces (7)

| Piece | Cut | Role |
|-------|-----|------|
| `front` | 2, mirrored | one-piece button-stand front; center edge breaks at the roll point into a notch lapel + straight gorge; 5 buttonhole crosses, roll line, chest + hip pocket placements |
| `back` | 2, mirrored | gently shaped CB seam (allowance 15), CB vent markings, half-belt marking at the waist, full back armhole |
| `sleeve` | 2, mirrored | one-piece set-in sleeve; cap solved to the summed armholes + cap ease; elbow + cuff-tab markings |
| `collar` | 1, on fold at CB | convertible upper collar (half on fold); neck edge solved to the gorge + back neck |
| `facing` | 2, mirrored | straight front facing strip; long edge verified against center + lapel + gorge |
| `patch_chest` | 1 | breast patch pocket — chamfered pouch, hem-faced opening, topstitch guide, **pen slot** division |
| `patch_hip` | 2 | large hip patch pockets — the same pouch, one per side |

## Solves, all declared and verified

- **Sleeve cap** is bisected to the measured `front.armhole + back.armhole`
  plus a 16 mm set-in **cap ease** (carried as declared ease), delta ≈ 0.
- **Upper collar** neck edge is bisected to the measured `front.gorge +
  back.neck` (collar-band method), delta ≈ 0.
- **Front facing** `long_edge` is verified against the measured
  `front.center + front.lapel + front.gorge` run plus both end allowances
  (carried as declared ease), delta ≈ 0.
- **Shoulder** (`front.shoulder ↔ back.shoulder`) and **side**
  (`front.side ↔ back.side`) seams are straight matches; the **sleeve underarm**
  closes on itself (front underarm ↔ back underarm). Six seam relationships are
  checked in the full set.

The **patch pockets are topstitched appliqué**, not balance seams: each pocket
outline is its own closed piece, and the chest + hip **placements are internal
traces** on the front. That is why the pockets appear as pieces and as markings,
but never as a declared seam.

## Construction order (teaching-grade)

1. Fuse the front edges + lapels, the upper collar, and the facing; mark the
   CF buttonholes and the roll line.
2. Join the two backs at the CB seam (leave the vent open below the vent stop);
   press the vent, tack the half-belt strap at the marked line.
3. Join shoulders (front ↔ back), then the side seams; finish the edges.
4. Solve + assemble the upper collar (half on fold at CB); set it to the
   neckline, matching the gorge-seam notch.
5. Attach the front facing along the center + lapel + gorge edge; turn and press
   the lapel roll at the roll point.
6. Set the sleeves into the armholes (ease the cap over the shoulder), close the
   underarm seams, then hem the wrist (tack the optional cuff tab at its line).
7. Hem the coat.
8. Fold the pocket hem facings, then **topstitch the three patch pockets** to
   their marked placements along the topstitch guide (leave the tops open);
   topstitch the chest pocket's **pen slot** division so it holds pens upright.
9. Sew the buttons; work the buttonholes.

## v0 honesty notes

- **Notch lapel, kept small.** The center edge breaks at the roll point into a
  straight diagonal lapel out to the lapel point at chest level, then a straight
  gorge back to the neck point — the `blazer`'s notch, drawn modestly
  (`lapel_width` 72) for a coat that mostly hangs open. A curved gorge or a
  rolled notch is future work.
- **Convertible collar, one piece.** A single upper collar (default height
  60 mm) solved to the gorge + back neck and cut on fold at CB; a two-piece
  collar with a separate stand, or a true undercollar, is future work. The
  classic ~10 mm **collar/lapel notch gap** is a construction note, not drafted
  into the pieces.
- **Straight facing.** The front facing is a straight strip whose length is the
  measured front-edge run plus both seam allowances (width 100 mm), enough to
  carry the buttonholes and the lapel fold; a shaped facing that mirrors the
  lapel is future work.
- **One-piece set-in sleeve.** The cap is a true set-in cap solved to the summed
  armholes **plus 16 mm ease** (not a two-piece tailored sleeve, not a flat drop
  shoulder). The back underarm carries a gentle outward bow for elbow room; it
  adds well under 1 mm over the straight front underarm, inside the declared
  tolerance. The **cuff tab** is a marking only — a fabric wrist tab is future
  work.
- **Shaped CB seam + vent + half-belt.** The back is cut in two with a gently
  shaped CB seam (allowance 15), a **CB vent** (underlap 50 mm, clamped clear of
  the waist) so a seated wearer isn't bound, and a **half-belt** marking at
  waist level — all the overcoat's back detailing, kept as a marking in v0.
- **Patch pockets are single-layer.** Each is one chamfered pouch (45° bottom
  corners, the `patch-pocket` enabler shape) with a hem-faced opening and a
  topstitch attach guide. The **chest pocket carries a pen slot** — a vertical
  topstitch division near its right third that partitions the pouch so it holds
  pens upright, the detail every lab coat wearer knows. A lined pocket or a
  bellows pocket is future work.
- **Unlined.** The lab coat is drafted as a single-layer shell; a lining is not
  drafted in v0.
- **Buttons are hardware** — a Yantra4D cartridge (the `shank-button` guide in
  this commons), referenced from the BOM, never re-implemented here.

## Run

```bash
python apps/api/services/engine/fc_runner.py projects/lab-coat/main.py coat.svg '{}' svg
```

Single pieces render on their own via `target_piece`, e.g.
`'{"target_piece": "patch_chest"}'` or `'{"target_piece": "collar"}'`.

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

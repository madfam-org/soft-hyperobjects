# Blazer — FC-100 rank #30

Teaching-grade single-breasted blazer ("saco") in `materials/popelina-algodon` —
the commons' **first tailoring garment**. Five pieces: front (cut 2), back
(cut 2 with a shaped CB seam), one-piece sleeve, upper collar (half on fold),
and a straight front facing.

## The lapel, the roll line, and the notch

A blazer front has no plain neckline. The center edge climbs the 20 mm button
stand only as far as the **roll point** at waist level (`roll_line_y` 300 above
the hem) — the top buttonhole sits exactly there. Above it the front **breaks
open**: the **lapel** edge runs as a straight diagonal up-and-out to the lapel
point, 85 mm past CF at chest level, and the **gorge** edge runs back in to the
neck point at the shoulder. The **roll line** — marked as an internal from the
roll point to the neck point — is the crease the lapel folds back along in
wear: everything outside it shows its facing side, which is why the facing (not
the front) becomes the public face of the lapel.

In construction, the upper collar sews along the gorge and back neck, and the
collar's front edge meets the lapel's gorge edge at the **notch** — the classic
V-shaped gap between collar and lapel point. Convention holds that gap around
**10 mm**: the collar's corner is drafted stopping ~10 mm short of the lapel
point so the notch opens cleanly when pressed. In this v0 draft the notch is a
construction note, not drafted geometry — the solved collar neck consumes the
full gorge + back neck run and the gap is left to the maker's iron.

Three solves, all declared and verified: the **sleeve cap** is bisected to the
measured front + back armholes **plus 25 mm of declared cap ease** — the
commons' first eased cap, `declare_seam(..., ease=25.0, tol=2.5)` — because a
tailored cap is longer than its armhole on purpose and gets shrunk in with
steam; the **upper collar** neck edge is bisected to the measured
`front.gorge + back.neck` per half (overlap 0, the collar-band method); and the
**facing** length is derived from the measured `center + lapel + gorge` run
plus end allowances, verified with the allowances as declared seam ease.

## v0 simplifications (honesty notes)

- **No lining, no canvas.** The lining is not drafted in v0 (noted in
  metadata); chest canvas, shoulder pads, and sleeve heads are replaced by a
  fusible-interfacing note in the BOM. A construction guide is future work.
- **The gorge doubles as the front neckline.** A true tailored gorge is a
  short seam near the collarbone; here it spans lapel point to neck point in
  one straight edge, so it is longer than a bespoke gorge. The 10 mm notch
  gap (above) is likewise a note, not drafted.
- **Straight facing.** The facing is a straight strip of the measured
  front-edge length, width 90 — a shaped facing mirroring the lapel blade is
  future work. Wide lapels get a manifest warning for exactly this reason.
- **One-piece sleeve.** Elbow shaping is a gentle outward bow on the back
  underarm edge (it adds well under 1 mm over the straight front underarm,
  inside the declared tolerance); a true two-piece tailored sleeve is future
  work.
- **Flap pockets are markings.** One hip flap + attach line per front — cut 2
  mirror puts the pair in the garment; jetted-pocket construction pieces are
  future work.
- **CB vent is markings.** Two internal lines (underlap at 45 mm, stop at
  `vent_height` 180) on the shaped CB seam (allowance 15); the vent's cut
  extension is future work.
- **Fisheye dart.** The front waist dart is an internal diamond, intake 18,
  waist to chest — the kernel's dart-rotation pass is a roadmap item, so the
  dart is marked, not rotated.
- **Buttons are hardware** — a Yantra4D cartridge (`shank-button` guide in
  this commons), referenced from the BOM, never re-implemented here.

```bash
python apps/api/services/engine/fc_runner.py projects/blazer/main.py blazer.svg '{}' svg
```

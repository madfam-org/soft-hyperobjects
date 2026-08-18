# Trench Coat — FC-100 rank #60

Teaching-grade **double-breasted trench coat** ("gabardina") in
`materials/lana-melton-abrigo` — the commons' most detailed coat, built on the
**blazer** lapel-front architecture (rank #30), lengthened to a coat and widened
for layering. Nine pieces: front (cut 2, double-breasted), back body (cut 2,
shaped CB seam + deep vent), back storm-shield yoke (cut 2), one-piece set-in
sleeve, upper collar (half on fold), gun flap (cut 1, right front), belt (cut 2),
epaulette (cut 2), and a wide front facing.

Un trazo didáctico de **gabardina cruzada** en melton de lana, la prenda más
detallada del común, sobre la arquitectura de solapa del saco.

## The double-breasted front, the lapel, and the roll line

A trench front wraps deep. The center edge climbs a **wide button stand**
(`button_stand` 140, the double-breasted wrap) only as far as the **roll point**,
then the front **breaks open**: the **lapel** runs as a straight diagonal up-and-out
to the lapel point (110 past CF at chest level) and the **gorge** runs back in to
the neck point. Two **button columns** cross the chest — the buttoning column near
CF and a decorative/anchor column out toward the stand edge — the double-breasted
signature. The **roll line** (roll point → neck point) is marked as an internal:
it is the crease the lapel folds back along, which is why the wide facing, not the
front, becomes the public face of the lapel.

## The iconic trench details, as verified pieces

- **Storm-shield cape (back yoke).** A separate cape yoke (cut 2, with a CB cape
  seam) sits over the back and sheds rain off the shoulders. Its straight bottom
  edge sews to the back body top as a **functional yoke seam** (declared, delta 0).
  Its free lower edge is marked as a styling line.
- **Gun flap (storm flap).** The signature shaped panel on the **right front**
  upper chest, caught in the shoulder seam and hanging free over the chest. Its
  `attach` edge is solved to the measured **front shoulder length** so it sews
  into that seam with delta ≈ 0 — `declare_seam(("gun_flap","attach"),
  ("front","shoulder"))`. Cut 1 (right side only, as on a real trench).
- **Belt.** A real long strap (cut 2 + CB seam, folded lengthwise to the finished
  `belt_width`) with three eyelet cross-marks at the tail. The **D-ring buckle**
  and belt loops are hardware — a Yantra4D cartridge in the BOM, never
  re-implemented here.
- **Epaulettes.** Real pointed shoulder straps (cut 2 mirror, folded) with a
  button cross-mark; the button is Yantra4D hardware.
- **Deep back vent.** Two internal marking lines (underlap at 60, stop at
  `vent_height` 420) on the shaped CB seam (allowance 16).
- **Cuff strap.** Marked at the wrist on the sleeve; its slider/buckle is BOM.

## The solves — all declared and verified

- **Sleeve cap** bisected to the measured `front.armhole + back.armhole` **plus
  `cap_ease` 30** of declared ease (`ease=30, tol=2.5`) — a set-in coat cap is
  longer than its armhole on purpose and gets eased in with heavy steam.
- **Upper collar** neck edge bisected to the measured `front.gorge +
  back_yoke.neck` per half (overlap 0, the collar-band method).
- **Facing** length derived from the measured `center + lapel + gorge` run plus
  end allowances, verified with the allowances as declared seam ease; width 150 to
  cover the deep double-breasted stand.

## Fabric honesty note

A real trench is cut in **gabardine** — a tightly-woven, water-shedding cotton or
poly/cotton twill (Burberry's original cloth). The commons does not yet carry a
gabardine card, so this cartridge uses **`lana-melton-abrigo`** (wool melton
coating, 420 gsm), the FC-100's heaviest woven and its designated coat cloth. Melton
is warmer and bulkier than gabardine and does not shed rain the same way, so:
seam allowances are widened to **14 mm** and the hem to **55 mm** for its bulk
(the card's own guidance), the undercollar layer should be trimmed to reduce
collar/lapel bulk, and its fulled face barely frays so some edges may be bound
rather than turned. Swap in a gabardine card when the commons adds one.

## v0 simplifications (honesty notes)

- **No canvas; lining noted-not-drafted.** The full body + sleeve lining is a BOM
  line (cut from the shell fronts/back/sleeves less the facings), not drafted
  geometry in v0. Chest canvas and shoulder work are replaced by a fusible-
  interfacing note. A construction guide is future work.
- **Set-in sleeve.** One-piece, eased. A **raglan** sleeve is equally authentic
  for a trench (the classic soft shoulder) and is a good future variant; a true
  two-piece tailored sleeve is also future work. Elbow shaping is a gentle bow on
  the back underarm edge, under 1 mm over the straight front underarm, inside tol.
- **Storm-shield cape is a yoke seam.** On a real trench the cape often hangs as a
  free flap; here it is a functional yoke seam (its free edge marked) so the seam
  is verifiable. A free-hanging cape layer is future work.
- **Gun flap caught in the shoulder seam.** Modeled as attaching along the full
  front shoulder length; a real gun flap spans the outer chest and tacks at the
  lapel. Drafted as one straight attach edge for a clean, verified seam.
- **Belt and epaulettes are free straps** — they attach via buckle/buttons
  (hardware in the BOM), so they are not declared as sewn seams; their fold lines
  and eyelet/button marks are drawn.
- **Straight facing.** A straight strip of the measured front-edge run, width 150
  — a shaped facing mirroring the lapel blade is future work.
- **Pocket flaps and vent are markings.** Slanted hip flap + attach line per
  front, and the CB vent lines — jetting/welt and the vent's cut extension are
  future work.
- **Buttons, buckles, D-rings, sliders are hardware** — Yantra4D cartridges
  (`shank-button` guide in this commons), referenced from the BOM, never
  re-implemented here.

```bash
python apps/api/services/engine/fc_runner.py projects/trench-coat/main.py trench-coat.svg '{}' svg
```

Official visualizer and configurator: Fashion Cabinet.
Visualizador y configurador oficial: Fashion Cabinet.

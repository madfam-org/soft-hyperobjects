# Cargo Pants — FC-100 rank #37

The **chinos block relaxed for utility wear** (`projects/chinos`, trouser
block family): front/back legs (cut 2 each) with the front inseam bowed by
the same solved bisection to match the deeper back fork, equal side seams by
construction, and the grown-on fly extension with fly J-topstitch guide and
fly-stop notch carried over unchanged. What the relaxation and the cargo
hardware change:

- **Relaxed fit** — total hip ease 160 mm (chinos: 100) and a wide straight
  hem, half-width 130 mm (chinos: 105), back +12 as usual. No pressed
  creases: casual utility trouser.
- **Bellows cargo pockets as real pieces** (the wave's new element) — the
  pocket is cut flat as **one closed 8-edge hexagonal outline**: the
  180 × 200 mm main face plus a 30 mm fold wing on each side, the wings
  tapering away over the bottom corners so the bellows folds flat. The two
  vertical fold lines at the face/wing boundaries are internal markings; the
  mouth and wing tops carry the hem allowance for the fold-down mouth hem,
  and a center notch matches the flap. Cut 2.
- **Angled-corner flaps** — 180 × 70 mm with 25 mm clipped lower corners and
  a center pocket-match notch; the flap `attach` edge is verified against the
  pocket `mouth` edge as a declared seam. Cut 2.
- **Thigh placement** — each front leg carries a `pocket_width` ×
  `pocket_height` placement rectangle at mid-thigh (top edge ≈ 120 mm below
  the crotch line) locating the pocket main face.
- **Pocket-mouth notches on the side seams** — the diagonal slash-pocket
  opening is kept from the chinos, and both front and back side seams gain a
  matching "pocket mouth" notch 140 mm below the waist where the opening
  meets the seam.
- **Split waistband with crossover tab** (dress-trousers approach) — the band
  is cut as two halves: the tab half extends +60 mm into a crossover tab with
  a button cross-mark and a tab line; each half's bottom edge is verified
  against front + back waists with its own declared ease (tab: 60 mm + 2 ×
  seam allowance; plain: 2 × seam allowance).
- **Six belt loops** — one more than the chinos' five, for the heavier belt.

v0 simplifications: the slash-pocket bags, flap closure hardware, and the
bellows box-corner construction guide are future work; the pocket and flap
are drafted, but their topstitch order is not yet a technique card. The fly
zipper federates to a Yantra4D notion via the `fly` (zipper_tape) interface
rather than being drafted here. Fabrics: `materials/mezclilla-denim`
(primary) and `materials/popelina-algodon`.

```bash
python apps/api/services/engine/fc_runner.py projects/cargo-pants/main.py cargo-pants.svg '{}' svg
```

# Bib Overalls — FC-100 rank #49

Denim dungarees on the **side-seamed trouser block** (chinos / jumpsuit
lineage) with **no fly**. The four fabric-body pieces plus straps and a bib
pocket build the whole garment:

- **Front / Back leg** (cut 2 each) — side-seamed leg. The front inseam is
  bowed outward by a bisection-solved bulge so it measures exactly the deeper
  back fork; the side seams are equal by construction. The **front waist is
  flat** (it seams to the bib bottom); the **back waist rises** `back_rise −
  front_rise` at CB, and its inner x is solved analytically
  (`√(WAIST_B² − rise_diff²)`) so the slanted waist edge measures exactly the
  back waist quarter.
- **Bib** (cut 1 on the CF fold) — a shaped chest panel that fans from a
  narrower topstitched top out to the front waist. Its bottom half-width **is**
  the front waist quarter, so the bib↔front-waist seam closes with delta ≈ 0.
- **Back panel** (cut 1 on the CB fold) — the lower upper-back panel; its
  bottom half-width **is** the back waist quarter, so the back-panel↔back-waist
  seam closes with delta ≈ 0.
- **Strap** (cut 2) — straight adjustable strips; a ladder of drill crosses
  near the free end marks the slider/adjustment positions.
- **Bib pocket** (cut 1 on the CF fold) — a patch pocket with a divider
  topstitch on the chest.

## The signature seams

Both waist joins are **declared seams** driven from the SAME shared waist
formulas — `(waist + ease)/4 ∓ 12` for the front/back quarters — so each check
closes with delta ≈ 0 by construction (the jumpsuit waist-seam method):

- `bib.bottom ×2 ↔ front.waist ×2` (bib is cut on fold → its half sews in
  twice; two front legs → one waist each). Default: 496 mm = 496 mm.
- `back_panel.bottom ×2 ↔ back.waist ×2`. Default: 544 mm = 544 mm.

Plus the ordinary leg seams: `front.side ↔ back.side` and
`front.inseam ↔ back.inseam`, both delta ≈ 0.

## Hardware is a Yantra4D reference, never drafted here

Per the federation contract, every hard good is a **Yantra4D cartridge
reference in the BOM note text**, not kernel geometry:

- **Overall buckles + sliders** (one buckle + one slider per strap) — the
  strap-buckle interface; the bib "buckle catch" and the strap-end are the
  attach marks.
- **Jean tack buttons** — 2 bib buckle catches + 4 side hip placket buttons.
- **Tubular rivets** — placket ends, bib corners, pocket mouth.

The buckle catch on the bib, the strap-attach on the back panel, and the strap
holes are **drill-cross internals** only; the side hip openings are **marked
button plackets** (internals + BOM buttons).

## Teaching-grade simplifications (honest)

- Straps are straight rectangular strips (no taper, no separate buckle tab).
- The side hip opening is a **marked** placket line with button drill crosses,
  not a drafted placket underlay / facing.
- The bib and back panel are single self-faced pieces (no separate facing
  drafted); their top edges carry a hem allowance for the turn-and-topstitch.
- Topstitch traces (out-seams, bib edges, back-panel top, pocket) are sewing
  guides, not cut lines.

Fabric: `materials/mezclilla-denim` (12 oz, 1500 mm wide).

Official visualizer and configurator: Fashion Cabinet.

```bash
python apps/api/services/engine/fc_runner.py projects/bib-overalls/main.py bib-overalls.svg '{}' svg
```

# Varsity Jacket — FC-100 rank #66

**Varsity jacket** / **Chamarra varsity** — the classic baseball / letterman
jacket. The **bomber-jacket** (rank #29) architecture with two signature
changes: the front zipper becomes a **snap-button placket**, and the sleeves
are cut in a **contrast fabric** (the two-tone letterman look).

- **Body** (`felpa-algodon`): front **cut 2 mirrored** — never on fold — plus a
  back cut 1 on fold. Each front's center edge is the **snap stand**: it laps
  past center front by `placket_ext`, and `snap_count` (default **5**) snap
  fasteners run the CF line as drill cross-marks. Each front also carries a
  horizontal **welt hand-pocket** marking (150 mm opening + surround box) and a
  **chenille chest-patch** placement zone.
- **Sleeves** (`mezclilla-denim`, contrast): a long **set-in** sleeve whose cap
  is **solved by bisection** to the measured armhole pair (ease 0), seam-checked
  at tol 2.0. Cut in the second card so the BOM orders it separately.
- **Ribs** (`collar_rib`, `cuff_rib`, `hem_rib`): the negative-eased knit trim
  that defines the letterman silhouette. **Derived — no solver, no seam check:**
  each rib length = its opening × a ratio (they stretch to fit the larger
  opening, so delta is 0 by construction). The **waist rib is split** for the
  placket opening, with a center notch (= center back when worn) marking the gap.

## Honest simplifications (teaching-grade)

- **Set-in, not raglan.** The authentic letterman uses **raglan** sleeves. This
  draft uses a **set-in cap solved to the armhole pair** — the bomber's proven,
  robust solver — and declares the choice in `metadata.sleeve_attachment`.
- **Two-tone via two cards.** `felpa-algodon` body + `mezclilla-denim` sleeves
  stands in for the **classic wool-melton body + leather sleeves** (noted in the
  BOM and `metadata.two_tone_note`).
- **Snaps, welts and the chest patch are markings / notions, not geometry.** The
  snap positions are drill cross-marks; the welt pocket and chenille patch are
  placement markings (blazer-pocket convention). Snap **hardware** is a Yantra4D
  cartridge — the `shank-button` notion guide — referenced in the BOM, never
  re-implemented here.

## Pieces

| id | cut | fabric | notes |
|----|-----|--------|-------|
| `front` | 2, mirror | `felpa-algodon` | snap stand + welt + patch marks |
| `back` | 1 on fold | `felpa-algodon` | |
| `sleeve` | 2, mirror | `mezclilla-denim` | contrast; set-in cap solved to armholes |
| `collar_rib` | 1 | rib trim | band collar, derived (neck × `collar_ratio`) |
| `cuff_rib` | 2 | rib trim | derived (sleeve hem × `cuff_ratio`) |
| `hem_rib` | 1 | rib trim | split waistband, derived (hem × `hem_ratio`) |

## Construction order

1. Sew shoulder seams (front ↔ back), then side seams.
2. Close each contrast sleeve's underarm; set the cap into the armhole pair.
3. Apply the rib **collar** band to the neckline, **cuff** ribs to the sleeve
   hems, and the split **waist** rib to the front + back hems (ends open at the
   placket).
4. Finish the **snap placket**: fold/face the front stands, then install the
   `snap_count` ring-snap sets down center front (Yantra4D `shank-button` notion).
5. Apply the chenille chest patch at its marked zone; bag the welt hand pockets.

## Run it

```bash
python apps/api/services/engine/fc_runner.py projects/varsity-jacket/main.py varsity.svg '{}' svg
```

Official visualizer and configurator: **Fashion Cabinet** ·
Visualizador y configurador oficial: **Fashion Cabinet**.

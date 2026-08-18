# School Polo — FC-100 rank #95

**EN** · A children's uniform polo shirt: the polo-shirt block scaled to child
proportions (smaller girths, shorter body and sleeve — the kids-tee range) for a
neat, uniform-appropriate fit, in cotton pique/jersey with knit ease. It keeps
the two signatures of a polo — a short centre-front button **placket** and a
folded **rib collar** — and adds the classic school-polo cut: short set-in
sleeves with rib bands, side vents at the hem, and a slightly longer "tennis
tail" back for tuck-in coverage.

**ES** · Un polo de uniforme infantil: el bloque de polo escalado a proporciones
de niño (contornos y largos menores — el rango de la playera infantil) para un
ajuste pulcro de uniforme, en piqué/jersey de algodón con holgura de punto.
Conserva las dos señas del polo — una **tapeta** corta de botones al centro y un
**cuello de rib** doblado — y suma el corte clásico del polo escolar: mangas
cortas montadas con puños de rib, aberturas laterales en el bajo y una "cola de
tenis" trasera un poco más larga.

## What the cartridge does

1. **The rib collar is solved, not drawn.** `build_collar` makes a folded rib
   band whose stitched neck edge is knit **shorter** than the measured neck
   opening — `opening × collar_ratio` — so it stretches on like a real 1×1 rib
   collar (negative ease). A halves-on-both-sides seam check
   (`collar.neck` vs `front.neck + back.neck`) enforces the fit at render time,
   with the designed negative ease recorded so the length balances exactly
   instead of the tolerance being loosened.
2. **The placket is marked and faced.** Two vertical placement lines run from the
   CF neck point down `placket_length` (the CF-side line rides the fold, the
   second sits `placket_width` away), with `button_count` (2 or 3) buttonhole
   drill crosses evenly spaced down the box. A separate backing strip —
   `(placket_length + 25) × (2 × placket_width)`, cut 1, interfaced — faces the
   slash.
3. **The sleeve cap is solved** by bisection against the front + back armholes
   (a multi-edge seam), and the short sleeve is finished with a derived rib band
   (`sleeve hem × collar_ratio`, cut 2), or a plain hem when `cuff_height = 0`.
4. **Side vents + tennis tail.** The side seam sews only from the underarm down
   to the vent top (`vent_height` above the front hem); below it the front and
   back hems are **independent finished edges**, so the back can drop
   `back_tail_drop` lower than the front without unbalancing any seam.

## Pieces

| id | piece | cut |
|----|-------|-----|
| `front` | Front (placket marked) | 1 on fold |
| `back` | Back (dropped tennis-tail hem) | 1 on fold |
| `sleeve` | Short set-in sleeve | 2, mirrored |
| `collar` | Rib collar band (folded) | 1 |
| `placket_backing` | Placket facing strip (interfaced) | 1 |
| `cuff` | Sleeve rib band | 2 |

## Construction order

1. Face and finish the **placket** slash with the backing strip; work the
   buttonholes at the marked crosses; sew shoulders (`front.shoulder ↔
   back.shoulder`).
2. Fold and attach the **rib collar band** around the neck opening
   (`collar.neck ↔ front.neck + back.neck`), stretching the band to fit.
3. Set the **sleeves** flat into the armholes (`sleeve.cap ↔ front.armhole +
   back.armhole`), then close each underarm (`sleeve.underarm_front ↔
   sleeve.underarm_back`).
4. Close the **side seams** from the underarm to the vent top only
   (`front.side ↔ back.side`); finish the side **vents** and both hems as
   separate edges (back longer for the tennis tail).
5. Attach the **sleeve rib bands** (`cuff.bottom ↔ sleeve.hem`) or hem the
   sleeves; sew on the buttons.

## Honest simplifications (teaching-grade)

- **Child proportions are a single default block**, not a full graded size run.
  Girths, body/sleeve lengths, armhole depth and shoulder slope are set to a
  representative ~age 7–8 uniform and driven by the sliders; a production kids'
  range would grade each size and adjust the neck/shoulder curves per age, not
  just scale the numbers.
- **The rib collar is a straight folded band**, solved by a stretch ratio rather
  than a shaped stand-and-fall collar with a separate stand piece. This is the
  common knit-polo construction and teaches the negative-ease idea cleanly, but
  a tailored polo may use a knitted flat-collar-and-placket set with a shaped
  neckline.
- **Drop-shoulder set-in sleeve.** Front and back armholes are drawn equal (a
  relaxed knit convention), so the cap is symmetric; a fitted polo would notch
  the front armhole deeper than the back.
- **Buttons are a reference, not geometry.** The buttonhole crosses are marked
  and the buttons are a Yantra4D hardware cartridge reference in the BOM
  (`shank-button` / flat-button), never re-implemented here per the federation
  contract.
- **Straight-line vents.** The vents are plain finished openings, not
  self-faced or bar-tacked vent facings; add a facing in production.

Suggested fabric: [`materials/jersey-algodon`](../../../materials/jersey-algodon/material.json)
— cotton/elastane single jersey (180 gsm), stretch running around the body,
comfortable to ~10% negative ease.

```bash
python apps/api/services/engine/fc_runner.py projects/school-polo/main.py school-polo.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/school-polo/main.py school-polo.json '{"chest_girth": 820, "button_count": 3}' json
```

Official visualizer and configurator: **Fashion Cabinet**.

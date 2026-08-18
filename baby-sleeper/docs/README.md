# Baby sleeper (footed pajama) — FC-100 #94

**Mameluco con pies (pijama).** The classic zip-up footed baby pajama, drafted
as a parametric knit **one-piece**: bodice + long leg + **enclosed foot** in a
single closed outline per body half, with a **full-length front zipper**.

Each body half runs continuously — neck → shoulder → armhole → side → leg
outseam → **around the foot** → inseam → back to the crotch. The `front` is cut
**2** (split at the centre front so the zipper joins the two halves); the
`back` is cut **1 on fold** at the centre back. Front and back share the same
shoulder / armhole / side / outseam / inseam / foot geometry, so all of those
declared seams close with **delta ~ 0 by construction** — the only front/back
difference is the neck scoop and the centre edge (CF zip edge vs CB fold).

## The two signature features

- **Footies.** The leg does not hem; it rounds into a toe box (the `foot`
  edge), and a flat `sole` (cut 2) is seamed underneath. The sole is a lens of
  two curves each **solved by bisection** to equal the body `foot` edge, so the
  foot-attach seam `sole.attach_out + sole.attach_in == front.foot + back.foot`
  balances exactly. Turn `footed` off for open, cuffed ankles (the sole is
  dropped and the leg ends in a straight hemmed `cuff`).
- **Zipper.** A full-length **separating** front zipper runs the CF from the
  neck to the crotch, marked as an internal CF trace + a stop notch, with an
  optional `zip_guard` chin flap at the top. The hardware itself is a **Yantra4D
  zipper cartridge** referenced in the BOM (`notion.hardware_ref`), never
  re-modelled here. A production sleeper uses a 2-way tail that diverts down one
  inner leg to the ankle — see the honest note below.

Long **sleeves** (cut 2) have a shallow knit cap **solved** to the combined
front + back armholes, with an optional **fold-over mitten cuff** (a newborn
hand cover) marked as a fold line. The neck is finished with a rib **binding**
strip derived from the measured opening (a bound edge, not a length-checked
seam — like the tee's neckband).

## Pieces

| id | cut | what |
|----|-----|------|
| `front` | 2, mirror | bodice + leg + foot half; CF is the zip edge |
| `back` | 1 on fold (CB) | bodice + leg + foot half, on the fold |
| `sleeve` | 2, mirror | long sleeve, cap solved to the armholes |
| `sole` | 2, mirror | flat foot sole, solved to the foot edge |
| `neck_binding` | 1 | rib strip from the measured neck opening |

## Construction order

1. Set the **front zipper** into the two `front` CF edges (separating zip;
   optional chin flap behind the top).
2. Join `front.shoulder` ↔ `back.shoulder`, then `front.side` ↔ `back.side`.
3. Set each `sleeve` cap into the armholes (`sleeve.cap` ↔ `front.armhole` +
   `back.armhole`); close `sleeve.underarm_front` ↔ `sleeve.underarm_back`.
4. Close the legs: `front.outseam` ↔ `back.outseam` and `front.inseam` ↔
   `back.inseam`.
5. Seam a `sole` under each foot (`sole.attach_out` + `sole.attach_in` ↔
   `front.foot` + `back.foot`).
6. Bind the neck with the rib strip; finish the sleeve cuffs (fold the mitten
   back, or hem plain).

## Honest simplifications (teaching-grade)

- The **foot** is a flat toe box closed by a seamed sole — a real footed-pajama
  construction. A couture sleeper may shape a 3D last-fitted foot; that is a
  later derived view.
- The **2-way ankle-diverting zip** is represented as a CF neck-to-crotch zip
  plus a construction note (the BOM length is the CF run); the leg-diverting
  tail is not drafted as a separate opening.
- **Sleepwear safety:** infant sleepwear is regulated. This block is a knit,
  low-ease **snug fit** (one compliant path); the other is inherently
  flame-resistant fabric. Loose cotton sleepwear is non-compliant in many
  markets — see the BOM compliance note. This is guidance, not certification.

Parameter contract lives in `project.json` and the `main.py` docstring.

Official visualizer and configurator: Fashion Cabinet.

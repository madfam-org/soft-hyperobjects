# Jumpsuit — FC-100 #47

One-piece woven garment: a sleeveless bodice (a-line-dress lineage) joins a
side-seamed trouser (sweatpants lineage) at THE WAIST SEAM. Both sides of the
seam are driven by the same waist formulas — `(waist + ease)/4 ∓ 10` for the
front/back quarters — so the declared eight-reference check (fold-cut bodice
front hem counted twice, cut-2 bodice backs, pant fronts, and pant backs once
per panel) closes with delta ≈ 0 by construction.

Bodice: front on fold; back cut 2 with a 20 mm CB allowance for the invisible
zipper. The zipper is measured from the neck DOWN; at the default 450 mm it is
longer than the bodice CB, so it conceptually continues past the waist seam
into the pant back CB — the stop notch then lands on the pant back crotch
edge (clamped above the fork). Neck facing (`2×front.neck + 2×back.neck +
2sa`, cut 1) and armhole facings (`front.armhole + back.armhole + 2sa`,
cut 2) are derived from the measured openings.

Trouser: woven ease, fitted waist. The back waist rises `back_rise −
front_rise` at CB and its inner x is solved so the slanted edge measures
exactly the back waist quarter. The front inseam is bowed outward by a
bisection-solved bulge to match the deeper back fork; hems are open. A
1800×40 waist tie threads the tie channel marked just above the waist seam
on both bodice pieces. Parameter contract: `project.json` + the `main.py`
docstring.

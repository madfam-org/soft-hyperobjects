# Romper — FC-100 #48

Relaxed pull-on summer romper: a sleeveless blouson bodice (front AND back
cut 1 on fold — no zipper; the back closes with a U-shaped CB neck keyhole
marked internal plus a button cross) over an athletic-shorts block whose
back hem width is solved analytically so the straight inseams match exactly.
The two blocks meet at an elasticized waist seam: the bodice hems are cut
wider than the shorts waists on purpose, and the blouson surplus
(`4×bodice_hem − 2×(short_front.waist + short_back.waist)`) is declared as
seam ease computed from the same width formulas — delta 0 by construction.
An elastic channel is marked inside the bodice hem; the waist elastic is a
BOM line at `waist_girth × 0.95`. Neck and armhole facings are derived from
the measured openings. Parameter contract: `project.json` + the `main.py`
docstring.

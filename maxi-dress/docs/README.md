# Maxi Dress — FC-100 rank #24

Empire-line strappy maxi in woven fabric (poplin hint). The **bodice** is the
camisole lineage ending at the underbust: front/back cut on fold, bound top
edges with **zero seam allowance**, finished by one binding strip derived from
the measured openings × `binding_ratio` (default 0.92) + 2 seam allowances,
plus two 24 mm strap strips sewn into 8 mm spaghetti. The **skirt** is the
maxi-skirt lineage: rectangular gathered panels cut on the fold, half-width =
`(hip_girth + dress_ease) / 4 × gather_ratio`, length = `skirt_length`.

Both assemblies join at the **empire seam**, declared with computed ease: at
defaults the skirt waists (2 × 382.5 = 765 mm drafted) sew to the bodice hems
(2 × 240 = 480 mm) with a gathered surplus of **285 mm** — the surplus is
derived from the same width formulas the pieces use, so the seam check's delta
is 0 by construction (tol 2.5) and any drift in either lineage fails the
render. "Empire quarter" notches at the midpoint of every waist/hem edge
distribute the gathers; side seams are declared and length-checked on both
assemblies. A soft-elastic **channel** is marked internal on the skirt panels
14 mm below the seam line (topstitched seam allowance forms it; the BOM lists
the elastic). The draft clamps the skirt half-width to never be narrower than
the bodice, so the surplus is never negative.

```bash
python apps/api/services/engine/fc_runner.py projects/maxi-dress/main.py maxi-dress.svg '{}' svg
```

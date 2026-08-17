# Pleated Skirt — FC-100 #34

The commons' first **pleat-spreading** draft. Front and back are identical
rectangular panels cut 1 on fold, whose flat width is the finished waist
spread by a multiplier; knife pleats consume the surplus and press the
panel back down to the finished waist. All pleat markings are computed
internals, and the waistband seam check proves the intake arithmetic.

## Pleat math (per half-panel)

```
finished_quarter = (waist_girth + waist_ease) / 4
half_width       = finished_quarter × pleat_multiplier
pleat_count      = floor(half_width / (pleat_face × 3))       # ≥ 1
repeat           = half_width / pleat_count
intake           = (half_width − finished_quarter) / pleat_count
face             = repeat − intake                            # visible width
```

At the default multiplier 3.0 each pleat hides 2× its face ("fully
pleated"). Each repeat leads with the visible face and trails with the
intake strip; the **solid fold line** bisects the intake, so folding on it
lays the crease exactly on the **dashed placement line** and hides `intake`
mm. A 3-point arrow below the waist points the fold toward the center fold
— the mirrored halves press symmetrically about CF/CB. Defaults give 5
pleats per half-panel (20 around the skirt), face 35.75 mm, intake 71.5 mm.

## Waistband accounting

The straight cut-1 band is sized off the **finished (pleated-down) waist**,
never the spread panels:

```
band bottom = (waist_girth + waist_ease) + overlap + 2 × seam_allowance
ease        = 4 × (half_width − finished_quarter) − (overlap + 2 × seam_allowance)
```

The declared check sews the four unpleated waist edges (each on-fold panel
counts twice) onto the band bottom with that ease — total pleat intake
minus the band's overlap-and-allowance extras — so it closes with delta 0
by construction, and any drift between the spread and the band errors out.

## Construction notes

Side zipper in the front-left side seam (the on-fold panels leave no CF/CB
seam), closing at the zipper-stop notch on both side edges; the side seam
carries a 15 mm allowance for it. **Pressing guide:** baste each pleat
closed across the waist, press the full length through a damp cloth —
cotton poplin (popelina) sets a crisp crease — and let the panel cool flat
before moving it. Re-press after hemming; edge-stitching the top 60–80 mm
of each fold keeps pleats sharp in wear. Parameter contract: `project.json`
+ the `main.py` docstring.

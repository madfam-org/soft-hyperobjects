# Leggings — FC-100 rank #7

Side-seamless negative-ease leggings: one leg piece (side on the draft's
vertical center), diamond gusset, fold-over waistband derived from the
measured waist edge. The back fork is deeper than the front, so the front
inseam is **bowed outward by a solved amount** until both inseams measure
equal — enforced by a seam check at render time.

Known v0 simplification (documented, not hidden): the gusset is a fixed
diamond; curve-fitting it to the fork openings is a later refinement.

```bash
python apps/api/services/engine/fc_runner.py projects/leggings/main.py leggings.svg '{}' svg
```

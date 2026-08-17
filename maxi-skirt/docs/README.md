# Maxi Skirt — FC-100 rank #82

Gathered elastic-waist maxi in woven fabric (poplin hint). Front and back are
**rectangular gathered panels** cut once on the fold: half-panel width =
`(hip_girth + hip_ease) / 4 × gather_ratio`, length = `skirt_length`. A
"gather zone" internal line marks the waist run that gathers into the
fold-over elastic casing, which is **derived from the measured waist edges**
(the leggings waistband lineage): casing length = full ungathered skirt waist
+ end seam allowances, height = `2 × (elastic_width + seam_allowance)`. The
side seams are declared and length-checked at render time.

Known v0 simplification (documented, not hidden): panels are pure rectangles —
no sweep shaping, side flare, or shaped hem; A-line and flared skirts belong
to the skirt-block lineage, not this draft.

```bash
python apps/api/services/engine/fc_runner.py projects/maxi-skirt/main.py maxi-skirt.svg '{}' svg
```

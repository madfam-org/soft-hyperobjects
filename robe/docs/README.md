# Robe — FC-100 rank #42

Shawl-front lounge robe ("bata"): back on fold, two wrap fronts, wide sleeves
with the cap solved to the front+back armholes (rank #6 numeric method, cap
ease 0), a self belt with loops, and patch pockets. Suggested fabrics:
`materials/felpa-algodon` (plush) or `materials/manta-cruda` (light summer).

**v0 honesty note:** the FC-100 index lists `shawl_collar` among this
garment's needs. This draft simplifies the shawl collar to a plain hemmed
wrap edge — a straight diagonal from the hem-side center front up to the
shoulder-neck point, replacing the front neck curve entirely. A true rolled
shawl collar (grown-on or a separate band piece) is future work; the belt is
sized from chest girth as a waist proxy.

```bash
python apps/api/services/engine/fc_runner.py projects/robe/main.py robe.svg '{}' svg
```

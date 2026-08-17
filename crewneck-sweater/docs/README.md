# Crewneck Sweater — FC-100 rank #38

The knitwear family's **cut-and-sew** entry: the sweatshirt (rank #6)
architecture redrawn for sweater knit. Deltas from the fleece block:

- **Slimmer**: 100 mm total ease (fleece runs 140).
- **Higher armhole**: AH factor +85 instead of +105 — set-in feel.
- **Long sleeve** (600 mm to cuff seam) into a **deep 70 mm cuff rib**;
  30 mm neckband, 50 mm hem band.
- **Hungrier rib ratios** — neck 0.80, cuff 0.72, hem 0.88 — because sweater
  knits stretch (and grow) more than fleece.
- **Taped shoulders**: each body piece carries a "tape shoulder seam"
  internal marking 6 mm inside the shoulder stitch line. Sew clear elastic
  or twill tape into the seam on that guide; knit shoulders grow otherwise.

Honest scope note: the FC-100 index lists `knitout_or_cut_and_sew` for this
slot. This cartridge is the cut-and-sew branch; a fully-fashioned
machine-knit (Knitout) version is future work. Fabric card gap: a dedicated
sweater-knit card is pending — `materials/felpa-algodon` stands in for the
body; use 1x1 sweater rib for the bands.

```bash
python apps/api/services/engine/fc_runner.py projects/crewneck-sweater/main.py sweater.svg '{}' svg
```

# Cardigan — FC-100 rank #39

The knitwear family's **button-front** entry: the crewneck sweater (rank
#38) block opened down the center front. Deltas from the crewneck:

- **Front cut 2 mirrored** (never on fold): the straight center edge is
  the band seam. Ease sits at 140 mm total — a cardigan layers over other
  garments.
- **Button band, cut 2**: length = the **measured** front center edge
  + 2 × seam allowance, width 2 × 28 mm (folded double to a 28 mm finished
  band). The relationship is a declared seam with `ease = 2 × seam
  allowance`, so a mis-sized band fails verification instead of rippling.
- **Five buttonhole crosses** marked on the band face — **mark both
  bands, work buttonholes on one**, sew shank buttons through the crosses
  on the other. Button hardware federates to the `shank-button` notion
  cartridge (Yantra4D solid); it is never redrawn here.
- **V-ish front neck**: 160 mm drop with a gentle near-chord curve that
  meets the band top; shallow 20 mm scooped back neck.
- **Long sleeve** (600 mm to cuff seam) with the crewneck's bisection-
  solved cap, into a **65 mm cuff rib** at ratio 0.72.
- **Split hem band** (cut 1, ratio 0.88, 50 mm): cut flat with a
  center-back notch; its open ends meet the button bands at center front.
- **Taped shoulders**: front and back carry the "tape shoulder seam"
  marking 6 mm inside the shoulder stitch line — knits grow, taped
  shoulders do not.

Honest scope note: the FC-100 index lists `knitout_or_cut_and_sew` +
`button_placket` for this slot. This cartridge is the cut-and-sew branch;
a fully-fashioned machine-knit (Knitout) version is future work. Fabric
card gap: `materials/felpa-algodon` stands in for the body; use 1x1
sweater rib for the cuffs and hem band, self fabric for the bands.

```bash
python apps/api/services/engine/fc_runner.py projects/cardigan/main.py cardigan.svg '{}' svg
```

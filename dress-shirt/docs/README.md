# Dress Shirt — FC-100 rank #4

Woven yoke-split dress shirt ("camisa de vestir") in `materials/popelina-algodon`:
button-stand fronts (cut 2) with seven buttonhole cross-marks on the CF line,
a back cut on fold whose top edge ends at the yoke seam, a yoke on fold that
carries the back neck and both shoulder edges, a long sleeve with placket slit
marking and rectangular cuff, and a two-piece collar.

This is the commons' first **chained multi-solve**: the sleeve cap is bisected
to the measured front + back armholes, the collar **stand** neck edge is
bisected to the measured half neckline (front + yoke) plus a 15 mm button
overlap (the collar-band enabler's method), and the collar **fall** neck edge
is then bisected to the stand's *measured top edge* — a solve chained off the
result of another solve. All seven seam relationships are declared and
verified, the stand↔neckline check carrying the overlap as declared ease.

**v0 honesty notes:**

- **Yoke doubling** — the yoke is drafted `cut 1 on fold`; construction uses it
  doubled (outer + burrito inner). Cut it twice in fabric, or once in self and
  once in lining.
- **Back armhole** — real shirts split the back armhole across back + yoke.
  Here the FULL back armhole is drafted on the back piece and the yoke keeps
  straight side edges clear of the armhole, so the cap ↔ armhole check stays a
  two-piece sum. The yoke seam sits at `yoke_drop` (default 100 mm) below HPS.
- **Sleeve placket** — simplified to a slit marking with a drill stop; a true
  tower placket (with its own binding pieces) is future work.
- **Hem** — straight in v0; the curved shirt-tail hem is future work.
- **Cuff** — length = `wrist_opening × 0.9 + 25 mm overlap + 2 × seam
  allowance`, drafted at double height and folded; sleeve wrist carries 1.15×
  fullness pleated into the cuff. The collar-stand button is in the BOM but
  not marked on the stand piece.
- **Buttons** are hardware — a Yantra4D cartridge (`shank-button` guide in
  this commons), referenced from the BOM, never re-implemented here.

```bash
python apps/api/services/engine/fc_runner.py projects/dress-shirt/main.py shirt.svg '{}' svg
```

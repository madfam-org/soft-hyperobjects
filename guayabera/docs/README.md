# Guayabera — FC-100 rank #96

The **guayabera** (also *guayabera cubana* / *camisa de Yucatán*) is a Latin
American and Mexican men's dress shirt of real cultural significance: a
formal-casual garment worn **untucked**, cool in tropical heat, and worn with
pride at everything from a workday to a wedding across Mexico, Cuba, and the
wider Caribbean. This cartridge drafts it from standard industry practice with
respect for that lineage, keeping the three details that make a guayabera a
guayabera — the **alforzas**, the **four pockets**, and the **vented, untucked
hem** — and adding a proper two-piece turndown collar.

A woven-tops sibling of the dress shirt (rank #4) and the camp-collar shirt
(rank #77): the same drop-shoulder block and button placket, the dress shirt's
chained collar solve, but decorated the guayabera way. Pieces: front (cut 2),
back (cut 1 on fold), sleeve (cut 2, short or long), collar stand (cut 2 on
fold), collar fall (cut 2 on fold), chest pocket (cut 2), hip pocket (cut 2),
and a side-vent tab (cut 2) — **four patch pockets in all**. What this cartridge
encodes:

1. **Alforzas — the signature (the heart of the garment).** The *alforzas* are
   the columns of fine vertical **pintucks** that decorate a guayabera. They are
   modelled as `fc.Internal(kind="trace")` vertical lines driven by
   `pintuck_rows` (3–5 traditional, 5 default): **two columns on each front**
   flanking the pocket stack, **three columns down the back**, and a matching
   column on **each pocket**. A twin needle or pintuck foot forms them on the
   real cloth; the trace lines are the stitching guide.
2. **Four patch pockets, each with its own alforza and button.** The classic
   guayabera carries four pockets — two chest + two lower/hip. They are drafted
   as **real cut pieces**: a chest pocket (120 × 130 mm, cut 2) and a larger hip
   pocket (165 × 175 mm, cut 2). Each has a shallow angled bottom point, a
   top-facing fold line, its own centred alforza column, and a button mark. Their
   placements are also traced on the front so the alforza columns flank them.
3. **Button placket + proper turndown collar.** The front's center edge is
   extended `button_stand` (32 mm) past CF as a folded placket carrying **seven**
   buttonhole cross-marks on the CF line — the guayabera buttons to the throat.
   The collar is a **two-piece turndown**: the **stand** has its neck edge
   bisected until it equals the half neckline + the 15 mm button overlap
   (collar-band method); the **fall** is then bisected to the *stand's own
   measured top edge* — the chained multi-solve inherited from the dress shirt.
   `stand.neck == front.neck + back.neck` closes at delta ≈ 0.1 mm (ease = the
   overlap); `fall.neck == stand.top` closes at delta ≈ 0.
4. **Worn untucked: straight hem, side vents, longer back.** A straight hem with
   a **side vent** (`vent_height`, 120 mm) marked on both side seams, each topped
   by a small **button tab** drafted as its own cut piece — the classic guayabera
   side slit. The back hem is shaped **`back_drop` longer** at center-back (a
   gentle shirt-tail dip) while the side-seam point stays level with the front,
   so the side seam still closes at delta 0.
5. **Set-flat sleeve, short or long.** The `sleeve` select drives a short
   (turn-up-friendly) or long sleeve; the cap is solved by bisection to the
   front + back armholes at zero ease (drop-shoulder wovens sew flat), reusing
   the dress-shirt / camp-shirt solver.

### Honest simplifications (teaching-grade)

- The **alforzas and side vents are placement traces / markings**, not consumed
  tuck fabric. Real pintucks eat width — roughly 2× the tuck depth per tuck — so
  a cutter should add that width back before cutting; the BOM note flags ~5–8%
  extra fabric for the take-up. The trace lines mark *where* the tucks go, on the
  finished (post-tuck) panel.
- The **full back armhole is kept equal to the front** on this drop-shoulder
  block. Finely tailored guayaberas split a smaller back armhole across a yoke;
  the equal-armhole block is the teaching form here.
- The **longer back is a shaped hem step**, not a separate curved shirttail
  pattern; the front hem is straight (v0).
- The collar is a **standard turndown** (stand + fall). Some guayaberas instead
  use a camp/Cuban collar — see the camp-collar-shirt cartridge (rank #77) for
  that variant.
- Buttons are **hardware**: the front, pocket, vent-tab, and collar buttons
  federate to the Yantra4D button family (shank-button cartridge) via the BOM
  note, and are never re-implemented in this kernel.

Suggested fabrics:
[`materials/popelina-algodon`](../../../materials/popelina-algodon/material.json)
(crisp cotton poplin — the woven-tops default, which names guayaberas
explicitly) or
[`materials/manta-cruda`](../../../materials/manta-cruda/material.json)
(unbleached cotton muslin, a linen-look guayabera).

```bash
python apps/api/services/engine/fc_runner.py projects/guayabera/main.py shirt.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/guayabera/main.py shirt.json \
  '{"chest_girth": 1400, "sleeve": "short", "pintuck_rows": 7}' json
```

Official visualizer and configurator: **Fashion Cabinet**.

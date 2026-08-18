# Kids' T-shirt — FC-100 rank #93 · Playera infantil

A children's crew tee, drafted as a scaled-down knit block: **front and back
cut on fold**, a **set-in sleeve** whose cap length is *solved* to the front +
back armholes, and a **bound rib neckline** whose strip length is *derived* from
the measured neck opening. It is the adult [`t-shirt-crew`](../../t-shirt-crew/)
block at child proportions, plus one kids-wear feature.

Una playera infantil trazada como bloque de punto a escala reducida: delantero
y trasero al doblez, manga montada con copa resuelta a las sisas, y cuello de
rib con vivo derivado de la abertura del escote. Es el bloque adulto
`t-shirt-crew` a proporciones de niño, más una característica de ropa infantil.

## The child-specific feature: the envelope (lap-shoulder) neckline

The `neckline` switch chooses:

- **envelope** (default) — the classic children's-wear opening. The neck is cut
  **wider**, and the front and back shoulders each carry a lapped **overlap** so
  they cross at the shoulders. The wide, overlapping neck **stretches over a
  child's head with no closure** (an optional light snap per shoulder keeps the
  lap flat). The overlap zone is marked on both panels.
- **crew** — a plain snug bound crew neck, exactly like the grown-up tee.

Envelope is the default because it is what makes a small tee actually go on a
wriggling toddler; older kids (the `8–10 (youth)` preset) can take the plain crew.

## Two things this cartridge encodes as rules, not numbers

1. **The sleeve cap is solved, not drawn.** `build_sleeve` bisects the
   half-biceps width until the cap curve's measured length equals the front +
   back armhole sum (a multi-edge seam check enforces it at render time). Change
   any body measurement and the sleeve re-solves — small/zero ease, as knits want.
2. **The neck binding is derived.** Strip length = measured neck opening ×
   rib ratio (default 0.88) + joins. The relaxed-shorter strip is stretched onto
   the opening; that negative stretch is carried as the seam's `ease`, so the
   declared seam still balances to delta ≈ 0.

## Pieces

| id | piece | cut |
|----|-------|-----|
| `front` | Front | 1 on fold (center), mirror |
| `back` | Back | 1 on fold (center), mirror |
| `sleeve` | Sleeve | cut 2, mirror (set-in) |
| `neckband` | Neck binding (rib) | cut 1, folded lengthwise |

## Construction order

1. Sew the **shoulder** seams — a plain seam for crew, or lap the marked
   **overlap** (front over back) and topstitch for envelope.
2. Set in each **sleeve**: match the cap notch to the shoulder, ease the cap
   into the front + back **armhole**, stitch.
3. Close the **underarm + side** in one pass (sleeve underarm → body side).
4. Apply the **neck binding**: join the rib strip into a loop, fold lengthwise,
   quarter it, and stretch it evenly around the neckline (0 mm seam allowance —
   the strip length already includes the joins).
5. Hem the **body** and **sleeves**.

All seams are declared and verified (`declare_seam`), so every match balances to
delta ≈ 0: shoulder f↔b, side f↔b, sleeve cap ↔ front+back armhole, sleeve
underarm f↔b, and neck-binding ↔ full neckline.

## Honest simplifications (teaching-grade)

- The rib **binding is a straight strip**; production ribbing is cut narrower and
  eased by the ratio. Bound edges use **0 seam allowance**.
- The envelope lap is drawn as **equal-length front/back shoulders with a marked
  overlap zone**, not a graded stepped placket — enough to cut and lap correctly,
  short of a full stepped-shoulder draft.
- Suggested fabric:
  [`materials/jersey-algodon`](../../../materials/jersey-algodon/material.json)
  (cotton/elastane single knit; weft stretch ~40%). Cut with the stretch running
  **around the body** so the neck opens over the head.
- **No hardware.** The optional shoulder snap is a **Yantra4D** cartridge
  reference (`notion.hardware_ref: snap-fastener`), never re-implemented here —
  this cartridge marks only the overlap.

```bash
python apps/api/services/engine/fc_runner.py projects/kids-t-shirt/main.py tee.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/kids-t-shirt/main.py tee.json '{"neckline": "crew", "chest_girth": 720}' json
```

Official visualizer and configurator: Fashion Cabinet ·
Visualizador y configurador oficial: Fashion Cabinet

# Gho wrap robe

The national dress of Bhutanese men (**གོ་**, *gho*): a knee-length wrapped robe, put on long,
crossed right-over-left, and then **hitched up** and belted at the waist with the woven **kera**
so the hem sits at the knee and the excess blouses over the belt to form the gho's front pouch.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Bhutanese).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A draft that takes the wearer's height and knee height, cuts the robe long, and reports the
> pouch that forms over the belt — because the gho's whole silhouette comes from how it is
> worn, not from its cut.

## Provenance

The **gho** is the national dress of men in Bhutan, worn daily and required in **dzong**
(fortress-monasteries), government offices and on formal occasions, where it is paired with the
ceremonial **kabney** scarf. It is a wrapped robe made **long**, crossed right-over-left, then
pulled up and belted with the woven **kera** so that its hem sits at the knee and the pulled-up
excess blouses over the belt into a large front pouch — the gho's traditional "pocket". It has
wide, deep sleeves finished with white folded-back cuffs (the **liṅgto**), and its finest cloth
is hand-woven **kushuthara** (supplementary-weft brocade) or checked **mathra**.

This cartridge drafts the gho as an original construction draft, and draws no weave.

## Why it earns its rank

**It is cut long and worn hitched.** The gho is made to the full ankle length and worn pulled
up to the knee — and the difference is the whole silhouette. The draft takes the wearer's
height and the floor-to-knee height, solves the worn length, and reports the **pouch blouse**
that forms over the belt:

```python
WORN_LENGTH  = (wearer_height - 260) - knee_height   # nape to knee, the hem as worn
POUCH_BLOUSE = cut_length - WORN_LENGTH              # the excess that forms the front pouch
```

At the defaults that is a worn length of **960 mm** and a pouch blouse of **220 mm**. Draft the
robe to the worn length instead and there is no pouch — which would be the wrong garment.

**The front crosses deep.** Each front is drafted with a real overlap (`front_overlap = 260 mm`
at the defaults) so the two fronts meet with a genuine cross, held by the belt. The low neckband
is cut to the **measured** neckline (`collar_run_mm ≈ 1000`). There is **no button or hook** —
the **kera** belt is the only closure.

## What is deliberately out of scope

No specific **kushuthara** or **mathra** weave, and no dzong or dratshang dress code, is drawn.
The cloth is the weaver's — Bhutanese hand-weaving is among the world's finest — and the wearing
is the wearer's.

## Parameters

`chest_girth`, `wearer_height`, `knee_height`, `cut_length`, `neck_girth`, `shoulder_width`,
`sleeve_reach`, `sleeve_depth`, `cuff_fold`, `front_overlap`, `collar_height`, `ease`,
`seam_allowance`, `hem_allowance`.

## Pieces

- **front** — one front (cut 2), with the deep centre-front overlap.
- **back** — the back, cut on the CB fold, one-piece wide sleeve.
- **sleeve** — the folded-back white cuff (liṅgto), cut 2.
- **collar** — the low neckband, cut to the measured neckline.

## Fabric

Bhutanese checked or striped cloth (mathra), or hand-woven kushuthara for formal wear; the white
liṅgto cuffs in plain white cloth. Closed entirely by the kera belt.

## The 500th garment

This is the **500th ratified garment of the Fashion Cabinet** — the last of the first half of
one thousand. It was drafted on **2026-08-26**, in the same plain, working way as the first:
a real pattern for a real garment, tested at its limits, with the weaving left to the weaver and
the wearing left to the wearer. There is nothing ceremonial about the draft itself, which is
the point — the commons is built one honest, cuttable pattern at a time, and this is one more.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living national dress of Bhutan; the kushuthara and mathra weaves
are the weavers'.

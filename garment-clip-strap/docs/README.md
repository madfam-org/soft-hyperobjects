# Clip-strap Garment Carrier

The over-the-shoulder carrier that **grips a stack of hangers**: a padded webbing strap runs
over the shoulder, a folded cradle at the working end holds the printed clip that bites the
hanger hooks, and a keeper loop tames the tail.

Part of the **Fashion Cabinet Commons** (FC-400, rank #367 — care & keeping).
**Yantra4D-bridged** (`garment-clip`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Carrying a wardrobe by the armful is how hangers tangle and shoulders end up on the floor;
the shop answer is a branded carry hook. This holds a printed clip on a strap cut from
webbing offcuts, so a whole rail moves in one trip and the hardware is printable, not bought.

## Pieces

`strap` (the shoulder webbing panel, cut 1) + `cradle` (the folded clip pocket, cut 1) +
`keeper` (the tail-taming loop, cut 1).

## The seam that solves

The cradle wraps the clip along its **length**: `2·jaw_len + wrap`, so the folded pocket is
one jaw-length deep and can never be cut short of the clip. Its width equals the strap width
— the cradle is cut from the **same webbing** and sews to the strap's clip end by
construction. All three pieces derive their clip-facing dimensions from the clip's own
`jaw_len`/`jaw_w`, the same parameters that drive the bridged solid, so the pocket and the
hardware are always cut to one measurement.

## Construction notes

Box-X stitch every load-bearing join; this carries a full wardrobe. Fold a foam pad under the
shoulder crest before topstitching. Fold the cradle around the clip and box-stitch the mouth
closed with the clip's spring free to open.

## Cross-commons bridge

Yantra4D **`garment-clip`** (`notion.hardware_ref`): its `jaw_len` and `jaw_w` are driven by
this carrier's `clip_jaw_len` and `clip_jaw_width`. The clip arrived on the yantra4d 500-push
shelf; the FC-400 index logs it `(co-create)`, and this cartridge links it live.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

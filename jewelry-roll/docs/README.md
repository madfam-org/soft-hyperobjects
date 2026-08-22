# Jewelry Roll

The travelling **jewelry roll**: a padded rectangle that lies flat, carries a band of
compartments across its lining, then rolls up on itself and cinches with a webbing tie
through a Yantra4D [`d-ring`](https://app.yantra4d.com). Chains do not tangle because each
one gets its own pocket and the curl of the roll keeps them under tension.

Part of the **Fashion Cabinet Commons** (FC-300, rank #256 — care & keeping). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Fine chains are usually stored in the blister packaging they arrived in, then thrown away
tangled and kinked. A padded roll cut to size gives jewelry that already exists a
repairable, launderable home, in cotton rather than the flocked polystyrene trays that
cannot be cleaned — and the tie hardware is a part you print rather than a roll you
replace.

## Pieces

`shell` (outer face, cut 1 — longer, by the measured spiral allowance) + `lining` (inner
face carrying the pockets, cut 1) + `pocket` (compartment band across the lining, cut 1) +
`tie` (webbing cinch strap through the D-ring, cut 1).

## The seam that solves

A roll is a **spiral, not a cylinder** — each wrap sits one fabric-thickness further out
than the last. The outer shell must therefore be **longer** than the lining by the
spiral's accumulated circumference difference, or the finished roll cups and the edges
will not align. This cartridge computes that difference by walking an Archimedean spiral
numerically and **measuring** it, then cuts `shell` that much longer than `lining` and
declares the seam with the difference as its declared `ease` rather than absorbing it
silently.

## Construction notes

Quilt the batting to the lining before attaching the pocket band, so the compartment
stitching also anchors the loft. Divide the band into compartments **after** it is sewn
down at the sides — dividing it flat produces pockets that are too tight once the padding
takes up depth. Roll the finished piece and mark the tie position from the real roll, not
from the flat pattern; `batting_thickness` predicts the diameter but the maker's own
padding is the truth.

## Cross-commons bridge

`notion.hardware_ref` → `d-ring`, mapping `webbing → tie_width`,
`wire_t → batting_thickness * 0.6`, and `bow_depth → tie_width * 0.8`. **Dimensional**:
the ring's sewn `bar_edge` flange is driven by `webbing` and `wire_t`, and both
`tie_width` and `batting_thickness` drive this roll's own `tie_anchor` interface — so the
same dimensions flow to the garment's sewn edge and the hardware's.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

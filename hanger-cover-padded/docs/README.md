# Padded Hanger Cover

A quilted slip-on cover that **pads a bare hanger** so a knit or silk blouse hangs without
shoulder dents. Two mirrored shell halves close around the shoulder; a gathered cuff grips
the hook shaft.

Part of the **Fashion Cabinet Commons** (FC-400, rank #364 — care & keeping).
**Yantra4D-bridged** (`garment-hanger`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Where the FC-300 padded cover (#257) stayed pattern-only against an imagined hanger, this
one is drafted to a **known** printed hanger body: the shell's inner arc matches the
Yantra4D `garment-hanger` shoulder, so cover and hanger are cut to the same sweep instead
of hoping a shop hanger happens to fit.

## Pieces

`shell` (one padded half, cut 2 mirrored) + `cuff` (gathered hook-shaft tube, cut 1).

## The seam that solves

A hanger shoulder is an **arc**. The shell's inner edge (against the bar) and outer edge
(the padded face) are two **concentric arcs sharing one centre** — a true uniform offset of
`pad_girth`, not two arcs pinched together at a shared crown (which collapses to a zero-area
lens on a shallow drop). The sagitta relation `R = (c²+s²)/2s` solves the shoulder radius
from span and drop; the drop is clamped under `0.85·half-span` so the arcs can never invert.
Both arcs are polygonised and **measured**; the outer-to-inner excess is declared as the
seam's ease, half taken by a crown dart.

## Construction notes

Quilt the shell before cutting if you are not using pre-wadded cloth. Sew the two shells
along the outer arc, turn over the hanger, and hand-slip the inner arc closed. Gather the
cuff loosely enough to slide the cover off for washing.

## Cross-commons bridge

Yantra4D **`garment-hanger`** (`notion.hardware_ref`): its `shoulder_w` and `slope` are
driven by this cover's `hanger_span` and `shoulder_drop`. The hanger body arrived on the
yantra4d 500-push shelf; the FC-400 index logs it `(co-create)` from the pinned-snapshot
state, and this cartridge links it live now that it resolves.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

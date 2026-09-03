# Shaped Shoe-Tree Fabric Stuffer

A stuffable fabric shoe tree: a **foot-shaped sack** that fills with cedar shavings, rolled
paper, or silica beads and holds a shoe's toe box open so it does not crease flat in storage.

Part of the **Fashion Cabinet Commons** (FC-400, rank #365 — care & keeping).
**Pattern-only** — no hardware bridge. Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

A crushed toe box is why good shoes look old before they wear out, and the shop answer is a
cedar tree per pair. This sews a stuffable form from drill offcuts and fills it with whatever
deodorises or dries — cedar, paper, silica — keeping a rack of shoes in shape for the cost
of scraps. It deepens the thin `care_keeping` family.

## Pieces

`upper` (the wrap over the foot form, cut 1) + `sole` (the asymmetric oval base, cut 1) +
`heel` (the drawstring casing that cinches the fill, cut 1).

## The seam that solves

The sole is a **foot outline** — wider at the ball than the heel — drafted as a smoothed,
**measured** polyline (a ball cap and a heel cap joined by two tangent straights). The
upper's `sole_edge` is cut to that measured perimeter, so the base seam closes on one number
regardless of shoe size. The upper wraps into a cone whose two ends (`back_seam` and
`heel_edge`) are plain verticals of equal height, so the wrap seams cleanly and all the foot
shape comes from the sole.

## Construction notes

Sew the upper into a tube, then set the oval sole matching the ball and heel notches. Turn,
stuff firmly through the heel opening, and cinch the drawstring casing. A firm cotton drill
holds the toe shape; a soft muslin sags once filled.

## Cross-commons bridge

**None.** `shoe-tree` *does* resolve in the pinned Yantra4D snapshot
(`docs/interfaces/yantra4d-hardware.snapshot.json`), but this cartridge still declares no
`notion.hardware_ref`, and that is the honest state rather than a gap: the stuffer is a
fabric *substitute* for a shoe tree, not a consumer of one. It is drafted from its own
foot measurements, so there is no dimensional handshake to make. The FC-400 index agrees —
entry 365 carries `hardware: null` and `needs: ["pattern"]`, with no `(co-create)` note.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

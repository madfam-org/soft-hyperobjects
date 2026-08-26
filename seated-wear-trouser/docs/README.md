# Seated-wear Rise-adjusted Trouser

A trouser cut for a body that **sits**: the back rise is drafted genuinely taller than a
standing trouser and the front rise lower, so the waistband stays level when seated instead of
gaping at the back and cutting at the front.

Part of the **Fashion Cabinet Commons** (FC-400, rank #372 — adaptive).
**Yantra4D-bridged** (`hook-loop-tape`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

A standing-drafted trouser worn seated gaps at the back and cuts at the front — the single
most common fit complaint for wheelchair users, and the reason many buy a size too large and
belt it. This takes the rise difference into the pattern, drops the back pockets that press
into a seat, and puts the whole waist on hook-and-loop so it fastens one-handed. The aid is in
the geometry, not just the label.

## Pieces

`front` (cut 2 mirrored, low front rise) + `back` (cut 2 mirrored, raised rise + fuller seat)
+ `waistband` (the hook-loop side-adjust band, cut 1).

## The seam that solves

The front and back **side seams must be equal length** even though the rises differ, or the
leg twists. Both panels share one `SIDE_LEN` and one shared crotch point, so the side and
inseam seams match by construction; the rise difference is taken entirely at the centre seams
(front lower, back higher) and the fuller seat at the centre-back curve. The extra back rise
is **clamped under 35% of the leg-below-waist** so the back waistline can never invert above
the hem. The waistband length is the **measured** sum of the four diagonal waist edges plus the
hook-loop overlap, so it can never come up short of the raised back.

## Construction notes

Flat-fell the inseam so it does not chafe a seated wearer. Use a soft elastic across the raised
back rather than a hard band. Set the hook-loop tape on each side seam so the waist adjusts
one-handed. The `side_adjust` parameter drives both the strip length and the waistband overlap.

## Cross-commons bridge

Yantra4D **`hook-loop-tape`** (`notion.hardware_ref`): its `strip_length` (a sew-face flange
parameter) is driven by this trouser's `side_adjust`, the same parameter that drives the
`hook_loop_waistband` interface — the dimensional handshake the hardware lane enforces.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

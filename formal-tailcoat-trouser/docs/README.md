# Braid-side formal trouser

The dress trouser of evening and morning wear: a plain-front trouser with a **galloon braid down
the outside seam** — one row for morning dress, two for white-tie — no belt loops, no turn-ups,
closing on a trouser hook and bar.

Part of the **Fashion Cabinet Commons** (FC-500, rank #446 — tailoring, T3).
**Yantra4D-bridged** (`trouser-hook-bar`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

The correctness of a braid trouser is all in the outside seam: the braid must run a seam that
closes true, or it wanders and the whole leg reads wrong. Sharing one side length between front
and back gives the braid a true line at any size.

## Pieces

`front` (cut 2, braid outseam) + `back` (cut 2, raised rise) + `waistband` (cut 1, hook and bar).

## The seam that solves

The front and back share **one measured `SIDE_LEN`** so the braided outside seam matches; the rise
difference is taken at the centre seams over **one shared crotch point**, so the inseams are
identical and the leg cannot twist. The extra back rise is **clamped under 35 % of the
leg-below-waist** so the waistline can never invert, whatever the sliders do.

## Construction notes

Set the silk galloon braid down each outside seam — one row for morning dress, two for white-tie.
No belt loops, no turn-ups. Build a proper curtained waistband. The hook and bar is the only
closure.

## Cross-commons bridge

Yantra4D **`trouser-hook-bar`** (`notion.hardware_ref`): its `hook_width` (a sew-plate flange
parameter) is driven by this trouser's `hook_width`, the same parameter that drives the
`waistband_closure` interface — the dimensional handshake the hardware lane enforces.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

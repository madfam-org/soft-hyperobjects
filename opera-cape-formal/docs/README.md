# Opera evening cape

The full-length evening cape worn over white-tie: a **sweeping circular cape** on a tall stand
collar, closing at the throat on a hook and eye.

Part of the **Fashion Cabinet Commons** (FC-500, rank #448 — tailoring, T3).
**Yantra4D-bridged** (`hook-and-eye`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

A true circular cape is a hard flat-pattern problem: it is a ring sector, and a ring sector drawn
with two arcs about *different* centres collapses into a shape that still closes but has no drape.
Getting it right restores the cape from fancy dress to real tailoring.

## Pieces

`cape` (cut 1 on fold at centre back, the ring sector) + `collar` (cut 1, stand, hook-and-eye).

## The seam that solves

The neck arc (radius `r_neck`) and the hem arc (radius `r_neck + cape_length`) are drawn about
**one shared centre**, so the sector is always a true annulus of positive area at every sweep —
never a zero-area lens the kernel would launder into a valid-looking outline. `r_neck` is solved
from the measured neck so the collar seam closes.

## Construction notes

Cut the cape on the fold at centre back in a wide sweep of cloth; satin-line it for drape. Stiffen
the stand collar so it stands away from the shoulders. A small covered chain weight at the hem
keeps it hanging straight.

## Cross-commons bridge

Yantra4D **`hook-and-eye`** (`notion.hardware_ref`): its `rows` is driven by this cape's
`hook_rows`, the same parameter that drives the `throat_closure` interface.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Pleated cummerbund

The pleated silk waist sash of black-tie dress: horizontal **knife pleats facing up**, worn over
the waistband, closing at the back on hooks and eyes.

Part of the **Fashion Cabinet Commons** (FC-500, rank #442 — tailoring, T2).
**Yantra4D-bridged** (`hook-and-eye`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

A cummerbund looks trivial and hides a real trap: the pleats eat height, so a panel cut to the
finished dimension comes out too short once folded. Taking the take-up into the pattern means the
sash is right the first time at any waist and any pleat count.

## Pieces

`band` (cut 1, the pleated sash) + `stay` (cut 2, the back closure reinforcement).

## The seam that solves

The flat cut height is solved as **`finished_height + pleat_count × 2 × pleat_depth`** — each
knife pleat consumes twice its depth — and the take-up is **clamped under 1.6× the finished
height** so the flat panel is always taller than finished and the finished height can never go
negative, whatever the sliders do.

## Construction notes

Cut a firm silk satin (barathea or grosgrain) so the pleats stay crisp and face up. Edge-stitch
each pleat. Stiffen the back stay so the hooks hold and the pleats do not sag.

## Cross-commons bridge

Yantra4D **`hook-and-eye`** (`notion.hardware_ref`): its `rows` is driven by this sash's
`hook_rows`, the same parameter that drives the `back_closure` interface.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Sling Bag

A **single-strap cross-body sling**: a teardrop panel wide at the shoulder and tapering to
a rounded hip point, a gusset that gives it depth, a webbing strap, and two anchor tabs.
The strap clips through a **swivelling snap hook** that bridges to the Yantra4D
[`snap-hook-swivel`](https://app.yantra4d.com) — the swivel is what stops a one-strap bag
from twisting on the body.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`panel` (teardrop, cut 2) + `gusset` (depth strip, cut 1) + `strap` (webbing cross-body
strap, cut 1) + `tab` (hook anchor tab, cut 2).

## The seam that solves

The teardrop's sides and point are **Bezier curves — their combined arc length has no
closed form**. So the gusset's span is taken from the *measured* run of one panel's
`side_r + point + side_l` rather than from a width/length formula, and both gusset long
edges verify against that run.

Four seams are declared and verified: both gusset long edges against the panel outer run,
the tab's hook end against the strap's hook end (both feed the same hook eye, so they must
be cut to the same webbing width), and the panel opening against its own mirror.

The hip width is additionally clamped to 90% of the shoulder width in the script, so no
parameter combination can invert the taper into a non-teardrop.

## Parameters

`bag_length`, `bag_width`, `point_width`, `bag_depth`, `webbing_width` (drives the
Yantra4D hook's webbing eye), `strap_length`, `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `snap-hook-swivel`, mapping `webbing_w → webbing_width` and
`webbing_t → max(2, webbing_width / 12)`. **Dimensional**: the hook's sewn
`eye_webbing_slot` flange is driven by `webbing_w`, and the same `webbing_width` drives
this bag's `hook_webbing` interface — enforced by `verify_hardware_links`.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

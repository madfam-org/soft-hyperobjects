# Roll-Top Backpack

A **roll-top rucksack**: a body wall with a roll extension above the load line, an oval
base panel, two curved shoulder straps, and webbing closure straps that buckle across the
rolled top. The buckle bridges to the Yantra4D
[`side-release-buckle`](https://app.yantra4d.com), sized to the pack's own webbing.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`body` (wall + roll extension, cut 1) + `base` (oval base panel, cut 1) + `shoulder`
(curved padded strap, cut 2) + `closure` (webbing closure strap, cut 2).

## The seam that solves

The base is a **stadium oval** — two straight runs joined by two semicircular caps,
sampled as a 48-point polygon. The body has to wrap that oval's entire perimeter, so the
body's wrap width is derived from the **measured polygon perimeter** rather than from a
`2·π·r + straight` formula: `body.base_edge` matches `base.rim_a + base.rim_b` exactly.

Three seams are declared and verified: the back seam (`wrap_a ↔ wrap_b`), the base seam,
and the closure webbing's two long edges.

## Parameters

`pack_width`, `pack_depth`, `pack_height`, `roll_height`, `webbing_width` (drives the
Yantra4D buckle's webbing channel), `strap_length`, `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `side-release-buckle`, mapping `webbing_w → webbing_width` and
`webbing_t → max(2, webbing_width / 12)`. **Dimensional**: the buckle's sewn
`webbing_channel` flange is driven by `webbing_w`, and the same `webbing_width` drives
this pack's `closure_webbing` interface — enforced by `verify_hardware_links`.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

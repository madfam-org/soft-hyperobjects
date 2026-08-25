# Messenger Bag

A **flap-over messenger**: a body panel folded at the base, wrap-around side gussets, a
curved cover flap, and a webbing closure strap that feeds a cam buckle. The buckle bridges
to the Yantra4D [`cam-buckle`](https://app.yantra4d.com) — one-handed, which is why
messengers use them.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`body` (front + base + back, cut 1) + `gusset` (side gusset, cut 2) + `flap` (cover flap,
cut 1) + `strap` (webbing closure strap, cut 1).

## The seams

The gusset is a continuous strip spanning the body's whole side run (front + base + back),
and the flap's `attach` edge sews onto the back panel's top opening. Both runs are taken
from the drafted geometry rather than assumed. Four seams are declared and verified: the
gusset against the body side, the flap against the body top, the two body openings against
each other, and the gusset against its own mirror (one gusset per side of the bag).

The flap's front edge is a three-segment chain — Bezier corner, straight run, Bezier corner
— so the rounded corners scale with the flap rather than being a fixed radius.

## Parameters

`bag_width`, `bag_height`, `bag_depth`, `flap_drop`, `webbing_width` (drives the Yantra4D
buckle's webbing throat), `strap_length`, `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `cam-buckle`, mapping `webbing_w → webbing_width` and
`webbing_t → max(2, webbing_width / 12)`. **Dimensional**: the buckle's sewn
`webbing_throat` flange is driven by `webbing_w`, and the same `webbing_width` drives this
bag's `closure_webbing` interface — enforced by `verify_hardware_links`.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

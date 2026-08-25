# Duffel Bag

The classic **cylinder duffel**: a body panel that wraps into a tube, two circular end
panels, a top zip opening, and two webbing carry handles. **Strap rings** anchor a
removable shoulder strap at each end — the ring bridges to the Yantra4D
[`strap-ring`](https://app.yantra4d.com), sized to the bag's own webbing.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`body` (cylinder wall, cut 1) + `end` (circular end panel, cut 2) + `handle` (webbing
carry handle, cut 2).

## The seam that solves

A circular end is drafted as a 48-segment polygon, whose perimeter is slightly under the
true circle `2·π·r`. The body's wrap length is therefore taken from the **measured
polygon perimeter**, not from `2·π·r` — so `body.circ_top` and `body.circ_bottom` each
match `end.rim_a + end.rim_b` exactly rather than carrying the chord error. All three
seams (`wrap_a↔wrap_b`, and both circumference seams) are declared and verified.

## Parameters

`bag_length`, `bag_diameter`, `webbing_width` (drives the Yantra4D ring's webbing
channel), `handle_length`, `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `strap-ring`, mapping `webbing_w → webbing_width` and
`opening → webbing_width + 6`. **Dimensional**: `strap-ring`'s sewn `tape_bar` flange is
driven by `webbing_w`, and the same `webbing_width` drives this bag's `ring_anchor_tab`
interface — so `verify_hardware_links` enforces name resolution **and** the
shared-dimension handshake.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

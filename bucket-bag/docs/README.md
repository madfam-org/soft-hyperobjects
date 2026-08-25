# Bucket Bag

A **drawcord bucket**: a circular base, a flared cylindrical wall, a drawcord casing at the
top, and a shoulder strap finished with a metal **strap end tip** — the part that stops a
leather strap end from curling and fraying. The tip bridges to the Yantra4D
[`strap-end-tip`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`body` (flared wall, cut 1) + `base` (circular base, cut 1) + `casing` (drawcord casing,
cut 1) + `strap` (shoulder strap, cut 1).

## The seams that solve

Two independent solves, following the [`bucket-hat`](../../bucket-hat/docs/README.md)
circular-drafting precedent:

1. The base is a **48-gon**, whose perimeter is under the true circle. The wall's base
   edge is derived from the *measured* polygon perimeter, so `body.base_edge` matches
   `base.rim_a + base.rim_b` exactly.
2. The wall **flares** — it is a trapezoid, not a rectangle, so its top edge is longer than
   its base edge (627.9 mm → 753.4 mm at defaults). The casing is drafted to the wall's
   *measured* top edge.

The flared top's circumference is scaled by the same polygon-vs-circle ratio the base
carries, so both ends of the wall stay dimensionally consistent with each other.

Four seams are declared and verified: the base seam, the casing seam, the wrap seam
(`wrap_a ↔ wrap_b`, the two leaning trapezoid sides), and the strap's two ends.

`top_flare = 0` degenerates the trapezoid cleanly back to a rectangle and still renders.

## Parameters

`base_diameter`, `bag_height`, `top_flare`, `casing_depth`, `strap_width` (drives the
Yantra4D tip's strap channel), `strap_length`, `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `strap-end-tip`, mapping `strap_w → strap_width`,
`strap_t → max(2, strap_width / 10)`, `tip_len → strap_width * 1.6`. **Dimensional**: the
tip's sewn `strap_channel` flange is driven by `strap_w`, and the same `strap_width` drives
this bag's `strap_tip` interface — enforced by `verify_hardware_links`.

## Provenance

Original draft for Fashion Cabinet; circular-drafting precedent from the Fashion Cabinet
`bucket-hat` cartridge. `CERN-OHL-W-2.0`.

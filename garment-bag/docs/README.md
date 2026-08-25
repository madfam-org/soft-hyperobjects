# Garment Bag

The hanging **garment bag**: a suit or a dress travels on its own hanger inside a shaped
sleeve that zips down the centre front. Two mirrored front halves take the zipper between
them, a whole back panel closes the other face, a shaped shoulder yoke caps the top and
carries the hanger-hook slot, and a depth gusset walks the side and hem so a jacket's
shoulders are not pressed flat. The centre-front zip bridges to the Yantra4D
[`zipper`](https://app.yantra4d.com), sized to the bag's own length.

Part of the **Fashion Cabinet Commons** (FC-300, rank #253 — care & keeping). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Garment bags are the point at which a wardrobe stops being clothing and starts being
storage, and the mass-market answer is unvented PVC — which traps the moisture that grows
mould on stored wool. A bag drafted to the coat someone actually owns, in cotton or
ripstop, is breathable, launderable, and cut once rather than bought in three sizes.

## Pieces

`front` (half front, cut 2 mirrored — the zip edge is `centre_front`) + `back` (whole
panel, cut 1) + `yoke` (shoulder cap with the hook slot, cut 2) + `gusset` (depth strip,
cut 2).

## The seam that solves

The yoke's two sloped edges are **not straight lines** — they are the same bowed
shoulder polyline the front and back panels carry at their tops. Rather than assume
`hypot(dx, dy)`, the yoke edge is built from the **same point list** as the panel edge and
both are **measured**, so `yoke.slope_l ↔ front.top` matches to the runner's tolerance
instead of drifting by the chord error. The gusset's length is likewise the summed
measured perimeter of the back panel's side and hem edges, doubled for the two sides.

## Construction notes

Sew the yoke to both faces before closing the gusset — the yoke is what holds the
shoulder shape while the long seams are run. The hook slot is drafted **without** seam
allowance; bind it rather than turning it, or the hanger neck will not pass. Grainlines
run vertically on `front` and `back` so the bag hangs without twisting on the bias.

## Cross-commons bridge

`notion.hardware_ref` → `zipper`, mapping `zip_length → bag_length` and
`tape_width → bag_depth / 4`. **Dimensional**: the zipper's sewn `tape_edge` flange is
driven by `zip_length`, and the same `bag_length` drives this bag's `zip_tape` interface —
so `verify_hardware_links` enforces name resolution **and** the shared-dimension
handshake.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

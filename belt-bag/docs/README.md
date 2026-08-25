# Belt Bag / Fanny Pack

A **curved-front belt bag**: a body panel (front + base + back folded at the base), a top
zip, and a webbing belt threaded through two loops. The zip bridges to the Yantra4D
[`zipper`](https://app.yantra4d.com), **sized to the bag's own length**.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 3 — accessories). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## Pieces

Body (front + base + back) + two belt loops.

## Parameters

`bag_width` (drives the Yantra4D zip length), `bag_height`, `bag_depth`, `belt_width`,
`seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `zipper`, mapping `zip_length → bag_width`. **Dimensional**: the
top-zip tape and the zipper's `tape_edge` flange share `bag_width`, so
`verify_hardware_links` enforces name resolution **and** the shared-dimension handshake.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Dopp Kit

A **boxed toiletry / wash bag**: a wrap body (front + base + back folded at the base),
two end gussets that give it its rigid box shape, and a top zip. The zip bridges to the
Yantra4D [`zipper`](https://app.yantra4d.com), **sized to the bag's own length**.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 3 — accessories). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## Pieces

Body (front + base + back) + two end gussets.

## Parameters

`kit_length` (drives the Yantra4D zip length), `kit_height`, `kit_depth`,
`seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `zipper`, mapping `zip_length → kit_length`. **Dimensional**: the
top-zip tape and the zipper's `tape_edge` flange share `kit_length`, so
`verify_hardware_links` enforces name resolution **and** the shared-dimension handshake.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

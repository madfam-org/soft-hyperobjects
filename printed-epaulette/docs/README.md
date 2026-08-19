# Printed Epaulette

A **Yantra4D-bridged notion** for the additive-manufacturing frontier of trims — a 3D-printed rigid structured shoulder board (tapered plate + rim + button post) for a uniform or costume shoulder line.
Fashion Cabinet owns the fashion (sizing to the wearer, the sewable-edge placement
guide); the printed part itself is the Yantra4D
[`epaulette-board`](https://app.yantra4d.com) solid, referenced through `notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 2 — AM-fashion). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A 2-D **Placement Guide** for the sewn edge where the printed part joins the garment.

## The cross-commons bridge (`notion.hardware_ref`)

Linked to the Yantra4D `epaulette-board` cartridge. The bridge is **dimensional**: the guide's
sewn edge and the printed part's `flange` cdg_interface share driving parameters, so
`verify_hardware_links` enforces name resolution **and** the shared-dimension handshake.

## Provenance

Original draft for Fashion Cabinet. Commons license **pending the FC1 commons-license
ruling** (`LicenseRef-FC1-pending`).

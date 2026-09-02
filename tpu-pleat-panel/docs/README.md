# TPU Pleat Panel

A **Yantra4D-bridged notion** for the additive-manufacturing frontier of the fabric
library — a 3D-printed TPU **accordion-pleated panel** that concertinas like pleated
cloth. Fashion Cabinet owns the fashion (finished panel dimensions, the pleat count from
the panel height, the sewable-edge placement guide); the pleated wall itself is the
Yantra4D [`tpu-pleat-panel`](https://app.yantra4d.com) solid, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 2 — AM-fashion). One material
identity, **Bambu TPU 95A**, spans this notion and that solid — the same panel is a
Fashion Cabinet fabric and a Yantra4D object at once. Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabi.net).

## What this cartridge produces

A 2-D **Panel Placement Guide**: the finished (relaxed) panel outline with its sewn edge
and horizontal marking lines at each pleat crease. Sew the printed pleat panel in at the
guide edge; it concertinas as a permanently-pleated fabric.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Panel Placement Guide** | `placement-guide` | Panel outline + sew edge + pleat-crease markings. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `panel_width_mm` | 200 mm | Finished width across the pleats; **capped at 300 mm** (the print bed). |
| `panel_height_mm` | 320 mm | Relaxed drop; the pleat count follows. |
| `pleat_depth` | 12 mm | Passed to the Yantra4D panel; deeper = more compression. |
| `wall` | 1.2 mm | Facet wall; thinner = softer folds. |
| `seam_allowance` | 10 mm | Tape-bound edge where the panel sews to a garment. |

## The cross-commons bridge (`notion.hardware_ref`)

Linked to the Yantra4D `tpu-pleat-panel` cartridge. The bridge is **dimensional**: the
guide's own sewn edge and the printed panel's `panel_edge` flange share driving
parameters, and the `params_map` derives the printed pleat count from the panel height —

    pleats = round(panel_height_mm / (2 · pleat_depth))

The FC cartridge computes the **same** pleat count in its metadata (e.g. a 320 mm drop at
12 mm depth is **13 pleats** on both sides), so both commons agree on the exact pleating.
`verify_hardware_links` enforces name resolution **and** the shared-dimension handshake.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

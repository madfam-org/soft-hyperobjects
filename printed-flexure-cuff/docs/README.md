# Printed Flexure Cuff

A **Yantra4D-bridged notion** for the additive-manufacturing frontier of trims — a
3D-printed TPU cuff that stretches over the hand and springs back, a sleeve or hem
finish with **no separate elastic**. Fashion Cabinet owns the fashion (cuff
circumference to the sleeve opening, height, the sew-in placement guide); the flexure
band itself is the Yantra4D [`tpu-flexure-cuff`](https://app.yantra4d.com) solid,
referenced through `notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 2 — AM-fashion). One material
identity, **Bambu TPU 95A**, spans this notion and that solid. Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A 2-D **Cuff Placement Guide**: the unrolled cuff band (circumference × height) with the
sewn cuff edge and marking lines showing where the printed flexure slot rows land. Sew
the printed cuff to the sleeve/hem at the guide edge.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Cuff Placement Guide** | `placement-guide` | Unrolled cuff band + sew edge + flex-row markings. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `wrist_girth` | 170 mm | Finished sleeve opening; drives the printed cuff circumference (bound to `wrist_girth`). |
| `cuff_height` | 60 mm | How tall the cuff band is up the sleeve. |
| `wall` | 2.0 mm | Passed to the Yantra4D band; thinner = softer flex. |
| `seam_allowance` | 10 mm | Tape-bound edge where the cuff sews to the sleeve. |

## The cross-commons bridge (`notion.hardware_ref`)

Linked to the Yantra4D `tpu-flexure-cuff` cartridge, mapping the sleeve opening
(`wrist_girth`), height, and wall to the printed band. The bridge is **dimensional**: the
guide's own cuff edge and the printed band's `cuff_edge` flange are driven by the same
parameters, so both commons agree on the finished band. `verify_hardware_links` enforces
name resolution **and** the shared-dimension handshake.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

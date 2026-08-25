# Articulated Scale Mail

A **Yantra4D-bridged notion** for the additive-manufacturing frontier of the fabric
library — a 3D-printed TPU **scale-mail panel** (overlapping scales on flexure necks)
that articulates like a dragon-scale garment. Fashion Cabinet owns the fashion (finished
panel dimensions, the scale field from the panel size, the sewable-edge placement
guide); the scale-and-neck field itself is the Yantra4D
[`tpu-scale-mail`](https://app.yantra4d.com) solid, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 2 — AM-fashion). One material
identity, **Bambu TPU 95A**, spans this notion and that solid. Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabinet.app).

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Panel Placement Guide** | `placement-guide` | Panel outline + sew edge + scale-row markings. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `panel_width_mm` | 180 mm | Finished width across the scales; **capped at 300 mm** (the print bed). |
| `panel_height_mm` | 280 mm | Finished height; the scale rows follow. |
| `scale_size` | 22 mm | Passed to the Yantra4D panel; sets scale width (and height = 1.3×). |
| `overlap` | 0.45 | Fraction each row overlaps the one below; more = tighter coverage. |
| `seam_allowance` | 10 mm | Tape-bound edge where the panel sews to a garment. |

## The cross-commons bridge (`notion.hardware_ref`)

Linked to the Yantra4D `tpu-scale-mail` cartridge. The bridge is **dimensional**: the
guide's sewn edge and the printed panel's `panel_edge` flange share driving parameters,
and the `params_map` derives the scale field from the panel size —

    cols = round(panel_width_mm  / scale_size)
    rows = round(panel_height_mm / (scale_size · 1.3 · (1 − overlap)))

The FC cartridge computes the **same** field in its metadata (a 180 × 280 mm panel at
22 mm scales, 0.45 overlap is **8 × 18** on both sides). `verify_hardware_links` enforces
name resolution **and** the shared-dimension handshake.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

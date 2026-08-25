# Lattice Armor Panel

A **Yantra4D-bridged notion** for the additive-manufacturing frontier of the fabric
library — a 3D-printed TPU **armor lattice** (rigid tiles on flexible bridges) that
drapes like a scale garment. Fashion Cabinet owns the fashion (finished panel
dimensions, the tile grid from the panel size, the sewable-edge placement guide); the
tile-and-bridge lattice itself is the Yantra4D
[`tpu-lattice-panel`](https://app.yantra4d.com) solid, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 2 — AM-fashion). One material
identity, **Bambu TPU 95A**, spans this notion and that solid. Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabinet.app).

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Panel Placement Guide** | `placement-guide` | Panel outline + sew edge + tile-grid markings. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `panel_width_mm` | 180 mm | Finished width across the tiles; **capped at 300 mm** (the print bed). |
| `panel_height_mm` | 260 mm | Finished height; the tile rows follow. |
| `tile_size` | 18 mm | Passed to the Yantra4D panel; larger tiles = stiffer, more armored. |
| `tile_gap` | 3 mm | Gap the flexure bridge spans; more = more drape. |
| `seam_allowance` | 10 mm | Tape-bound edge where the panel sews to a garment. |

## The cross-commons bridge (`notion.hardware_ref`)

Linked to the Yantra4D `tpu-lattice-panel` cartridge. The bridge is **dimensional**: the
guide's sewn edge and the printed panel's `panel_edge` flange share driving parameters,
and the `params_map` derives the tile grid from the panel size —

    cols = round(panel_width_mm  / (tile_size + tile_gap))
    rows = round(panel_height_mm / (tile_size + tile_gap))

The FC cartridge computes the **same** grid in its metadata (a 180 × 260 mm panel at
18 mm tiles is **9 × 12** on both sides). `verify_hardware_links` enforces name
resolution **and** the shared-dimension handshake.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

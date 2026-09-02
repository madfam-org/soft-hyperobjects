# Cord Stopper

A **Yantra4D-bridged notion** — the 2-D **placement guide** for the spring toggle that locks a drawcord at a hood, hem, or waist. Fashion
Cabinet owns the fashion (spacing, placement, the guide that transfers every position
to the garment); the fastener **solid** is the Yantra4D
[`cord-lock`](https://app.yantra4d.com) cartridge, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 1 — findings & fasteners).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What this cartridge produces

A **Placement Guide** strip: pin it to the garment placement line and transfer each
fastener position as a drill-cross plus an outline, with alignment notches on the guide
edge. Print/plot flat, mark, then set the Yantra4D-printed (or off-the-shelf) fastener.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Placement Guide** | `placement-guide` | Fastener positions marked along the placement line. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `count` | 5 | How many fasteners along the line. |
| `run_length` | 300 mm | Length of the edge they space along. |
| `end_offset` | 15 mm | First/last inset from the ends. |
| `strip_width` | 40 mm | Width of the printed guide strip. |
| `cord_dia` | 4.0 | Drawcord diameter (mm) |

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`cord-lock` cartridge and maps the garment `cord_dia` to the solid's `cord_dia`. Resolution is enforced in CI by
`scripts/qa/verify_hardware_links.py` against the pinned snapshot
`docs/interfaces/yantra4d-hardware.snapshot.json`. The fastener attaches at a point/slot
(not a sewn edge), so the bridge is name + parameter resolution — no edge-length
handshake.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the fastener as *placement* — spacing math, the
  guide, transfer to the garment.
- **Yantra4D** (`cord-lock`): the fastener as a *solid* — the printable geometry.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

# Snap Fastener

A **Yantra4D-bridged notion** — the 2-D **placement guide** for the snap sockets and studs that close plackets, cuffs, and western shirts without a buttonhole. Fashion
Cabinet owns the fashion (spacing, placement, the guide that transfers every position
to the garment); the fastener **solid** is the Yantra4D
[`sew-on-snap`](https://app.yantra4d.com) cartridge, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 1 — findings & fasteners).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

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
| `socket_dia` | 12.0 | Snap socket diameter (mm) |

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`sew-on-snap` cartridge and maps the garment `socket_dia` to the solid's `snap_dia`
(and a fixed 4 rim `sew_holes`). Resolution is enforced in CI by
`scripts/qa/verify_hardware_links.py` against the pinned snapshot
`docs/interfaces/yantra4d-hardware.snapshot.json`. `sew-on-snap` declares a `sew_face`
**flange** interface driven by `snap_dia`, so this link also carries the **dimensional
handshake**: `socket_dia` feeds that flange dimension *and* drives the `placement_line`
garment interface, so the two edges are dimensionally coupled.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the fastener as *placement* — spacing math, the
  guide, transfer to the garment.
- **Yantra4D** (`sew-on-snap`): the fastener as a *solid* — the printable geometry.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

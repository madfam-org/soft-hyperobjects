# Chainmail Panel

A **Yantra4D-bridged notion** for the additive-manufacturing frontier of the fabric
library — a **3D-printed TPU chainmail panel that behaves as cloth**. Fashion Cabinet
owns the *fashion* here (panel sizing, the sewable-edge placement guide, cut planning
against the printed panel's fixed width); the flexible ring lattice itself is a Yantra4D
solid, [`tpu-chainmail-panel`](https://app.yantra4d.com), printed in place.

This is the **soft-goods ↔ hard-goods seam made physical** from the Fashion Cabinet
side: the first FC notion that is *also* a Yantra4D object. One material identity —
**Bambu TPU 95A**, the `tpu-panel-impreso` fabric card — spans this card and that solid,
so the same panel is a Fashion Cabinet fabric and a Yantra4D object at once.

Part of the **Fashion Cabinet Commons**. Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A 2D **Panel Placement Guide**: the finished panel outline with its tape-bound sew edge
(the `panel_edge` interface) and a faint marking grid showing how many ring rows and
columns the print will fill. It is the fashion-facing artifact — sew the printed panel
in like any cloth, tape-bound at the perimeter.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Panel Placement Guide** | `placement-guide` | Finished panel outline + sew edge + ring-grid markings. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `panel_width_mm` | 200 mm | Finished width; **capped at 250 mm** (the printed panel's bed-bound width). |
| `panel_height_mm` | 300 mm | Finished height down the body. |
| `ring_id` | 9.0 mm | Ring inner diameter — passed to the Yantra4D panel; larger = looser, drapier weave. |
| `wire_d` | 2.4 mm | Ring cross-section — thicker = stiffer panel. |
| `seam_allowance` | 10 mm | Tape-bound sew-edge allowance where the panel joins a garment. |

## Presets

- **Chest guard** — 200 × 300, 9 mm rings, 2.4 mm wire.
- **Sleeve panel** — 140 × 420, 8 mm rings, 2.2 mm wire.

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`tpu-chainmail-panel` cartridge. The bridge is dimensional, not just nominal: the
placement guide's own sew edge and the printed panel's `panel_edge` flange are driven
by the **same** parameters, and the `params_map` sizes the printed weave from the
finished panel dimensions:

| Yantra4D param | ← mapped from (FC) |
| :--- | :--- |
| `ring_id` | `ring_id` |
| `wire_d` | `wire_d` |
| `cols` | `round(panel_width_mm / (ring_id + wire_d))` |
| `rows` | `round(panel_height_mm / ((ring_id + 2·wire_d) · 0.62))` |

The FC cartridge computes the **same** `cols`/`rows` in its metadata, so both commons
agree on the exact ring grid — e.g. a 200 × 300 mm panel at 9 mm/2.4 mm rings is
**18 columns × 35 rows** on both sides. The `scripts/qa/verify_hardware_links.py` lane
enforces this handshake in CI (name resolution **and** the shared-dimension coupling)
against the pinned snapshot `docs/interfaces/yantra4d-hardware.snapshot.json`.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the panel as a *fabric* — finished dimensions, the
  sewable edge, cut planning against the bed-bound width, the placement guide.
- **Yantra4D** (`tpu-chainmail-panel`): the panel as a *solid* — the printable 4-in-1
  ring lattice, print-in-place, watertight rings, articulation clearance.

Both agree on the material `bambu-tpu-95a`, so a garment plans the cut/drape from this
card while the printable geometry comes from Yantra4D. Print flat in TPU; run Yantra4D's
3×3 swatch first to tune clearance, then print the full panel and sew it in.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

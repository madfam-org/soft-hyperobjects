# Boning Channel

A **Yantra4D-bridged notion** — the 2-D **channel stitching template** for spiral or
flat stays. Fashion Cabinet owns the channel (its width, its length, and the dead
space that keeps the bone out of the seam allowance); the stay **solid** is the
Yantra4D [`boning-stay`](https://app.yantra4d.com) cartridge, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (Wave T — findings II).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A **Channel Template**: for each channel, twin parallel stitch lines set at the stay
width plus its running clearance, squared off by bar tacks at each stay end, laid out
at the given pitch across the panel. Notches on the guide edge mark both stay ends.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Channel Template** | `placement-guide` | Twin stitch lines, bar tacks, and end notches per channel. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `stay_length` | 300 mm | Cut length of one bone; the channel is squared off at exactly this. |
| `stay_width` | 7 mm | Spiral steel 5–7 mm; flat steel 8–12 mm. |
| `channel_clear` | 0.5 mm | Running ease per side, so the stay slides without buckling the fabric. |
| `stay_count` | 8 | Channels laid out side by side. |
| `channel_pitch` | 60 mm | Centre to centre; closer pitch = smoother shaping, stiffer garment. |
| `end_clear` | 6 mm | Keeps the bone end out of the seam allowance. |

## Relationship to `structured-corset`

`structured-corset` marks its boning channels but spends its single
`notion.hardware_ref` slot on the `corset-busk`. A manifest carries **one**
hardware_ref, not an array, so the corset cannot also bridge the stay — this
cartridge is its boning companion, drafted to the same channel geometry.

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`boning-stay` cartridge, mapping `stay_length`, `stay_width`, and `channel_clear`
through. Resolution is enforced in CI by `scripts/qa/verify_hardware_links.py`
against the pinned snapshot `docs/interfaces/yantra4d-hardware.snapshot.json`.

`boning-stay` declares a `sew_face` **flange** interface driven by `stay_length` and
`channel_wall`, so this link also carries the **dimensional handshake**:
`stay_length` feeds the hardware's sewn face *and* drives this cartridge's own
`channel_run` interface, coupling the channel's length to the stay's.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the stay as a *channel* — width, clearance,
  end-stop, and the template that stitches it.
- **Yantra4D** (`boning-stay`): the stay as a *solid* — the bone and its channel
  profile.

## Provenance

Original draft for Fashion Cabinet. Commons license **pending the FC1 commons-license
ruling** (`LicenseRef-FC1-pending`).

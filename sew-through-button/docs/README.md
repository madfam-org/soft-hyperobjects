# Sew-Through Button

A **Yantra4D-bridged notion** — the 2-D **placement guide** for the ordinary 2- or
4-hole button, the most-replaced component in the world's wardrobe. Fashion Cabinet
owns the fashion (ligne sizing, spacing, and the thread-hole pattern the sewer has to
hit); the button **solid** is the Yantra4D
[`sew-through-button`](https://app.yantra4d.com) cartridge, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (Wave T — findings II).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A **Placement Guide** strip: pin it to the placket centre line and transfer each
button position as its outline circle plus the 2- or 4-hole thread pattern inside it,
with alignment notches on the guide edge. Print/plot flat, mark, then sew.

The distinction from `shank-button` is the whole point: a shank button is sewn
through a loop underneath, so the guide only needs the centre. A sew-through button
is stitched through its own face, so the guide must carry the **holes**.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Placement Guide** | `placement-guide` | Button positions, outlines, and hole clusters along the placket. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `button_ligne` | 24 | Trade sizing; 1 ligne = 0.635 mm. Shirt 16–20L, coat 30–40L. |
| `button_count` | 6 | Buttons spaced along the placket. |
| `placket_length` | 300 mm | The run they space along. |
| `end_offset` | 15 mm | First/last button inset from the ends. |
| `strip_width` | 40 mm | Width of the printed guide strip. |
| `hole_count` | 4 | 2 holes (bar) or 4 holes (cross/parallel). |
| `show_outline` | true | Draw the button footprint around each hole cluster. |

The hole spacing is derived, not set: trade practice puts the holes on a square about
a third of the button diameter across, so the stitch never rides the rim.

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`sew-through-button` cartridge, mapping `button_ligne` and `hole_count` straight
through, `hole_spacing` as `button_ligne * 0.635 / 3`, and a fixed 1.8 mm `hole_dia`.
Resolution is enforced in CI by `scripts/qa/verify_hardware_links.py` against the
pinned snapshot `docs/interfaces/yantra4d-hardware.snapshot.json`.

`sew-through-button` declares a `sew_face` **flange** interface driven by
`button_ligne`, `hole_count`, `hole_dia`, and `hole_spacing`, so this link also
carries the **dimensional handshake**: `button_ligne` and `hole_count` feed the
hardware's sewn face *and* drive this cartridge's own `button_stand` interface, so
the garment's edge and the hardware's sewn face are dimensionally coupled.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the button as *placement* — spacing math, the hole
  pattern, the guide that transfers both to the placket.
- **Yantra4D** (`sew-through-button`): the button as a *solid* — the printable
  geometry, dish, and holes.

## Provenance

Original draft for Fashion Cabinet. Commons license **pending the FC1 commons-license
ruling** (`LicenseRef-FC1-pending`).

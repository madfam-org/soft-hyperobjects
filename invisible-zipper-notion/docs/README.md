# Invisible Zipper

A **Yantra4D-bridged notion** — the 2-D **installation guide** for the concealed coil
zipper. Fashion Cabinet owns the installation (the stitch line, the stops, the
crossing seam); the zipper **solid** is the Yantra4D
[`invisible-zipper`](https://app.yantra4d.com) cartridge, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (Wave T — findings II).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What this cartridge produces

An **Installation Guide** strip laid along the seam, carrying:

- the **stitch line**, set one coil radius off the guide edge — this is the single
  thing that makes an invisible zipper invisible, and it is invisible in every
  finished garment you could inspect;
- the **tape edge**, so the seam allowance is known to be wide enough;
- **stop bars** at the top and bottom of the slider's travel;
- an optional **crossing seam** line and notch, for a waist or midriff seam that must
  match across the opening.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Installation Guide** | `installation-guide` | Stitch line, stops, tape edge, and crossing-seam mark. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `zipper_length` | 560 mm | Stop to stop, not tape end to tape end. |
| `tape_width` | 24 mm | Full width of one tape; sets the seam allowance needed. |
| `coil_dia` | 4 mm | Sets the stitch offset — the foot rides half a coil off the seam. |
| `end_margin` | 30 mm | Guide run past each stop, so the template can be pinned. |
| `cross_seam` | 0 | Distance from the top stop to a crossing seam; 0 = none. |

## Relationship to `zipper-notion`

`zipper-notion` bridges the Yantra4D `zipper` cartridge — a closed-end coil zipper
with a conventional, topstitched installation. This cartridge is the **concealed**
variant: a different solid, a different stitch offset, and a different seam finish.
They are complements, not duplicates.

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`invisible-zipper` cartridge, mapping `zipper_length` → `zip_length`, `tape_width`,
and `coil_dia` through. Resolution is enforced in CI by
`scripts/qa/verify_hardware_links.py` against the pinned snapshot
`docs/interfaces/yantra4d-hardware.snapshot.json`.

`invisible-zipper` declares a `tape_edge` **flange** interface driven by
`tape_width`, `tape_thick`, and `zip_length`, so this link also carries the
**dimensional handshake**: `zipper_length` and `tape_width` feed the hardware's sewn
edge *and* drive this cartridge's own `zipper_tape` interface — the same dimensions
flow to both edges.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the zipper as *installation* — the offset, the
  stops, the matching.
- **Yantra4D** (`invisible-zipper`): the zipper as a *solid* — tape, coil, slider.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

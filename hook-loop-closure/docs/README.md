# Hook-and-Loop Closure

A **Yantra4D-bridged notion** — the 2-D **tape placement template** for hook-and-loop
tape, the closure that makes dressing possible without fine motor control. Fashion
Cabinet owns the closure (the footprint, the sew margin, the segmentation); the tape
**solid** is the Yantra4D [`hook-loop-tape`](https://app.yantra4d.com) cartridge,
referenced through `notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (Wave T — findings II).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A **Tape Template**: per segment, the tape footprint plus a perimeter sewing line
inset by the sew margin on all four sides — stitching on that line never rides the
hook field, which is the failure that makes a retrofitted closure shred its own
thread. Long runs are broken into segments separated by gaps, so the closure peels
progressively instead of demanding two hands and one hard pull.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Tape Template** | `placement-guide` | Per-segment footprint, inset sew line, and start/end notches. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `strip_length` | 200 mm | Cut length of one piece of tape. |
| `strip_width` | 25 mm | Wider holds more force but is harder to peel one-handed. |
| `sew_margin` | 3 mm | Inset of the stitching line; too small and the needle rides the hooks. |
| `segments` | 1 | Splitting a long run makes it peel progressively. |
| `segment_gap` | 10 mm | Unclosed space between pieces — where the closure flexes. |

## Relationship to the adaptive garments

`side-opening-top` and `adaptive-wrap-skirt` both bridge `magnetic-clasp`. Magnets and
hook-and-loop are different adaptive closures with different trade-offs — magnets open
with no grip strength at all but hold weakly; hook-and-loop holds strongly but needs a
peel. This cartridge is the second option, not a replacement for the first.

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`hook-loop-tape` cartridge, mapping `strip_length`, `strip_width`, and `sew_margin`
straight through. Resolution is enforced in CI by
`scripts/qa/verify_hardware_links.py` against the pinned snapshot
`docs/interfaces/yantra4d-hardware.snapshot.json`.

`hook-loop-tape` declares a `sew_face` **flange** interface driven by exactly those
three parameters, so this link also carries the **dimensional handshake**: all three
feed the hardware's sewn face *and* drive this cartridge's own `tape_run` interface.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the tape as a *closure* — footprint, sew margin,
  segmentation, and the template that places them.
- **Yantra4D** (`hook-loop-tape`): the tape as a *solid* — base, hook field, loop
  field.

## Provenance

Original draft for Fashion Cabinet. Commons license **pending the FC1 commons-license
ruling** (`LicenseRef-FC1-pending`).

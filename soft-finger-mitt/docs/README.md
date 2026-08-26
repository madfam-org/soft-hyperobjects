# Soft-finger dressing mitt

A dressing mitt for a hand with **limited grip**: a neoprene mitt carrying one soft-finger
actuator that curls to pinch a zip-pull, a button hook or a sock edge against the palm.

Part of the **Fashion Cabinet Commons** (FC-500, rank #433 — adaptive / soft-exo).
**Yantra4D-bridged** (`soft-finger`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Dressing is the first task independence is measured by, and it rests on a pinch a limited hand
may not have. A dressing mitt gives that pinch back by carrying one soft actuator that curls an
object against the palm; making the actuator the printable part lets it be re-fitted and re-tuned
as the hand changes. The assist is in the geometry, not just the label.

## Pieces

`palm` (cut 1, actuator pocket) + `back` (cut 1) + `thumb` (cut 2, a rounded stall) + `cuff`
(cut 1, the wrist band). All four fingers share one pocket; the thumb is separate.

## The seam that solves

The palmar pocket runs the drafted `finger_len` from the palm base to the tip — the same number
that drives the Yantra4D `soft-finger` actuator. The mitt-top **dome depth is clamped between
20 mm and 90 % of the half-width** so the top can never collapse to a degenerate point, whatever
the sliders do; `finger_len` is clamped under `hand_length − 50`. Palm and back sew at both
sides and across the top dome; the cuff mouth is the palm ring.

## Construction notes

Cut the neoprene at a small negative ease so the mitt grips. Flatlock the seams so nothing
presses a hand with limited grip. Slide the printed soft-finger into the palmar pocket; route
its air line to a small squeeze bulb.

## Cross-commons bridge

Yantra4D **`soft-finger`** (`notion.hardware_ref`): its `finger_len` is driven by this mitt's
`finger_len`, the same parameter that drives the `actuator_pocket` interface — the printed
actuator is exactly as long as the pocket that holds it.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

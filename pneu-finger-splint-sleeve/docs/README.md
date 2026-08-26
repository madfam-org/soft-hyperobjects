# Pneumatic finger-splint sleeve

A splint sleeve for a single finger that **cannot extend or flex on its own**: a printed TPU
wrap that holds a PneuNet bending actuator along its dorsal length. Inflate to extend the
finger; vent to flex it.

Part of the **Fashion Cabinet Commons** (FC-500, rank #432 — adaptive / soft-exo).
**Yantra4D-bridged** (`pneu-net-finger`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

A static splint only holds a joint still; it cannot move it through its range, which is exactly
what a recovering finger needs to avoid contracture and win back its pinch. A pneumatic splint
does the moving. Making the actuator the printable, replaceable part lets the assist be re-fitted
and re-tuned as recovery changes. The assist is in the geometry, not just the label.

## Pieces

`sleeve` (cut 1, the tapered finger wrap with the dorsal actuator channel) + `anchor` (cut 1,
the strap that ties the sleeve to the back of the hand so the base does not slide).

## The seam that solves

The dorsal channel runs the drafted `finger_len` from the base knuckle to the tip — the same
number that drives the Yantra4D `pneu-net-finger` actuator. The `tip_girth` is **clamped under
`base_girth − 4`** so the tapered wrap can never invert, whatever the sliders do; both closing
seams run base to tip so they match by construction.

## Construction notes

Back the dorsal side with the airtight layer so the channel holds the actuator's line. Seal the
closing seam narrow. Close the wrap and the anchor strap on hook-and-loop dots so a swollen
finger can still pass. Route the air tube to a small hand pump: inflate to extend, vent to flex.

## Cross-commons bridge

Yantra4D **`pneu-net-finger`** (`notion.hardware_ref`): its `finger_len` is driven by this
sleeve's `finger_len`, the same parameter that drives the `actuator_channel` interface — the
printed actuator is exactly as long as the channel that holds it.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

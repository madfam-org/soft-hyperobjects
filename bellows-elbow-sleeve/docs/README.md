# Bellows-actuated elbow sleeve

An elbow sleeve that **flexes and extends** an arm that cannot bend on its own: a printed TPU
sleeve over the upper arm and forearm, carrying a bellows actuator along the inner crook —
inflate to flex the elbow, vent to straighten.

Part of the **Fashion Cabinet Commons** (FC-500, rank #436 — adaptive / soft-exo).
**Yantra4D-bridged** (`bellows-actuator`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

An arm that cannot bend loses the reach that brings a cup to the mouth. Rigid powered braces are
heavy, loud and one-size; a soft bellows moves the elbow gently and silently and follows the arm
rather than forcing it. Making the bellows the printable part lets the assist be re-tuned to the
person's strength. The assist is in the geometry, not just the label.

## Pieces

`upper` (cut 1, the upper-arm section with the bellows channel) + `fore` (cut 1, the forearm
section, channel continuing) + `cuff` (cut 1, the wrist gripper).

## The seam that solves

The inner channel runs the drafted `bellows_run` across the crook — the same number that drives
the bellows convolutions. The upper and forearm sections **meet at ONE shared elbow girth** so
the sleeve is continuous at the elbow; every section width is clamped above a minimum so no panel
can collapse, whatever the sliders do. The cuff attaches to the forearm's wrist edge.

## Construction notes

Print the crook side airtight to back the bellows; keep the rest soft. Seal the seams narrow.
Slide the printed bellows into the crook channel; route the air line to a small pump or CO2
cartridge. Anchor the sleeve top and wrist so the bellows works the elbow, not the fabric.

## Cross-commons bridge

Yantra4D **`bellows-actuator`** (`notion.hardware_ref`): its `outer_dia` is driven by this
sleeve's `elbow_girth`, and the crook channel — the garment's `bellows_channel` interface — is
solved to `bellows_run` so the printed bellows is exactly as long as the channel that holds it.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

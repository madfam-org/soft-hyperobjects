# Assistive grip glove

A **soft-exoskeleton grip glove** for a hand that cannot close on its own: a neoprene shell
whose palmar side carries Fin-Ray finger ribs that flex the wearer's fingers around an object
when a tendon line is pulled and open them on release.

Part of the **Fashion Cabinet Commons** (FC-500, rank #431 — adaptive / soft-exo).
**Yantra4D-bridged** (`finray-gripper`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

A hand that cannot close loses the everyday grip that independence is built on — a cup, a rail,
a fork. The rigid off-the-shelf answer forces the fingers to one fixed shape and swallows all
tactile feedback. Fin-Ray fingers close *softly* around whatever they meet, so one glove holds
many shapes; making the actuator the printable part means it can be re-fitted as the hand
changes. The assist is in the geometry, not just the label.

## Pieces

`palm` (cut 1, four finger channels + a thumb channel) + `back` (cut 1, plain) + `cuff`
(cut 1, the wrist band).

## The seam that solves

Each palmar finger channel runs the drafted `finger_len` from the knuckle line to the
fingertip — the same number that drives the Fin-Ray rib. `finger_len` is **clamped under
`hand_length − 50`** so the fingertip can never invert above the knuckle line, whatever the
sliders do; the channel seams are drawn straight so the rigid rib does not buckle. The palm and
back sew at both sides and across the fingertip dome; the cuff length is the wrist ring.

## Construction notes

Cut the neoprene shell at a small negative ease so it grips and the ribs do not slide when they
work. Flatlock the shell seams so nothing presses a hand that cannot re-grip. Slide each printed
Fin-Ray finger into its palmar channel; route the tendon cord to the pull.

## Cross-commons bridge

Yantra4D **`finray-gripper`** (`notion.hardware_ref`): its `fin_len` is driven by this glove's
`finger_len`, the same parameter that drives the `finger_channel` interface — the printed rib is
exactly as long as the channel that holds it.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

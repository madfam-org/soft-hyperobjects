# Tendon-knuckle wrist brace

A wrist-and-knuckle brace that **lends a tendon back** to a hand that has lost extension: a
printed TPU wrap over forearm, wrist and back of the hand, carrying an articulated tendon-knuckle
linkage so a pull at the forearm extends the knuckles.

Part of the **Fashion Cabinet Commons** (FC-500, rank #435 — adaptive / soft-exo).
**Yantra4D-bridged** (`tendon-knuckle`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

A wrist-drop from radial-nerve palsy, a stroke or a tendon injury is a loss of *motion*, and a
static splint can only prop it. An articulated linkage restores the motion — lift on the pull,
fall on the spring. Making the linkage the printable part lets the brace be re-tuned as strength
returns. The assist is in the geometry, not just the label.

## Pieces

`forearm` (cut 1, the tapered forearm-to-wrist wrap with the tendon channel) + `hand` (cut 1,
the back-of-hand knuckle band) + `strap` (cut 2, the closures).

## The seam that solves

The dorsal channel runs the drafted `linkage_span` from the forearm anchor to the knuckle line —
the same number that drives the Yantra4D `tendon-knuckle` segment run. The `wrist_girth` is
**clamped under the forearm girth** so the tapered wrap can never invert, and the channel is
clamped under the dorsal run. The forearm and hand join at the wrist edge (both the same wrist
ring); each wrap closes on itself.

## Construction notes

Print the dorsal side semi-rigid and the palmar side soft. Seal the channel seam narrow. Slide
the printed linkage in; route the tendon cord and return spring. Cinch on the hook-and-loop
straps one-handed.

## Cross-commons bridge

Yantra4D **`tendon-knuckle`** (`notion.hardware_ref`): its `seg_len` is driven by this brace's
`linkage_span`, the same parameter that drives the `linkage_channel` interface — the printed
linkage is exactly as long as the channel that holds it.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

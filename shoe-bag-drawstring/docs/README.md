# Shoe Bag (Drawstring)

The travelling **shoe bag**: a flat-bottomed drawstring sack that swallows a pair of shoes
sole-to-sole and cinches shut on a cord. A single body panel wraps into a tube, an oval
base closes the bottom, and a folded casing band at the mouth carries the drawcord out to
a Yantra4D [`cord-lock`](https://app.yantra4d.com) toggle on the tail.

Part of the **Fashion Cabinet Commons** (FC-300, rank #254 — care & keeping). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Hotel shoe bags are single-use non-woven polypropylene, and the alternative most people
use is a supermarket carrier that tears in a week. This is the smallest useful object in
the care lane: one rectangle, one oval, one band, cut from offcuts, and it keeps a dirty
sole off clean clothing for years rather than one trip.

## Pieces

`body` (tube wall — `wrap_a` meets `wrap_b` at the side seam) + `base` (oval bottom,
cut 1) + `casing` (folded drawcord channel at the mouth, cut 1).

## The seam that solves

The base is an **oval** — a stadium, two half-circles joined by straights — because a shoe
pair is long and narrow and a circular base wastes fabric across the width. Once
polygonised, that outline has no clean closed form, so the body's wrap length is taken
from the **measured base perimeter**, and the casing band is measured against the same
wrap. Three seams solve off one measurement instead of three independent guesses that
would not agree.

## Construction notes

Run the casing before closing the side seam — a folded band is far easier to attach flat
than in the round. Leave the cord exit at the side seam so the drawcord's two tails emerge
together and can share one cord-lock. The base is eased, not gathered: clip the seam
allowance at the curve ends rather than adding fullness.

## Cross-commons bridge

`notion.hardware_ref` → `cord-lock`, mapping `cord_dia → cord_diameter`, `cords → 2`, and
`body_size → cord_diameter * 4`. The cord-lock declares no flange interface — its mating
geometry is a `snap` and a `pocket` — so the dimensional-handshake rule is satisfied by
name resolution alone, while `cord_diameter` still drives this bag's own `cord_casing`
interface.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

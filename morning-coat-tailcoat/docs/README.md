# Morning coat

Formal daywear, the descendant of the riding coat: below the single fastening button the front
**sweeps away in a continuous cutaway** to the side seam, and the coat continues behind as a long
tail skirt.

Part of the **Fashion Cabinet Commons** (FC-500, rank #439 — tailoring, T4, made-to-measure).
**Yantra4D-bridged** (`shank-button-solid`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

The morning coat is the surviving daytime formal coat — weddings, Ascot, state occasions — and
its defining cutaway is exactly the part a flat pattern most easily gets wrong: sketch the sweep
by eye and at some sizes it runs backwards, inverting the front into an outline that still closes
but no longer describes a coat.

## Pieces

`front` (cut 2, cutaway) + `back` (cut 1 on fold) + `tail` (cut 1 on fold, waist-seamed skirt) +
`sleeve` (cut 2) + `collar` (cut 1).

## The seam that solves

The cutaway is a **clamped span** — its horizontal run and the button height are both floored
positive, so a negative span can never invert the front into geometry the kernel's CCW
normalization launders into a valid-looking outline. The tail top is the **measured back waist**
so the waist seam closes; the sleeve cap is **solved to the armscye ring** by iteration.

## Construction notes

Hair-canvas the front and lapel so the cutaway rolls and holds. Cut the tail on its own grain so
it hangs. Edge-stitch the cutaway and the tail; face the peak lapel; fully line.

## Cross-commons bridge

Yantra4D **`shank-button-solid`** (`notion.hardware_ref`): its `diameter_mm` is driven by this
coat's `button_dia`, the same parameter that drives the `button_stand` interface.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

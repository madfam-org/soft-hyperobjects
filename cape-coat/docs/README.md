# A-line Cape Coat

A wool-melton **cape coat with no set sleeves**: the body flares from the shoulder to a wide
A-line sweep that drapes over the arms, with vertical arm slits, a stand collar, and a row of
toggle-and-loop closures.

Part of the **Fashion Cabinet Commons** (FC-400, rank #378 — outerwear).
**Yantra4D-bridged** (`toggle`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

A cape is the most forgiving winter coat there is — it fits a changing body, a pregnancy, a
wheelchair, or a plaster cast without a refit, because there is no set sleeve to bind. In
non-fraying wool melton with a raw sweep and printable toggles, a beginner can cut it from a
single length and keep it across years and shapes.

## Pieces

`front` (cut 2 mirrored, A-line flare + arm slit + toggle placket) + `back` (cut 1 on fold,
A-line flare) + `collar` (stand collar, cut 2 on fold).

## The seam that solves

An A-line flare makes the hem far wider than the shoulder, so the side seam is **not vertical —
it slants out**. The front and back side seams must still be equal length despite the slant, so
the flare is applied symmetrically: both panels run the side seam from the shoulder point to a
hem point offset by the same `hem_flare`, and the seam matches by construction. The arm slit is
clamped inside the panel; the toggle pitch is solved so the row lands exactly; the back neck
width is solved from the front's measured shoulder with the flatten clamp; the collar is cut to
the measured neckline.

## Construction notes

Bind the arm-slit edges — they take the strain of the hands coming through. Wool melton does not
fray, so the A-line sweep can be cut raw with no hem. Set the frog loops to the same
`toggle_len` the toggle barrel is bored for.

## Cross-commons bridge

Yantra4D **`toggle`** (`notion.hardware_ref`): its `barrel_len` (a cord-face flange parameter) is
driven by this cape's `toggle_len`, the same parameter that drives the `toggle_placket` interface
— the dimensional handshake the hardware lane enforces.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

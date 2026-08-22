# Structured Fascinator

A **cocktail fascinator built over a rigid base**: fabric discs cover the base's two
faces, a gored shallow dome stands proud of the disc, and a bias trim ring binds the
outer edge. The rigid base is the Yantra4D
[`fascinator-base`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300 #212, Lane 2 — millinery). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

Cover top + cover underside (48-gon discs), dome gore (cut `dome_gores`, mirrored),
and the bias trim ring.

## Parameters

`base_dia` (the shared bridge dimension), `dome_height`, `dome_gores`, `trim_width`,
`cover_margin`, `seam_allowance`.

## Drafting

Discs are **48-gons on a corrected radius** (`r = C / (2n·sin(π/n))`) so the drafted
perimeter equals the intended circumference exactly. The dome is a gore set — two
Bézier edges to a shared apex over a straight base — sized to 72% of the base
circumference so it sits inboard of the rim. The trim ring is a straight bias strip
whose ends join into a ring (a self-seam, declared join-to-join).

## Cross-commons bridge

`notion.hardware_ref` → `fascinator-base`, mapping `base_dia → base_dia`,
`dome_h → dome_height`, `brim_w → trim_width`, `sew_holes → max(8, round(base_dia / 12))`.

**Dimensional (sew-ring handshake).** The base declares a `trim_sew_ring` **flange**
driven by `base_dia`/`brim_w`/`sew_holes`. On the garment side, `base_dia` also drives
the `sew_ring` interface — the trim ring's inner edge, whose drafted run *is* the base
circumference. So the same dimension flows to both the hardware's sewn edge and the
garment's own edge, and `verify_hardware_links` enforces name resolution **and** the
shared-dimension coupling. Re-pointing that flange key at a non-interface parameter is
detected as a handshake failure.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

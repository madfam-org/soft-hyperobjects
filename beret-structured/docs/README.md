# Structured Beret

The **classic two-piece beret**: a full circular top and an annular under whose outer
edge matches the top's circumference and whose inner hole is the head opening, finished
by a structured band. Sizing is delegated to the Yantra4D
[`hat-size-reducer`](https://app.yantra4d.com) that clips inside the band.

Part of the **Fashion Cabinet Commons** (FC-300 #216, Lane 2 — millinery). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

Top (full circle), under (half-annulus cut on fold + mirrored), and the structured band.

## Parameters

`head_girth` (ISO 8559), `overhang`, `band_height`, `ease`, `seam_allowance`.

## Drafting

The beret is two concentric rings: the head opening at `head_girth + ease`, and the
outer ring `overhang` further out. That difference is the beret's whole character — it
is what makes the crown flop over the band.

Rings use a **corrected radius** (`r = C / (2n·sin(π/n))`) so drafted perimeters equal
their intended circumferences exactly. The under is a **half-annulus cut on the fold**,
so *both* its curved edges measure half their rings; each is declared against its mate
with the edge listed **twice** — the piece against its own mirror, **join-to-join**
rather than join-to-fold. At defaults the two ring seams read `923.30 vs 923.30` and
`578.00 vs 578.00`.

## Cross-commons bridge

`notion.hardware_ref` → `hat-size-reducer`, mapping `head_circ → head_girth + ease` and
`strip_height → min(band_height, 32)`. The reducer is **point/slot hardware** — it clips
inside the band rather than being sewn into a garment edge, so it declares no `flange`
interface and the dimensional-coupling rule does not apply. Name resolution is still
enforced by `verify_hardware_links`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

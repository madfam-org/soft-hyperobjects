# Lapelled formal waistcoat

A formal evening waistcoat with a **proper lapel** — the low-cut, lapelled vest worn under a
dinner jacket or tailcoat, as opposed to a plain V-neck vest. Points at the hem, a cinch strap
at the back.

Part of the **Fashion Cabinet Commons** (FC-500, rank #441 — tailoring, T3).
**Yantra4D-bridged** (`sew-through-button`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

The lapel is the detail cheap formalwear drops because it is fiddly to draft, and the reason a
hired outfit looks hired. Bringing it into a parametric commons — with the lapel roll and pointed
hem solved so no size produces an inverted edge — puts made-to-measure evening tailoring within
reach.

## Pieces

`front` (cut 2, lapel + point) + `back` (cut 2, cinch strap) + `strap` (cut 2).

## The seam that solves

The front hem **point drop is clamped under a quarter of the front length** so the point can
never fall below the hem baseline and invert the hem edge, whatever the sliders do; the lapel
break is clamped between the shoulder and the hem. Front and back share identical side and
shoulder geometry so the seams match by construction.

## Construction notes

Canvas the lapel and front edge so the lapel rolls. Cut a satin or lining back with the cinch
strap. Fully line. Set five sew-through buttons down the front edge below the lapel break.

## Cross-commons bridge

Yantra4D **`sew-through-button`** (`notion.hardware_ref`): its `button_ligne` (a sew-face flange
parameter) is driven by this waistcoat's `button_ligne`, the same parameter that drives the
`button_stand` interface — the dimensional handshake the hardware lane enforces.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

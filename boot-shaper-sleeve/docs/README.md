# Boot Shaper Sleeve

The stiffened sleeve that stands inside a **tall boot** so the shaft does not crease and
collapse at the ankle. A leather boot left slumped for a season learns the fold; this is
the removable insert that prevents it. A tapered sleeve wraps into a truncated cone, a
batten pocket runs its slant height, and a hook-and-loop tab lets one sleeve fit a range of
calves — bridging to the Yantra4D [`hook-loop-tape`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300, rank #258 — care & keeping). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Commercial boot shapers are single-size polypropylene tubes that fit one boot and are
thrown out with it. Cutting the true cone to a measured calf makes one insert that fits the
boots someone actually owns, in canvas offcuts, and keeps a repairable leather boot upright
for another decade — the cheapest possible intervention against the single most common way
a good boot dies.

## Pieces

`sleeve` (the annular-sector cone development, cut 1) + `batten` (stiffener pocket running
the slant height, cut 1) + `tab` (hook-and-loop adjustment tab, cut 2).

## The seam that solves

A boot shaft is a **truncated cone**, and the flat pattern for a cone is an **annular
sector** — not a trapezoid. The trapezoid is the classic error: rolled up, it gives a cone
whose seam edges do not lie flat against each other. This cartridge solves the true cone
development — slant height from the radius difference, sector angle from the ratio — and
then **polygonises and measures** both arcs, so the top arc really equals `calf_circ` and
the bottom arc really equals `ankle_circ`, rather than carrying the chord error of an
unmeasured curve.

## Construction notes

Cut the sector with the grain running along the slant, not around the arc — a bias-run
sleeve will not hold the shaft up, which is the whole job. Sew the batten pocket to the
sleeve while it is still flat, then close the cone seam last. Size the batten to slide out
before washing; a permanently enclosed stiffener makes the sleeve unlaunderable, and a
shaper that cannot be cleaned goes back into a boot dirty.

## Cross-commons bridge

`notion.hardware_ref` → `hook-loop-tape`, mapping `strip_width → tab_width`,
`strip_length → calf_circ * 0.25`, and `sew_margin → seam_allowance * 0.3`.
**Dimensional**: the tape's sewn `sew_face` flange is driven by `strip_width`,
`strip_length`, and `sew_margin` — and `tab_width`, `calf_circ`, and `seam_allowance` all
drive this sleeve's own `closure_tab` interface, so the same dimensions reach both sewn
edges.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

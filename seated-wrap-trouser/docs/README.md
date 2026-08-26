# Seated-wear wrap trouser

A trouser that **dresses from a seated position** without standing: the whole front wraps open
flat and closes with magnetic clasps, so a wearer who cannot stand lays it under themselves,
folds the wrap fronts across, and the clasps snap shut. The rise is drafted for sitting.

Part of the **Fashion Cabinet Commons** (FC-500, rank #437 — adaptive).
**Yantra4D-bridged** (`magnetic-clasp`). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Dressing lying down or seated is the reality for many wheelchair users and people recovering from
surgery, and an ordinary trouser must be pulled over the hips — which needs a stand or a lift —
and gaps at the back when the wearer sits. This wraps completely open to be laid under the body,
closes on clasps that need no aim or pinch grip, and holds a seated rise. The aid is in the
geometry, not just the label.

## Pieces

`front` (cut 2, the overlapping wrap fronts, low rise) + `back` (cut 2, raised rise) + `waistband`
(cut 1, carries the clasps).

## The seam that solves

The front and back **side seams share one measured `SIDE_LEN`** so they match despite the
differing rises; the wrap overlap is added **at the waist only**, above a crotch and inseam that
are identical to the back, so the leg cannot twist. The wrap overlap is **clamped under 90 % of a
quarter-hip** so it never folds back on itself, and the extra back rise is **clamped under 35 % of
the leg-below-waist** so the waistline can never invert — every extreme stays watertight.

## Construction notes

Cut a soft four-way stretch jersey so it lays flat to wrap under and moves with a seated body.
Flat-fell the inseam so it does not chafe. Set the magnetic clasps at the marked wrap line;
route a soft elastic across the raised back.

## Cross-commons bridge

Yantra4D **`magnetic-clasp`** (`notion.hardware_ref`): its `disc_dia` is driven by this trouser's
`clasp_diameter`, the same parameter that drives the `wrap_closure` interface — the dimensional
handshake the hardware lane enforces.

## Provenance

Original draft for Fashion Cabinet; seated-rise lineage from `seated-wear-trouser` (FC-400 #372).
`CERN-OHL-W-2.0`.

# Rehab Sensor Cuff

A forearm cuff that holds a motion sensor in one place on a limb that is trying to
push it off. Wave FC3-H (E-textile II) of the FC-300 commons.

> **This is a garment pattern, not a medical device.** It holds a sensor and
> positions it. It does not measure, monitor, or diagnose anything, and it makes no
> clinical claim.

## What it is

| Piece | Cut | Role |
|---|---|---|
| `cuff` | 1 | The outer shell: the solved annular sector, carrying the sensor plate footprint, its four sew points, and the lead run. |
| `lining` | 1 | The skin side, cut to the **same** sector, carrying the anti-migration grip bands. |
| `strap` | 1 | The closure strap, cut to the shell's **measured** proximal arc plus the overlap, with a tension index at the arc. |

## Why it earns a commons rank

Two neighbours in the commons look adjacent and are not:

- **`printed-flexure-cuff`** is a Yantra4D-bridged notion — a printed TPU trim that
  finishes a sleeve. Its only FC piece is a placement guide.
- **`arm-warmers`** is a tapered stretch tube for warmth, cut as a single flat panel
  with one straight join seam. Beginner, and deliberately approximate.

This one is a **carrier**, and it earns the rank on a fact about rehab hardware:
motion-capture kit is sold with straps in two or three sizes, and the strap is where
the measurement quality actually goes. A cuff that rotates or slides gives you a
session that cannot be compared to last week's. Clinics work around it with tape and
marker pen on the skin. Making the repeatability a property of the garment — a
solved cone, a plate that cannot hinge, a tension index that reproduces the same
compression every session — is a real contribution, and it is a *pattern* problem,
not an electronics one.

## The seam that had to solve

**The flat pattern of a tapered cuff is an annular sector, not a trapezoid.**

This is the classic mistake and it is easy to make: two girths, one height, so draw
a trapezoid. But a cuff whose ends differ in circumference is a **frustum** — a
truncated cone — and unrolling a frustum gives you a ring segment with two *curved*
edges. Cut the trapezoid and your two curved edges are straight lines: the cuff
cones the wrong way and its edges cup away from the limb, which is precisely the
migration the cuff exists to prevent.

The kernel solves the sector properly:

```python
_r_p  = C_P / (2·π)                      # cone radius at the elbow end
_r_d  = C_D / (2·π)                      # cone radius at the wrist end
SLANT = hypot(cuff_height, _r_p - _r_d)  # the SURFACE distance, not the axis
R_D   = _r_d * SLANT / (_r_p - _r_d)     # similar triangles
R_P   = R_D + SLANT
THETA = C_P / R_P                        # sector angle, radians
```

And then `R_D × THETA` equals `C_D` **exactly** — which is not an assumption, it is
the arithmetic closing on itself, and it is the proof that the draft is right. The
kernel measures the drawn distal arc and reports the residual:

| case | sector angle | R_D / slant | distal arc drawn | target | **error** |
|---|---|---|---|---|---|
| default (280→220 mm) | 26.29° | 3.67 | 202.399 mm | 202.400 mm | 0.0008 mm |
| large (400→250 mm) | 39.30° | 1.67 | 229.998 mm | 230.000 mm | 0.002 mm |
| extreme (520→120 mm) | 251.47° | 0.30 | 110.362 mm | 110.400 mm | 0.039 mm |

Two things that would have quietly broken it, both handled:

- **The slant, not the height.** The radial span of the sector is the distance along
  the cone's *surface*, `hypot(height, Δr)` — not the axial height. Substituting the
  height cuts the cuff short by `slant_vs_height_mm`: 0.32 mm at the defaults,
  1.20 mm on the large preset, **23.85 mm** at the extreme taper. Small at the
  defaults, but it is a compression garment; the whole fit budget is a few
  millimetres, and the error is worst exactly where the cone is most pronounced.
- **The degenerate case is real, and the obvious guard is not enough.** As the taper
  goes to zero `R_D` diverges and there is no cuttable sector. But a bare epsilon on
  `Δr` does not catch it: a 10 mm taper over a 380 mm calf is *numerically* fine and
  *geometrically* absurd — a 3.5° sector on a five-and-a-half-metre radius, which is
  a straight line wearing a disguise. So the guard is on the sector radius itself,
  as a multiple of the piece's own slant (`R_D ≤ 12 × slant`). The `calf_untapered`
  preset (380→370 mm) trips it and drafts as a rectangle at the proximal girth,
  declaring the 9.2 mm of taper it gave up as `rect_fallback_slack_mm` rather than
  silently absorbing it.

The measured arcs are then load-bearing. The arcs are drawn as 48-chord polylines
(sagitta under 0.02 mm at these radii), so the *drawn* length is very slightly under
the true arc — and that difference is real cloth. The strap is cut to the
**measured** `prox` edge plus the overlap, declared as a seam with `ease =
strap_overlap`, so if the sector solve ever drifts the check fires rather than the
maker discovering it at the machine.

Declared seams: `lining.prox ↔ cuff.prox`, `lining.dist ↔ cuff.dist`,
`lining.closure_p ↔ cuff.closure_p`, and `strap.top ↔ cuff.prox` with the overlap
as declared ease.

**The lining is deliberately not eased.** Every other two-layer garment in this wave
eases its lining; this one must not. A lining eased inside a coned cuff rotates
independently of the shell — which is exactly the failure mode the cuff exists to
prevent, reintroduced one layer in.

## Placement by arc length

`sensor_offset` is a fraction of arc length, not an x-coordinate. On a circular arc
uniform angle *is* uniform arc length, so the fraction maps directly — which means
`sensor_offset = 0.25` names the same anatomical landmark (the ulnar border, say) on
a 180 mm wrist and a 400 mm calf. An offset expressed in millimetres, or as a
fraction of a bounding box, would slide to a different place on the body every time
the limb size changed, and the whole point of the cuff is that the sensor sits in
the same place every session.

The grip bands follow the same logic, sampled along arcs at fractions of the slant
so they stay parallel to the cuff edges rather than to the cutting table.

## Hardware bridge

`notion.hardware_ref` → **`yantra4d/sensor-mount-plate`**.

`plate_w` × `plate_d` are the shared dimension: they drive the plate's `base_w` ×
`base_d` and they are the exact rectangle the shell draws as `sensor-plate`. They
also derive the plate thickness, corner radius, screw diameter and inset. The
manifest's `sensor_seat` interface declares both against the shell's proximal edge.

Note the plate's `cdg_interfaces` are a `thread` (the ¼-20 stud) and a
`bolt_pattern` — there is no `flange`, so the dimensional-handshake lane has no sewn
edge to couple and correctly reports nothing to check here. The coupling is still
made explicit in the manifest so a future flange on that solid finds the garment
side already wired.

**Four sew points, not two.** `plate-sew-nw/ne/sw/se` are drills at the plate's
corners. A plate sewn at two points is a hinge and will rock; at four it is a mount.
This is the difference between a sensor reading limb motion and a sensor reading its
own wobble.

## Construction notes

- **Fabric.** `poliester-elastano-compresion` — a power knit with real recovery,
  because `compression` is what holds the sensor still and a knit that relaxes
  loses the fit between sessions. Watch the 110 °C iron ceiling near the traces.
- **Marker efficiency is bad and that is honest.** The BOM assumes 62% rather than
  the usual 80%: an annular sector nests poorly. That is the cost of drafting the
  cone properly instead of approximating it with a trapezoid that nests beautifully
  and fits badly.
- **Order.** Sew the plate to the shell while it is flat, at all four points. Mark
  and apply the grip bands to the lining while *it* is flat. Then join the layers,
  then the strap. Nothing inside is reachable afterwards.
- **The tension index is the clinical bit.** The strap carries a drill at exactly
  the measured proximal arc. Pulled to that mark, the cuff is at the compression the
  pattern was cut for — every session, by any technician, without a judgement call.
- **Nothing electrical is drafted.** The plate footprint, its sew points, the lead
  run, and the grip bands are marked footprints and paths for a maker. No sensor,
  IMU, goniometer, or circuit is generated by this cartridge.

## Provenance

Original draft for Fashion Cabinet. The frustum development is standard sheet-metal
and millinery layout, well over a century old and not remotely novel; the
contribution is applying it where soft-goods drafting normally reaches for a
trapezoid, carrying the slant-versus-height distinction through to the cut, guarding
the degenerate cylinder honestly instead of dividing by a very small number, and
placing the hardware by arc-length fraction so the sensor lands on the same anatomy
at every size.

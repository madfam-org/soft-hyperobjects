# Sensor Hem Band

The instrumented hem of a compression garment: a doubled band at the leg or sleeve
opening that both **grips** and **carries**. Wave FC3-K (long-tail band, rank 297) of
the FC-300 commons.

> **This is a garment pattern, not a medical device.** It holds a plate and positions
> it. It does not measure, monitor, or diagnose anything, and it makes no clinical
> claim. Nothing electrical is drafted: the plate seat, its four sew points, the
> channel stitch lines and the run path are marked footprints for a maker.

## What it is

| Piece | Cut | Role |
|---|---|---|
| `band` | 1 | The outer band, cut to the **solved** length, carrying the plate seat and the dead-length markers. |
| `facing` | 1 | The inner layer, cut to the band's **measured** length, carrying the interlayer conductive channel. |
| `tab` | 1 | The service tab where the run leaves the channel for the garment's own seam. |

## Why it earns a commons rank

Two neighbours look adjacent and are not:

- **`rehab-sensor-cuff`** is a standalone tapered cuff that clamps a sensor to a bare
  limb. It is a frustum problem; its band is the whole garment.
- **`biometric-bra-band`** is an underbust band carrying electrodes against the skin.
  Its problem is skin contact, not opening grip.

This one is a **hem**. It is sewn to a garment opening that already exists, and its
entire difficulty is that it must be *shorter* than that opening while containing
something that refuses to be shorter than itself.

## The seam that had to solve

**A gripping band is cut short — but a rigid plate cannot be part of the shortening.**

The formula everyone writes is:

```python
band = hem_opening * (1 - grip)          # WRONG the moment a plate lives in the band
```

It is wrong because the plate's footprint, plus the margin either side of it, is a
**dead length**: it contributes in full to the sewn band and contributes *nothing* to
the stretch. Take the grip out of the whole opening and you have taken it out of cloth
that cannot give it. So the grip comes out of the **live remainder** only:

```python
DEAD     = plate_w + 2 * plate_margin
LIVE     = hem_opening - DEAD
BAND_LEN = DEAD + LIVE * (1 - grip)
```

and the difference from the naive version is exactly `DEAD × grip`:

| case | opening | dead | live | naive | **solved** | shortfall avoided |
|---|---:|---:|---:|---:|---:|---:|
| default | 380 | 58 | 322 | 334.4 | **341.4 mm** | **6.96 mm** |
| `wrist_tight` | 180 | 40 | 140 | 140.4 | **149.2 mm** | **8.80 mm** |
| `wide_plate_hard_grip` | 520 | 88 | 432 | 364.0 | **390.4 mm** | **26.40 mm** |

On a compression hem those millimetres are not a fitting nuisance. 26 mm short on a
520 mm band is a band that will not reach — or one that reaches by stretching cloth
*across the plate* until the plate rocks, the stitching cuts, and the join fails long
before the electronics do.

The solved difference is then declared: the band's `attach` edge is 341.4 mm against a
380 mm opening, and `grip_ease_mm` (38.64 mm) is the deliberate shortfall. The facing
and the tab are cut to the band's **measured** edge, so the two layers cannot drift.

Declared seams: `facing.attach ↔ band.attach`, `facing.join_r ↔ band.join_r`, and
`band.join_l ↔ band.join_r`.

**The facing is deliberately not eased.** An eased facing inside a gripping band takes
the stretch unevenly, and the plate — which lives in the band, not the facing — ends up
pulled off its marks. Same discipline, same reason, as `rehab-sensor-cuff`'s lining.

## The dead island, and the negative band

At the parameter extremes the dead length **exceeds the opening**: a 120 mm plate with
40 mm margins is a 200 mm island in a 140 mm opening, so `LIVE` goes negative and the
band is drafted shorter than nothing. That does not fail `verify()` — the kernel
CCW-normalizes the outline and hands back a piece with a positive area, closed edges,
and no complaint. It looks like a band. It cannot be sewn.

So the island is capped at 55% of the opening, and the plate width is re-derived from
what the cap actually leaves:

| requested | opening | dead asked | **dead capped** | plate re-derived | live | band |
|---|---:|---:|---:|---:|---:|---:|
| plate 120, margin 40, grip 0.30 | 140 | 200 | **77.0** | 120 → **69 mm** | 63.0 | 121.1 mm |

`dead_capped: true` is reported in the metadata, so the reduction is visible rather
than silent, and the manifest carries the same rule as a `warning`-severity constraint
so the studio says so before the render does.

The band depth carries a floor for the same reason — `plate_d + channel_w + 20` — since
a 110 mm plate beside a 30 mm channel in a 25 mm band gives a channel offset that runs
off the piece.

The cartridge was probed at the **minimum and maximum of all 10 parameters**, plus
all-min, all-max, cross extremes, and every `target_piece` at both defaults and all-max
— 59 cases, all `errors=0`, every declared seam ok, no degenerate bbox.

## The channel is between the layers

The conductive run does not go on the face of the band. It lies in a channel formed by
two stitch lines between the band and its facing, interrupted only where the plate's
leads come through (`channel-break`). A hem is the part of a garment that meets a shoe,
a sleeve cuff, a chair edge and a washing-machine drum; a run on the face of it is a
run with a service life. The channel also keeps the conductor away from the iron — the
compression knit's ceiling is 110 °C, and the channel is the part you never press.

The `tab` carries a marked **strain land**: the run is tacked to cloth before it enters
the garment's seam, so a tug is taken by the tab rather than by the conductor.

## Hardware bridge

`notion.hardware_ref` → **`yantra4d/sensor-mount-plate`**.

`plate_w` × `plate_d` drive the plate's `base_w` × `base_d`, and are the exact rectangle
the band marks as `plate-seat` — and the exact footprint the dead-length solve accounts
for. The plate's thickness, corner radius, screw diameter and inset derive from
`plate_d`, so there is one set of numbers rather than two.

The plate's `cdg_interfaces` are a `thread` (the ¼-20 stud) and a `bolt_pattern` — no
`flange` — so the dimensional-handshake lane correctly reports nothing to check on that
side. The coupling is declared anyway, so a future flange on that solid finds the
garment side already wired. This matches `rehab-sensor-cuff`, which bridges the same
solid.

**Four sew points, not two.** `plate-sew-nw/ne/sw/se` are drills at the plate's corners.
Two points is a hinge, and a hinge in a band that stretches every step is a plate that
rocks.

## Construction notes

- **Fabric.** `poliester-elastano-compresion` — a power knit with real recovery,
  because `grip` is the whole mechanism and a knit that relaxes gives the grip back.
- **Coverstitch everything that stretches.** The channel's two lines and the attach
  seam all want a stitch that stretches; a lockstitch there snaps on the first wear.
- **The dead-length markers are instructions, not decoration.** `dead-start` and
  `dead-end` bracket the rigid island: between them the band is fed flat, and the whole
  38.6 mm of grip is distributed across the live run outside them. Clear elastic along
  the dead length is the belt-and-braces version for a hurried machinist.
- **Order.** Sew the plate to the band at all four points while flat. Lay the run in
  the channel and close the channel on the facing while *it* is flat. Then join the two
  layers, then close the band, then attach it to the garment — stretching only outside
  the markers. Nothing inside is reachable afterwards.
- **`plate_pos` is a fraction of the solved band**, held clear of both ends, so the seat
  never straddles the band's own join seam.

## Provenance

Original draft for Fashion Cabinet. Banded hems with negative ease are ordinary knitwear
practice and not remotely novel; distributing stretch around a non-stretching insert is
ordinary craft knowledge on a factory floor. The contribution is writing that knowledge
down as arithmetic the pattern carries — naming the dead length, taking the grip out of
the live remainder only, declaring the resulting difference as seam ease so the check
proves it, capping the island so the extreme case cannot produce a band that verifies
and cannot be sewn, and marking on the cut file itself where the machinist must not
stretch.

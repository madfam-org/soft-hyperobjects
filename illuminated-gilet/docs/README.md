# Illuminated Cycling Gilet

A close-fitting sleeveless windshell drafted for the drops: short in front, long
and curved at the back, with the LED harness routed along a real seam instead of
cable-tied to whatever the rider already owns. Wave FC3-H (E-textile II) of the
FC-300 commons.

> **This is a garment pattern, not a lighting product.** It routes and seats a
> harness. No LED, driver, battery, or circuit is drafted here, and it makes no
> photometric or conspicuity claim.

## What it is

| Piece | Cut | Role |
|---|---|---|
| `front` | 2, mirrored | Gilet front, centre-front zip. Carries the chest strip trace, the LED spur, and the conduit-clip footprints along the side seam. |
| `back` | 1 on fold (CB) | Full-length back with the curved drop tail. Carries the shaped-seam harness run, the battery pocket at the tail, and the rear-light seat. |
| `placket` | 2, mirrored | Centre-front zip facing, cut to the front's **measured** `cf` edge. |

## Why it earns a commons rank

The commons already has three sleeveless things this could be confused with, and it
is none of them:

- **`hi-vis-vest`** is a boxy economy over-vest with hook-and-loop, cut to go over
  street clothes. Beginner, deliberately shapeless.
- **`heated-vest`** is a softshell with serpentine heating routes and a battery
  holder — same *domain*, opposite *function*, and cut straight.
- **`led-trim-jacket`** (this same wave) is a raglan jacket carrying a printed
  `led-channel` extrusion along its raglan curve.

This one is cut **for the cycling posture**, and that is what earns the rank. On a
bike the spine lengthens and the front shortens: a garment cut square rides up at
the front and exposes the lower back at exactly the moment the rider is most bent
over. So the back is `tail_drop` longer with a *curved* hem, the front is
deliberately short, and both side seams are suppressed at the waist because an aero
shell that flaps is slower and louder than no shell at all.

It also earns it on repairability. Lit cycling kit is sold either as a disposable
slap-on strip or as a sealed garment you cannot wash, resize, or repair. Routing the
harness through replaceable printed clips along a real seam makes the garment
repairable at the precise point these things fail: the wire, where it flexes.

## The seam that had to solve

**The front's hem height is not `armhole_drop + back_side_len`.**

Both side seams are *shaped* — bowed inward by `waist_suppress` — and a bowed edge
is longer than the vertical drop it spans. So the back's side seam has a known
measured length, and the front's side seam has to match it, but the front's hem
height that produces that length is not the length itself.

The obvious closed form takes the back's arc length and uses it as a vertical drop.
That is a category error, and it overshoots:

| `waist_suppress` | back side (measured) | naive hem y | solved hem y | **error** |
|---|---|---|---|---|
| 22 mm (default) | 272.66 mm | 522.66 mm | 520.00 mm | 2.65 mm |
| 60 mm (race fit) | 288.82 mm | 538.82 mm | 519.99 mm | **18.83 mm** |

At a racing fit the closed form is nearly two centimetres long on a seam that has to
match to the millimetre — and the error grows with exactly the parameter a rider
turns up to get the fit they want. So the kernel bisects instead:

```python
def _solve_front_hem(target_len, tol=0.02, iters=60):
    lo = armhole_drop + 1.0
    hi = armhole_drop + target_len + max(waist_suppress, 1.0) * 4.0
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if _front_side_edge(mid).length() < target_len:
            lo = mid
        else:
            hi = mid
        ...
```

Arc length is monotonic in the hem height (a longer drop at fixed absolute
suppression is a strictly longer arc), so the bisection converges cleanly. The
result is machine-checked: `front.side ↔ back.side` is a declared seam, and the
metadata reports `side_seam_mismatch_mm` — **0.0 mm** at the defaults, 0.007 mm at
the extremes, against a 1.0 mm tolerance.

The same measured run then drives the hardware. Clip count is floor-divided from the
**measured** side seam, respaced evenly along it, and each clip is seated by
**arc-length fraction** on the drawn curve:

```python
CLIP_COUNT   = max(2, int(BACK_SIDE_LEN // clip_pitch))
CLIP_SPACING = BACK_SIDE_LEN / (CLIP_COUNT + 1)
seat, _tangent = side_edge.point_at_fraction(CLIP_SPACING * (i + 1) / BACK_SIDE_LEN)
```

Placing them at a nominal `x = QUARTER` instead would drop every waist-region clip
*off* the seam it is meant to be caught in, by up to the full suppression. The
back's harness run is sampled off its own drawn side edge for the same reason.

Declared seams: `front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`,
`placket.attach ↔ front.cf`.

## Hardware bridge

`notion.hardware_ref` → **`yantra4d/seam-conduit-clip`**.

`clip_tab` is the dimensional handshake. It drives the clip's `seam_tabs` **flange**
interface (`tab_w`, `tab_t`, `clip_len`, `hole_dia`) — the sewn face — and it is the
exact rectangle the front draws as `conduit-clip-{i}`. The manifest's
`side_harness_seam` interface declares `clip_tab` and `clip_pitch` against the
`front.side ↔ back.side` seam, so the dimensional-handshake lane can verify the
garment's sewn edge and the hardware's sewn edge are one dimension.

The clip's `bundle_channel` socket is fed from `strip_w` — the conduit sizes to the
harness that goes through it. The kernel caps `clip_tab` at 2.4× `seam_allowance`:
a tab wider than the allowance can hold has nothing to bite on.

## Construction notes

- **Fabric.** `nylon-ripstop-shell` — windproof, packable, and it holds the turned
  hem the gripper needs. The drop tail nests badly, so the BOM's marker efficiency
  is deliberately set at 72% rather than the usual 80%.
- **Order.** Mark and sew the clips to the seam allowances *before* closing the side
  seams; they are caught in that seam as it closes. Then the shoulders, then the
  zip and placket, then the hem last so the gripper goes in over a finished tail.
- **The gripper is not optional.** A drop tail without an elastic or silicone
  gripper at the hem flaps at speed and defeats the point of the shape. The BOM
  sizes it to the back hem's measured length.
- **Battery at the tail.** Low, on the fold side, out of the wind and off the
  shoulder blades — the two places a hard object is worst on a bike.
- **Rear-light seat** is centred on the tail, where a following driver's headlights
  actually land.
- **Nothing electrical is drafted.** `chest-strip`, `led-spur`, `harness-run`,
  `side-harness-run`, `battery-pocket` and `rear-light-seat` are marked routes and
  footprints for a maker.

## Provenance

Original draft for Fashion Cabinet. The drop-tail sleeveless shell is standard
cycling-apparel practice and the shaped side seam is ordinary tailoring. The
contribution here is refusing the closed form where it is wrong: solving the front
hem against a *measured* shaped seam rather than an assumed drop, and seating the
hardware by arc length on the drawn curve rather than on the nominal straight the
curve replaced.

# Haptic Navigation Belt

A soft waist belt that gives direction by touch: vibration tactors spaced evenly
around the waist, so "north" or "turn left" arrives as a buzz at a place on your
body instead of a sound in your ear or a line on a screen. Wave FC3-H
(E-textile II) of the FC-300 commons.

> **This is a garment pattern, not a navigation device.** It carries motors and
> positions them around a measured waist. It does not locate, sense, or route
> anything, and no motor, driver, or circuit is drafted here.

## What it is

| Piece | Cut | Role |
|---|---|---|
| `shell` | 1 | The outer belt — the body run plus the buckle overlap; carries the main harness run and the buckle bar-tack. |
| `tactor` | 1 | The inner layer, cut to the shell's **measured** body run; carries the motor pockets, the strain-relief plate footprints, and the spurs down from the harness. |
| `tail` | 1 | The buckle tail: `tail_rows` of adjustment ladder plus the controller pocket at the front where you can reach it. |

## Why it earns a commons rank

The commons already has belts — `belt-bag`, `belt-buckle-notion`, `belt-clip-notion`.
None of them is a *carrier*: a belt drafted around the thing it has to hold in a
particular place.

Tactile wayfinding belts exist almost entirely as research prototypes and one-off
assistive-tech builds, each one rebuilt from scratch because there is no pattern to
start from. That is the gap this fills. Direction delivered to the waist frees the
ears, which matters most to people whose ears are already doing the navigating, and
to anyone working somewhere a screen or an earpiece is unsafe.

And it earns the rank on construction, not just on concept: the electrical failure
point is **designed for** rather than discovered. Every motor is a place a wire
terminates; a terminated wire at a flexing waist is where this garment dies. So every
tactor pocket is paired with a printed strain-relief plate caught in the top seam
beside it, and the plate's footprint is a real, drawn pattern feature.

## The seam that had to solve

**The tactor pitch is not `belt_length / n`.**

This is the whole draft. The motors have to be evenly spaced around the *wearer* —
if the belt is a compass, then tactor *i* has to sit at bearing `i × 360°/n` on the
body. But the shell is longer than the body: it carries `overlap` extra millimetres
that the buckle tail rides over. Divide the whole belt length and every motor's
bearing is skewed by the ratio `waist / (waist + overlap)` — at the defaults that is
a 17% error, which puts "north" 30° off by the time you reach the far side.

So the kernel refuses to assume the number. It splits the shell's top and bottom
edges into a named `body_run` / `overlap_run` pair, drafts the shell, **measures**
the `body_run` edge, and divides *that*:

```
_SHELL = build_shell()
MEASURED_BODY_RUN = _SHELL.edge("body_run").length()
TACTOR_PITCH      = MEASURED_BODY_RUN / tactor_count
```

At the defaults: shell 1060 mm long, measured body run 880 mm, 8 tactors, pitch
110 mm. Perturbed to a 1080 mm waist with 12 tactors: shell 1260 mm, measured body
run 1080 mm, pitch 90 mm. The naive divisor would have given 132.5 mm and 105 mm
respectively — wrong in both directions.

The tactor layer is then cut to that same measured run, and the seams are declared,
so the two layers' pockets register instead of drifting:

- `tactor.body_run ↔ shell.body_run`
- `tactor.top ↔ shell.body_top`
- `tail.attach ↔ shell.tail_end`
- `tail.bottom ↔ shell.overlap_run` — the tail's own length **is** the belt's
  adjustment range, so it has to equal the overlap the shell was drafted with.
  Declaring it as a seam is what stops the two from silently diverging.

The quieter solve is the stacking floor. A motor pocket and a relief plate both live
in the belt's height, and they must not overlap or the plate presses on the motor:

```
belt_width  = max(belt_width, tactor_dia + relief_width + 22)
relief_len  = min(relief_len, waist_girth / tactor_count × 0.5)
```

The second line is the collision guard along the seam — a plate longer than half the
pitch would run into its neighbour. Both are mirrored as manifest constraints so the
configurator warns before the kernel silently clamps.

## Hardware bridge

`notion.hardware_ref` → **`yantra4d/seam-strain-relief`**.

`relief_len` and `relief_width` are the dimensional handshake. They drive the
hardware's `seam_edge` **flange** interface (`plate_len`, `plate_w`, `sew_holes`,
`hole_dia`) — the plate's sewn face — and they are the exact rectangle the tactor
layer draws as `relief-plate-{i}`, one per motor, seated at
`plate_y = belt_width − relief_width/2 − seam_allowance` so the plate lands inside
the top seam allowance. The manifest's `relief_seam` interface declares both
parameters against the `tactor.top ↔ shell.body_top` seam, so the dimensional
handshake lane can verify that the garment's sewn edge and the hardware's sewn edge
are one dimension rather than two names that happen to resolve.

The plate's `cable_channel` socket is fed from `tactor_dia` — the motor's lead gauge
scales with the motor.

## Construction notes

- **Fabric.** `nylon-ripstop-shell` — webbing-weight, low stretch, and it holds a
  crease at the turned edge. The belt must not grow under load or the tactor
  bearings walk.
- **Order.** Mark and sew everything on the tactor layer while it is flat: pockets,
  plates, spurs. Then join the layers, then attach the tail. Nothing on the inner
  layer is reachable once the belt is turned.
- **The plates go in the seam.** Each `relief-plate-{i}` footprint is caught in the
  top seam allowance as the layers are joined — that is why `seam_allowance`
  defaults to 10 mm here rather than the usual 8. The wire from each motor passes
  through its plate's channel *before* it reaches the flex zone.
- **Harness.** `harness-run` on the shell keeps the main run along the upper third,
  away from the fold line where the belt creases. `tactor-spur-{i}` drops from the
  plate to the motor. These are marked routes for conductive thread or ribbon cable,
  not drafted conductors.
- **Buckle.** Maker's choice, bar-tacked at the marked `buckle-tack`. The BOM names
  a buckle but the pattern does not dictate one; the `tail_rows` ladder is what
  actually sets the adjustment granularity.
- **Controller.** Lives in the tail's marked pocket, at the front. Deliberately: it
  is the one thing you need to reach without taking the belt off.

## Provenance

Original draft for Fashion Cabinet. The three-layer belt with a bar-tacked tail is
ordinary bag-and-belt technique. The contribution here is drafting the tactor
spacing off a *measured* body run rather than a computed belt length, and treating
the strain relief as a pattern feature with a drawn footprint and a declared
hardware handshake rather than a note telling the maker to be careful.

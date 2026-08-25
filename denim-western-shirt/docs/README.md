# Denim Western Shirt

**FC-300 #290 · denim · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-on-snap`**

Pointed sawtooth yokes front and back, a snap-fastened centre front placket, snap
cuffs, and heavy contrast topstitching throughout.

## What it is

Six pieces: front (cut 2, with the placket extension), back on the fold, a front
sawtooth yoke (cut 2) and a back sawtooth yoke on the fold, a sleeve (cut 2), and
a barrel cuff (cut 2). The yokes carry the neck, the shoulders and the upper
armhole; the body panels carry everything below the yoke line.

## Why it earns its rank

`denim` was one of the two thinnest families in the 300-rank catalog. It also had
a specific hole: the western shirt is the most-copied and least-published
silhouette in commercial denim. Sawtooth yokes are drafted in-house at every
heritage brand and shared nowhere — which is exactly the kind of geometry a
commons should hold.

The snap front is not decoration either. It is there so a shirt tears open rather
than dragging a rider caught on a saddle horn or a fence, and it is the reason
the shirt is still worn by people who work around machinery.

## What is actually solved (not assumed)

### 1. The sawtooth seam, generated once and shared

**A western yoke's lower edge is not a line. It is a run of Vs, and the length
those Vs add to the seam is not linear in either the tooth count or the tooth
depth.** At defaults:

```
sawtooth_span_mm                 : 295.00     (the straight-line span)
sawtooth_run_measured_mm         : 358.67
sawtooth_added_over_straight_mm  :  63.67     (+21.6%)
```

Draft the yoke and the body panel independently and reconcile them with a
tooth-length formula, and you get a yoke that is tens of millimetres out on a
seam that is on the outside of the garment and topstitched in gold. On 12 oz
denim that is a pucker no amount of pressing removes.

So the sawtooth is **generated once** by `_sawtooth()` as a real polyline, and
both edges are built from it — the yoke's lower edge walking it one way, the body
panel's upper edge walking the reversed list:

```python
_SAW_PTS_DOWN = _sawtooth(SAW_X_FROM, SAW_X_TO, YOKE_Y, TOOTH_D, N_TEETH, True)
_SAW_PTS_UP   = list(reversed(_SAW_PTS_DOWN))
```

Their seam lengths are therefore equal **by construction**, not by arithmetic.
`declare_seam` checks both yoke seams at `tol=0.3` — far tighter than any seam
needs — precisely so it goes red the day somebody redrafts one side by formula
instead of from the shared generator.

### 2. The tooth depth, clamped twice

```
tooth_depth_requested_mm : 34.00
tooth_depth_clamped_mm   : 34.00
tooth_depth_was_clamped  : false     (true at the parameter extremes)
```

`TOOTH_D ≤ min(yoke_drop × 0.55, (YOKE_Y − UNDERARM_Y) × 0.60)`. A tooth deeper
than the yoke cuts the yoke through; a tooth deeper than the space above the
underarm runs the sawtooth into the armscye. Either produces an inverted outline
— which the kernel CCW-normalizes and `area()` reports as positive, so it renders
and passes `verify()` looking entirely healthy. It is caught here instead, and the
clamp is reported.

### 3. The snap column, pitched over a MEASURED run

```
placket_edge_measured_mm : 644.00
cf_snap_run_mm           : 610.00
snap_pitch_requested_mm  :  95.000
snap_pitch_solved_mm     :  91.167    (6 intervals, 7 snaps)
```

The placket edge is measured off the built front — it is two segments, the CF run
and the turn onto the hem, and only the vertical run carries snaps. Whole
intervals are then fitted across what remains after both clearances (the yoke
seam at the top, the hem turn at the bottom) and the pitch recomputed. A snap
cannot be nudged the way a button can: the stud has to land on the socket.

### 4. The sleeve cap, bisected against a MEASURED armscye

The yoke split each armhole into two edges, so one armscye ring is four measured
edges: front body + front yoke + back body + back yoke.

```
armscye_measured_mm  : 459.45
cap_ease_mm          :  18.00
cap_target_mm        : 477.45
half_biceps_solved_mm: 212.10
```

The **half-biceps** is bisected (not the cap height) until the measured cap equals
the target, which keeps the cap height at its drafted proportion of the armhole
depth rather than letting the solver distort it.

## Denim-family conventions

Carried from `jeans-5-pocket`, `denim-jacket` and `bib-overalls`:

- **7 mm twin-needle topstitch gauge** throughout — both sawtooth yoke seams (the
  topstitch traces follow the generated polyline exactly, offset by the gauge),
  the placket box, and both cuffs.
- **Flat-felled side, armhole and underarm seams** at `seam_allowance + 6 mm`.
- **Every hard good is a Yantra4D reference**, never re-implemented here.
- **Two spools of topstitch thread** in the BOM. A western shirt is mostly
  topstitch.

## Construction notes

- **Sew the yokes before anything else**, and topstitch each sawtooth seam
  immediately. Clip into every inner corner of the V to the stitch line, not past
  it — that clip is what lets the point turn.
- **Interface both placket edges and both cuffs.** A sew-on snap through unbacked
  denim works its own hole open over a season.
- **The yoke is drafted single-layer.** Real western shirts double it; cut the
  yokes twice and treat the second as an inside facing.
- **The sleeve's hem pleats** (two marked fold lines, 26 mm apart) take the
  difference between the sleeve's flat hem and the cuff opening. The placket slit
  is marked, not drafted as a separate piece.
- **A lighter denim suits this shirt.** The draft is unchanged at 8–10 oz or in
  chambray; only the hand changes. 12 oz makes a jacket-weight shirt.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-on-snap` solid, **dimensionally**.
The snap's `snap_dia` — the parameter driving its `sew_face` flange, i.e. the
sewn mating face — is fed from this garment's `snap_diameter`, which is also a
parameter of the garment's own `snap_placket` interface. The same number sizes
the snap, the placket it runs on, and every drilled snap mark on the cuffs.
`stud_dia` and `engage_clear` scale from it too.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/denim-western-shirt/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `front_yoke`,
`back_yoke`, `sleeve`, `cuff`. Presets: `classic-three-point`,
`single-v-workwear`, `showman-six-point`.

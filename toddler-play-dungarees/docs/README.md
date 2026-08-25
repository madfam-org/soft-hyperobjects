# Toddler Play Dungarees

**FC-300 #287 · kids_baby · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `overall-buckle`**

Denim dungarees for a child who is still in nappies and already running. The
inseam does not sew shut — it snaps.

## What it is

Five pieces: two mirrored front legs, two mirrored back legs, a bib on the fold,
a crossing strap (cut 2), and a gusset facing (cut 4). The bib fastens with two
sliding overall buckles; the straps cross at the back and are caught in the back
waist. The inseam closes on a run of snaps that carries from one knee, through
the crotch, to the other knee.

## Why it earns its rank

`kids_baby` was the thinnest family in the whole 300-rank catalog. What it was
missing was not another tee — it was the garment a parent actually fights with.

A nappy change on a child in ordinary dungarees means the boots off, the trousers
down, and a toddler flat on their back on whatever floor is available. Snap-gusset
children's wear has solved this for a century. But in the sizes past 18 months —
exactly where it matters most for a late-training child or a disabled one — it is
sold as a specialist adaptive item at a specialist price, if at all. This is the
ordinary version, in hard-wearing denim, with buckles that print at home.

## Child proportion, not a shrunk adult

The block is drafted from child measurements directly (`bodies/child-6y`), and
the toddler-specific proportions are stated in the geometry rather than inherited
from an adult draft:

- **No waist indentation.** `QUARTER_WAIST` is the hip quarter less a token
  (14 mm), floored at 90% of it. A toddler has no waist to draft to, and a shaped
  waist produces a garment that will not pass over the hips of the child it was
  measured on.
- **The rise carries a nappy.** `back_rise` is a direct parameter, not a fraction
  of the leg, and the front rise is derived 34 mm shorter — a toddler stands with
  a forward pelvic tilt and the nappy sits behind. The back fork extension is
  correspondingly the deeper of the two (`0.21 × ¼ hip` vs `0.13`).
- **The hip is measured over the nappy**, and the manifest warns if it comes in
  under the chest, because that is almost always a mis-measurement.
- **The bib comes from the chest**, not from a fashion proportion — and is then
  clamped against the waist it sews to.
- **The hem is deep on purpose** (30 mm default, up to 50) so the turn-up is let
  down as the child grows.

## What is actually solved (not assumed)

Both hard problems here are **register** problems.

### 1. The snap gusset, pitched across a MEASURED three-run opening

The snapped opening is not one seam. It is the left inseam, the crotch curve, and
the right inseam, end to end. So all three are measured off the built pieces:

```
gusset_inseam_run_mm : 155.46   (each side)
gusset_crotch_run_mm : 154.09
gusset_run_total_mm  : 465.00
```

The requested pitch is then a **target, never a result**. Whole intervals are
fitted across the run less both end clearances, and the pitch is recomputed:

```
snap_pitch_requested_mm : 40.000
snap_pitch_solved_mm    : 39.318    (11 intervals, 12 snaps)
```

Without that recomputation the column drifts and the last snap lands in the
**crotch seam allowance** — the one place a toddler's entire weight rests when
they sit down without looking.

### 2. The two inseams closed to zero

The snap column runs down the inseam, so both inseams must measure the same to
well under a millimetre or every snap after the first is out of register. The
back inseam is drafted plain; the front inseam's **bulge is bisected** until it
measures the back's:

```
front_inseam_bulge       : 0.33723
front_inseam_measured_mm : 282.65
back_inseam_measured_mm  : 282.65
inseam_delta_mm          : 0.0
```

`declare_seam` then checks the pair at `tol=0.4` — far tighter than a normal
trouser inseam, because on an ordinary trouser this error is a twist and here it
is a garment that will not close.

### 3. The strap cut to a MEASURED path, with the buckle's travel centred on it

The strap runs bib corner → over the shoulder → across to the opposite back
waist. That path is derived, not entered:

```
strap_path_measured_mm : 566.40   (bib_height + back_rise + shoulder arc)
buckle_travel_mm       :  90.62   (16% of the path, floored at 45 mm)
strap_cut_length       : 681.02
```

An overall buckle slides, but only ± its own travel. A strap cut to a guessed
length runs out of adjustment on a growing child inside one season — which is the
entire reason the buckle is on the garment. The travel is drawn on the strap as a
real marked span (`buckle travel`, with a `nominal buckle position` across it) so
the maker can see the adjustment the child actually gets.

### 4. The bib clamped against its own seam

```
bib_half_requested_mm : 111.33     (chest / 6 + 8)
bib_half_clamped_mm   : 111.33
bib_half_was_clamped  : false      (true at the parameter extremes)
```

The clamp is `BIB_HALF ≤ QUARTER_WAIST − 12`. A bib wider than the waist it is
sewn to is a piece that pleats itself shut, and — because the kernel
CCW-normalizes an inverted outline and `area()` takes an absolute value — such a
piece passes `verify()` looking healthy. Every derived dimension in this cartridge
is clamped for that reason, and every one of them is rendered at the min *and* max
of every parameter as part of the build check.

## Construction notes

- **The facing is the registration jig.** It is cut to the *measured* gusset run
  with all 12 snap centres already drilled on its centreline, plus marks for
  where the crotch run starts and ends. Mark both sides of the opening from the
  facing, not from a ruler.
- **Cut four facings.** One behind each side of the opening on each leg. A snap
  set through a single layer of denim tears out at the crotch.
- **Bar-tack both gusset stops.** The `gusset stop` notch on each inseam is
  derived from `gusset_extent`; that is where the opening ends and where it will
  tear if it is not tacked.
- **Twin-needle topstitch at 7 mm** on out-seams, the bib edge, and both strap
  edges. The strap is folded in thirds (two marked fold lines) and topstitched
  down both sides — that is what keeps it stiff enough to stay on a small
  shoulder.
- **The straps cross.** The `strap catch` drill mark on the back leg is set in
  from the side seam for exactly that: crossed straps stay on a toddler, parallel
  ones slide off.
- **Knee patches.** The front leg carries a marked knee-patch zone. A toddler
  wears through the knee long before anything else fails.
- **Wash the denim before cutting.** 12 oz mezclilla shrinks, and this garment is
  on a child who outgrows it before it wears out.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `overall-buckle` solid,
**dimensionally**. The buckle's `strap_w` — the parameter driving its `strap_slot`
flange, i.e. the sewn mating slot — is fed from this garment's `strap_width`,
which is also a parameter of the garment's own `bib_strap_buckle` interface. One
number sizes the slot and the strap that runs through it. `frame_h`, `wire_t` and
the catch `button_dia` are derived from the same strap width, so the whole
fastener scales with the garment rather than being a fixed part with a garment
built around it.

The gusset snaps are a *second* finding: they are marked (drill crosses on the
facing, sized off `snap_diameter`) and counted in the BOM, but not modelled here
— the hard-goods rule is one bridged solid per notion.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/toddler-play-dungarees/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front_leg`, `back_leg`, `bib`, `strap`,
`facing`. Presets: `eighteen-months`, `three-years`,
`six-years-out-of-nappies`. Body preset reference: `bodies/child-6y`.

# Kids School Pinafore

**FC-300 #288 · kids_baby · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `shank-button-solid`**

The school jumper worn over a shirt, with shoulder straps that **button** instead
of sewing shut — and a ladder of buttonholes so the same garment is let out three
or four times.

## What it is

Four pieces: a bodice front and a bodice back, both cut on the fold; an A-line
skirt panel cut twice on the fold; and a shoulder strap cut twice. The straps are
caught in the back bib and button to the front bib. Each strap carries the growth
ladder.

## Why it earns its rank

`kids_baby` was the thinnest family in the 300-rank catalog, and school uniform is
the most compulsory clothing purchase there is — repeated every year, and the
single clothing cost that most reliably pushes a household toward uniform-exchange
schemes.

Children outgrow a pinafore's **length** years before its width. That is why the
buttoned shoulder existed for most of the twentieth century, and why it was
quietly dropped when uniform moved to annual replacement. This pattern puts it
back: a ladder of buttonholes plus a deep let-down hem gives two to three years
from one garment, and the buttons print at home.

## Child proportion, not a shrunk adult

Drafted from child measurements directly (`bodies/child-6y`):

- **No bust shaping at all.** No dart, no princess seam. Not a simplification —
  on a school-age child there is nothing there to shape, and drafting one puts a
  fold in the front of a flat chest.
- **Shallow waist suppression.** `QUARTER_WAIST` comes from the waist measurement
  but is floored at **86% of the chest quarter**. A school-age child's waist is
  only slightly under the chest, and a pinafore drafted narrower than that will
  not pull on over the head — there is no closure to open.
- **The ease is a shirt allowance.** 110 mm total by default, and the armhole is
  cut generously to clear a sleeve, because this garment is never worn next to
  the skin.
- **The hem is deep** (40 mm default, up to 70) to be let down *on top of* the
  ladder's adjustment.

## What is actually solved (not assumed)

### 1. The growth ladder, pitched across a DERIVED span

The whole point of the garment. The growth range the ladder must cover is derived
from the bodice height (`max(30, BH × 0.55)`), not picked — a small pinafore gets
a short ladder and a large one a long ladder. Whole intervals are then fitted
across that span and the pitch recomputed:

```
growth_span_mm        : 99.00
rungs_requested       : 4
rungs_solved          : 4
rung_pitch_requested  : 22.000
rung_pitch_solved_mm  : 33.000
ladder_bound_by       : count
```

The requested rung *count* and the requested *pitch* are both upper bounds;
whichever binds first wins, and `ladder_bound_by` reports which one did. A ladder
pitched blind runs its last rung into the strap's own turning — a buttonhole that
cannot be cut.

Each rung is drawn as a real slot at the button's diameter **plus 2 mm**
(`15.24 + 2 = 17.24 mm` at defaults). A buttonhole cut to the button's own
diameter will not pass it.

### 2. The pleat depth, solved against a MEASURED waist

An A-line skirt's top edge is **not** the waist measurement — it is whatever the
flare made it. The skirt top is drafted at the hip quarter, measured, and the
pleat depth solved so the pleated edge equals the bodice's measured waist:

```
skirt_top_half_mm : 197.50
pleat_takeup_mm   :  25.00
pleat_count       :   3
pleat_depth_mm    :   4.167     (a knife pleat eats twice its depth)
```

`PLEAT_TAKEUP` is floored at zero. A flare small enough to leave nothing to pleat
is a legitimate setting (a plain A-line pinafore); a *negative* take-up would be
drawn as a pleat folding backwards — geometry that renders, and lies.

`declare_seam` checks the skirt top against the bodice waist with the take-up as
declared ease, landing at delta = 0. That check goes red the day the pleat solve
stops agreeing with the drafted flare.

### 3. The armhole and the bib, clamped

```
armhole_depth_requested_mm : 86.25
armhole_depth_clamped_mm   : 86.25
armhole_was_clamped        : false      (true at the parameter extremes)
bib_half_requested_mm      : 78.75
bib_half_clamped_mm        : 78.75
```

`AH_DEPTH ≤ BH − 34`, because a child's torso is short enough that a
chest-scaled armhole reaches past the waist seam at the small end of the range.
`BIB_HALF` is clamped **both ways** — floored against the strap it must carry, and
capped against the waist below it. The kernel CCW-normalizes an inverted outline
and `area()` takes an absolute value, so an unclamped piece that turns itself
inside out passes `verify()` looking healthy; every derived dimension here is
clamped, and the cartridge is rendered at the min *and* max of every parameter as
part of the build check.

### 4. The side seam that the raised back bib nearly broke

The back bib sits higher than the front (it carries the strap's fixed end, so it
needs no button clearance). Dropping the armhole from each panel's *own* top made
the back side seam exactly that much longer than the front's — caught by
`declare_seam` on the first render. The underarm is now measured off the **front**
bib line on both panels, and the extra height is absorbed by the back armhole's
curve instead. `BACK_BIB_RISE` is itself clamped against the armhole depth, so
there is always curve left to absorb it.

## Construction notes

- **Interface every rung.** A buttonhole in 115 gsm poplin with nothing behind it
  frays open inside a term. Fusible goes behind the whole ladder and both bib
  tops.
- **Work the ladder from the button end back.** The strap is cut to the *longest*
  setting; the shortest simply leaves strap unused inside. Cutting to the
  shortest setting is the classic error — it makes the ladder decorative.
- **Bar-tack the back end of each strap** where it is caught in the bib seam.
  That is the join a child gets lifted by.
- **A shank button, not a sew-through.** The strap has to move on the button each
  time the ladder is let out; a sew-through sits flat and binds.
- **The `growth span` mark** on the strap shows the adjustment the child actually
  gets, so a parent can see it before the first wearing rather than discovering
  it at the end of a year.
- **Wash the poplin before cutting** — 2.5% warp shrinkage, and this garment is
  washed weekly for years.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `shank-button-solid`. The solid's
`diameter_mm` is fed from this garment's `button_ligne` on the standard
0.635 mm-per-ligne conversion, and `button_ligne` is also a parameter of the
garment's own `strap_growth_ladder` interface — the same number sizes the button
and every buttonhole slot in the ladder. `thickness`, `hole_dia` and `rim` scale
from the same ligne size, so the button is proportioned to the garment rather
than being a fixed part with a garment built around it.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/kids-school-pinafore/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `bodice_front`, `bodice_back`, `skirt`,
`strap`. Presets: `reception-4y`, `year-two-6y`, `year-five-long-ladder`.
Body preset reference: `bodies/child-6y`.

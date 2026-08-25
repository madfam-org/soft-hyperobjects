# Raglan Knit Pullover

The other knit body architecture: no shoulder seam, no armhole, one diagonal per side.

## Provenance

The raglan is named for FitzRoy Somerset, 1st Baron Raglan, whose coat was cut this way
after he lost an arm at Waterloo — the story is usually told as a tailoring anecdote,
but the shape survived for a structural reason rather than a sentimental one. A sleeve
that runs all the way to the neck moves with the shoulder instead of pivoting against a
fixed armhole, which is why the raglan ended up on sweatshirts, baseball shirts,
outerwear and, above all, on sweaters.

For knitting it is more than convenient, it is native. A set-in armhole is a curve, and
a curve in a knitted fabric has to be either cut (and then it unravels and must be
overlocked) or approximated by a stepped bind-off. A raglan seam is a **straight line**,
and a straight line is exactly what a paired decrease worked every *n* rows produces.
The raglan is therefore the architecture that lets a garment be *shaped* on the needles
or the machine rather than shaped by scissors — that is why nearly every top-down
sweater pattern ever written is a raglan.

## Why this earns a commons rank

The commons already holds three cut-and-sew knits on the set-in block —
`crewneck-sweater`, `turtleneck-sweater`, `cardigan`. All three are the *same*
architecture with different necklines. This cartridge is the first of the **other**
architecture, and holding both is the point: the choice between set-in and raglan is a
real constructional fork with different fit behaviour, different tooling and different
skill requirements, not a styling checkbox.

It is also the most forgiving sweater there is. There is no shoulder seam to fit and no
armhole curve to match, so one draft covers a much wider range of bodies than a set-in
block does, and a beginner can actually finish it. That is why the raglan dominates
charity and relief knitting patterns.

## Construction notes

Six pieces: **front** and **back** (each cut 1 on the centre fold), the **sleeve** (cut
2, mirrored), and three ribs — **neckband**, **cuff** (cut 2) and **hem band**.

**The raglan is what solves.** The body's raglan and the sleeve's raglan are drafted as
*congruent right triangles*: the same rise and the same run. The rise is the raglan
depth less that panel's neck drop; the run is the neck span (quarter width less half
neck width) less whatever share `neck_share` gives the sleeve heads. The sleeve is then
drafted **from** those two numbers rather than guessed at, so all four raglan seams
balance to **delta 0.0 with zero declared ease** at every parameter combination. No
tolerance is loosened to absorb a mismatch anywhere in this cartridge.

**The neckline is the raglan's terminus.** On a raglan the neck opening is not an
independent curve that happens to meet the seam — it *is* the top end of the four
raglan seams plus the two sleeve heads. The body's neck edge is therefore drafted to
land exactly on the raglan's neck point, and the neckband is measured around the whole
six-edge circuit (both bodies and both sleeve heads), not around the body alone.

**Negative ease is the sign convention.** `knit_ease` is **signed** and defaults to
**−60 mm**: the draft is *smaller* than the measured chest and stretches onto the body.
This is the opposite of every woven block in the commons, where ease is added. Setting
it positive gives a genuinely oversized sweater; the drafted girth is floored at 520 mm
so the deepest negative ease cannot produce something unwearable.

**The full-fashioned ladder is drawn, not implied.** Both the body and the sleeve carry
a marked decrease ladder along each raglan line — one tick every `fashion_rows` of rise,
set `fashion_step` in from the seam. A knitter works those; a sewer ignores them and
cuts the diagonal. The same cartridge serves both, which is the point of marking them.

**The biceps is solved, not assumed.** A raglan sleeve is genuinely wider at the biceps
than a set-in one, because the sleeve has swallowed the shoulder and must contain the
whole raglan run plus a real sleeve head. The draft solves it as `run + head` and only
falls back to the anatomical estimate when that is already wider.

## The clamps, and why they are load-bearing

Every dimension named above is *derived*, and a derived dimension that goes negative
does **not** fail loudly. It inverts the piece, and the kernel's CCW normalization then
hands `verify()` an outline that looks perfectly valid. So each one carries an explicit
floor, applied **before any point is built**:

| Derived quantity | Floor | What it prevents |
| :-- | --: | :-- |
| raglan rise (front and back) | 90 mm | a short body with a deep front neck inverting the panel |
| neck span (quarter width − half neck) | 50 mm | a wide neck on a narrow body collapsing the run |
| raglan run | 35 mm | a vertical "raglan" and an unsewable neckline |
| sleeve head half-width | 22 mm | a sleeve head degenerating to a point |
| biceps half-width | run + head | a sleeve too narrow to contain its own raglan |
| decrease ladder ticks | 40 | a fine row gauge asking for thousands of marks |
| drafted chest girth | 520 mm | maximum negative ease producing an unwearable draft |

`metadata.solved` reports which floors actually bit on any given render, so a clamped
draft is visible rather than silent. The cartridge was probed at the min **and** max of
every one of its 16 parameters, at all-min, all-max and two mixed-extreme combinations,
and at each `target_piece` — 43 renders, all with zero error issues and every declared
seam balancing.

## Hardware

**None.** A pullover raglan has no closure at all — that is the shape. This cartridge
declares no `notion.hardware_ref`, which is the honest answer rather than an invented
bridge.

## Honest simplifications

- This is the **cut-and-sew** branch. The ladder is *marked*, but the cartridge emits a
  cutting pattern, not a Knitout machine program. A fully machine-knitted version is
  future work, and it is the version the marked ladder is really for.
- The rib bands are drafted as straight double-height strips folded in half, which is
  what is normally cut. A shaped neckband sits slightly better on a deep stand.
- Row and stitch gauge are not modelled. `fashion_rows` is expressed in **millimetres of
  rise** between decreases rather than in rows, because the kernel is dimensional and
  has no gauge concept; a knitter converts once via their swatch.
- No sleeve or body taper is drafted below the biceps beyond the straight underarm line
  into the cuff. Real sweaters often carry a waist shaping; here that would duplicate
  the ladder mechanism without adding a new idea.

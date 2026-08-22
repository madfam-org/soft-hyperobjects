# Cavalier Cloak

**FC-300 · Costume & historical · c. 1620–1660**

The short circular half-cloak of the 17th century, drafted on period construction logic.

## What it is

The half-cloak worn slung from one shoulder — the garment that gives the "cavalier" its
outline. It hangs open at the front and is thrown back over one shoulder, which is why it
is a *half*-cloak rather than a full circle, and why its front edges are faced rather than
merely turned: the underside is on show most of the time it is worn.

It is a garment of **pure geometry**. Nothing about it is eased, gathered, or fitted. A
sector of an annulus, a collar, two facings, one clasp.

| | Cavalier cloak (this) | The costume-shop cape |
|---|---|---|
| Cut | **a sector of an annulus** | a rectangle gathered at the neck |
| How it falls | soft rolling folds of its own weight | stiff pleats standing away at the neck |
| Neck radius | **derived** from neck run ÷ sweep | picked to look right |
| Fastening | **one clasp** at the throat | buttons down the front |

The difference between the first two rows is visible the moment the garment is worn, and
it is the single thing that separates the two.

## Why it earns a commons rank

This is the clearest case in the whole costume family where the garment is decided by
**one piece of arithmetic**, and nothing downstream can rescue a wrong answer. There is no
easing to absorb an error, no dart to redistribute it, no fitting to correct it.

The neck radius is not a design choice:

```
inner arc = r × θ        so        r = neck_run ÷ θ
```

Publishing that as a *derived, measured, and reported* quantity rather than a number
picked to look right on the page is what makes the cut teachable.

## Construction notes

### The arithmetic is proved, not trusted

The cartridge computes `r` from the neck run and the requested sweep, builds the inner arc
as a real polyline at that radius, then **measures it back off the built curve** and
reports the residual against the neck run it is supposed to equal.

At default settings: neck run 446.0 mm, derived inner radius 85.2 mm, measured arc
445.9 mm — residual **−0.124 mm**. That residual is pure polyline discretisation (the arc
is flattened to 64 segments, and a chord is always slightly shorter than its arc); it is
reported rather than rounded away, and it shrinks with a narrower sweep. Reporting it is
how you know the arithmetic is right rather than assuming it.

### The inverse people get wrong by eye

A **wider** sweep gives a **smaller** neck radius, because the same neck run is spread over
more angle — while the hem run grows sharply:

| sweep | inner radius | hem run |
|---|---|---|
| 140° | 133.4 mm | 1254 mm |
| 220° | 116.2 mm | 3364 mm |
| 300° | 85.2 mm | 4424 mm |
| 350° | 105.8 mm* | 8279 mm |

*\* the 350° row is at a larger neck girth and a longer cloak, which is why its radius is
not the smallest — the relationship is with sweep at a fixed neck run.*

Guessing a neck radius that "looks about right" and then choosing a sweep independently is
how a cloak ends up either strangling the wearer or gaping off the shoulders.

### The collar edge is solved, not assumed

The collar's neck edge is drafted as a shallow **curve**, because it is set to a curved
neck edge and a straight band on a curve either ripples at the top or strangles at the
bottom. But a curve is longer than the chord it spans — so setting the collar's half-width
to half the neck arc makes its edge overshoot.

An earlier revision of this cartridge did exactly that and left a **1.6 mm surplus** the
verifier caught. The half-width is now solved by bisection until the built curve *measures*
half the neck arc; the residual is 0.0000 mm.

### The hem allowance is deliberately shallow

A circular hem is cut on **every grain at once**. A deep turned hem on that edge will never
lie flat, so it is turned narrowly or faced. The `hem` allowance is set well below the
garment's seam allowance for that reason, not by oversight.

### Cloth and nesting

A circular sector nests **terribly**, and the BOM says so: the marker estimate assumes only
a 55% yield, well below the other cartridges in this wave. That low number is the honest
cost of the cut, and it is exactly why period cloaks on narrow cloth are seamed at the
centre back.

The cartridge reports the piece's widest span and a `needs_cb_seam_at_1400mm` flag, so a
maker can see *before cutting* whether the cloak will fit their cloth in one piece. At
default settings it does not: the piece spans 1690 mm.

A fulled wool is what makes the folds roll; a thin cloth flutters instead.

## Provenance

This is an original draft built on the documented construction tradition of the
17th-century short cloak: a circular cut of less than a full sweep, hanging open at the
front, with a standing collar set to the neck arc, faced front edges, and a single clasp at
the throat. It is **not** traced from any single extant garment, and it is not a
transcription of any published pattern. The features above are the well-attested general
characteristics of the type, described here as a construction tradition rather than
attributed to a specific source.

The bridged clasp is a modern magnetic one. The period fastening is a hook-and-chain or a
pair of cords, which the BOM notes — the bridge is offered as the openly printable
equivalent, not as a claim of period accuracy for that component.

Anyone working toward museum-grade accuracy should measure an extant garment or consult a
scholarly pattern-drafting source; this cartridge is a faithful working draft of the
*type*, not a reproduction of a particular object.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `cloak` | 1 (or 2 seamed at CB) | the annular sector; CB balance line marked |
| `collar` | 1 on fold | half-width SOLVED against the measured neck arc |
| `facing` | 2 mirrored | cut to the MEASURED front edge |

## Hardware bridge

- `magnetic-clasp` — the single throat clasp; `disc_dia` ← `collar_height × 0.34`

## Fabric

A wool broadcloth or melton is the period cloth. `lana-melton-abrigo` is the closest card
in the Fashion Cabinet material set. A contrast lining is period-plausible and worth doing:
it shows whenever the cloak is thrown back, which is most of the time it is worn.

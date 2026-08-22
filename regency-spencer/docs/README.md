# Regency Spencer

**FC-300 · Costume & historical · c. 1800–1825**

The short high-waisted jacket of the Regency, drafted on period construction logic.

## What it is

A spencer is a garment defined by what it **lacks**: a coat bodice with the skirts cut off
entirely, ending at the Empire waistline directly under the bust. It is worn over a gown of
the same period, and its whole job is to be short enough that the gown's own waistline
continues uninterrupted underneath.

That is not a detail. **A spencer cut to the natural waist is not a spencer** — it is a
short jacket, and it fights the Empire line of the gown it is worn over instead of
completing it. `back_length` is therefore nape to the *high* waist, and the constraint
messages say so.

Two more period markers the draft holds to:

- shaping is taken at the **side and back seams** and by the curve of the underbust edge,
  never by a modern bust dart. The period bodice is small-scale and seamed, and a dart in
  it reads immediately as modern.
- the sleeve is **two-piece** — an upper and a narrower under sleeve — which is what gives
  the period sleeve its forward curve at the elbow. A one-piece sleeve hangs straight and
  is the commonest tell of a modern draft.

It also pairs with `regency-stays` (#267), which is the foundation this is worn over.

## Why it earns a commons rank

The two-piece sleeve is the single technique that most separates a tailored historical
garment from a costume, and it is also the one an automated check is most likely to get
wrong — because **neither of its two caps means anything on its own**. Only their sum sets
into the armscye.

A spencer also takes very little cloth, which makes it one of the few tailored period
garments a beginner can attempt from a remnant. That is exactly how they were often made:
from a good offcut, or cut down from a worn-out gown.

## Construction notes

### The cap is checked as a SUM

```
upper cap  +  under cap   =   armscye  +  ease
```

The armscye is measured off the built body pieces; the **cap height** is then solved by
bisection until that sum measures the target, with both pieces driven from the one solved
height (the under sleeve's cap stays a fixed shallow fraction of the upper's, which is what
lets it sit under the arm). The declared seam is written against the sum of the two caps,
so the verifier checks the relationship that actually matters.

Residual: **0.0000 mm**, across every configuration tested — armscyes from 212.9 mm to
577.1 mm, ease from 0 to 60 mm, under-sleeve shares from 0.20 to 0.45.

**Why height and not curvature.** An earlier revision solved the cap's *bulge* instead. It
hit a wall: the sleeve's width at the biceps is already fixed by the armscye, so at zero
bulge the cap was **already 318.7 mm against a 256.7 mm target**. No curvature could reach
it, and the bisection silently returned its own ceiling — leaving a 62 mm mismatch the
verifier caught. Height is the variable that actually governs the length here. The solver
now also checks both ends of its bracket, so an unreachable target is reported through the
residual rather than hidden behind a returned bound.

### The long sleeve seams must solve too

The upper and under sleeves are seamed to each other down **both** sides, so those edges
are one seam and must be equal. The first revision tapered each piece from its own width to
its own wrist share — different insets, genuinely different lengths, and a **4.2 mm
mismatch on each side**.

Both pieces now share a **single seam profile**: one shared taper, and for the side of the
outline that runs upward the identical curve is *reversed* rather than redrawn. The two
edges are equal by construction. The pieces still differ in width — that is what makes one
the upper and one the under — but the seam that joins them is one seam.

### The collar edge is solved

The collar's neck edge is drafted as a shallow curve, and a curve is longer than the chord
it spans, so a collar cut to half the neck run overshoots the neckline it is sewn to. The
half-width is solved by bisection until the built curve *measures* half the measured neck
run. Residual 0.0000 mm.

(The same trap and the same fix appear in `cavalier-cloak` (#275), where it cost a 1.6 mm
surplus before it was solved.)

### Shoulder seams

Front and back carry different neck widths, so each panel's shoulder-point drop is solved
against a shared reference chosen so the wider-necked panel still has a real solution. Both
shoulder seams measure the same by construction — no degenerate fallback, no widened
tolerance.

### Closure and lining

The period prefers **hooks and eyes** to visible buttons on a woman's spencer. The bridged
`trouser-hook-bar` takes its plate length from `hook_pitch`, which is the dimensional
handshake — the plate has to fit within its own spacing.

A spencer is **fully lined**. It is a tailored garment, and the lining is what makes the
small seamed shaping hold its form.

## Provenance

This is an original draft built on the documented construction tradition of the Regency
spencer: a bodice ending at the high Empire waist, shaping taken at the side and back seams
rather than by darts, a two-piece sleeve giving the forward elbow curve, a small standing
collar, and a front closed with hooks and eyes. It is **not** traced from any single extant
garment, and it is not a transcription of any published pattern. The features above are the
well-attested general characteristics of the type, described here as a construction
tradition rather than attributed to a specific source.

Anyone working toward museum-grade accuracy should measure an extant garment or consult a
scholarly pattern-drafting source; this cartridge is a faithful working draft of the
*type*, not a reproduction of a particular object.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `front` | 2 mirrored | hook stand, the defining underbust curve |
| `back` | 2 mirrored | CB seam; the period back is narrow |
| `upper_sleeve` | 2 mirrored | drafted at the SOLVED cap height; elbow marked |
| `under_sleeve` | 2 mirrored | shallow cap; shares the upper's seam profile |
| `collar` | 1 on fold | half-width SOLVED against the measured neck run |

## Hardware bridge

- `trouser-hook-bar` — the centre-front closure; `plate_len` ← `hook_pitch × 0.45`

## Related cartridges

- `regency-stays` (#267) — the foundation garment this is worn over
- `cavalier-cloak` (#275) — the same solved-collar-curve problem, two centuries earlier

## Fabric

A fine wool, silk, or velvet is the period cloth. `lana-peinada-traje` is the closest card
in the Fashion Cabinet material set. The marker estimate assumes 1200 mm at 74% — a small
garment, and a forgiving one to lay out.

# Edwardian Walking Skirt

**FC-300 · Costume & historical · c. 1900–1910**

The practical gored skirt of the Edwardian decade, drafted on period construction logic.

## What it is

A *walking* skirt is the one cut to clear the ground — ankle length or a little above — as
against the trained or floor-length skirt of the same years. It is the everyday garment of
the period, and it is built from **shaped gores**, not from a rectangle gathered onto a
waistband.

The silhouette is a **progression**: smooth and flat over the front, with the fullness
carried steadily toward the back. That progression is the whole look. A skirt with even
fullness all round reads as a later garment even when everything else about it is right,
which is why `back_fullness` is a first-class parameter and setting it to 1.0 visibly
flattens the period out of the draft.

## Why it earns a commons rank

A gored skirt is a **chain of seams that has to close all the way round the body**, and it
is the classic case where a costume draft passes its own check only because the tolerance
was widened until it stopped complaining.

That is not hypothetical here. An early revision of this cartridge drafted each gore's
side edge from its own waist point to its own hem point — the obvious approach — and left
adjacent-seam mismatches of **30 to 166 mm** depending on the size. The only way to make
that pass was to set the seam tolerance to whatever the mismatch happened to be. Solving
it properly turns a judgement call into a number anyone can check.

## Construction notes

### The gore seam must be COMMON, not merely similar

Two adjacent gores are sewn along **one seam**. Their edges are therefore not two
independent curves that ought to come out close — they are the same seam, and they must be
the same length. The fullness difference between a flat front gore and a full back gore has
to show up as a **wider hem**, never as a longer seam.

The draft solves this in two moves:

1. The common seam length is taken from the **widest** gore. No gore's seam can be shorter
   than the distance it has to span, so the widest one sets the floor.
2. Every narrower gore's **hem line is dropped** by a bisection-solved amount until its own
   side seam measures that same length.

Adjacent gores then meet along equal edges by construction. The reported residual is
`0.00 mm` at every size tested, from a 520 mm waist with one gore pair to a 1250 mm waist
with four.

The dropped hem is also the period behaviour: a gored skirt's hem is **trued after making
up**, precisely because the narrower gores hang differently once the seams are closed.

### The waist closes on the waist

The gores' waist shares sum to `waist_girth` exactly — every gore, the front one included,
is drafted at one half-body share, and the front's fold doubles its drafted piece into a
whole front. An earlier revision let the front's fold count differently from the rest,
which left the measured waist run 87 mm short of the girth it was supposed to fit.

The waistband is then cut to the **measured** sum of the built gores' waist edges plus a
named placket underlap — not to `waist_girth`, because the gores are what the band is
actually sewn to. The underlap is declared as ease in the seam check, so the check compares
like with like rather than being tuned to pass.

The band is drafted with a slight **curve**, not as a straight strip: a straight band on a
body that is smaller at the waist than above and below it will not lie flat.

### The sweep is measured, not claimed

`hem_sweep` is a *target*. The achieved sweep is the **sum of the built gore hems**, and it
is reported separately under `solved.hem_measured_mm` next to the target. The two differ —
at default settings the target is 3000 mm and the measured sweep is 2884.6 mm — because the
flare has to reconcile with the fitted hip and the solved seam length. Reporting both is the
honest thing; quoting the target as though it were the result is not.

### Hem and closure

A walking skirt takes its wear **at the hem**, so the hem allowance is deep and the period
finish is a faced hem, often with a brush braid at the edge. The centre-back placket closes
with **hooks and bars** — not a zip, which does not belong in this decade — and an inside
petersham waist stay carries the skirt's weight so the outer band does not stretch.

The bridged `trouser-hook-bar` solid takes its hook width from `band_height`, because the
hook plate has to sit inside the finished band. That is the dimensional handshake.

## Provenance

This is an original draft built on the documented construction tradition of the Edwardian
walking skirt: a body of shaped gores fitted over the hip and flaring below it, fullness
graded from a flat front to a full back, a shaped waistband over an inside waist stay, and
a centre-back placket closed with hooks and bars. It is **not** traced from any single
extant garment, and it is not a transcription of any published pattern. The features above
are the well-attested general characteristics of the type, described here as a construction
tradition rather than attributed to a specific source.

Anyone working toward museum-grade accuracy should measure an extant garment or consult a
scholarly pattern-drafting source; this cartridge is a faithful working draft of the *type*,
not a reproduction of a particular object.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `front_gore` | 1 on fold | the flattest gore, smooth over the front |
| `side_gore` | 2 per pair, mirrored | drafted at the middle fullness weight |
| `back_gore` | 2 mirrored | the fullest gore; carries the placket and hooks |
| `waistband` | 1 | shaped; cut to the MEASURED waist run plus underlap |

## Hardware bridge

- `trouser-hook-bar` — the centre-back placket; `hook_width` ← `band_height × 0.45`

## Fabric

A firm wool suiting or serge is the period cloth, and it is what makes a gored skirt swing
from the hip instead of clinging — the gores are cut, not gathered, so the cloth does the
work. `lana-peinada-traje` is the closest card in the Fashion Cabinet material set.
Edwardian suiting comes wider than earlier cloth, so the marker estimate assumes 1400 mm at
75%.

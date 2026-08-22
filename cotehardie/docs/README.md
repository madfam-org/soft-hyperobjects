# Cotehardie

**FC-300 · Costume & historical · c. 1340–1400**

The fitted gown of the mid-to-late 14th century, drafted on period construction logic.

## What it is

The cotehardie is the moment European dress stops being a draped tube and becomes
*tailored*. It fits the torso closely — but it does so without a single dart and without
a waist seam, which is exactly the part a modern draft usually gets wrong.

| | Cotehardie (this) | The usual costume shortcut |
|---|---|---|
| Body construction | four panels, **one cut length** shoulder to hem | bodice + skirt joined at the waist |
| Torso shaping | the **shape of the seams themselves** | darts, or a princess seam over a lining |
| Skirt fullness | **gores set into slits** in the body seams | a gathered or A-line skirt sewn on |
| Closure | **side lacing** through worked eyelets | a back zip, or lacing added as decoration |
| Sleeve | close, buttoned elbow to wrist | a set-in sleeve with modern ease |

A bodice sewn to a skirt reads as Victorian-with-a-medieval-trim from any distance where
the seam is visible, and it hangs differently: the gored body carries the skirt's weight
from the shoulder down a continuous grain line, while a waist-seamed gown hangs the
skirt from the waist. That is a difference in drape, not only in authenticity.

## Why it earns a commons rank

The gore is a genuinely non-obvious technique — a triangle inserted into a *slit*, not
into an open seam — and it is the one piece of medieval tailoring knowledge most often
skipped in favour of a modern equivalent. It is also the technique most sensitive to
getting a measurement right: a gore whose sewn side does not match the slit it goes into
either buckles or leaves the slit gaping, and no amount of easing fixes it.

Publishing it parametrically, with the gore's sewn side **measured off the built
triangle** and the body's slit cut to that measurement, keeps the actual technique
legible and fittable to a real body. That matters more for historical dress than for
modern wear, because there is no graded size chart to fall back on.

## Construction notes

### The gore must solve, not approximate

A gore is inserted into a **slit** cut up into a seam, and its two long sides are each
sewn to one lip of that slit. So the slit's depth and the gore's sewn side must be
equal — not approximately, exactly, because there is no ease to distribute:

```
slit depth  =  gore side (measured)
```

The cartridge therefore builds the gore **first**, measures `side_l` off the built
polygon, and only then draws each body panel's side edge with a straight lower run of
exactly that measured length. The gore seam balances by construction rather than by
luck, and the measured value is reported in the explode metadata under
`solved.gore_side_measured_mm`.

The hem sweep is handled the same way: it is **summed from the built panel hems and the
built gore bases**, not computed as `gown_length × some flare factor`. A flare factor
would be a guess that happens to look plausible; the sum is the number you will actually
be hemming.

### Three shoulder seams, one length

The period neckline is not symmetrical between panels — the front scoops lower and
narrower, the back sits higher and wider, the side splits the difference. Each panel's
shoulder edge runs from its own neck point out to the *common* shoulder point, so a
naive draft leaves three shoulder seams of three different lengths. They are sewn to
each other, so that is a real defect.

This draft solves it: a shared `SHOULDER_LEN` is chosen large enough that **every**
panel has a real solution (the panel with the widest neck sets the floor — its shoulder
run alone cannot exceed the shared hypotenuse), and each panel's shoulder-point drop is
then solved as the remaining leg of that right triangle. There is no degenerate fallback
branch and no widened tolerance. An earlier revision of this cartridge derived the
reference from the front panel alone, which left the side panel unsolvable and produced
a genuine 1.0 mm mismatch that the verifier caught.

### The sleeve cap is solved against a measured armscye

The armscye is measured off the built body panels; the sleeve cap's bulge is then found
by bisection until the cap measures the armscye plus a declared ease. Computing both
from formulas and hoping they meet is what leaves a sleeve that will not set in. The
residual is reported under `solved.cap_residual_mm`.

### Lacing and buttons

Side lacing through **worked eyelets** is how a garment with no elastic and no back zip
gets close enough to fit, and it is why the cotehardie can be cut as closely as it is —
the wearer laces into it. The forearm buttons closing the sleeve from elbow to wrist are
the period finish; they are opposed by worked thread loops, not by cut buttonholes.

Hand-worked thread eyelets are the period technique. The bridged `garment-eyelet` solid
is the practical modern equivalent, and its flange diameter is driven from the eyelet
pitch — because a flange wider than the spacing puts neighbouring eyelets into each
other. That is the dimensional handshake: the same number that spaces the garment's
lacing bounds the hardware's sewn face.

## Provenance

This is an original draft built on the documented construction tradition of the
mid-to-late 14th-century fitted gown: a four-panel body with no waist seam, fullness
delivered by gores set into the seams below the hip, side lacing through worked eyelets,
and close forearm-buttoned sleeves. It is **not** traced from any single extant garment,
and it is not a transcription of any published pattern. The features above are the
well-attested general characteristics of the type, described here as a construction
tradition rather than attributed to a specific source.

Anyone working toward museum-grade accuracy should measure an extant garment or consult
a scholarly pattern-drafting source; this cartridge is a faithful working draft of the
*type*, not a reproduction of a particular object.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `front` | 1 on fold | boat neck, gore slit mark |
| `back` | 1 on fold | higher neck, gore slit mark |
| `side` | 2 mirrored | carries the lacing eyelet field |
| `gore` | 4 | built first; its measured side sets every slit |
| `sleeve` | 2 mirrored | solved cap, forearm button field |

## Hardware bridge

- `garment-eyelet` — the side lacing field; `flange_dia` ← `eyelet_pitch × 0.42`

## Fabric

A fulled wool is the period cloth for an outer cotehardie, and it is what makes the
gored hem hang rather than flap; `lana-melton-abrigo` is the closest card in the Fashion
Cabinet material set. Period cloth is narrow, so the marker estimate assumes a narrow
width. The gore seams take the skirt's whole weight — backstitch them by hand or use a
short machine stitch, and finish the allowances.

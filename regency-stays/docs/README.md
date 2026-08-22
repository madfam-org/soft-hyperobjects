# Regency Stays

**FC-300 · Costume & historical · c. 1800–1825**

Long corded stays of the Regency/Empire mode, drafted on period construction logic.

## What it is

Stays — not a corset in the Victorian sense. The distinction is structural, not just
terminological, and it is the whole reason this cartridge exists separately from
`structured-corset`:

| | Regency stays (this) | Victorian corset (`structured-corset`) |
|---|---|---|
| Purpose of the garment | lift and lengthen the torso | reduce and shape the waist |
| Waist suppression | almost none | substantial |
| Source of bust shape | **triangular gussets set into slashes** | shaped panel seams |
| Stiffening | **cording channels**, one back bone per side | spiral and flat steel at every seam |
| Front closure | a single straight busk in a stitched casing | a hinged split busk that opens |
| Waist position | just under the bust | at the natural waist |

Drafting the Regency body as a nipped hourglass is the single most common fancy-dress
error, and it produces the wrong silhouette under an Empire-line gown. This draft takes
the underbust as the base ring and delivers *all* bust and hip fullness through gussets.

## Why it earns a commons rank

Historical costuming keeps a large amount of hard-won construction knowledge alive, and
that knowledge is usually locked inside out-of-print pattern books sold in fixed sizes.
A parametric stay lets a reenactor, a museum workroom, or a student fit the garment to a
real body rather than grading a printed size — which matters more here than in modern
wear, because a foundation garment that does not fit does not do its job at all.

The busk is bridged to an open, printable Yantra4D solid instead of a part to source
from a shrinking supplier list.

## Construction notes

### The gusset is the whole trick

A set-in gusset is not appliquéd. The ground fabric is **slashed**, the slash is
**spread open**, and the triangle's two long sides are sewn to the two sides of the
spread slash. So:

```
gusset sewn length  =  side_l + side_r
slash length        =  (side_l + side_r) / 2
```

because the slash is stitched on *both* of its sides. The cartridge builds the gusset
triangles first, **measures** `side_l` and `side_r` off the built polygons, and only
then cuts the front's slash marks to exactly half that measured total. Nothing is
assumed from a formula, so the set-in seam balances by construction. The measured values
are reported in the explode metadata under `solved`.

Both slash lines are emitted as `kind="trace"` internals — they are cut lines, not
stitch guides, and should be marked and slashed before the gussets go in.

### Cording, not boning

The channels marked on the front are for **cotton cording**, run through after the two
fabric layers are stitched. This is what gives corded stays their shape. Substituting
plastic boning throughout produces a rigid tube with the wrong drape and defeats the
point of the garment. The only rigid elements are one flat bone either side of the back
lacing.

### The busk

The period front busk is a **plain straight slat** of wood, whalebone, or steel, slid
into a stitched casing and removable for laundering. The hinged split busk that opens
down the front is a later Victorian development. The bridged `corset-busk` solid is
therefore driven with `knobs: 0` — used unsplit, as the period requires. Its length is
driven by the stays' own centre-front length, which is the dimensional handshake.

### Lacing

Period backs are **spiral-laced** from the top with a single cord, not criss-crossed
with two ends and a bow. Eyelets are offset accordingly rather than set in facing pairs.
Hand-worked thread eyelets are the period finish; the bridged `garment-eyelet` solid is
the practical modern equivalent.

## Provenance

This is an original draft built on the documented construction tradition of English and
French stays of roughly 1800–1825: a one-piece gusseted front, corded channels, a
straight busk casing, and a spiral-laced back. It is **not** traced from any single
extant garment, and it is not a transcription of any published pattern. The features
above are the well-attested general characteristics of the type, described here as a
construction tradition rather than attributed to a specific source.

Anyone working toward museum-grade accuracy should measure an actual extant garment or
consult a scholarly pattern-drafting source; this cartridge is a faithful working draft
of the *type*, not a reproduction of a particular object.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `front` | 1 on fold | busk casing, cording channels, both slash marks |
| `bust_gusset` | 4 | two per bust |
| `hip_gusset` | 2 | one per side |
| `back` | 2 mirrored | eyelet field + back bone |
| `strap` | 2 mirrored | tied to the front, period-adjustable |

## Hardware bridge

- `corset-busk` — one straight busk, `busk_len` ← `stays_length`
- `garment-eyelet` — the back lacing field (see BOM; the manifest bridges the busk)

## Fabric

Two layers of firm linen or cotton jean, stitched together — the strength is in the
cording, not in a modern fused interlining. `manta-cruda` is the closest card in the
Fashion Cabinet material set. Period cloth is narrow, so the marker estimate assumes
900 mm.

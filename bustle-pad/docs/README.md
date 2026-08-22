# Bustle Pad

**FC-300 · Costume & historical · c. 1870–1875 and c. 1883–1889**

The small stuffed bustle — the soft pad, drafted on period construction logic.

## What it is

The soft pad is the bustle as against the **caged or wired** bustle of the same decades.
It is the version most people actually wore, and the version most useful today: it is
quiet, it packs flat, it does not collapse when you sit on it, and it is the right
understructure for the smaller bustle silhouettes at either end of the bustle era.

The defining feature is that it is a **crescent, not a cushion**: deepest at the centre
back and tapering to *nothing* at the sides. The fullness is held out behind and the hips
stay flat. A pad of even depth all round widens the hips, and no skirt above it can
correct that.

## Why it earns a commons rank

Understructure is the part of historical dress most often faked, precisely because it is
invisible once the skirt is on — and getting it wrong makes every layer above it hang
wrong.

The soft bustle is also the **accessible** one. It needs no cane, no steel, and no
specialist supplier; it is the single cheapest piece of equipment that makes a Victorian
skirt sit correctly, and it can be made out of scrap cloth and wadding. Publishing it
parametrically means the shape can be fitted to a specific body and a specific decade
rather than bought as one size.

## Construction notes

### The gusset must be measured, not calculated

The gusset is what turns two flat crescents into a bag with volume, so its length must
equal the crescent's curved **outer** edge exactly or the bag will not close. That run is
not a formula — the outer edge is a cosine-tapered polyline through the crescent profile.
The cartridge builds the crescent first, **measures** that polyline, and cuts the gusset to
precisely the measured length. Both crescent faces share the one gusset, so the seam is
declared against each face and both balance.

### The two curves are different lengths, and that is the point

A crescent's inner and outer edges have different radii, so the **inner run is shorter
than the outer run** — at default settings, 424.3 mm against 650.8 mm, a difference of
226.6 mm.

That difference *is* the pad's shape. It is also the thing a maker has to ease at the
tips, so both runs are measured and reported under `solved` rather than only the one the
gusset needs. Knowing you are easing 227 mm is the difference between planning the seam
and fighting it.

The inner edge is drafted as a shallow **arc**, not a straight line: the waist is a curve,
and a pad cut with a straight top edge stands away from the body at the sides.

### The channels are structural

The horizontal stitched channels divide the bag into compartments so the stuffing cannot
migrate to the bottom and leave the top empty. That is the difference between a bustle that
keeps its shape and a sagging bag of wool, and it is why the channel stitching is
structural rather than decorative.

Each channel is a **different length** as the crescent tapers — at default settings
369.0, 307.5 and 225.1 mm. They are reported individually rather than batched to one
figure, because cutting them all the same is exactly how the compartmenting stops working
near the tips.

Stuff each compartment **separately and firmly**. A softly stuffed pad flattens under the
skirt's weight within an hour.

### Cloth and closure

A firm, closely woven cotton twill or ticking — a loose weave lets the stuffing beard
through and the pad sheds inside the skirt.

The waist tape is generously long and carries several hooks, because the pad fastens
**over stays** and the waist it fastens at is not the wearer's bare measurement. The
bridged `trouser-hook-bar` takes its plate length from `hook_pitch`, which is the
dimensional handshake — the plate has to fit within its own spacing.

## Provenance

This is an original draft built on the documented construction tradition of the soft
stuffed bustle: a crescent pad deepest at the centre back and tapering at the sides, two
faces joined by a depth gusset, horizontal stitched channels compartmenting the stuffing,
and a waist tape fastening at the front. It is **not** traced from any single extant
garment, and it is not a transcription of any published pattern. The features above are the
well-attested general characteristics of the type, described here as a construction
tradition rather than attributed to a specific source.

Bustle sizes varied enormously across the two decades named above, and the parameters are
offered as a range across that variation rather than as a claim about any particular year.

Anyone working toward museum-grade accuracy should measure an extant garment or consult a
scholarly pattern-drafting source; this cartridge is a faithful working draft of the
*type*, not a reproduction of a particular object.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `crescent` | 2 | the two faces; channels marked at their true graduated lengths |
| `gusset` | 1 | cut to the MEASURED outer run; stuffing opening marked |
| `waist_tape` | 1 | hooks for adjustment over stays |

## Hardware bridge

- `trouser-hook-bar` — the waist tape closure; `plate_len` ← `hook_pitch × 0.6`

## Related cartridges

- `pocket-hoops` (#268) — the same gusseted-bag logic, applied to 18th-century side hoops
- `edwardian-walking-skirt` (#272) — the era after the bustle, where the fullness moves into
  cut gores instead of an understructure

## Fabric

`manta-cruda` is the closest card in the Fashion Cabinet material set. The marker estimate
assumes 900 mm at 70%.

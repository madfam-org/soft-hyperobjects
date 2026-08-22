# Tudor Kirtle

**FC-300 · Costume & historical · c. 1500–1560**

The supportive gown of the 16th century, drafted on period construction logic.

## What it is

The kirtle sits between the smock and the outer gown, and it is the layer that does the
structural work. In the 16th century **bust support comes from the kirtle bodice** — a
stiffened, close-laced body that holds the bust by compression. There is no separate
foundation garment underneath and no bra; drafting one in, or drafting the bodice with
shaped cups, is the standard modern error and it produces the wrong shape.

| | Tudor kirtle (this) | Cotehardie (`cotehardie`) |
|---|---|---|
| Waist | **has a waist seam** — bodice and skirt made separately | no waist seam at all |
| Skirt fullness | a **rectangle**, controlled by cartridge pleats | **gores** set into seam slits |
| Bust support | the bodice, stiffened and laced | the close cut and side lacing |
| Bodice stiffening | **filled boning channels** | none — shaped seams only |

The two garments answer the same problem from opposite directions, roughly two centuries
apart, and the difference between them is exactly the waist seam. That is why they are
separate cartridges rather than presets of one.

## Why it earns a commons rank

Cartridge pleating is a **length problem**, and it is the part a costume draft can get
provably wrong. It is also the part most often fudged: pick a fullness ratio that sounds
right — "three times the waist" — cut the rectangle, and discover at the fitting that the
pleats either will not go onto the bodice or sit slack.

Solving it against a measured waist turns a rule of thumb into a number, for whatever
body the wearer actually has. That matters more here than in modern wear, because
historical dress has no graded size chart to fall back on.

## Construction notes

### The pleating must solve

The skirt is a flat rectangle. Pleated up, it must reduce to exactly the bodice's waist
run. Each cartridge pleat consumes `pleat_pitch` of flat fabric and occupies
`pleat_takeup` of finished waist, so:

```
pleats that fit   =  floor(flat_width / pleat_pitch)
pleated length    =  pleats * pleat_takeup      # must equal the measured waist
```

The cartridge builds the **bodice first**, measures its waist edge off the built polygons
(two front halves plus two backs — the front is cut on the fold, so its waist edge is
half the front), and then **solves the skirt's flat width by bisection** so the pleated
length matches that measured run.

The pleat count is an integer — a half pleat is not a thing you can sew — so the
continuous solve lands between two whole-pleat widths. The draft takes whichever whole
count pleats up **closest** to the measured waist, rather than always rounding one way.
The residual is then at worst half a pleat's take-up, it is **reported** in the explode
metadata under `solved.pleat_residual_mm`, and it is eased in at the centre back the way
a period skirt is. Reported residuals across the tested size range run from 0.0 mm to
3.0 mm.

`pleat_takeup` is clamped below `pleat_pitch` (at 0.75 of it): a pleat cannot take up
more waist than the flat fabric it consumes, and allowing that would produce a fullness
ratio below 1 — a skirt narrower than the waist it mounts to. There is a further guard
that widens the skirt by whole pleat pitches if an extreme parameter combination would
still land under the waist run, so the piece stays cuttable at every setting.

### Cartridge pleats, not gathers

Cartridge (organ-pipe) pleats are gathered over a stiff roll on **two or three parallel
rows of running stitch**, so each pleat stands out from the waist as a tube. This is why
a Tudor skirt springs away from the body at the waist. A skirt gathered flat onto a
waistband reads as a much later garment, and it also hangs differently — the tubes carry
the skirt's weight outward, which is what supports the silhouette.

The gathering rows and every pleat fold are emitted as internals at the true pitch. The
deep hem allowance is not decorative: it weights the pleats down so they hang as tubes
rather than collapsing.

A firm wool holds the pleats standing; a soft cloth lets them flatten, which defeats the
technique.

### Boning is filled, not topstitched

The marked channels are for **filled** stiffening — whalebone, reed, or bundled cord.
The bodice supports the bust by compression, so an unfilled channel is decorative
topstitching and does nothing. The bodice is deliberately drafted **under** the body
measure for the same reason: the reduction is the garment's function, not a drafting
error.

### Lacing

The period back is **spiral-laced** from the top with a single cord, not criss-crossed
with two ends and a bow, and it is laced with a **visible gap** between the edges rather
than closed edge to edge — `lacing_gap` is that gap, and it comes off each back half.
Hand-worked thread eyelets are the period finish; the bridged `garment-eyelet` solid is
the practical modern equivalent, with its flange diameter driven from the eyelet pitch,
because a flange wider than the spacing puts neighbouring eyelets into each other. That
is the dimensional handshake.

## Provenance

This is an original draft built on the documented construction tradition of the
16th-century kirtle: a stiffened, laced bodice supporting the bust by compression, a
separate rectangular skirt joined at a waist seam and controlled by cartridge pleats, and
spiral lacing through worked eyelets. It is **not** traced from any single extant
garment, and it is not a transcription of any published pattern. The features above are
the well-attested general characteristics of the type, described here as a construction
tradition rather than attributed to a specific source.

Anyone working toward museum-grade accuracy should measure an extant garment or consult a
scholarly pattern-drafting source; this cartridge is a faithful working draft of the
*type*, not a reproduction of a particular object.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `bodice_front` | 1 on fold | filled boning channels |
| `bodice_back` | 2 mirrored | boning + the lacing eyelet field |
| `skirt` | 2 | width SOLVED against the measured waist; pleat folds marked |
| `strap` | 2 mirrored | tied or pinned to the front, period-adjustable |

## Hardware bridge

- `garment-eyelet` — the back lacing field; `flange_dia` ← `eyelet_pitch × 0.40`

## Fabric

A firm worsted wool is the period cloth and it is what makes the cartridge pleats stand;
`lana-peinada-traje` is the closest card in the Fashion Cabinet material set. The marker
estimate assumes a 1000 mm width at 72%.

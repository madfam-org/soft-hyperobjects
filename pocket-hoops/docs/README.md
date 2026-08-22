# Pocket Hoops

**FC-300 · Costume & historical · c. 1740–1770**

Paired side hoops (small panniers) — the understructure that gives a mid-18th-century
gown its width.

## What it is

Two separate baskets, one tied at each hip, joined only by a shared waist tape. That
separateness is the definition. A farthingale or a bell hoop is a single continuous cage
that pushes the skirt out in every direction; pocket hoops push it out **sideways only**,
leaving the front and back of the gown nearly flat.

That flatness is not a limitation — it is the period silhouette. A gown built over a
round hoop reads as the wrong century no matter how correct the bodice is. It is also
why the front of a robe à la française can carry a flat decorated stomacher and a
flat-fronted petticoat at all.

They are called *pocket* hoops because the inner face is left open at the top and used
as a genuine pocket. This cartridge marks that opening (`pocket-mouth`) rather than
stitching the bag closed.

## Why it earns a commons rank

Understructure is the most-faked part of historical dress, precisely because it is
invisible once the gown is on. The consequence is that every layer above it hangs wrong.

Two things here are hard to get from a bought cage:

1. **Fit to a real body.** Hoop width, depth, drop, and waist are all parametric.
2. **The stays are not all the same length.** As the bag widens downward, every casing
   is a different length. Commercial kits often ship one length; this cartridge measures
   and reports each casing individually in `metadata.solved.casing_lengths_mm`.

## Construction notes

### The gusset is the seam that must solve

Two flat side panels do not make a bag. The **gusset** — a strip `hoop_depth` wide sewn
all the way around the curved outer edge — is what gives the hoop its thickness. Its
length must equal the panel's curved outer run *exactly*, or the bag simply will not
close.

That run is a flaring curve, not a straight line, so it has no closed-form length worth
trusting. The cartridge:

1. drafts the outer edge as a 24-segment polyline through the hip flare,
2. **measures** that polyline off the built piece,
3. cuts the gusset to precisely that measured length.

Both side panels of a hoop share the one gusset, so the seam is declared against each.
Both check at 1 mm tolerance and match exactly.

The flare is eased (`1 - (1-t)^2.2`), so most of the width is gained in the upper third
and the hoop then carries almost straight down. A linear flare gives a cone, which is
the wrong shape.

### Graduated stays

Casings run horizontally across the side panels at even height intervals. Each is
marked at its own true width. Cut each stay to its own casing — do not batch one length
and trim, because the top stays need to be genuinely shorter for the hoop to taper
correctly toward the waist.

Period stock is **cane or whalebone**. The bridged `boning-stay` solid is the open
printable equivalent; cane is closer to period and behaves better, if you can get it.

The `stay-crossing` marks on the gusset let the stays continue around the outer edge, so
the hoop is a continuous stiffened ring rather than two stiff faces flapping against a
soft strip.

### The shared tape

One tape carries both hoops and ties around the waist **over the stays**. This is why
`waist_girth` should be measured over the corset, not on the bare body. Tying rather
than hooking means the hoops can be shed independently — which is how they were
actually worn.

## Provenance

An original draft built on the documented construction tradition of mid-18th-century
side hoops: paired gusseted bags on a shared waist tape, graduated horizontal stay
casings, and an open inner face used as a pocket. It is **not** traced from any single
extant garment and is not a transcription of any published pattern.

The features described are the well-attested general characteristics of the type. For
museum-grade accuracy, measure an extant garment or consult a scholarly pattern source;
this is a faithful working draft of the *type*.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `side_panel` | 4, mirrored | 2 per hoop; casings + pocket mouth marked |
| `gusset` | 2 | one per hoop, cut to the measured outer run |
| `waist_tape` | 1 | carries both hoops, ties at the waist |

## Hardware bridge

`boning-stay` — `stay_length` ← `hoop_width`, `channel_wall` ← `hoop_depth`.

## Fabric

Firm plain-weave linen or striped cotton ticking, unlined. `manta-cruda` is the closest
card in the material set. Period cloth is narrow, so the marker estimate assumes 900 mm.

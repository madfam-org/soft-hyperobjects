# Sarafan (сарафан)

A long trapezoidal pinafore-dress worn **over** a shift (рубаха, *rubakha*), suspended
from two shoulder straps and hanging free from a narrow band above the bust.

## Provenance

The sarafan is the characteristic dress of Russian women across the North, the Volga
basin and much of Great Russia from roughly the 16th century into the early 20th, and
it remains living dress in folk-ensemble and village practice today. It is an
**over**-garment: it is not worn against the skin, and the sleeves and collar visible
in most photographs belong to the *rubakha* beneath it, not to the sarafan itself. A
sarafan drafted with sleeves attached would be a costume, not a sarafan.

Two broad constructional families exist. The older **косоклинный** (*kosoklinny*,
"oblique-gore") sarafan is built from a straight centre panel with wedge gores set into
the sides, producing a strongly flared cone. The later and far more widespread
**прямой** (*pryamoy*, "straight") sarafan — the one this cartridge drafts — is made
from straight loom-widths gathered into a narrow chest band.

**Why the straight form only.** The oblique-gore cut is not a style choice that scales;
its gores are struck to a *specific historical loom width*, and the wedge angles are a
consequence of that width. Parameterising it would mean inventing gore angles that no
tradition used. Drafting the straight sarafan is the honest option: it is the common
form, and its geometry genuinely does generalise.

Regional sarafans carry meaningful ornament — embroidery bands, braid (*позумент*),
and printed motifs whose placement and colour signal region, marital status and
occasion. This cartridge drafts **construction only** and marks no ornament. Ornament
belongs to the maker and to the tradition it comes from, not to a parametric default.

## Why this earns a commons rank

The sarafan is a working answer to a problem the commons cares about: fitting a wide
range of bodies from one pattern with almost no cloth waste. Because it fits by
**gathering** rather than by tailoring, a single draft accommodates very different
bodies, spans a pregnancy, and can be let out or handed on. The straight panels nest
as rectangles-with-a-taper, so marker efficiency is high.

It also lets the commons take a narrow handloom seriously. `fabric_width` is a real
parameter: the draft derives its **panel count** from the hem sweep and the usable
cloth width, so a 700 mm handloom width and a 1500 mm mill bolt both produce a correct
pattern rather than one being an afterthought.

## Construction notes

Three pieces: the **band** (нагрудник), the **skirt panel** (полотнище, cut *n*), and
the **strap** (лямка, cut 2).

**The gather seam is declared, not fudged.** The skirt top is deliberately longer than
the band — that surplus *is* the gather. The kernel declares the band-to-skirt seam
with an `ease` equal to the exact surplus the `gather_ratio` calls for, so the seam
check proves the gather is what was asked for rather than passing because two numbers
happened to land near each other. Notches at the band's quarter points and each panel's
centre give real gather-distribution matches.

**Panel count is solved from cloth.** `PANELS` is derived from the hem sweep divided by
the usable fabric width, so changing `fabric_width` genuinely re-drafts the pattern.
The hem is additionally floored at the gathered top plus 200 mm — a sarafan flares, and
the draft will not let you produce a tube.

**Order of work.** Join the panels into a ring; gather the top to the band, matching
notch to notch; close the band at centre back; set the straps at the back anchors, then
button them at the front. Buttoning the straps at the front — rather than sewing them
down — is traditional and is what makes the dress adjustable over time.

**Hem.** Use the deep default (45 mm). The weight is what makes the trapezoid hang.

## Hardware

The strap buttons bridge to the Yantra4D **`sew-through-button`** solid. `button_ligne`
drives the printed button, the band's button seat, and the strap's buttonhole length
together, so the three cannot drift apart. Four holes at the standard spacing
(`button_ligne * 0.635 / 3`) — the historical sarafan button was often a cast or
cloth-covered dome, and a printed sew-through is the honest modern equivalent for a
garment whose buttons take real load.

## Honest simplifications

- The band is drafted as a flat rectangle. Some regional sarafans shape the band with a
  slight upward curve at centre front; that shaping is regional and is left to the maker.
- Straps are drafted straight. Traditional straps are sometimes cut wider at the shoulder
  and tapered; the width parameter covers the practical range.
- No lining is drafted. Festival sarafans in heavier cloth were frequently lined.

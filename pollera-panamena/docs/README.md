# Pollera panameña

The elaborate national dress of Panama — a two-piece of extraordinary fullness: the **camisa**,
an off-shoulder blouse of two gathered flounces, and the **pollerón**, a two-tier gathered
skirt of several loom widths, both worked in fine white cotton with **calado** (drawn-thread)
and **sombreado** (appliqué) embroidery and edged with lace.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Panamanian; made-to-measure).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A made-to-measure draft that solves every gather to its band and sizes the off-shoulder
> band from the shoulder span — a correct base for a national treasure, with none of the
> year-long embroidery drawn.

## Provenance

The **pollera panameña** is the national dress of Panama and one of the most labour-intensive
garments in the world: a **pollera de gala** (the formal, fully embroidered pollera) can take
**a year** of hand work. It has two parts — the off-shoulder **camisa** blouse of two ruffled
flounces (**arandela superior** and **inferior**), and the two-tier **pollerón** skirt of
enormous fullness — both in fine white cotton or linen, worked in **calado** drawn-thread
embroidery and **sombreado** / **marcado** appliqué, edged with lace, and finished with the
beaded **tembleque** head ornaments and gold jewellery.

This cartridge drafts the pollera's construction as a made-to-measure block and draws **no**
embroidery.

## Why it earns its rank

**The fullness is solved at every gathered seam.** The pollera is a chain of gathers, each of
which must match its band or the whole dress hangs wrong. Every gathered panel width is *solved*
from the band it gathers onto:

```python
CAMISA_TOP_WIDTH = BAND_LEN * camisa_gather          # camisa flounce onto the off-shoulder band
POLLERA_UP_WIDTH = WAIST_BAND * skirt_gather          # upper tier onto the waistband
POLLERA_LO_WIDTH = POLLERA_UP_WIDTH * tier_gather     # lower tier onto the upper
```

Each gather ratio is reported, tier by tier, so the pollera's volume is a set of solved facts
rather than a guess.

**The camisa is off-shoulder, so the band is solved from the shoulder span.** The blouse sits
off the shoulders on a wide band, and that band's length is solved from the shoulder-to-shoulder
span plus arm room — not from a neck girth. The waist closes with a **hook-and-eye** (bridged to
the Yantra4D `hook-and-eye` solid, driven from `closure_span`) and laces with the **lana** wool
cords.

## What is deliberately out of scope

No specific **calado**, **sombreado**, or **tembleque** design is drawn. Those are the true art
of the pollera — the work of artisans who spend months on a single dress — and belong to them,
not to a pattern generator.

## Parameters

`shoulder_span`, `arm_room`, `waist_girth`, `camisa_top_drop`, `camisa_bot_drop`,
`camisa_gather`, `pollera_up_drop`, `pollera_lo_drop`, `skirt_gather`, `tier_gather`,
`band_height`, `closure_span`, `seam_allowance`, `hem_allowance`. The shoulder span and waist
carry ISO 8559 measurement codes for made-to-measure fitting.

## Pieces

- **camisa_top** / **camisa_bot** — the two camisa flounces (arandela superior / inferior).
- **band** — the off-shoulder camisa band.
- **pollera_up** / **pollera_lo** — the two pollerón tiers.
- **waistband** — the pollera waistband, with the hook-and-eye.

## Hardware

A waist hook-and-eye via the Yantra4D `hook-and-eye` cartridge (linked), sized from the closure
span. The pollera also laces with the lana wool cords.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with deep respect for the artisans of the pollera panameña; the calado, sombreado and
tembleque are theirs.

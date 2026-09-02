# Agbàdá

The wide-sleeved flowing outer robe of the **Yorùbá** of southwestern Nigéria and Bénin,
worn over a **bùbá** (tunic) and **ṣòkòtò** (drawstring trousers), usually with a **fìlà**
(cap). Cognate garments run across West Africa — the Hausa **babban riga**, the Wolof and
Mande **grand boubou** — and share this construction logic, though the naming and the
embroidery vocabulary used here are Yorùbá.

Part of the **Fashion Cabinet Commons** (FC-300, long-tail — heritage — West African).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A draft that solves the strip count as an integer tells a weaver and a tailor exactly
> what the garment will consume before a thread is cut.

## Provenance

The agbàdá is the senior garment of Yorùbá men's dress, worn for weddings, naming
ceremonies, funerals, chieftaincy occasions and — in plainer cloth — for ordinary formal
wear. Its prestige form is made from **aṣọ òkè**, the hand-woven strip cloth of the
region, and its chest and neck are worked by specialist embroiderers whose craft is a
distinct profession from tailoring.

The garment is worn with the wings **gathered up onto the shoulders**, which is why its
flat span is so much larger than the wearer — the drape and the gesture of shrugging the
wings back are part of how the garment is worn, not an accident of cut.

This is an original draft made from the garment's published construction logic. It is not
a copy of any particular workshop's or family's pattern.

## Why it earns its rank

**The loom is in the pattern.** Traditional aṣọ òkè comes off a narrow men's treadle loom
in strips roughly 100–150 mm wide. A robe as wide as an agbàdá is therefore *assembled
from many strips sewn selvedge to selvedge* — and those seams are visible, regular, and
intentional. Most drafts would treat this as a finishing detail. Here it is the governing
constraint:

- The strip count per half-span is an **integer ceiling** from the real `strip_width`.
- The assembled span is then **recomputed from that integer** — so the drafted panel is a
  width the loom can actually produce.
- The delta against the width you requested is **reported in the metadata**, not hidden.
  At the defaults that is 9 strips and a +60 mm surplus. You cannot half-weave a strip,
  and a draft that pretended otherwise would be lying to the weaver.

**There is no armscye and no set-in sleeve.** The body simply continues outward past the
shoulder to the full wing span; the wing *is* the sleeve. This is why `wing_span` is a
single fingertip-to-fingertip measurement rather than a chest width plus a sleeve length —
drafting it as two numbers would invite them to contradict each other. The wing's hang
depth is likewise **solved** from the span and the body width rather than left free.

**The neck facing is measured, not assumed.** The ọrùn is a scooped curve, so the facing
that finishes it is a curve too. Its inner and outer edge lengths are measured from the
drafted polygon and reported (188.6 mm and 274.5 mm at the defaults) — the outer is
necessarily longer, since it is the same curve offset outward, and stating both proves the
offset is consistent rather than eyeballed.

## Construction notes

Pieces: **body** (cut 2, on the fold at the shoulder), **neck_facing** (cut 4), and
**chest_panel** (onídìí, cut 1 on the fold).

1. **Weave or assemble the strips first.** Join strips selvedge to selvedge until you have
   two panels of the assembled half-span width. The `strip-seam` internals mark the first
   two repeats so the pitch is visible on the draft. Flat-fell these seams — they show.
2. Cut each body panel on the fold at the shoulder. Front and back are continuous; there
   is no shoulder seam.
3. Cut the ọrùn opening and the ìlà slit below it. Together they must admit the head —
   there is no closure anywhere on this garment, which is why the manifest warns if the
   two are too small combined.
4. Face the neck with the four facing pieces (two layers, front and back), joining them at
   their short ends to ring the opening.
5. If using an applied breast panel, embroider it **flat, before assembly** — this is how
   the dense onídìí work is actually done — then apply it over the chest, aligning its
   `ila-passage` to the slit.
6. Close the side seams from the hem up to the underarm notch, then close the wing
   underseams from the underarm out to the wingtip. Hem the wingtips and the hem.

## Hardware

**None.** The agbàdá is pulled over the head and has no closure of any kind. There is no
`notion.hardware_ref` on this cartridge because there is nothing to fasten.

## What is deliberately excluded

**The embroidery is not drafted.** The chest and neck work of an agbàdá — the **olówu**
and the dense **onídìí** breast field — is a named specialist craft with its own motif
vocabulary, executed by embroiderers, and the specific motifs carry lineage, title and
occasion. This cartridge marks the **field** where that work goes and leaves the work
itself to the embroiderer. Generating motifs would be counterfeiting a craft.

**Title and chieftaincy regalia are not drafted**, nor are the specific agbàdá worn for
**ìṣọmọlọ́rùkọ** (naming) and other rites. Those garments are conferred and occasion-bound;
they are not configurations of a robe.

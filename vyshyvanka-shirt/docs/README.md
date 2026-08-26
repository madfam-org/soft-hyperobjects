# Vyshyvanka embroidered shirt

The Ukrainian embroidered shirt (**вишиванка**): a straight, loose linen or hemp shirt built
from rectangular panels, gathered at the neck into a narrow band, with straight sleeves set on
square underarm gussets — worn by men and women alike.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Ukrainian).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> The garment beneath the embroidery, drafted honestly — straight panels, square gussets, a
> gathered band — with the embroidery marked but never drawn, because the вишивка is the
> region's, not the generator's.

## Provenance

The **vyshyvanka** is the embroidered shirt of Ukraine, worn across every region and social
class, and one of the strongest living symbols of Ukrainian identity — celebrated each year on
**Vyshyvanka Day**. Its cut is a peasant-chemise construction of straight linen or hemp: a
rectangular body folded at the shoulder, straight sleeves gathered into the neck, and square
underarm gussets. What distinguishes one vyshyvanka from another is the **embroidery**
(вишивка) — the regional pattern, colour and placement, which can identify a village, a family,
or a stage of life.

This cartridge drafts the shirt's construction and **marks** the embroidery zones, but draws
**no** embroidery pattern.

## Why it earns its rank

**It is panels and gussets, not shaped pattern pieces.** The body is a rectangle folded at the
shoulder; the sleeve is a rectangle; the underarm is a **square gusset** — declared square, so
a rhombus cannot sneak in — that lets the straight sleeve meet the straight body without a
curved armscye:

```python
pattern.declare_seam(("gusset", "body_lower"), ("gusset", "sleeve_lower"), tol=0.5)
pattern.declare_seam(("gusset", "body_upper"), ("gusset", "sleeve_upper"), tol=0.5)
```

The gathered neck is solved from the body width, not the neck girth: the whole body top is
gathered into the band, and the actual gather ratio is reported (`actual_gather_ratio`).

**The embroidery is a marked field, not decoration.** The chest, sleeve, cuff, collar and hem
embroidery zones are drawn as **marked fields** the maker fills. No specific vyshyvka pattern,
colour scheme or regional motif is drawn or named — the worst thing a pattern generator could
do with a vyshyvanka is invent or reproduce the patterns that identify real people and places.

## What is deliberately out of scope

Every embroidery pattern. The вишивка belongs to the regions and families that keep it; this
cartridge gives a correct base to embroider in one's own tradition and draws none of it.

## Parameters

`body_width`, `shirt_length`, `neck_girth`, `neck_gather`, `sleeve_length`, `sleeve_width`,
`cuff_girth`, `gusset_size`, `collar_height`, `neck_drop_front`, `seam_allowance`,
`hem_allowance`.

## Pieces

- **body** — the shirt body, cut on the shoulder fold, gathered neck, chest/hem zones marked.
- **sleeve** — the straight sleeve (cut 2), gathered top, sleeve/cuff zones marked.
- **gusset** — the square underarm gusset (cut 2).
- **collar** — the neck band the gathered body top is set into.

## Fabric

Linen or hemp; the neck is a band or drawstring — there is no hardware closure.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living embroidery traditions of Ukraine; the вишивка is the
maker's and the region's.

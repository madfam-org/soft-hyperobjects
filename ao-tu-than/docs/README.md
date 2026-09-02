# Áo tứ thân (four-panel dress)

The **four-panel** long dress of northern Vietnam's countryside — the everyday and festival
dress of the Kinh before the fitted **áo dài** — worn with the **yếm** (bib), a wide waist
sash (**thắt lưng**) and the flat **nón quai thao** hat.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Vietnamese).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A four-panel draft that declares the centre-back seam and hangs the front as free flaps —
> instead of flattening the dress into a single-piece robe with a diagonal edge.

## Provenance

**Tứ thân** means "four panels", and the name is the construction: the dress is built from
four separate lengths of narrow handloom cloth — two **back** panels seamed at centre back,
and two **front** panels left free as flaps that hang open and are crossed low and tied over
the waist sash. It was the working and festival dress of the Kinh of the northern Vietnamese
delta, worn over the **yếm** bib, and it is the ancestor of the later, fitted **áo dài** (a
two-panel, body-fitted evolution). It survives today in folk performance, at festivals, and
in quan họ singing.

This cartridge drafts the four-panel garment as an original construction draft, not a copy of
any particular village pattern, and it draws no bib or brocade motif.

## Why it earns its rank

**It is four panels, and the back centre seam is real.** The garment is *not* a fold-cut
body: it is four panels, and the two back panels meet at a real centre-back seam. The panel
width is a parameter, and the body circuit is computed from it:

```python
BODY_CIRCUIT = panel_width * 2 + panel_width * 2 * flap_overlap
```

A loom too narrow to make the two back panels plus the flaps' crossing reach round the wearer
is reported as `panel_sufficient: false` rather than silently widened — the same honesty the
`changpao` and `haori` cartridges apply to their own weaving traditions.

**The front is flaps, not a closed front.** There is no buttoned placket up the chest. The
two front panels are worn open, crossed low and tied, and the dress is held by the waist sash.
Only a single **throat hook-and-eye** holds the collar band at the neck — bridged to the
Yantra4D `hook-and-eye` solid, driven from the garment's `closure_span`. The neck band is cut
to the **measured** neckline (both back quarters plus both flap necks), not to a neck girth.

## What is deliberately out of scope

The **yếm** bib is a separate garment and is not drafted here; no brocade or printed motif is
drawn. The cloth's pattern is the maker's.

## Parameters

`panel_width`, `chest_girth`, `dress_length`, `neck_girth`, `collar_height`, `shoulder_slope`,
`sleeve_reach`, `armhole_depth`, `flap_overlap`, `closure_span`, `seam_allowance`,
`hem_allowance`.

## Pieces

- **back** — the back, two panels seamed at CB (drafted as one on-fold half with the CB seam
  marked), one-piece sleeve run past the panel.
- **flap** — one front flap (cut 2), the free crossing panel.
- **collar** — the neck band (cut 2), cut to the measured neckline.

## Hardware

A throat hook-and-eye via the Yantra4D `hook-and-eye` cartridge (linked), sized from the
closure span. The dress is otherwise held by the sash and the tied flaps.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living folk dress of northern Vietnam; the cloth and the wearing
are the maker's and the wearer's.

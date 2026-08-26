# Aymara pollera skirt

The full, gathered skirt of the Aymara and Quechua women of the Bolivian and Peruvian
altiplano — the **cholita's pollera**, worn in layers over the enagua underskirt with the
manta shawl and the bowler hat.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Aymara / Quechua, Bolivia & Peru).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A draft that treats the pollera's fullness as a *solved* dimension and adds the alforza
> tucks' take-up to the cut length — the two things an ordinary-skirt draft leaves out.

## Provenance

The **pollera** is the full, gathered skirt worn by Aymara and Quechua women across the
Bolivian and Peruvian altiplano — the skirt of the **cholita**, worn in several layers over an
**enagua** underskirt, with a **manta** shawl and a bowler hat. It is a garment of great cloth
volume: many loom widths gathered or knife-pleated tightly onto a firm waistband. Near the hem
it carries horizontal decorative tucks — **alforzas** — that ornament it and, practically, let
it be lengthened as it is passed down or as fashion shifts. Once imposed by colonial dress
codes, the pollera is now a proud and deliberate marker of Aymara and Quechua identity.

This cartridge drafts the pollera's construction and marks its detail zones, drawing no
**aguayo** pattern or hem-band colourway.

## Why it earns its rank

**The fullness is solved, and it is extreme.** The panel width is *solved* from the waist times
a large gather ratio (2.5–6.5×), so the gathered top matches the band by construction and the
true cloth volume is reported:

```python
BAND_LEN    = waist_girth + 40
PANEL_WIDTH = BAND_LEN * gather_ratio     # at 4.5×, a ~780 mm waist becomes a ~3.7 m panel
```

The pollera's volume is not decoration added on — it *is* the panel width.

**The alforzas eat length.** Each horizontal tuck takes twice its depth in cloth, so the cut
length must include the tuck take-up or the finished skirt comes up short:

```python
TUCK_TAKEUP = alforza_count * alforza_depth * 2
CUT_LENGTH  = finished_length + TUCK_TAKEUP + hem_allowance
```

Both the finished and the cut length are reported. The tucks also let the pollera be lengthened
later — a real, practical reason they exist.

## What is deliberately out of scope

No specific aguayo pattern, embroidery, or trim colourway is drawn. Those are the maker's and
the region's; this cartridge draws the pollera's construction and none of its identifying
ornament.

## Parameters

`waist_girth`, `finished_length`, `gather_ratio`, `band_height`, `alforza_count`,
`alforza_depth`, `hem_band_depth`, `tie_length`, `seam_allowance`, `hem_allowance`.

## Pieces

- **skirt** — the very full gathered skirt panel, with the alforza tucks and hem band marked.
- **band** — the waistband the panel gathers onto, with ties at the ends.

## Fabric

Bayeta wool, velvet, or aguayo cloth. The pollera fastens with ties at the band.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living dress and identity of the Aymara and Quechua; the aguayo
patterns and colourways are the makers' and the communities'.

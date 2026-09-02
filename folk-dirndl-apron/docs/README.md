# Dirndl apron overlay

The dirndl apron (**Dirndlschürze**): the front overlay worn over the dirndl dress across the
Alpine regions of Bavaria, Austria, South Tyrol and beyond — a rectangular panel gathered onto
a waistband and tied with long ties whose **bow** carries a social message.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Alpine).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A draft that solves the gathered panel to its band and records the meaningful bow position
> as a marking — the apron only, not the dirndl dress beneath it.

## Provenance

The **dirndl** is the traditional dress of the Alpine German-speaking world — a fitted bodice,
a full skirt, a blouse, and the **Schürze** (apron) worn over the front. The apron is a
rectangular panel of cloth gathered onto a waistband and tied with long ties, and its **bow**
is a small piece of social signalling long recognised across the region:

| bow position | meaning |
|---|---|
| tied on the **left** | single / available |
| tied on the **right** | taken / married |
| tied **centre-front** | a child, or (by convention) a server |
| tied at the **back** | a widow |

This cartridge drafts **only the apron** — the panel, its waistband and its ties — not the
dirndl dress (which is a separate garment in the commons).

## Why it earns its rank

**The apron is gathered, and the gather is solved.** The panel is wider than the band and
gathered onto it; the panel width is *solved* from the band length times the gather ratio, so
the gathered top matches the band by construction:

```python
BAND_LEN    = waist_girth * apron_span
PANEL_WIDTH = BAND_LEN * gather_ratio      # solved, so the gather matches
```

**The bow side is a choice, and it is marked.** The tie exit and a bow-position guide are drawn
as markings, and the socially meaningful placement is recorded (`bow_placement`) — as
information the wearer signals, never a rule the pattern imposes.

## What is deliberately out of scope

The dirndl dress itself, and any specific printed dirndl fabric or regional trim. This is the
apron overlay only, in plain cloth.

## Parameters

`waist_girth`, `apron_span`, `apron_length`, `gather_ratio`, `band_height`, `tie_length`,
`tie_width`, `bow_side`, `seam_allowance`, `hem_allowance`.

## Pieces

- **apron** — the gathered apron panel.
- **band** — the waistband the panel gathers onto.
- **tie** — one waist tie (cut 2), tying into the bow.

## Fabric

Cotton, silk, or printed dirndl fabric; the apron ties — there is no hardware closure.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living Alpine dress tradition; the bow's meaning is the wearer's
to signal.

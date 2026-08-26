# Chamanto poncho

The fine dress poncho of the Chilean **huaso** — the elegant counterpart to the everyday
**manta**, woven in fine wool and silk, **reversible**, banded with the **listado** field of
fine coloured stripes, and edged with the woven **trencilla** border.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Chilean).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A poncho draft that centres and sizes the neck slit from the head and keeps the border
> symmetric because the cloth is reversible — the two things a one-sided printed copy loses.

## Provenance

The **chamanto** is the formal poncho of central Chile, worn by the **huaso** (the Chilean
horseman) on dress occasions — the fine, silk-and-wool counterpart to the coarser everyday
**manta**. Its finest examples are the work of the master weavers of **Doñihue**, and its
three signatures are: it is **reversible**, woven double so that a light "day" face and a dark
"night" face both show; it carries the **listado**, a field of fine coloured stripes; and it is
edged all round with the woven **trencilla** border. Traditionally it is woven whole on the
loom with the neck slit left in the weaving.

This cartridge drafts the chamanto's assembled form so a maker working from cut cloth can build
one, and **marks** the listado and trencilla zones the weaver fills — drawing no colourway or
motif.

## Why it earns its rank

**The neck slit is centred and sized from the head.** The slit length is solved from the head
girth (half the head girth plus ease, capped at half the drop) so it clears the head but no
more, and it is centred on the cloth:

```python
NECK_SLIT = min(head_girth / 2 + neck_slit_ease, cloth_length * 0.5)   # centred at cloth_width/2
```

An off-centre or oversized slit is the first thing a poncho draft gets wrong.

**It is reversible, so the border is symmetric.** Because both faces show, the trencilla border
and the listado are drawn symmetric front-to-back, and both faces are marked as finished
(`reversible-face`) — the kernel drafts the flat form, and the double-face finishing is recorded
as an instruction.

## What is deliberately out of scope

No specific listado colourway or trencilla motif is drawn. Those are the weaver's — and the
finest chamantos are the named work of the weavers of Doñihue.

## Parameters

`cloth_width`, `cloth_length`, `head_girth`, `neck_slit_ease`, `trencilla_width`,
`listado_count`, `fringe_depth`, `seam_allowance`.

## Pieces

- **cloth** — the whole chamanto rectangle (two loom halves seamed at the shoulder), with the
  centred neck slit and marked listado + trencilla zones.
- **border** — one representative trencilla border strip, for the weaver, cut to the perimeter.

## Fabric

Fine wool and silk, woven reversible. A poncho has no closure.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living weaving tradition of Doñihue; the listado, the trencilla
and their colours are the weavers'.

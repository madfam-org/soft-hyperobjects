# Kente wrapper cloth

The Akan (Asante) and Ewe women's formal kente ensemble: **two whole wrappers**, each an
assembly of narrow warp-striped strips woven on the men's double-heddle loom and sewn
edge-to-edge — a large lower wrapper (**ntoma**) wound round from the waist, and a smaller
upper wrapper worn over it or as a cover-cloth.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Ghana / Togo, Akan & Ewe).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A strip-assembly draft keeps the logic of kente — the loom-width strip as the real unit,
> the wrapper as a whole number of strips, the field never cut — instead of treating it as
> a print to be sliced like any bolt.

## Provenance

Kente is the strip-woven cloth of the Akan (Asante) and Ewe peoples of Ghana and Togo, woven
in narrow strips (roughly 90–110 mm) on a horizontal double-heddle loom and sewn side by
side into large cloths. Its named weaves (**setts**) carry proverbs, histories and social
meaning, and particular patterns are associated with particular people and occasions.

This cartridge drafts the **women's two-piece ensemble** — a large lower wrapper wound from
the waist and a smaller upper wrapper or cover-cloth — which is a distinct garment from the
men's single toga-style wearing cloth (drafted separately in the commons as `kente-wrap`).
It is an original dimensions-and-drape draft, not a copy of any particular weaver's cloth,
and it draws **no** kente pattern.

## Why it earns its rank

**The cloth is an assembly of strips, and the strip width is real.** A wrapper is not a
free rectangle: it is a whole number of loom strips sewn edge-to-edge, so its width snaps to
a multiple of `strip_width`. The draft solves the strip count from the target width (the hip
girth plus the tuck overlap) and reports the true assembled width:

```python
LOWER_STRIPS = max(6, round((hip_girth + wrap_overlap) / strip_width))
LOWER_WIDTH  = LOWER_STRIPS * strip_width
```

| hip | overlap | strip | target | strips | assembled | tuck ease |
|---:|---:|---:|---:|---:|---:|---:|
| 1020 | 380 | 100 | 1400 | 14 | 1400 | +380 |
| 1020 | 380 | 80 | 1400 | 18 | 1440 | +420 |
| 1500 | 700 | 140 | 2200 | 16 | 2240 | +740 |

The assembled width is always a whole number of strips, and the tuck ease it actually gives
is reported rather than assumed — a wrapper that does not reach round the hip with a real
overlap will not stay tucked.

**The cloth is never cut.** Cutting kente severs the strip weave and the proverb woven into
it, so the wrap is a **marked path**, not a set of pattern pieces: the strip joins, the
waist-tuck line and the wound turn are internal markings, and the sides are the woven
selvedge. There are no piece-to-piece seams to verify because there are no cut pieces — only
whole cloths.

## What is deliberately out of scope

No named kente **sett** or proverb-weave is drawn or named. Those carry specific meaning and
belong to Akan and Ewe weavers and communities. This cartridge supplies the **cloth
dimensions and the drape only**; the weave is the weaver's.

## Parameters

`hip_girth`, `lower_length`, `upper_fraction`, `wrap_overlap`, `strip_width`,
`hem_allowance`, `seam_allowance`. Made to measure to the wearer's hip and height; the strip
width is the weaver's loom width.

## Pieces

- **lower** — the large lower wrapper (ntoma), whole cloth, cut 1, uncut.
- **upper** — the smaller upper wrapper / cover-cloth, whole cloth, cut 1, uncut.
- **strip** — one representative loom strip (cut = the two wrappers' total strips), for the
  weaver.

## Fabric

Hand-woven kente strip cloth (cotton, silk or rayon). Only the top and bottom edges are
hemmed; the sides are the woven selvedge. The wrappers are wound and tucked — no closure.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living weaving traditions of the Akan and Ewe; the strips, the
setts and their meanings are the weavers' and the communities'.

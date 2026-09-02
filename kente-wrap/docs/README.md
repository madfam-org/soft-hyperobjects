# Kente wrapper cloth garment

Kente is the strip-woven cloth of the **Akan (Asante)** and **Ewe** peoples of Ghana and Togo:
narrow warp-striped strips woven on a double-heddle loom and sewn edge-to-edge into a large
rectangle. The men's wearing cloth is that **whole uncut rectangle**, draped over the left
shoulder and wound round the body.

Part of the **Fashion Cabinet Commons** (FC-400, lane 10 — heritage). Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabi.net).

> The single most important fact about the wearing cloth is that it is **not cut**. Cutting kente
> destroys the strip weave and the meaning woven into it — so this cartridge cuts nothing.

## Provenance

Kente is woven by the Akan and Ewe of Ghana and Togo. Its named weaves and proverb-named setts
carry specific meaning and **belong to those weavers and communities**. This cartridge draws **no
kente pattern** and names none — it supplies the cloth **dimensions** and the **drape** only, and
the weave is the weaver's.

## Why it earns its rank

**The cloth is an assembly of strips, and the strip width is real.** Kente is woven in strips of
a fixed loom width (`strip_width`, ~100 mm), and the cloth is a **whole number** of them sewn side
by side. So the cloth's width is not free — it is `strip_count × strip_width`. This cartridge
solves the strip count from the target width and reports the true assembled width, and marks each
strip join as a real straight seam, because that is where the weaver's strips actually meet.

**The garment is the drape, not a cut.** The wearing cloth is sized by its **dimensions** (length
from the wearer's height, width from the strip count) and the wrapping is a **path**, not a set of
pattern pieces. The draft marks the shoulder line and the wrap turns so a wearer knows how the
rectangle sits — while leaving the cloth whole.

## Construction notes

Pieces: **cloth** (the whole assembled rectangle, cut 1, **uncut**), **strip** (one representative
loom strip, cut `strip_count`, for the weaver).

1. Weave the strips to length in the weaver's own named pattern.
2. Join them edge-to-edge into the whole cloth; hem the two ends.
3. Wear by the drape — over the left shoulder and wound round the body, following the marked
   shoulder line and wrap turns. **Do not cut the cloth.**

## Hardware

**None.** The wearing cloth is draped, not fastened.

## Made to measure

Drafted to the wearer's **height** and **reach** (which set the cloth length and width) plus the
loom **strip width**. The assembled width snaps to a whole number of loom strips and is reported;
every slider extreme renders watertight.

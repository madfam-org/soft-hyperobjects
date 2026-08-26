# Haori (women's lined)

The hip- or thigh-length jacket worn **open** over a kimono, closed only by a short braided cord
(**haori-himo**) tied between two chest loops (**chi**) — in the women's **lined (awase)** version.

Part of the **Fashion Cabinet Commons** (FC-400, lane 10 — heritage). Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabinet.app).

> The FC-300 [haori](../../haori/docs/README.md) got the hardest thing right — keeping the bolt as
> the unit — but left the lining as bolt goods. In a women's haori the lining is the whole point.

## Provenance

The haori is Japanese. This cartridge drafts the women's everyday **lined** haori. The **紋付**
(*montsuki*) crested formal haori is **not** drafted — a **家紋** (*kamon*, family crest) is a
family's mark, not a decoration, and this cartridge places none. The surface dyeing traditions
(**友禅** *yūzen*, **絞り** *shibori*) belong to their own crafts.

## Why it earns its rank

Everything the FC-300 haori encodes is **inherited**: the **bolt is the unit** (pieces are
rectangles of a ~375 mm tanmono bolt used whole), the front **overlap is solved** from the bolt
width and chest, the **furi stays open**, and the **collar is solved** to the measured neck run.
On top of that, this cartridge adds the two things that make it the women's lined haori:

**The lining is drafted, not bought-by-the-bolt.** The **羽裏** (*hauro*) body and sleeve linings
are cut to the shell's own measured runs, a few mm smaller (`lining_reduction`) so they do not
peek, and **declared as seams against the shell** — so the lining is a real, verified member of
the pattern. In a women's haori the lining is the expressive surface: plain outside, patterned
within.

**The front corner is rounded (maru).** The women's haori often finishes the lower front corner
with a soft **丸** (*maru*) curve rather than the square men's corner; this is drawn as a solved
arc at the front hem (set `maru_radius` to 0 for the square corner).

## Construction notes

Pieces: **body** (migoro, cut 2 on fold, maru corner), **okumi** (front panel, cut 2), **sleeve**
(sode, cut 2 on fold), **collar** (eri, cut 1), **chi** (cord loops, cut 2), **body_lining**
(hauro, cut 2 on fold), **sleeve_lining** (cut 2 on fold).

1. Assemble the shell as the FC-300 haori: body halves at centre back, okumi to the body sides,
   sleeves along the **attach** edge only (the furi stays open), collar folded back for the maeeri.
2. Assemble the drafted lining to the same runs, cut smaller by `lining_reduction`.
3. Bag the lining into the shell so the jacket is reversible-clean; hand-finish.
4. Set the two chi loops; the haori-himo cord ties between them.

## Hardware

**None.** Closed only by the braided haori-himo cord between two cloth loops.

## Made to measure

Drafted via the **bolt width** and **chest** (the overlap is solved), plus haori length, sleeve
depth and reach. The lining is drafted to the shell and the front corner is rounded; every slider
extreme renders watertight, and `bolt_sufficient` reports honestly whether the bolt closes the
chest.

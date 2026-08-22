# Haori (羽織)

The hip- or thigh-length jacket worn **open** over a kimono, closed only by a short
braided cord (**羽織紐**, *haori-himo*) tied between two small cloth loops at the chest.

Part of the **Fashion Cabinet Commons** (FC-300, long-tail — heritage — Japanese). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> An open draft that keeps the bolt as the unit preserves the unpick-wash-resew logic
> instead of quietly translating the garment into shaped Western panels.

## Provenance

The haori began as outerwear for men in the Sengoku and Edo periods and was adopted by
women in the nineteenth century; it is now worn by anyone, over kimono and increasingly
over Western clothing. It is neither a coat nor a short kimono. It hangs **open**, is never
wrapped closed, and its only fastening is a cord tied between two loops.

This cartridge drafts an everyday haori. It is an original draft made from the garment's
construction logic, not a copy of any particular workshop's pattern.

## Why it earns its rank

**The bolt is the unit, not the body.** This is the single idea the cartridge exists to
encode, and it is genuinely different from every Western draft in this commons. Kimono-
family garments are cut from **反物** (*tanmono*) — a bolt roughly 375 mm wide — and the
pieces are **rectangles of that bolt used whole**: the body panel is one bolt width, the
sleeve is one bolt width, the okumi is a half.

So this draft does *not* cut panels to a chest measurement. It takes `bolt_width` as a real
parameter, computes the body circuit from it, and **solves the front overlap** as what
remains after that circuit wraps the chest:

| bolt | circuit | overlap | closes? |
|-----:|--------:|--------:|:--------|
| 375 mm | 1125 mm | 145 mm | yes |
| 420 mm | 1260 mm | 280 mm | yes |
| 310 mm (chest 1400) | 930 mm | 0 mm | **no** |

That last row matters. The draft reports `bolt_sufficient: false` rather than silently
producing a garment whose fronts cannot meet. Fit here comes from **where the straight
seams fall**, which is why one haori fits a range of wearers.

**The 振り (furi) must stay open.** The sleeve hangs free below the arm: it attaches along
its **upper portion only**, and the opening below is deliberate. The commonest haori error
is drafting the attachment equal to the full sleeve depth, which sews that opening shut.
Here the attachment length is **solved** as `sleeve_depth − furi_open` (320 mm at the
defaults), and the body's armhole is drafted *to that solved length*, with the seam check
proving it.

**The 前衿 (maeeri) is what makes it a haori.** The collar folds outward along its length
to form a shallow lapel. So the collar strip is cut at **double** its finished width plus
turn-of-cloth, and its **length is measured** — the sum of both back-neck curves and both
front edge runs (1866.5 mm at the defaults, growing to 2286.5 mm at a 1050 mm length) —
rather than estimated from a neck circuit.

## Construction notes

Pieces: **body** (migoro, cut 2 on the shoulder fold), **okumi** (front panel, cut 2),
**sleeve** (sode, cut 2 on the fold), **collar** (eri, cut 1), **chi** (cord loops, cut 2).

1. Join the two body halves at centre back. Attach the okumi panels to the body panels'
   side edges.
2. Attach each sleeve along its `attach` edge **only**, matching the midpoint notches.
   **Stop at the furi notch.** The gap below stays open and is finished as an edge, not
   sewn to the body.
3. Close the side seams below the armhole.
4. Apply the collar: fold it back along the `maeeri-fold` marking, matching its centre-back
   notch to centre back and its quarter notches to the shoulders. It runs down both fronts
   to the hem.
5. Attach the two chi loops at the marked `chi-seat` height on each front. The haori-himo
   cord ties between them.
6. Hem, and line.

A haori is normally **fully lined** (胴裏 *dōura*), and the lining is often the expressive
surface — traditionally the outside stays plain while the inside carries the pattern.
Traditionally the whole garment is hand-sewn so it can be unpicked, washed flat as bolt
lengths, and re-sewn.

## Hardware

**None.** The haori is closed only by the braided haori-himo cord tied between two cloth
loops. There is no `notion.hardware_ref` on this cartridge; the cord is a purchased or
hand-braided item, not a fastener to bridge.

## What is deliberately excluded

**The 紋付 (montsuki) crested formal haori is not drafted.** Its formality is set by the
**number and placement of 家紋** (*kamon*, family crests) — one, three or five. A kamon is
a family's mark, not a decoration, and this cartridge will not place crests.

Also out of scope: the **十徳** (*jittoku*), the haori of specific professional and
religious orders, and the surface dyeing traditions (**yūzen**, **shibori**), which belong
to their own crafts and artisans.

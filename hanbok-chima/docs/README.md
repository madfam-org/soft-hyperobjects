# Chima (치마)

The skirt of the Korean **hanbok**: a very full, high-waisted wrap skirt suspended from
a chest band (**말기**, *malgi*) and fastened with long ties (**끈**, *kkeun*). It is worn
with the short **jeogori** jacket, drafted separately in this commons as
[`hanbok-jeogori`](../../hanbok-jeogori/).

Part of the **Fashion Cabinet Commons** (FC-300, long-tail — heritage — Korean). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> An open, made-to-measure chima keeps a living Korean garment makeable and repairable by
> the people who wear it — the draft tells a maker exactly how much cloth to buy and
> exactly where each fold goes.

## Provenance

The chima is one half of the two-piece hanbok, the everyday and formal dress of Korea, in
continuous use from the Three Kingdoms period through the Joseon dynasty and into the
present. It is not a historical costume: chima and jeogori are worn today at weddings,
holidays (설날 *Seollal*, 추석 *Chuseok*), first birthdays, and increasingly as everyday
wear in the 생활한복 (*saenghwal hanbok*, "living hanbok") movement.

The garment's defining feature is **where it hangs from**. The chima is suspended from a
band that sits *above the bust*, on the ribcage — not at the waist. Everything about the
silhouette follows from that one decision: the bell begins high, the waist is never
engaged or defined, and the volume reads as column rather than as a gathered skirt. A
draft that took a waist measurement would be drafting a different garment.

This cartridge draws the everyday and festival chima. It is an original draft made from
the garment's published construction logic, not a copy of any particular regional or
family pattern.

## Why it earns its rank

Three things make this a real draft rather than "a big rectangle on a band":

**Pleating is treated as discrete.** You cannot sew 27.4 pleats. Most parametric skirt
drafts declare a continuous "fullness ratio" and leave the maker to work out the folds —
which is precisely the part that is hard. Here the pleat count is rounded to an integer
*first*, and then the pleat face, the pleat depth, the cloth each pleat consumes, and the
flat panel width are all **back-solved from that integer**, so the pleats tile the band
exactly with nothing left over.

**Knife and box pleats are different amounts of cloth.** A knife pleat folds cloth back on
itself once and consumes 2× its visible face; a box pleat folds twice and consumes 4×.
Switching `pleat_style` therefore roughly doubles the fabric requirement and the piecing
count — the draft reports this rather than hiding it.

**Loom width is real.** A chima at full fullness is far wider than any bolt of cloth, so
it is always pieced from several straight widths. The panel count is solved from the
actual usable `fabric_width` you enter, and the BOM's yardage follows from the drafted
polygon areas, not from a rule of thumb.

The band-to-panel seam is declared with its ease **measured from both drafted polygons**,
so the surplus the pleats absorb is proven by the geometry rather than asserted in a
comment.

## Construction notes

Pieces: **band** (malgi, cut 1), **panel** (pok, cut *n* — solved from loom width), and
**tie** (kkeun, cut 2 on the fold).

1. Join the skirt panels at their vertical side seams into one long flat width. Where
   possible, place these seams so they fall inside a pleat fold and disappear.
2. Hem the skirt first, while it is still flat — a deep hem (`hem_allowance`, default
   60 mm) weights the bell and is much easier to sew before pleating.
3. Pleat the top edge to the marked repeat. The `pleat-fold` internals mark one full
   repeat unit at each panel's start; the rest continue at `cloth_per_pleat` intervals.
   Baste the pleats down before you go near the band.
4. Set the pleated top into the band's `bottom` edge. The band is interfaced firmly — it
   carries the entire weight of the skirt.
5. Attach the two ties at the band ends (`tie-anchor` markings). The anchor button seats
   at the `overlap-line`; it holds the wrap closed while the ties are tied.

The wrap overlaps at the **back**. `wrap_overlap` is real cloth carried by both the band
and the pleating — reduce it too far and the skirt gaps as the wearer moves, which is why
the manifest warns below 120 mm.

## Hardware

The band's anchor button bridges to the Yantra4D `sew-through-button` solid via
`notion.hardware_ref`. `button_ligne` drives both the drafted button seat on the band and
the printed solid's `sew_face` flange, so the two are dimensionally coupled rather than
merely named.

## What is deliberately excluded

Ceremonial and rank-bearing hanbok are **not** drafted here:

- **활옷** (*hwarot*) — the bridal robe
- **당의** (*dangui*) — the court jacket
- **금박** (*geumbak*) — gold-leaf surface work

These are not "decorated chima." They are distinct garments carrying ritual and social
meaning, historically governed by rank and occasion, and reducing them to a checkbox on a
skirt cartridge would be exactly the costume-ification this commons refuses. Surface
decoration in general is left to the maker rather than dictated by the draft.

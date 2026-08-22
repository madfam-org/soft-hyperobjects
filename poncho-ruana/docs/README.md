# Ruana

The open-front wool wrap of the Colombian and Venezuelan Andes.

## Provenance

The ruana is everyday working dress of the cold Andean highlands — Boyacá,
Cundinamarca, Santander and Nariño in Colombia, and the Venezuelan Andean states of
Mérida, Táchira and Trujillo. It is *páramo* clothing: high, wet, windy country where
a heavy fulled wool that sheds drizzle matters more than tailoring.

The word is generally traced to Chibcha *ruana* / the Spanish *ruan* (a cloth name),
and the garment as worn today is a colonial-era synthesis — Andean backstrap and
treadle weaving in wool, in a form shaped by both Indigenous and Iberian wrap
traditions.

**Ruana is not a synonym for poncho**, and the difference is not regional vocabulary —
it is construction. A poncho is a **closed** rectangle with a neck hole; you put it on
over your head and it stays a tube. A ruana is **split up the centre front**: it opens
like a cape, wraps across the chest, and can be thrown back over one shoulder to free
the arms for work. That single split is the whole garment, and it is why this cartridge
exists separately from the commons' `sarape-poncho`, which draws the closed Mexican
form.

The ruana is secular working and everyday dress, not ceremonial or restricted wear, so
drafting it for the commons is straightforward. Its stripe and colour conventions do
carry regional meaning; this cartridge marks no colourway and leaves that to the maker.

## Why this earns a commons rank

Three rectangles and one real seam. The ruana is close to the cheapest warm outer
layer a person can make, it fits almost anyone *because* it is not fitted, and nothing
about it is shaped — so worn cloth can be cut down and re-hemmed rather than discarded.

It also completes a pair in the commons. Holding the closed poncho and the open ruana
as two distinct cartridges, rather than one with a "split?" checkbox, records an actual
constructional distinction that matters to the people who wear them.

## Construction notes

Three pieces: **back** (cut 1 on the centre-back fold), **front** (cut 2, mirrored) and
a **neck binding**.

**The shoulder seam is the thing that solves.** The back's shoulder edge is the full
half-span. The neck slot is carved out of it, and each front's shoulder edge is then
solved as *the back's measured shoulder minus the half slot*. So two fronts plus the
slot exactly reconstitute the back. The declared seam carries the `front_overlap` as
honest `ease` — that surplus is the crossing allowance that lets the ruana be pulled
shut, not a mismatch. If a wide `neck_slot` would leave less than 60 mm of shoulder to
sew, the kernel narrows the slot rather than emitting an unsewable pattern.

**The back drop is declared, not implied.** The back is longer than the fronts by
`back_drop`. That difference is declared as the ease on the side-edge check, so the run
proves the drop is exactly the working proportion asked for.

**The neck is a slot, not a scoop.** On a woven wrap in heavy cloth you do not cut a
curved neckline — you cut a straight slit across the shoulder line and bind or face it.
The binding piece is drafted to the full slot circuit. Set `collar_depth` to 0 for a
simply bound edge instead of a stand.

**Fringe.** `fringe_depth` marks a line at the hems for warp fringe, which is how a
loom-finished ruana normally ends. Set it to 0 for a turned-and-stitched hem. Note the
hem, side and centre-front edges carry **zero** seam allowance in the draft — on a
selvedge-finished wool wrap these edges are not turned at all.

## Hardware

Two throat toggles bridge to the Yantra4D **`toggle`** solid. `barrel_len` and
`cord_dia` drive the printed toggle, the marked toggle seat on the centre-front edge,
and the cord loop together, so a bigger toggle cannot end up with a loop it will not
pass through. A toggle rather than a button is the right call for heavy fulled wool
and cold hands.

## Honest simplifications

- No stripe, ikat or woven-motif placement is drafted. Regional colourways carry
  meaning; a default would be an invention.
- The traditional ruana is often woven to final width on a narrow loom, with selvedges
  as finished edges and no cutting at all. This draft assumes cut cloth, which is the
  practical case for a sewing-machine maker; a weaver should treat the panel dimensions
  as loom targets.
- The neck binding is drafted as a straight strip. A shaped facing sits slightly better
  on a deep stand; the straight strip is what is normally used.

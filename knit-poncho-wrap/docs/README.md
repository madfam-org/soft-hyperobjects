# Knit Poncho Wrap

The wrap you fasten: a drafted neckline, a solved stand collar, and a toggle band.

## Why this is not the two ponchos the commons already holds

This is the question worth answering first, because the word "poncho" covers three
genuinely different constructions and the commons now holds all three.

| Cartridge | Neck | Front | What it is |
| :-- | :-- | :-- | :-- |
| `sarape-poncho` | a head slit | closed | one rectangle, nothing shaped; a cloth you pull on |
| `poncho-ruana` | a plain slot | split at CF | an open heritage wrap; a cloth you drape or throw back |
| **this one** | a drafted scoop | split, **fastened** | a shaped garment you close |

The difference is constructional, not vocabulary. A head slit and a plain slot are cut
*through* a flat panel and bound. This cartridge instead drafts a real scooped neckline
from a measured neck girth, solves a stand collar against it, and closes the front with
a toggle band. That is what makes it a garment you fasten rather than a cloth you drape,
and it is why it is the only one of the three that needs hardware at all.

## Why this earns a commons rank

The contemporary poncho wrap is what most people actually buy and wear as a poncho now,
and it is the shape that survives the transition from a woven blanket tradition to a
heavy knit or fulled cloth. It is also very close to the cheapest warm outer layer a
person can make: four pieces, one real seam per side, no sleeves to set and no armhole
to fit. Because almost nothing about it is fitted, one draft covers a very wide range of
bodies — but unlike a plain rectangle it stays on the shoulders and stays shut in wind,
which is the difference between a decorative wrap and a working one.

## Construction notes

Four pieces: **front** (cut 2, mirrored), **back** (cut 1 on the centre-back fold),
**collar** (half on the CB fold) and **toggle band** (cut 2, mirrored).

**The shoulder fall is the thing that makes it a wrap and not a hoop.** Each panel's
outer edge sits `shoulder_slope` *below* the neck end of the shoulder line. On a soft
knit that matters less; in fulled melton a flat rectangle stands up in a stiff ring
around the neck instead of falling over the shoulders. Front and back use the same
sloped line — same half-neck width, same half-span, same fall — so the shoulder seam
balances to **delta 0.0** by construction.

**The collar is solved, not assumed.** Its neck edge is found by bisection against the
*measured* front scoop plus back scoop. A collar cut shorter than its neckline puckers;
one cut longer flutes. The solver converges to under 1 mm or raises rather than shipping
a collar that nearly fits.

**The toggle count is derived.** It is the clamped closure run divided by the toggle
pitch, floored at 1 and capped at 8. Both the front panel's centre edge and the toggle
band carry the *same* derived ladder, so panel and band cannot disagree about where the
toggles go. The band is drafted with the ladder marked as drill points, plus a cord
channel per toggle sized to `cord_dia`.

**The back drop is declared, not implied.** The back is longer than the fronts by
`back_drop`. The outer edges are *not* sewn — the wrap is open at the sides — so that
difference is declared as the `ease` on the outer-edge check, which makes the render
prove the drop is exactly the length asked for.

**Edges that are not turned.** The fulled face of melton barely frays, so the outer and
hem edges can be raw-cut and topstitched. The centre-front edge carries **zero** seam
allowance in the draft because the toggle band finishes it.

## The clamps, and why they are load-bearing

Four dimensions here are *derived*, and a derived dimension that goes negative does not
fail loudly — it inverts the piece, and the kernel's CCW normalization then hands
`verify()` an outline that looks perfectly valid. Each therefore carries an explicit
floor applied **before any point is built**:

| Derived quantity | Bound | What it prevents |
| :-- | :-- | :-- |
| shoulder fall | ≤ `wrap_length − 120` | a fall so deep no panel remains below the shoulder |
| neck span (half span − half neck) | ≥ 80 mm | a wide neck on a narrow wrap collapsing the shoulder |
| closure run | ≥ 60, ≤ front length below the neck | toggle marks landing above the neckline or off the hem |
| toggle count | 1 … 8 | a band with no toggles, or a fine pitch asking for dozens |
| collar stand height | ≥ 25 mm | a zero-height collar, which is not a piece |

`metadata.solved` reports which bounds actually bit, so a clamped draft is visible rather
than silent. The cartridge was probed at the min **and** max of every one of its 13
parameters, at all-min, all-max and two mixed-extreme combinations, and at each
`target_piece` — 35 renders, all with zero error issues and every declared seam
balancing.

## Hardware

The toggles bridge to the Yantra4D **`toggle`** solid via `notion.hardware_ref`.
`barrel_len` and `cord_dia` drive the printed toggle, its marked seat on the band, the
cord channel through the band and the loop opposite — together, so a bigger toggle can
never end up with a loop it will not pass through. `barrel_dia` is mapped as
`cord_dia * 2.4`, the proportion that keeps a barrel stiff enough not to bend against a
heavy melton edge.

A toggle rather than a button is the right call here for the same reason it is on a
duffel coat: cold hands, thick cloth, and a closure that has to be worked without
looking.

## Honest simplifications

- The wrap is drafted as a shaped rectangle-family panel, not a true circular cape. A
  ring-segment draft (see `capelet`) gives more sweep at the hem for the same shoulder
  fit; this one trades that for a marker yield close to 75%, which matters at melton
  prices.
- No side seam is drafted at all — the outer edges are open, which is what a poncho is.
  A version seamed to the underarm would be a cape-coat and a different cartridge.
- Pockets are not drafted. In-seam pockets have nowhere to live in an open-sided wrap;
  a patch pocket is a maker's addition and would fix a placement the draft has no
  business fixing.
- The collar is a straight stand solved by length. A shaped (curved) stand hugs the neck
  better on a tall collar; the straight one is what is normally cut in heavy cloth.

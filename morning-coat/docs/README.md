# Morning Coat

Formal daywear: one button, a front that sweeps away below it, and waist-seamed tails.

## Provenance

The morning coat is the last surviving descendant of the nineteenth-century riding coat.
The cutaway front is not decoration and never was: a coat you ride in cannot have skirts
across the front of the saddle, so the fronts were cut away and the length kept behind.
When riding stopped being how a gentleman arrived, the shape stayed and turned into
formal daywear — the *chaqué* in Spanish, the *jaquette* in French — and it is now worn
almost exclusively at weddings, at Ascot, and at state occasions.

It is the coat that most clearly shows its own history in its pattern. Every other
formal coat in the commons has a horizontal hem because it was never meant to be worn on
a horse.

## Why this earns a commons rank

The commons already holds `suit-jacket`, `blazer`, `overcoat`, `trench-coat` and
`waistcoat`. None of them can be parameterised into a morning coat, and that is worth
being precise about, because "add a curved hem option" is the tempting wrong answer:

- The front has **no hem edge at all**. Its outline is centre → lapel → gorge → shoulder
  → armhole → side seam → break → **cutaway**, and the cutaway closes the loop back to
  the button. There is no horizontal bottom to make curved.
- The button sits at the **top** of the cutaway rather than partway down a straight
  front, so the whole relationship between the fastening and the hem is different.
- The back is **not one panel**. It is a bodice seamed at the waist plus a separate tail
  skirt, so the tails can be cut on their own grain and hang.

Three structural differences, not a styling flag. That is what earns a rank.

## Construction notes

Seven pieces: **front** (cut 2), **back bodice** (cut 2, CB seam), **tail** (cut 2),
**upper** and **under sleeve** (cut 2 each), **collar** (half on the CB fold) and
**facing** (cut 2).

**The cutaway is the piece that solves.** It is drawn as two chained arcs over a span
derived from the button height (its rise) and the sweep (its run): a shallow lower arc
running back nearly horizontally from the tail break — which is what keeps the tail root
looking like a coat instead of a chopped hem — and a deeper upper arc that turns up into
the button so the edge meets the button stand cleanly. Change either parameter and the
whole curve re-solves; nothing about it is sketched.

**The waist seam is bisected, not assumed.** The tail's waist edge is solved by
bisection against the back bodice's *measured* waist edge, so the join that carries the
tails balances to **delta 0.0** rather than being trusted to arithmetic. Same method for
the collar's neck edge against the measured gorge plus back neck, and for the two-piece
sleeve cap against the measured armholes plus the declared `cap_ease`.

**The facing follows the cutaway.** On a straight-fronted coat a facing runs the centre,
lapel and gorge. Here it must also continue around the cutaway curve, because *that* is
the edge that shows when the coat swings. Its length is the measured centre + lapel +
gorge + cutaway run, with the end allowances declared as honest `ease`.

**The armhole is waist-referenced, and this is a real difference from the commons' other
coats.** `suit-jacket` and `blazer` measure `body_length` nape-to-*hem*, so a deep
armhole still leaves most of the panel below the chest. Here `back_length` is
nape-to-*waist-seam* — a much shorter run — and reusing their formula unmodified drives
the chest line down almost onto the waist and produces an armhole around 40% too deep.
The depth is scaled to the waist length instead and capped so at least 48% of the bodice
stays below the chest line.

## The clamps, and why they are load-bearing

Every dimension the cutaway depends on is *derived*, and a derived dimension that goes
negative does not fail loudly — it inverts the panel, and the kernel's CCW normalization
then hands `verify()` an outline that looks perfectly valid. Each therefore carries an
explicit bound applied **before any point is built**:

| Derived quantity | Bound | What it prevents |
| :-- | :-- | :-- |
| button height (cutaway rise) | ≥ 25 mm, ≤ chest line − 60 | a zero or negative rise inverting the front |
| cutaway run | 50 mm … side seam + button stand | a break landing outboard of the panel |
| tail break inset | ≥ 25 mm from the side seam | a zero-length `break` edge, which cannot close an outline |
| tail break | ≥ button stand + 40 mm | the break collapsing back onto the button |
| cutaway span | re-derived from the clamped break | arcs drawn over a span the panel does not have |
| armhole depth | 160 mm … 52% of the bodice | the chest line landing on the waist seam |
| front dart intake | 4 … 16 mm | a waist larger than the chest inverting the suppression |
| tail flare | ≤ 25% of the tail length, ≤ 160 mm | a tail wider than it is long |

`metadata.solved` reports `button_clamped` and `sweep_clamped` on every render, so a
clamped draft is visible rather than silent. The cartridge was probed at the min **and**
max of every one of its 15 parameters, at all-min, all-max and two mixed-extreme
combinations, and at each `target_piece` — 44 renders, all with zero error issues and
every declared seam balancing. The two hardest cases (maximum sweep on the shortest,
narrowest body; minimum sweep with the highest button on the largest body) were
inspected edge-by-edge rather than only counted as passes.

## Hardware

The single front button and the cuff buttons bridge to the Yantra4D
**`sew-through-button`** solid via `notion.hardware_ref`. `button_ligne` drives the
printed button, its hole spacing (`button_ligne * 0.635 / 3`, the standard proportion)
and the drilled buttonhole marks on the pattern — so the printed button and the mark it
must pass through can never disagree. `card_count` is 9: one front plus four per cuff.

A morning coat closes at **one** point. The single button is not a simplification of a
two-button front; it is what a cutaway front physically permits, since there is no
straight edge below it to carry a second one.

## Honest simplifications

- **Teaching-grade tailoring.** A fusible front plus a floating chest canvas panel; a
  full hand-padded canvas is future work. So is a drafted lining — lining is
  noted-and-costed in the BOM but not drafted, as in `suit-jacket`.
- **No drafted pockets.** A morning coat carries a breast welt and jetted hip pockets in
  practice. The commons' `suit-jacket` already demonstrates welt and jetted markings; a
  cutaway front has less room for hip pockets and their placement is a house decision,
  so drafting a default here would fix something the draft has no business fixing.
- **The under sleeve's scye is not part of the cap seam.** As in `suit-jacket`, the whole
  cap↔armhole relationship lives on the upper sleeve and the under sleeve tucks under —
  a teaching-grade two-piece rather than a fully split cap.
- **No braid, no facings in silk.** Morning coats are frequently made with silk-faced
  lapels and braided edges. Both are material choices the fabric card system would
  express better than the pattern, and neither changes the draft.
- **The lapel is drafted as a straight peak.** A slightly bellied lapel edge is more
  usual on a good coat; the straight peak is what balances cleanly against a
  bisection-solved collar and is what the commons' other tailored blocks use.

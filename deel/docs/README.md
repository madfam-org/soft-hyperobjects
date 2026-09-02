# Deel (дээл)

The wrap coat of Mongolia and Inner Mongolia: a full-length robe crossed right over left
and fastened along a diagonal, worn with a long sash (**бүс**, *büs*) wound at the waist.
Related forms are worn by Buryat, Kalmyk and Tuvan communities.

Part of the **Fashion Cabinet Commons** (FC-300, long-tail — heritage — Mongolian).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The two things an outside pattern most often gets wrong are the enger's diagonal and the
> blousing. This draft solves both from measurements rather than estimates.

## Provenance

The deel is **ordinary working dress**, not a costume. It is worn daily across rural
Mongolia and on formal occasions in the cities, and it is still commonly made at home. Its
construction answers a specific set of conditions — riding, severe cold, and being a long
way from a tailor — and every feature below is an answer to one of them.

This cartridge drafts an **everyday** deel. It is an original draft made from the
garment's construction logic, not a copy of any particular regional pattern.

## Why it earns its rank

**The энгэр (enger) is the garment.** The closure is not a straight centre front. The
right front carries a **stepped, angled flap** running from the neck across the chest to
the right underarm, with the fastenings spaced along it. That diagonal is the deel's
defining line, and it is the thing that goes wrong first:

- The flap's diagonal edge is **measured from its drafted polygon** (428.0 mm at the
  defaults).
- The body panel's own diagonal edge is then **solved to that measurement** by
  recomputing its run and re-solving its drop for the clamped result.
- The seam check confirms both read 428.0 mm exactly.

If these merely "nearly agree," the flap does not lie flat and the whole front twists.

**The collar is solved from measured necklines, not from a neck girth.** The enger's
angled neck edge is *longer* than the neck circuit it sits above. So the collar band's
length is the **sum of the measured curves** — two body necks plus the enger's neck edge
(422.7 mm at the defaults) — rather than a girth estimate that would come out short.

**Cut length ≠ worn length.** The deel is cut long and worn **bloused**: the sash is wound
at the waist and the body pulled up over it, forming a pouch that historically carried
everything from a bowl to a lamb. So this draft asks for the **worn** length — the length
on the body, which is what a wearer can actually state — and **solves the cut length** as
worn + `blouse_allowance`. At the defaults that is 1180 mm worn, **1330 mm cut**. A draft
that ignored this would be correct on the table and short on the body.

**The armscye is a measured curve** and the sleeve head is solved from it, growing from
237.6 mm to 309.6 mm as the chest goes from 1000 to 1250 mm.

**The fastening count is derived, not chosen.** It is an integer computed from the
measured diagonal and a comfortable spacing, because the fastenings have to space evenly
along that specific line.

## Construction notes

Pieces: **body** (cut 2), **enger** (chest flap, cut 2 — face and facing), **sleeve**
(cut 2), **collar** (zakh, cut 2), **sash** (büs, cut 1).

1. Sew the shoulders and set the sleeves into the measured armscyes. The sleeve carries a
   `nudarga` turn-back notch at 82% of its length — traditionally the sleeve runs past the
   fingertips and is turned back as a cuff, or left down against cold.
2. Close the side seams, leaving the marked riding vent open at the hem.
3. Assemble the **enger**: face it, topstitch its edges, and set its `diagonal` edge onto
   the body's `enger_diag` edge, matching the midpoint notches.
4. Set the collar onto the assembled neckline — two body necks plus the enger's neck edge.
   The collar's quarter notches match the shoulder seams.
5. Work the fastenings along the enger's diagonal at the drilled seats.
6. Hem. The `sash-line` marking shows where the büs winds and where the body blouses over
   it — check the worn length on the body with the sash on, not flat on the table.

A winter deel is lined and often wadded; a summer one is not.

## Hardware

The enger fastenings bridge to the Yantra4D `sew-through-button` solid via
`notion.hardware_ref`. `button_ligne` drives both the drilled fastening seats on the flap
and the printed solid's `sew_face` flange, so the garment's edge and the hardware's sewn
edge are dimensionally coupled.

## What is deliberately excluded

This is the **everyday** deel. Not drafted:

- **Ceremonial and festival forms** — the *khantaaz* and *khurim* deels.
- **Rank- and status-marking conventions** — the specific colours, trims and knot forms
  that signal marital status and standing.
- **Regional cuts.** Khalkha, Buryat, Kazakh and Torguud deels differ in **cut**, not
  merely in braid. A Buryat deel is a different draft, not this one with different edging,
  and offering the difference as a trim option would be false.
- **Monastic dress**, which is out of scope entirely.

These distinctions are how people read one another. Flattening them into a slider would be
exactly the costume-ification this commons refuses.

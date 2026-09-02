# Aṅgarkhā (अंगरखा)

The tie-fastened overlapping robe of northern South Asia. The name is from Sanskrit
**aṅga-rakṣaka**, "body-protector." Worn across Rajasthan, Gujarat, the Punjab and the
Deccan from the medieval period onward, in forms running from a hip-length everyday coat
to a full-skirted formal garment.

Part of the **Fashion Cabinet Commons** (FC-300, long-tail — heritage — South Asian).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> An asymmetric garment cannot be drafted by mirroring half a pattern — which is exactly
> why the asymmetry is the first thing lost when heritage clothing is industrialised.

## Provenance

The aṅgarkhā is a long-lived and widely varied garment. Its everyday forms were and are
ordinary working and formal dress across a wide region; its elaborated forms belonged to
Mughal and Rajput court wardrobes. What unites them is the **crossed, cut-away chest** and
the **cloth-tie fastening** — not a particular length, cloth, or degree of decoration.

This is an original draft made from the garment's construction logic. It is not a copy of
any particular regional or workshop pattern, and it deliberately drafts an everyday form
rather than a court one.

## Why it earns its rank

**The two fronts are different pieces.** This is the whole reason the cartridge exists.
Almost every garment in this commons — and almost every pattern block anywhere — is drafted
as a half and mirrored. The aṅgarkhā cannot be:

- The **right front** crosses over the left and is **cut away in a curve**, a rounded scoop
  from the neck outward and down.
- The **left front** lies beneath, and the portion the curve reveals is a **designed
  surface**, often cut in a contrasting cloth. It is not "what happens to be underneath."

So `outer_front` and `inner_front` are separate drafted pieces with different edge sets,
different internals, and different tie placements. The draft marks the `exposed-field` on
the inner panel so the maker can place contrast cloth deliberately.

**The curves are measured, and things are solved from the measurements.**

- The **armscye** is a real Bezier, not a straight drop. Its arc length is measured from
  the drafted curve (208.0 mm at the defaults) and the **sleeve head is solved from that
  measurement**. A draft that used the straight-line drop would produce a sleeve head
  shorter than the hole it has to fill. Perturb the chest to 1240 mm and the measured
  armscye grows to 280.9 mm, with the head following.
- The **overlap curve** is likewise measured (400.5 mm), and the inner front's exposed
  field is set from it so the two panels agree where they cross.

**The gore sets in flat.** The skirt gore's slant edge is measured from its own polygon
(661.0 mm at the defaults) and the body panel's lower side edge is **solved to that
measured length** by recomputing its horizontal run. This is the difference between a gore
that lies flat and one that nearly does — the latter puckers at the waist point, which on a
long skirt is where it shows most.

## Construction notes

Pieces: **outer_front** (cut 1), **inner_front** (cut 1), **back** (cut 1 on the fold),
**sleeve** (cut 2), **gore** (kalī, cut 4), **tie** (bandhan, cut 6).

1. **Stay-stitch the overlap curve before anything else.** At its steepest it runs close to
   the bias, and it will grow if handled unstayed.
2. Join the shoulders (both fronts to the back) and set the sleeves into the armscyes.
   The notch at the armscye midpoint matches the sleeve head notch.
3. Close the side seams above the waist point.
4. Set the four gores into the lower side seams, matching the gore-point notch to the
   waist notch on the body panels. Two gores per side — one to each front, one to the back.
5. Attach the ties: **three pairs**. Inner ties at the left underarm hold the under-panel
   down; outer ties at the right side hold the crossed panel. Tie inner first, then outer.
6. Finish the overlap curve with a narrow facing or bias binding, and hem.

There is no closure at the centre front — the garment is held entirely by the ties, which
is why their placement matters more than their decoration.

## Hardware

**None.** The aṅgarkhā is fastened entirely by cloth ties. There is no
`notion.hardware_ref` on this cartridge; adding a button, hook or snap would make it a
different garment.

## What is deliberately excluded

**The चकदार (chakdar) aṅgarkhā is not drafted.** That is the multi-pointed court form
whose hem is cut into four, six or more hanging points. It is a distinct and considerably
more complex garment associated with Mughal and Rajput court dress, and its point count
carried rank and occasion. Offering it as a slider on a coat pattern would misrepresent
what it was.

**The surface work is not drafted.** **Zarī**, **mukaish** and the block-print traditions
of the region belong to their own crafts and their own artisans. This draft provides the
panels and marks the exposed field; what goes on them is not the pattern's business.

# Zip-front rash guard

A zip-front long-sleeve rash guard in swim-lycra: the second-skin UV surf top, split down the
centre front and closed with a full **separating zipper** so it comes on and off wet without
dragging over the head.

Part of the **Fashion Cabinet Commons** (FC-400, lane 9 — active/structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Deepens the FC-100 [rash guard](../../rash-guard/docs/README.md) (a pull-on UV top, no
> hardware) into the zip version surfers and swimmers actually reach for — because a wet
> pull-on rash guard is a fight and a zip one is not.

## Why it earns its rank

**The zip is solved to the front length — the dimensional handshake.** The front is split into
a left and a right half, and the centre-front edges carry the separating zipper. The Yantra4D
`zipper` solid is parameterised by `zip_length`, and here `zip_length` **is** the drafted
centre-front run from hem to collar top, so the specified zipper is exactly as long as the
opening it closes. A zipper too short gaps at the collar; too long buckles the hem. Solving it
removes the guess.

**Negative ease still rules, but the zip tape is stable.** A rash guard is a second skin, cut
at negative ease so the lycra grips and does not billow. But the zipper tape is **not**
stretchy, so the centre-front is stabilised and the negative ease is taken up everywhere
**except** the zip line — the fronts close flat at the tape while the side and back keep the
grip.

## Construction notes

Pieces: **front_left**, **front_right** (the two zip halves), **back** (cut 1 on fold),
**sleeve** (cut 2, cap solved to the armhole ring), **collar** (stand, cut 1).

1. Join each front half to the back at the side seam and the shoulder (drafted congruent by a
   fixed shoulder-point drop).
2. Set in the sleeves — the cap run is **solved** to one front-half armhole plus the back
   armhole, so it sets in without easing a mismatch.
3. Apply the stand collar, its length the measured neckline run.
4. Stabilise both centre-front edges and set the separating zipper, running it up to the
   collar top.
5. Flatlock every seam so nothing chafes a wet body.

## Hardware

The zipper is a **Yantra4D solid** (`notion.hardware_ref → zipper`, linked), a full separating
front zip, never modelled here. `zip_length ← back_length` (the manifest map; the garment adds
the collar height so `zip_length == cf_run + collar` by construction).

## Made to measure

Drafted to **chest**, **waist** and **hip** girths plus **back** and **sleeve** lengths. Every
slider extreme (back length, bicep, collar height) renders watertight, including the
solved-to-ring sleeve cap.

# Wide-Brim Sun Hat

A **packable wide-brim sun hat** cut to the actual head: a six-gore crown, a straight
sweatband at the head line, and a wide shade brim. Pure soft goods — **no hardware**.

Part of the **Fashion Cabinet Commons** (FC-300 #213, Lane 2 — millinery). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

Crown gore (cut `gores`, mirrored), sweatband, and the brim (cut on fold + mirrored).

## Parameters

`head_girth` (ISO 8559), `crown_height`, `brim_width`, `gores`, `sweatband_height`,
`ease`, `seam_allowance`.

## Drafting

Three solves make the hat close:

- **Gore bases sum to the head opening.** Each gore's base is `(head_girth + ease) /
  gores`, so `gores` bases sewn together measure the sweatband's crown edge exactly.
  The seam is declared with the gore's `bottom` edge repeated `gores` times.
- **Gore side seams are symmetric**, so a gore's left seam and its neighbour's right
  seam measure the same run — declared gore-to-gore.
- **The brim is a half-annulus cut on the fold and mirrored**, so its drafted `inner`
  edge is a *half* ring. It is declared against the sweatband's head line as the brim's
  inner edge listed **twice** — the piece against its own mirror, join-to-join rather
  than join-to-fold. Arcs use a corrected radius (`r = C / (2n·sin(π/n))`) so the
  drafted polygon perimeter equals the intended circumference exactly.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

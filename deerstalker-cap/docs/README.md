# Deerstalker Cap

The **deerstalker**: a four-gore crown, twin peaks front and rear (the cap's defining
feature), and ear flaps that either cover the ears or fold up and tie across the crown
with self-fabric tapes. Pure soft goods — **no hardware**.

Part of the **Fashion Cabinet Commons** (FC-300 #218, Lane 2 — millinery). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

Crown gore (cut `gores`, mirrored), headband, peak (cut on fold + mirrored, four cuts
for the two peaks), ear flap (cut 2 mirrored), and two flap ties.

## Parameters

`head_girth` (ISO 8559), `crown_height`, `peak_length`, `flap_drop`, `gores`,
`headband_height`, `ease`, `seam_allowance`.

## Drafting — the head line is provably tiled

Two independent solves both land on the head opening:

- **The gore bases sum to it.** Each gore's base is `(head_girth + ease) / gores`, so
  `gores` bases sewn together measure the headband's crown edge exactly.
- **The peaks and flaps tile it.** Each peak takes 28% of the head line and the two ear
  flaps split what remains. That is declared as one seam: the headband's head line
  against four peak `back` listings plus two flap `head_edge` listings. Peaks are cut on
  the fold, so each drafted `back` edge is a *half* span — hence two listings per peak,
  the piece against its own mirror, **join-to-join** rather than join-to-fold. At
  defaults it reads `590.00 vs 590.00`.

Peak positions are carried on the headband as `marking` internals so the marker shows
where the front and rear peaks land.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

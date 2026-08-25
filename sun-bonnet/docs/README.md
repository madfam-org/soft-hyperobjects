# Sun Bonnet

The **working sun bonnet**: a stiffened front brim that shades the face, a gathered caul
covering the head, a neck curtain shading the nape and shoulders, and self-fabric ties
under the chin. Pure soft goods — **no hardware**.

Part of the **Fashion Cabinet Commons** (FC-300 #217, Lane 2 — millinery). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

Brim, caul and neck curtain (each cut on fold + mirrored), plus two chin ties.

## Parameters

`head_girth` and `neck_girth` (both ISO 8559), `brim_depth`, `caul_depth`,
`curtain_drop`, `caul_gather`, `curtain_gather`, `tie_length`, `seam_allowance`.

## Drafting — both gathers are real seams

The brim spans ~55% of the head girth, the caul's back ~42%. The caul is cut
`caul_gather` times the brim's head run and the curtain `curtain_gather` times the
caul's back run, and **each gather is declared as a seam with ease equal to the fullness
removed** — so the fullness is a checked dimension, not a sewing instruction. At defaults
they read `532.90 vs 313.50` and `335.20 vs 239.40`.

All three shaped pieces are cut on the fold, so every drafted edge is a *half* run. Each
is declared with the edge listed **twice** on both sides — the piece against its own
mirror, **join-to-join** rather than join-to-fold.

The brim carries a `cording` marking internal for the traditional corded stiffening: rows
of cotton cord between the two brim layers, which is how a bonnet stays washable and
still holds its shade.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

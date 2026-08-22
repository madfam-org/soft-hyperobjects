# Turban Band

A **pleated turban band**: a wide fabric band knife-pleated across its length, wrapped
around and sewn to a rigid Yantra4D [`headband-blank`](https://app.yantra4d.com), with a
knot panel at centre front for the signature twist.

Part of the **Fashion Cabinet Commons** (FC-300 #215, Lane 2 — millinery). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

Pleated band, knot panel, and the band lining that casings the blank.

## Parameters

`head_girth` (ISO 8559), `band_width` (the shared bridge dimension), `blank_arc`,
`pleat_ratio`, `knot_width`, `seam_allowance`.

## Drafting — the pleating is a real seam

The band is cut flat at `blank_arc × pleat_ratio` and **pleated down** onto the lining's
casing run (the blank's arc), so the pleats do the shaping rather than a curved seam.
That is declared as a seam **with ease equal to the fullness the pleats remove** — at
defaults it reads `612.00 vs 340.00` with 272 mm taken up, and it goes red if
`pleat_ratio` and `blank_arc` ever drift apart. Pleat positions are carried as `fold`
internals so the marker shows where each tuck falls.

The band is cut at double width and folds to `band_width`.

## Cross-commons bridge

`notion.hardware_ref` → `headband-blank`, mapping `band_w → band_width`,
`head_width → head_girth / 3` and `sew_holes → max(4, round(blank_arc / 60))`.

**Dimensional (band-width handshake).** The blank declares a `casing_sew_edge`
**flange** driven by `band_w`/`band_t`/`tip_w`/`sew_holes`. On the garment side the same
`band_width` drives the `casing` interface — the lining's casing edge and the band's own
casing edge. So the casing the fabric forms and the arc it encloses are one dimension.
Re-pointing that flange key at a non-interface parameter is detected as a handshake
failure.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

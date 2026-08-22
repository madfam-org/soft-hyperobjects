# Veiled Cocktail Hat

A small **perched cocktail hat with a birdcage veil**: a shallow gored crown on a short
side band, and a wide veil panel gathered down onto a Yantra4D
[`veil-comb`](https://app.yantra4d.com) bar through a self-fabric casing.

Part of the **Fashion Cabinet Commons** (FC-300 #214, Lane 2 — millinery). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

Crown gore (cut `gores`, mirrored), side band, birdcage veil (cut on fold + mirrored),
and the comb casing.

## Parameters

`head_girth` (ISO 8559), `bar_length` (the shared bridge dimension), `crown_dia`,
`veil_drop`, `gather_ratio`, `gores`, `band_height`, `seam_allowance`.

## Drafting — the gather is a real seam

The veil is cut on the fold, so the mirrored pair's **flat** heading run is
`bar_length × gather_ratio`. It is gathered down onto the comb casing, whose `bar` edge
measures `bar_length`. That relationship is declared as a seam **with ease equal to the
fullness removed** — so the check is substantive rather than decorative: at defaults it
reads `192.00 vs 80.00` with 112 mm of gathered fullness, and it goes red the moment
`gather_ratio`, `bar_length` and the casing drift apart.

The veil hem carries `allowances={"hem": 0.0}` — birdcage netting is cut raw and never
hemmed.

## Cross-commons bridge

`notion.hardware_ref` → `veil-comb`, mapping `bar_length → bar_length`,
`slot_count → max(3, round(bar_length / 16))` and
`slot_pitch → bar_length / max(3, round(bar_length / 16))`.

**Dimensional (gathered-width handshake).** The comb declares a `veil_gather_bar`
**flange** driven by `bar_length`/`slot_count`/`slot_pitch`. On the garment side the same
`bar_length` drives the `veil_heading` interface — the casing's bar edge and the veil's
gathered heading. So the finished gathered width and the hardware's sewn bar are one
dimension, not two that happen to agree. Re-pointing that flange key at a non-interface
parameter is detected as a handshake failure.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

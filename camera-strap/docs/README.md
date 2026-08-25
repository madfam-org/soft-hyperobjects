# Camera Strap

An **adjustable webbing camera strap**: two tails that thread the camera lugs, a
length-adjusting tri-glide slider, and a shaped shoulder pad with a webbing channel
through it so the pad slides to where the shoulder wants it. The slider bridges to the
Yantra4D [`tri-glide-slider`](https://app.yantra4d.com) — one slider is the entire
adjustment mechanism.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`tail` (webbing tail, cut 2) + `pad` (shoulder pad shell, cut 2 — face and lining) +
`channel` (webbing channel, cut 1).

## The seam that solves

The pad is a **lozenge whose long edges are Beziers** — bowing from a webbing-width end out
to the full pad width and back. That run has no closed form, so the channel's length is
taken from the *measured* `pad.inner` edge, and the channel-to-pad seam verifies exactly.

Four seams are declared and verified: the channel against the pad's inner run, the tail's
slider end against the pad end (both are the webbing width), the pad's outer edge against
its own mirror (face sewn to lining), and the two tails against each other — the slider
must see the same width from both sides.

`lug_taper` is additionally clamped to `webbing_width` in the script, so the lug end can
never be drafted wider than the webbing it narrows out of.

## Parameters

`strap_length`, `webbing_width` (drives the Yantra4D slider's webbing openings),
`pad_length`, `pad_width`, `lug_taper`, `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `tri-glide-slider`, mapping `webbing_w → webbing_width` and
`webbing_t → max(1.5, webbing_width / 14)`. **Dimensional**: the slider's sewn
`webbing_openings` flange is driven by `webbing_w`, and the same `webbing_width` drives
this strap's `slider_webbing` interface — enforced by `verify_hardware_links`.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

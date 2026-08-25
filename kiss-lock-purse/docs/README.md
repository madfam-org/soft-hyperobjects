# Kiss-Lock Purse

A curved-top clutch whose **mouth is sewn INTO the kiss-lock frame's channel**. The frame
bridges to the Yantra4D [`kiss-lock-frame`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`front` (purse panel, cut 2) + `gusset` (side/base gusset strip, cut 1).

## The seam that solves — edge-mated hardware

The kiss-lock frame is **edge-mated**, not a point fastener: the purse mouth has to follow
the frame's channel for its whole run. The run a mouth must match is the frame arch's
**arc length**, not the frame's chord width — a 200 mm frame with a 34 mm arch has a
215.07 mm channel run.

So this cartridge measures the frame's own arc (a circular arc through the two hinge
points and the crown, sampled at 48 segments) and then **bisects the mouth Bezier's bulge
until the mouth run equals that arc within 0.05 mm**. Across the whole clamp range —
including the extreme 90 mm frame with an 80 mm arch — the solved delta is 0.000 mm. The
mouth *seats* in the channel instead of being eased or stretched into it.

Three seams are declared and verified: both gusset long edges against a panel's
`side_r + base + side_l` run, and the mouth against its own mirror (front and back panels
take the two channel sides of the same frame, so their runs must be equal).

## Parameters

`frame_width`, `frame_arch`, `purse_depth`, `gusset_width`, `channel_width`,
`seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `kiss-lock-frame`, mapping `frame_w → frame_width`,
`arch_h → frame_arch`, `channel_w → channel_width`. **Dimensional**: the frame's sewn
`sew_channel` flange is driven by `frame_w` and `channel_w`, and those same garment
parameters drive this purse's `frame_mouth` interface — the hardware's channel and the
garment's mouth are the same numbers, enforced by `verify_hardware_links`.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

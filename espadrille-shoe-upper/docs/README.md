# Espadrille Upper

The closed **espadrille** (the classic flat slip-on): a single **vamp** over the toes and
instep and a **heel counter** round the back, joined at two side seams and stitched down to
a jute sole. The plain closed alpargata — no eyelets, no hardware.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — footwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Toe + instep; solved lasting arc, two straight side seams. |
| `heel_counter` | 1 | Back wrap; side seams drafted to the vamp's exactly. |

## Sizing — no invented landmark codes

ISO 8559 declares **no foot landmark codes**; drafted from **plain sized parameters**
(`foot_length`, `foot_girth`).

## Solving and clamps

Both lasting edges are **solved arcs** whose length is a **proportionate bow over each
piece's chord**, never a share of the whole sole perimeter (which slivers at the short-foot
/ wide-foot extreme). The counter's side seams are drafted to the vamp's side seam length
so both declared side seams verify at delta ≈ 0.

## Declared seams

`vamp.side_r ↔ heel_counter.side_l` and `vamp.side_l ↔ heel_counter.side_r`. The lasting
edge is a stitch-down (declared as an interface).

## Hardware

**None** — a closed slip-on espadrille has no hardware.

## Parameters

`foot_length`, `foot_girth`, `vamp_depth`, `counter_height`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

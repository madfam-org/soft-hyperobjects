# Lattice-Drape Printed Skirt

A made-to-measure A-line skirt of printed TPU accordion pleats — the drape is printed in,
not pressed, so it never falls out.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, am_fashion).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `panel` | 2 on the fold, mirrored | A-line skirt panel; the vertical pleat field. |

## Solving and clamps

The pleat **count** is derived from the panel width and the pitch, **floored at 2** (a
single pleat is not an accordion). The hip half is never below the waist half and the hem
half never below the hip half, so the A-line never inverts into an hourglass the kernel
would CCW-normalize into a healthy-looking sliver. The pleat depth is **clamped** under the
pitch so the accordion folds never cross. Verified at defaults, all-min, all-max, and every
parameter swung to each bound (including waist-larger-than-hip and a coarse pitch on a narrow
panel).

## Declared seams

The panel cuts on the fold (`cf`); the two panels join at the `side` seams (declared as an
interface).

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-pleat-panel`**, mapping `pleats`, `pleat_pitch`,
`panel_width` and `wall` from the panel dimensions and pitch. These are the panel's
**flange** params, so the `pleat_field` interface lists every driving param (`waist_girth`,
`hip_girth`, `hem_flare`, `pleat_pitch`, `wall`) — the dimensional handshake holds.

## Parameters

`waist_girth`, `hip_girth`, `skirt_length`, `hem_flare`, `pleat_pitch`, `pleat_depth`,
`wall`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

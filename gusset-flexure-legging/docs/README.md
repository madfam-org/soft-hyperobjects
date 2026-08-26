# Flexure-Gusset Performance Legging

A compression legging with a printed TPU **flexure gusset** at the crotch — a slit-and-hinge
diamond panel that stretches diagonally with the stride and returns.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 5 — AM-fashion). Official visualizer
and configurator: [Fashion Cabinet](https://fashioncabi.net).

## What FC owns vs Yantra4D

The flexure gusset is Yantra4D territory (`notion.hardware_ref → tpu-gusset-flexure`).
Fashion Cabinet owns the leg panel (sized from waist/hip/thigh/ankle girths, inseam and
rise) and the gusset diamond (`diag_w × diag_h`).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `placement-guide` | 2 mirrored | Tapered leg; crotch edge is the gusset seam; gusset diamond marked. |

## Solving and clamps

Every leg width is derived with **compression (negative) ease** and floored; the ankle
quarter is clamped **never wider than the thigh** so the taper never inverts. The gusset
diamond is floored.

## Cross-commons bridge

`notion.hardware_ref` → **`tpu-gusset-flexure`**, mapping `diag_w → gusset_w`, `diag_h →
gusset_h`, `wall`. All three are flange params driven by garment params in the
`gusset_seam` interface, so the **dimensional handshake** holds.

## Parameters

`waist_girth`, `hip_girth`, `thigh_girth`, `ankle_girth`, `inseam`, `rise`, `knit_ease`,
`gusset_w`, `gusset_h`, `wall`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Pattern-Weight Bag Set

A soft, non-marking cover for a printed pattern-weight core: two discs and a gusset band, cut
to the core so it holds tissue flat without marking or sliding.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `top` | 1 | Polygonised top disc. |
| `bottom` | 1 | Polygonised bottom disc. |
| `gusset` | 1 | Band cut to the measured disc circumference; turning gap. |

## Solving and clamps

The disc radius is the core radius plus the wall; the gusset length is the **measured**
(polygonised) disc circumference so the cover neither strains over the core nor bags loose.
The gusset height is **clamped** to at least the core height plus a seam, never a hairline
the kernel would still close. Verified at defaults, all-min, all-max, and every parameter
swung to each bound.

## Declared seams

`gusset.end_a ↔ gusset.end_b` (the band closes into a ring). The two discs seam to the
gusset's long edges at the measured circumference.

## Cross-commons bridge

`notion.hardware_ref` → **`pattern-weight`**, mapping `weight_dia`, `weight_h` and
`stack_clear` from the core dimensions. The pattern-weight declares no flange interface — the
cover holds the core, so no dimensional handshake is owed.

## Parameters

`core_dia`, `core_height`, `wall`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

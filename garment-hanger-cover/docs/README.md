# Padded Garment-Hanger Cover

A quilted slip-on cover that pads a bare hanger so a knit or a silk blouse hangs without
shoulder dents — two shell halves and a gathered hook cuff, drafted to the printed hanger
shoulder.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `shell` | 2 mirrored | Concentric inner/outer arcs; crown dart; hook slot. |
| `cuff` | 1 | Gathered hook-shaft tube. |

## Solving and clamps

The shell's inner edge (against the bar) and outer edge (the padded face) are two
**concentric arcs sharing one centre** — not per-radius centres, which collapse to a
zero-area lens on a shallow drop. Both are polygonised and **measured**, and the excess of
outer over inner is declared as the seam ease (half taken by a crown dart). The sagitta
relation R=(c²+s²)/2s solves the shoulder radius, and the drop is **clamped** under
0.85·half-span so the arcs never invert. Verified at defaults, all-min, all-max, and every
parameter swung to each bound.

## Declared seams

`shell.outer_arc ↔ shell.outer_arc` (the two halves), `shell.outer_arc ↔ shell.inner_arc`
(the concentric excess declared as ease), the two tips, and the cuff seam.

## Cross-commons bridge

`notion.hardware_ref` → **`garment-hanger`**, mapping `shoulder_w`, `bar_drop` and
`shoulder_t` from the hanger and pad. The garment-hanger declares no flange interface — the
cover slips over the hanger, so no dimensional handshake is owed.

## Parameters

`hanger_span`, `shoulder_drop`, `pad_girth`, `cuff_rise`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

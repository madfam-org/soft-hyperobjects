# Stirrup Knit Legging

A pull-on jersey legging with an under-arch **stirrup**: the leg continues past the ankle
into a narrow strap that passes under the foot and rejoins the leg, holding the hem down.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, knitwear).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 2 mirrored | Two-panel stretch tube; stirrup tongue below the ankle. |
| `back` | 2 mirrored | Deeper seat scoop on the inseam; side edge identical to the front. |

## Solving and clamps

Drafted with **negative ease** — the panel widths are the body quarters times a stretch
factor **floored at 0.62**, so an over-aggressive stretch can never draw a hairline panel
the kernel would CCW-normalize into a healthy-looking sliver. The two stirrup tongues are
drawn to the **same width** so the under-arch strap seam is flush, and the strap length is
**measured** (front tongue + back tongue). The seat fullness lives on the inseam scoop, not
the outseam, so the two side seams sew flush. Verified at defaults, all-min, all-max, and
every parameter swung to each bound.

## Declared seams

`front.side ↔ back.side`, `front.strap_end ↔ back.strap_end` (the under-arch strap), and
`front.inseam ↔ back.inseam` with the measured seat excess declared as ease (the back
inseam eases onto the front on the stretch).

## Cross-commons bridge

None — a pull-on knit with no closure. The folded waist casing takes elastic.

## Parameters

`waist_girth`, `hip_girth`, `ankle_girth`, `inside_leg`, `body_rise`, `stretch_factor`,
`stirrup_width`, `stirrup_drop`, `waist_casing`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

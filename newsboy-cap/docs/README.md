# Eight-Panel Newsboy Cap

The gavroche/newsboy: a full, soft **eight-panel crown** gathered to a covered button at
the apex, with a short stiff peak at the front.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — millinery depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `panel` | 8 | Crown wedge; base arc is a precise eighth of the head ring; straight sides to a short apex flat. |
| `band` | 1 | Headband. |
| `peak` | 2 mirrored | Stiff front peak (self + lining). |

## Solving and clamps

The eight panel bases **tile the band top exactly** (`8 × head/8 == head`). The panel sides
are **straight** so the wedge never degenerates at any rise (the earlier curved-seam draft
collapsed at the short-rise extreme). The apex flat is clamped below the base half so the
wedge stays a proper trapezoid, and the crown rise is floored.

## Declared seams

`8 × panel.base ↔ band.top`, and adjacent panels join `panel.seam_r ↔ panel.seam_l`.

## Cross-commons bridge

`notion.hardware_ref` → **`sew-through-button`** at the apex, mapping `button_ligne →
button_ligne`, `thickness → max(3, seam_allowance)`. `button_ligne` (a flange param) drives
the `apex_button` interface, so the **dimensional handshake** holds — the covered button is
sewn through, so it is point hardware.

## Parameters

`head_girth`, `ease`, `crown_rise`, `fullness`, `band_height`, `peak_depth`, `button_ligne`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

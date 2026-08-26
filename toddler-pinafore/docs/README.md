# Toddler Pinafore Dress

The pinafore (*pichi*): a sleeveless bib bodice over a gathered skirt, the shoulder straps
crossing at the back and buttoning to two growth rows so the dress lasts a season longer.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, kids_baby).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `bodice_front` | 1 | The bib; clamped top width. |
| `bodice_back` | 1 | Two strap-button growth rows. |
| `strap` | 2 | Crossed-back straps with a buttonhole end. |
| `skirt` | 1 | Gathered to the measured bodice waist. |

## Solving and clamps

The skirt gathers to the **measured** bodice waist — its fullness is declared as the seam's
ease against the real waist edge, so the gather is honest. The strap button rows are stepped
in off the bodice back's top edge so a growth adjustment never lands a button on the turned
edge. The bib top is **clamped** under the chest quarter so a small-body request never draws
a bib wider than the chest, folding the piece. Verified at defaults, all-min, all-max, and
every parameter swung to each bound.

## Declared seams

`skirt.waist` against the two summed bodice waists (declared as the gather ease). The strap
buttons and the gathered waist are declared as interfaces.

## Cross-commons bridge

`notion.hardware_ref` → **`sew-through-button`**, mapping the thickness, dish depth and card
count from `button_ligne`. The sew-face params (`button_ligne`, `hole_count`, `hole_dia`,
`hole_spacing`) are **left unmapped** — the button sits on the cloth face, no sewn seam, so
no dimensional handshake is owed.

## Parameters

`chest_girth`, `waist_girth`, `bib_height`, `skirt_length`, `bib_width`, `strap_length`,
`strap_width`, `gather_ratio`, `button_ligne`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

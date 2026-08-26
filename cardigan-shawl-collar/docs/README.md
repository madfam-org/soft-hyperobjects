# Shawl-Collar Cardigan

A drop-shoulder knit cardigan whose feature is a **continuous shawl collar**: one
collar-and-lapel that rolls from the back neck down both fronts to the placket hem, with
no shoulder-break seam.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 2 mirrored | Opens (not on fold); button band added outside centre front; drop-shoulder armhole; buttonholes marked. |
| `back` | 1 on fold | Drop-shoulder armhole. |
| `sleeve` | 2 | Straight head solved to the armhole length. |
| `collar` | 2 mirrored | Shawl strip; each half covers half the neckline. |
| `cuff` / `hem_band` | 2 / 1 | Rib bands, double-height, folded. |

## Solving and clamps

The button band is added **outside** the centre front, so the two fronts overlap by two
band widths when closed. The shoulder run is derived (quarter width less half neck) and
**floored at 45 mm** so a wide neck on a narrow body never inverts the yoke; the shoulder
slope is capped at `0.45 × armhole_depth`. The shawl collar strip length is **solved from
the measured neckline** — both fronts plus the full back neck — and each of the two
mirrored halves covers half of it, so the collar seam balances at delta ≈ 0. Knit ease is
signed and defaults **positive** (a cardigan is worn over layers).

## Declared seams

Armholes ↔ sleeve head edges, `front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`,
sleeve underarm to itself, and the two collar strips ↔ the full neckline
(`2×collar.neck_seam == 2×front.neck + 2×back.neck`).

## Cross-commons bridge

`notion.hardware_ref` → **`shank-button-solid`**, mapping `diameter_mm → button_dia` and
`thickness → max(3, seam_allowance)`. A shank button is **point hardware** (set through a
worked buttonhole, not sewn along an edge), and `shank-button-solid` declares no `flange`
interface, so per `hardware_dimensional_rules` no dimensional handshake is owed. The
buttonholes appear as `drill`-kind internals sized from `button_dia`.

## Parameters

`chest_girth`, `body_length`, `neck_girth`, `sleeve_length`, `knit_ease`, `armhole_depth`,
`front_neck_drop`, `shoulder_slope`, `band_width`, `collar_width`, `button_count`,
`button_dia`, `cuff_ratio`, `hemband_ratio`, `rib_height`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

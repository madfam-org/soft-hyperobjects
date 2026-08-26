# Hand-Sewn Moccasin Upper

The true **moccasin** (plug construction): a single **wraparound** piece that comes up from
under the foot and wraps the sides and heel, gathered at the toe, and a raised **plug** (the
apron) that fills the U-shaped throat and is whip-stitched to the gathered wrap. There is no
separate sole — the wraparound is the bottom.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — footwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `wrap` | 1 | Bottom-and-sides; U-throat at the front; the sole is part of this piece. |
| `plug` | 1 | Raised apron filling the U-throat. |

## Sizing — no invented landmark codes

ISO 8559 declares **no foot landmark codes**; drafted from **plain sized parameters**
(`foot_length`, `foot_girth`).

## Solving and clamps

The plug's three sewn sides (`sew_r + front + sew_l`) are measured, and the wrap's U-throat
is drafted as a symmetric V whose two sew edges sum to exactly that length. The throat
opening half-width is **clamped below the half-target** so the V can always reach the target
(a wide opening on a short sewn perimeter would otherwise be unreachable); the plug width is
clamped below the wrap half so the throat never inverts.

## Declared seams

`plug.sew_r + plug.front + plug.sew_l ↔ wrap.sew_r + wrap.sew_l` — the plug fills the
wrap's U-throat, balancing at delta ≈ 0.

## Hardware

**None** — a hand-sewn moccasin is whip-stitched.

## Parameters

`foot_length`, `foot_girth`, `plug_length`, `plug_width`, `side_height`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

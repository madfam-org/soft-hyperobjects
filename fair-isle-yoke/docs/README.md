# Fair Isle Yoke Sweater

The **circular-yoke** sweater: front, back and both sleeves join one **round yoke** — an
annular field worked in the round from the neckline to the underarm, with no shoulder or
armhole seam. That field is where the stranded **Fair Isle** colourwork lives.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `yoke` | 2 on fold | Half-annulus; outer = half the underarm ring, inner = half the neckline. Fair Isle bands marked. |
| `body` | 1 on fold | Straight tube; top feeds the yoke. |
| `sleeve` | 2 | Straight tube; top feeds the yoke. |
| `neckband` / `cuff` / `hem_band` | 1 / 2 / 1 | Rib bands, double-height, folded. |

## Solving — the ring sums exactly

The yoke's outer ring is the **exact sum of the four tube tops**: the body tube (full body
girth) plus two sleeve tubes (`SLEEVE_TUBE` each). Every ring is drafted on the
**corrected polygon radius** (`r = C / (2n·sin(π/n))`) so the drafted perimeter equals the
intended circumference. The inner (neckline) radius is **floored below the outer** so a
huge neck on a tiny body can never invert the annulus into valid-looking geometry after
CCW normalization. The draft girth is floored for negative-ease compression.

## Declared seams

The yoke `outer` (a half ring, cut on fold and mirrored — listed twice for the full ring)
takes the four tube tops: `body.top` twice (on-fold half-width) plus `sleeve.top` twice.
At defaults this balances 1552 mm ↔ 1552 mm, and at every extreme.

## Parameters

`chest_girth`, `body_length`, `neck_girth`, `sleeve_length`, `knit_ease`, `yoke_depth`,
`sleeve_frac`, `pattern_bands`, `cuff_ratio`, `hemband_ratio`, `neckband_ratio`,
`rib_height`, `neckband_width`, `seam_allowance`.

## Hardware

**None** — a yoke pullover has no closure.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

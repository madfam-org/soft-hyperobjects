# Chukka Boot Soft Upper

An ankle chukka upper: a vamp over the toes and instep, and two ankle-rise quarters carrying
two or three lace pairs on open-throat facings.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 3 — footwear soft goods III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Toe + instep; solved lasting arc below, throat above. |
| `quarter` | 2 mirrored | Ankle wrap; lace facing over the vamp; centre-back seam. |

## Sizing — no invented landmark codes

ISO 8559, as vendored, declares **no foot landmark codes**. This cartridge drafts from
**plain sized parameters** (`foot_length`, `foot_girth`, `ankle_height`); nothing is claimed
the schema cannot back.

## Solving and clamps

Both lasting edges are **solved arcs** whose length is a **proportionate bow over the piece's
own chord** — never a share of the whole sole perimeter, which degenerates into a sliver at
the short-foot / wide-foot extreme. The quarter facing seam is drafted to the vamp throat so
the declared seam balances, and the quarter back rises to at least the facing top so the
facing length is preserved. The ankle rise is **clamped** under 4× the quarter half-width so
the topline never folds through the lasting edge. Verified at defaults, all-min, all-max, and
every parameter swung to each bound.

## Declared seams

`vamp.throat_r ↔ quarter.facing`, `vamp.throat_l ↔ quarter.facing`, and the two quarters at
the centre back. The lasting edge stitches to the sole (declared as an interface).

## Cross-commons bridge

`notion.hardware_ref` → **`lacing-hook`**, mapping `hook_count`, `pitch` and `cord_dia` from
the lace pairs, ankle height and lace diameter. The sew-plate params (`plate_w`, `plate_t`,
`rivet_hole_dia`) are **left unmapped** — the hooks set through drilled holes, no sewn seam,
so no dimensional handshake is owed.

## Parameters

`foot_length`, `foot_girth`, `vamp_depth`, `ankle_height`, `lace_pairs`, `lace_dia`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

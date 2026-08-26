# Derby Shoe Upper

The **Derby** (open-lacing) shoe upper: a **vamp** over the toes and instep, and two
**quarters** whose eyelet facings sit over the vamp — the open throat that distinguishes a
Derby from an Oxford.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — footwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Toe + instep; solved lasting arc below, throat above. |
| `quarter` | 2 mirrored | Side + back wrap; eyelet facing over the vamp; centre-back seam. |

## Sizing — no invented landmark codes

ISO 8559, as vendored, declares **no foot landmark codes**. This cartridge drafts from
**plain sized parameters** (`foot_length`, `foot_girth`); nothing is claimed the schema
cannot back.

## Solving and clamps

Both lasting edges are **solved arcs** whose length is a **proportionate bow over the
piece's own chord** (`2 × half-width`), not a share of the whole sole perimeter — a lasting
arc far longer than its chord bows into a thin degenerate sliver at the short-foot /
wide-foot extreme (an early draft failed there). The quarter's facing seam is drafted to
the vamp's throat seam length so the declared seam balances at delta ≈ 0.

## Declared seams

`vamp.throat_r ↔ quarter.facing`, `vamp.throat_l ↔ quarter.facing`, and the two quarters
join at the centre back. The lasting edge is a stitch-down to the sole (declared as an
**interface**, not a seam).

## Cross-commons bridge

`notion.hardware_ref` → **`garment-eyelet`**, mapping `inner_dia → eyelet_dia`, `barrel_h →
max(3, seam_allowance)`. The eyelet is **point hardware** (set through a drilled hole), and
neither mapped key is a `flange` param, so no dimensional handshake is owed.

## Parameters

`foot_length`, `foot_girth`, `vamp_depth`, `quarter_height`, `eyelet_pairs`, `eyelet_dia`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Shoe-Horn Boot Sock

A tall knit boot sock with a heel channel holding a printed shoe-horn to guide the heel into
a tight boot without crushing the sock's back or bruising the achilles.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 3 — footwear soft goods III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `leg` | 2 mirrored | Tapered stretch tube; calf to ankle. |
| `foot` | 2 mirrored | Foot panel; ankle drafted to the leg ankle. |
| `channel` | 1 | Stiffened heel channel holding the shoe-horn. |

## Solving and clamps

The horn channel is cut to the **measured** shoe-horn length plus a seat and its width to the
scoop plus a clearance. Negative ease is **floored** (stretch factor ≥ 0.66) so a tight sock
never draws a hairline panel. The foot and leg panels join at a **measured** ankle seam so
the tube is continuous. Verified at defaults, all-min, all-max, and every parameter swung to
each bound.

## Declared seams

`foot.ankle ↔ leg.ankle` (the tube join) and `leg.seam_r ↔ leg.seam_l` (the leg back seam).

## Cross-commons bridge

`notion.hardware_ref` → **`shoe-horn`**, mapping `horn_len`, `scoop_w` and `blade_t` from the
horn. The shoe-horn declares no flange interface — the horn slides into the sock channel, so
no dimensional handshake is owed.

## Parameters

`calf_girth`, `ankle_girth`, `foot_length`, `leg_height`, `horn_length`, `horn_scoop`,
`stretch_factor`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

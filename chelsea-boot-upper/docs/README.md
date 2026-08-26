# Chelsea Boot Upper

The **Chelsea boot**: an ankle boot with no laces — a vamp, two quarters up the ankle, an
**elastic side gusset** each side that lets the boot pull on, and a back pull tab.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 6 — footwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Toe + instep; solved lasting arc. |
| `quarter` | 2 mirrored | Ankle wrap with a gusset opening; centre-back seam. |
| `gusset` | 2 | Elastic side panel filling the quarter's gusset opening. |
| `tab` | 1 | Back pull tab. |

## Sizing — no invented landmark codes

ISO 8559 declares **no foot landmark codes**; this cartridge drafts from **plain sized
parameters** (`foot_length`, `foot_girth`).

## Solving and clamps

Lasting arcs are **proportionate bows over each piece's chord**, never a share of the whole
sole (which slivers at extremes). The quarter's throat edge is drafted to the vamp's throat
side length **exactly** (an early draft capped it at the boot height and broke the seam at
the short-boot / deep-vamp extreme); the effective boot height is `max(boot_height,
throat_top)` so the shaft always contains the throat. The gusset opening is clamped below
the throat length and the gusset panel is built to that same length, so the declared seam
balances.

## Declared seams

`vamp.throat_r/l ↔ quarter.throat`, `quarter.gusset_edge ↔ gusset.attach`, and the two
quarters join at the centre back. The lasting edge is a stitch-down (declared as an
interface).

## Cross-commons bridge (co-create)

`notion.hardware_ref` → **`side-release-buckle`** *(co-create)* — the wearable buckle exists
in the yantra4d-500 catalog; this is its first Fashion Cabinet boot use, as the elastic
gusset tension element. Maps `webbing_w → webbing_w` (a flange param, driven by the
`gusset_tension` interface, so the **dimensional handshake** holds) and `wall_t → max(2,
seam_allowance)`.

## Parameters

`foot_length`, `foot_girth`, `boot_height`, `vamp_depth`, `gusset_width`, `gusset_height`,
`webbing_w`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

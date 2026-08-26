# Boot-Hook Pull Tab

A finger-loop pull tab sewn at the boot back, its hole cut to the boot-hook blade so a
boot-hook catches it to pull the boot on.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 3 — footwear soft goods III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `tab` | 1, folded | The loop tab with the hook hole and the attach end. |
| `facing` | 1 | Leather reinforcement behind the hole. |

## Solving and clamps

The hole is cut to the **measured** hook blade plus a clearance and stepped in off the loop
end by its own width plus a margin so it never tears out the fold. The tab length clears the
hook reach so the loop stands proud, floored to a real loop, and the tab width is **clamped**
to at least the hole plus the reinforcement. Verified at defaults, all-min, all-max, and every
parameter swung to each bound.

## Declared seams

None between pieces — the tab is a single folded outline; the hole is an internal cut.

## Cross-commons bridge

`notion.hardware_ref` → **`boot-hook-puller`**, mapping `blade_w`, `blade_t` and `hook_r`
from the blade and reach. The boot-hook-puller declares no flange interface — the hook passes
through the tab hole, so no dimensional handshake is owed.

## Parameters

`blade_width`, `blade_thick`, `hook_reach`, `tab_width`, `hole_clear`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

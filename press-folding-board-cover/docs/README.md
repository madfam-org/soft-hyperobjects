# Folding-Board Press Cover

A fitted padded cover that turns a shirt-folding board into a padded pressing surface — a top
and bottom panel wrapping the board, joined by a spine gusset, with elastic corners.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `top` | 1 | Top panel, board outline, corner elastics. |
| `bottom` | 1 | Bottom panel, corner elastics. |
| `spine` | 1 | Spine gusset the thickness of the board plus the pad. |

## Solving and clamps

The panels are the board face plus a **measured** wrap; the spine gusset is the board
thickness plus the pad. The corner pockets are **clamped** under a quarter of the panel so a
deep corner never crosses the panel centre and folds it. The pad wall is floored so the cover
always has a real pressing loft. Verified at defaults, all-min, all-max, and every parameter
swung to each bound.

## Declared seams

`spine.attach_a ↔ top.right` and `spine.attach_b ↔ bottom.right` (the spine joins the two
panels along the board's long edge).

## Cross-commons bridge

`notion.hardware_ref` → **`folding-board`**, mapping `fold_w`, `fold_h` and `panel_t` from
the board. The folding-board declares no flange interface — the cover wraps the board, so no
dimensional handshake is owed.

## Parameters

`board_w`, `board_h`, `board_thick`, `pad`, `wrap`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

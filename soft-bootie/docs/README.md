# Soft Bootie

An indoor **bootie** — a slipper that comes up over the ankle. Three pieces plus a padded
collar.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 4 — footwear soft goods). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `sole` | 2, mirrored | A lens of two solved arcs to a heel–toe chord. |
| `side` | 2, mirrored | Wraps toe → heel → toe; sole seam, centre back, collar line, vamp seam. |
| `vamp` | 1 | Toe closure; both side edges solved to the side panel's vamp seam. |
| `collar` | 1 | Padded band, cut double, with a fold line and a quilt line marked. |

## Solving

Two independent solves keep every seam honest:

1. **The sole** is a lens of two arcs, each bisected until its length equals the side
   panel's `sole_seam` run (the `baby-sleeper` sole-solver precedent — the right
   construction for any soft-sole footwear). Both attach seams then verify at delta ≈ 0.
2. **The vamp's** top corners are placed by Pythagoras so each straight side edge equals
   the side panel's `vamp_seam` exactly, rather than being drawn to a guessed height.

## Declared seams

| Side A | Side B | Note |
| :-- | :-- | :-- |
| `side.sole_seam` | `sole.attach_out` | One side panel to one sole arc. |
| `side.sole_seam` | `sole.attach_in` | The mirrored pair. |
| `vamp.side_r` | `side.vamp_seam` | Toe closure, right. |
| `vamp.side_l` | `side.vamp_seam` | Toe closure, left. |
| `side.centre_back` | `side.centre_back` | Self-seam: the mirrored panel meets itself at centre back (join-to-join, per the accessory self-seam rule). |
| `collar.attach` | `side.collar_line` ×2 + `vamp.throat` | Ease carries the band's joins and ankle clearance. |

## Sizing

`ankle_girth` is claimed as a true ISO 8559 landmark — a bootie genuinely clears that
ring. `foot_length` is a **plain sized parameter** with no `measurement` block, because
ISO 8559 as vendored declares no foot landmark codes. Nothing is invented.

## Cross-commons bridge

**None.** Rank 232 asks for `pattern` only; a soft bootie has no hardware — it pulls on.

## Parameters

`foot_length`, `ankle_girth`, `shaft_height`, `vamp_length`, `collar_pad`, `foot_ease`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

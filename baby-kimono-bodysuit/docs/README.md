# Kimono-Wrap Baby Bodysuit

The newborn bodysuit that wraps like a kimono — the left front crosses over the right and
fastens with sew-on snaps down the side, so it goes on without pulling anything over a
newborn's head. Kimono sleeves are cut in one with the body; a snap crotch gusset opens for
changes.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, kids_baby).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front_right` | 1 | Right front, kimono sleeve in one. |
| `front_left` | 1 | Left front with the wrap overlap and the snap run. |
| `back` | 1 | Back, kimono sleeve in one. |
| `gusset` | 1 | Snap crotch gusset. |

## Solving and clamps

The wrap overlap is a **real added extension**, clamped so it can neither vanish (nothing to
snap) nor pass the centre (a gaping wrap) — added cloth, not stolen. The shoulder and side
seams are drafted equal so the kimono shoulder sews flush, and each snap is stepped in off
the finished wrap edge so it seats on cloth. Verified at defaults, all-min, all-max, and
every parameter swung to each bound.

## Declared seams

`front_right/front_left.shoulder ↔ back.shoulder`, the `side`s and `sleeve_seam`s to the
back. The wrap and crotch snaps are declared as interfaces.

## Cross-commons bridge

`notion.hardware_ref` → **`sew-on-snap`**, mapping the disc thickness, stud and engagement
clearance from `snap_disc`. The sew-face params (`snap_dia`, `sew_holes`, `hole_dia`) are
**left unmapped** — the snap seats through the cloth face, no sewn seam, so no dimensional
handshake is owed.

## Parameters

`chest_girth`, `body_length`, `shoulder_width`, `sleeve_length`, `neck_width`, `overlap`,
`snap_disc`, `ease`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

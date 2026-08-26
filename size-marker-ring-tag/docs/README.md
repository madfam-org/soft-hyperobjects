# Size-Marker Ring Tag Set

A set of soft fabric size tags that thread onto a printed size-marker ring, the hole cut to
the ring rod so several sit on one ring without crowding.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `tag` | per ring | Chamfered fabric tag with a punched ring hole and a size field. |

## Solving and clamps

The ring hole is cut to the **measured** ring rod plus a clearance and stepped in off the tag
top by its own diameter plus a margin so it never tears out the top edge. The tag is
**clamped** to a legible minimum so a small ring never yields a tag too small to letter, and
the corner chamfer is clamped under 40% of the tag so it never crosses the tag centre.
Verified at defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

None between pieces — the tag is a single closed outline; the ring hole is an internal drill.

## Cross-commons bridge

`notion.hardware_ref` → **`size-marker-ring`**, mapping `rod_dia`, `ring_w` and `tab_h` from
the ring and tag. The size-marker-ring declares no flange interface — the tags thread onto
the ring, so no dimensional handshake is owed.

## Parameters

`tag_count`, `tag_width`, `tag_height`, `ring_rod`, `hole_clear`, `corner`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

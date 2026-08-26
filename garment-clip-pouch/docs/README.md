# Garment-Clip Travel Pouch

A slim divided pouch for a set of printed garment clips, sized to the clip footprint with a
fold-over flap.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 2 — the sewing-room shelf, care_keeping).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 1 | Divided clip bed (dividers + row lines). |
| `back` | 1 | Back with the fold-over flap. |

## Solving and clamps

The pouch is cut to the clip footprint (clip size × count) plus a margin, floored to hold at
least a couple. The **flap is clamped** shorter than the pouch height so the mouth is never
sealed shut. The divider count is derived from the per-row clip count, floored at 1. Verified
at defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

`front.bottom ↔ back.bottom` and `front.left ↔ back.left` (the taller back-with-flap declared
with the height ease).

## Cross-commons bridge

`notion.hardware_ref` → **`garment-clip`**, mapping `jaw_len`, `jaw_w` and `jaw_t` from the
clip footprint. The garment-clip declares no flange interface — the pouch holds the clips, so
no dimensional handshake is owed.

## Parameters

`clip_count`, `clip_length`, `clip_width`, `rows`, `flap`, `margin`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

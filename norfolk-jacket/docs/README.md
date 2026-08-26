# Norfolk Jacket

The Norfolk: a belted country tweed jacket with vertical box pleats front and back (they
give reach room for shooting and casting) and a self-fabric belt through side loops.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, tailoring).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 2 mirrored | Button stand, box pleat, belt loop. |
| `back` | 1 | Box pleat, higher round CB neck. |
| `sleeve` | 2 mirrored | Solved cap. |
| `collar` | 1 | Notch collar cut to the measured neckline. |
| `belt` | 1 | Self-fabric belt with a pointed tongue. |

## Solving and clamps

The sleeve cap is a **solved bow** whose length equals the measured front + back armhole, so
it sets in without easing a mismatch. The collar is cut to the **measured** neckline. The
box-pleat take-up is **clamped** under the panel half-width and **added** to the panel width,
not stolen from it, so a deep pleat can never consume the panel and fold it into a
self-crossing outline the kernel would still close and pass. Verified at defaults, all-min,
all-max, and every parameter swung to each bound.

## Declared seams

`front.shoulder ↔ back.shoulder`, `front.side ↔ back.side`, and `collar.lower` against the
four summed neck edges (declared as ease). The sleeve cap sets into the measured armscye
(declared as an interface).

## Cross-commons bridge

`notion.hardware_ref` → **`shank-button-solid`**, mapping `diameter_mm → button_dia` (and
thickness / rim proportionally). The shank-button-solid declares no flange interface, so no
dimensional handshake is owed.

## Parameters

`chest_girth`, `body_length`, `shoulder_width`, `armhole_depth`, `sleeve_length`,
`neck_width`, `back_neck_rise`, `pleat_depth`, `belt_width`, `button_dia`, `ease`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

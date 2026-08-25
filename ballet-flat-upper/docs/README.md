# Ballet Flat Upper

The upper of a **ballet flat**: a one-piece wrap cut on the fold at centre front, with a
deep scooped topline bound by a folded strip that doubles as an **elastic casing**, and a
single heel seam at centre back.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 4 — footwear soft goods). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `upper` | 1 **on fold** (centre front), mirrored | Lasting edge, scooped topline, heel edge; casing line marked. |
| `binding` | 1 | Folded strip = the casing; fold line and casing stitch line marked. |

Cut both again for the second shoe. The **sole unit** is out of scope — a hard good.

## The casing is the closure

This is the one cartridge in the lane that is **hardware-free by design**, and that is
the point of a ballet flat: no buckle, no zip, no part that can break and cannot be
replaced. Two numbers carry the whole closure, and both are drafted honestly:

```
CASING_W    = elastic_w + 2 × turn-under      # the binding's real folded width
elastic_len = topline_run − draw_in           # the elastic is cut SHORTER
```

The binding is drafted at twice `CASING_W` so it folds over the raw topline and actually
passes the elastic it must carry — the casing width follows the elastic, not a decorative
constant. The `draw_in` is the gather that holds the shoe on the foot; it appears in the
BOM as the real cut length of elastic rather than being left to the maker to guess.

## Declared seams

| Side A | Side B | Note |
| :-- | :-- | :-- |
| `upper.heel` | `upper.heel` | Centre-back self-seam: the mirrored piece meets its own heel edge (join-to-join, per the accessory self-seam rule — **not** join-to-fold). |
| `binding.attach` | `upper.topline` ×2 | The upper is cut on the fold, so the finished topline is twice the drafted edge; ease carries the binding's own joins. |

## Sizing

`foot_length` and `foot_girth` are **plain sized parameters** with no `measurement` block:
ISO 8559 as vendored declares no foot landmark codes. A ballet flat does not reach the
ankle, so `ankle_girth` is not claimed either — only what the garment actually touches.

## Cross-commons bridge

**None**, and deliberately so. Rank 234 asks for `pattern` only. The elastic casing
replaces hardware entirely; claiming a `hardware_ref` here would be inventing a bridge
where the garment genuinely has none.

## Parameters

`foot_length`, `foot_girth`, `topline_depth`, `heel_height`, `elastic_w`, `draw_in`,
`seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

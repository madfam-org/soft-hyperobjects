# Aran Cable Sweater

The **fisherman's Aran**: a heavy full-fashioned crewneck of cable, diamond and
moss-stitch panels. Architecturally a **drop-shoulder set-in** body — a wide, shallow
armhole and a straight sleeve head, the shape a hand-knitter works flat and seams.

Part of the **Fashion Cabinet Commons** (FC-400, Lane 4 — knitwear depth). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front` | 1 on fold | Straight sides, drop-shoulder armhole, scooped crew neck. |
| `back` | 1 on fold | As front, shallow back-neck drop. |
| `sleeve` | 2 | Straight drop-shoulder sleeve; head solved to the armhole length. |
| `neckband` / `cuff` / `hem_band` | 1 / 2 / 1 | Rib bands, drafted double-height and folded. |

## Negative-ease knit drafting

`knit_ease` is **signed** and defaults slightly negative (−20 mm): an Aran is worn
close, so the draft is a touch smaller than the measured chest and stretches on. The
draft girth is floored (`max(560, chest+ease)`) so it stays wearable at maximum
compression — the opposite sign convention from every woven block in the commons.

## Drop-shoulder solving and the clamps

The armhole is a straight vertical drop of `armhole_depth`; the sleeve head is a straight
run whose length equals the armhole opening **exactly**, so the armhole seam balances by
construction. The **shoulder run** is derived (quarter width less half neck width) and
**floored at 45 mm** — a wide neck on a narrow body would otherwise drive it to zero or
negative and invert the yoke into valid-looking geometry after CCW normalization. The
back-neck rise tracks the floored shoulder (the **back-neck-rise clamp lesson**): the
shoulder slope is capped at `0.45 × armhole_depth` so the neck point can never dip below
the underarm. The biceps is widened when it cannot contain the solved head run plus a
minimum crown, so the sleeve-head crown curve is never degenerate.

## Declared seams

`front.armhole ↔ sleeve.head_front`, `back.armhole ↔ sleeve.head_back`,
`front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`, and the sleeve underarm to
itself. All balance at delta ≈ 0 at every parameter combination, including the clamped
extremes.

## Cable architecture

The central cable panel (`cable_panel_frac` of the half width) and the underarm line are
marked as `marking` internals so the pattern carries the stitch plan, not merely the
silhouette.

## Parameters

`chest_girth`, `body_length`, `neck_girth`, `sleeve_length`, `knit_ease`,
`armhole_depth`, `front_neck_drop`, `shoulder_slope`, `cable_panel_frac`, `cuff_ratio`,
`hemband_ratio`, `neckband_ratio`, `rib_height`, `neckband_width`, `seam_allowance`.

## Hardware

**None** — a crewneck pullover has no closure.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

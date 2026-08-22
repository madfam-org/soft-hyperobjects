# Ankle Gaiter

A short tapered **wrap gaiter** worn over the boot top, closing up the front on a **ladder
of lacing hooks** and held down by an under-instep strap.

This is the cartridge that finally **consumes `lacing-hook`** — one of the two honestly
unbridged Wave-T shelf findings that FC-300 set out to claim.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 4 — footwear soft goods). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `wrap` | 1 | Tapered ankle→calf panel; hook drill points up both closure edges. |
| `instep_strap` | 1 | Passes under the boot so the gaiter cannot ride up. |

Cut both again for the second leg.

## The hook ladder is dimensional, not decorative

`hook_count` hooks at `hook_pitch` spacing occupy a real run:

```
HOOK_RUN = (hook_count - 1) × hook_pitch + hook_plate_w
```

The closure edge is then drafted to **at least** that run plus a plate width of clearance
at each end. If you ask for ten hooks at 45 mm pitch on an 80 mm gaiter, the closure edge
grows to 447 mm to hold the 419 mm the hooks need, rather than silently overflowing the
edge and drawing hooks off the end of the piece. The effective values are reported in
`metadata.solved` (`closure_len_mm`, `hook_run_mm`).

The drill points are placed on the **tapered** edge — their x-position is interpolated
between the ankle and calf widths at each hook's own height — so the ladder follows the
real edge rather than a straight line the piece doesn't have.

## Declared seams

| Side A | Side B | Note |
| :-- | :-- | :-- |
| `wrap.closure_l` | `wrap.closure_r` | The laced-shut closure — a self-seam, join-to-join. |
| `instep_strap.attach_a` | `instep_strap.attach_b` | Both mount ends, `strap_w` tall. |

Both verify at delta 0 by the symmetric taper.

## Cross-commons bridge — a flange handshake

`notion.hardware_ref` → [`lacing-hook`](https://app.yantra4d.com), mapping
`hook_count → hook_count`, `pitch → hook_pitch`, `plate_w → hook_plate_w`.

The lacing hook **does** declare a flange (`sew_plate`, driven by `plate_w`, `plate_t`,
`rivet_hole_dia`) — it is riveted to a sewn edge, not set through a point — so a
dimensional handshake is **owed, and paid**. `hook_plate_w` drives the garment's own
`hook_closure` interface as well as the hardware's sew plate, so the plate the maker
rivets and the edge it rivets to are the same millimetre.

Verified as genuinely engaged rather than vacuously passing: removing `hook_plate_w` from
the garment interfaces makes `hardware_dimensional_rules` report the uncoupled-edge
violation.

## Sizing

Both body parameters are **real ISO 8559 landmarks** and both are claimed:
`ankle_girth` and `calf_girth`. A gaiter wraps exactly those two rings, which is what
makes it honestly measurable where the rest of this lane cannot be — the schema declares
no foot codes, so no foot code is claimed anywhere in FC-300 lane 4.

## Parameters

`ankle_girth`, `calf_girth`, `gaiter_height`, `wrap_ease`, `hook_count`, `hook_pitch`,
`hook_plate_w`, `strap_w`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

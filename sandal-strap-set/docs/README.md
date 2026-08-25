# Sandal Strap Set

The strap set of a flat sandal: a buckling **ankle strap**, a forefoot **toe strap**, and a
**heel strap** linking them — all mounting to a footbed.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 4 — footwear soft goods). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `ankle_strap` | 1 | Buckle fold + `hole_count` prong holes down the tongue. |
| `toe_strap` | 1 | Crosses the forefoot, mount tab to mount tab. |
| `heel_strap` | 1 | Links footbed to ankle strap behind the heel. |

Cut all three again for the second sandal. The **footbed** is deliberately out of scope —
it is a hard good, not a soft good, and this repo's kernel is 2-D pattern drafting.

## One width, and why

Every strap in the set is exactly `strap_w` wide. That is not a simplification: a sandal
that mixes strap widths **cannot share hardware** — each width would need its own buckle,
its own slot, its own rivet spacing. Holding one width is what lets a single buckle size
serve the whole sandal, and it makes the strap-to-strap seams verify at delta 0 by
construction, since both mount ends are the same edge length.

## Declared seams

| Side A | Side B | Note |
| :-- | :-- | :-- |
| `heel_strap.attach_b` | `ankle_strap.attach_a` | The heel link joins the ankle strap. |
| `toe_strap.attach_a` | `heel_strap.attach_a` | Both meet at the footbed mount. |

Both verify at delta 0 — the shared `strap_w` *is* the joint.

## Cross-commons bridge — a real dimensional handshake

`notion.hardware_ref` → [`belt-buckle`](https://app.yantra4d.com), mapping
`strap_width → strap_w` and `prong_d → min(4, strap_w / 5)`.

This is the **dimensional** half of the handshake, not just name resolution. The buckle
declares `strap_anchor_flange` as a `flange`-type interface driven by `strap_width` — a
sewn mating edge. Per `hardware_dimensional_rules`, the garment parameter feeding that
flange must **also** drive one of the garment's own interfaces, and `strap_w` drives both
`buckle_strap_end` and `strap_mounts`. So the same millimetre flows to the strap's mount
edge *and* to the buckle's slot; they cannot drift apart.

Verified as genuinely engaged rather than vacuously passing: removing `strap_w` from the
garment interfaces makes `hardware_dimensional_rules` report the uncoupled-edge violation.

## Sizing

`ankle_girth` is claimed as a true ISO 8559 landmark (`{"standard": "iso_8559", "code":
"ankle_girth"}`) — the ankle strap genuinely wraps it. `foot_length` is a **plain sized
parameter** with no `measurement` block, because ISO 8559 as vendored declares no foot
landmark codes at all. Nothing is invented.

## Parameters

`ankle_girth`, `foot_length`, `strap_w`, `overlap`, `hole_count`, `hole_pitch`,
`heel_rise`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

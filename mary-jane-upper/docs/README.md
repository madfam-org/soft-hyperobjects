# Mary Jane Upper

The upper of a **Mary Jane**: a low-cut **quarter** with a scooped topline, closing at the
heel, crossed by an **instep strap** that buttons on the outer side.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 4 — footwear soft goods). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `quarter` | 1 | Lasting edge, scooped topline, heel seam; strap anchor + button position marked. |
| `instep_strap` | 1 | Buttonhole slot drafted at the real length for the chosen ligne. |

Cut both again for the second shoe. The **sole unit** is out of scope — a hard good.

## The ligne is the shared dimension

`button_ligne` is the **trade's own diameter unit**: 1 ligne = 0.635 mm, so a 24-ligne
button is 15.24 mm across. This cartridge treats it as the real number it is, and derives
the buttonhole from it:

```
BUTTON_DIA = button_ligne × 0.635
HOLE_LEN   = BUTTON_DIA + button_thickness     # the standard buttonhole allowance
```

So the **buttonhole is drafted, not decorated** — the finished hole actually passes the
button it is bridged to. If the chosen ligne needs a slot wider than the requested strap,
the strap widens to carry it (a 45-ligne button on a 10 mm strap request yields a 28.1 mm
strap, a 28.57 mm button, and a 36.58 mm slot) rather than drawing a hole off the edge of
the piece. Effective values are reported in `metadata.solved`.

## Declared seams

| Side A | Side B | Note |
| :-- | :-- | :-- |
| `quarter.heel_r` | `quarter.heel_l` | Heel self-seam — the piece's own two ends, join-to-join. |
| `instep_strap.attach` | `instep_strap.free_end` | Both strap ends, `STRAP_W` tall. |

## Cross-commons bridge — a flange handshake

`notion.hardware_ref` → [`sew-through-button`](https://app.yantra4d.com), mapping
`button_ligne → button_ligne`, `thickness → button_thickness`, `hole_count → 4`,
`card_count → 1`.

The button declares `sew_face` as a `flange` interface driven by `button_ligne`, so a
dimensional handshake is **owed and paid**: `button_ligne` also drives the garment's own
`button_closure` interface — the strap's free end and buttonhole edge. The same ligne
therefore sizes the hardware and the hole it must pass through.

Verified as genuinely engaged rather than vacuously passing: removing `button_ligne` from
the garment interfaces makes `hardware_dimensional_rules` report the uncoupled-edge
violation.

`hole_count` and `card_count` map to numeric literals — per `hardware_ref_rules` these are
constants, not parameter references, and carry no coupling obligation.

## Sizing

`foot_length` and `foot_girth` are **plain sized parameters** with no `measurement` block:
ISO 8559 as vendored declares no foot landmark codes. This upper does not reach the ankle,
so `ankle_girth` is not claimed either. Nothing is invented.

## Parameters

`foot_length`, `foot_girth`, `topline_drop`, `strap_w`, `strap_len`, `button_ligne`,
`button_thickness`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

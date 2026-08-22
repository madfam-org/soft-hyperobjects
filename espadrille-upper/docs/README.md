# Espadrille Upper

The **two-piece canvas upper** of an espadrille: a **vamp** over the toes and instep, a
**heel counter** round the back of the foot. They join at two side seams; the whole lower
edge — the **lasting edge** — is what the maker stitches down to a jute-braid sole. An
optional eyelet ladder up the counter takes ankle ties (the *alpargata con cintas*).

Part of the **Fashion Cabinet Commons** (FC-300, Lane 4 — footwear soft goods; the first
FC footwear cartridges). Official visualizer and configurator:
[Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 | Solved lasting arc below, turned topline above, two straight side seams. |
| `heel_counter` | 1 | Solved lasting arc, eyelet drill points when `eyelets` is on. |

Cut both again for the second shoe — the draft is one upper, a pair is two.

## Sizing — no invented landmark codes

ISO 8559, as vendored in `packages/schemas/body-measurements.schema.json`, declares **no
foot landmark codes**: there is no `foot_length`, no foot girth, no instep code in
`$defs/landmark_code`. This cartridge therefore drafts from **plain sized parameters**
(`foot_length`, `foot_girth` are ordinary millimetre inputs carrying no `measurement`
block). Nothing is claimed that the schema cannot back. `ankle_girth` *is* canonical, but
an espadrille upper does not reach the ankle, so it is not used here.

## Solving

Both lasting edges are **solved**, not eyeballed: the sole perimeter is split between the
two pieces by `vamp_depth`, and each piece's lasting edge is a Bézier whose bulge is
bisected until its arc length equals its share (the `baby-sleeper` sole-solver precedent).
The counter's top corners are then placed so each of its straight side seams equals the
vamp's exactly — so both declared side seams verify at delta ≈ 0.

## Declared seams

`vamp.side_r ↔ heel_counter.side_l` and `vamp.side_l ↔ heel_counter.side_r`. The lasting
edge is a stitch-down to the sole (a hardware-free construction operation, not a
fabric-to-fabric seam), so it is declared as an **interface**, not a `declare_seam`.

## Cross-commons bridge

`notion.hardware_ref` → [`garment-eyelet`](https://app.yantra4d.com), mapping
`inner_dia → eyelet_dia` and `barrel_h → max(3, seam_allowance)`.

**Point hardware, no edge coupling.** The eyelet's flange interface (`set_face`) is not
fed by this map — an eyelet is set *through a drilled hole*, not sewn along an edge, so
per `hardware_dimensional_rules` no dimensional handshake is owed. The eyelets appear in
the pattern as `drill`-kind internals on the counter and as a quantity line in the BOM.

## Parameters

`foot_length`, `foot_girth`, `vamp_depth`, `counter_height`, `eyelets`, `eyelet_pairs`,
`eyelet_dia`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

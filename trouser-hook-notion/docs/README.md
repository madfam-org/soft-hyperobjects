# Trouser Hook and Bar

A **Yantra4D-bridged notion** — the 2-D **waistband closure template** for the flat
hook-and-bar fastening tailored trousers use because a button would print through
under a jacket. Fashion Cabinet owns the closure geometry (underlap, insets, sew-hole
pattern); the plate **solids** are the Yantra4D
[`trouser-hook-bar`](https://app.yantra4d.com) cartridge, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (Wave T — findings II).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A **Closure Template** spanning both waistband ends: the hook plate on the underlap
and the bar plate on the overlap, offset by the underlap so the two meet with the fly
centred, each inset from the finished end and centred on the waistband height, with
their sew-hole crosses and a per-plate notch on the guide edge. The closure centre is
marked so the fly can be checked against it.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Closure Template** | `placement-guide` | Both plate footprints, sew-hole crosses, closure centre, per-plate notches. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `hook_width` | 18 mm | Must fit inside the finished waistband without showing at the edges. |
| `waistband_height` | 40 mm | Finished height; the plates are centred on it. |
| `end_offset` | 15 mm | Plate inset from the finished end and its turn-back. |
| `underlap` | 40 mm | Overlap of the two waistband ends; sets where the fly falls. |
| `sew_holes` | 4 | More holes spread the closure's strain across the waistband. |

## Relationship to the trouser garments

`suit-trousers` now carries its own link to `trouser-hook-bar`, mapping the
hardware's `hook_width` from the garment's existing `fly_width` — the cleanest
garment-side link in the wave, because `fly_width` already drives the garment's
`fly` interface and so is already dimensionally coupled. `dress-trousers` is
deliberately left alone; it references this cartridge in prose rather than spending
a hardware_ref slot.

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`trouser-hook-bar` cartridge, mapping `hook_width` and `sew_holes` straight through.
Resolution is enforced in CI by `scripts/qa/verify_hardware_links.py` against the
pinned snapshot `docs/interfaces/yantra4d-hardware.snapshot.json`.

`trouser-hook-bar` declares a `sew_plate` **flange** interface driven by
`hook_width`, `plate_t`, and `sew_holes`, so this link also carries the **dimensional
handshake**: both mapped parameters feed the hardware's sewn plate *and* drive this
cartridge's own `waistband_closure` interface.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the closure as *placement* — underlap, insets,
  hole pattern, and the template that transfers them to the waistband.
- **Yantra4D** (`trouser-hook-bar`): the closure as *solids* — hook plate, bar plate,
  wire.

## Provenance

Original draft for Fashion Cabinet. Commons license **pending the FC1 commons-license
ruling** (`LicenseRef-FC1-pending`).

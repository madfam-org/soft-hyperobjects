# Belt Buckle

A **Yantra4D-bridged notion** — the 2-D **strap tip template** for a centre-bar prong
buckle. Fashion Cabinet owns the strap (the fold-back, the prong slot, the punch-hole
pitch); the buckle **solid** is the Yantra4D
[`belt-buckle`](https://app.yantra4d.com) cartridge, referenced through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (Wave T — findings II).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A **Strap Tip Template** carrying:

- the **fold-back line and notch**, where the strap wraps the centre bar;
- the **prong slot**, cut on the strap centre line inside the fold;
- the **punch holes** as drill crosses with their outlines, at the given pitch;
- the **nominal-fit notch** on the middle hole, so the remaining adjustment is
  symmetric in both directions.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Strap Tip Template** | `placement-guide` | Fold-back, prong slot, punch holes, nominal-fit mark. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `strap_width` | 38 mm | Must match the buckle's inside frame width; 38 mm is the dress standard. |
| `buckle_return` | 70 mm | Fold-back around the centre bar before it is stitched. |
| `hole_count` | 7 | Odd counts put a hole exactly at the nominal fit. |
| `hole_pitch` | 25 mm | The fit resolution of the belt; 25 mm is the trade standard. |
| `hole_dia` | 5 mm | Should clear the prong with slack, not swallow it. |
| `tip_length` | 45 mm | Tail past the last hole, through the keeper. |

## Relationship to `webbing-belt` / `strap-buckle-notion`

`webbing-belt` bridges `strap-buckle` — a side-release or slide buckle for webbing,
which adjusts **continuously**. A centre-bar prong buckle adjusts in **discrete
steps**, so its hole pitch is the fit resolution and therefore a drafting parameter.
Different closure class, different cartridge; `webbing-belt` keeps its own link.

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`belt-buckle` cartridge, mapping `strap_width` through and pinning `bar_dia` to a
6 mm literal. Resolution is enforced in CI by `scripts/qa/verify_hardware_links.py`
against the pinned snapshot `docs/interfaces/yantra4d-hardware.snapshot.json`.

`belt-buckle` declares a `strap_anchor_flange` **flange** interface driven by
`strap_width`, `bar_dia`, and `frame_t`, so this link also carries the **dimensional
handshake**: `strap_width` feeds the hardware's anchor flange *and* drives this
cartridge's own `buckle_end` interface. (`bar_dia` is a numeric literal, which the
rule exempts — there is no garment dimension to couple.)

## How the two commons divide the work

- **Fashion Cabinet** (this card): the buckle as a *strap* — fold-back, slot, hole
  pitch, cut length.
- **Yantra4D** (`belt-buckle`): the buckle as a *solid* — frame, bar, prong, roller.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

# Webbing Belt

A **made-to-measure belt** — one strap piece with a folded buckle end, a pointed
billet, and punched adjustment eyelets. Fashion Cabinet owns the belt (total length
from the waist measurement, the taper, eyelet spacing so the **middle eyelet lands at
the measured waist**); the buckle **solid** is the Yantra4D
[`strap-buckle`](https://app.yantra4d.com) cartridge, bridged through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 3 — accessories). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Webbing Belt** | `strap` | The full strap: buckle fold, body, eyelet field, billet tip. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `waist_girth` | 900 mm | Sets belt length; the middle eyelet lands here (bound to the `waist_girth` landmark). |
| `strap_width` | 38 mm | Passed to the Yantra4D buckle so the strap fits its slot. |
| `tip_length` | 60 mm | Pointed billet past the last eyelet; `0` = square end. |
| `eyelets` | 5 | Adjustment holes; odd counts center cleanly on the waist. |
| `eyelet_pitch` | 25 mm | Center-to-center between holes. |
| `buckle_return` | 80 mm | The end that folds back through the buckle and rivets down. |

## The cross-commons bridge (`notion.hardware_ref`)

Linked to the Yantra4D `strap-buckle` cartridge, mapping the belt's `strap_width` to
the buckle's `webbing` slot width so the printed buckle fits the strap. Resolution is
enforced in CI by `scripts/qa/verify_hardware_links.py`. The strap threads the buckle
(no sewn edge), so the bridge is name + parameter resolution.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the belt as *pattern* — length to the waist, taper,
  eyelet layout, the billet.
- **Yantra4D** (`strap-buckle`): the buckle as a *solid* — the printable hardware.

## Provenance

Original draft for Fashion Cabinet. Commons license **pending the FC1 commons-license
ruling** (`LicenseRef-FC1-pending`).

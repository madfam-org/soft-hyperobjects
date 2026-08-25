# Watch Strap

A **made-to-measure two-piece watch strap** — the buckle half (lug end → tapered body
→ billet with eyelets) and the keeper half (lug end → tapered body → buckle tab +
floating keeper loop). Fashion Cabinet owns the strap (lug width, wrist-sized split,
taper); the lug adapter and buckle **solids** are the Yantra4D
[`watch-adapter`](https://app.yantra4d.com) cartridge, bridged through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 3 — accessories). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Watch Strap** | `buckle-half`, `keeper-half` | Both halves, tapered from the lug to the buckle. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `lug_width` | 20 mm | Where the strap meets the watch; passed to the Yantra4D adapter. |
| `wrist_girth` | 180 mm | Sets the combined strap length (bound to the `wrist_girth` landmark). |
| `taper` | 4 mm | How much each side narrows from lug to buckle. |
| `eyelets` | 6 | Adjustment holes on the buckle half. |

## The cross-commons bridge (`notion.hardware_ref`)

Linked to the Yantra4D `watch-adapter` cartridge, mapping the strap's `lug_width` to the
adapter's `lug_width` so the printed adapter matches the strap and the watch case.
Resolution is enforced in CI by `scripts/qa/verify_hardware_links.py`. The strap pins to
the spring bar (no sewn edge), so the bridge is name + parameter resolution.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the strap as *pattern* — lug width, wrist split,
  taper, eyelets.
- **Yantra4D** (`watch-adapter`): the lug adapter + buckle as *solids*.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

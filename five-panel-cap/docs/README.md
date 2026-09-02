# Five-Panel Cap

A **made-to-measure five-panel cap** from the head girth: five crown **gores** (a
front, two side, two back — the side and back cut ×2 mirrored), a stiffened **peak**
(half-ellipse on the fold), and a **snap-back tab**. Fashion Cabinet owns the cap (the
five gores summing to the head girth, the crown height, the peak); the snap **solid** is
the Yantra4D [`snap-fit`](https://app.yantra4d.com) cartridge, bridged through
`notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 3 — accessories). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Five-Panel Cap** | `front-panel`, `side-panel`, `back-panel`, `peak`, `snap-tab` | Five gores + peak + closure. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `head_girth` | 580 mm | The five gores sum to this at the headband (bound to the `head_girth` landmark). |
| `crown_height` | 130 mm | Gore height from headband to apex. |
| `peak_length` | 70 mm | How far the peak projects. |
| `snap_dia` | 12 mm | Passed to the Yantra4D snap so the tab holes fit. |
| `ease` | 8 mm | Added to the head girth. |

## The cross-commons bridge (`notion.hardware_ref`)

Linked to the Yantra4D `snap-fit` cartridge, mapping the cap's `snap_dia` to the snap's
`bore_dia` so the printed snap-back fits the tab holes. Resolution is enforced in CI by
`scripts/qa/verify_hardware_links.py`. The snap sets into the tab (no sewn edge), so the
bridge is name + parameter resolution.

## Drafting

Each gore spans `(head_girth + ease) / 5` at the headband and curves via two Bézier
edges to a shared apex, so all five seam smoothly into the crown. The peak is a
half-ellipse cut on its straight back edge and mirrored; the snap-back tabs carry two
rows of snap holes.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

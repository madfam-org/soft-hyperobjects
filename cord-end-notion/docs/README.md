# Cord End

A **Yantra4D-bridged notion** — the 2-D **cord cutting and tip guide** for the aglet
or bell tip that stops a drawcord fraying and lets it be threaded at all. Fashion
Cabinet owns the cord (cut length, crimp allowance, channel entry and exit); the tip
**solid** is the Yantra4D [`cord-end`](https://app.yantra4d.com) cartridge,
referenced through `notion.hardware_ref`.

Part of the **Fashion Cabinet Commons** (Wave T — findings II).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## What this cartridge produces

A **Cord Cutting Guide**: a full-cut-length strip with the cord drawn down the centre
at its true diameter, a **crimp zone** boxed at each tipped end with its crimp line as
a drill mark and a notch, and the **channel in / channel out** marks that show what is
left over as the two pull tails.

The cut length is *not* the finished length: each tip swallows its own length of cord
in the crimp, so the guide adds `tip_length` once per tipped end. Getting that wrong
by one tip is the reason a replacement drawcord comes out short.

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Cord Cutting Guide** | `placement-guide` | Cut length, crimp zones and lines, channel marks, notches. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `cord_dia` | 5 mm | Sets the tip bore — the tip must grip *this* cord. |
| `cord_length` | 900 mm | Finished, tip to tip; the cut length is longer. |
| `tip_length` | 20 mm | Cord swallowed per tip, added to the cut length. |
| `ends` | 2 | One tip for an anchored cord; two for a free drawcord. |
| `channel_run` | 700 mm | Casing length; the remainder becomes the two pull tails. |

## Relationship to `cord-stopper` / `drawcord-anchor`

Both of those bridge the Yantra4D `cord-lock` — the spring **stopper** that holds an
adjustment. This cartridge is the **tip**: a different finding on the same cord,
solving a different failure. A drawcord typically needs both.

## The cross-commons bridge (`notion.hardware_ref`)

This notion's manifest declares a **linked hardware reference** to the Yantra4D
`cord-end` cartridge, mapping `cord_dia` and `tip_length` straight through.
Resolution is enforced in CI by `scripts/qa/verify_hardware_links.py` against the
pinned snapshot `docs/interfaces/yantra4d-hardware.snapshot.json`.

`cord-end` declares a `cord_mouth` **flange** interface driven by `cord_dia`, `wall`,
and `bell_flare`, so this link also carries the **dimensional handshake**: `cord_dia`
feeds the hardware's mouth *and* drives this cartridge's own `cord_run` interface —
the cord the guide measures is the cord the tip grips.

## How the two commons divide the work

- **Fashion Cabinet** (this card): the tip as a *cord* — cut length, crimp allowance,
  channel run, pull tails.
- **Yantra4D** (`cord-end`): the tip as a *solid* — bore, wall, flare, lanyard eye.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).

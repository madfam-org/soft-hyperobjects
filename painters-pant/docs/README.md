# Painter's Utility Pant

**FC-400 #308 · workwear_uniforms · tier 2 · `fc` pattern kernel · hardware bridge (co-create) → Yantra4D `hammer-loop`**

The painter's pant: a straight loose leg in cotton duck, a hammer loop, thigh
brush/pencil pockets, and a double-knee zone. The hammer loop's stiffening insert
is a **co-created** Yantra4D solid this garment pulls onto the shelf.

## What it is

Five pieces: two mirrored front legs, two mirrored back legs, a waistband, the
hammer loop, and the brush/pencil pocket panel. `target_piece` selects any one
piece or the full `set`.

## Why it earns its rank

`workwear_uniforms` needed the painter's staple, and it carries a real demand-pull
co-creation: the loop-stiffening insert the shelf did not have.

## What is actually solved (not assumed)

### 1. The hammer loop cut to a MEASURED swing

```
hammer_loop_run_mm = 2·tool_clearance + strap_run + turnings
```

The co-created insert's `span` maps to the same `tool_clearance`, so the printed
part matches the sewn loop and holds it open for a one-handed drop.

### 2. The brush pockets pitched across the MEASURED panel

```
brush_pitch_solved_mm    : usable / (brush_count − 1)
brush_panel_was_clamped  : true at the extremes
```

Whole gaps recomputed so the last pocket lands on the panel.

### 3. Inseams balanced to zero, double-knee clamped

```
inseam_delta_mm         : 0.0    (tol=0.4)
double_knee_was_clamped : true at the extremes
```

A loose leg twists on an unequal inseam; a knee zone wider than the leg is
CCW-normalized into a healthy-looking inverted piece. Rendered at the min *and*
max of every parameter.

## Hardware bridge — co-creation

`notion.hardware_ref` names the Yantra4D `hammer-loop` solid with `linked: false`
— a **Group-B co-creation** under the FC-200 demand-pull ruling. The insert is not
yet in FC's pinned hardware snapshot, so the notion maps its params (`span ←
tool_clearance`) and logs the pull onto the wearables shelf. The hardware-link
lane only checks `linked: true` notions, so a co-create passes without a snapshot
entry.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/painters-pant/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front_leg`, `back_leg`, `waistband`,
`hammer_loop`, `brush_panel`. Presets: `classic-white`, `heavy-trades`,
`slim-decorator`.

# Children's Hooded Raincoat

**FC-400 #323 · kids_baby · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `snap-fit`**

A hooded raincoat for a child in PU-coated nylon: a snap storm-flap front, an
attached hood, raglan sleeves, and sealed seams.

## What it is

Five pieces: two mirrored fronts, a back on the fold, a raglan sleeve (cut 2), a
hood (cut 2), and a snap storm flap. `target_piece` selects any one piece or the
full `set`.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The rain garment fails in
two predictable places — the hood and the storm flap — both fixed here by
measurement.

## What is actually solved (not assumed)

### 1. The hood drafted to the MEASURED head

```
hood_face_final_mm : ≥ head_girth · 0.55
hood_clears_head   : true
```

A hood scaled from the neckline is far too small for a child's large head. Floored
on the head girth.

### 2. The storm flap wider than the snap gap

```
flap_width_final_mm : 2·(snap_stand + overlap), clamped ≥ 2·stand + 2·SA
flap_covers_gap     : true
```

A flap narrower than its gap lets water track down the snaps; a naive draft ties
flap width to a fraction of the chest and shrinks below the gap at small sizes.
The snaps are solved across the placket. Rendered at the min *and* max of every
parameter (raglan seams drafted to the measured body).

## Child proportion & safety

Drafted from `bodies/child-6y`. A soft drawcord in the hood brim, **not** a
cord-lock at the neck — a deliberate safety choice for a young child. Taped seams.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `snap-fit` solid. `bore_dia` is fed
from `snap_dia`, which also spaces the snap column. Covered by the storm flap.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/kids-raincoat/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `hood`,
`storm_flap`. Presets: `puddle-3y`, `long-mac`, `over-layers`. Body preset:
`bodies/child-6y`.

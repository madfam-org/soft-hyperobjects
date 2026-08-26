# Children's Anorak

**FC-400 #329 · kids_baby · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `cord-lock`**

A pullover anorak for a child in ripstop nylon: a half-zip front, a kangaroo pouch,
an attached hood, and a drawcord hem on a cord-lock.

## What it is

Five pieces: two mirrored fronts, a back on the fold, a raglan sleeve (cut 2), a
hood (cut 2), and a kangaroo pouch. `target_piece` selects any one piece or the
full `set`.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The pullover anorak is a
favourite child's shape whose whole risk is head clearance.

## What is actually solved (not assumed)

### 1. The half-zip floored so the opening clears the head

```
half_zip_floored_mm       : floored so neck + zip ≥ head girth
head_opening_mm           : neckline + 2·half_zip
head_opening_clears_head  : true
```

A pullover has no full front, so the head passes through the neckline **plus** the
half-zip. A zip cut to a fashion length jams over the head — frightening and
dangerous if it covers the face.

### 2. The hem drawcord reconciled with the cord-lock

```
hem_circ_mm       : the measured hem
cord_cut_mm       : hem + grip tail + cord-lock allowance
channel_width_mm  : driven by cord_dia so the cord runs free
```

### 3. The kangaroo pouch clamped

```
pocket_width_was_clamped : true at the extremes
```

Rendered at the min *and* max of every parameter (raglan seams drafted to the
measured body).

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `cord-lock` solid. `cord_dia` is fed
from `cord_dia`, which also sizes the drawcord channel. The half-zip is a
companion hard good, floored for head clearance.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/kids-anorak/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `hood`,
`pocket`. Presets: `trail-3y`, `packable`, `long-6y`. Body preset:
`bodies/child-6y`.

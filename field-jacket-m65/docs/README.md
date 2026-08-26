# Field Jacket (M-65 pattern)

**FC-400 #310 · workwear_uniforms · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `snap-fit`**

The M-65 field jacket: a snap-over-zip front, four bellows cargo pockets with
snap-down flaps, a stand collar with a concealed hood, and a drawcord waist.

## What it is

Six pieces: two mirrored fronts, a back on the fold, a sleeve (cut 2), a stand
collar (cut 2 on the fold), the snap storm flap, and a bellows cargo pocket with
flap (cut 4). `target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`workwear_uniforms` needed the M-65 — one of the most-copied jackets in the world
— and its signature is the snap column, which is exactly the kind of thing that
drifts when it is not solved.

## What is actually solved (not assumed)

### 1. The front snap run solved across the MEASURED storm flap

```
front_snap_pitch_solved_mm : run / (snaps − 1)
snap_end_clear_mm          : top under collar, bottom above the drawcord
```

Whole intervals recomputed so the last snap never lands in the hem drawcord.

### 2. The pocket-flap snaps placed by measuring each flap

Two snaps per flap, stepped in from each end by the snap diameter — never a fixed
offset that walks off a narrow flap or bunches on a wide one.

### 3. The bellows cargo pockets clamped against the front

```
pocket_width_was_clamped : true at the extremes
```

A pocket wider than the panel folds over the placket; the kernel CCW-normalizes
it into a healthy-looking outline. Clamped `≤ QUARTER_CHEST − 2·SA` and rendered
at the min *and* max of every parameter. The sleeve cap is eased to the measured
armscye.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `snap-fit` solid. `bore_dia` — the
socket the stud seats into — is fed from `snap_dia`, which also sizes and spaces
the whole snap column. The front zip is a companion hard good, marked and counted
(one bridged solid per notion — the snaps are the finding).

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/field-jacket-m65/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `collar`,
`storm_flap`, `pocket`. Presets: `og-107`, `cold-weather`, `trim-field`.

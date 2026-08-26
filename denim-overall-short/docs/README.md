# Denim Short Overall (Shortall)

**FC-400 #305 · denim · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `overall-buckle`**

The adult shortall: a bib front, crossing back straps on sliding overall buckles,
side-button waist openings, and short legs above the knee.

## What it is

Four pieces: two mirrored front legs, two mirrored back legs, a bib on the CF
fold, and a crossing strap (cut 2). `target_piece` selects any one piece or the
full `set`.

## Why it earns its rank

`denim` was the thinnest family (6 of 300). The shortall carries the family's bib
and cross-strap convention in an adult block, and its hard problem is the strap
length — the number a shortall lives or dies on.

## What is actually solved (not assumed)

### 1. The strap cut to a MEASURED path, buckle travel centred

```
strap_path_measured_mm : bib_height + back_rise + shoulder arc
buckle_travel_mm       : centred on the path
```

Too long and the bib sags, too short and it drags; the buckle absorbs the
difference only if the strap reaches its range. Derived, never entered.

### 2. The side opening solved across the measured seam

```
side_opening_len_mm         : taken out of the side seam
side_button_pitch_solved_mm : run / (buttons − 1)
```

The last button lands on cloth, not on the leg hem.

### 3. The bib clamped against the waist it sews to

```
bib_half_was_clamped : true at the extremes
```

Clamped `≤ QUARTER_WAIST − 12`; an inverted bib is CCW-normalized into a
healthy-looking piece. Rendered at the min *and* max of every parameter.

The inseams are balanced to zero (`inseam_delta_mm : 0.0`, `tol=0.4`), same fork
as the jeans (both side seams end at `FRONT_RISE`, the back waist tilts up to CB).

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `overall-buckle` solid. `strap_w` is
fed from `strap_width`, sizing both the buckle's slot and the strap that slides
through it; `button_dia` from `button_head`. The side buttons are marked, not
modelled.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/denim-overall-short/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front_leg`, `back_leg`, `bib`, `strap`.
Presets: `classic-shortall`, `gardener`, `short-short`.

# Toddler Dungaree

**FC-400 #321 · kids_baby · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `overall-buckle`**

A bib-front dungaree for a toddler: a bib, crossing back straps on sliding overall
buckles, and full-length legs — drafted from child measurements, not a shrunk
adult.

## What it is

Four pieces: two mirrored front legs, two mirrored back legs, a bib on the CF
fold, and a crossing strap (cut 2). `target_piece` selects any one piece or the
full `set`.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The everyday toddler
dungaree carries the family's bib/strap/buckle convention in a true child block.

## Child proportion, not a shrunk adult

Drafted from `bodies/child-6y`. `QUARTER_WAIST` is the hip quarter less a token
(no waist to draft to); the rise carries a nappy (`FRONT_RISE` shorter than
`back_rise`, the back fork deeper); the bib comes from the chest, clamped to the
waist; the hem is deep to let down as the child grows.

## What is actually solved (not assumed)

### 1. The strap cut to a MEASURED path, buckle travel centred

```
strap_path_measured_mm : bib_height + back_rise + shoulder arc
buckle_travel_mm       : centred on the path
```

A strap cut to a guessed length runs out of buckle in one season.

### 2. The bib clamped against the waist

```
bib_half_was_clamped : true at the extremes
```

An inverted bib is CCW-normalized into a healthy-looking piece. The inseams are
balanced to zero (`tol=0.5`). Rendered at the min *and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `overall-buckle` solid. `strap_w` is
fed from `strap_width`, sizing both the buckle's slot and the strap.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/toddler-dungaree/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front_leg`, `back_leg`, `bib`, `strap`.
Presets: `eighteen-months`, `two-years`, `three-years`. Body preset:
`bodies/child-6y`.

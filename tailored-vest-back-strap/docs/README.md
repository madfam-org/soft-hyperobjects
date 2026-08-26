# Cinch-Back Tailoring Vest

**FC-400 #320 · tailoring · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `strap-buckle`**

The cinch-back waistcoat: a tailored vest whose split back is drawn together by a
strap through a buckle, so the wearer nips the waist to fit.

## What it is

Four pieces: two mirrored fronts, two mirrored back halves, a cinch strap (cut 2),
and a welt (cut 4). `target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300), and the cinch-back vest
is the one waistcoat that fits a range of bodies from a single pattern — if the
strap reaches the buckle's range.

## What is actually solved (not assumed)

### 1. The strap cut to the gap PLUS the buckle's travel

```
back_gap_mm      : the measured centre gap
buckle_travel_mm : the cinch/let-out range
strap_cut_mm     : gap + travel + wrap + turnings
```

A strap cut to the gap alone cannot tighten, so the vest fits exactly one waist.
Cut to the gap plus travel, the same piece adjusts across a real range.

### 2. The front buttons pitched above the point

Same waistcoat logic as `waistcoat-6button`: the run is measured to the last
button above the divergence so the undone bottom button sits on cloth.

### 3. The point floored, the welts clamped

```
point_drop_was_floored : true at the extremes
welt_was_clamped       : true at the extremes
```

Both are rendered at the min *and* max of every parameter. The back halves'
shoulder and armscye match the front's so the seams close.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `strap-buckle` solid. `webbing` is
fed from `strap_width`, sizing both the buckle and the strap it grips. The front
buttons are a companion hard good, marked and counted.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/tailored-vest-back-strap/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `strap`, `welt`.
Presets: `classic-cinch`, `wide-adjust`, `low-point-6`.

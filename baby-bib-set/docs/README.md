# Bandana Feeding Bib

**FC-400 #325 · kids_baby · tier 1 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-on-snap`**

A bandana feeding bib: a rounded terry-backed triangle worn like a kerchief,
closing at the neck on a two-position growth snap.

## What it is

Two pieces: the bandana (cut 2 — face + terry) and a neck band (cut 2).
`target_piece` selects `bandana`, `band`, or the full `set`.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The feeding bib is the
humblest garment in the catalog, and its whole longevity turns on the neck
closure.

## What is actually solved (not assumed)

### 1. Two solved snap positions for growth

```
snap_tight_x_mm     : the tight setting
snap_loose_x_mm     : a growth step looser
snap_growth_step_mm : the step
```

Both are placed so neither lands off the band, so one bib fits a range as the baby
grows. A single-position bib chokes or falls off within weeks.

### 2. The bandana drop clamped

```
drop_clamped_mm    : floored ≥ 2·band_width, ≤ HALF_WIDTH·1.8
drop_was_clamped   : true at the extremes
```

It always covers the chest but cannot trail in the food; a drop larger than the
piece inverts it (CCW-normalized into a valid-looking piece). Rendered at the min
*and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-on-snap` solid, both by name and
dimensionally (`snap_dia ← snap_diameter`), the same number that sets the band
overlap.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/baby-bib-set/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `bandana`, `band`. Presets:
`newborn-drool`, `teething`, `toddler`.

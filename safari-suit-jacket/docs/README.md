# Safari-Suit Bush Jacket

**FC-400 #319 · tailoring · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

The safari (bush) jacket: a belted single-breasted jacket in cotton twill, four
bellows pockets, a self belt through loops, a camp collar, and epaulettes.

## What it is

Six pieces: two mirrored fronts, a back on the fold, a sleeve (cut 2), a camp
collar (cut 2 on the fold), a self belt, and a bellows pocket (cut 4).
`target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300). The safari jacket is the
belted utility-tailoring staple, and its whole fit turns on the belt reaching a
buckle.

## What is actually solved (not assumed)

### 1. The self belt cut to the MEASURED waist plus a tail

```
belt_tail_mm     : the tail past the buckle
belt_cut_mm      : waist + tail + wrap + turnings
belt_loop_pitch_mm : solved across the measured waist
```

A belt cut to the girth alone meets end-to-end and cannot fasten.

### 2. The four bellows pockets clamped against the panels

```
pocket_width_was_clamped : true at the extremes
```

A pocket wider than the front folds the panel over; the kernel CCW-normalizes the
inversion into a healthy-looking piece. Rendered at the min *and* max of every
parameter.

### 3. The buttons pitched above the belt line, the cap eased

The front buttons run from the neck to the belt line at a solved pitch; the sleeve
cap is eased to the measured armscye.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face, the buttonholes, and the front run. The belt
buckle is a companion hard good.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/safari-suit-jacket/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `collar`,
`belt`, `pocket`. Presets: `classic-safari`, `bush-long`, `trim-safari`.

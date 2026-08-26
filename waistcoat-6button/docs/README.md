# Six-Button Tailored Waistcoat

**FC-400 #313 · tailoring · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

The tailored waistcoat: a six-button front with a pointed hem, welted pockets, a
waist dart, a lining back, and a back cinch buckle.

## What it is

Three pieces: two mirrored fronts, two mirrored backs, and a welt (cut 4).
`target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300). The waistcoat is the one
where small errors show most, because it is worn open at the bottom button.

## What is actually solved (not assumed)

### 1. The six buttons pitched above the point

```
button_pitch_solved_mm       : run / (buttons − 1)
button_bottom_above_point    : true
```

The run is measured from the top button below the gorge to the last button above
the divergence, so the traditionally-undone bottom button sits on cloth, never on
the open point.

### 2. The front point floored so it cannot invert

```
point_drop_floored_mm : ≤ front_length·0.4
point_drop_was_floored: true at the extremes
```

A negative or excessive drop would cross the hem, which the kernel CCW-normalizes
into a valid-looking piece.

### 3. The welts clamped against the front

```
welt_was_clamped : true at the extremes
```

Clamped `≤ QUARTER_CHEST − 2·SA`; rendered at the min *and* max of every
parameter. The back's shoulder and armscye match the front's exactly so the seams
close — the fix the first draft needed, where the narrower back put the shoulder
7.6 mm off.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face, the buttonholes, and the six-button spacing.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/waistcoat-6button/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `welt`. Presets:
`morning-6`, `single-point-5`, `straight-hem-4`.

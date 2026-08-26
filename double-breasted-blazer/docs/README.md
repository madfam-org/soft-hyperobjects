# Double-Breasted Blazer

**FC-400 #311 · tailoring · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

The double-breasted blazer: two columns of buttons, a wide wrap, peak lapels, a
waist-suppressed body with two darts, and a two-piece tailored sleeve.

## What it is

Five pieces: two mirrored fronts, two mirrored backs, an upper sleeve (cut 2), an
under sleeve (cut 2), and a collar (cut 2 on the fold). `target_piece` selects any
one piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300). The double-breasted
jacket is the one most often drafted wrong at home, because its wrap, button
columns, and lapel roll are one interlocked system.

## What is actually solved (not assumed)

### 1. Wrap + two button columns + pitch, one solved system

```
wrap_mm                    : front-edge extension past CF
button_column_spacing_mm   : derived from the wrap
button_pitch_solved_mm     : run / (rows − 1)
```

The columns sit symmetric about CF at a spacing derived from the wrap; the rows
are pitched across the measured run from the roll to the hem. Guess the spacing
and the outer column falls off the front edge.

### 2. Waist suppression split between two clamped darts

```
total_suppression_mm    : QUARTER_CHEST − QUARTER_WAIST
bust_dart_was_clamped   : true at the extremes
waist_dart_was_clamped  : true at the extremes
```

A dart deeper than the panel is CCW-normalized into a healthy-looking piece.
Both are clamped and rendered at the min *and* max of every parameter.

### 3. The two-piece sleeve seams close by construction

The fore and hind seams run **vertical** at `sleeve_length` on both the upper
and under sleeve, so they measure identically at every size — the fix the first
draft needed, where angled cuff-taper seams drifted 3.7 mm apart at the chest
extreme. The sleeve cap is eased to the measured armscye.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face, the buttonholes, and the whole two-column layout.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/double-breasted-blazer/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `upper_sleeve`,
`under_sleeve`, `collar`. Presets: `kent-6x2`, `reefer-4x2`, `roomy-drape`.

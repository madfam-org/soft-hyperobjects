# Jetted-Pocket Unstructured Blazer

**FC-400 #317 · tailoring · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

The unstructured blazer: a soft, canvas-free single-breasted jacket in a
linen-wool blend, notch lapels, three jetted (besom) pockets, and a two-piece
sleeve.

## What it is

Six pieces: two mirrored fronts, two mirrored backs, an upper sleeve (cut 2), an
under sleeve (cut 2), a collar (cut 2 on the fold), and a notch lapel facing
(cut 2). `target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300). The unstructured jacket
is the accessible entry to real tailoring — and the one where a misplaced pocket
shows most, because there is no canvas to hide it.

## What is actually solved (not assumed)

### 1. Three jetted welts clamped against the panel

```
welt_was_clamped : true at the extremes
breast_welt_mm   : derived, clamped
```

A welt longer than the panel folds it over; the kernel CCW-normalizes the
inversion into a healthy-looking piece. All three are clamped and rendered at the
min *and* max of every parameter.

### 2. Button run + lapel facing solved together

```
button_pitch_solved_mm : run / (buttons − 1)
facing_covers_lapel    : true
```

The buttons are pitched across the measured front; the notch lapel facing is
derived from the measured lapel run so it always covers the roll.

### 3. The dart clamped, the cap eased low

Without canvas the dart does all the shaping, so it is clamped `≤
QUARTER_CHEST·0.24`; the two-piece sleeve's vertical seams close by construction
and the cap is eased low to the measured armscye.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face, the buttonholes, and the front run.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/welt-pocket-blazer/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `upper_sleeve`,
`under_sleeve`, `collar`, `lapel_facing`. Presets: `soft-3-roll-2`,
`summer-1-button`, `roomy-2-button`.

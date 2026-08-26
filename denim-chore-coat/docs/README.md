# Denim Chore Coat

**FC-400 #303 · denim · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

The workwear chore coat (bleu de travail): a boxy, square-shouldered jacket in
12 oz denim with three patch pockets and a two-piece collar band.

## What it is

Five pieces: two mirrored fronts, a back on the fold, a sleeve (cut 2), a collar
band (cut 2 on the fold), and a patch pocket (cut 3). `target_piece` selects any
one piece or the full `set`.

## Why it earns its rank

`denim` was the thinnest family (6 of 300). The chore coat is the family's plain
jacket — the most-copied workwear garment in fashion — and the natural home for a
solved button run and an eased sleeve cap.

## What is actually solved (not assumed)

### 1. The button run solved across the MEASURED placket

```
button_pitch_solved_mm : button_run / (button_count − 1)
button_end_clear_mm    : top and bottom held off collar and hem
```

Whole intervals are fitted across the measured placket between two end
clearances and the pitch recomputed, so the bottom button never lands in the hem
turn where its buttonhole would cut through the fold.

### 2. The sleeve cap eased to the MEASURED armscye

```
armscye_run_measured_mm : front + back armscye, built
cap_run_measured_mm     : the cap seam, built
cap_ease_mm             : worked-in ease (low — denim eases badly)
```

`declare_seam` checks the cap against the armscye at `tol=2.5` with the ease
declared, so a cap drawn independently of the armscye goes red.

### 3. The patch pockets clamped against the front

```
pocket_width_was_clamped : true at the extremes
```

A pocket wider than the panel folds over the placket and the kernel
CCW-normalizes it into a healthy-looking outline. Clamped `≤ QUARTER_CHEST −
2·SA` and rendered at the min *and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid. The
button's `button_ligne` — its face diameter — is fed from this garment's
`button_ligne`, which also sizes the buttonholes and the button spacing.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/denim-chore-coat/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `collar`,
`pocket`. Presets: `classic-chore`, `cropped`, `long-shop-coat`.

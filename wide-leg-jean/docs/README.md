# Wide-Leg Jean

**FC-400 #304 · denim · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `jeans-button`**

The wide straight jean: a single front pleat, a full leg falling straight from
the hip, and a deep turn-up.

## What it is

Five pieces: two mirrored front legs (with the waist pleat), two mirrored back
legs, a waistband, a fly (cut 2), and a front pocket bag (cut 4). `target_piece`
selects any one piece or the full `set`.

## Why it earns its rank

`denim` was the thinnest family (6 of 300). The wide leg is the silhouette the
straight jean does not cover, and it carries a real drafting lesson: where the
extra width goes, and how a pleat is reconciled with the waistband.

## What is actually solved (not assumed)

### 1. The pleat reconciled with the waistband

```
flat_front_waist_run_mm     : the front waist edge as drawn (with pleat)
pleat_depth_mm              : folded out
finished_front_waist_run_mm : flat − pleat
band_length_measured_mm     : 2·finished_front + 2·back + fly lap
```

The pleat is folded out *before* the waist is measured, so the band is cut to the
finished waist. A band cut to the flat waist is loose by the whole pleat depth on
both fronts.

### 2. The width added at hem and knee, not the hip

The seat (hip quarter) is unchanged; the width lives at the hem and knee, where a
wide leg wants it. The hem is clamped **no narrower than the knee**
(`hem_clamped_above_knee : true`) so a wide-leg jean cannot become a peg-leg by
accident.

### 3. The two inseams balanced to zero

`inseam_delta_mm : 0.0`, checked at `tol=0.4` — more leg to twist here, so it
matters more, same jean fork (rise carried at CB, both side seams equal).

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `jeans-button` solid. `head_dia` is
fed from `button_head`, which also sets the button's step-in from the band's
finished end. Four pocket rivets are marked, not modelled.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/wide-leg-jean/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front_leg`, `back_leg`, `waistband`,
`fly`, `pocket_bag`. Presets: `wide-straight`, `sailor-flare`, `clean-column`.

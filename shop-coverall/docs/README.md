# Mechanic's Shop Coverall

**FC-400 #309 · workwear_uniforms · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `zipper`**

The one-piece shop coverall: a bodice joined to a trouser at the waist, a full
centre-front two-way zipper, set-in sleeves, and chest/thigh pockets.

## What it is

Seven pieces: two mirrored bodice fronts, a bodice back on the fold, two mirrored
trouser fronts, two mirrored trouser backs, a sleeve (cut 2), a collar (cut 2 on
the fold), and a patch pocket (cut 3). `target_piece` selects any one piece or
the full `set`.

## Why it earns its rank

`workwear_uniforms` needed the coverall — the most-worn garment in any workshop —
and its whole fit turns on a single dimension: the zipper length.

## What is actually solved (not assumed)

### 1. The zipper specified to a standard length AT OR ABOVE the measured run

```
zip_run_measured_mm   : bodice CF + front rise
zip_length_chosen_mm  : nearest standard tape ≥ run
zip_overage_mm        : chosen − run
zip_at_or_above_run   : true
```

A zip short of the crotch cannot be stepped into. The choice is always at or
above the measured run, never below, and rounds to a real tape length.

### 2. The bodice and trouser waists reconciled

Both are drafted to the same `QUARTER_WAIST`, so the join closes at delta zero;
`declare_seam` catches a redraft that breaks it. The bodice sweeps out to
`QUARTER_CHEST` at the armhole — which is the fix the first draft needed, when the
bodice waist came off the chest quarter and the join was 30 mm out.

### 3. Cap eased to the armscye, pocket clamped

The inseams are balanced to zero (`tol=0.4`); the sleeve cap is eased to the
measured armscye; the chest pocket is clamped `≤ QUARTER_CHEST − 2·SA` and
rendered at the min *and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `zipper` solid. `zip_length` is fed
from the measured CF run (`front_rise + back_length`) and `chain_size` from
`zip_chain`. Two-way so the wearer can vent the crotch when kneeling.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/shop-coverall/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `bodice_front`, `bodice_back`,
`leg_front`, `leg_back`, `sleeve`, `collar`, `pocket`. Presets: `shop-standard`,
`insulated-roomy`, `trim-fit`.

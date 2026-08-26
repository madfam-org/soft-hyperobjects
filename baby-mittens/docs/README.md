# Baby Scratch Mittens

**FC-400 #330 · kids_baby · tier 1 · `fc` pattern kernel · pattern-only (no hardware)**

Thumbless scratch mittens for a newborn: a rounded mitten in soft cotton
interlock with an elastic cuff. The smallest garment in the catalog.

## What it is

Two pieces: a mitten (cut 4) and an elastic cuff (cut 2). `target_piece` selects
`mitten`, `cuff`, or the full `set`. This is a **pattern-only** garment
(`needs: ["pattern"]`) — its only closure is a soft elastic in a turned cuff.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). Scratch mittens are the
first thing many parents make for a newborn, and honestly carry no hardware — one
of the 25 pattern-only garments FC-400 ratified.

## What is actually solved (not assumed)

### 1. The cuff drafted to pass the HAND

```
cuff_open_final_mm : palm_width + ease  (≥ palm, not just wrist)
cuff_passes_hand   : true
```

A cuff drafted to the wrist alone will not pass the hand and the mitten cannot be
put on. `declare_seam` checks the cuff opening against the mitten's cuff edge with
the pass-the-hand margin as the declared ease.

### 2. The tip radius floored against the width

```
tip_radius_floored_mm : ≤ HALF_PALM − 4
tip_radius_was_clamped: true at the extremes
```

At the smallest sizes a tip larger than the width inverts the curve — geometry the
kernel CCW-normalizes into a valid-looking piece. Rendered at the min *and* max of
every parameter.

## Safety

Cotton interlock sheds no loose fibre a baby could pull into its mouth; every seam
turns inward so no allowance touches the skin; the cuff elastic is soft so it does
not mark the wrist. `hardware_bridge: false`.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/baby-mittens/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `mitten`, `cuff`. Presets: `newborn`,
`three-months`, `six-months`.

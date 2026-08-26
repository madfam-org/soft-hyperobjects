# Nehru Collar Jacket

**FC-400 #315 · tailoring · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `shank-button-solid`**

The Nehru jacket: a single-breasted straight-front jacket with a stand (mandarin)
collar closing to the throat, no lapel, and a two-piece sleeve.

## What it is

Five pieces: two mirrored fronts, a back on the fold, an upper sleeve (cut 2), an
under sleeve (cut 2), and a stand collar (cut 2 on the fold). `target_piece`
selects any one piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300), and the Nehru/bandhgala
— central to South Asian formalwear — was absent. Its whole difficulty is the
stand collar.

## What is actually solved (not assumed)

### 1. The stand collar bisected to the MEASURED neck

```
neck_run_measured_mm : both front necks + the back neck
collar_meets_at_cf   : true
```

The collar length is derived from the measured neckline so its two ends meet
exactly at the centre front where the fronts meet — a guessed length gaps at the
throat or overlaps and buckles. `declare_seam` checks the collar against the
neckline run.

### 2. The button run solved across the MEASURED centre front

Whole intervals recomputed so the top button clears the collar seam and the
bottom clears the hem.

### 3. The dart clamped, the sleeve cap eased

The waist dart is clamped `≤ QUARTER_CHEST·0.24`; the two-piece sleeve's vertical
seams close by construction; the cap is eased to the measured armscye. Rendered at
the min *and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `shank-button-solid` solid.
`diameter_mm` is fed from `button_dia`, which also sizes the button run.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/nehru-jacket/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `upper_sleeve`,
`under_sleeve`, `collar`. Presets: `classic-nehru`, `bandhgala`, `short-mao`.

# Toddler Footed Legging

**FC-400 #327 · kids_baby · tier 1 · `fc` pattern kernel · pattern-only (no hardware)**

A footed stretch legging for a toddler: one wrap-around leg piece per side with an
attached foot, drafted for a stretch knit with negative ease. No hard goods.

## What it is

Two pieces: a leg (cut 2, mirrored) and a foot (cut 2, mirrored). `target_piece`
selects `leg`, `foot`, or the full `set`. This is a **pattern-only** garment
(`needs: ["pattern"]`) — its only closure is a soft elastic in a turned waist
casing.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The footed legging is the
day-and-night baby basic, and it honestly carries no hardware — one of the 25
pattern-only garments FC-400 ratified.

## What is actually solved (not assumed)

### 1. Negative ease applied to GIRTHS only, lengths kept true

```
hip_girth_cut_mm   : hip · (1 − knit_stretch)
ankle_girth_cut_mm : ankle · (1 − knit_stretch)
lengths_kept_true  : true
```

Applying negative ease to every dimension (the common home error) rides the
legging up short and pulls the foot off the heel. Here the rise and inside leg
keep their measured length.

### 2. The foot reconciled with the measured ankle

`declare_seam` checks the leg's ankle edge against the foot's opening (both cut to
`HALF_ANKLE`), so the foot seam closes clean. Rendered at the min *and* max of
every parameter (the foot is drawn as a clean four-sided sole so it cannot
degenerate at the extremes).

## Child proportion

Drafted from `bodies/child-6y`: `FRONT_RISE` shorter than `back_rise` (the rise
carries a nappy); the foot from the child's own foot length.

## No hardware

`hardware_bridge: false`, `knit_negative_ease: true`. The only closure is a soft
elastic casing — a technique, not a hard good.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/toddler-legging/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `leg`, `foot`. Presets: `twelve-months`,
`two-years`, `firm-grip`.

# Baby Swaddle Cocoon

**FC-400 #328 · kids_baby · tier 1 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-on-snap`**

A swaddle cocoon (sleep sack) for a newborn: a tapered jersey tube with shoulder
snaps that open the top, so the baby is laid in rather than pulled over the head.

## What it is

Two pieces: the cocoon body (cut 2, on the fold) and a shoulder snap tab (cut 4).
`target_piece` selects `body`, `shoulder`, or the full `set`.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The swaddle cocoon is
where fit is a safety question, and it carries a dimensionally-bridged snap.

## What is actually solved (not assumed)

### 1. The hip deliberately looser than the chest

```
quarter_hip_final_mm    : hip + legroom, floored ≥ chest + 6
hip_looser_than_chest   : true
```

A swaddle that pins the legs risks hip dysplasia; a chest too loose lets the baby
slip down. The taper is floored so the hip can never invert below the chest — an
inverted tube the kernel CCW-normalizes into a valid-looking piece. Rendered at
the min *and* max of every parameter.

### 2. The shoulder snap dimensionally bridged

```
snap_diameter_mm : drives BOTH the shoulder overlap AND the solid's snap_dia
```

`sew-on-snap` declares a sewn `flange` interface driven by `snap_dia`, so the
shared `hardware_dimensional_rules` lane requires `snap_diameter` to also drive a
garment interface (`shoulder_snap`) — which it does. The same number flows to both
sewn edges.

## Safety

Hip loose enough for the legs to move (hip-dysplasia safe); chest snug so the baby
cannot slip down; shoulder-open so it is snapped over, never pulled over the head;
breathable single jersey.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-on-snap` solid, both by name and
dimensionally (`snap_dia ← snap_diameter`).

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/baby-cocoon/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `body`, `shoulder`. Presets: `newborn`,
`three-months`, `six-months-legroom`. Body preset: `bodies/infant-6m`.

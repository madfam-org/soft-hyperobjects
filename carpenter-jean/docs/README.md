# Carpenter Jean with Tool Loops

**FC-400 #302 · denim · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `rivet`**

The utility jean: a straight leg carrying a hammer loop, a thigh rule pocket, and
a stack of tool loops. Every load path terminates at a rivet, not a bar-tack.

## What it is

Six pieces: two mirrored front legs, two mirrored back legs, a waistband, the
hammer loop, the tool-loop panel, and the rule pocket. `target_piece` selects any
one piece or the full `set`.

## Why it earns its rank

`denim` was the thinnest family (6 of 300). The carpenter jean is the utility
staple — and it is the garment where the *hard goods* matter, which is exactly
where a print-at-home rivet earns its place.

## What is actually solved (not assumed)

### 1. The hammer loop cut to a MEASURED swing

```
hammer_loop_run_mm = 2·tool_clearance + strap_run + turnings
```

A hammer loop is not a fixed strip. It must clear the hammer's head with room to
drop the handle through, so its cut length is derived from a measured clearance.

### 2. The tool loops pitched across the MEASURED panel

```
loop_count           : whole loops
loop_pitch_solved_mm : usable_panel / (loop_count − 1)
```

The requested count is fitted to whole gaps across the measured panel width and
the gap recomputed, so the last loop always lands on the panel.

### 3. The rule pocket and loop panel clamped against the leg

```
loop_panel_was_clamped : true at the extremes
rule_width_was_clamped : true at the extremes
```

A piece wider than its panel folds back on itself and the kernel CCW-normalizes
it into a healthy-looking outline. Both are clamped `≤ QUARTER_HIP − 2·SA` and
reported, and rendered at the min *and* max of every parameter.

### 4. The rise carried at CB, the inseams balanced to zero

Same jean fork as `selvedge-jean`: both side seams end at `front_rise`, the back
waist tilts up to the raised CB, and the front inseam's bulge is bisected until
it measures the back's (`inseam_delta_mm : 0.0`, checked at `tol=0.4`).

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `rivet` solid, **dimensionally**. The
rivet's `cap_dia` — the flange that bears on the cloth — is fed from `rivet_cap`,
which also sets every rivet's step-in from the edges it lands between. The tool
loops and pocket rivets are marked, not modelled — one bridged solid per notion.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/carpenter-jean/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front_leg`, `back_leg`, `waistband`,
`hammer_loop`, `loop_panel`, `rule_pocket`. Presets: `framing`, `finish-work`,
`slim-utility`.

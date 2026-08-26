# Welder's Cotton Duck Jacket

**FC-400 #307 · workwear_uniforms · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

The welder's jacket in heavy cotton duck: a throat-high stand collar, a spark
storm flap over the placket, and generous set-in sleeves.

## What it is

Five pieces: two mirrored fronts, a back on the fold, a sleeve (cut 2), a stand
collar (cut 2 on the fold), and the storm flap. `target_piece` selects any one
piece or the full `set`.

## Why it earns its rank

`workwear_uniforms` needed protective wear that is safety-by-construction. The
welder's jacket is the archetype, and its safety lives in one dimension: does the
flap cover the placket.

## What is actually solved (not assumed)

### 1. The storm flap wider than the gap it covers

```
button_stand_mm         : buttons inboard of CF
flap_width_requested_mm : 2·(stand + overlap)
flap_width_final_mm     : clamped ≥ 2·stand + 2·SA
flap_covers_gap         : true
```

A flap narrower than its gap is worse than none. A naive draft ties flap width to
a fraction of the chest and shrinks below the gap at small sizes; here it is
derived from the actual gap and clamped so the protective feature can never
silently disappear.

### 2. The button run solved across the MEASURED placket

Whole intervals between two end clearances, pitch recomputed, so the top button
sits under the collar and the bottom clears the hem.

### 3. The sleeve cap eased to the MEASURED armscye

`cap_ease_mm` is low (duck eases badly), checked against the armscye at `tol=2.5`
with the ease declared.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face diameter, the buttonholes, and the spacing. The
buttons are covered by the storm flap so no spark reaches the thread.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/welder-jacket/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `collar`,
`storm_flap`. Presets: `shop-welder`, `heavy-fab`, `cropped-torch`.

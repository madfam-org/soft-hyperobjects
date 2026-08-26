# Double-Pleat Tailored Trouser

**FC-400 #316 · tailoring · tier 3 · `fc` pattern kernel · hardware bridge → Yantra4D `trouser-hook-bar`**

The dress trouser: two forward pleats, a curtained waistband closed by a
hook-and-bar (no button showing), a fly, and a clean straight leg.

## What it is

Four pieces: two mirrored front legs (with the two pleats), two mirrored back
legs, a curtained waistband, and a fly (cut 2). `target_piece` selects any one
piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300). The pleated dress trouser
is where home drafts most often go loose at the waist.

## What is actually solved (not assumed)

### 1. Both pleats folded out before the waist is measured

```
flat_front_waist_run_mm     : with both pleats
pleat_total_clamped_mm      : folded out
finished_front_waist_run_mm : flat − pleats
pleat_total_was_clamped     : true at the extremes
```

The band is cut to the finished waist plus the hook overlap. Cut to the flat run,
it is loose by both pleats on each front. The pleat depths are together clamped so
they cannot exceed the flat front waist and fold the panel through itself.

### 2. The hook-and-bar dimensionally bridged

```
hook_span_mm : drives BOTH the drafted overlap AND the solid's hook_width
```

`trouser-hook-bar` declares a sewn `flange` interface driven by `hook_width`, so
the shared `hardware_dimensional_rules` lane requires the garment param feeding it
(`hook_span`) to also drive a garment interface — which it does (`hook_bar_waistband`).
The same number flows to the garment's edge and the hardware's sewn flange.

### 3. The inseams balanced to zero

`inseam_delta_mm : 0.0`, checked at `tol=0.4`. Rendered at the min *and* max of
every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `trouser-hook-bar` solid, both by name
and dimensionally (`hook_width ← hook_span`). The fly zip is a companion hard
good, marked and counted.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/tailored-trouser-pleat/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front_leg`, `back_leg`, `waistband`,
`fly`. Presets: `classic-2-pleat`, `deep-drape`, `single-pleat`.

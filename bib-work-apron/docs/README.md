# Denim Bib Work Apron

**FC-400 #306 · workwear_uniforms · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `d-ring`**

The adjustable bib apron: one body panel on the fold, a D-ring neck strap, and two
wrap-and-tie waist ties.

## What it is

Four pieces: the apron body on the CF fold, a D-ring neck strap, a waist tie
(cut 2), and a divided patch pocket on the fold. `target_piece` selects any one
piece or the full `set`.

## Why it earns its rank

`workwear_uniforms` is a broad family, and the plain bib apron — the most-made
workshop garment — needed the D-ring version drafted as the default rather than
the upgrade.

## What is actually solved (not assumed)

### 1. The neck strap cut to its adjustment range

```
neck_adjust_range_mm : measured fraction of the drop
neck_strap_cut_mm    : drop + range + webbing + turnings
```

A D-ring adjusts only if the strap has a tail to thread. Cut to the nominal drop
alone, the ring is a stitched loop in disguise.

### 2. The waist ties cut to wrap and tie

```
waist_wrap_allow_mm : reach round the back
waist_bow_tail_mm   : tie in front
waist_tie_cut_mm    : half-waist + wrap + tail
```

A tie cut to the half-waist meets uselessly at the back.

### 3. The pocket and bib clamped against the body

```
bib_half_was_clamped    : true at the extremes
pocket_half_was_clamped : true at the extremes
```

An inverted piece is CCW-normalized into a healthy-looking outline; both are
clamped and rendered at the min *and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `d-ring` solid. `webbing` — the bar
width the strap threads — is fed from `dring_webbing`, which also sizes the neck
strap that runs through it. The tie and pocket anchors are marked, not modelled.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/bib-work-apron/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `body`, `neck_strap`, `waist_tie`,
`pocket`. Presets: `workshop`, `kitchen`, `narrow-frame`.

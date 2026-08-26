# Baby Knit Cardigan

**FC-400 #322 · kids_baby · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

A soft merino-jersey cardigan for a baby: a raglan-sleeve body with a button band,
drafted from infant measurements, not a shrunk adult.

## What it is

Four pieces: two mirrored fronts, a back on the fold, a raglan sleeve (cut 2), and
a button band (cut 2). `target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The baby cardigan carries
the family's most common home-sewing failure — a neckline too small for the head.

## What is actually solved (not assumed)

### 1. The neckline clears the head

```
neck_run_measured_mm : both front necks + back neck
head_girth_min_mm    : head · (1 − knit_stretch)
neck_clears_head     : true
```

A baby's head does not compress. A neckline cut to an adult chest proportion is
far too small to pass it, so the finished garment cannot be put on. Floored on the
head girth.

### 2. The button band solved across the MEASURED front

Whole intervals recomputed so no button lands in the neck rib or the hem; buttons
small and flush so they do not press on a baby lying down.

### 3. The raglan seams close by construction

The sleeve's raglan seams are drafted to the **measured** front and back raglan
lengths (`FRONT_RAGLAN`, `BACK_RAGLAN`), so they close — the fix the first draft
needed, where guessed apex points put the seams up to 5.7 mm apart. Rendered at
the min *and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face and the buttonholes.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/baby-cardigan/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `band`.
Presets: `newborn`, `six-months`, `twelve-months`. Body preset: `bodies/infant-6m`.

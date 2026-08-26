# Peak-Lapel Dinner Jacket (Tuxedo)

**FC-400 #312 · tailoring · tier 4 · `fc` pattern kernel · hardware bridge → Yantra4D `shank-button-solid`**

The dinner jacket: a single-button front closing at the waist, a satin-faced peak
lapel that rolls to a low break, jetted pockets, and a two-piece sleeve.

## What it is

Six pieces: two mirrored fronts, two mirrored backs, an upper sleeve (cut 2), an
under sleeve (cut 2), a collar (cut 2 on the fold), and a satin lapel facing
(cut 2). `target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300). The T4 dinner jacket is
the formal-tailoring archetype, and its hard problem is the satin lapel facing.

## What is actually solved (not assumed)

### 1. The satin lapel facing derived from the MEASURED lapel

```
lapel_run_measured_mm : lapel + gorge, built
facing_covers_lapel   : true
```

The facing outline is taken from the measured lapel run plus a facing width, so
it always meets the roll — a facing drawn to a guessed shape falls short (showing
cloth) or overhangs the buttonhole. `declare_seam` checks the facing's outer edge
against the lapel run.

### 2. The single button at the measured waist, welts clamped

```
button_y_mm       : the measured waist
welt_was_clamped  : true at the extremes
```

The link button sits at the waist so the jacket breaks correctly; the jetted
welts are clamped `≤ QUARTER_CHEST − 2·SA` so a welt wider than the panel cannot
invert it (the kernel would CCW-normalize it into a healthy-looking piece).

### 3. Collar and sleeve off the measured gorge/armscye

The two-piece sleeve's fore/hind seams run vertical at `sleeve_length` and close
by construction; the cap is eased to the measured armscye. Rendered at the min
*and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `shank-button-solid` solid.
`diameter_mm` is fed from `button_dia` — the covered link button and cuff buttons.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/peak-lapel-tuxedo/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `upper_sleeve`,
`under_sleeve`, `collar`, `lapel_facing`. Presets: `midnight-classic`,
`low-break-drape`, `slim-shawl-adjacent`.

# Morning Coat (cutaway)

**FC-400 #314 · tailoring · tier 4 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

Formal daywear, the descendant of the riding coat: below the single fastening
button the centre-front edge sweeps away in a continuous cutaway curve to the
side, and the coat continues behind as long tails.

## What it is

Six pieces: two mirrored fronts, two mirrored backs, two mirrored tails, an upper
sleeve (cut 2), an under sleeve (cut 2), and a collar (cut 2 on the fold).
`target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300). The morning coat is the
last living formal daycoat, and its defining feature — the cutaway sweep — is a
single hard curve.

## What is actually solved (not assumed)

### 1. The cutaway solved over a floored span

```
sweep_run_floored_mm  : the horizontal run, floored ≤ QUARTER_WAIST + 40
sweep_drop_mm         : the vertical drop, floored
cutaway_curve_measured_mm : the built sweep
```

The sweep is a Bezier whose span is derived from the button break and the side.
Both run and drop are floored, because at the extremes a negative span does not
fail — it inverts the front into geometry the kernel's CCW normalization launders
into a valid-looking outline. Rendered at the min *and* max of every parameter.

### 2. The tails a separate waist-seamed skirt

The tail is drafted to the measured back waist; `declare_seam` checks the back
waist against the tail waist so the seam closes at delta zero and the tails hang
on their own grain.

### 3. Button, lapel, and sleeve solved off measurements

The single button sits at the measured break; the two-piece sleeve's vertical
seams close by construction and its cap is eased to the measured armscye.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face and the buttonhole; the single fastening button
sits at the top of the cutaway.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/morning-tailcoat/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `tail`, `upper_sleeve`,
`under_sleeve`, `collar`. Presets: `ascot-morning`, `deep-cutaway`, `short-tail`.

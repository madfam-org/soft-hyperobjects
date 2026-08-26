# Frock Coat

**FC-400 #318 · tailoring · tier 4 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

The frock coat (levita, redingote): a waist-seamed knee-length double-breasted
coat — a fitted bodice above the waist, a full skirt hung below on its own grain.

## What it is

Seven pieces: two mirrored bodice fronts, two mirrored bodice backs, two mirrored
skirt fronts, two mirrored skirt backs, an upper sleeve (cut 2), an under sleeve
(cut 2), and a collar (cut 2 on the fold). `target_piece` selects any one piece or
the full `set`.

## Why it earns its rank

`tailoring` was one of the thinnest families (7 of 300). The frock coat — the
ancestor of every tailored coat — was absent, and its T4 difficulty is real: it
is two garments joined at a seam that shows every error.

## What is actually solved (not assumed)

### 1. Bodice waist and skirt top reconciled to one measured waist

```
waist_quarter_mm : both the bodice waist and the skirt top
```

`declare_seam` checks the bodice waist against the skirt waist (front and back),
so the waist seam — the whole reason a frock coat is cut this way — closes at
delta zero.

### 2. The skirt flare added at the HEM, not the waist

```
skirt_hem_quarter_mm : waist + flare/2
skirt_hem_ge_waist   : true
```

Flaring from the waist pulls the seam open; here the skirt falls straight from the
waist and flares only below. The flare is floored so the hem is never narrower
than the waist — an inverted panel the kernel CCW-normalizes into a
healthy-looking piece. The skirt front/back side seams measure equal by
construction (the wrap lives only at the front edge — the fix the first draft
needed, when the wrap spread across the whole hem put the seams 31 mm apart).

### 3. The double-breasted button system solved off the wrap

Same solved system as `double-breasted-blazer`. Rendered at the min *and* max of
every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face, the buttonholes, and the two-column layout.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/frock-coat/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `bodice_front`, `bodice_back`,
`skirt_front`, `skirt_back`, `upper_sleeve`, `under_sleeve`, `collar`. Presets:
`victorian-frock`, `riding-cut`, `short-frock`.

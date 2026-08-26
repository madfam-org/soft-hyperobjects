# Children's Pinafore Dress

**FC-400 #324 · kids_baby · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

A pinafore dress for a child: a bib bodice and a gathered skirt at a raised waist,
with shoulder straps that button to the bib for growth.

## What it is

Three pieces: a bib bodice on the CF fold, a skirt (cut 2 on the fold), and a
shoulder strap (cut 2). `target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The pinafore is the
grow-with-me child's dress, and it hinges on the strap adjustment.

## Child proportion

Drafted from `bodies/child-6y`: the waist sits high (short torso, no defined
waist); the skirt is gathered full; a deep hem lets down as the child grows.

## What is actually solved (not assumed)

### 1. The skirt gathered to the bodice waist

```
skirt_top_final_mm     : QUARTER_WAIST · gather_ratio (clamped ≥ waist + 10)
skirt_wider_than_waist : true
```

Clamped so the skirt is never narrower than the waist (which would stretch, not
gather). The finished waist seam closes at the bodice waist by construction.

### 2. The straps cut to a MEASURED path with button adjustment

```
strap_path_measured_mm : back rise + bib height + shoulder arc
button_adjustment_mm   : the growth run
```

A run of buttonholes lets the straps out. `bib_half_was_clamped : true at the
extremes` (an inverted bib the kernel CCW-normalizes into a healthy-looking
piece). Rendered at the min *and* max of every parameter.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face, the buttonholes, and the strap-adjustment run.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/child-pinafore/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `bib`, `skirt`, `strap`. Presets:
`school-3y`, `party-full`, `school-6y`. Body preset: `bodies/child-6y`.

# School Smock (Pinny)

**FC-400 #326 · kids_baby · tier 1 · `fc` pattern kernel · hardware bridge → Yantra4D `sew-through-button`**

A pull-on school art smock for a child: a loose overhead tabard with elbow-length
raglan sleeves, a back-neck button opening, and a big divided front pocket.

## What it is

Four pieces: a front on the CF fold, a back (cut 2, mirrored, with the CB slit), a
raglan sleeve (cut 2), and a divided front pocket. `target_piece` selects any one
piece or the full `set`.

## Why it earns its rank

`kids_baby` was one of the thinnest families (7 of 300). The school smock is made
by the classroom-full, and it fails at one place — the neck.

## What is actually solved (not assumed)

### 1. The back button slit floored so the head passes

```
back_slit_floored_mm     : floored so neck + slit ≥ head girth
head_opening_mm          : neckline + 2·slit
head_opening_clears_head : true
```

A closed neckline sized for the neck will not pass a child's large head; the
button closes the slit for wear.

### 2. The big front pocket clamped against the body

```
pocket_width_was_clamped : true at the extremes
```

A pocket wider than the front folds it over; the kernel CCW-normalizes the
inversion into a healthy-looking piece. Rendered at the min *and* max of every
parameter (raglan seams drafted to the measured body).

## Child proportion

Drafted from `bodies/child-6y`; elbow-length elasticated sleeves keep the cuffs
out of the paint; poly-cotton drill survives the hot wash.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-through-button` solid.
`button_ligne` drives the face and the buttonhole that closes the head-clearing
slit.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/kids-school-pinny/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `pocket`.
Presets: `reception`, `junior`, `big-pockets`. Body preset: `bodies/child-6y`.

# Selvedge Straight Jean

**FC-400 #301 · denim · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `jeans-button`**

The five-pocket straight jean cut for selvedge denim: the outseam is left on the
loom's finished edge and felled, so the outseam is the one edge that must stay
straight.

## What it is

Six pieces: two mirrored front legs, two mirrored back legs, a straight
waistband, a fly shield/facing (cut 2), a coin pocket, and a front pocket bag
(cut 4). `target_piece` selects any one piece or the full `set`.

## Why it earns its rank

`denim` was one of the two thinnest families in the 300-rank catalog (6 of 300).
The base straight jean was missing, and a selvedge jean is the one that carries
the family's defining convention: the outseam laid on the loom's finished edge.

## What is actually solved (not assumed)

### 1. The selvedge outseam is drafted straight

A selvedge edge is the finish, so it cannot be shaped. The `side` edge on both
legs is a straight line hem → knee → waist, felled with the white line showing.
Everything that would normally be taken out of the side seam is taken out
elsewhere.

### 2. The two inseams balanced to zero

A straight jean has no drape to hide a twist. The back inseam is drafted plain;
the front inseam's bulge is **bisected** until the two measure the same:

```
front_inseam_bulge       : (solved per size)
inseam_delta_mm          : 0.0
```

`declare_seam` checks the pair at `tol=0.4`.

### 3. The back rise carried at CB, not at the side

The naive back — waist edge level at the deeper back rise — lengthens the side
seam by the whole rise difference (40 mm at defaults) and twists the leg. Both
side seams instead end at the **same height** (`front_rise`); the back waist
tilts up from the side point to the raised centre back. That is the correct jean
fork, and the fix the first draft of this cartridge needed.

### 4. The waistband cut to the MEASURED waist

```
front_waist_run_mm       : measured off the built front
back_waist_run_mm        : measured off the built back (longer — it tilts up)
band_length_measured_mm  : 2·front + 2·back − seam + fly lap
```

A band cut to a laid-flat girth is always wrong by the fly lap and the shaping.
Here it is the sum of the panel waist runs as built.

### 5. The jeans button seats on cloth

```
button_head_mm : drives BOTH the solid's head AND the button's step-in
```

The button is stepped in from the band's finished end by its own head diameter
plus a clearance — never on the turned extension where it holds nothing. The
waist quarter is clamped `≤ QUARTER_HIP − 6` so a big waist cannot invert the
side seam, geometry the kernel would CCW-normalize into a healthy-looking piece.
Every derived dimension is clamped and rendered at the min *and* max of every
parameter as part of the build check.

## Construction notes

- **Cut selvedge-to-selvedge.** The outseam must fall on the finished edge.
- **Twin-needle gold at 7 mm** on the felled seams, the fly J-stitch, both pocket
  mouths, and the band.
- **Set the button on the extension**, not the fold; tap it with a die.
- **Rivet the front pocket corners and the coin pocket** (marked, not modelled).

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `jeans-button` solid,
**dimensionally**. The button's `head_dia` — the bearing head that shows on the
band — is fed from this garment's `button_head`, which is also what sets the
button's step-in from the band's finished end. `socket_dia`, `tack_dia` and the
heights are derived from the same head. The five rivets are a second finding:
marked (drill crosses) and counted, not modelled — one bridged solid per notion.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/selvedge-jean/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front_leg`, `back_leg`, `waistband`,
`fly`, `coin_pocket`, `pocket_bag`. Presets: `slim-32`, `classic-straight`,
`relaxed`.

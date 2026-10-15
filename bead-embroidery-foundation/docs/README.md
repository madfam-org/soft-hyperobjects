# Bead embroidery foundation

An original, shield-shaped foundation and flush backing for a beaded pendant or
ornamental insert. This is an **unranked jewellery technique enabler**, closing
the gap between decorative beadwork and a dimensioned, backed wearable ornament.
It claims no FC band slot. Canonical pattern geometry belongs in the soft commons;
beads, findings and other solid hardware remain outside this cartridge.

## Construction

1. Cut one foundation and one backing from stable, non-fraying materials suitable
   for the intended bead load and skin contact. The named perimeter is both the
   cut and joining line; no seam allowance is added.
2. Transfer the centre registration line, beading field and two attachment crosses.
   The crosses locate attachment planning points; they are **not pierced holes**.
3. Embroider the foundation within the guide and secure thread ends. Bead packing,
   individual bead positions and thread consumption require the maker's layout.
4. Align foundation and backing using the centre-top notch. Edge-overcast the
   seven corresponding perimeter edges. All seven edge pairs are declared and
   checked for length equality. This is a flush edge finish, not a turned seam.
5. Select, attach and test the chosen suspension separately. The cartridge does
   not qualify a finding, knot, load capacity or retention method.

The seven-edge shield is generated from first principles, with no cultural
pattern or attributed heritage claim. It is not a copy of a purchased pattern.
CERN-OHL-W-2.0 is declared in both manifest licence fields and supplied by the
commons root licence, with no cartridge-local licence file.

## Parameters and native outputs

| Parameter | Default | Range | Effect |
|---|---:|---:|---|
| `length` | 70 mm | 35–140 | Top-to-point dimension of both pieces |
| `width` | 45 mm | 25–100 | Widest span of both pieces |
| `embroidery_margin` | 5 mm | 3–12 | Controls proportional contraction of the beading field |
| `attachment_spacing` | 18 mm | 8–50 | Distance between the two upper registration crosses |

Contraction must be below one quarter of both length and width. Attachment spacing
must be at most 60% of width. Invalid combinations fail explicitly in the native
generator. The field uses scale `1 - 2 * embroidery_margin / min(width, length)`
about `(0, length / 2)`: **it is not a constant-distance offset**, and the value
must not be interpreted as a guaranteed clearance at every sloping edge.

SVG, DXF, native explode JSON and tiled PDF are supported. Pattern units are
millimetres and drafting coordinates are Y-up. There is no simulated assembled
jewellery mesh, drape model or solid export.

## Census and review status

The census read 516 base soft-commons manifests plus all five FC-100 through
FC-500 indexes (100 entries each). There was no bead-embroidery foundation
cartridge. The closest jewellery-labelled object, `jewelry-roll`, is a storage
roll rather than an ornament substrate. `structured-fascinator` is a shaped
headwear construction rather than a matched flat beadwork foundation and backing.
No index was changed. The user-requested jewellery catalogue is the demand
rationale; no unsupported market ranking is claimed.

All manifest labels and descriptions are drafted in en/es/fr/pt. **Human language
review is pending for all four languages, including Spanish trade vocabulary and
French/Portuguese wording.** Draft translation presence is not review evidence.

## Local native verification

Default parameters: `length=70`, `width=45`, `embroidery_margin=5`,
`attachment_spacing=18`. Changed probe: `length=95`, `width=60`,
`embroidery_margin=7`, `attachment_spacing=28`.

The local Fashion Cabinet runner emitted all four declared formats for both
cases: eight successful native exports. Every render reported:

```text
verify: pieces=2 errors=0 warnings=0
```

Both JSON payloads contain two pieces, seven passing seam checks and zero issues.
Piece area changes from 2472.75 to 4474.5 mm²; dimensions change from 45 × 70 to
60 × 95 mm. Attachment spacing changes from 18 to 28 mm. Checks also reported:

```text
fc-spec check: contract=garment-manifest files=1 failures=0
fc-spec check: contract=explode-json files=2 failures=0
All checks passed!  # ruff on main.py
```

[Native validation record](native-validation.json) retains dimensions, seam
measurements and hashes of the eight local exports. Temporary exports were
removed after inspection; hashes are a record of that run, not downloadable
artifacts. Validation used the local keystone environment and the owning native
Fashion Cabinet runner. The live commons CI specifies `SPEC_PIN` beginning
`142db180`; this local run does not assert that the environment is that CI pin.

This is a local macOS draft, not Linux CI evidence, human translation approval,
production readiness or maker qualification. Material stiffness, bead weight,
needle/thread suitability, edge durability, skin contact and attachment strength
need physical sampling. No price, body-fit guarantee or manufacturing approval is
asserted.

## Piece dispatch

`target_piece="pattern"` exports the complete set. `foundation`, `backing` are individual-piece targets; an unknown target fails. The complete construction is checked before selection. A subset retains only seams whose two sides are present; omitted cross-piece seams are counted explicitly in native `metadata.dispatch`. Subset exports retain the full-assembly BOM, explicitly labelled as such. Full-set geometry and seam declarations are preserved. The per-cartridge `tests/verify_native.py` checks default and changed full sets, every single-piece branch, retained/omitted seam scope, quantities and invalid-target rejection through the native runner.

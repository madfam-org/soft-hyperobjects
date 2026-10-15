# Woven Ribbon Jewel Panel

An original unranked jewellery enabler: a plain-weave panel made from two
perpendicular sets of finished-edge ribbon, with a marked textile backing.
The native result is three **cutting templates**, with source-derived cut
quantities and lengths. It is a flat construction guide, not a draped assembly.
It can inform a brooch, pendant or sewn garment ornament; attachment hardware
and a wearable assembly are not included or qualified.

## Census and provenance

Census on 2026-10-15 read the 516 starting commons manifests, all five FC band
indexes (`fc100` through `fc500`), and platform material cards. Searches included
ribbon, weaving, woven, ruban, cinta, fita, tejido and tecel. The closest existing
objects were `chainmail-panel` (an interface to solid link geometry),
`kente-wrap` and `kente-wrap-cloth` (garment cuts using woven cloth). None drafts
individual ribbon strips with an alternating crossing table for a jewellery
panel. Parallel jewellery work also includes a three-strip braid blank and
ribbon tie choker; those use different construction mechanisms. This object
claims no ranked garment slot and changes no band index.

Geometry is original rectangular drafting with the elementary `(row + column)
modulo 2 over/under rule. No designer pattern, named traditional motif or
cultural attribution is claimed. The root CERN-OHL-W-2.0 licence applies; both
manifest licence declarations agree. The object remains a local proposal,
subject to coordinator integration, commons review and the relevant CI lanes.

## Parameters and lengths

All dimensions use millimetres; the FC draft uses y-up coordinates.

| Parameter | Default | Supported range |
|---|---:|---:|
| `ribbon_width` | 6 | 4–12 |
| `columns` (warp strips) | 5 | 4–12, integers |
| `rows` (weft strips) | 7 | 4–16, integers |
| `gap` (flat separation) | 0.5 | 0–3 |
| `tail` (reserve at each end) | 12 | 10–30 |

`panel_width = columns * ribbon_width + (columns - 1) * gap`.
`panel_height = rows * ribbon_width + (rows - 1) * gap`.
Each warp strip is `panel_height + 2 * tail` long; each weft strip is
`panel_width + 2 * tail` long. The backing is the weft length by warp length.
Zero seam allowance makes the native outline the actual cut outline.

At defaults, cut five 6 × 69 mm warp strips, seven 6 × 56 mm weft strips,
and one 56 × 69 mm backing. The central panel is 32 × 45 mm, the crossing
table has 35 entries and total flat ribbon length is **737 mm**.

The nondefault wide preset (`columns=8`, `rows=6`, `ribbon_width=8`, `gap=1`,
`tail=15`) yields eight 8 × 83 mm warp strips, six 8 × 101 mm weft strips,
and one 101 × 83 mm backing. The central panel is 71 × 53 mm, there are
48 crossings and total flat ribbon length is **1270 mm**.

## Construction

1. Cut the quantities printed on the warp and weft templates from finished-edge
   ribbon. Cut the single backing from a non-fraying textile. Transfer placement
   marks using a method compatible with the chosen materials.
2. Place the warp strips vertically on the backing marks. The marked central
   rectangle excludes the adjustable tails.
3. Starting at the bottom, pass weft row 1 over warp column 1, under column 2,
   and alternate. Row 2 starts under column 1. Continue alternating every row.
   Native JSON metadata lists every crossing, its centre and the weft order.
4. After sampling the materials, secure the loose ends to the backing with
   hand tacks. Tack spacing, strength and thread quantities are not solved.
5. Verify the sample and choose a separately validated attachment before use.

The backing markings are literal placement guides. They do not depict a
physically settled weave. Material thickness, bending and take-up can reduce
the final panel dimensions: the tail parameter is an explicit reserve, **not**
a calculated compensation. Ribbon purchase waste is not included in the BOM.
There are no declared continuous sewn seams; zero seam checks does not verify
hand tacks. No hardware, friction, drape, strength, skin-contact suitability or
wearable safety is established by the native rendering checks.

`target_piece` supports `set`, `warp`, `weft` and `backing`; subset exports
retain full-assembly metadata and BOM, as stated in their metadata.

## Local verification

The owning Fashion Cabinet runner generated SVG, DXF, JSON and PDF for both
defaults and the wide preset. Each of the eight invocations exited 0 and printed:

```text
verify: pieces=3 errors=0 warnings=0
```

The `fc-spec check garment-manifest` result was:

```text
fc-spec check: contract=garment-manifest files=1 failures=0
```

Ruff reported `All checks passed!`. Native JSON assertions checked strip
quantities, bounding-box dimensions, total BOM lengths, crossing parity and
centres inside the central panel, plus minimum/maximum parameter cases and
individual-piece dispatch. Fractional rows were rejected. Generated temporary
exports are not part of this source cartridge.

These are local macOS checks using the available FC kernel. They are not a
Linux CI verdict, physical sample verification or a platform pin advancement.
The commons workflow declares SPEC_PIN `142db1802bbf9e1135ceae6c9c531c469f2d295b`
and FC_PLATFORM_PIN `e56247bee457b2e3adbb9dc5a4f88b33b21676f2`;
local platform execution uses the working checkout recorded by the coordinator,
not a claim that those CI pins were executed here.

## Language review

Manifest strings are supplied in English, Spanish, French and Portuguese as
an agent-authored draft. **Human review remains pending for all four, especially
French and Portuguese.** No reviewed-translation claim is made. Native runtime
labels and this technical construction guide are currently English.

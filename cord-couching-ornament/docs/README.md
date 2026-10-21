# Cord-couching ornament

Original parametric textile foundation for a pendant panel, cuff insert or other
wearable ornament. The model drafts a rectangular non-fraying foundation, a
sinusoidal cord center route and transverse couching stitch marks at equal
arc-length stations. The foundation is cut; the route and stitches are transfer
marks, never cutting lines. The orientation arrow can align nap or material
direction. All dimensions are millimetres, in the native FC y-up drafting frame.

This is an **unranked technique enabler** dedicated to jewellery construction. It
is not a complete wearable closure or a garment and claims no ranked band slot.
Use a separately designed, tested attachment to connect the finished panel to a
pendant bail, cuff or garment. Surface couching stitches are not paired edge
seams; an empty seam list does not verify their strength or construction.

## Inputs and quantity derivation

Width and height control the foundation. Amplitude and whole-number wave count
control the route. Cord diameter controls edge clearance and stitch-mark span;
maximum stitch spacing controls station count. Each tail allowance is added
once, making two allowances total. The fixed edge margin is 4 mm plus half the
cord diameter. Invalid height, pitch or parameter ranges fail rather than clamp.

The authored route is a polyline sampled at 96 segments per wave. Its **polyline
length**, which is also exported in the trace, determines the cord BOM. It is
not described as the exact length of a continuous mathematical sine curve.
`ceil(route_length / stitch_spacing)` intervals produce one more station than
intervals, with marks at both ends. Actual spacing never exceeds the selected
maximum. Thread consumption is deliberately unestimated; it depends on material
thickness, stitch method and securing knots. The minimum four-diameter wave pitch
is a simple layout guard, not a bend-radius or overlap proof.

1. Cut one foundation from a non-fraying textile such as an appropriate felt.
2. Transfer the center route and the transverse stitch marks.
3. Cut one cord to the native BOM length, including both end allowances.
4. Lay the cord along the route and couch at every transverse mark.
5. Turn both tail allowances to the reverse and secure using a material-tested
   finish. Add a separately tested wearable attachment.

No fraying allowance, backing piece, fastening hardware, knot topology, cord
bending stiffness, thread estimate, strength, drape or physical making test is
included. A route can be unsuitable for a stiff cord despite passing the planar
layout checks. `manufacturing_qualified` remains false.

## Census and provenance

The authoring census searched the 516 existing commons manifests, all five
FC-100 through FC-500 band indexes, and the platform material cards for English,
Spanish, French and Portuguese couching terms and related cord objects.
`chaleco-charro` mentions soutache in a heritage waistcoat; this new object does
not reproduce that garment, motif or cultural claim. `cord-end-notion` drafts a
cord cutting/tip guide; `drawcord-anchor` marks garment anchoring positions.
Neither produces this ornamental foundation, route-length BOM and arc-spaced
surface stitches. `jewelry-roll` stores jewellery rather than forming an ornament.
No existing dedicated cord-couching ornament cartridge was found.

Geometry was drafted here from first principles. The waveform is an original
geometric construction, with no attribution to or reproduction of a named
traditional motif. The manifest declares CERN-OHL-W-2.0 consistently with the
repository's root licence; no per-object licence file is supplied.

## Local verification

Two complete parameter sets were rendered through the native FC runner to SVG,
DXF, JSON and PDF: **eight successful exports**, each reporting `pieces=1
errors=0 warnings=0`. Manifest conformance checked one file with zero failures;
Ruff checked the source with zero findings. Native JSON issues are empty.

| Probe | width | height | amplitude | waves | cord diameter | max stitch spacing | each tail |
|---|---:|---:|---:|---:|---:|---:|---:|
| Default | 50 | 26 | 6 | 3 | 1.5 | 4 | 8 |
| Cuff insert | 90 | 40 | 11 | 4 | 2 | 5 | 12 |

Default: 288 route segments, 85.319161880 mm route, 101.319161880 mm cut cord,
23 stations, 3.878143722 mm actual spacing. Alternate: 384 route segments,
198.867763615 mm route, 222.867763615 mm cut cord, 41 stations,
4.971694090 mm actual spacing. Invalid height/amplitude, fractional wave count,
and too-tight wave pitch were separately rejected by the runner.

These are local macOS native checks, not a Linux CI result or physical
fabrication qualification. The commons CI workflow currently pins
`hyperobjects-spec` at `142db1802bbf9e1135ceae6c9c531c469f2d295b`; local checks
used the available Fashion Cabinet environment and should be repeated by the
coordinator's pinned verification lane before integration.

## Language review status

English, Spanish, French and Portuguese user-facing manifest strings are draft
translations. **Human language review is pending for all four**, particularly
French and Portuguese trade terminology. No human-review attestation is implied
by schema conformance. This is local internal-wave work awaiting coordinator and
reviewer integration, not a published, merged or production-qualified object.

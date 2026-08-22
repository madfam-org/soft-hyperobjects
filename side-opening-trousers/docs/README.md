# Side-Opening Trousers

Trousers with **no outseam**. Both side edges run open from waistband to hem and close on
hook-and-loop tape, so the garment lies flat on a bed or a wheelchair seat, the wearer is
transferred onto it, and the sides are pressed shut. No standing, no stepping in, no fly,
no button. The tape bridges to the Yantra4D
[`hook-loop-tape`](https://app.yantra4d.com) solid, sized from this trouser's own
measured open edge.

Part of the **Fashion Cabinet Commons** (FC-300, Adaptive II). Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns a rank

Adaptive trousers are usually a conventional pattern with a slit cut in it. This one is
drafted from the dressing motion outward: the outseam is not a seam that happens to open,
it is the *only* way the garment closes, and everything else in the block is arranged so
that works. Two properties fall out of that decision and are enforced in the draft.

**Seated rise, taken at the centres.** `seat_rise_extra` raises the back rise and lowers
the front rise, so the waistline tilts to a hip flexed at 90° instead of gaping behind and
cutting in at the front. Crucially the tilt is taken at centre front and centre back only —
the *side* waist point is shared by both pieces at one common height (`RISE_SIDE`, the mean
of the two rises). A draft that split the side height too would make the two tape carriers
structurally different lengths, and no amount of hem shaping could recover it.

**Equal carriers.** A hook-and-loop closure lies flat only if the two strips it joins
measure the same. That is solved, not asserted.

## Pieces

`front` (cut 2 mirrored) + `back` (cut 2 mirrored, seated rise, one seat dart) +
`band` (waistband, cut 1 on fold) + `placket` (tape carrier strip, cut 2 mirrored).

## The seam that solves

Front and back side edges share a top point and a crotch level, so they differ only in
hip and hem width. The back's hem half-width is then **bisected** until
`back.side_open` measures equal to `front.side_open` — convergence to better than
0.02 mm across the whole parameter range, verified by perturbation. At the defaults the
back hem lands at 261 mm against a 200 mm front hem: the extra seat width the back
carries has to be paid back somewhere, and the draft pays it at the hem rather than
leaving a 48 mm mismatch in the closure.

A second measured relationship governs the waistband. The seated tilt makes each waist
edge a *sloped* line, so its true length exceeds the flat quarter-width. `BAND_LEN` is
taken from the measured diagonal of all four waist edges plus the CF overlap, declared as
that overlap's `ease`, and checked to 1 mm.

## Construction notes

- **Hooks on the back carrier, loops on the front.** An open leg then never presents hook
  field to skin — this is the single most common failure of home-made adaptive trousers.
- **Bar-tack both ends of every tape run.** Tape peels from its ends first; the bar-tack is
  what makes the closure last past a season of daily transfers.
- The waistband elastic sits in the **back half only**, so the front stays flat under a lap
  belt.
- The hem takes a 40 mm turn-up (`allowances`), not the garment seam allowance.
- There is no fly and no front pocket bag by design: both add bulk exactly where a seated
  wearer's weight sits.

## Parameters

`waist_girth`, `hip_girth`, `outseam_length`, `front_rise`, `hem_width`,
`seat_rise_extra` (the adaptive control), `tape_width`, `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `hook-loop-tape`, mapping `strip_length → outseam_length - 42`,
`strip_width → tape_width`, `sew_margin → seam_allowance`. **Dimensional**: the tape's
sewn `sew_face` flange is driven by `strip_length`/`strip_width`/`sew_margin`, and the
same `outseam_length` and `tape_width` drive this trouser's `open_outseam` and
`tape_carrier` interfaces — so `verify_hardware_links` enforces name resolution *and* the
shared-dimension handshake.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

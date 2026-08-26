# Selvedge Straight-Leg Jean

The five-pocket **straight-leg** jean cut for **selvedge** denim: the outseam is left on
the loom's finished edge (the selvedge) and felled with the tell-tale white line — the one
edge of the whole garment drafted flat and straight, because a selvedge edge cannot be
curved without cutting off the very finish that makes it selvedge.

Part of the **Fashion Cabinet Commons** (FC-500, Lane 1 — family-depth backfill, denim).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `front_leg` | 2 mirrored | Selvedge outseam straight; front pocket rivet stepped in off both edges. |
| `back_leg` | 2 mirrored | Deeper back rise (the jean fork) carried at CB; patch-pocket mark. |
| `waistband` | 1 | Cut to the **measured** waist runs; the jeans button seated on cloth. |
| `fly` | 2 | Shield / facing, J-stitch. |
| `coin_pocket` | 1 | Watch pocket. |
| `pocket_bag` | 4 | Front pocket lining. |

## Solving and clamps

Two things are solved by measurement, not formula:

1. **The two inseams close to zero.** The front inseam's bulge is bisected until it
   measures the plain back inseam to well under a millimetre — a straight leg has no drape
   to hide a twist.
2. **The waistband is cut to the measured waist.** Its length is the summed front + back
   waist runs *as built*, less the fly seam, plus the button extension — never a laid-flat
   girth.

Every derived dimension is **clamped**: the waist quarter is held under the hip quarter so
a big waist cannot invert the side seam (geometry the kernel would CCW-normalize into a
healthy-looking piece), and the **half-knee is clamped to at least the half-hem** so a
straight leg never renders a boot-cut sliver at the narrow-knee extreme. Verified at
defaults, all-min, all-max, and every parameter swung to each bound.

## Declared seams

`front_leg.inseam ↔ back_leg.inseam` (tol 0.4), the two `side` outseams, the two `hem`s,
and `waistband.lower` against the four summed panel waist runs (declared as an ease so a
band redrafted off a girth goes red).

## Cross-commons bridge

`notion.hardware_ref` → **`jeans-button`**, mapping `head_dia → button_head` (and the
socket/tack params proportionally). One number sizes the button's bearing head **and** its
step-in from the band's finished end, so it seats on cloth. `button_head` also drives the
garment's `buttoned_waistband` interface, so the sewn/set face is dimensionally coupled.

## Parameters

`waist_girth`, `hip_girth`, `inside_leg`, `front_rise`, `hem_width`, `knee_width`,
`band_depth`, `button_head`, `wear_ease`, `hem_allowance`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# LED Trim Jacket

A hip-length raglan jacket whose illuminated trim is a **drafted seam**, not a strip
stuck on afterwards. Wave FC3-H (E-textile II) of the FC-300 commons.

## What it is

| Piece | Cut | Role |
|---|---|---|
| `front` | 1 on fold | Raglan front. Carries the marked LED trim path and the driver/battery pocket footprint. |
| `back` | 1 on fold | Raglan back, with the mirrored trim path. |
| `sleeve` | 2, mirrored | Raglan sleeve, drafted on the bodice raglan's own chord. |
| `trim` | 1 | The LED carrier band — a continuous strip cut to the measured raglan + hem run, with segment marks. |

## Why it earns a commons rank

The commons already has `led-costume-panel`: a flat panel with a channel layout. This is
the other half of that problem — what happens when the LED run has to follow a **curve**
on a garment that has to fit a body. The answer is the fourth piece. Making the carrier
band a real pattern piece, rather than treating the trim as a finish, is what lets every
part of the illuminated seam be replaced independently: the band is a flat rectangle
anyone can recut, the channel is an open printable solid, the strip is a commodity, and
the driver lives in a marked pocket rather than a sealed pouch.

That matters because the retail answer to night visibility is a disposable jacket glued
to a sealed light strip. When one LED dies the jacket is landfill.

## The seam that had to solve — twice

**1. The raglan.** A raglan seam is *one* seam sewn from two pieces, so the sleeve cap is
not free geometry. The first draft of this cartridge got this wrong: the cap was drawn on
the bicep width and the bodice raglan on the chest width, and the runner caught it —

```
seam_mismatch: sleeve.cap_front = 316.9 mm vs front.raglan = 326.1 mm (delta -9.3)
```

The fix is the correct drafting move, not a fudge factor. The bodice raglan chord is
`(HALF − NECK_HALF)` across by `raglan_depth` down; the sleeve cap is drafted on that
**same chord**, opened out from the apex to each side, with the same `RAGLAN_BULGE`. Now
the two curves are congruent by construction and the declared seam proves it. A requested
`bicep_girth` wider than the chord is honoured by **flaring the sleeve below the underarm**
— widening the underseam rather than distorting the cap that has to match.

**2. The trim run.** The raglan is a Bezier. You cannot know how long a strip of LED
channel to print until you have measured the curve you actually drew. So the kernel
drafts the front, back, and sleeve *first*, off-pattern, purely to measure:

```
RAGLAN_RUN = (front.raglan + back.raglan) × 2      # four raglan seams
HEM_RUN    = (front.hem × 2) + (back.hem × 2)      # both panels are cut on the fold
TRIM_RUN   = RAGLAN_RUN + HEM_RUN
```

At the defaults that is 1304.5 + 1139.9 = **2444.4 mm**. The trim band's `attach` edge is
cut to exactly that, the segment marks fall at the four raglan lengths so the maker knows
where to break the run, and the same number goes into the BOM as the length of channel to
print. The declared seam checks `trim.attach` against the eight edges it was measured from.

## Hardware bridge

`notion.hardware_ref` → **`yantra4d/led-channel`**.

`strip_w` is the dimensional handshake: it is the channel's `strip_width`, it sets the
channel `depth` and retention `lip`, and it is the width of the band's marked
`channel-seat` line. The band's `trim_width` sets the channel wall. The two commons share
one number, and the manifest's `led_carrier` interface declares both parameters so the
coupling is machine-checkable rather than a comment.

## Construction notes

- **Fabric.** `popelina-algodon` by default — a 200 °C iron ceiling gives room to press
  the raglan seams properly before the trim goes on. The band is cut from the same cloth.
- **Order.** Sew and press the raglan seams and the side seams. Hem. *Then* topstitch the
  carrier band over the finished seams and clip the channel in. The band is applied to a
  finished garment, which is exactly why it is replaceable.
- **Cable.** The sleeve-to-bodice run passes at the marked `cable-pass` drill point just
  inside the underarm, where there is no flex crease. Leave a service loop.
- **The circuit is marked, not drafted.** No driver, wiring, or strip is generated here.
  Route power at low voltage.

## Provenance

Original draft for Fashion Cabinet. The raglan block is classical technique — redrawn
here so the raglan chord is shared explicitly between bodice and sleeve, which is what
makes the trim run measurable.

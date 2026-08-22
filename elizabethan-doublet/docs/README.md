# Elizabethan Doublet

**FC-300 · Costume & historical · c. 1570–1600**

A man's doublet of the later 16th century, drafted on period tailoring logic.

## What it is

The doublet is the fitted upper garment worn over the shirt — close through the body,
buttoned up the centre front, with a stiffened front that in the fashionable extreme
becomes the **peascod**: a padded belly shaped to a point that overhangs the waist.

Three things separate a period draft from a costume approximation, and this cartridge
holds all three:

1. **No darts.** Period tailoring solved fit at the **seams**. All shaping here is taken
   at the side and back seams. Adding a bust or waist dart is the fastest way to make a
   doublet read as a modern jacket in costume fabric.
2. **The centre front butts.** The two fronts **meet edge to edge** and are held by many
   small closely-spaced buttons opposed by worked thread loops. There is no lapped
   placket and no facing extension, because nothing overlaps.
3. **A high, small armscye.** The armhole sits high and tight (`back_length * 0.46`).
   Counter-intuitively this lets the arm rise *further*, because the garment does not
   lift off the shoulder when the arm does.

## Why it earns a commons rank

This is the cartridge in the wave where the drafting engine is doing the most real work,
and it is a genuinely instructive draft: it demonstrates dartless seam shaping and a
properly solved set-in sleeve, which are transferable skills, not just a costume.

Parametric matters more here than usual. Doublets are close-fitting, so a graded fixed
size fits almost nobody, and the peascod is a continuous style axis (0 → 90 mm) rather
than a binary — the same draft covers a plain 1570 doublet and a 1585 court extreme.

## Construction notes

### The seam that must solve: the sleeve cap

A set-in sleeve is the honest test of any bodice draft. The cap must equal the armscye it
sews into, **plus** a declared ease worked in over the cap head.

Most drafts compute the armhole from one formula and the cap from another and hope they
agree. This cartridge does it the honest way round:

1. build the front and back armhole curves,
2. **measure** their combined length off the built polygons → `armscye_measured_mm`,
3. **solve** the sleeve cap's bulge factor by bisection (80 iterations) until the cap's
   *measured* length equals armscye + ease.

The residual is reported as `cap_residual_mm` and converges to **0.0 mm** at every size
tested — chest 1000 → 1280 mm, shoulder 145 → 195 mm. Neither side is a formula hoping
to agree with the other.

The cap is a two-lobe S: hollowed on the front half (`bulge * 0.55`), fuller on the
back, which is what makes a sleeve hang with the arm rather than twisting forward.

### The back shoulder is also solved

The back neck is drafted **wider and shallower** than the front — the period cut, since
the front neck scoops while the back sits high across the nape. Done naïvely that leaves
the back shoulder seam shorter than the front's, which is a real defect: the verifier
caught it at a 9.9 mm mismatch during development.

The fix was not to widen the tolerance. The back neck point's *height* is solved
trigonometrically so the two shoulder seams come out equal:

```
ny = L + sqrt(front_shoulder_len² − (shoulder_width − back_neck_w)²)
```

Both shoulders now measure identically. If the back neck were ever drafted so wide that
no rise could match the front, the code falls back to a flat shoulder and lets the
declared seam report the truth rather than silently fudging.

### The peascod

At `peascod_bow > 0` the CF edge bows forward below the chest and returns at the waist.
The bow alone does not make the shape — it is held by **wool or cotton wadding quilted
into the linen interlining** along the marked `peascod-padding` line. At zero the CF is
straight and you have the plainer earlier doublet.

### Three layers

A period doublet is fashion fabric + a **linen interlining that carries the shape** +
a lining. The stiffness belongs in the interlining. Fusible interfacing gives a
board-like hand and is the wrong structure.

## Provenance

An original draft built on the documented construction tradition of later-16th-century
men's doublets: butt-buttoned centre front, high small armscye, shaping at side and back
seams, a padded peascod front, set-on waist skirts, and a standing collar. It is **not**
traced from any single extant garment and is not a transcription of any published
pattern.

These are the well-attested general characteristics of the type. For museum-grade work,
measure an extant garment or consult a scholarly pattern source.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `front` | 2, mirrored | butt CF, peascod bow, button marks |
| `back` | 2, mirrored | solved shoulder, CB seam |
| `sleeve` | 2, mirrored | solved cap, tapered to wrist |
| `skirt` | 2, mirrored | waist tabs; divisions marked as cut lines |
| `collar` | 1 on fold | standing band for ruff or falling band |

All five declared seams verify exactly at default and across perturbation.

## Hardware bridge

`sew-through-button` — `hole_spacing` ← `button_pitch / 8`,
`card_count` ← `round(back_length / button_pitch)`.

## Fabric

Wool broadcloth or silk over a linen interlining, fully lined.
`lana-peinada-traje` is the closest card in the material set.

# Zip-Pull Aid Vest

**FC-300 #252 · adaptive II · `fc` pattern kernel · hardware bridge → Yantra4D `zipper-loop-aid`**

An insulated vest built around the part of a zip that actually defeats people:
**not the pulling — the starting.**

## What it is

A sleeveless quilted vest: two fronts with a cut-on zip stand, a back on the
fold, two front facings carrying an interfaced starting block, and a binding
strip. Four pieces.

## Why it earns its rank

"Adaptive" outerwear almost always answers the wrong question. It makes the
**pull** bigger. But the operation people actually fail at is *engaging the box
and the pin*: holding two small parts in register, with two hands, at the hem,
below the field of view, against the weight of the garment.

Add tremor, one working hand, low vision, an arthritic pinch grip, or cold
fingers, and the pin misses the box — repeatedly, in a cold doorway, while
somebody waits. That failure is invisible in a shop and total in real life, and it
is why a coat somebody already owns goes unworn.

Three things are drafted in to fix it, and **none of them is a bigger zip**:

1. **A rigid starting box.** The bottom band of both fronts is interfaced *firm*
   into a starting block, so the box side cannot fold, curl or wander while the
   pin is offered up. Nearly every "easy zip" garment **softens** the hem; this
   one deliberately hardens it, because a floppy box is the actual failure mode.
2. **A funnel.** A marked V above the block guides the pin down onto the chain,
   so the hand can be several millimetres wrong and still engage.
3. **A finger-ring pull.** The slider carries a printed ring aid that a whole
   finger — or a dressing hook — passes through. No pinch grip is required
   anywhere in the operation.

And it is a **vest on purpose**. No sleeves means no second arm to thread, which
is the other half of why outerwear gets abandoned. It goes on like a waistcoat
and closes on one line.

## What is actually solved (not assumed)

### 1. The zip length, from the MEASURED opening

A separating zip is bought — or printed — at a **length**. And the opening is
*not* the vest length: the neckline curves up past the centre-front point, and
the hem is squared off the stand rather than off CF. So the opening edge is
measured off the built piece and the zip taken from that:

```
opening_run_measured_mm : 559.33
zip_length_specified_mm : 540.0
zip_shortfall_mm        :  19.33
```

The rounding is deliberately **downward**, to a stocked 10 mm step. A zip longer
than its opening cannot be fitted at all; a slightly short one simply finishes
below the neck seam, which is where a zip should stop anyway on a garment meant
to be pulled on over a jumper. The length tracks the opening across the range —
540 mm at 640 mm body, 700 mm at 800 mm, 380 mm at 480 mm.

### 2. Shoulder seam equality — and why it matters *here*

The back neck sits higher than the front neck; drafting both at the same neck
width leaves the back shoulder roughly 23 mm long. On most garments that is a
wrinkle. Here the consequence is specific and mechanical: **an unequal shoulder
tips the whole front panel, and a tipped front panel puts the box out of plumb
with the pin** — the one alignment this entire garment exists to preserve.

So `NECK_W_BACK` is solved by Pythagoras from the front's *measured* shoulder
length:

```
front_shoulder_measured_mm : 143.04
back_neck_half_width_mm    : 113.38
```

and checked at `tol=0.5`.

### 3. The facing must not lose its interfacing

The facing is cut to the **measured** opening run and declared against the
front's zip edge at `tol=0.5`. A facing cut to the vest length instead would run
past the neck seam and have to be trimmed at assembly — and the thing trimmed
away would be precisely the interfaced region the design depends on.

### 4. The binding, cut to what the pieces present

Both armholes and the neckline are measured off the built pieces, then the strip
is cut short by a stretch factor. This is not cosmetic: the binding's job is to
hold the armhole flat against the body, because **a vest that swings while the
zip is being started is a vest whose box will not stay under the pin**.

## Construction notes

- **Firm woven interfacing in the block, not knit.** This is the one place in the
  garment that must not be soft. Fuse the block region of both facings only.
- **Topstitch the block's upper edge.** That line is what stops the rigid section
  flexing at its boundary — without it the block hinges where the interfacing
  ends and you are back to a floppy box.
- **The zip edge takes no seam allowance.** The stand *is* the allowance, folded
  back onto the tape. Adding one doubles the stand and throws the two chain
  halves out of plane, which presents the pin at an angle to the box.
- **Keep the pocket clear of the block.** It is placed above `BLOCK_H` on purpose;
  a pocket bag stitched through the block softens it.
- **Mirror the stands exactly.** Equal stands either side of centre front are what
  put the two chain halves in one plane. This is guaranteed by construction here
  (the piece is drafted about `x = 0` and cut mirrored), but it is the first
  thing to check if a made garment will not start.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `zipper-loop-aid` solid. The aid's
`ring_id` is fed from this vest's `ring_inner`, and its clip dimensions (`tab_t`,
`tab_w`) from `zip_chain` — the same chain size the pattern sizes its stand for.

A note on the handshake for anyone reading the wave's other cartridges: this
solid declares **no `flange`-type interface** (its two interfaces are `snap`
and `profile`), so `fc_spec`'s `hardware_dimensional_rules` has no sewn edge to
couple against and correctly returns early. The coupling is still wired the same
way — `ring_inner` and `zip_chain` both appear in the garment's own `zip_opening`
interface — so the mapping stays honest if the solid ever gains a sewn face.

**The ring alone retrofits any zip a person already owns.** A few pence of
filament against a coat left in a cupboard; and the funnel and the block can be
added to an existing garment by anyone with an iron and a straight stitch. The
pattern is one route to the result, not a condition for it.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `LicenseRef-FC1-pending`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/zip-pull-aid-vest/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `facing`, `binding`.

# Suspender belt (six-strap)

The classic waist-sitting suspender belt (**liguero**) in satin tricot: a shaped belt that
sits at the natural waist and hangs **six** suspender straps — a front pair, a side pair, and
a back pair — each ending in a clip that grips a stocking welt.

Part of the **Fashion Cabinet Commons** (FC-400, lane 9 — structured intimates). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The four-strap [garter belt](../../garter-belt/docs/README.md) sits low and holds a
> stocking well enough. Six straps at the **waist** hold a fully-fashioned stocking dead
> straight — the depth this rank adds.

## Why it earns its rank

**The belt is shaped, not straight.** The body narrows to the waist and flares to the hip, so
a rectangle rides up or falls down. The belt is a flattened **truncated cone**: its top edge
sums to the waist ring and its bottom edge to the high-hip ring, and the flare is split
**equally** over the vertical seams — equal flare per panel means congruent slants, so the
ring closes by construction (the verifier catches a proportional flare that would not meet).
Sitting at the waist rather than the high hip is what lets six straps keep the stocking seam
straight down the leg.

**Six straps are placed, not sprinkled.** A front pair either side of centre front, a side
pair over each hip, and a back pair either side of centre back. Six points is what holds a
fully-fashioned stocking without the welt sagging between suspenders, and the drop is set so
each clip lands on the welt.

## The dimensional handshake

The clip is the Yantra4D solid `garter-clip`, whose sewn feature is a `strap_slot` flange
driven by `strap_w` and `strap_t`. A strap wider than the slot will not thread; narrower and
it twists. So `strap_w` drives **both** the drafted strap's cut width (its `strap_edge`
interface) **and** the clip's slot — one number, two objects — and `strap_t` feeds the slot
clearance for the folded webbing (`grip_clear = 0.3 mm`).

## Construction notes

Pieces: **front_panel** (cut 1 on fold), **side_panel** (cut 2 pairs), **back_panel** (cut 1
on fold, hook closure), **strap** (cut 6).

1. Join the panels front → side → back into the shaped ring; the mirror supplies the other
   half.
2. Line the belt fully so the strap stitching is enclosed.
3. Bar-tack each of the six straps to the lower edge at its marked position.
4. Thread a clip onto each strap's free end (it folds back through the slot) and a slider for
   length adjustment.
5. Stabilise the waist and lower edges lightly, and close the centre back with hook-and-bar
   tape.

## Hardware

The clips are **Yantra4D solids** (`notion.hardware_ref → garter-clip`, linked), never
modelled here. `strap_w → strap_w`, `strap_t → strap_t`, `grip_clear = 0.3 mm`. The sliders
and the hook-and-bar tape are standard notions.

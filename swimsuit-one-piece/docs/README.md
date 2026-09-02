# Structured one-piece swimsuit

A **structured** one-piece maillot in swim-lycra: a full-torso swimsuit with a built-in shelf
bra and **adjustable** ring-and-slider straps.

Part of the **Fashion Cabinet Commons** (FC-400, lane 9 — active/structured intimates).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Distinct from the FC-100 [one-piece swimsuit](../../one-piece-swimsuit/docs/README.md), a
> pull-on maillot with no hardware. Here the structure — the shelf bra and adjustable straps —
> is the whole point of the rank.

## Why it earns its rank

A swimsuit that actually **supports** needs two things a fixed-size pull-on maillot cannot
give, and this cartridge draws both:

**The straps adjust — that is the structure.** The straps run from the back, through a
**ring** at the front bust line, over the shoulder, and back through a **slider**, so the
wearer sets the height and the shelf bra sits where their bust is. `strap_w` drives both the
drafted strap's cut width and the ring/slider channel. Adjustable straps are what let one
drafted suit fit a range of torso lengths.

**The shelf bra is a real inner layer.** A separate lined front shelf, solved to the underbust
ring at negative ease and finished with elastic, gives support the outer layer alone cannot.

**The leg is a high-cut opening on a gusset.** Front and back join at the side seams and a
lined gusset; the leg openings are high-cut curves finished with elastic — no inseam — and the
whole suit is negative-ease so the lycra grips.

## Construction notes

Pieces: **front** (cut 1), **back** (cut 1, higher back), **shelf** (inner bra, cut 1, lined),
**gusset** (cut 2 — self + swim lining), **strap** (cut 2).

1. Join front to back at both side seams (drafted congruent by a fixed armhole height).
2. Bridge the crotch with the lined gusset.
3. Attach the inner shelf bra to the front, gathered to the underbust line, and finish its top
   and underbust with swim elastic.
4. Finish the neckline and high-cut legs with swim elastic; flatlock all seams so they do not
   chafe under water.
5. Thread each strap through the ring at the shelf bust line and a slider on the shoulder.

## Hardware

Rings and sliders are **Yantra4D solids** (`notion.hardware_ref → bra-ring-slider`, linked),
never modelled here. `strap_w → strap_w`, `wire_d = 1.8 mm`. They must resist chlorine and can
be reprinted when they wear.

## Made to measure

Drafted to **bust**, **underbust**, **waist** and **hip** girths plus the **shoulder-to-crotch**
length. Every slider extreme (shelf rise, leg height, neck scoop, negative ease) renders
watertight.

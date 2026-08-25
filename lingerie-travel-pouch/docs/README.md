# Lingerie Travel Pouch

The two-compartment **travel pouch** that keeps clean underthings away from worn ones — the
most useful and least glamorous object in a suitcase. A shaped shell front and back, a
boxed base, a mesh divider that splits the interior, and a zip that runs three sides so the
pouch opens flat rather than gaping through a slot. The zip bridges to the Yantra4D
[`zipper`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300, rank #259 — care & keeping). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Packing cubes arrive in sets, in laminated polyester that delaminates within a few trips
and can be neither repaired nor recycled. One cube cut to the case someone actually travels
with, in ripstop offcuts, with a seam a home machine can reopen, replaces a set — and the
clean/worn divider is the thing the retail versions leave out.

## Pieces

`shell` (front/back panel with rounded top corners and boxed base, cut 2) + `base` (the
flat bottom the boxed corners close onto, cut 1) + `divider` (mesh partition, cut 1) +
`pull_tab` (zip pull tab, cut 2).

## The seam that solves

The zip runs a **U** — down one side, across the top, and down the other — around a shell
whose top corners are **rounded**. Its length is therefore *not* `2·height + width`; it is
the **measured** length of that rounded three-sided path. This cartridge polygonises the
corner arcs, measures the U, and both sizes the zipper from that measurement and declares
the seam against it. The boxed base is solved the same way: a boxed corner removes a square
of side `depth/2` from each bottom corner, which **shortens** the side and bottom edges by
a measured amount rather than an assumed one.

## Construction notes

Attach the divider to the base seam before closing the shells — reaching in afterwards
through a three-sided opening is possible but miserable. Use mesh for the divider so the
worn side breathes; a solid partition turns the pouch into two sealed damp compartments.
The pull tabs are cut in pairs so each end of the zip is capped, which is what stops the
slider running off the tape at the corner.

## Cross-commons bridge

`notion.hardware_ref` → `zipper`, mapping `zip_length → pouch_width + pouch_height * 2`,
`tape_width → corner_radius * 0.25`, and `chain_size → 5`. **Dimensional**: the zipper's
sewn `tape_edge` flange is driven by `zip_length` and `tape_width`, and `pouch_width`,
`pouch_height`, and `corner_radius` all drive this pouch's own `zip_tape` interface — the
same U that the pattern measures is the U the hardware is cut to.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

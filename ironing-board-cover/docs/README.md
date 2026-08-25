# Ironing Board Cover

The drawstring cover for **the one tool every other cartridge in this commons depends on**.
A cover that is loose scorches and creases what it is pressing; a cover that is drum-tight
is what makes a pressed seam stay pressed. The cover is drafted to the board's tapered
nose-and-shoulder outline plus a turn-under skirt, a bias-cut casing carries the drawcord
round the whole perimeter to a Yantra4D [`cord-lock`](https://app.yantra4d.com), and a felt
pad softens beneath.

Part of the **Fashion Cabinet Commons** (FC-300, rank #260 — care & keeping). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

Every other cartridge in this lane assumes a working press surface. Replacement covers are
sold in two or three sizes with a metallised coating that flakes into whatever is being
pressed, and a board whose cover no longer fits is usually thrown out whole. A cover cut to
a measured board, in plain cotton over a felt pad, is launderable, repairable, and fits the
board someone already owns — and closes the loop on the commons' own tooling.

## Pieces

`cover` (the board outline plus skirt, cut 1) + `casing` (bias drawcord channel cut to the
measured perimeter, cut 1) + `pad` (felt underlayer, cut to the board line only, cut 1).

## The seam that solves

The casing runs the cover's **outside perimeter** — a closed curve made of a nose arc, two
long tapering sides, and a square heel. There is no formula for its length, and a casing
cut short will not close. This cartridge builds the outline once, **measures** the full
perimeter, and cuts the casing to it. Separately: because the casing is a strip applied
round a **curve**, its inner edge travels a shorter path than its outer edge; that
difference is computed by measuring an **offset copy** of the same outline, and is what
forces the casing to be cut on the **bias** rather than the straight grain.

## Construction notes

Cut the casing on the true bias, not a near-bias — the measured inner/outer difference is
what it has to absorb, and straight-grain strip will ripple at the nose where the curvature
is tightest. The pad is cut to the board line **without** the skirt, so it does not bunch
under the drawcord. Leave the cord exit at the heel, where the board's underside is flat
and the lock will not press into whatever the board rests against.

## Cross-commons bridge

`notion.hardware_ref` → `cord-lock`, mapping `cord_dia → cord_diameter`, `cords → 2`,
`body_size → cord_diameter * 4`, and `wall → cord_diameter * 0.5`. The cord-lock declares
no flange interface — its mating geometry is a `snap` and a `pocket` — so the
dimensional-handshake rule resolves by name, while `cord_diameter` still drives this
cover's own `cord_casing` interface on both sides of the bridge.

## Provenance

Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

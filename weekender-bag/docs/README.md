# Weekender Bag

A **boxed weekender** on the [`dopp-kit`](../../dopp-kit/docs/README.md) construction
precedent, scaled to overnight luggage: a wrap body folded at the base, two end gussets
that give it its rigid box shape, a top zip, and two carry handles. **Bag feet** are
riveted through the marked base bores — the foot bridges to the Yantra4D
[`bag-feet`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`body` (front + base + back, cut 1) + `end` (end gusset, cut 2) + `handle` (carry handle,
cut 2).

## The seam that solves — and the mistake it caught

The end gussets **crown toward the zip**, so a gusset's attach run is a Bezier and *not*
`2·height + depth`. The body panel height is therefore derived from the **measured** gusset
run. At the default size the crowned top measures 263.8 mm against a flat 260 mm — a 3.8 mm
error per gusset that a formula-drafted body would have silently absorbed.

The first draft of this cartridge declared the body side against all four gusset edges
(including `bottom`) and `verify()` rejected it with a 343.9 mm mismatch. The gusset's
`bottom` lies along the base fold and is not sewn to the body side at all; the seam is
`attach_l + top + attach_r`. Fail-closed verification caught a real geometry error, which
is what it is for.

Four seams are declared and verified: both body sides against the gusset attach run, the
two zip tapes against each other, and the gusset's two side edges against each other.

## Parameters

`bag_length`, `bag_height`, `bag_depth`, `handle_length`, `handle_width`, `foot_diameter`
(drives the Yantra4D foot), `seam_allowance`.

## Cross-commons bridge — point-placed, not edge-mated

`notion.hardware_ref` → `bag-feet`, mapping `foot_dia → foot_diameter`,
`foot_h → max(6, foot_diameter / 2)`, `washer_dia → foot_diameter * 0.8`.

`bag-feet` exposes only `socket` and `snap` interfaces — **no flange**, so there is no sewn
edge to couple. The foot is point-placed hardware: it takes a *drilled bore position* (four
`foot-bore` drill marks inset from the base corners), not an edge coupling. The dimensional
handshake rule correctly requires no edge for this class of hardware.

## Provenance

Original draft for Fashion Cabinet; boxed-bag construction precedent from the Fashion
Cabinet `dopp-kit` cartridge. `LicenseRef-FC1-pending`.

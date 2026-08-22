# Wallet Organizer

A **folded multi-pocket organizer**: a shell that folds down its centre, a ladder of
card-pocket tiers on each inner face, a cash sleeve behind them, and **chicago screws**
binding the four corners. The screw bridges to the Yantra4D
[`chicago-screw`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`shell` (folds at centre, cut 1) + `pocket` (card tier, cut 2 per tier) + `cash` (cash
sleeve, cut 1).

## The computed stack

A chicago screw has to be long enough for the stack it binds. Rather than a nominal guess,
the stack is **computed**: the shell (doubled at the bound corner) plus every pocket tier
plus the cash sleeve, each one `material_thickness`. At defaults that is
`1.2 × (2 + 3 + 1) = 7.2 mm`, and it drives the screw's `stack_t` directly — the screw is
dimensioned to the wallet it actually closes.

## The clamp that a probe earned

The tier ladder is `(tiers − 1) × card_reveal` tall and must fit inside the wallet height.
A worst-case probe (70 mm height, 5 tiers, 26 mm reveal) drove the tier height to −34 mm —
and the kernel's CCW normalization *silently flipped it into a valid-looking 34 mm piece*
that passed `verify()`. Geometry that verifies is not automatically geometry that is right.
The reveal is now auto-capped so every tier keeps at least a 30 mm usable pocket; the
default is untouched, and the worst case now lands exactly on that floor.

Four seams are declared and verified: the pocket base against the cash base, the pocket
mouth against the cash mouth, the pocket's two binding edges against each other, and the
shell's two half-widths against each other.

## Parameters

`wallet_width`, `wallet_height`, `card_reveal`, `pocket_tiers`, `material_thickness`,
`screw_head` (both drive the Yantra4D screw), `seam_allowance`.

## Cross-commons bridge — point-placed, not edge-mated

`notion.hardware_ref` → `chicago-screw`, mapping `head_dia → screw_head`,
`post_dia → screw_head * 0.45`, `stack_t → material_thickness * (3 + pocket_tiers)`.

`chicago-screw` exposes `thread` and `socket` interfaces — **no flange**, so there is no
sewn edge to couple. The screw is point-placed: a threaded post through a drilled bore
stack, marked as four `screw-bore` cross marks inset from the shell corners.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

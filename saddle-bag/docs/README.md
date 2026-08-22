# Saddle Bag

The **saddle silhouette**: a body panel whose base is a deep arc, a one-piece gusset
wrapping that whole curved run, and a curved flap caught by a **twist-lock**. The lock
bridges to the Yantra4D [`twist-lock-closure`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300, Lane 1 — bags & soft luggage). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

`body` (saddle panel, cut 2) + `gusset` (wrap gusset, cut 1) + `flap` (cover flap, cut 1).

## The seam that solves

The saddle arc and the flap arc are **Beziers with no closed-form length**, so neither can
be drafted from a formula. Two solves:

1. The gusset's span is taken from the *measured* run of one body panel's
   `side_r + saddle + side_l`.
2. The flap's front bulge is **bisected until its arc equals the body's measured saddle
   arc** (328.1 mm at defaults, converging to within 0.05 mm). The flap and the bag bottom
   therefore read as *one continuous curve* — which is the entire visual point of a saddle
   bag, and would be off by several millimetres if both arcs were merely given the same
   bulge parameter over the same chord.

Five seams are declared and verified: both gusset long edges against the body's curved run,
the flap attachment against the body opening, the solved flap arc against the saddle arc,
and the two body openings against each other.

## Parameters

`bag_width`, `bag_height`, `saddle_curve`, `bag_depth`, `flap_drop`, `lock_plate` (drives
the Yantra4D lock), `seam_allowance`.

## Cross-commons bridge — point-placed, not edge-mated

`notion.hardware_ref` → `twist-lock-closure`, mapping `plate_l → lock_plate`,
`plate_w → lock_plate * 0.6`, `turn_l → lock_plate * 0.7`.

`twist-lock-closure` exposes `pocket`, `bolt_pattern` and `socket` interfaces — **no
flange**, so there is no sewn edge to couple. The keeper rivets to the front body panel and
the turn to the flap's underside, both at drilled `lock-keeper` / `lock-turn` cross marks.
The dimensional handshake rule correctly requires no edge coupling for this hardware class.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

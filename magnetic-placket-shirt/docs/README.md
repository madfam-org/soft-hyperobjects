# Magnetic-Placket Shirt

A button-front shirt that **never asks a hand to pinch**. Real buttons are sewn to the
outside of the placket as the visible face; underneath, a column of magnetic button
covers does the closing. The shirt reads as an ordinary dress shirt and shuts with a
nudge of a knuckle. The cover bridges to the Yantra4D
[`magnetic-button-cover`](https://app.yantra4d.com).

Part of the **Fashion Cabinet Commons** (FC-300, Adaptive II). Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns a rank

Adaptive clothing that announces itself is clothing people decline to wear. The design
constraint here is therefore not "make it easier to fasten" but "make it easier to fasten
*and* indistinguishable from a shirt anyone else would put on". Keeping the buttons and
moving the work behind them is the whole idea, and it puts a real geometric demand on the
draft: a magnetic pair holds only if the two magnet **centres** land on top of each other
when the shirt is closed.

That is enforced two ways. The placket stands are mirror-equal about centre front by
construction — the front is drawn from `x = -STAND` outward with CF at `x = 0`, so
mirroring the piece for the other front puts every magnet centre on its partner without a
separate calculation. And the pitch is solved, not assumed.

## Pieces

`front` (cut 2 mirrored, placket cut on) + `back` (cut 1 on fold at CB) +
`sleeve` (cut 2 mirrored) + `collar` (cut 2).

## The seams that solve

**The magnet column.** `magnet_pitch` is a *request*, not a result. The closure run is
measured from below the collar seam to above the hem (both ends held clear so no magnet
fights a seam), whole intervals are fitted to it, and the pitch is then **recomputed**
from that integer count. At the defaults a requested 95 mm becomes a solved 98.07 mm
across 6 magnets. Without the recompute the column would drift and the last magnet would
land in the hem allowance.

**The back neck width.** A back neck sits higher than a front neck, so a back drafted at
the same neck width gives a *longer* shoulder — 183.9 mm against the front's 160.9 mm in
the first draft of this cartridge. `NECK_W_BACK` is therefore solved from the front's
measured shoulder length by Pythagoras against the known vertical drop, so the shoulder
seam is equal by construction rather than by hoping two formulas agree.

**The sleeve cap.** Cap height is bisected until the cap measures both armholes plus
14 mm of ease. The armholes are read off the *built* pieces, not reconstructed from
formula. A dropped-shoulder adaptive sleeve takes little ease deliberately: too much and
the cap ripples, which a wearer dressing by feel will catch on.

**The collar.** Cut to the measured neckline (front ×2 + back ×2, the back being on
fold), which is the usual place a collar comes up short.

## Construction notes

- **Fuse the placket.** An unfused placket lets the covers tilt, and a tilted magnet pair
  loses most of its holding force. This is the single highest-leverage step.
- The visible shank buttons **never pass through a hole** — there are no buttonholes in
  this shirt at all.
- The **cuff is open**, no button, so a hand passes without help.
- The chest pocket is placed clear of the magnet column so a card or a phone never rests
  on a magnet.
- The armhole is dropped 250 mm and the chest carries 160 mm of ease: an arm that cannot
  be lifted far still finds the sleeve.

## Parameters

`chest_girth`, `shirt_length`, `shoulder_width`, `sleeve_length`, `neck_girth`,
`button_diameter`, `magnet_pitch` (requested — see above), `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `magnetic-button-cover`, mapping `button_dia → button_diameter`,
`button_t → 3`, `hole_dia → seam_allowance / 8`, `sew_holes → 4`. **Dimensional**: the
cover's sewn `plate_sew_ring` flange is driven by `button_dia`, and the same
`button_diameter` drives this shirt's `magnetic_placket` interface — so
`verify_hardware_links` enforces name resolution *and* the shared-dimension handshake.

Because the cover's snap lip grips a conventional shank button, the same open hardware
converts shirts a wearer already owns. The pattern is one route to the result, not a
requirement for it.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

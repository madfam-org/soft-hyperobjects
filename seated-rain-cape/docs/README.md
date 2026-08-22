# Seated Rain Cape

A rain cape cut for a body that is **sitting down**. The front falls over the knees to the
footplate, the back stops clear of the seat and the push rims, and a side panel ramps
between the two hem radii so the hem sweeps up without a step. The chest strap closes on a
Yantra4D [`side-release-buckle`](https://app.yantra4d.com) — one hand, one click, no
overhead motion.

Part of the **Fashion Cabinet Commons** (FC-300, Adaptive II). Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns a rank

Rainwear quietly makes rain *worse* for seated users, and it does so through a geometry
problem rather than an oversight. A cape hangs from the shoulders to a hem that is level
all round. Sit down and that level hem becomes two different problems at once: it rides up
over the thighs and leaves the knees bare, while the back — now unsupported by a standing
body — pools into a long wet tail that drags into the wheels. Lengthening the cape fixes
the knees and worsens the wheels. Shortening it does the reverse.

The fix is to stop treating the hem as one radius. This cape carries **two**: `R_FRONT`
for knee coverage and `R_BACK` for seat clearance, with the side panel's hem radius
ramping linearly between them across its swept angle. The hem therefore sweeps up
continuously — there is no notch or step where the lengths change, which is what a
naive two-length cape produces.

## Pieces

`front` (cut 2 mirrored, knee length) + `side` (cut 2 mirrored, hem transition) +
`back` (cut 1 on fold at CB, seat clearance) + `hood` (cut 2 mirrored).

## The seams that solve

A cape is a **partial annulus**, and two things have to close for it to fit at all.

**The neck radius.** The neck edge is an arc of `sweep_deg` at radius `R_NECK`, and its arc
*length* must equal the eased neck girth — so the radius follows from the sweep, not the
other way round. It is bisected until the measured 40-gon arc equals the target, landing
exactly on 480.0 mm against a 480.0 mm target at the defaults. Bisecting against the
measured polygon rather than dividing by `θ` keeps this consistent with every other length
in the cartridge, all of which are measured the same way.

**The panel angles.** Two fronts, two sides and two half-backs must sum to the sweep or
the cape will not close on the body. The front and side shares are taken as fractions; the
back's half-angle is then taken as the **remainder**, so the sum is exact rather than
`sweep ± rounding`. Verified across the range: 96.0 + 41.6 + 22.4, doubled, gives 320.0°
against a 320° sweep.

**The hood neck.** Drafted to the *measured* neckline (all six panel neck edges), with the
curve's bulge bisected until it measures the run it has to take. A hood cut to a neck-girth
formula is the classic source of a hood that will not sit down on the shoulders.

## Construction notes

- **Seam-seal every radial seam.** They run top to bottom down the wearer; an unsealed
  radial seam is a channel straight to the lap.
- **Reflective tape along the back hem.** The back is short by design, which puts its hem
  at roughly driver eye height — this is a safety consequence of the adaptive cut, not a
  styling choice.
- A **hand slit** is marked on each front so a hand reaches the push rim without lifting
  the whole cape. Cut by the maker; leaving it marked lets a wearer who does not self-propel
  skip it.
- The radial panels nest poorly (62% marker) — this is inherent to annulus patterns, and
  the BOM already accounts for it.

## Parameters

`neck_girth`, `front_length`, `back_length` (clamped to at least 120 mm under the front),
`sweep_deg`, `strap_webbing`, `hood_height`, `seam_allowance`.

## Cross-commons bridge

`notion.hardware_ref` → `side-release-buckle`, mapping `webbing_w → strap_webbing`,
`webbing_t → 2`, `body_t → seam_allowance`. **Dimensional**: the buckle's sewn
`webbing_channel` flange is driven by `webbing_w`, and the same `strap_webbing` drives this
cape's `chest_strap` interface — so `verify_hardware_links` enforces name resolution *and*
the shared-dimension handshake.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.

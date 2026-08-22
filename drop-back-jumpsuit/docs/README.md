# Drop-Back Jumpsuit

**FC-300 #251 · adaptive II · `fc` pattern kernel · hardware bridge → Yantra4D `d-ring`**

A jumpsuit whose entire seat drops away on two webbing straps, so a seated wearer
can use a toilet **without taking the garment off, without standing, and without a
second person in the room**.

## What it is

Front and back cut as bodice-and-leg in one piece (cut 2 mirrored each), a drop
seat panel cut on the fold, a waistband carrying both D-ring anchors, and a strap
facing. Five pieces.

## Why it earns its rank

The problem is not comfort. It is autonomy and time.

A one-piece garment is the warmest, tidiest, least-riding-up thing a wheelchair
user can wear — no waistband digging into a seated abdomen, no gap at the back
when leaning forward, no shirt hem working its way up under a lap belt all day.
It is *also* the garment that turns a five-minute toilet transfer into a
twenty-minute undressing that needs help. So the standard advice is simply: don't
wear a jumpsuit.

Independent toileting is the single most-cited determinant of whether a
wheelchair user can hold a job, travel, or live alone. When clothing is the only
thing standing in the way of it, that is a clothing problem worth solving rather
than designing around.

### Why hinged, not detachable

Commercial drop-seat garments exist. They cost several times a plain jumpsuit,
and most of them use a **fully detachable** panel — which, in a public toilet, on
a transfer, one-handed, ends up on a wet floor. That is why people buy them once
and abandon them.

Here the panel is **hinged at the front crotch and never detaches**. Unhook the
two rings and it falls forward between the legs, still attached. It cannot be
dropped, lost, or contaminated. Rehooking is a one-handed upward pull against a
ring that holds tension while the hand lets go — the same property that makes the
D-ring the right closure for a single hand elsewhere in this wave.

## What is actually solved (not assumed)

### 1. The seated rise tilt — and where it must NOT be taken

The back rise is lengthened and the front rise shortened by `seat_rise_extra`, so
the waistband sits level on a body flexed at 90° instead of gaping at the back
and cutting in at the front.

**The tilt is taken at centre front and centre back only — never at the side.**
Front and back therefore share ONE side-waist point at a common height. This is
the trap the cartridge was written around: apply the tilt at the side too, and
the two side edges differ by the full `seat_rise_extra`, no hem width can bring
them back, and the seam the entire garment hangs from can only be closed by
easing.

```
front_side_mm : 422.40
back_side_mm  : 422.40
side_delta_mm :   0.000
```

Holding at exactly 0.0 across `seat_rise_extra` 0 → 130 mm.

### 2. The hip step — sharing a seam while keeping a wider hip

The back needs more width than the front at the hip, but the bodice side seam has
to be *equal* to the front's. Both cannot be true of one edge. So the bodice side
seam runs between the two points the front also uses, and the back's extra width
lives only on the outer **leg** edge below the waist, joined by a short `hip_step`
edge — a waist dart in all but name.

The back's hem half-width is then bisected until the outer legs measure equal:

```
front_out_leg_mm : 1039.74
back_out_leg_mm  : 1039.76
out_leg_delta_mm :    0.016
```

Note the bisection uses the **same branch-aware technique** as the
`flat-seam-base-layer` cartridge: this length is not monotone in hem width (it
falls to a minimum where the hem point sits below the waist point, then rises),
so the minimum is located first and the search runs on the single monotone branch
that can reach the target. A naive bracket across the minimum has the same sign
at both ends and silently returns an endpoint.

### 3. The panel must actually close the hole

The panel's attached edge and the opening the back leaves are the same seam seen
from two sides. Both are measured off the built pieces, and the panel's own bulge
is bisected until they agree:

```
seat_opening_run_mm : 1091.66
panel_attach_run_mm : 1091.67
panel_delta_mm      :    0.004
```

A drop seat drafted as a rectangle against a curved rise always comes up short —
this is the failure the check exists to catch.

Two further geometry corrections worth recording, because both produced a garment
that verified clean and would have been wrong in fabric:

- **The attach edge must bow OUTWARD.** Bowed inward it still measures the right
  length, but it scoops the volume out — a panel that matches the opening on
  paper and has no seat in it. (Panel area went from 15,769 mm² to 74,031 mm² on
  that one sign flip.)
- **The panel top must finish below the band.** At the first draft it sat 6.7 mm
  *above* the band's lower edge, leaving no rise for the strap to span, and the
  strap length collapsed onto its own floor. It is now held clear by a strap
  width plus a working margin.

### 4. Strap length from measurement

The strap runs from the panel's top corner to its ring. Its length is taken from
the **measured** vertical gap between the built panel and the built band, plus
the ring wrap and an adjustment range — never from a rise formula, because the
rise is the one thing that has just been deliberately tilted.

## Construction notes

- **Four points carry the entire weight of the dropped panel**: both ring anchors
  on the band and both panel corners. Box-and-cross all four.
- **Bag the webbing inside the shell-fabric facing.** Raw webbing against the
  small of the back abrades a body that sits on it all day.
- **Elastic in the FRONT half of the band only.** The back half must stay flat and
  stable — it is what the two rings pull against.
- **A little elastane in the shell is not for fit.** It is so the seat panel does
  not fight the transfer.
- **Check the hem width against the castors.** The constraint warns above
  `hip_girth / 3`; a leg that catches in a front castor is a fall.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `d-ring` solid, **dimensionally**. The
ring's `webbing` parameter — the one driving its `bar_edge` flange, i.e. the sewn
mating edge — is fed from this garment's `strap_width`, which is also a parameter
of the garment's own `drop_seat_suspension` interface. The same number cuts the
strap and sizes the bar it passes over.

Two D-rings cost pennies to print. The same rings and the same panel geometry
convert a jumpsuit somebody already owns — **the pattern is one route to the
result, not a condition for it.**

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `LicenseRef-FC1-pending`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/drop-back-jumpsuit/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `seat`, `band`, `strap`.

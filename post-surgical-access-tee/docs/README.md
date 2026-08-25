# Post-Surgical Access Tee

**FC-300 #249 · adaptive II · `fc` pattern kernel · hardware bridge → Yantra4D `sew-on-snap`**

A tee whose shoulder and upper sleeve open on one straight run of snaps, so a
chest port, a PICC line, a shoulder dressing, a pacemaker site or telemetry leads
can be reached **with the garment still on**.

## What it is

A crew-neck jersey tee: front and back cut on the fold, a dropped set-in sleeve,
and a facing strip. The adaptive geometry is that the shoulder seam is not sewn
shut. It carries a cut-on stand on both sides, and the stand is a snap column
that continues past the shoulder point and down the sleeve's upper seam.

## Why it earns its rank

The clinical reality this is drafted against is mundane and constant. Someone
with a chest port comes in for a flush every few weeks. Someone with a shoulder
repair has a dressing changed. Someone on telemetry needs leads moved. In every
case the instruction is *"take your top off"* — and for a person with a fresh
surgical shoulder, an arm that will not abduct, or a drain pinned to their
waistband, that means being undressed by somebody else in a cold room, or wearing
a hospital gown that opens at the back and covers nothing.

Clinical access clothing does exist commercially. It costs several times what a
plain tee costs and it looks unmistakably medical, which is why the garment
people actually end up in is the gown. That is a loss of dignity with no clinical
purpose whatsoever.

This tee reads as an ordinary crew tee from a metre away. Its opening is a
shoulder seam — which is where a seam belongs anyway — and it runs from the neck
binding to mid-sleeve on a single line of snaps a person can work along one-handed
without looking.

## What is actually solved (not assumed)

A snap pair holds only if the stud lands on the socket. That makes register the
whole ballgame, and three things are solved by measurement rather than formula.

### 1. The snap column, pitched across a MEASURED two-seam run

The access run is not one seam. It is the shoulder seam **plus** the sleeve
split, end to end. So the shoulder is measured off the built front piece and
added to the split run:

```
shoulder_run_measured_mm : 146.35
sleeve_split_run_mm      : 168.00
access_run_total_mm      : 314.35
```

The requested pitch is then treated as a **target, never a result**. Whole
intervals are fitted across the run (less a neck clearance and a tip clearance),
and the pitch is recomputed:

```
snap_pitch_requested_mm : 45.000
snap_pitch_solved_mm    : 46.059     (6 intervals, 7 snaps)
snaps_on_shoulder       : 3
snaps_on_sleeve         : 4
```

Without that recomputation the column drifts, and the last snap lands in a seam
allowance or under the neck binding. The split between shoulder and sleeve is
reported too, so the maker knows how many facings go where.

### 2. Shoulder seam equality — the thing that makes or breaks the column

The back neck sits higher than the front neck. Draft both at the same neck width
and the back shoulder comes out roughly 23 mm longer than the front's. On an
ordinary tee that is a wrinkle. **Here it puts every snap after the first out of
register**, which is a garment that will not shut.

So `NECK_W_BACK` is solved by Pythagoras from the front's *measured* shoulder
length against the vertical offset between the two neck points:

```
front_shoulder_measured_mm : 146.35
back_neck_half_width_mm    : 115.90   (vs a front NECK_W of 78.67)
```

`declare_seam` then checks the two shoulders at `tol=0.5` — tighter than a normal
shoulder seam, because this one carries hardware.

### 3. The access span, reported as a number

"The shoulder opens" is not a specification. The opened panel has to admit a
gloved hand and a dressing tray, not just a cannula. The clear span is derived
from the measured armholes and reported in metadata (`access_clear_span_mm`,
165.5 mm at default size) so the maker can check it rather than trust it. The
front also carries a `port-site-check` marking box at the usual chest-port
location, so the panel can be verified to clear it *before* anything is cut.

The sleeve cap height is likewise bisected against the measured front and back
armholes rather than drafted to a cap formula.

## Construction notes

- **The facing strip is the registration jig.** It is cut to the *measured*
  access run with every snap centre already drilled on its centreline, plus a
  notch and a marking at the shoulder/sleeve junction. Mark the stands from the
  facing, not from a ruler — that is what guarantees all four stands agree.
- **Cut four facings.** One behind each stand: front shoulder, back shoulder, and
  both sides of the sleeve split. A sew-on snap pulled through unbacked jersey
  tears a hole on about the third use, and this garment is opened daily.
- **Bar-tack the head of the sleeve split.** That is where the opening stops and
  where it will tear if it does not.
- **Bind the neck last.** Apply the neck binding *after* the snap stands, or the
  first snap ends up trapped under it.
- **The split is a real edge, not a slash.** The sleeve's split is drafted so both
  sides carry a stand and a facing. A slashed sleeve frays at exactly the point
  that gets handled most.
- **Keep the crew wide and low.** On days when nothing needs opening the tee is
  pulled on normally, and the head still has to pass.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `sew-on-snap` solid, **dimensionally**.
The snap's `snap_dia` parameter — the one driving its `sew_face` flange, i.e. the
sewn mating face — is fed from this garment's `snap_diameter`, which is also a
parameter of the garment's own `access_snap_column` interface. The same number
sizes the snap and the stand it is carried on. `fc_spec`'s
`hardware_dimensional_rules` is what checks that coupling actually exists rather
than merely that the name resolves.

A sew-on snap prints at home in a few minutes. The same hardware and the same
construction convert a tee somebody already owns and already likes — **the pattern
is one route to the result, not a condition for it.**

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/post-surgical-access-tee/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `snap_facing`.

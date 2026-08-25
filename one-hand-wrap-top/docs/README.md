# One-Hand Wrap Top

**FC-300 #248 · adaptive II · `fc` pattern kernel · hardware bridge → Yantra4D `d-ring`**

A wrap top that one working hand can put on, close, adjust and take off — without
help, without teeth, and without pinning anything against the body to hold it.

## What it is

A short-sleeved wrap top in jersey. Two fronts, a back cut on the fold, a set-in
short sleeve, and a tie strip. What makes it adaptive is not a feature bolted on
top of a wrap top; it is the closure and the two front pieces being drafted
differently from the start.

## Why it earns its rank

An ordinary wrap top defeats a single hand **twice**, and both failures are so
ordinary they are rarely named:

1. **The knot needs two hands.** Both wrap edges must be held under tension at
   the same time while a bow is tied. One hand can hold one edge. It cannot hold
   two and tie.
2. **The inner tie is invisible.** The classic construction sends the under
   front's tie out through a hole in the side seam, to be found by feel behind
   the body and brought round. That is a two-handed, sighted-by-touch operation
   at the exact place a hemiplegic or one-handed wearer has least reach.

This top removes both. The under front's tie is **short** and terminates in a
sewn-in **D-ring**. The over front's tie is **long**. Closing the top is: pick up
the long tie, thread it through the ring, pull back on itself. One straight
motion in one plane, and — the part that actually matters — **the ring holds the
tension while the hand lets go**, so the wearer can release, re-grip, and pull
again without losing what they have already gained. Every knot in the world
requires the opposite.

The population this serves is not small or exotic: hemiplegia after a stroke, a
congenital limb difference, a wrist in a cast, an arm in a sling after surgery, a
hand with a tremor or a grip that will not close on a small object, and anyone
holding an infant. They all hit the same wall, which is a fastening that assumes
two hands.

## What is actually solved (not assumed)

The cartridge is a real draft, and three things in it are solved by measurement
rather than by formula.

### 1. The two fronts are not mirror images

An under front only wraps as far as the opposite side seam. An over front must
cross the body, pass that side seam, and keep going. So the two wrap edges are
drafted as real Béziers landing at **different** hem x (`UNDER_X_HEM` positive,
`OVER_X_HEM` negative — the over front crosses centre front and keeps travelling),
and then both are **measured**:

```
under_wrap_measured_mm : 487.60
over_wrap_measured_mm  : 541.72
wrap_run_delta_mm      :  54.12
```

The two tie lengths are then computed from those measured runs plus the girth the
tie still has to cross — never from a rise-plus-girth closed form. The long tie
also responds to `waist_girth` alone (892 mm → 1132 mm across the range), because
it is the waist, not the bust, that it has to travel round.

### 2. Ring register — both anchors at ONE height

If the two tie anchors sit at different heights above the hem, the closed top
pulls one shoulder down and rides up on the other side. So a single `RING_Y` is
chosen, and each front's anchor x is found by **walking that front's own
flattened wrap polygon** until it crosses `RING_Y` — the same polygon the seam
checker measures. Inverting the Bézier analytically would have been shorter and
would have let the drill mark and the measured edge disagree.

### 3. The back neck width, solved by Pythagoras

The back neck sits higher than the front neck. Draft both at the same neck width
and the back shoulder seam comes out roughly 23 mm longer than the front's — a
mismatch that shows as a dragging wrinkle from neck to armhole and is nearly
impossible to diagnose from a finished garment.

So `NECK_W_BACK` is solved from the front's **measured** shoulder length against
the vertical offset between the two neck points:

```
front_shoulder_measured_mm : 132.83
back_neck_half_width_mm    : 102.80   (vs a front NECK_W of 73.33)
```

The two shoulder seams are then equal *by construction*, and `declare_seam` at
`tol=0.5` proves it on every render. The sleeve cap height is likewise bisected
against the **measured** front and back armholes rather than drafted to a cap
formula.

## Construction notes

- **The three load points are the ring tab, the over-front tie anchor, and the
  back tie slot.** Bar-tack all three and interface behind all three. They are
  the only things holding the garment shut; a jersey will tear at an unreinforced
  anchor long before the tie fails.
- **Cut the tie strip twice from one pattern.** The tie piece is drafted at the
  *long* length with the short tie's cut line marked on it (`short-tie-cut`
  internal, plus a notch on the lower edge). One shape, two cuts — so there is no
  second pattern piece to lose and no way to cut two of the same length by
  accident, which is the failure that renders the garment unclosable.
- **Hooks and grip.** `tie_width` is the one dimension that crosses the hardware
  bridge (see below). Widen it for a weak grip — a 50 mm tie is far easier to
  catch and pull than a 20 mm one — and the D-ring's bar widens with it.
- **Ring orientation.** Sew the D-ring with its straight bar against the body and
  the bow outward, so the long tie enters over the bar and the friction of the
  turn does the holding.
- **Jersey, not wovens.** The default fabric is a medium cotton jersey. It
  forgives a wrap pulled a little tighter on a stiff morning; a crisp woven turns
  the same variation into a visible drag line.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `d-ring` solid, and the link is
**dimensional**, not nominal. The ring's `webbing` parameter — the one that drives
its `bar_edge` flange, i.e. the sewn mating edge — is fed from this garment's
`tie_width`, which is also a parameter of the garment's own `ring_closure`
interface. So the same number cuts the tie and sizes the bar it passes over, on
both sides of the bridge. `verify_hardware_links.py` checks the name resolves;
`fc_spec`'s `hardware_dimensional_rules` checks that this coupling exists.

The D-ring is a commodity part, printable at home for pennies, and it works
equally well sewn onto a garment the person already owns. As with the rest of
this wave: **the pattern is one route to the result, not a condition for it.**

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/one-hand-wrap-top/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `under_front`, `over_front`, `back`,
`sleeve`, `tie`.

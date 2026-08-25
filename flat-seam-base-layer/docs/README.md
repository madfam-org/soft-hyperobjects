# Flat-Seam Base Layer

**FC-300 #250 · adaptive II · `fc` pattern kernel · pattern-only (no hardware, by design)**

A long-sleeved base layer drafted so that **no seam crosses a pressure point**.

## What it is

Front and back both cut on the fold, a one-piece long sleeve with a single
underarm seam, and a neck band. Four pieces, five seams, no hardware.

## Why it earns its rank

A seam under a backpack strap is a mild annoyance to most people. To some it is
the reason a day ends early.

The people this is drafted for:

- **Autistic and otherwise sensory-sensitive wearers**, for whom a seam or a
  woven label is not a preference but a hard stop. A label is the single most
  frequently reported reason a sensory-sensitive person refuses a garment.
- **Fragile and hypersensitive skin** — epidermolysis bullosa, graft sites,
  radiotherapy fields, neuropathy, allodynia after shingles.
- **Wheelchair users**, whose whole body weight rests on the ischial tuberosities
  and the shoulder blades for hours at a stretch.
- **Prosthetic socket and brace wearers**, where a seam under a liner becomes a
  pressure sore rather than a complaint.

The conventional answers do not actually work. "Seamless" knitwear still has a
bound neck, a closing seam somewhere, and a heat-set label. Turning a normal tee
inside out moves the *allowance* outward but leaves the seam **line** in exactly
the same place on the body.

So this is drafted the other way round. The seams are moved off the loaded lines
**first**, and the pattern is then solved to whatever that costs.

### Where the seams went

| Seam | Conventional location | Here |
|---|---|---|
| Side | on the lateral pressure line | rotated **forward** off it (`seam_rotation`) |
| Shoulder | on the trapezius crest | rotated **forward** onto the front deltoid |
| Centre front | often a seam | **none** — cut on the fold |
| Spine | often a seam | **none** — cut on the fold |
| Cuff | applied band = a ring at the wrist | deep **fold-back**, no band |
| Label | woven, at the nape | **none** — size printed on the fabric |

The lateral pressure line is what an armrest, a wheelchair side guard, a
waistband and a bra band all load — it is marked on both body pieces
(`pressure-line-cleared`) so a maker can see the clearance they bought and check
it against a real body. The back also carries a `scapula-keep-clear` box: nothing
may be seamed, printed or bar-tacked inside it.

## What is actually solved (not assumed)

### 1. The rotated side seam, and why it is a real problem

Rotating the seam forward makes the front narrower and the back wider. The two
pieces are **no longer symmetric**, so their side edges are no longer
automatically equal — and a flatlock seam cannot ease one edge into a shorter
one without puckering. **A pucker is precisely the ridge this garment exists to
avoid.** This is not a tolerance question; it is the whole thesis.

So the back's hem half-width is bisected until its measured side edge equals the
front's:

```
front_side_mm : 395.77
back_side_mm  : 395.77
side_delta_mm :   0.000
```

Verified at `tol=0.5` — far tighter than a normal side seam — and holding at
`delta 0.0` across the full parameter range (rotation 0 → 110 mm, chest 650 →
1240 mm, hem extra 0 → 220 mm).

### 2. Two traps this solve had to be dug out of

Both are worth recording, because both produced a plausible-looking garment that
was silently wrong.

**Trap one — dropping the whole back hem.** The first draft put the entire back
hem `back_hem_extra` lower, including its side point. That lengthens the back's
side edge by the full drop, and then *no* hem width can bring it back to the
front's: the minimum achievable back edge was 485.75 mm against a front of
395.77 mm. The seam was over-constrained and could only have been closed by
easing — i.e. by the pucker.

The fix: **the back's side hem point sits at the same height as the front's**,
and all the extra back length is taken at centre back as a swept hem. That is the
general lesson for any open or asymmetric side seam — share one side point at a
common height, take the rise or drop at CF/CB, and bisect the hem width to close
the residual.

**Trap two — the length is not monotone in hem width.** Even after the fix, the
side-edge length **falls to a minimum** where the hem point sits directly below
the side-top point, and rises again on either side. A naive bracket spanning that
minimum has the *same sign at both ends*, so sign-based bisection silently falls
back to an endpoint — which is how the seam ended up 38 mm out while the solver
reported success.

The fix: locate the minimum first (it is at `x = BACK_HALF_NOMINAL`), then bisect
on the single **monotone branch** that can reach the target, preferring the
tapered branch because a base layer wants its hem drawn in rather than flared. If
the target lies below the achievable minimum, the minimum is returned and the
residual is *reported in metadata* rather than hidden.

### 3. Shoulder and cap

The back neck width is solved by Pythagoras from the front's **measured**
shoulder length — and here the back shoulder also starts from a different outer
x, because the shoulder itself has been rotated forward. Drafting both at one
neck width mismatches by roughly 23 mm; on a flatlocked base layer an eased-in
shoulder is a pucker, and a pucker under a strap is the exact ridge this garment
avoids.

**Cap ease is zero.** Ease is fabric gathered into a shorter edge; on this
garment that is a ripple under the sleeve head. Zero is a deliberate choice, not
an oversight, and the neck band is likewise cut to the *measured* neckline and
then shortened by a stretch factor chosen so the band holds without needing to be
stretched hard enough to roll — a rolled band is a cord across the collarbones,
which for this wearer is worse than no band at all.

## Construction notes

- **Flatlock (coverstitch) every seam, stitch side against the skin.** Use a
  textured/woolly thread: on this garment the thread *is* the surface the body
  touches.
- **Keep allowances small.** They are set to 8 mm by default and 12 mm at the
  hems for a reason — a wide allowance folded back **is** the ridge.
- **No woven label anywhere.** Print the size and care mark directly on the
  fabric at the marked location.
- **Pre-wash the fabric.** A finish that softens after three washes has already
  cost this wearer three days.
- **The cuff is a fold-back, turned twice.** An applied cuff means a seam ring
  exactly where a watch, a splint, a cannula dressing or a walking-frame grip
  sits.

## Why there is no hardware

This cartridge is **pattern-only by design**, not for want of a solid on the
shelf. The entire adaptive claim is *where the seams are and are not*; adding a
fastening would add the one thing the garment is defined by not having. It is
also the practical point: this can be made by anyone with a coverstitch machine
and **no printer, no supplier and no proprietary notion**, and everything it
claims can be checked against the marked pressure lines on a real body.

Recorded for the wave report as `co-create:flat-seam-base-layer` — no
`notion.hardware_ref`, and `hyperobject.capabilities.hardware_bridge` is `false`.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/flat-seam-base-layer/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `front`, `back`, `sleeve`, `neck_band`.

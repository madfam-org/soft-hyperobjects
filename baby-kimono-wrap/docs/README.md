# Baby Kimono Wrap

**FC-300 #289 · kids_baby · tier 1 · `fc` pattern kernel · no hardware**

A newborn's first shirt. It never goes over the head, and it has no closure of
any kind.

## What it is

Five pieces, all flat: a back cut on the fold, two mirrored fronts that cross
over it, a shallow flat-set sleeve, one binding strip, and four side ties. The
shoulder is **not a seam on the back** — the back is cut in one piece from hem to
neck, which is what "seamless-shoulder" means here and what makes the whole neck
run a single continuous bound edge.

The baby is laid down on the open garment; the fronts are folded across; the ties
are knotted at the side. Nothing is pulled over the skull and no arm is pushed
through a tube.

## Why it earns its rank

`kids_baby` was the thinnest family in the 300-rank catalog (4 entries before the
long tail). It also had a hole in it: every existing infant cartridge in the
commons — `baby-bodysuit`, `baby-sleeper` — still puts *something* over the head
or closes with snaps. For the first few weeks of a life, and for the whole of a
NICU stay, neither is what a parent actually wants.

A newborn cannot hold their own head up. Dressing one is the thing first-time
parents are most openly afraid of. The commercial answer is a wrap bodysuit sold
as a hospital or premature item at several times the price of a plain one. This
is four flat pieces of the softest jersey a household can find — including a
worn-out adult t-shirt, which is usually the softest cotton already in the house
— sewable by someone whose entire experience is a straight stitch.

## What is actually solved (not assumed)

This is an honest tier-1 garment: no closures, no shaping to trust, no hardware.
But "simple" is not the same as "guessed", and two numbers are computed rather
than picked.

### 1. The crossover is derived, then CLAMPED

Each front carries its crossover as part of the piece, so the panel is
`W + WRAP` wide where `W` is the quarter chest. The overlap is derived from `W`:

```
wrap_overlap_requested_mm : 57.75      (¼ chest × wrap_depth)
wrap_overlap_clamped_mm   : 57.75
wrap_overlap_was_clamped  : false      (true at the parameter extremes)
```

The clamp is `WRAP ≤ W − 45`. Without it, a small chest with a deep `wrap_depth`
produces a front **narrower than its own overlap** — geometry that folds inside
out. The kernel's `Piece._validate_and_normalize` CCW-normalizes an inverted
outline and `area()` takes an absolute value, so such a piece passes `verify()`
looking entirely healthy. It is caught here, at the source, rather than
discovered on a cutting table.

### 2. The armhole depth is clamped against the MEASURED body length

An infant torso is short. `AH` is scaled off the chest in the usual way and then
clamped to `L − 70`, because at the small end of the chest range a chest-scaled
armhole reaches past the hem and the side seam — the seam the ties are caught in
— disappears entirely.

### 3. The binding is cut to a MEASURED run, not a neck formula

On a seamless-shoulder kimono the binding goes on in one pass: up one wrap edge,
around the back neck, down the other wrap edge. So the strip is cut to that
measured total:

```
wrap_edge_run_mm    : 171.43   (×2)
back_neck_run_mm    :  95.39   (both halves of the fold)
binding_run_total_mm: 438.25
```

`declare_seam` then checks the strip against all four measured edges with the two
joins as declared ease, landing at delta ≈ 0.

The sleeve is likewise solved: the cap height is fixed deliberately shallow (a
kimono cap, not a shirt cap) and the **half-biceps is bisected** until the
measured cap equals the measured front + back armholes exactly, with zero ease —
a flat-set jersey sleeve goes in before the side seam and takes none.

## Construction notes

- **Sew the sleeve in flat.** Cap to armhole while the garment is still open,
  *then* close the side seam and the underarm in one run. That is why the cap
  carries no ease.
- **Bind in one pass.** Start at one front hem, run up the wrap edge, around the
  back neck, down the other side. The strip carries `back-neck start` and
  `back-neck end` marks so it is positioned by its own marks instead of eased in
  by eye.
- **Catch the ties in the side seam.** Two ties inside (they hold the under-front
  shut), two outside. Bar-tack each one where it is caught — that join takes
  every pull the garment ever gets.
- **The cuff turns back.** The sleeve carries a marked `mitten-cuff fold`; turned
  up it covers the hand for the first weeks, turned down it is a normal cuff.
- **Wash the fabric before cutting.** This garment is laundered daily and cotton
  jersey shrinks on its first wash.

## No hardware, deliberately

`needs` for this entry is `["pattern"]` only, and that is a design decision, not
a gap. A snap, button or buckle at the front of a newborn wrap is a hard object
pressed between an infant's chest and an adult's forearm for hours at a time.
The ties sit at the side seam where nothing is lain on.

For an infant garment that *does* bridge to hardware, see `baby-bodysuit` (snap
crotch) — the crotch is under the garment, not against the front of the chest.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `CERN-OHL-W-2.0`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/baby-kimono-wrap/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `back`, `front`, `sleeve`, `binding`,
`tie`. Presets: `newborn`, `six-months`, `twelve-months-deep-wrap`.
Body preset reference: `bodies/infant-6m`.

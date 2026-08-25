# Denim Chore Apron

**FC-300 #291 · denim · tier 2 · `fc` pattern kernel · hardware bridge → Yantra4D `rivet`**

The cross-back work apron. **No neck strap at all** — and every load path ends in
a rivet.

## What it is

Three pieces: the body (bib and skirt in one, cut on the fold), a cross-back
strap cut twice, and a divided patch pocket cut on the fold. Two straps run from
the bib's top corners, cross between the shoulder blades, and tie to the opposite
waist.

## Why it earns its rank

`denim` was one of the two thinnest families in the 300-rank catalog, and this
fills the gap at the *simple* end of it — the family's other entries are all
tailored garments.

A neck-loop apron transfers the whole weight of a loaded pocket onto the cervical
spine. People who wear one for a full shift — cooks, welders, potters, mechanics,
barbers — end the day with the specific ache that comes from it. The cross-back
harness is the fix, it has been known for a century, and it is nonetheless the
version sold at a premium as an "artisan" product while the neck loop stays
standard.

## What is actually solved (not assumed)

### 1. The strap is a HYPOTENUSE

This is the cartridge's whole reason for existing. A crossing strap does **not**
run straight down the back. It runs diagonally from one bib corner, over the
shoulder, across the back, to the **opposite** waist anchor. So its length is
solved by Pythagoras from a measured horizontal spread and a measured vertical
drop:

```
strap_dx_mm          : 650.00    (back width + both anchor offsets)
strap_dy_mm          : 330.00    (bib top down to the waist)
strap_diagonal_mm    : 728.97
shoulder_arc_mm      : 109.20
strap_path_solved_mm : 838.17

strap_path_naive_mm  : 439.20    (vertical drop + arc — what a guess produces)
naive_shortfall_mm   : 398.97
```

**399 mm short.** That is not a fitting adjustment; it is a strap that cannot be
crossed at all. `strap_dx` is the number a naive draft omits entirely, and it is
the larger of the two components.

The strap carries a `waist anchor point` mark where the diagonal ends and the tie
tail begins, and a `shoulder crossing point` mark, so the maker positions it by
its own marks rather than by holding the apron up and guessing.

### 2. The rivets sit where the load paths terminate

Eight rivets, none decorative:

| Site | What pulls on it |
| :-- | :-- |
| Bib corners (×2) | the straps |
| Waist anchors (×2) | the opposite strap |
| Pocket outer corners (×2) | a hand going in with a full weight of tools |
| Pocket divider (×2) | the two compartments pulling apart |

Each is placed by **measuring the piece it lands on** and stepping in from *both*
edges by the cap's own diameter plus a clearance — so a rivet is never set
through a turned hem (where it holds nothing) nor close enough to an edge to tear
out through it. Each is drawn to **actual size** as a ring at the cap diameter,
not as a symbol, so the maker can see whether the cap really clears the topstitch
line beside it.

**Why rivets and not bar-tacks.** On 12 oz denim the thread abrades before the
cloth does. A bar-tack is the thing that gives first; a rivet moves the load into
the cloth and spreads it over the cap. The BOM lists the setting die as a
required tool, because a rivet set with a hammer and no die deforms the burr and
the joint works loose.

### 3. Everything derived is clamped

```
bib_half_requested_mm     : 150.00   bib_half_clamped_mm     : 150.00
pocket_half_requested_mm  : 200.00   pocket_half_clamped_mm  : 200.00
pocket_height_requested_mm: 220.00   pocket_height_clamped_mm: 220.00
```

All three report `..._was_clamped`, and all three bind at the parameter extremes.
`HALF_BIB` is clamped **both ways** — capped against the skirt below it (a bib
wider than the waist turns the underarm sweep inside out) and floored on the
strap width plus a margin (the bib has to carry both strap ends and their
turnings). The pocket is capped against the skirt's width and its length.

Without those clamps the offending piece still renders and still passes
`verify()`: the kernel CCW-normalizes an inverted outline and `Piece.area()`
takes an absolute value, so inside-out geometry reports a healthy positive area.
Every cartridge in this build is rendered at the min *and* max of every parameter
for exactly that reason.

### 4. Three declared seams on an almost-seamless garment

A chore apron is deliberately nearly seamless — the body is one piece and every
outer edge is turned, not joined. What is declarable is checked:

- `pocket.side` vs `pocket.cf_fold` — proves the pocket did not invert (on an
  inverted outline the CCW normalization reverses the edge order and `side` would
  no longer measure the clamped `POCKET_H` it was drafted to).
- `strap.lower` vs `strap.upper` — both long edges fold to the same centre line,
  so they must measure identically.
- `body.bib_top` vs `strap.bib_end` with the bib's floor margin as declared ease
  — goes red the day the floor is loosened or the strap widened past what the bib
  can receive.

## Denim-family conventions

Carried from `jeans-5-pocket`, `denim-jacket` and `bib-overalls`:

- **7 mm twin-needle topstitch gauge** on every turned edge, both strap edges, the
  pocket mouth and both dividers.
- **Turned, not seamed.** Every outer edge takes the hem allowance and is turned
  and topstitched.
- **Every hard good is a Yantra4D reference**, never re-implemented here.
- **12 oz mezclilla is right** for this one garment in the family — it is
  *supposed* to be stiff, and it softens exactly where it is used.

## Construction notes

- **Turn and topstitch every outer edge first**, before anything is attached.
  Once the straps are riveted on you cannot get the body flat under the machine.
- **Set the rivets last**, through all the layers that will actually be there in
  wear. A rivet set through the strap alone and then sewn down does nothing.
- **Cross the straps, do not parallel them.** Parallel straps slide off the
  shoulders under load; the crossing is what holds them on, and it is why the
  strap is a diagonal in the first place.
- **The pocket gets four compartments** on the finished apron (two per half,
  drafted on the fold). The dividers are topstitched, and both ends of each
  divider are riveted.
- **The tie tail** is sized at 22% of the strap path with a 120 mm floor —
  enough to knot at the side, not so much that it hangs into the work.

## Hardware bridge

`notion.hardware_ref` links to the Yantra4D `rivet` solid, **dimensionally**. The
rivet's `cap_dia` — the parameter driving its `set_face` flange, i.e. the face
that bears on the cloth — is fed from this garment's `rivet_cap`, which is also a
parameter of the garment's own `riveted_bib_anchor` and `riveted_pocket`
interfaces. **One number sizes the rivet and places it**: the same `rivet_cap`
sets every rivet's step-in from the edges it lands between. `post_dia`,
`bore_dia` and `burr_dia` all scale from it, so the burr matches the post it is
set over.

## Provenance

Original draft for Fashion Cabinet (Innovaciones MADFAM). No third-party pattern
lineage. Commons licence: `LicenseRef-FC1-pending`.

## Render

```
python apps/api/services/engine/fc_runner.py \
  projects/denim-chore-apron/main.py out.json '{}' json
```

`target_piece` accepts `set` (default), `body`, `strap`, `pocket`. Presets:
`workshop-full-length`, `kitchen-short`, `narrow-frame`.

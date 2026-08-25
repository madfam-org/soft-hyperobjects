# Epaulette Dress Tunic

The first garment in the commons that *mounts* the Yantra4D shoulder board.

## Provenance

The dress tunic is the high-collared, straight-fronted uniform coat that arrived with
nineteenth-century military reform and then spread far past the army: marching bands,
honour guards, cadet corps, drum corps, hotel doormen, cinema ushers, orchestra
attendants. Wherever an organisation wants a person to read as *representing* it rather
than as an individual, this is roughly the garment it reaches for.

Its defining feature is not the collar and not the closed front — both of those it
shares with a dozen other tunics. It is the **shoulder board**: a rigid, tapered plate
sitting flat along each shoulder, carrying rank or unit insignia, sewn into the shoulder
seam at its wide end and buttoned down at its narrow one. Take the boards off and the
garment stops being a dress tunic.

## Why this earns a commons rank

Because the board is what the FC-300 mandate calls a **shelf consumer**. Yantra4D's
`epaulette-board` solid already existed, and the commons already held
`printed-epaulette` — but that is a *notion*: a finding with a placement guide, bridging
the board as a component. Nothing in the commons actually **wore** one.

This cartridge is the garment that does, and the bridge is dimensional rather than
nominal. `shoulder_len`, `board_wide_w` and `board_narrow_w` size the printed board *and*
the fabric tab drafted here; `board_button_dia` drives the board's own button boss *and*
the drilled retaining mark on the tab and the shoulder. There is no separate "tab size"
parameter that could be set inconsistently with the board — the sleeve of cloth and the
board inside it are driven by one set of numbers, so they cannot drift apart.

## Construction notes

Five pieces: **front** (cut 2), **back** (cut 1 on the CB fold), **sleeve** (cut 2),
**collar** (half on the CB fold) and **epaulette tab** (cut 2).

**The board seat is marked on the garment, not just on the tab.** Both the front and the
back carry the board's own outline drawn along the shoulder seam, computed from the
seam's actual direction vector — wide end at the shoulder point (where the board is
widest and the shoulder broadest), narrow end at the neck point, with the retaining
button drill exactly at the narrow end. Marking it on both panels means the front and
back tab positions cannot disagree.

**The tab is the board plus turn-under.** It is drafted to the board's footprint with
`seam_allowance` added on the three free sides and extra at the seam end, tapering from
`board_wide_w` at the armhole to `board_narrow_w` at the neck. Its board outline is
marked *inside* the turn-under so the maker can see exactly where the rigid board must
land.

**The board seam is declared with honest ease.** The tab's wide end is caught in the
shoulder seam, but the shoulder is much longer than the tab is wide — the tab sits *on*
the seam, it does not replace it. That surplus is declared as `ease` on the seam check
rather than hidden behind a loosened tolerance, so the render proves the tab is exactly
as wide as the board it covers.

**The collar is solved.** Its neck edge is bisected to the *measured* front plus back
necklines. On a dress tunic the stand is the piece that holds the posture; a collar cut
to an assumed length either strangles or gapes, and both are visible at ten paces on a
parade ground.

**The front button count is derived**, from the clamped closure run over the pitch — so
changing the tunic length or the pitch re-solves the ladder rather than leaving a fixed
count of buttons in the wrong places.

## The clamps, and why they are load-bearing

Three quantities here are *derived*, and a derived dimension that goes negative does not
fail loudly — it inverts the piece, and the kernel's CCW normalization then hands
`verify()` an outline that looks perfectly valid. Each carries an explicit bound applied
**before any point is built**:

| Derived quantity | Bound | What it prevents |
| :-- | :-- | :-- |
| board length | 50 mm … measured shoulder seam − 10 | a board emitted hanging off the shoulder |
| board narrow end | ≤ board wide end | a wedge tapering the wrong way, which is not a board |
| front closure run | 120 mm … neckline − 60 | buttonhole marks landing above the neck or off the hem |
| front button count | 2 … 14 | a fine pitch asking for dozens of marks, or a run with none |
| armhole depth | 175 mm … `tunic_length − 230` | the chest line landing near the hem |

`metadata.solved` reports `board_clamped`, `taper_clamped` and `button_run_clamped` on
every render, so a clamped draft is visible rather than silent. The cartridge was probed
at the min **and** max of every one of its 15 parameters, at all-min, all-max and two
mixed-extreme combinations, and at each `target_piece` — 40 renders, all with zero error
issues and every declared seam balancing. The two board-hostile cases (maximum board
length with an inverted taper on the smallest body; minimum length with the widest board
and the finest button pitch on the largest body) were inspected edge-by-edge: in the
first, the board correctly clamps to the 130.7 mm shoulder and the taper collapses to a
parallel 20 mm strap rather than inverting.

## Hardware

The shoulder boards bridge to the Yantra4D **`epaulette-board`** solid via
`notion.hardware_ref`, with seven mapped parameters:

| Board parameter | Driven by | Note |
| :-- | :-- | :-- |
| `board_len` | `shoulder_len` | the shared length; also the tab's length |
| `wide_w` | `board_wide_w` | armhole end, sewn into the shoulder seam |
| `narrow_w` | `board_narrow_w` | neck end, where the button goes |
| `button_dia` | `board_button_dia` | the same value drills the retaining mark |
| `plate_t` | 2.4 mm | a plate that holds flat without reading through the cloth |
| `rim_h` / `rim_w` | 2.0 / 1.6 mm | the rim the tab's turn-under grips |

The first four are the dimensional handshake — each is driven by a garment parameter
that also drives the garment's own `shoulder_board` interface, so the same numbers reach
the cloth edge and the printed edge. The last three are fixed printing dimensions with
no garment counterpart, declared as numeric literals rather than invented parameters.

## Honest simplifications

- **No insignia, rank marks, braid, piping or lace are drafted.** These are entirely
  organisation-specific, and a default would be an invention with real social meaning
  attached — exactly the kind of thing the commons should not guess at. The board is
  drafted as a blank carrier.
- **A one-piece set-in sleeve**, not the two-piece tailored sleeve of `suit-jacket` or
  `morning-coat`. Uniform tunics are made both ways; the one-piece is the more common
  and much the more repairable, which matters for a garment worn by a rotating group.
- **No drafted lining and no pockets.** Dress tunics are usually half-lined and often
  have no external pockets at all by design. Lining is BOM-noted, not drafted.
- **The back is cut on the fold with a marked vent**, not seamed at the CB. A CB seam
  gives better fitting range; the fold is what a uniform maker cutting many tunics to a
  size run actually does, and it is what the vent marking assumes.
- **The tab is drafted flat.** A shoulder board sits on a curved shoulder, so a very long
  board on a very sloped shoulder wants a slight curve in the tab. That is a
  second-order refinement and would need a shoulder-curvature input the body schema does
  not yet carry.

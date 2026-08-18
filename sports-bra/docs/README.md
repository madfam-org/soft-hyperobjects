# Sports Bra (compression) — FC-100 rank #12

A **compression-style** athletic bra: a no-hardware pullover that supports by
tensioning power-stretch against the body — **not** by encapsulating each
breast in a wired, molded cup. This is the honest compression teaching draft;
a wired/molded encapsulation bra is a separate future cartridge.

Pieces (four, all cut on the fold):

- **Front (scoop)** — a deeper scoop neckline with grown-on straps at the
  shoulder point.
- **Back (racer)** — sits high at center and the grown-on straps converge
  toward the spine (the racerback signature). Both shells taper from the bust
  half-width down to the underbust half-width.
- **Underband (compression)** — a wide band whose top edge equals the summed
  shell lower edges **by construction** (both are fold-cut halves). Its bottom
  edge is the elastic underband hem.
- **Front Lining (inner support)** — an optional inner front layer,
  understitched to the shell for a double layer of support without wire. It is
  caught in the same side and underband seams (not sewn as a separate ring),
  so it carries no extra seam checks.

## What this cartridge teaches

**Negative ease + matched elastic accounting** (mirrors `panties-bikini`) laid
over **bound-edge tank construction** (mirrors `tank-top`):

- Every girth-derived width is multiplied by `NEG = 1 - negative_ease_pct/100`,
  so the flat pattern is drafted **smaller** than the body and the fabric
  tensions to fit. Compression bras run higher negative ease (~15–25%) than a
  soft bra because the power-stretch interlock recovers hard. Body girths stay
  full-body measurements — the reduction is baked into the draft, not asked of
  the user.
- Three seams are **declared and verified** at render time, all balancing to
  `delta ≈ 0`: `front.shoulder ↔ back.shoulder` (equal-length grown-on strap
  tops), `front.side ↔ back.side` (identical shell sides), and
  `underband.top ↔ front.band_join + back.band_join` (the band matches the
  summed shell lower edges because everything is fold-cut).
- Neckline, armholes and the underband hem carry **zero seam allowance**
  (elastic/bound finish, with marked application zones as internal traces), and
  the BOM emits **exact-mm elastic cut lengths** recomputed from the measured
  openings for any body size: neckline elastic = full neck opening × 0.88,
  underband elastic = full underband opening × 0.92, per-arm armhole elastic =
  (front + back armhole) × 0.85.

**No hardware, by design.** No wire, hooks, rings or sliders — the pull-on is
the whole point. Any optional bra hardware would be a Yantra4D notion cartridge
referenced via `notion.hardware_ref`, never drafted here.

## Known v0 simplifications (documented, not hidden)

- **Compression, not encapsulation:** a single tensioned shell, no separate
  cup pieces, no wire channel, no bust-apex dart. Support comes from the
  underband compression and the double front layer.
- The straps are **grown-on** (continuous with the shell, meeting at a shoulder
  seam), not adjustable set-in straps with sliders.
- Front and back share one **side** profile and one bust/underbust taper, so
  the side seams match by construction; back-specific ease is expressed through
  the neck drop and racer pull-in only.
- The front lining duplicates the full front outline (understitched), rather
  than a separately shaped power-mesh cradle.

```bash
python apps/api/services/engine/fc_runner.py projects/sports-bra/main.py sports-bra.svg '{}' svg
```

Official visualizer and configurator: Fashion Cabinet.

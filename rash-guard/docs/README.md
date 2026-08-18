# Rash Guard — FC-100 #57 / Playera de licra

**EN** — A rash guard is a second-skin long-sleeve top worn for sun protection
and chafe-free surf/swim wear. It is, geometrically, a *fitted long-sleeve tee*
in a stretch swim fabric: the only real differences from an ordinary knit top
are (1) it is drafted **smaller than the body** (negative ease) so the fabric
tensions to fit, and (2) its seams are finished **flatlock/coverstitch** so they
lie flat against bare skin. This cartridge draws the long-sleeve fitted knit
block, applies the negative-ease reduction, and finishes the neckline with a
bound self strip.

**ES** — Una playera de licra (rash guard) es una prenda de manga larga de
segunda piel para protección solar y uso sin rozaduras en surf/baño.
Geométricamente es una *playera entallada de manga larga* en tela elástica de
baño: las únicas diferencias reales frente a un top de punto común son (1) se
traza **más pequeña que el cuerpo** (holgura negativa) para que la tela se ajuste
bajo tensión, y (2) sus costuras se rematan **flatlock/recubridora** para que
queden planas contra la piel. Este cartucho traza el bloque entallado de manga
larga, aplica la reducción por holgura negativa y remata el escote con una tira
de la misma tela.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front | Delantero | 1 on fold (mirror) |
| `back` | Back | Trasero | 1 on fold (mirror) |
| `sleeve` | Sleeve (long, tapered) | Manga (larga, entallada) | 2 (mirror) |
| `neck_binding` | Neck binding (bound crew) | Tira de escote (redondo) | 1 on fold at CB (mirror) |

Dispatch on the `target_piece` parameter (`front` \| `back` \| `sleeve` \|
`neck_binding` \| `set`); `set` (default) builds all four and declares every seam.

## Construction order / Orden de confección

1. **Flatlock or coverstitch the shoulders** — front↔back at the shoulder seam.
2. **Set the sleeves in flat** — sleeve `cap` into the joined front+back
   `armhole`. Knits set with little to no cap ease (`cap_ease` defaults to 0),
   so the sleeve goes in flat before the side is closed.
3. **Close each side and sleeve underarm in one pass** — front `side` ↔ back
   `side`, continuing up the sleeve `underarm_front` ↔ `underarm_back`.
4. **Bind the neckline** — fold the `neck_binding` strip lengthwise, apply it
   **stretched** around the crew opening (cut length = opening × `binding_ratio`),
   and coverstitch. The strip's attach edge is drafted to the opening, so the
   pattern balances; the stretch is taken up at the machine.
5. **Coverstitch the body hem and the wrist cuffs.**

Every structural seam is a **flatlock or 3-thread coverstitch** — that flat,
low-profile finish is the whole point of a rash guard against skin. Sew on a
stretch/overlock machine with a ballpoint (75/11) needle and textured
wooly-nylon looper thread.

## Honest simplifications (teaching-grade)

- **Flatlock is a seam *treatment*, not geometry.** The pieces here are a normal
  fitted tee. Flatlock shows up three ways only: modest **7 mm** seam allowances
  (the range a flatlock/coverstitch foot wants), the flatlock/wooly-nylon thread
  line in the BOM, and these notes — not as any change to the outlines.
- **Negative ease is baked into the draft, not asked of the user.** You still
  enter your true full-body `chest_girth` and `neck_girth`; the script multiplies
  the girth-derived widths by `NEG = 1 − negative_ease_pct/100` (default 10%).
  Because the reduction is applied equally to both sides of every seam, matched
  seams stay matched (all deltas ≈ 0). The swim-tricot fabric card carries a
  `cut_scale < 1.0` that encodes the same idea for the digital twin.
- **The neckline seam is expressed through the fold.** Front and back necks are
  each drafted at half (they are cut on the fold), so the binding is likewise
  cut on the fold at center-back and drafted to that same half-opening — the
  declared `neck_binding.neckline ↔ front.neck + back.neck` seam balances at
  delta ≈ 0. The exact-mm **stretched** binding cut length (opening ×
  `binding_ratio`) lives in the BOM and metadata, the way factories keep it on a
  private spec sheet.
- **Cap solved, not eyeballed.** The sleeve-cap half-breadth is found by
  bisection so the cap length equals the front+back armhole (plus any `cap_ease`);
  the solver raises if it cannot converge rather than shipping a loose seam.
- **UPF is a fabric property, reported not modeled.** A tightly-knit
  nylon/elastane at this gsm reads UPF 50+ when worn to fit; the BOM/metadata
  carry that note. Negative ease keeps the knit stretched thin enough to stay
  UV-rated.
- **Straight hems.** Body and cuff hems are straight (the brief allows straight
  or slightly curved); this keeps the side seams matched without a hem-shaping
  solve.

## Hardware / Herrajes

None. A rash guard has no buttons, zips, or buckles. Any future hardware variant
(e.g. a front-zip surf top) would reference a **Yantra4D** cartridge through the
manifest `notion.hardware_ref`, never re-implemented here.

---

Official visualizer and configurator: **Fashion Cabinet** ·
Visualizador y configurador oficial: **Fashion Cabinet**

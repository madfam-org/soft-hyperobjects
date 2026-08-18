# Track Pants — FC-100 rank #50

The classic athletic track pant, drafted as the side-seamed trouser block
restyled for sportswear. It reuses the joggers/sweatpants leg family — a
separate front and back leg (cut 2 mirror each) with the front inseam bowed by
a **solved** amount until it matches the deeper back fork, and equal side seams
by construction — but cut **relaxed**: a straight-to-slightly-tapered leg with
small **positive** ease (`relaxed_ease` added to the hip girth). This is *not*
a compression cut; the power-stretch interlock only lends comfort give, and the
metadata says so explicitly.

The signature is the **side stripe**. One or two contrast stripes run the full
outseam of both legs, modelled as `kind="trace"` internals laid parallel to the
`side` edge on the front *and* back legs, aligned across the side seam. The BOM
emits the exact contrast-tape length: `2 legs x outseam x stripe_count`.

The ankle is either an **elastic/rib cuff** (cut 2, length = ankle opening x
`cuff_ratio`) or, with `cuffed` off, a plain open hem. The waist is an elastic
**casing** (cut 1) whose length is derived from the summed leg waists, with an
optional **drawcord** threaded through two marked centre-front eyelets.

El pantalón deportivo (track) clásico: mismo bloque de pantalón con costura
lateral que joggers/pants, pero holgado (pierna recta, holgura positiva — no
compresión), con la franja lateral de contraste característica, puño de tobillo
elástico/rib opcional y pretina de casing con cordón opcional.

## Pieces

- **Front Leg** (`front`) — cut 2 mirror. Carries the side-stripe trace(s).
- **Back Leg** (`back`) — cut 2 mirror, wider with the deeper fork. Same stripe(s).
- **Ankle Cuff** (`cuff`) — cut 2, elastic/rib, only when `cuffed` is on.
- **Waistband Casing** (`waistband`) — cut 1, fold-over, with drawcord eyelets
  when `drawcord` is on.

## Construction order

1. Topstitch the contrast stripe(s) down each leg's outseam (front and back)
   **before** closing the side seam — flat is easier than in the round.
2. Sew inseams (front↔back), then outseams (front↔back). Both balance to delta ≈ 0.
3. Join the two legs at the centre-front/centre-back crotch.
4. Close each ankle cuff into a ring and coverstitch to the leg hem (cuffed), or
   turn and topstitch the open hem.
5. Close the waistband casing into a ring, attach to the waist, leave a gap and
   feed the elastic; set the two eyelets and thread the drawcord.

## Honest v0 simplifications (documented, not hidden)

- **Relaxed fit via positive ease, no negative-ease scaling.** Unlike the
  compression garments in this cluster (leggings, panties), a track pant is
  relaxed, so fit is driven by `relaxed_ease` added to the hip — not by cutting
  under the body. The fabric card's `cut_scale < 1.0` is *not* applied here.
- **Stripe as a placement trace, not a seamed inset panel.** The stripe is a
  contrast tape topstitched on top (the common construction), not a cut-in
  contrast panel; it is drawn as an internal guide riding the outseam.
- **Cuff/casing are rectangles** sized from the measured openings; their join
  allowance is carried as an exact `ease` on the declared seam so lengths still
  balance to delta ≈ 0 (the cuff is deliberately smaller than the ankle — the
  rib recovers).
- **Eyelets are hardware**, referenced as a Yantra4D cartridge in the BOM note,
  never re-drafted here (per the federation contract).

```bash
python apps/api/services/engine/fc_runner.py projects/track-pants/main.py track-pants.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/track-pants/main.py open.svg '{"cuffed": false, "stripe_count": 1}' svg
```

Official visualizer and configurator: Fashion Cabinet.

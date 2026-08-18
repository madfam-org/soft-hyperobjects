# Puffer Jacket — FC-100 rank #31

A roomy insulated zip jacket (ES: *chamarra acolchada*) on the **bomber-jacket**
(rank #29) architecture, itself the **zip-hoodie** (rank #14) front. The front is
**cut 2 mirrored** — never on fold: its center edge is the **separating** zipper
seam, with a 15 mm tape allowance, top/bottom stop notches, and a 7 mm stitch
line (zipper-notion's installation convention). The body is drafted with a large
default ease (300 mm) for insulation loft and layering over other garments.

## The signature — quilt channels

Every shell piece (front, back, sleeve) carries **horizontal quilt channels**
drawn as `fc.Internal(kind="trace")` lines every `channel_spacing` mm (default
80). Each channel is clipped to that piece's silhouette by scanning the stitch
ring for the scanline crossing (`_x_span_at`), so no trace runs off the cut
edge. The garment is **shell + downproof lining quilted to each other over the
fill**, channel by channel — the geometry stays a normal roomy jacket; the
channels are markings, exactly like the blazer's pocket traces. A production
puffer would add baffle geometry (box-wall or sewn-through) and a wind flap
behind the zip; that is called out as teaching-grade in the metadata.

## Pieces

- **front** (cut 2, mirrored): quilted half front; center edge = zipper seam;
  24 mm hem allowance for the elastic casing.
- **back** (cut 1 on fold): quilted back.
- **sleeve** (cut 2, mirrored): quilted long sleeve; the **cap is solved by
  bisection** against the measured armhole pair (front + back), delta ≈ 0.
- **collar** (cut 1 on fold): self-fabric **funnel (stand) collar**, derived —
  cut on fold at center back, so its drafted neck edge is `neck_opening/2 +
  seam_allowance` and sews to one front + one back neck with the 1 sa as the
  declared ease (delta ≈ 0).
- **cuff** (cut 2): **elastic band**, derived length = sleeve opening ×
  `cuff_ratio`, folded to 2 × `cuff_height` with elastic threaded through.

The hem is an **elastic-cased finish** (no separate piece): a 24 mm hem
allowance forms the casing, elastic length = hem circumference ×
`hem_elastic_ratio`.

## Construction order

1. Quilt each shell panel to its lining over the fill along the channel traces.
2. Sew shoulders, then set the sleeve caps into the armholes, then close the
   side + underarm seams in one pass.
3. Sew the funnel collar to the neckline (fold at CB), turn and edgestitch.
4. Join each cuff into a ring, attach to the sleeve hem, thread the cuff elastic.
5. Install the separating zipper along the two center-front edges (stops at the
   notches); fold and stitch the hem casing and thread the hem elastic.

## Declared seams (all delta ≈ 0)

| seam | ease | tol |
| --- | --- | --- |
| front.side ↔ back.side | 0 | 1.5 |
| front.shoulder ↔ back.shoulder | 0 | 1.5 |
| sleeve.cap ↔ front.armhole + back.armhole | 0 | 2.0 |
| sleeve.underarm_front ↔ sleeve.underarm_back | 0 | 1.0 |
| collar.neck ↔ front.neck + back.neck | 1 sa | 2.0 |

## BOM

Nylon-ripstop **shell** + downproof **lining** (both by marker length) +
**insulating fill** budgeted by quilted panel area (~120 gsm synthetic, ~m² of
front + back + sleeves) + one **closed-end separating zipper** + **cuff & hem
elastic** (exact mm) + thread. The zipper slider/pull is a **Yantra4D**
cartridge (`projects/zipper-notion`, linked via the manifest `notion` block),
never re-implemented here. Fabric card: `materials/nylon-ripstop-shell`.

```bash
python apps/api/services/engine/fc_runner.py projects/puffer-jacket/main.py puffer.svg '{}' svg
```

Official visualizer and configurator: Fashion Cabinet.

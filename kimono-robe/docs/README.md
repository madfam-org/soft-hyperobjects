# Kimono-style Robe — FC-100 rank #100

A **kimono-STYLE** wrap robe (`bata estilo kimono`): the common lounge /
dressing robe whose geometry is borrowed from the kimono. Back cut on fold,
two straight-centre-front panels, wide rectangular sleeves on a straight
dropped-shoulder armhole, one continuous front/collar band, and self ties.
Suggested fabric: `materials/popelina-algodon` (crisp cotton poplin).

## This is a kimono-STYLE robe, not a traditional kimono

Offered with respect for the source. This draft borrows the kimono's
**rectangular geometry** but is the everyday wrap robe, **not** a formal
traditional kimono. It deliberately omits:

- the **okumi** (front overlap panel) and its tuck,
- the layered **eri** collar / juban construction,
- the bolt-width (**tan**) cutting discipline that governs an authentic kimono,
- the seated-wear proportions and formal sleeve rules.

If you need an authentic kimono, this is not it — it is the robe the West
calls a "kimono robe."

## The signature: rectangular construction

Every piece is a **straight-edged rectangle** joined by **straight seams**.
The only curves are two shallow neck scoops. The teaching point is
**rectangular economy** — a whole robe nests from rectangles with almost no
fabric waste, and it closes by wrapping and tying (no hardware at all).

## Pieces

| Piece | Cut | Notes |
|-------|-----|-------|
| `back` | 1 on fold (CB) | rectangle; shallow back-neck scoop on the top edge |
| `front` | 2 mirror | rectangle; straight full-length centre-front edge (the band covers it); shallow front-neck scoop |
| `sleeve` | 2 mirror | wide rectangle; straight sleevehead (dropped shoulder) |
| `band` | 1 | one long rectangle — the continuous front/collar band; inner edge **solved** to the measured neckline run |
| `belt` | 1 | long self tie (the wrap belt) |
| `inner_tie` | 2 | short self anchor ties |

## The solved band

The band's inner (attach) edge length is **solved by bisection** so it equals
the measured neckline run =
`right-front centre-front edge + back-neck edge + left-front centre-front edge`
(both fronts are cut mirror, so two centre-front edges contribute). This is
the `collar-band` method — a band fitted to a measured neckline — applied to
the long continuous kimono band, and the band ↔ neckline seam is declared and
verified to **delta ≈ 0**.

## Construction order

1. Sew the two front panels to the back at the **shoulder** and **side** seams
   (straight seams; front and back panels are the same width so both balance).
2. Set each wide **sleeve** into the straight dropped-shoulder **armhole**
   (the sleevehead is a straight vertical matching the armhole), then close the
   **underarm** seam.
3. Attach the continuous **band** down the right front, around the back neck,
   and down the left front; the notches mark centre-back neck and the two
   shoulder-neck points.
4. Hem the sleeves and the bottom; make up the **belt** and **inner ties** and
   attach the inner tie / add a belt carrier as desired.

## v0 honesty notes (teaching-grade)

- Front and back panels are the **same width**, so the shoulder and side seams
  balance by construction; the wrap overlap comes from the two panels crossing
  over the band and from the wrap ease, not from a wider front panel.
- The **underarm** is a simple full seam in v0. A partially-open underarm (the
  authentic deep-sleeve *furi* opening) is a finishing option, not drafted here.
- The neck scoops are shallow gentle curves; everything else is straight.
- **No hardware** — the robe closes by wrapping and tying. Ties are cut from
  the shell fabric.

```bash
python apps/api/services/engine/fc_runner.py projects/kimono-robe/main.py kimono-robe.svg '{}' svg
```

Official visualizer and configurator: Fashion Cabinet.

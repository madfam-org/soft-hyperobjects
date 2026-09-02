# Changpao (長袍)

The Chinese men's long robe: straight, ankle-length, with a stand collar (**立領**),
closed along a curved diagonal (**大襟**, *dàjīn*) from the throat across the chest to
the right underarm, fastened with knotted cloth frogs (**盤扣**, *pánkòu*), and slit at
both sides for walking.

Part of the **Fashion Cabinet Commons** (FC-300, long-tail band — heritage — Chinese).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A panel-width draft keeps the logic of the garment — cloth as the unit, the sleeve cut
> in one, fit from where the straight seams fall — instead of translating the robe into
> a Western block with a diagonal edge added on top.

## Provenance

The changpao was **ordinary dress**, not a costume. It was the everyday and formal wear
of men across late-Qing and Republican China, worn plain for work and paired with the
short **馬褂** (*mǎguà*) riding jacket as the **長袍馬褂** formal combination. It is worn
still — at weddings, at New Year, on stage, and by people who simply prefer it — and it
is the direct ancestor of the Cantonese **長衫** (*chèuhngsāam*) and of the garments now
sold as **唐裝**.

It is a men's garment in this lineage; the woman's robe of the same period that shares
its collar and its dajin is the **旗袍** (*qípáo* / cheongsam), which is a different
draft and is not this cartridge.

This cartridge drafts an **everyday** changpao. It is an original draft made from the
garment's construction logic, not a copy of any particular workshop's pattern.

## Why it earns its rank

**The cloth is the unit, not the body.** Handloom silk and cotton ran roughly the width
of a seated weaver's reach, and the robe is built from panels of that width **used
whole**. There is no shaping cut into the panel; the fit comes from where the straight
seams fall. So `panel_width` is a real parameter here, and the body circuit is computed
**from** it — the chest measurement is checked *against* the cloth, never used to size
it:

```python
BODY_CIRCUIT = panel_width * 2 + DAJIN_X     # two panels + the dajin's wrap-past
CHEST_EASE   = BODY_CIRCUIT - chest_girth
```

| panel | chest | circuit | ease | sufficient? |
|---:|---:|---:|---:|:--|
| 480 mm | 1000 mm | 1108.8 mm | +108.8 mm | yes |
| 760 mm | 1000 mm | 1862.0 mm | +862.0 mm | yes (a very full robe) |
| 320 mm | 1400 mm | 773.3 mm | **−626.8 mm** | **no** |

That last row is the point. The draft reports `panel_sufficient: false` rather than
quietly inventing a wider loom, exactly as the `haori` cartridge reports
`bolt_sufficient` for the same reason in a different weaving tradition.

**The sleeve is cut in one with the body (連袖).** There is no armscye anywhere on this
robe. The shoulder line runs straight from the neck out to the wrist, and the underarm
is a **corner** — which is why the **插角** gusset exists, and why a right angle under
the arm is drafted rather than a curve. Setting a sleeve in here would be a different
garment wearing this one's name.

**The 大襟 is the garment.** The curved overlap carrying the closure is what makes a
changpao a changpao, and it is the thing an outside pattern gets wrong first.

## The seam that had to solve

**The dajin's curve is drafted once, measured once, and everything reads the
measurement.**

The panel underneath the overlap must carry an edge of *exactly* the dajin's length, or
the overlap does not lie flat and the whole front twists on the body. So the curve is a
single Bézier — biased outward near the neck and downward near the underarm, which is
the shape of a real dajin rather than a quarter-circle — and its length is measured off
the drawn edge. The body's `dajin-seat` marking is the **same curve**, so the two are
equal by construction rather than by two formulas hoping to agree.

The frogs then follow the **measured arc**, not the chord:

| case | dajin drop | curve | chord | curve − chord | frog pitch (arc) | (chord) |
|---|---:|---:|---:|---:|---:|---:|
| default | 300 | 248.3 | 245.1 | **3.2 mm** | 49.65 | 49.02 |
| `deep_dajin_formal` | 400 | 358.3 | 350.8 | **7.5 mm** | 51.18 | 50.12 |
| extreme | 480 | 513.1 | 482.8 | **30.3 mm** | 102.62 | 96.55 |

Spacing by chord bunches the pánkòu at the shoulder and gaps them at the underarm. It is
a small error that is *visible from across a room*, and it is the signature of a robe
drafted flat by someone who measured a straight line.

**The 立領 is cut to the measured neckline.** The collar runs both back quarters, the
left front quarter, and the dajin's own neck edge on the right — all four measured off
the drawn pieces. The naive estimate (`neck_girth + ease`) misses by **28.9 mm** at the
defaults, because the drafted neckline is four curves plus a front drop plus a
right-front run, not a circle.

Declared seams: `collar.neck_edge ↔ body.neck ×2 + front.neck + dajin.neck`,
`body.side ↔ front.side`, `body.sleeve_under ↔ front.sleeve_under`,
`body.shoulder ↔ front.shoulder`, `body.cuff ↔ front.cuff`, and both gusset diagonals.
The side and shoulder seams are declared **because** they should be equal by
construction — a shaped panel can never sneak into a robe whose whole logic is the
unshaped panel.

## The neckline is Chinese, not Western

A 立領 stands **on** the base of the neck. The Western `neck_girth / 6` formula is
drafted for a turndown collar that sits well *below* the neck base, and using it here
gives a 307 mm opening for a 400 mm neck — a robe that will not do up at the throat. So
the opening is `neck_girth + 26 mm` of wearing ease, divided into quarters, and the
collar is then cut to what those quarters actually measure.

## Clamping

Three derived dimensions carry explicit bounds, and each answers a real parameter
combination rather than a hypothetical:

- **The dajin's reach** must clear the neck opening on one side and stop short of the
  side seam on the other, or the overlap has no panel to lie on. A 320 mm panel with a
  520 mm neck leaves **no legal band at all** — the two bounds cross — so the draft
  splits the difference and reports `dajin_reach_clamped: true` rather than drawing an
  edge that crosses the neckline into geometry the kernel would CCW-normalize into a
  piece that verifies and cannot be cut.
- **The side slit** is capped at 62% of the body below the underarm. It is a walking
  slit; a slit reaching the armhole is an open side, which is a different garment.
- **The dajin drop** is bounded by the parameter range and checked against the robe
  length as a manifest constraint.

The cartridge was probed at the **minimum and maximum of all 14 parameters**, plus
all-min, all-max, cross extremes, and every `target_piece` at both defaults and all-max
— 71 cases, all `errors=0`, every declared seam ok, no degenerate bbox.

## Hardware

**Bridged.** The closures are **盤扣** — knotted cloth frogs, made from bias strip of
the robe's own fabric. There is no hard-goods fastener here at all; what the bridge
carries is the *former* — the Yantra4D `frog-closure` solid the knot is made over.

The manifest declares a `notion.hardware_ref` naming `yantra4d/frog-closure` with
**`linked: true`**. This was an honest `linked: false` co-create placeholder — the
FC-200 form for a solid not yet on the shelf — until the solid was built upstream and
vendored into the pinned snapshot; the claim was re-pointed on 2026-09-02 (PR #140)
and now resolves. The garment side was already wired with the two dimensions that
matter, and they are what the map drives: `span` ← `frog_width`, `knots` ←
`frog_count`. Both couple to this robe's own closure interface, which is what makes
the flange a driven flange rather than a coincidence.

`tail_w` and `tail_t` are the finding's own printed tail dimensions; no parameter of
this garment determines them, so they stay **unmapped** rather than invented.

**The frogs stay hand-knotted cloth**, which is what they are.

## Construction notes

Pieces: **body** (back half, cut 2, joined at centre back), **front** (left front panel,
cut 1), **dajin** (overlap, cut 2 — face and facing), **collar** (立領, cut 2),
**underarm** (插角 gusset, cut 2).

1. Join the two body halves at centre back. The panel is used whole; do not shape it.
2. Join body to front at the shoulder and down the side, **stopping at the slit head**.
   Finish the slit edges rather than sewing them.
3. Set the 插角 gussets into the underarm corners. Cut on the true bias if the cloth
   allows — the gusset is what lets the arm come down, and a right angle without one
   tears at the first reach.
4. Apply the dajin over the left front, matching its curve to the panel's marked seat.
   The robe crosses **right over left**.
5. Apply the collar, matching its centre-back and centre-front notches. Interline it:
   an unstiffened 立領 collapses at the throat.
6. Knot the pánkòu and attach them along the marked arc positions, plus one at the
   collar.
7. Hem deep — the allowance is generous so the robe can be let down; a long robe is
   expected to outlast one wearer's height.

Traditionally the whole garment is hand-sewn so it can be unpicked, washed as flat
panels, and re-sewn. `manta-cruda` shrinks 5% in the warp: **wash before cutting**, or
the finished robe is 66 mm shorter than drafted.

## What is deliberately excluded

**No 補子 rank badge, no dragon roundel, no clan or official insignia.** A 補子 is the
mark of an office and a 家紋-equivalent clan crest is the mark of a family; neither is
decoration a pattern generator should hand out. Silk brocade grounds, embroidery
traditions, and the 旗袍 women's draft all belong to their own crafts and their own
cartridges.

## Honest simplifications

- The sleeve is drafted with a straight lower edge and a straight cuff. Some changpao
  taper slightly toward the wrist; the `sleeve_opening` parameter covers the practical
  range but the taper is left to the maker.
- The dajin is drafted as a single Bézier. Regional and period variation in that curve
  is real and considerable — a Qing-era dajin runs higher and rounder than a 1930s one —
  and `dajin_drop` plus `dajin_reach` are offered as the two handles for it rather than
  a claim that one curve is canonical.
- The robe is drafted unlined. A winter changpao is lined or wadded (**棉袍**), which
  changes the ease budget; add it to `chest_girth` rather than to the panel.

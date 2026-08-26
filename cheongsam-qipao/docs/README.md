# Cheongsam (qipao)

The fitted women's Chinese dress — Cantonese **長衫** (*cheongsam*), Mandarin **旗袍**
(*qipao*) — that took its modern form in 1920s Shanghai: a body-skimming sheath with a stand
collar (**立領**), the curved **大襟** (*dàjīn*) diagonal opening from the throat across the
chest to the right underarm, hook-and-eye and knotted-frog closures along that curve, and
high side slits.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Chinese).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A fitted draft that solves the waist from the three girths and measures the 大襟 so the
> overlap lies flat — instead of a Western sheath with a mandarin collar and a printed
> diagonal added on top.

## Provenance

The cheongsam / qipao evolved from the looser **Manchu banner gown** (the 旗 *qí*, "banner")
of the Qing into a fitted, tailored women's dress in the treaty-port modernism of 1920s–30s
Shanghai, and it has been an icon of Chinese women's dress ever since — everyday, formal, and
on stage. Its companion is the men's **changpao** (drafted separately in the commons); the
two share the stand collar and the 大襟, but the changpao is a **panel** garment while the
qipao is **shaped** to the figure.

This cartridge drafts the fitted dress as an original block, not a copy of any particular
tailor's pattern, and draws **no** embroidery or roundel.

## Why it earns its rank

**The body is fitted, through the waist.** The waist is *solved* from the three girths — bust,
waist, hip — and the suppression is split between the side seam and a vertical dart:

```python
WAIST_SUPPRESSION = max(BUST_Q - WAIST_Q, 0)   # never a reversed dart
SIDE_TAKE = 0.45 * WAIST_SUPPRESSION
DART_TAKE = WAIST_SUPPRESSION - SIDE_TAKE
```

At the defaults that is 55.0 mm of suppression per panel (24.8 mm at the side, 30.3 mm in the
dart). A waist *wider* than the bust simply yields no dart — the clamp prevents a reversed
one, which is one of the extremes the draft is tested against.

**The 大襟 is drafted once and measured.** The curved overlap that carries the closure must
match the panel beneath it exactly, or the front twists. The curve is a single Bézier,
measured off the drawn edge (**172.1 mm** vs a straight chord of **162.1 mm** at the
defaults), and the panel's `dajin-seat` marking is the same curve. The **立領** stand collar is
then cut to the **measured** neckline — the left front, both back quarters, and the dajin's
own neck run — which is `collar_run_mm = 402.0`, off the naive `neck_girth + ease` estimate by
`collar_vs_neck_estimate_mm = 18.0`, because the drafted neckline is four curves plus the
dajin's run, not a circle. The **hook-and-eye** closures are spaced by arc length along the
measured curve and bridged to the Yantra4D `hook-and-eye` solid, whose `size_mm` is driven
from the garment's `closure_span`.

## What is deliberately out of scope

No dragon roundel, embroidery motif or clan mark is drafted. Those are the maker's cloth and
choice; this cartridge supplies the fitted body, the measured dajin, the collar and the
closure.

## Parameters

`bust_girth`, `waist_girth`, `hip_girth`, `qipao_length`, `neck_girth`, `collar_height`,
`shoulder_width`, `armhole_depth`, `bust_to_waist`, `dajin_drop`, `slit_height`, `bust_ease`,
`closure_span`, `closure_count`, `seam_allowance`, `hem_allowance`.

## Pieces

- **front** — fitted front, cut on the CF fold, waist dart + marked 大襟 seat.
- **dajin** — the 大襟 overlap panel (cut 2), its curved edge the measured curve.
- **back** — fitted back, cut on the CB fold, waist dart and high side slit.
- **collar** — the 立領 stand collar (cut 2), cut to the measured neckline.

## Hardware

Hook-and-eye closures along the dajin via the Yantra4D `hook-and-eye` cartridge (linked),
sized from the closure span and spaced along the measured curve. Knotted 盤扣 frogs are
traditional alongside; those remain hand-made cloth, not drafted here.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living tradition of the cheongsam; the cloth and its ornament
are the maker's.

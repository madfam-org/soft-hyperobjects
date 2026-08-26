# Hanbok magoja overjacket

The Korean overjacket (**마고자**, *magoja*) worn over the **jeogori**: a hip-length jacket,
**straight** down the centre front — not wrapped and tied like the jeogori — fastened with a
few buttons, with the soft one-piece sleeve carrying the gentle **배래** (*baerae*) curved
underarm, and short side vents.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Korean).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A draft that gives the magoja its *own* straight buttoned front and soft baerae sleeve —
> instead of borrowing the jeogori's wrap-and-tie, which is the very thing the magoja is not.

## Provenance

The **magoja** entered Korean dress in the late 19th century — its form derived from a Manchu
jacket brought back by the reformer Heungseon Daewongun — and became a standard warm outer
layer of the **hanbok** for both men and women, worn over the **jeogori** (the inner jacket,
drafted separately in the commons). Its distinguishing features are a **straight, buttoned**
centre front (the jeogori wraps and ties with **goreum**; the magoja does not), amber or
knotted buttons, and often a lightly padded, lined body for warmth.

This cartridge drafts the overjacket as an original construction draft, not a copy of any
particular workshop's pattern.

## Why it earns its rank

**The sleeve is cut in one, with the 배래 curve.** There is no set-in armscye. The sleeve runs
straight out from the shoulder, and the underarm is the soft **baerae** curve — a gentle dip
rather than a right angle or a Western scye. The seam that closes it (the sleeve underseam
continuing into the side seam) is declared and measured, so the front and back agree:

```python
pattern.declare_seam(("front", "baerae"), ("back", "baerae"), tol=1.0)
```

**The front is straight and buttoned, not wrapped.** This is the feature that separates the
magoja from the jeogori it covers. The front meets at centre front and **buttons** — no
goreum ties — with real buttons bridged to the Yantra4D `sew-through-button` solid, driven
from the garment's `button_ligne`. The **깃** (*git*) collar band is cut to the **measured**
neckline (both fronts + both back quarters), and the white **동정** (*dongjeong*) collar strip
is marked on top of it, applied in make-up.

## What is deliberately out of scope

No woven or embroidered motif is drawn. The cloth, the dye and any pattern are the maker's
and the family's.

## Parameters

`chest_girth`, `magoja_length`, `neck_girth`, `back_neck_width`, `sleeve_length`,
`sleeve_depth`, `cuff_opening`, `baerae_curve`, `git_width`, `wrap_ease`, `side_vent`,
`button_ligne`, `button_count`, `seam_allowance`, `hem_allowance`.

## Pieces

- **back** — the back, cut on the CB fold, one-piece sleeve with the 배래 curve.
- **front** — the front (cut 2), straight buttoned centre front, one-piece sleeve.
- **git** — the 깃 collar band (cut 2), cut to the measured neckline, 동정 strip marked.

## Hardware

Front buttons via the Yantra4D `sew-through-button` cartridge (linked), sized in lignes
(amber or shell traditional).

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living tradition of the hanbok; the cloth and its ornament are
the maker's.

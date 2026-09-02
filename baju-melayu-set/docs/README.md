# Baju Melayu set

The Malay men's outfit: a loose, long-sleeved shirt (the **baju**) with a raised stand collar
(the **cekak musang**, "civet's grip") and a short buttoned front placket, worn with matching
trousers (**seluar**) and the **samping** — a short cloth, often **songket**, wrapped over the
trousers at the waist and folded to hang in front.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Malay).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A draft that gives the baju melayu its raised cekak musang collar, its measured-armscye
> sleeve, and a samping whose fold is solved from the waist — not a collarless shirt with a
> sarong.

## Provenance

The **baju melayu** is the traditional men's dress of the Malay world — Malaysia, Brunei,
Singapore, southern Thailand and parts of Indonesia — worn to the mosque, at weddings, and
especially at **Hari Raya**. Its three components are the loose **baju** shirt, the matching
**seluar** trousers, and the **samping**: a short wrapped cloth (often the prestigious
gold-and-silver **songket**) folded over the trousers. The shirt's signature is the **cekak
musang**, a tall raised stand collar, though a turned-down **teluk belanga** collar is also
worn.

This cartridge drafts the baju shirt, its cekak musang collar, and the samping wrap as an
original construction draft, and draws no songket weave or embroidery.

## Why it earns its rank

**The cekak musang collar is cut to the measured neckline.** The raised stand is cut to the
**measured** neck run (both fronts + both back quarters), not to a neck girth, so it stands
cleanly at the throat — reported against the naive estimate as `collar_vs_neck_estimate_mm`.

**The sleeve is set in to the measured armscye, and the samping is solved from the waist.** The
sleeve cap is iterated until it equals the measured front + back armhole plus ease, so it hangs;
and the samping wrap is solved from the waist plus a front-fold overlap so the fold sits right:

```python
SAMPING_WRAP = waist_girth + waist_girth * 0.55   # once round plus the front-fold overlap
```

The front placket carries real **sew-through buttons**, bridged to the Yantra4D
`sew-through-button` solid and driven from `button_ligne`.

## What is deliberately out of scope

No songket weave, tekat embroidery, or state-specific/royal motif is drawn. Those are the
weaver's and the region's — the pride of Malay textile art.

## Parameters

`chest_girth`, `baju_length`, `neck_girth`, `shoulder_width`, `sleeve_length`, `armhole_depth`,
`wrist_girth`, `collar_height`, `placket_length`, `ease`, `waist_girth`, `samping_drop`,
`button_ligne`, `button_count`, `seam_allowance`, `hem_allowance`.

## Pieces

- **front** — baju front (cut 2), short buttoned placket.
- **back** — baju back, cut on the CB fold.
- **sleeve** — long sleeve (cut 2), cap measured to the armscye.
- **collar** — cekak musang stand collar (cut 2), cut to the measured neckline.
- **samping** — the samping wrap cloth, solved from the waist.

## Hardware

Front-placket buttons via the Yantra4D `sew-through-button` cartridge (linked), sized in
lignes.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living Malay dress tradition; the songket and tekat are the
weavers' and the artisans'.

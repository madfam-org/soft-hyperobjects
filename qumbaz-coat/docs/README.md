# Qumbaz linen robe

The long men's coat-robe of the Levant (**قمباز**, also *kumbaz* / *qombaz*): ankle-length,
opening all the way down the centre front, crossed right-over-left and held with a long sash
and a row of small buttons, with long straight sleeves and side slits for walking and riding.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Levantine).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A wrap-front draft that gives each front a real overlap and runs the buttons up the crossing
> edge — not an edge-to-edge coat that loses the cross the qumbaz is built around.

## Provenance

The **qumbaz** is the long coat-robe worn by men across the Levant — Palestine, Syria, Jordan
and Lebanon — over a shirt, in washed linen for everyday wear or in the striped **atlas**
silk-cotton of Damascus for dress. It opens down the front, crosses right-over-left, and is
held by a long sash at the waist (and, in many regions, by a row of small ball or cloth
buttons and loops up the chest), with deep side slits for walking and riding. It is close kin
to the Ottoman **entari** and the various regional **kaftan** robes.

This cartridge drafts the qumbaz as an original construction draft, not a copy of any
particular tailor's pattern, and draws no woven-stripe colourway.

## Why it earns its rank

**The front wraps, and the overlap is real.** The qumbaz is not an edge-to-edge coat: each
front is drafted with an overlap **past** centre front (`front_overlap = 140 mm` at the
defaults), so the right front crosses and the left sits beneath it, and the buttons run up the
crossing edge. The overlap is a real parameter, so the two fronts always meet with a genuine
cross rather than gaping.

**The stand collar is cut to the measured neckline.** The low stand is cut to the **measured**
neck run — both fronts *including their overlaps* plus both back quarters — which is
`collar_run_mm = 771.2` at the defaults, off the naive `neck_girth + ease` estimate by
`collar_vs_neck_estimate_mm = 333.2`. The set-in sleeve cap is likewise solved to the measured
armscye (540.2 mm) plus a light shoulder gather (cap drawn 556.2 mm).

## What is deliberately out of scope

No woven-stripe (**atlas**) colourway or regional trim is drawn. The cloth is the maker's — the
striped silks of Damascus and the linens of Palestine are the weavers'.

## Parameters

`chest_girth`, `robe_length`, `neck_girth`, `shoulder_width`, `sleeve_length`, `sleeve_width`,
`armhole_depth`, `collar_height`, `front_overlap`, `side_slit`, `ease`, `button_ligne`,
`button_count`, `seam_allowance`, `hem_allowance`.

## Pieces

- **front** — one front (cut 2), with the centre-front overlap and the button run.
- **back** — the back, cut on the CB fold, with side slits.
- **sleeve** — the long straight sleeve (cut 2), cap measured to the armscye.
- **collar** — the low stand collar (cut 2), cut to the measured neckline.

## Hardware

Front-crossing-edge buttons via the Yantra4D `sew-through-button` cartridge (linked), sized in
lignes. The robe is also held by the sash.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living dress traditions of the Levant; the striped silks and
linens are the weavers'.

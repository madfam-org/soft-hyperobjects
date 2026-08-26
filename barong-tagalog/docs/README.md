# Barong Tagalog

The Philippine formal shirt: a sheer, untucked, straight-cut shirt of **piña**
(pineapple-leaf fibre) or **jusi** (banana / abacá-silk), worn open at the hem over a plain
undershirt (**camisa de chino**), with an embroidered chest panel (the **pechera**), a front
button placket, a band collar, long sleeves with cuffs, and side slits.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Philippines).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A shirt draft that hangs the sleeve on a *measured* armscye and marks the pechera as an
> embroidery field the maker fills — instead of a plain shirt with a diagonal panel of print
> stitched on top.

## Provenance

The **barong tagalog** ("Tagalog dress") is the national formal wear of Filipino men. Its
sheer construction — worn untucked over a plain undershirt, unlined and diaphanous — is
often traced to the Spanish colonial era, and the garment has since become the standard
formal dress for weddings, state occasions and office wear (in its lighter **polo barong**
form). It is made in **piña** (hand-loomed pineapple-leaf fibre), **jusi**, or **piña-seda**,
and its defining ornament is the **pechera** — the worked chest panel — carrying **calado**
(drawn-thread openwork), **sombrado** (shadow work) and hand embroidery.

This cartridge drafts the shirt's construction geometry as an original draft, not a copy of
any particular tailor's pattern, and it draws **no** embroidery.

## Why it earns its rank

**The sleeve cap is cut to the measured armscye.** A set-in sleeve hangs cleanly only if the
cap seam equals the armhole it sews into. The front and back armholes are drafted and
measured, and the cap width is **iterated** until the drawn cap curve's length equals the
armscye plus a little ease:

```python
ARMSCYE    = front_armhole.length() + back_armhole.length()   # 515.2 mm at defaults
CAP_TARGET = ARMSCYE + 12                                       # a shirt's small cap ease
# cap span iterated until the drawn cap curve length == CAP_TARGET → 527.2 mm
```

| front scye | back scye | armscye | cap target | cap drawn |
|---:|---:|---:|---:|---:|
| 258.0 mm | 257.2 mm | 515.2 mm | 527.2 mm | 527.2 mm |

The declared seam `sleeve.cap ↔ front.armhole + back.armhole` (ease 12) proves the cap is
solved to the armhole rather than recomputed from a formula and hoped to agree. The band
collar is likewise cut to the **measured** neckline (`collar_run_mm = 520.9`).

**The finish is the garment.** The barong is sheer and untucked, so its character lives in
the placket, the band collar and the pechera. The **pechera is a marked field**, not drawn
decoration — the openwork and embroidery that fill it are the embroiderer's. The front
placket carries real **sew-through buttons** (mother-of-pearl traditional), bridged to the
Yantra4D `sew-through-button` solid and driven from the garment's own `button_ligne`.

## What is deliberately out of scope

No calado, sombrado or hand-embroidery pattern is drawn. The pechera's ornament belongs to
the embroiderers who make it; this cartridge supplies the shirt and marks where the worked
field sits.

## Parameters

`chest_girth`, `shirt_length`, `neck_girth`, `shoulder_width`, `sleeve_length`,
`armhole_depth`, `wrist_girth`, `cuff_height`, `collar_height`, `pechera_width`, `side_slit`,
`ease`, `button_ligne`, `button_count`, `seam_allowance`, `hem_allowance`.

## Pieces

- **front** — shirt front (cut 2), with the button placket and pechera field.
- **back** — shirt back, cut on the CB fold, with a shallow yoke line marked.
- **sleeve** — long sleeve (cut 2), cap solved to the measured armscye.
- **cuff** — sleeve cuff (cut 2).
- **collar** — band collar (cut 2), cut to the measured neckline.

## Hardware

Front-placket buttons via the Yantra4D `sew-through-button` cartridge (linked), sized in
lignes and coupled to the garment's placket dimension.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living craft of the Philippine barong; the piña weaving and the
embroidery are the weavers' and the embroiderers'.

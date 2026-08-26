# Salwar kameez set

The two-piece everyday and formal dress of Punjab and much of South Asia: the **kameez** (a
long straight tunic with side slits) over the **salwar** (a loose, pleated trouser drawn in at
the waist and gathered narrow at the ankle), worn with a **dupatta** scarf (a separate
garment, not drafted here).

Part of the **Fashion Cabinet Commons** (FC-500, heritage — South Asian).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A salwar drafted as it actually is — gathered at both ends, with a diamond crotch gusset —
> not a Western trouser with a curved crotch stitched under a tunic.

## Provenance

The **salwar kameez** (also **shalwar kameez**) is the everyday and formal dress of Punjab and
much of South Asia — Pakistan, northern India, Afghanistan, Bangladesh and the diaspora — worn
by women and men. The **kameez** is a long straight tunic with **chaak** side slits; the
**salwar** is a loose, full trouser gathered in at the waist by a drawstring (**naala**) and
tapering to a narrow ankle. A **dupatta** scarf completes the ensemble.

This cartridge drafts the kameez and salwar together as a set, and draws no embroidery,
**phulkari** or print.

## Why it earns its rank

**The salwar is panels and a gusset, gathered at both ends.** The leg is a wide rectangle,
gathered in at the waist and at the ankle — not cut to the body's crotch curve. The waist and
ankle fullness are fractions of the flat leg width, gathered in, and both ratios are reported.
The generous crotch is a **diamond gusset** (the **miyani** / **nala**), declared
square-on-point so it stays a symmetric diamond rather than a lopsided wedge:

```python
pattern.declare_seam(("gusset", "leg_r_lower"), ("gusset", "leg_l_lower"), tol=0.5)
pattern.declare_seam(("gusset", "leg_r_upper"), ("gusset", "leg_l_upper"), tol=0.5)
```

This is the kernel's differential-rise trouser trap avoided directly: one symmetric gusset with
equal-length mating edges, rather than two legs with a mismatched crotch.

**The kameez is a straight tunic with side slits and a faced neck.** Front and back are cut on
the fold; the side seams and grown-on short sleeves are declared equal.

## What is deliberately out of scope

No embroidery, phulkari, or print motif is drawn. The dupatta is a separate garment. The cloth
and its ornament are the maker's.

## Parameters

`chest_girth`, `kameez_length`, `neck_girth`, `neck_v_depth`, `shoulder_width`, `side_slit`,
`body_ease`, `hip_girth`, `salwar_length`, `ankle_girth`, `gusset_size`, `seam_allowance`,
`hem_allowance`.

## Pieces

- **kameez_f** — kameez front, cut on the fold, side slit, faced V-neck.
- **kameez_b** — kameez back, cut on the fold, side slit.
- **salwar** — one salwar leg (cut 2), full waist tapering to the narrow ankle.
- **gusset** — the diamond crotch gusset (miyani / nala).

## Fabric

Cotton voile or lawn; the salwar draws with a cord, and the kameez pulls over the head.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living dress traditions of South Asia; the embroidery and prints
are the makers' and the communities'.

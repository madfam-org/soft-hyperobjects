# Shweshwe pinafore dress

A pinafore dress in **shweshwe** printed cotton: a sleeveless bib-front shift with a fitted
bodice, a gathered skirt, faced neck and armholes, and a button closure down the centre
back — the everyday and Sunday form of the Southern African shweshwe frock.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Southern Africa: Sotho, Xhosa,
Tswana). Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A parametric bodice-and-skirt draft that balances the waist seam by construction, faces
> the sleeveless armhole honestly, and sizes the back closure to real buttons — while the
> shweshwe print, the identity of the cloth, is left entirely to the fabric.

## Provenance

**Shweshwe** (also **seshoeshoe** / **isishweshwe**) is a discharge-printed cotton with a
distinctive small-scale geometric or floral print, produced by acid-discharge on an indigo,
chocolate or red ground. Once imported to the Cape, it has been manufactured in South Africa
by **Da Gama Textiles** in the Eastern Cape (the "Three Cats" / "Toto" trademarks) since the
mid-20th century, and it is woven into the everyday and ceremonial dress of Sotho, Xhosa,
Tswana and other Southern African peoples — the Sotho **seshoeshoe** dress, the makoti's
wedding attire, and the ubiquitous pinafore.

The fabric arrives stiff with a starch finish and is traditionally soaked and ironed before
cutting. This cartridge drafts the **pinafore dress** — a sleeveless bib bodice over a
gathered skirt, faced and back-buttoning — as an original construction draft, not a copy of
any particular dressmaker's pattern.

## Why it earns its rank

**The waist seam must balance.** A gathered skirt joined to a fitted bodice only works if
the two waist edges match once the skirt is gathered. Rather than draft the skirt to a free
width and hope, the draft **solves** the skirt waist from the bodice waist times the gather
ratio:

```python
BODICE_WAIST_Q = waist_girth / 4
SKIRT_WAIST_Q  = BODICE_WAIST_Q * gather_ratio
```

| waist girth | ratio | bodice waist ¼ | skirt waist ¼ | gather take-up |
|---:|---:|---:|---:|---:|
| 740 mm | 1.9 | 185.0 mm | 351.5 mm | 166.5 mm |
| 600 mm | 1.3 | 150.0 mm | 195.0 mm | 45.0 mm |
| 1080 mm | 2.6 | 270.0 mm | 702.0 mm | 432.0 mm |

The waist seam is declared and verified, so the balance is a proven fact rather than a hope.

**The pinafore is sleeveless, and the back opens.** The armscye is a finished, faced edge —
not a mount for a sleeve — clamped to stay above the waist seam. The neck point is clamped
inboard of the shoulder tip so the bib can never invert. The centre back is split to a
button placket sized to the bodice length, closed with real **sew-through buttons**
(measured in lignes) — bridged to the Yantra4D `sew-through-button` solid, whose `button_ligne`
dimension is driven from the garment's own `button_ligne` parameter so the same size flows to
both the garment's placket and the button.

## What is deliberately out of scope

No specific shweshwe print motif is drawn. The print — the identity of the cloth — belongs
to its makers and printers; this cartridge supplies the dress geometry, and the fabric
supplies the pattern.

## Parameters

`bust_girth`, `waist_girth`, `bodice_length`, `skirt_length`, `gather_ratio`, `neck_width`,
`neck_drop`, `armhole_drop`, `shoulder_width`, `button_ligne`, `button_count`,
`seam_allowance`, `hem_allowance`.

## Pieces

- **front** — the pinafore front (bib bodice + gathered-skirt front), cut on the CF fold.
- **back** — the pinafore back half (cut 2), with the centre-back button placket.
- **facing** — the neck + armhole facing.

## Hardware

Back-closure buttons via the Yantra4D `sew-through-button` cartridge (linked), sized in
lignes and coupled to the garment's placket dimension.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living dress traditions of Southern Africa; the shweshwe print
and its making are the fabric-makers' and the wearers'.

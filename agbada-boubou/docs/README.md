# Agbada (grand boubou)

The West African grand gown: an enormous width of cloth folded once at the shoulder, with
an opening cut for the head, worn as the widest layer over a long-sleeved tunic and
drawstring trousers — the Yoruba **agbада** over the **bùbá** and **ṣòkòtò**, the
Senegambian **grand boubou** (Wolof **mbubb**) over the caftan and the **tubay**.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — West African).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A width-and-fold draft keeps the logic of the gown — the cloth as the unit, no shoulder
> seam, the arm reaching out through open sides, the neck faced rather than collared —
> instead of translating the boubou into a caftan with sleeves set into an armscye.

## Provenance

The grand boubou is one of the most widespread garments of West Africa and the Sahel. In
Yorùbá dress it is the **agbada**, the flowing outer gown of a three-piece outfit worn with
the **bùbá** (tunic) and **ṣòkòtò** (trousers); across Senegal, the Gambia, Mali and among
Wolof, Mandinka, Fula and Hausa communities it is the **grand boubou** / **mbubb**, worn
over a caftan and the wide **tubay** trousers. It is everyday and ceremonial dress at once —
plainer cotton for daily wear, richly embroidered damask (**bazin riche**) for weddings,
naming ceremonies and religious festivals — and it travels with its wearers throughout the
diaspora.

The garment's defining feature is its scale: it is cut from a single very wide width of
cloth, folded at the shoulder, so that the "sleeves" are simply the sides of the rectangle
falling to and past the fingertips. The worked zones are the **neck yoke** — a deep, faced
opening ringed with hand or machine embroidery — and a large **chest pocket**. This
cartridge drafts the gown's construction geometry. It is an original draft made from the
garment's construction logic, not a copy of any particular workshop's pattern.

## Why it earns its rank

**The garment is a width, folded.** There is no shoulder seam and no armscye. The cloth is
folded along the top edge (the shoulder line), the head-hole is cut *on that fold*, and the
spread of the cloth is a real parameter:

```python
BOLT_SUFFICIENT = BOLT_WIDTH >= wing_span + seam_allowance
```

| wing span | bolt | wing needed | sufficient? |
|---:|---:|---:|:--|
| 1150 mm | 1400 mm | 1162 mm | yes |
| 800 mm | 1400 mm | 812 mm | yes (a modest gown) |
| 1500 mm | 1400 mm | 1512 mm | **no** |

That last row is the point. When the wing exceeds the bolt the draft reports
`bolt_sufficient: false` rather than quietly inventing a wider cloth — exactly as `changpao`
reports `panel_sufficient` and `haori` reports `bolt_sufficient` for the same reason in
different weaving traditions. The arm reaches out through the **open side** above the closed
side seam; the side is sewn only up to `side_seam`, which is capped below the neck depth so
the arm-gap always remains.

**The opening is faced, not collared.** The boubou has no collar. Its neck is a wide, deep
opening — round, or the squared Yoruba form — bound with the worked yoke. The facing is cut
to the **measured** neckline, not to a neck girth, because a folded-cloth neckline is two
curves plus a deep front drop, not a circle. At the defaults the measured head-hole runs
**1175.5 mm** while `neck_girth + 40` would estimate only **440 mm** — a gap of
`facing_vs_neck_estimate_mm = 735.5 mm`, reported so the difference between the drape's real
opening and a fitted collar's circle is a visible fact.

## The seam that had to solve

**The facing's inner edge is the gown's measured front neck run.** The overlap panel of the
worked yoke must carry an edge of *exactly* the neckline's length on both sides of the fold,
or the facing will not turn cleanly and the embroidered field ripples at the throat — the
first thing an outside pattern gets wrong. So the neck curve is a single Bézier, drafted
once on the gown and measured off the drawn edge; the facing's inner edge is cut to that
same run. The declared seam `facing.neck_inner ↔ gown.neck + gown.neck` proves the two are
equal by construction.

## What is deliberately out of scope

No specific embroidery motif, no named **bazin** damask pattern, and no tribal or regional
mark is drafted here. The worked yoke and the cloth's pattern are the **maker's** — this
cartridge supplies the gown's geometry and the faced opening, and the embroidery belongs to
the embroiderer.

## Parameters

`wing_span`, `gown_length`, `chest_girth`, `neck_girth`, `neck_front_drop`, `neck_width`,
`facing_depth`, `pocket_width`, `pocket_drop`, `side_seam`, `seam_allowance`,
`hem_allowance`. Made to measure: the wearer's chest is checked (never used to size the
drape) and the gown length and wing span size the cloth.

## Pieces

- **gown** — the whole robe, cut 1 on the shoulder fold (mirror), head-hole on the fold.
- **facing** — the neck facing / worked yoke, cut to the measured neckline.
- **pocket** — the large chest patch pocket, placed on the measured chest field.

## Fabric

Plain or embroidered cotton, damask (**bazin riche**), or **wax-print** for the grand form.
The gown is closure-free — pulled over the head.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living traditions of West Africa and the Sahel; the cloth, the
embroidery and the meaning are the maker's and the community's.

# Guayabera (de alforzas)

The pleated men's dress shirt of the Caribbean and the Mexican Gulf — worn untucked in light
linen or cotton, and defined by its two vertical bands of fine pleats (**alforzas**) down each
front and the back, its four patch pockets, and its side vents.

Part of the **Fashion Cabinet Commons** (FC-400, lane 10 — heritage). Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabinet.app).

> The one detail that defines a guayabera is the one a naive draft gets wrong: the alforzas.
> Pleats consume cloth, so this cartridge solves the take-up into the cut width rather than
> "adding pleats" to a chest-sized panel.

## Provenance

The guayabera is a living regional dress garment of the Spanish-speaking Caribbean and the
Mexican Gulf coast, with a **contested but well-documented** Cuban/Mexican origin. It is worn
untucked, in light linen or cotton, for everyday and formal wear alike.

This cartridge drafts an **everyday four-pocket alforza guayabera**. It is not a ceremonial or
badge-bearing variant, and it invents no motif — the geometry is the shirt's own construction
logic, not a copy of any workshop's block.

## Why it earns its rank

**The alforzas are pleats, and pleats eat cloth.** Each front and the back carry two vertical
bands of narrow pleats. A pleat of fold depth `d` consumes `2·d` of cloth, so a panel with `N`
pleats per band and two bands must be cut **wider** than its finished width by `4·N·d`. The
commonest error is drafting the panel to the finished chest and then "adding pleats," which
runs short or shifts the pockets. Here the take-up is **solved** and added to the cut width, so
the finished chest is what the wearer measured while the pleats sit on cloth that still fits.

**The pockets and buttons sit on the alforza grid.** Two chest and two lower patch pockets,
each aligned to a pleat band and closed with a button. The buttons are the Yantra4D
`sew-through-button`, and `button_ligne` drives both the drafted buttonhole spacing and the
printed button so placket, pockets and buttons agree.

## Construction notes

Pieces: **front** (cut 2, alforza take-up + placket), **back** (cut 1 on fold, alforza
take-up), **sleeve** (cut 2, cap solved to the armhole), **collar** (band, cut 1), **pocket**
(cut 4).

1. Press and topstitch the alforza folds down their length on each front and the back before
   assembling — they are pressed knife pleats stitched close to the fold.
2. Join fronts to back at the shoulders and side seams, leaving the side vents open at the hem.
3. Set in the sleeves (cap solved to the armhole ring) and apply the collar band.
4. Make the four patch pockets (each with its own centre pleat) and set them on the pleat grid.
5. Work the placket buttonholes at the `button_ligne` spacing and sew the buttons.

## Hardware

The buttons are **Yantra4D solids** (`notion.hardware_ref → sew-through-button`, linked). The
map drives `button_ligne → button_ligne`, a 4-hole button, `hole_spacing` from the ligne, and
`hole_dia = 1.8 mm`.

## Made to measure

Drafted to **chest** and **waist** girths plus **shirt** and **sleeve** lengths. Every slider
extreme — pleat count and depth, ease, button size, sleeve length — renders watertight, and the
pleat take-up is reported in the metadata.

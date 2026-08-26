# High-Waist Shaping Brief

A high-waist compression brief (**faja calzón**): a front control panel and back panel cut at a **measured, graduated** negative ease — firmer at the waist, gentler at the hip — under a folded high waistband, with a **gusset that opens** on a Yantra4D `hook-and-eye` so the brief can be worn without full removal. Made to measure to waist and hip girths. FC-500 lane 7 (intimates & loungewear III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 7 — intimates & loungewear III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Shaping briefs are sold in a handful of sizes with a fixed compression the wearer cannot see or choose. This cartridge makes the squeeze a graduated, measured negative ease the panels are cut to, and closes the gusset on a printable hook-and-eye that can be reprinted rather than condemning the garment when it fails.

## Graduated compression is a number

Each panel is cut to its body girth times `(1 − compression)` at each level:

| Level | Cut width | Rule |
| :-- | :-- | :-- |
| Waist | `waist_girth · (1 − waist_compression)` | firmest |
| Hip | `hip_girth · (1 − hip_compression)` | gentler |

`waist_compression` is **clamped never gentler than `hip_compression`** (and an error-severity constraint mirrors it), so the squeeze is always graduated the right way.

## The gusset handshake

The gusset closes on the Yantra4D [`hook-and-eye`](https://yantra4d.com) tape. `gusset_width` drives the drafted placket **and** the hook column count (`round(gusset_width / hook_pitch)`), and `hook_pitch` drives the hardware's `size_mm` (its `sew_plate` flange) **and** the garment's own `gusset_closure` interface — so the placket the hooks sew to is exactly as wide as the tape.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front` | 1 on fold | front control panel |
| `back` | 1 on fold | back panel (higher CB rise) |
| `gusset` | 2 | gusset with the hook-and-eye placket |
| `waistband` | 1 folded | high waistband |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Una faja calzón de talle alto con compresión graduada y medida — más firme en la cintura, más suave en la cadera — bajo una pretina alta, con una entrepierna que abre con un broche `hook-and-eye`. Hecha a medida a cintura y cadera. Carril 7 de FC-500.

## Français
Une culotte gainante taille haute à compression graduée et mesurée — plus ferme à la taille, plus douce à la hanche — sous une ceinture haute, avec un gousset qui s'ouvre sur une agrafe `hook-and-eye`. Faite sur mesure aux tours de taille et de hanches. Couloir 7 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

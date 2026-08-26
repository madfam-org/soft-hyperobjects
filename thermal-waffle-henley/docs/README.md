# Waffle Thermal Henley

A long-sleeve waffle-knit thermal with a **henley placket**: a fitted knit body, set-in long sleeves, a ribbed neckband, and a partial button placket down the centre front closing on a column of Yantra4D `sew-through-button`. Made to measure to chest/bust, waist, arm length, bicep and neck. FC-500 lane 7 (intimates & loungewear III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 7 — intimates & loungewear III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A thermal henley is a base-layer everyone owns, sold in a grid that fits the torso or the arm but rarely both. This cartridge fits the body to a real chest and arm, then derives the button column from the drafted placket rather than the other way round, so the buttons sit where the opening actually is.

## The button handshake

The placket buttons are the Yantra4D solid [`sew-through-button`](https://yantra4d.com). `button_ligne` drives **both** the drafted button seats **and** the hardware's `sew_face` flange, and it drives the garment's own `placket` interface. `button_count = placket_length // button_pitch` — the column is derived from the opening.

## The cap solve

The sleeve cap is solved to **exactly** the measured armscye run (front + back) by bisecting the cap height, so the cap and the armhole balance at every extreme. The bicep chord is clamped below the armscye run, so a large bicep on a small chest can never force a cap the armhole cannot take.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `back` | 1 on fold | back body |
| `front` | 2 mirror | front body (CF placket opening) |
| `sleeve` | 2 mirror | set-in long sleeve (cap solved to armscye) |
| `placket` | 2 | button placket (overlap + underlap) |
| `neckband` | 1 | ribbed neckband (cut to the solved neck run) |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Una henley térmica de manga larga en nido de abeja con tapeta: cuerpo ajustado de punto, mangas largas montadas, cuello acanalado y una tapeta parcial al centro que cierra con una columna de botones `sew-through-button`. Hecha a medida a pecho, cintura, brazo, bíceps y cuello. Carril 7 de FC-500.

## Français
Un henley thermique à manches longues en nid d'abeille avec patte : corps ajusté en maille, manches longues montées, encolure côtelée et une patte partielle au milieu se fermant sur une colonne de boutons `sew-through-button`. Fait sur mesure à la poitrine, à la taille, au bras, au biceps et au cou. Couloir 7 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

# Pantomime Dame Gown

The panto **dame** gown: the deliberately outsize, comic gown of the British pantomime dame — a padded bust shelf, an enormous gathered skirt on a bumroll, giant puff sleeves, and a fast centre-back Yantra4D `hook-and-eye` because the dame changes costume many times a show. Made to measure to chest, waist and lengths. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> British pantomime is a mass-participation theatre form — every town has one at Christmas, most staffed by volunteers — and the dame's gown is the show's visual centrepiece, normally cobbled together at ruinous effort or hired at ruinous cost. Encoding it as a parametric object with one exaggeration dial lowers the cost of a costume that keeps a genuinely popular tradition on its feet.

## Provenance

The pantomime dame is a British theatrical tradition (a man in comic drag as a grotesque older woman) dating to the Victorian music hall. The costume is deliberately outsize and changes many times a show — so it wants a fast closure.

## The exaggeration solve

The comedy is in the **ratio**, not the raw size, so a single `exaggeration` factor scales the bust shelf, the skirt fullness, and the sleeve puff together — over a bodice still cut to the performer's real chest, so it fits. The skirt gather is declared as gathered ease so the enormous fullness is proven arithmetic.

## The closure handshake

The centre back closes on the Yantra4D [`hook-and-eye`](https://yantra4d.com); `closure_rows` drives the hook columns and `bodice_length` drives the drafted placket and the `cb_closure` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `bodice_front` | 1 on fold | padded bust bodice |
| `bodice_back` | 2 mirror | back (CB hook) |
| `skirt` | 1 | very full gathered skirt |
| `sleeve` | 2 mirror | giant puff sleeve |
| `placket` | 2 | fast CB hook-and-eye placket |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
El vestido de dama de pantomima: el vestido cómico enorme de la pantomima británica — busto acolchado, falda enorme, mangas de farol gigantes y un cierre rápido de broches. Hecho a medida a pecho, cintura y largos. Carril 9 de FC-500.

## Français
La robe de travesti de pantomime : la robe comique démesurée de la pantomime britannique — buste rembourré, jupe énorme, manches ballon géantes et une fermeture rapide à agrafes. Faite sur mesure à la poitrine, à la taille et aux longueurs. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

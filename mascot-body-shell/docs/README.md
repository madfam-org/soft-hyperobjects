# Mascot Body-Shell Suit

The body shell of a mascot costume: the oversized foam-lined torso the performer climbs into, cut enormous to clear a foam under-structure and give the exaggerated barrel shape a mascot needs, with a full-length centre-back Yantra4D `zipper` for entry and ventilation. Made to measure to chest and length plus the foam. FC-500 lane 9 (costume, dance & performance).

Part of the **Fashion Cabinet Commons** (FC-500, lane 9 — costume, dance & performance).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Mascot suits are a fixture of schools, sports teams, and community events, almost always bought as a sealed one-size product that fits badly and cooks the wearer alive. The two things that make a mascot suit wearable — foam clearance and airflow — are exactly what a bought suit gets wrong. This cartridge engineers both.

## Provenance

The mascot body shell descends from carnival and pageant giants and the modern sports/brand mascot: an oversized foam-and-plush torso worn over the performer's own body. Its defining problems are the foam clearance and the ventilation.

## The foam solve

A mascot shell is cut not to the body but to the **body plus the foam** (the foam wraps the whole circumference) plus a movement ease:

```
shell_circ = (body_girth + 2π·foam_thickness) + movement_ease
```

so the shell clears a foam layer of the stated thickness all the way round with room to move.

## The zip handshake

The centre back opens on the Yantra4D [`zipper`](https://yantra4d.com); `zip_length` drives the zipper tape **and** the drafted CB opening **and** the `cb_zip` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `shell_front` | 1 on fold | barrel-shaped front |
| `shell_back` | 2 mirror | back split for the CB zip |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
La carcasa de una botarga de mascota: el torso forrado de espuma sobredimensionado, cortado para librar una estructura de espuma, con un `zipper` completo al centro de la espalda para entrar y ventilar. Hecho a medida a pecho y largo más la espuma. Carril 9 de FC-500.

## Français
La coque d'un costume de mascotte : le torse doublé de mousse surdimensionné, coupé pour dégager une sous-structure de mousse, avec un `zipper` pleine longueur au milieu du dos pour entrer et ventiler. Fait sur mesure à la poitrine et à la longueur plus la mousse. Couloir 9 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

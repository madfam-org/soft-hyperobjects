# Nursing Sleep Bra

A **wire-free** nursing bra cut for sleep: an ultra-soft gathered **drop cup** on a wide, low-ease comfort band with a front crossover (no back closure), the cup detaching at a Yantra4D `bra-ring-slider` for one-handed feeding in the dark. Made to measure to underbust and bust girths. FC-500 lane 7 (intimates & loungewear III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 7 — intimates & loungewear III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> Night feeding is relentless, and the bra worn for it is either a day nursing bra with hooks that press into a side-lying ribcage or nothing at all. This cartridge makes a dedicated sleep bra to a real, changing postpartum body — the band eases *positive* so it never compresses, the cup is soft and gathered, and the one hard part (the drop clip) is a printable ring-slider.

## Distinct from `nursing-bra`

| | Sleep (this) | Day (`nursing-bra`) |
| :-- | :-- | :-- |
| Band ease | **positive** (never compresses) | negative (support) |
| Cup | soft, gathered, single piece | structured |
| Closure | pull-on front crossover | hooks |

## The gather + drop handshake

The cup mouth is drafted **longer** than the band's `cup_seat` by `cup_gather`; `declare_seam(..., ease=…)` proves the gather. The drop clip is the Yantra4D [`bra-ring-slider`](https://yantra4d.com): `strap_width` drives the drafted clip tab **and** the slider's `strap_face` flange **and** the garment's own `drop_clip` interface.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `cup` | 2 pairs | soft drop cup, gathered, with the ring-slider clip tab |
| `band` | 2 pairs | wide comfort band with front crossover |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un brasier de lactancia sin varillas para dormir: una copa suave fruncida con caída sobre una banda ancha de poca holgura con cruce delantero (sin cierre trasero), que se suelta en un anillo-corredera para amamantar con una mano. Hecho a medida al bajo busto y al busto. Carril 7 de FC-500.

## Français
Un soutien-gorge d'allaitement sans armatures pour la nuit : un bonnet souple froncé à bascule sur une bande large à faible aisance avec croisé devant, se détachant sur un anneau-coulisse pour nourrir d'une main. Fait sur mesure aux tours de dessous de poitrine et de poitrine. Couloir 7 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

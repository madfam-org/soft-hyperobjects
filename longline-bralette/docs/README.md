# Longline Soft Bralette

A wire-free bralette with a **longline** front frame: a soft gathered lace cup seated on a deep, stable panel over a negative-ease underband. Support is spread across the longline zone of ribcage rather than concentrated on a wire, and cup shape comes from a declared gather onto the frame rather than from moulding. Made to measure to underbust and bust girths. FC-500 lane 7 (intimates & loungewear III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 7 — intimates & loungewear III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> The wire-free bralette is where most people who cannot wear an underwire comfortably end up, and the market answers with three sizes of stretchy triangle that support nothing. This cartridge makes the wire-free case a measured garment instead: the longline frame is cut to a real ribcage at a declared negative ease, the soft cup's volume comes from the wearer's own bust surplus, and the only hardware is a printable ring-slider that can be reprinted when it cracks.

## The gather seam

There is no wire and no moulded cup. The cup is a soft lace triangle whose **mouth is drafted longer than the frame it sews to** — the difference is gathered in, and that gather is the cup's whole shaping:

| Quantity | Source |
| :-- | :-- |
| Frame seat | `frame.cup_seat` = `CUP_W` (drafted straight) |
| Cup mouth | `cup.mouth` = `CUP_W · (1 + cup_gather)` |
| Declared ease | `frame_seat · cup_gather` |

`declare_seam(cup.mouth, frame.cup_seat, ease=…)` proves the gather arithmetic — the cup is longer by exactly the ease, at every parameter extreme.

## The strap handshake

The adjustable straps thread through the Yantra4D solid [`bra-ring-slider`](https://yantra4d.com), referenced via `notion.hardware_ref`. `strap_width` drives **both** the drafted `strap_tab` on cup and wing **and** the hardware's `strap_face` flange interface, so the printed slider is exactly as wide as the tab it rides — a dimensionally coupled handshake, not a slug that merely resolves.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `cup` | 2 pairs | soft lace cup — gathered onto the frame |
| `frame` | 2 pairs | longline front frame (the stable support panel) |
| `band` | 2 pairs | negative-ease elastic underband |
| `back` | 2 pairs | back wing carrying the ring-slider strap |

Every sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un bralette largo sin varillas: una copa suave de encaje fruncida sobre un marco frontal profundo y estable, encima de una banda de holgura negativa. El soporte se reparte por la zona larga de las costillas en lugar de concentrarse en una varilla, y la forma de la copa surge de un fruncido declarado sobre el marco. Hecho a medida al contorno bajo el busto y al busto. Carril 7 de FC-500 (lencería y ropa de descanso III).

## Français
Une brassière longue sans armatures : un bonnet souple en dentelle froncé sur un cadre avant profond et stable, au-dessus d'une bande à aisance négative. Le maintien se répartit sur toute la zone longue des côtes plutôt que de se concentrer sur une armature, et la forme du bonnet vient d'un fronçage déclaré sur le cadre. Fait sur mesure aux tours de dessous de poitrine et de poitrine. Couloir 7 de FC-500 (lingerie et vêtements d'intérieur III).

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

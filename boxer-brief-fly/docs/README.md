# Fly-Front Boxer Brief

A knit boxer brief with a **real working fly**: a front cut in two halves joined by an overlapping placket that closes on a single Yantra4D `sew-through-button`, a shaped pouch, a seat-room back, an inner-leg gusset, and a folded knit waistband. Made to measure to waist, hip and thigh girths. FC-500 lane 7 (intimates & loungewear III).

Part of the **Fashion Cabinet Commons** (FC-500, lane 7 — intimates & loungewear III).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A working fly is a genuine convenience the knit-underwear market quietly deleted: almost every knit boxer brief sold today has a decorative flap sewn shut. This cartridge restores the function and makes the one part that wears out — the button — a printable commons object, sized to its placket by construction so it never sits proud or pulls through.

## The button handshake

The fly button is the Yantra4D solid [`sew-through-button`](https://yantra4d.com), referenced via `notion.hardware_ref`. `button_ligne` (button size, 1 ligne = 0.635 mm) drives **both** the drafted button seat on the overlap **and** the hardware's `sew_face` flange, and it drives the garment's own `fly_closure` interface. `fly_width` is **floored** at `button_dia + 14 mm`, so at every ligne the placket holds the button with margin — the classic failure (a button pulling through a placket cut too narrow) can't occur.

## Pieces

| Piece | Cut | Role |
| :-- | :-- | :-- |
| `front` | 2 mirror | fly halves (the two front panels) |
| `back` | 2 mirror | seat-room back |
| `gusset` | 1 | inner-leg gusset |
| `fly` | 2 | overlap + underlap placket (button + buttonhole) |
| `waistband` | 1 folded | knit waistband |

The fly placket is **topstitched** onto the CF region (a construction detail, not a balanced edge seam), so it is marked rather than declared as a seam. Every other sewn relationship is declared and verifies at defaults and at every parameter min/max.

## Español
Un bóxer de punto con bragueta funcional: un delantero en dos mitades unidas por una tapeta que traslapa y cierra con un solo botón `sew-through-button`, una bolsa conformada, una espalda con asiento y una entrepierna interior. Hecho a medida a cintura, cadera y muslo. Carril 7 de FC-500.

## Français
Un boxer en maille à braguette fonctionnelle : un devant en deux moitiés réunies par une patte qui chevauche et se ferme sur un seul bouton `sew-through-button`, une poche formée, un dos à assise et un gousset. Fait sur mesure aux tours de taille, de hanches et de cuisse. Couloir 7 de FC-500.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.

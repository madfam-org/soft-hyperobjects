# Formal Shirt — FC-100 #70 · Camisa formal

**EN** — A tuxedo / evening dress shirt. It is the plain dress shirt (rank #4)
taken up to black-tie: the same woven yoke-split body and chained collar solve,
plus the three things that make a shirt *formal* — a stiff **marcella bib**, a
**wing collar** option, and a **french cuff** option.

**ES** — Una camisa de esmoquin / de gala. Es la camisa de vestir (rango #4)
llevada a etiqueta: el mismo cuerpo de tejido plano con canesú y la misma
resolución en cadena del cuello, más las tres cosas que hacen *formal* a una
camisa — una **pechera de marcella** rígida, opción de **cuello de paloma** y
opción de **puño francés**.

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

---

## What it is / Qué es

A shirt drafted button → garment on the woven drop-shoulder block. The signature
of the formal shirt is the **bib (plastron)**: a distinct panel across the upper
front chest, cut in stiffer marcella / piqué, that reads as the dress front under
a dinner jacket. Studs (or covered buttons) close the front; a wing or turndown
collar sits on the stand; french or barrel cuffs finish the sleeves.

## The pieces / Las piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front | Delantero | 2, mirrored |
| `bib` | Bib (marcella / piqué) | Pechera | 2, mirrored (overlay) |
| `back` | Back | Espalda | 1 on fold |
| `yoke` | Yoke (doubled) | Canesú (doble) | 1 on fold |
| `sleeve` | Sleeve | Manga | 2, mirrored |
| `cuff` | Cuff | Puño | 2 |
| `stand` | Collar stand | Pie de cuello | 2 on fold |
| `fall` | Collar fall / wing | Cuello / paloma | 2 on fold |

Each piece renders on its own via the `target_piece` parameter
(`front|bib|back|yoke|sleeve|cuff|stand|fall|set`).

## The solves (why this is a hyperobject) / Las resoluciones

Every sewn seam is **declared and length-balanced** — the point of the commons.
The interesting ones:

- **Sleeve cap ↔ front + back armholes** — the cap curve half-width is found by
  bisection so the cap equals the summed armholes (ease 0).
- **Collar stand ↔ neckline** — the stand's neck edge is solved (bisection) to
  the measured half neckline (`front.stand_top + front.neck + yoke.neck`) plus a
  15 mm button/stud overlap.
- **Collar fall / wing ↔ stand top** — the fall's neck edge is solved to the
  stand's own *measured top edge*: a second solve **chained off the first**.
  Switching `collar_style` changes only the silhouette above that shared neck
  edge (a tall pointed turndown, or a short band with turned-back wing tabs), so
  the seam balances in either style.
- **Cuff ↔ pleated sleeve hem** — the sleeve hem is eased/pleated into the
  shorter cuff band; the seam is declared with the *measured* ease
  (`hem − cuff`), never a loosened tolerance.
- **Bib ↔ front (the overlay)** — the bib's `neck` and `shoulder` edges are the
  **same geometry** as the front's neckline and shoulder, so the bib is caught in
  the collar seam and the shoulder seam with **delta ≡ 0**. Its CF, side, and
  U-shaped lower edges are edge-stitched onto the front (an overlay, not a sewn
  seam). Pintuck fold lines on the bib face are `kind="trace"` marks — fold them
  for a pleated bib, or leave them for a flat marcella plastron.

## Options / Opciones

- **`collar_style`**: `wing` (formal, default) or `turndown`.
- **`cuff_style`**: `french` (double, cufflink; default) or `barrel` (single,
  button). French cuffs are cut at **2× band depth** so they fold back on
  themselves; the cufflink pierces all four layers (both ends are marked).

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- The **full back armhole is drafted on the back piece**; real shirts split the
  armhole across the back and the yoke. The yoke here carries the back neck and
  the shoulders only.
- **Straight hem** (v0). No shirttail curve yet.
- **Slit sleeve placket** — a marked slit + drill stop, not a separate
  tower-placket piece.
- The **bib is a flat overlay panel**. The pintucks are trace lines the maker
  folds; there is no separate boxed-pleat construction piece.
- Collar point / wing-tab shapes are simple; a couture pattern would true the
  points to the stand more finely.

## Hardware is federated / La herrería está federada

Per the Fashion Cabinet contract, hard goods are **Yantra4D cartridges**,
referenced in the BOM, never re-implemented here:

- **shirt studs / shank buttons** — the front closure (evening studs or covered
  buttons) and the collar-stand button;
- **cufflinks** — the french-cuff closure (a *pair*), or cuff buttons for the
  barrel cuff.

## BOM / Lista de materiales

Cotton poplin body (`popelina-algodon`), a marcella / piqué bib panel, fusible
interfacing (stand, fall/wing, cuffs, front stands, bib), shirt studs-or-buttons,
cufflinks-or-cuff-buttons, and thread. Fabric length is estimated from the total
piece area at the card width and a 65 % marker efficiency.

## Run it / Ejecútalo

```bash
python apps/api/services/engine/fc_runner.py projects/formal-shirt/main.py /tmp/formal-shirt.svg '{}' svg
# one piece, non-default options:
python apps/api/services/engine/fc_runner.py projects/formal-shirt/main.py /tmp/bib.svg '{"target_piece":"bib","collar_style":"turndown","cuff_style":"barrel"}' svg
```

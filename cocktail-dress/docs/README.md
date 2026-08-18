# Cocktail Dress / Vestido de coctel

**FC-100 rank #71.** A fitted, knee-length occasion dress — the family's first
garment built in **two stories joined at a true waist seam**: a princess-seamed
bodice over a lightly flared, hip-shaped skirt.

*Un vestido de coctel entallado a la rodilla — la primera prenda de la familia
construida en **dos cuerpos unidos por una costura de cintura real**: un corpiño
con costura princesa sobre una falda ligeramente acampanada moldeada en la
cadera.*

## What it is / Qué es

A tailored evening sheath. The bust is shaped the elegant, three-dimensional way
— by an **armhole princess seam** that splits the front into a center-front
panel (cut on the fold) and a side-front panel, rather than by a flat dart. The
back is cut in two with a **center-back invisible zipper** and a fisheye waist
dart per panel. The skirt continues the same waist quarter and the same CB
zipper line. Choose **strapless** (boned) or **strapped**; the whole thing is
**fully lined**.

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **Poplin stand-in.** The shell is drafted for `popelina-algodon` (cotton
  poplin) because that is the woven card the commons ships. A real cocktail
  dress is usually **crepe, satin, taffeta, or duchesse** — a drapier or crisper
  hand than poplin. The block is valid; swap the fabric for the occasion.
- **Lining is noted, not drafted as separate geometry.** The bodice and skirt
  are fully lined; in v0 the lining is cut from the **same shell pieces** and
  appears as a BOM line, not as its own pattern outline. A separately drafted
  lining (with the standard back-neck/pleat ease) is future work.
- **Boning as channel markings.** When boned, spiral-steel **boning channels**
  are drawn as `kind="trace"` guides down the CF princess, both side-front
  princess/side seams, and both back CB/side seams — a sewing guide, not a cut
  line. The steel and channel tape are a BOM notion (a Yantra4D cartridge).
- **Hardware is federated.** The invisible zipper and the spiral-steel boning
  are **Yantra4D hardware cartridges**, referenced in the BOM and the manifest
  `notion` / `hardware_ref` — never re-implemented in this drafting script.
- **Internal darts, not rotated.** The back fisheye waist dart stays an internal
  marking (teaching-grade); it is not rotated/closed into the panel outline.
- **Strapless is forced boned.** A strapless bodice cannot stay up unsupported,
  so selecting the strapless neckline turns boning on regardless of the checkbox.

## Pieces / Piezas

| id | piece | cut |
|----|-------|-----|
| `bodice_cf` | Bodice Center Front / Corpiño Centro Delantero | 1 on fold |
| `bodice_sf` | Bodice Side Front / Corpiño Lateral Delantero | 2 mirror |
| `bodice_back` | Bodice Back / Corpiño Espalda | 2 mirror (CB zip) |
| `skirt_front` | Skirt Front / Falda Delantero | 1 on fold |
| `skirt_back` | Skirt Back / Falda Espalda | 2 mirror (CB zip) |

The strapped neckline adds a shoulder-strap segment to `bodice_sf` (its `neck`
edge) and `bodice_back` (its `strap_top` edge); the two sew together at the
shoulder.

## How the seams are made to match / Cómo empatan las costuras

Every sewn relationship is declared and length-verified (fail-closed). The two
seams that would normally be fiddly are solved **by construction**, not by a
tolerance fudge:

- **Front princess** (`bodice_cf.princess ↔ bodice_sf.princess`): the princess
  curve is authored **once** and shared by both panels (one reversed), so the
  two edges are identical in length — like `suit-jacket`'s panel seams.
- **Waist seam** (`bodice_cf.waist + bodice_sf.waist ↔ skirt_front.waist`, and
  `bodice_back.waist ↔ skirt_back.waist`): the bodice side seam tapers from the
  bust quarter in to the **waist quarter**, and the skirt waist is drawn at that
  same waist quarter. Both waist edges are straight horizontals of equal total
  length, so the join solves at **delta ≈ 0**.
- **Bodice side seam** and **skirt side seam** reuse one shaped curve on both
  mated panels (same endpoints + bulge magnitude → equal length).

## Construction order / Orden de confección

1. Stitch the **front princess** seams (CF panel to each side-front panel);
   press toward center.
2. If boned, insert spiral steel into the **boning channels** (CF princess, SF
   princess + side, back CB + side).
3. Join **bodice side seams** (side-front to back).
4. Sew **back darts**; for the strapped version, join the **shoulder straps**.
5. Assemble the **skirt**: CB seam (leaving the zipper opening), then side seams.
6. Sew the **waist seam** joining bodice to skirt, matching the waist notches.
7. Insert the **center-back invisible zipper** (bodice top down across the waist,
   ending at the skirt zipper-stop notch).
8. Attach the **lining** at the neckline/armholes and zipper; hem the skirt shell
   and lining separately.

## Parameters / Parámetros

Girths are full-body millimetres. Fit: `bust_girth`, `waist_girth`, `hip_girth`,
`bodice_length`, `skirt_length`. Style: `neckline` (strapless | straps), `boned`,
`front_drop`, `skirt_flare`, `strap_width`. Notion: `zipper_length`. Advanced:
`waist_dart_intake`, `seam_allowance`, `hem_allowance`, `target_piece`.

---

Official visualizer and configurator: **Fashion Cabinet**.
Visualizador y configurador oficial: **Fashion Cabinet**.

# Crop Top — FC-100 rank #75 · Top corto

A cropped knit top whose hem sits **at or above the waist** — the defining
feature. Front and back are cut on fold with light knit ease, and the neck (plus
the armholes, or the sleeve hems) are finished with **binding strips** whose
lengths are computed from the measured openings × a rib-stretch ratio, not
guessed. A `style` switch turns the same block into a sleeveless tank crop or a
short-sleeve crop.

Un top de punto corto cuyo dobladillo queda **a la cintura o por encima** — la
característica que lo define. Delantero y trasero al doblez con holgura de punto
ligera; el escote (y las sisas, o los dobladillos de manga) se rematan con
**tiras de vivo** cuyas longitudes se calculan a partir de las aberturas medidas
× una proporción de estiramiento de rib, sin adivinar. Un selector `style`
convierte el mismo bloque en un top sin mangas o de manga corta.

Suggested fabric / Tela sugerida: `materials/jersey-algodon` (cotton/elastane
single knit — the stretch runs around the body).

## Pieces / Piezas

**Sleeveless (default):** front (cut 1 on fold), back (cut 1 on fold),
neck binding (cut 1 strip), armhole binding (cut 2 strips).

**Short sleeve:** front, back, neck binding, and a short sleeve (cut 2) whose
cap length is solved numerically to the front + back armholes.

## Construction order / Orden de construcción

1. Sew the shoulder seams (front ↔ back). / Cierra los hombros.
2. **Sleeveless:** sew side seams, then bind each armhole with a rib strip.
   **Short sleeve:** set each sleeve into its armhole (cap solved to the
   armhole), then sew side + underarm in one pass.
3. Bind the neckline with the neck rib strip, stretched to seat. / Remata el
   escote con la tira de rib, estirada al colocar.
4. Hem the cropped body (sleeve hems bound or turned). / Dobladilla el cuerpo
   corto (dobladillos de manga con vivo o volteados).

## Honest simplifications (teaching-grade)

- **Straight rib strips.** Real ribbing is cut narrower than its opening and
  eased in as it is stitched; here each binding strip is drafted straight at
  `opening × binding_ratio` (default 0.90) so the encoded rule is visible and
  the seam balances (delta ≈ 0). The exact cut lengths are emitted in the BOM.
- **Bound edges use zero seam allowance** — they are turned/bound, not
  seam-turned — matching the tank-top and t-shirt-crew knit references.
- **Identical front/back armholes** and a shared scoop curve keep the block
  simple; a graded production block would differentiate them slightly.
- **No hardware.** This is an all-knit, notion-free garment; the only notions
  are thread and a ballpoint/stretch needle.

The seam matching is real: every sewn relationship (shoulders, sides, neck
binding ↔ neckline, armhole binding ↔ armhole, or sleeve cap ↔ armholes) is a
declared seam verified to balance in length before the pattern can render.

## Run it / Ejecútalo

```bash
python apps/api/services/engine/fc_runner.py projects/crop-top/main.py crop.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/crop-top/main.py crop.svg '{"style": "short_sleeve"}' svg
```

Official visualizer and configurator: Fashion Cabinet ·
Visualizador y configurador oficial: Fashion Cabinet

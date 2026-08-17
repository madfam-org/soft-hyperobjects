# Shank Button (Yantra4D-bridged notion)

The federation pattern in miniature. The **solid button** is Yantra4D
territory (CadQuery → STL/3MF for printing); Fashion Cabinet owns the
**fashion semantics**:

- ligne sizing (1 ligne = 0.635 mm) → hardware diameter,
- placement math (count, placket length, end offsets),
- the 2D fabrication output: a printable **placement guide** strip whose
  `guide` edge pins to the placket center line, with a drill-cross (and
  optional button outline) at every position plus transfer notches.

`project.json → notion.hardware_ref` carries the bridge:
`{platform: "yantra4d", project_slug: "", linked: false, params_map: …}`.
`linked` stays `false` honestly until a shank-button cartridge exists in the
Yantra4D commons and the slug is verified — the contract is in place, the
link is not fabricated.

```bash
python apps/api/services/engine/fc_runner.py projects/shank-button/main.py guide.svg \
  '{"button_ligne": 18, "button_count": 7, "placket_length": 380}' svg
```

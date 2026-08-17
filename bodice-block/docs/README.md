# Bodice Block (Sloper)

A simplified metric flat block drafted from body measurements: front and back
bodice pieces with waist darts (as internal markings), matched side and
shoulder seams, fold-cut center lines, notches, and grainlines.

**Teaching-grade simplifications, on purpose** (v0.1): the waist stays
straight (darts are not rotated into the outline), shoulder ease is zero, and
the armscye is a single tuned curve. The contract is the point — measurements
in, seam-verified pieces out. Production-grade drafting refinements are
roadmap, not scope creep in a seed cartridge.

Parameters use ISO 8559-style measurement names (`bust_girth`,
`back_neck_to_waist`, …) so made-to-measure inputs stay portable across the
future commons.

```bash
python apps/api/services/engine/fc_runner.py projects/bodice-block/main.py out.svg '{}' svg
python apps/api/services/engine/fc_runner.py projects/bodice-block/main.py out.dxf '{"target_piece": "front"}' dxf
```

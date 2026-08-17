# Chinos — FC-100 rank #17

Tailored woven trouser on the **scrubs-pants block**: front/back legs (cut 2
each) with the front inseam bowed by a solved bisection to match the deeper
back fork, equal side seams by construction, a grown-on fly extension on the
upper front crotch edge (line down the extension, bezier rejoining the fork)
with a fly J-topstitch guide and fly-stop notch, a ~150 mm diagonal
slash-pocket opening from waist to side, pressed front/back creases, two back
waist darts (intake 12, length 90) with a back-pocket placement rectangle, a
two-piece waistband (left/right halves) whose bottom edge is verified against
front + back waists with the 40 mm closure overlap declared as seam ease, and
five 55 × 12 mm belt-loop strips. Fabrics: `materials/popelina-algodon`,
`materials/mezclilla-denim`.

v0 simplifications: the fly shield and French bearer are simplified out; the
fly zipper itself federates to a Yantra4D notion via the `fly` (zipper_tape)
interface rather than being drafted here.

```bash
python apps/api/services/engine/fc_runner.py projects/chinos/main.py chinos.svg '{}' svg
```

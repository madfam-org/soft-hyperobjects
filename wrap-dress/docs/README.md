# Wrap Dress — FC-100 #25

The shift-dress body opened into a true wrap. One front piece cuts 2 mirrored:
its center edge extends `wrap_extension` (default 240) past CF at the hem and
runs as a single straight diagonal up to the shoulder-neck point, so the
surplice `neck` edge IS the wrap edge — the CF crossing is notched at its
computed arc fraction and the mirrored pair overlaps below it. Back cuts 1 on
fold with a shallow scoop. Both panels share one side construction: straight
from the underarm to the waist, then an A-line flare (`flare_mm`, default 100)
to the hem. The tie exit — the side-seam opening the inner of the two 900 x 45
waist ties passes through — is notched on BOTH side edges at the waist arc
fraction and marked internally on the front. The short cap sleeve is
bisection-solved to the measured front + back armholes (zero ease, multi-edge
seam check, tol 2.0); shoulder and side seams match by shared construction.
Parameter contract: `project.json` + the `main.py` docstring.

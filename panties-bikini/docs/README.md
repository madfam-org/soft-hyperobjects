# Bikini Panties — FC-100 rank #45

The commons' first intimates draft. Three fold-cut pieces: a high-cut front,
a fuller-coverage back, and a waisted trapezoid gusset cut twice (self +
liner). All three draft as half-pieces on the fold, so the gusset's front and
back edges equal the bodies' gusset edges **by construction** — enforced by
two declared seam checks (tol 1.0 mm) at render time.

The star is the elastic accounting: waist and leg edges carry zero allowance
(elastic finish, with marked application zones) and the BOM emits exact-mm
cut lengths — waist elastic = full waist opening x 0.90, per-leg elastic =
(front + back leg curves) x 0.85 — recomputed from the measured pattern for
any body size.

Known v0 simplifications (documented, not hidden): front and back share one
rise height (no separate back rise); the leg elastic formula spans the front
and back curves only, with the gusset side edges caught flat underneath;
sides join edge-to-edge without a discrete side-seam panel.

```bash
python apps/api/services/engine/fc_runner.py projects/panties-bikini/main.py panties.svg '{}' svg
```

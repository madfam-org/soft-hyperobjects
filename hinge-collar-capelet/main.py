"""
Articulated hinge-collar capelet — FC-400 rank #344, Lane 5 (am_fashion). Fashion Cabinet.

A short shoulder cape (capelet) that stands on an articulated printed TPU hinge collar —
a printed living-hinge band at the neck that folds crisply where a sewn collar would only
crease, so the capelet stands up and turns down on a real hinge. The hinge collar is
Yantra4D territory (notion.hardware_ref → tpu-hinge-collar); Fashion Cabinet owns the cape
FASHION: the capelet drafted as a half-annulus (inner ring = neckline, outer ring = the
hem sweep) and the collar band length DERIVED from the neckline.

What this cartridge owns:
  - THE CAPE placement guide: a half-annulus (cut on the fold, mirrored) whose inner ring
    is the neckline and whose outer ring is the hem sweep, sized from neck girth and cape
    length. Corrected-polygon radii so drafted perimeters equal circumferences.
  - THE HINGE-COLLAR band length DERIVED from the neckline (collar_len == neck opening).

Solving and clamps. The inner (neck) radius is floored below the outer (hem) radius so the
annulus never inverts; the cape length is floored. The collar length is floored. Match the
manifest params_map exactly.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # cape|set

neck_girth = float(PARAM(lambda: neck_girth, 400.0))
collar_ease = float(PARAM(lambda: collar_ease, 40.0))
cape_length = float(PARAM(lambda: cape_length, 320.0))   # neck ring to hem (radial)
band_h = float(PARAM(lambda: band_h, 60.0))              # hinge collar band height
wall = float(PARAM(lambda: wall, 1.2))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

neck_girth = max(300.0, min(neck_girth, 560.0))
collar_ease = max(0.0, min(collar_ease, 160.0))
cape_length = max(150.0, min(cape_length, 700.0))
band_h = max(25.0, min(band_h, 180.0))
wall = max(0.6, min(wall, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

SEGS = 64
COLLAR_LEN = max(200.0, neck_girth + collar_ease)         # neck opening
CAPE_L = max(100.0, cape_length)


def _poly_radius(c, n):
    return c / (2.0 * n * math.sin(math.pi / n))


R_INNER = _poly_radius(COLLAR_LEN, SEGS)                  # neckline ring
R_OUTER = R_INNER + CAPE_L                                # hem sweep ring
OUTER_SWEEP = 2.0 * SEGS * R_OUTER * math.sin(math.pi / SEGS)


def _arc_points(r, a0, a1, n):
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def build():
    half = SEGS // 2
    outer = _arc_points(R_OUTER, -math.pi / 2.0, math.pi / 2.0, half)
    inner = _arc_points(R_INNER, math.pi / 2.0, -math.pi / 2.0, half)
    edges = [
        fc.Edge("hem", [fc.Line(outer[i], outer[i + 1]) for i in range(len(outer) - 1)]),
        fc.Edge("centre_back", [fc.Line(outer[-1], inner[0])]),
        # neck seam (the sewn edge the printed collar attaches to)
        fc.Edge("guide", [fc.Line(inner[i], inner[i + 1]) for i in range(len(inner) - 1)]),
        fc.Edge("centre_front", [fc.Line(inner[-1], outer[0])]),
    ]
    piece = fc.Piece(
        "cape", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("guide", 0.5, "shoulder"), fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(R_INNER + CAPE_L * 0.4, -R_OUTER * 0.25),
                               fc.P(R_INNER + CAPE_L * 0.4, R_OUTER * 0.25)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Capelet (half-annulus)",
    )
    pattern = fc.PatternSet("hinge-collar-capelet")
    pattern.add(piece)
    # The two half-annulus copies join at the centre-back seam.
    pattern.declare_seam(("cape", "centre_back"), ("cape", "centre_back"), tol=1.0)
    pattern.metadata = {
        "fc400_rank": 344, "family": "am_fashion", "lane": 5,
        "collar_len_mm": round(COLLAR_LEN, 1), "cape_length_mm": round(CAPE_L, 1),
        "band_h_mm": round(band_h, 1), "wall_mm": wall,
        "neck_ring_mm": round(COLLAR_LEN, 1), "hem_sweep_mm": round(OUTER_SWEEP, 1),
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A) collar; soft shell cape",
        "hardware": "articulated collar delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-hinge-collar)",
        "note": "the neck ring is on the corrected polygon radius so the drafted "
                "perimeter equals the collar length; the inner radius is floored below "
                "the outer so the annulus never inverts",
    }
    return pattern


result = build()

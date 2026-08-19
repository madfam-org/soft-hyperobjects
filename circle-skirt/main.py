"""
Circle Skirt — Fashion Cabinet Garment Cartridge (FC-200 #178, skirt gap).

The full circle skirt: a skirt cut as an annulus so the hem is a full circle and the skirt
falls in even waves with no gathers. Drafted as a QUARTER annulus (cut on both folds → a full
circle in 1 or 2 pieces) whose inner arc equals a quarter of the waist (solved: inner radius =
waist / 2π) and whose outer radius is inner + length. A fullness slider trades a full circle
for a half/three-quarter circle by scaling the subtended angle. Distinct from FC-100's gathered
and A-line skirts — the circle skirt's volume is pure geometry, not gathering.

Pieces:
  - skirt : quarter-annulus panel (cut on fold both ways), waist arc solved to the measure.
  - waistband : a fitted band strip solved to the waist.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))    # skirt|waistband|set

waist_girth  = float(PARAM(lambda: waist_girth, 760.0))
skirt_length = float(PARAM(lambda: skirt_length, 600.0))   # waist to hem
fullness     = float(PARAM(lambda: fullness, 1.0))         # 1.0 = full circle, 0.5 = half
band_height  = float(PARAM(lambda: band_height, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 15.0)) # small hem — bias, circular

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(500.0, min(waist_girth, 1400.0))
skirt_length = max(250.0, min(skirt_length, 1100.0))
fullness     = max(0.5, min(fullness, 1.0))
band_height  = max(20.0, min(band_height, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 40.0))

# A "full circle" of fullness F has total waist circumference = waist_girth, distributed over
# an angle 2*pi*F. Inner radius so that the inner arc over that angle == waist_girth:
#   r_in = waist_girth / (2*pi*F)
# We draft a QUARTER of the whole (angle = (2*pi*F)/4), cut on both folds → full skirt.
FULL_ANGLE = 2.0 * math.pi * fullness
r_in = waist_girth / FULL_ANGLE
QUARTER = FULL_ANGLE / 4.0
r_out = r_in + skirt_length


def build_skirt():
    n = 24
    inner = [fc.P(r_in * math.cos(QUARTER * i / n), r_in * math.sin(QUARTER * i / n))
             for i in range(n + 1)]
    outer = [fc.P(r_out * math.cos(QUARTER * i / n), r_out * math.sin(QUARTER * i / n))
             for i in range(n + 1)]
    waist_edge = fc.Edge("waist", [fc.Line(inner[i], inner[i + 1]) for i in range(n)])
    side_b = fc.Edge("side", [fc.Line(inner[n], outer[n])])
    hem_edge = fc.Edge("hem", [fc.Line(outer[n - i], outer[n - i - 1]) for i in range(n)])
    side_a = fc.Edge("center", [fc.Line(outer[0], inner[0])])
    return fc.Piece(
        "skirt",
        [waist_edge, side_b, hem_edge, side_a],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.0, "centre front"), fc.Notch("waist", 1.0, "side")],
        grainline=fc.Grainline(fc.P(r_in + 20.0, 8.0), fc.P(r_out - 20.0, 8.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Skirt (quarter circle)",
    )


def build_band():
    band_len = waist_girth + 40.0
    h = band_height * 2.0
    return fc.Piece(
        "waistband",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, h))]),
            fc.Edge("fold", [fc.Line(fc.P(band_len, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("attach", 0.25, "quarter"), fc.Notch("attach", 0.75, "quarter")],
        grainline=fc.Grainline(fc.P(band_len * 0.2, h / 2.0), fc.P(band_len * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Waistband",
    )


def build():
    pattern = fc.PatternSet("circle-skirt")
    everything = target_piece == "set"
    if everything or target_piece == "skirt":
        pattern.add(build_skirt())
    if everything or target_piece == "waistband":
        pattern.add(build_band())

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)          # circular layout wastes more
    pattern.bom = [
        {"item": "drapey woven (crepe, cotton-sateen, light denim)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 62% marker; circular pieces nest loosely — expect waste."},
        {"item": "invisible side zip", "qty": 1, "unit": "pc",
         "note": "the skirt closes at a side seam with an invisible zip."},
        {"item": "waistband interfacing", "qty": 1, "unit": "as needed",
         "note": "stabilises the fitted band."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "a narrow rolled or bias-faced hem suits the circular edge."},
    ]
    pattern.metadata = {
        "fc200_rank": 178, "family": "skirts", "fabric_hint": "crepe-sateen",
        "silhouette_note": "A circle skirt cut as an annulus: the waist arc is solved so its "
            "inner radius = waist / (2*pi*fullness); the hem is a full (or part) circle that "
            "falls in even waves with no gathers. Volume is pure geometry.",
        "solved": {"r_in_mm": round(r_in, 1), "r_out_mm": round(r_out, 1),
                   "fullness": fullness, "waist_girth_mm": round(waist_girth, 1)},
    }
    return pattern


result = build()

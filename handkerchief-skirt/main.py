"""
Handkerchief Skirt — Fashion Cabinet Garment Cartridge (FC-200 #180, skirt gap).

The handkerchief (pointed-hem) skirt: a skirt whose hem falls in points because the panels are
squares hung from a circular waist by their midpoints, so the corners drop lower than the sides.
This cartridge drafts it as two square panels (front + back), each cut on fold, with a quarter-
circle waist arc removed at the top-inner corner (solved to a quarter of the waist) so the square
hangs from the waist and its outer corners become the handkerchief points. Distinct from FC-100's
straight/gathered skirts — the pointed hem is the square geometry, not shaping.

Pieces:
  - panel : square handkerchief panel (cut on fold; 2 of them = front + back), waist arc solved.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # panel|waistband|set

waist_girth  = float(PARAM(lambda: waist_girth, 760.0))
point_drop   = float(PARAM(lambda: point_drop, 620.0))     # length to the handkerchief points
band_height  = float(PARAM(lambda: band_height, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 12.0)) # narrow rolled hem

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(520.0, min(waist_girth, 1300.0))
point_drop   = max(300.0, min(point_drop, 1100.0))
band_height  = max(20.0, min(band_height, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 30.0))

# The waist opening is a circle of circumference waist_girth → radius r_w = waist / 2pi.
# Each panel (front/back) spans a quarter of the waist on the fold. The square's half-diagonal
# reaches point_drop below the waist. Build the panel as: inner quarter-circle (waist) + two
# straight sides meeting at the dropped outer point.
r_w = waist_girth / (2.0 * math.pi)
QUARTER = math.pi / 2.0
# outer point sits on the fold-diagonal at radius r_w + point_drop
r_point = r_w + point_drop


def build_panel():
    n = 18
    inner = [fc.P(r_w * math.cos(QUARTER * i / n), r_w * math.sin(QUARTER * i / n))
             for i in range(n + 1)]
    # the square's outer edges: from the side hem corner straight to the dropped centre point.
    # side hem corners sit level with the waist ends, dropped straight down by point_drop*0.55
    side_drop = point_drop * 0.55
    hem_corner_a = fc.P(inner[0].x, inner[0].y - side_drop)          # near CF side
    hem_corner_b = fc.P(inner[n].x, inner[n].y - side_drop)          # near side-seam side
    outer_point = fc.P(r_point * math.cos(QUARTER * 0.5),
                       r_point * math.sin(QUARTER * 0.5))            # dropped diagonal point
    waist_edge = fc.Edge("waist", [fc.Line(inner[i], inner[i + 1]) for i in range(n)])
    side_b = fc.Edge("side", [fc.Line(inner[n], hem_corner_b)])
    hem_edge = fc.Edge("hem", [fc.Line(hem_corner_b, outer_point),
                               fc.Line(outer_point, hem_corner_a)])
    side_a = fc.Edge("center", [fc.Line(hem_corner_a, inner[0])])
    return fc.Piece(
        "panel",
        [waist_edge, side_b, hem_edge, side_a],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.0, "centre"), fc.Notch("waist", 1.0, "side")],
        grainline=fc.Grainline(fc.P(r_w + 20.0, 8.0), fc.P(r_point - 20.0, 8.0)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="center", mirror=True),
        label="Handkerchief panel (front + back)",
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
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(band_len * 0.2, h / 2.0), fc.P(band_len * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Waistband",
    )


def build():
    pattern = fc.PatternSet("handkerchief-skirt")
    everything = target_piece == "set"
    if everything or target_piece == "panel":
        pattern.add(build_panel())
    if everything or target_piece == "waistband":
        pattern.add(build_band())

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.64)
    pattern.bom = [
        {"item": "very light woven (chiffon, georgette, voile)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 64% marker; a light fabric lets the points float."},
        {"item": "invisible side zip", "qty": 1, "unit": "pc",
         "note": "closes at a side seam."},
        {"item": "narrow rolled-hem thread", "qty": 1, "unit": "spool",
         "note": "a fine rolled or lettuce hem finishes the pointed edges."},
    ]
    pattern.metadata = {
        "fc200_rank": 180, "family": "skirts", "fabric_hint": "gasa-georgette",
        "silhouette_note": "A pointed-hem skirt: square-ish panels hung from a solved circular "
            "waist arc so their outer corners drop into handkerchief points below the side hem. "
            "The points are the square geometry, not shaping.",
        "solved": {"waist_radius_mm": round(r_w, 1), "point_drop_mm": round(point_drop, 1)},
    }
    return pattern


result = build()

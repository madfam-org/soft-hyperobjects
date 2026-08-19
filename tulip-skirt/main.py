"""
Tulip Skirt — Fashion Cabinet Garment Cartridge (FC-200 #181, skirt gap).

The tulip (petal) skirt: a short, rounded skirt whose front is made of two overlapping curved
petal panels that wrap over each other like tulip leaves, narrowing to the hem, over a plain
back. The petals' curved outer edges create the rounded, tapering tulip line. This cartridge
drafts a petal panel (cut 2, overlapping at CF) and a back panel sharing the straight side seam
(balances by construction). Distinct from FC-100's straight/gathered skirts — the shape is the
overlapping curved petals.

Pieces:
  - petal : curved front petal (cut 2, overlapping at CF).
  - back  : plain back panel (cut on fold), darted to the waist.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))    # petal|back|set

waist_girth  = float(PARAM(lambda: waist_girth, 760.0))
hip_girth    = float(PARAM(lambda: hip_girth, 980.0))
skirt_length = float(PARAM(lambda: skirt_length, 480.0))   # short tulip
overlap      = float(PARAM(lambda: overlap, 140.0))        # how far the petals cross CF
petal_curve  = float(PARAM(lambda: petal_curve, 90.0))     # how much the petal rounds in at hem
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(520.0, min(waist_girth, 1300.0))
hip_girth    = max(700.0, min(hip_girth, 1500.0))
skirt_length = max(300.0, min(skirt_length, 700.0))
overlap      = max(60.0, min(overlap, 260.0))
petal_curve  = max(30.0, min(petal_curve, 200.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

WAIST_HALF = waist_girth / 4.0
HIP_HALF   = hip_girth / 4.0
L = skirt_length
HIP_Y = L - 130.0


def build_petal():
    # petal front (cut 2 mirror). Extends past CF by `overlap` at the waist so the two petals
    # cross; the outer hem curves IN by petal_curve for the rounded tulip shape. Side seam is a
    # straight vertical (balances the back).
    waist_in = fc.P(-overlap, L)                       # crosses past CF at the waist
    side_top = fc.P(HIP_HALF, HIP_Y)
    hem_in = fc.P(0.0, 0.0)
    internals = [fc.Internal("dart", [fc.P(WAIST_HALF * 0.5, L),
                                      fc.P(WAIST_HALF * 0.5, L - 120.0)], kind="dart")]
    return fc.Piece(
        "petal",
        [
            fc.Edge("waist", [fc.Line(waist_in, fc.P(WAIST_HALF, L))]),
            fc.Edge("side", [fc.Line(fc.P(WAIST_HALF, L), side_top),
                             fc.Line(side_top, fc.P(HIP_HALF, 0.0))]),
            fc.Edge("hem", [fc.curve_through(fc.P(HIP_HALF, 0.0), hem_in,
                                             bulge=petal_curve / max(HIP_HALF, 1.0), side=1.0)]),
            fc.Edge("center_front", [fc.curve_through(hem_in, waist_in, bulge=0.14, side=1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "side"), fc.Notch("side", 1.0, "hip")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 60.0), fc.P(WAIST_HALF * 0.5, L - 80.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front petal (overlapping)",
    )


def build_back():
    side_pts = [fc.P(WAIST_HALF, L), fc.P(HIP_HALF, HIP_Y), fc.P(HIP_HALF, 0.0)]
    internals = [fc.Internal("dart", [fc.P(WAIST_HALF * 0.5, L),
                                      fc.P(WAIST_HALF * 0.5, L - 120.0)], kind="dart")]
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, L), fc.P(WAIST_HALF, L))]),
            fc.Edge("side", [fc.Line(side_pts[0], side_pts[1]), fc.Line(side_pts[1], side_pts[2])]),
            fc.Edge("hem", [fc.Line(fc.P(HIP_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "side"), fc.Notch("side", 0.5, "hip")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 60.0), fc.P(WAIST_HALF * 0.5, L - 80.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build():
    pattern = fc.PatternSet("tulip-skirt")
    everything = target_piece == "set"
    if everything or target_piece == "petal":
        pattern.add(build_petal())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything:
        pattern.declare_seam(("petal", "side"), ("back", "side"), tol=1.5)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "crisp woven with body (cotton-sateen, faille)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 72% marker; a fabric with body holds the petal curve."},
        {"item": "invisible side zip", "qty": 1, "unit": "pc", "note": "closes at a side seam."},
        {"item": "lining (recommended)", "qty": 1, "unit": "as chosen",
         "note": "a lining lets the overlapping petals sit smoothly; the maker's choice."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "seams + darts."},
    ]
    pattern.metadata = {
        "fc200_rank": 181, "family": "skirts", "fabric_hint": "sateen-faille",
        "silhouette_note": "A short skirt whose front is two overlapping curved petals crossing "
            "at CF and rounding in at the hem (tulip line), over a darted back. The overlap and "
            "the curved petal edges are the shape; the straight side seam balances.",
        "solved": {"waist_q_mm": round(WAIST_HALF, 1), "overlap_mm": round(overlap, 1),
                   "petal_curve_mm": round(petal_curve, 1)},
    }
    return pattern


result = build()

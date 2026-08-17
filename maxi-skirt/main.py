"""
Maxi Skirt — FC-100 rank #82. Fashion Cabinet Garment Cartridge.

Gathered elastic-waist maxi skirt in woven fabric. Front and back are
RECTANGULAR gathered panels cut once on the fold: each drafted half-width is
(hip_girth + hip_ease) / 4 widened by `gather_ratio`, so the fullness of the
gather is a computed parameter, not a guess. A fold-over elastic casing is
derived from the measured waist edges (the leggings waistband lineage), and a
"gather zone" internal line marks the waist run that gathers into it.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|waistband|set

waist_girth    = float(PARAM(lambda: waist_girth, 700.0))
hip_girth      = float(PARAM(lambda: hip_girth, 940.0))
skirt_length   = float(PARAM(lambda: skirt_length, 950.0))
gather_ratio   = float(PARAM(lambda: gather_ratio, 1.6))   # panel width / body quarter
hip_ease       = float(PARAM(lambda: hip_ease, 40.0))
elastic_width  = float(PARAM(lambda: elastic_width, 35.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(600.0, min(hip_girth, 1700.0))
skirt_length = max(600.0, min(skirt_length, 1200.0))
gather_ratio = max(1.2, min(gather_ratio, 2.2))
hip_ease = max(0.0, min(hip_ease, 150.0))
elastic_width = max(20.0, min(elastic_width, 50.0))

CASING_RATIO = 1.0    # casing length / ungathered skirt waist (casing gathers with the elastic)
GATHER_DROP = 15.0    # gather-zone guide sits this far below the waist stitch line
HALF_W = (hip_girth + hip_ease) / 4.0 * gather_ratio   # half-panel width (fold at center)


def build_panel(name, label):
    """One rectangular gathered panel, center line on the fold."""
    w, ln = HALF_W, skirt_length
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
        fc.Edge("waist", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
        fc.Edge("center", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5)],
        grainline=fc.Grainline(fc.P(w * 0.5, ln * 0.1), fc.P(w * 0.5, ln * 0.9)),
        internals=[fc.Internal("gather zone", [fc.P(0.0, ln - GATHER_DROP),
                                               fc.P(w, ln - GATHER_DROP)])],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_waistband(front, back):
    """Fold-over elastic casing derived from the measured waist edges."""
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    length = circ * CASING_RATIO + 2.0 * seam_allowance
    band_h = 2.0 * (elastic_width + seam_allowance)
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Waistband casing (fold-over)",
    )


def build():
    pattern = fc.PatternSet("maxi-skirt")
    front = build_panel("front", "Skirt Front (gathered panel)")
    back = build_panel("back", "Skirt Back (gathered panel)")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "waistband":
        pattern.add(build_waistband(front, back))
        pattern.bom.append({
            "item": "fold-over elastic",
            "qty": round(waist_girth + 20.0),
            "unit": "mm",
            "note": "cut to waist girth + 20 mm join overlap; the casing gathers onto it",
        })
    if all_pieces:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 82,
        "fabric_hint": "popelina-algodon",
        "gather_ratio": gather_ratio,
        "drafting": "rectangular gathered panels on the fold; casing derived from the "
                    "measured waist edges",
    }
    return pattern


result = build()

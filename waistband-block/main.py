"""
Waistband Block — Fashion Cabinet Enabler Cartridge (not FC-100 counted).

A straight fold-over waistband strip drafted cut-ready: the rectangle carries
its own seam allowances (both ends and both long edges) and folds at
mid-height, so the BOTTOM edge is the waist-seam interface that skirts,
trousers, and shorts in the FC-100 bind their waists to.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "waistband"))

waist_length   = float(PARAM(lambda: waist_length, 0.0))   # FULL waist seam; 0 = auto
waist_girth    = float(PARAM(lambda: waist_girth, 700.0))
standing_ease  = float(PARAM(lambda: standing_ease, 20.0))
band_height    = float(PARAM(lambda: band_height, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

waist_girth = max(400.0, min(waist_girth, 1400.0))
standing_ease = max(0.0, min(standing_ease, 60.0))
waist = waist_length if waist_length > 0 else waist_girth + standing_ease
waist = max(360.0, min(waist, 1600.0))
band_height = max(20.0, min(band_height, 80.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

LENGTH = waist + 2.0 * seam_allowance                  # end allowances drafted in
HEIGHT = 2.0 * (band_height + seam_allowance)          # fold-over: two bands + long-edge SAs


def build():
    origin = fc.P(0.0, 0.0)
    br = fc.P(LENGTH, 0.0)
    tr = fc.P(LENGTH, HEIGHT)
    tl = fc.P(0.0, HEIGHT)
    fold_y = HEIGHT / 2.0
    piece = fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(origin, br)]),
            fc.Edge("end_b", [fc.Line(br, tr)]),
            fc.Edge("top", [fc.Line(tr, tl)]),
            fc.Edge("end_a", [fc.Line(tl, origin)]),
        ],
        seam_allowance=0.0,  # strip is drafted cut-ready; allowances live in the rectangle
        notches=[fc.Notch("bottom", 0.5, "side seam match")],
        grainline=fc.Grainline(fc.P(LENGTH * 0.08, HEIGHT * 0.3),
                               fc.P(LENGTH * 0.92, HEIGHT * 0.3)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, fold_y), fc.P(LENGTH, fold_y)]),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Waistband (fold-over strip)",
    )
    pattern = fc.PatternSet("waistband-block")
    pattern.add(piece)
    pattern.metadata = {
        "enabler": True,
        "interface": "waistband",
        "band_bottom_mm": round(LENGTH, 1),
        "drafting": "straight fold-over band; allowances drafted in, fold line at mid-height",
    }
    return pattern


result = build()

"""
Band Collar (Mandarin) — Fashion Cabinet Enabler Cartridge (not FC-100 counted).

A curved half-collar (cut on fold at CB) whose NECK EDGE is solved to half
the target neckline length plus a button-stand overlap — the second consumer
in the cross-cartridge interface lane, fed by the bodice block's measured
neckline in CI.

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


target_piece = str(PARAM(lambda: target_piece, "collar"))

neckline_length = float(PARAM(lambda: neckline_length, 0.0))  # FULL opening; 0 = auto
neck_girth      = float(PARAM(lambda: neck_girth, 370.0))
collar_height   = float(PARAM(lambda: collar_height, 30.0))
overlap         = float(PARAM(lambda: overlap, 15.0))         # button-stand extension
rise            = float(PARAM(lambda: rise, 14.0))            # front-edge curl
seam_allowance  = float(PARAM(lambda: seam_allowance, 8.0))

neck_girth = max(280.0, min(neck_girth, 540.0))
opening = neckline_length if neckline_length > 0 else neck_girth * 1.12
opening = max(260.0, min(opening, 700.0))
collar_height = max(20.0, min(collar_height, 60.0))
overlap = max(0.0, min(overlap, 40.0))

HALF_TARGET = opening / 2.0 + overlap


def _neck_edge(flat_len):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat_len, rise), bulge=0.05, side=-1.0)],
    )


def build():
    lo, hi = HALF_TARGET * 0.7, HALF_TARGET * 1.05
    for _ in range(44):
        mid = (lo + hi) / 2.0
        if _neck_edge(mid).length(0.05) < HALF_TARGET:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(_neck_edge(flat).length(0.05) - HALF_TARGET) > 1.0:
        raise ValueError("collar neck-edge solver did not converge")
    neck = _neck_edge(flat)
    top_start = fc.P(0.0, collar_height)
    top_end = fc.P(flat, rise + collar_height)
    piece = fc.Piece(
        "collar",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, rise), top_end)]),
            fc.Edge(
                "top",
                [fc.curve_through(top_end, top_start, bulge=0.05, side=1.0)],
            ),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, collar_height * 0.5),
                               fc.P(flat * 0.75, collar_height * 0.5 + rise * 0.7)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Band Collar (half, on fold)",
    )
    pattern = fc.PatternSet("collar-band")
    pattern.add(piece)
    pattern.metadata = {
        "enabler": True,
        "interface": "neckline",
        "half_target_mm": round(HALF_TARGET, 1),
        "overlap_mm": overlap,
        "drafting": "curved band collar; neck edge solved to opening/2 + overlap",
    }
    return pattern


result = build()

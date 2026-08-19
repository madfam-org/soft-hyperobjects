"""
Printed Hinge Collar — Fashion Cabinet Notion Cartridge (Yantra4D-bridged printed finding).

The printed part itself is Yantra4D territory (CadQuery; see the manifest's
notion.hardware_ref -> tpu-hinge-collar). What Fashion Cabinet owns is the fashion — sizing to
the wearer and the 2-D placement guide for the sewn edge. One material identity spans
this notion and that solid.

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


neck_girth = float(PARAM(lambda: neck_girth, 400.0))
band_h = float(PARAM(lambda: band_h, 30.0))
stand_h = float(PARAM(lambda: stand_h, 35.0))
wall = float(PARAM(lambda: wall, 2.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

neck_girth = max(280.0, min(neck_girth, 600.0))
band_h = max(10.0, min(band_h, 120.0))
stand_h = max(10.0, min(stand_h, 120.0))
wall = max(1.0, min(wall, 6.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

GW = max(10.0, float(neck_girth))
GH = max(10.0, float(stand_h + band_h))


def build():
    origin, tl, tr, br = fc.P(0.0, 0.0), fc.P(0.0, GH), fc.P(GW, GH), fc.P(GW, 0.0)
    edges = [
        fc.Edge("guide",  [fc.Line(origin, tl)]),   # sewn edge
        fc.Edge("top",    [fc.Line(tl, tr)]),
        fc.Edge("side",   [fc.Line(tr, br)]),
        fc.Edge("bottom", [fc.Line(br, origin)]),
    ]
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=float(seam_allowance),
        grainline=fc.Grainline(fc.P(GW * 0.5, GH * 0.15), fc.P(GW * 0.5, GH * 0.85)),
        cut=fc.CutSpec(quantity=1),
        label="Printed Hinge Collar Placement Guide",
    )
    pattern = fc.PatternSet("printed-hinge-collar")
    pattern.add(piece)
    pattern.metadata = {
        "guide_w_mm": round(GW, 1), "guide_h_mm": round(GH, 1),
        "hardware": "printed part delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-hinge-collar)",
    }
    return pattern


result = build()

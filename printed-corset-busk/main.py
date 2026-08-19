"""
Printed Corset Busk — Fashion Cabinet Notion Cartridge (Yantra4D-bridged printed finding).

The printed part itself is Yantra4D territory (CadQuery; see the manifest's
notion.hardware_ref -> corset-busk). What Fashion Cabinet owns is the fashion — sizing to
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


busk_len = float(PARAM(lambda: busk_len, 300.0))
plate_w = float(PARAM(lambda: plate_w, 16.0))
plate_t = float(PARAM(lambda: plate_t, 3.0))
knobs = int(PARAM(lambda: knobs, 5))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

busk_len = max(120.0, min(busk_len, 500.0))
plate_w = max(8.0, min(plate_w, 40.0))
plate_t = max(1.5, min(plate_t, 8.0))
knobs = max(2.0, min(knobs, 12.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

GW = max(10.0, float(plate_w))
GH = max(10.0, float(busk_len))


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
        label="Printed Corset Busk Placement Guide",
    )
    pattern = fc.PatternSet("printed-corset-busk")
    pattern.add(piece)
    pattern.metadata = {
        "guide_w_mm": round(GW, 1), "guide_h_mm": round(GH, 1),
        "hardware": "printed part delegated to Yantra4D "
                    "(notion.hardware_ref -> corset-busk)",
    }
    return pattern


result = build()

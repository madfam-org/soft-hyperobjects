"""
Patch Pocket — Fashion Cabinet Enabler Cartridge (not FC-100 counted).

A rectangular patch pocket whose two BOTTOM corners are cut by 45° chamfers —
six Line edges forming a closed hexagon. The TOP edge is the opening and
carries a hem-facing allowance; a topstitch guide traces the attach path 8 mm
inside the sides and bottom. Provider half of the `pocket` interface reused by
shirts, aprons, and workwear across the FC-100.

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


pocket_width   = float(PARAM(lambda: pocket_width, 160.0))
pocket_height  = float(PARAM(lambda: pocket_height, 180.0))
corner_chamfer = float(PARAM(lambda: corner_chamfer, 30.0))
hem_facing     = float(PARAM(lambda: hem_facing, 25.0))    # TOP edge (opening) allowance
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

pocket_width = max(80.0, min(pocket_width, 400.0))
pocket_height = max(80.0, min(pocket_height, 400.0))
hem_facing = max(0.0, min(hem_facing, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))
# Chamfers stay strictly under a third of the smaller side.
corner_chamfer = max(5.0, min(corner_chamfer, min(pocket_width, pocket_height) / 3.0 - 0.5))

TOPSTITCH_INSET = 8.0


def build():
    w, h, c = pocket_width, pocket_height, corner_chamfer
    inset = TOPSTITCH_INSET
    piece = fc.Piece(
        "pocket",
        [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, c))]),
            fc.Edge("chamfer_r", [fc.Line(fc.P(w, c), fc.P(w - c, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w - c, 0.0), fc.P(c, 0.0))]),
            fc.Edge("chamfer_l", [fc.Line(fc.P(c, 0.0), fc.P(0.0, c))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, c), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": hem_facing},
        notches=[fc.Notch("top", 0.5, "center match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.15), fc.P(w / 2.0, h * 0.85)),
        internals=[fc.Internal(
            "topstitch guide",
            [fc.P(w - inset, h), fc.P(w - inset, inset),
             fc.P(inset, inset), fc.P(inset, h)],
        )],
        cut=fc.CutSpec(quantity=1),
        label="Patch Pocket",
    )
    pattern = fc.PatternSet("patch-pocket")
    pattern.add(piece)
    pattern.metadata = {
        "enabler": True,
        "interface": "pocket",
    }
    return pattern


result = build()

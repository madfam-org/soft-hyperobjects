"""
Parametric printed ruff collar — FC-400 rank #349, Lane 5 (am_fashion). Fashion Cabinet.

The Elizabethan ruff, reimagined as a printed TPU pleat panel: a long figure-of-eight
pleated band, printed with the springy accordion folds that a starched linen ruff once got
from setting-sticks, so it holds its cartwheel shape and folds flat to pack. The pleat panel
is Yantra4D territory (notion.hardware_ref → tpu-pleat-panel); Fashion Cabinet owns the ruff
FASHION: the flat pleated band length (the OUTER run of the ruff, far longer than the neck)
and the pleat count DERIVED from that length and the pleat pitch.

What this cartridge owns:
  - THE RUFF BAND placement guide: a long rectangle whose length is the ruff's outer run
    (neck opening × the fullness ratio) and whose height is the ruff depth.
  - THE PLEAT FIELD: pleats = band length / pleat_pitch, floored — the exact number the
    tpu-pleat-panel prints.

Solving and clamps. The band length is DERIVED (neck girth × fullness) and FLOORED; the
pleat count is floored at 2 so it is genuinely a ruff. The ruff depth is floored. Match the
manifest params_map exactly.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # placement-guide|set

neck_girth = float(PARAM(lambda: neck_girth, 400.0))
fullness = float(PARAM(lambda: fullness, 4.0))           # outer run / neck opening
ruff_depth = float(PARAM(lambda: ruff_depth, 120.0))     # radial depth of the ruff
pleat_pitch = float(PARAM(lambda: pleat_pitch, 28.0))
pleat_depth = float(PARAM(lambda: pleat_depth, 22.0))
wall = float(PARAM(lambda: wall, 0.9))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

neck_girth = max(300.0, min(neck_girth, 560.0))
fullness = max(2.0, min(fullness, 8.0))
ruff_depth = max(40.0, min(ruff_depth, 260.0))
pleat_pitch = max(10.0, min(pleat_pitch, 60.0))
pleat_depth = max(5.0, min(pleat_depth, 60.0))
wall = max(0.5, min(wall, 3.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

BAND_LEN = max(600.0, neck_girth * fullness)             # the ruff's flat outer run
H = max(40.0, ruff_depth)
pleats = max(2, round(BAND_LEN / pleat_pitch))


def build():
    origin = fc.P(0.0, 0.0)
    br = fc.P(BAND_LEN, 0.0)
    tr = fc.P(BAND_LEN, H)
    tl = fc.P(0.0, H)
    edges = [
        fc.Edge("guide", [fc.Line(origin, br)]),           # neck-edge (sewn, gathered)
        fc.Edge("end_b", [fc.Line(br, tr)]),
        fc.Edge("outer", [fc.Line(tr, tl)]),
        fc.Edge("end_a", [fc.Line(tl, origin)]),
    ]
    internals = []
    for p in range(1, pleats):
        x = BAND_LEN * p / pleats
        internals.append(fc.Internal(f"pleat-{p}", [fc.P(x, 0.0), fc.P(x, H)],
                                     kind="marking"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(BAND_LEN * 0.5, H * 0.2), fc.P(BAND_LEN * 0.5, H * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Parametric Ruff Placement Guide",
    )
    pattern = fc.PatternSet("parametric-ruff")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 349, "family": "am_fashion", "lane": 5,
        "neck_opening_mm": round(neck_girth, 1), "band_len_mm": round(BAND_LEN, 1),
        "fullness": round(fullness, 2), "ruff_depth_mm": round(H, 1),
        "pleat_pitch_mm": pleat_pitch, "pleat_depth_mm": pleat_depth, "wall_mm": wall,
        "pleats": pleats,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "pleat field delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-pleat-panel)",
        "note": "the band length is DERIVED (neck girth × fullness) and floored; the pleat "
                "count is floored at 2 so it is genuinely a ruff",
    }
    return pattern


result = build()

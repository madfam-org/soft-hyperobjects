"""
Printed pleat-panel collar — FC-400 rank #343, Lane 5 (am_fashion). Fashion Cabinet Cartridge.

A standing collar built from a printed TPU pleat panel — accordion pleats printed into the
flat panel that spring the collar up around the neck and let it fold flat, a living-hinge
pleat field. The pleat panel is Yantra4D territory (notion.hardware_ref → tpu-pleat-panel);
Fashion Cabinet owns the collar band dimensions and the pleat count DERIVED from the collar
length and the pleat pitch so the pleats exactly fill the band.

What this cartridge owns:
  - THE COLLAR BAND placement guide: a rectangle `collar_len` long (the neck opening) and
    `stand_height` tall, with a sewn (neck-seam) lower edge.
  - THE PLEAT FIELD: pleats = collar_len / pleat_pitch, floored — the exact number the
    tpu-pleat-panel solid prints.

Solving and clamps. The collar length is DERIVED from the neck girth and the ease and
FLOORED; the pleat count is floored at 1 so the panel is never flat. Match the manifest
params_map exactly.

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
collar_ease = float(PARAM(lambda: collar_ease, 30.0))
stand_height = float(PARAM(lambda: stand_height, 70.0))
pleat_pitch = float(PARAM(lambda: pleat_pitch, 18.0))
pleat_depth = float(PARAM(lambda: pleat_depth, 12.0))
wall = float(PARAM(lambda: wall, 1.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

neck_girth = max(300.0, min(neck_girth, 560.0))
collar_ease = max(0.0, min(collar_ease, 120.0))
stand_height = max(30.0, min(stand_height, 220.0))
pleat_pitch = max(6.0, min(pleat_pitch, 50.0))
pleat_depth = max(3.0, min(pleat_depth, 40.0))
wall = max(0.5, min(wall, 3.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

COLLAR_LEN = max(200.0, neck_girth + collar_ease)         # neck opening the collar spans
H = max(30.0, stand_height)
pleats = max(1, round(COLLAR_LEN / pleat_pitch))


def build():
    origin = fc.P(0.0, 0.0)
    br = fc.P(COLLAR_LEN, 0.0)
    tr = fc.P(COLLAR_LEN, H)
    tl = fc.P(0.0, H)
    edges = [
        fc.Edge("guide", [fc.Line(origin, br)]),           # neck-seam (sewn) lower edge
        fc.Edge("end_b", [fc.Line(br, tr)]),
        fc.Edge("top", [fc.Line(tr, tl)]),
        fc.Edge("end_a", [fc.Line(tl, origin)]),
    ]
    internals = []
    for p in range(1, pleats):
        x = COLLAR_LEN * p / pleats
        internals.append(fc.Internal(f"pleat-{p}", [fc.P(x, 0.0), fc.P(x, H)],
                                     kind="marking"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(COLLAR_LEN * 0.5, H * 0.2),
                               fc.P(COLLAR_LEN * 0.5, H * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Pleat-Panel Collar Placement Guide",
    )
    pattern = fc.PatternSet("pleat-panel-collar")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 343, "family": "am_fashion", "lane": 5,
        "collar_len_mm": round(COLLAR_LEN, 1), "stand_height_mm": round(H, 1),
        "pleat_pitch_mm": pleat_pitch, "pleat_depth_mm": pleat_depth, "wall_mm": wall,
        "pleats": pleats,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "pleat field delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-pleat-panel)",
        "note": "the collar length is DERIVED from the neck girth + ease and floored; the "
                "pleat count is floored at 1 so the panel is never flat",
    }
    return pattern


result = build()

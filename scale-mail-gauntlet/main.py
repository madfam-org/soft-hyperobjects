"""
Printed scale-mail gauntlet — FC-400 rank #348, Lane 5 (am_fashion). Fashion Cabinet Cartridge.

An armoured gauntlet — forearm to knuckles — clad in a printed TPU scale-mail field, the
scales articulating over the wrist and back of the hand. The scale field is Yantra4D
territory (notion.hardware_ref → tpu-scale-mail); Fashion Cabinet owns the gauntlet FASHION:
the tapered forearm-to-hand panel and the scale field (rows × cols) DERIVED from the panel
so the scales exactly clad the sewn shape.

What this cartridge owns:
  - THE GAUNTLET panel placement guide: a tapered panel (cut 2, mirrored) from the elbow
    girth down to the knuckle width, sized from forearm length, elbow girth and hand width.
  - THE SCALE FIELD: cols/rows DERIVED from the panel size and the overlapped scale pitch.

Solving and clamps. The elbow and knuckle widths are DERIVED and FLOORED, and the taper is
monotone-clamped so the knuckle is never wider than the elbow. The scale field cols/rows are
floored at 1. Match the manifest params_map exactly.

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

forearm_length = float(PARAM(lambda: forearm_length, 300.0))   # elbow to knuckles
elbow_girth = float(PARAM(lambda: elbow_girth, 280.0))
hand_width = float(PARAM(lambda: hand_width, 100.0))
scale_size = float(PARAM(lambda: scale_size, 18.0))
overlap = float(PARAM(lambda: overlap, 0.45))
wall = float(PARAM(lambda: wall, 1.2))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

forearm_length = max(150.0, min(forearm_length, 480.0))
elbow_girth = max(180.0, min(elbow_girth, 460.0))
hand_width = max(70.0, min(hand_width, 160.0))
scale_size = max(8.0, min(scale_size, 60.0))
overlap = max(0.0, min(overlap, 0.7))
wall = max(0.6, min(wall, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

H = max(120.0, forearm_length)
ELBOW_HALF = max(70.0, elbow_girth / 2.0)                # half the elbow girth (flat panel)
KNUCKLE_HALF = max(45.0, min(hand_width * 0.9, ELBOW_HALF - 10.0))   # never wider than elbow
W = (ELBOW_HALF + KNUCKLE_HALF) / 2.0                    # for the scale field
scale_h_mm = scale_size * 1.3
cols = max(1, round(W / scale_size))
rows = max(1, round(H / (scale_h_mm * (1.0 - overlap))))


def build():
    # Tapered gauntlet panel: elbow edge (top, wide), sides taper, knuckle edge (bottom).
    el = fc.P(-ELBOW_HALF, H)
    er = fc.P(ELBOW_HALF, H)
    kr = fc.P(KNUCKLE_HALF, 0.0)
    kl = fc.P(-KNUCKLE_HALF, 0.0)
    edges = [
        fc.Edge("guide", [fc.Line(kl, el)]),               # wrist-side sewn seam (left)
        fc.Edge("elbow", [fc.Line(el, er)]),
        fc.Edge("side", [fc.Line(er, kr)]),
        fc.Edge("knuckle", [fc.Line(kr, kl)]),
    ]
    internals = []
    for r in range(1, rows):
        y = H * r / rows
        internals.append(fc.Internal(f"scale-row-{r}", [fc.P(-ELBOW_HALF, y), fc.P(ELBOW_HALF, y)],
                                     kind="marking"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(0.0, H * 0.12), fc.P(0.0, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Scale-Mail Gauntlet Placement Guide",
    )
    pattern = fc.PatternSet("scale-mail-gauntlet")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 348, "family": "am_fashion", "lane": 5,
        "forearm_length_mm": round(H, 1), "elbow_half_mm": round(ELBOW_HALF, 1),
        "knuckle_half_mm": round(KNUCKLE_HALF, 1), "panel_width_mm": round(W, 1),
        "scale_size_mm": scale_size, "overlap": overlap, "wall_mm": wall,
        "field_cols": cols, "field_rows": rows,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "scale field delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-scale-mail)",
        "note": "cols/rows DERIVED from the panel size; the knuckle half is clamped never "
                "wider than the elbow so the taper never inverts",
    }
    return pattern


result = build()

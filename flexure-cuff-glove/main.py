"""
Printed flexure-cuff glove — FC-400 rank #345, Lane 5 (am_fashion). Fashion Cabinet Cartridge.

A glove whose wrist is a printed TPU flexure cuff — a slotted living-hinge band that flexes
with the wrist and springs back, printed rather than elasticated. The flexure cuff is
Yantra4D territory (notion.hardware_ref → tpu-flexure-cuff); Fashion Cabinet owns the glove
FASHION: the hand/back placement guide and the cuff circumference DERIVED from the wrist
girth so the printed cuff exactly matches the sewn wrist opening.

What this cartridge owns:
  - THE GLOVE BACK placement guide: a hand-back panel sized from hand length and hand
    width, with a wrist edge (the sewn cuff seam) and a finger edge.
  - THE FLEXURE CUFF circumference DERIVED from the wrist girth + ease.

Solving and clamps. The hand width and length are floored; the wrist edge is the sewn edge
the cuff attaches to. The cuff circumference is floored. Match the manifest params_map.

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

hand_length = float(PARAM(lambda: hand_length, 190.0))   # wrist to fingertip
hand_width = float(PARAM(lambda: hand_width, 100.0))     # across the knuckles
wrist_girth = float(PARAM(lambda: wrist_girth, 170.0))
cuff_ease = float(PARAM(lambda: cuff_ease, 20.0))
cuff_height = float(PARAM(lambda: cuff_height, 70.0))
wall = float(PARAM(lambda: wall, 1.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

hand_length = max(120.0, min(hand_length, 260.0))
hand_width = max(70.0, min(hand_width, 150.0))
wrist_girth = max(120.0, min(wrist_girth, 240.0))
cuff_ease = max(0.0, min(cuff_ease, 80.0))
cuff_height = max(30.0, min(cuff_height, 200.0))
wall = max(0.5, min(wall, 3.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

HW = max(60.0, hand_width)
HL = max(100.0, hand_length)
CUFF_CIRC = max(120.0, wrist_girth + cuff_ease)
# Wrist edge width for the sewn seam is half the cuff circumference (a folded/flat panel).
WRIST_W = max(50.0, CUFF_CIRC / 2.0)


def build():
    # Glove-back panel: wrist edge (bottom), side seams up, a rounded finger top.
    bl = fc.P(-HW / 2.0, 0.0)
    br = fc.P(HW / 2.0, 0.0)
    tr = fc.P(HW / 2.0, HL * 0.75)
    tip_r = fc.P(HW * 0.30, HL)
    tip_l = fc.P(-HW * 0.30, HL)
    tl = fc.P(-HW / 2.0, HL * 0.75)
    edges = [
        # wrist (sewn cuff seam) — drafted at the WRIST width, centred, then jogs to hand
        fc.Edge("guide", [fc.Line(fc.P(-WRIST_W / 2.0, 0.0), fc.P(WRIST_W / 2.0, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(WRIST_W / 2.0, 0.0), br),
                           fc.Line(br, tr)]),
        fc.Edge("fingers", [fc.curve_through(tr, tip_r, bulge=0.10, side=1.0),
                            fc.curve_through(tip_r, tip_l, bulge=0.18, side=1.0),
                            fc.curve_through(tip_l, tl, bulge=0.10, side=1.0)]),
        fc.Edge("side_l", [fc.Line(tl, bl),
                           fc.Line(bl, fc.P(-WRIST_W / 2.0, 0.0))]),
    ]
    internals = [
        fc.Internal("knuckle line", [fc.P(-HW / 2.0, HL * 0.75), fc.P(HW / 2.0, HL * 0.75)],
                    kind="marking"),
    ]
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, HL - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Flexure-Cuff Glove Placement Guide",
    )
    pattern = fc.PatternSet("flexure-cuff-glove")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 345, "family": "am_fashion", "lane": 5,
        "hand_length_mm": round(HL, 1), "hand_width_mm": round(HW, 1),
        "cuff_circum_mm": round(CUFF_CIRC, 1), "cuff_height_mm": round(cuff_height, 1),
        "wall_mm": wall, "wrist_edge_mm": round(WRIST_W, 1),
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A) cuff; soft glove body",
        "hardware": "flexure cuff delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-flexure-cuff)",
        "note": "the cuff circumference is DERIVED from the wrist girth + ease and floored; "
                "the wrist edge is the sewn seam the printed cuff attaches to",
    }
    return pattern


result = build()

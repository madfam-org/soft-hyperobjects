"""
Flexure-spine fashion harness — FC-400 rank #351, Lane 5 (am_fashion). Fashion Cabinet.

A body harness whose back is a printed TPU flexure band running down the spine — a slotted
living-hinge strip that curves with the back and springs back, so the harness holds its
architectural line and still bends. The flexure band is Yantra4D territory
(notion.hardware_ref → tpu-flexure-cuff, used here as a straight spine band rather than a
wrap); Fashion Cabinet owns the harness FASHION: the strap placement guide and the spine
band length DERIVED from the back length.

What this cartridge owns:
  - THE HARNESS strap placement guide: a back panel with a central spine channel (the
    sewn edge the printed band attaches to) and two shoulder straps, sized from shoulder
    width, back length and strap width.
  - THE SPINE BAND length (cuff_circum reused as the straight band length) DERIVED from
    the back length, and the band width from strap width.

Solving and clamps. The strap width is floored below half the shoulder width so the two
straps never overlap at the centre; the spine channel width is floored. The band length is
floored. Match the manifest params_map exactly.

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

shoulder_width = float(PARAM(lambda: shoulder_width, 380.0))
back_length = float(PARAM(lambda: back_length, 420.0))    # nape to waist
strap_width = float(PARAM(lambda: strap_width, 45.0))
spine_width = float(PARAM(lambda: spine_width, 60.0))     # printed spine band width
wall = float(PARAM(lambda: wall, 1.4))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

shoulder_width = max(240.0, min(shoulder_width, 560.0))
back_length = max(220.0, min(back_length, 640.0))
strap_width = max(20.0, min(strap_width, 120.0))
spine_width = max(25.0, min(spine_width, 160.0))
wall = max(0.6, min(wall, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SHOULDER_HALF = shoulder_width / 2.0
# Strap width floored below half the shoulder so the two straps clear the centre spine.
STRAP_W = max(15.0, min(strap_width, SHOULDER_HALF - 30.0))
SPINE_HALF = max(15.0, min(spine_width, SHOULDER_HALF - STRAP_W - 5.0)) / 2.0
BACK_L = max(150.0, back_length)
SPINE_LEN = BACK_L                                       # the straight spine band length


def build():
    # Back panel outline: centre spine channel (the sewn edge), straps up to the shoulders,
    # a waist edge across the bottom. Frame: x=0 centre spine, y=0 waist.
    # Right half drafted; cut 2 mirrored gives both sides.
    spine_bottom = fc.P(SPINE_HALF, 0.0)
    spine_top = fc.P(SPINE_HALF, BACK_L)
    strap_out_top = fc.P(SPINE_HALF + 8.0 + STRAP_W, BACK_L)
    strap_out_bot = fc.P(SHOULDER_HALF, BACK_L * 0.35)
    waist_out = fc.P(SHOULDER_HALF * 0.7, 0.0)
    edges = [
        fc.Edge("guide", [fc.Line(spine_bottom, spine_top)]),   # spine channel (sewn band)
        fc.Edge("shoulder", [fc.Line(spine_top, strap_out_top)]),
        fc.Edge("strap_out", [fc.Line(strap_out_top, strap_out_bot),
                              fc.Line(strap_out_bot, waist_out)]),
        fc.Edge("waist", [fc.Line(waist_out, spine_bottom)]),
    ]
    internals = [
        fc.Internal("spine band", [fc.P(SPINE_HALF * 0.5, 10.0),
                                   fc.P(SPINE_HALF * 0.5, BACK_L - 10.0)], kind="marking"),
    ]
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(SPINE_HALF + STRAP_W * 0.5, 20.0),
                               fc.P(SPINE_HALF + STRAP_W * 0.5, BACK_L - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Flexure-Spine Harness Placement Guide",
    )
    pattern = fc.PatternSet("flexure-spine-harness")
    pattern.add(piece)
    # The two mirrored halves join at the centre spine channel (the printed band bridges).
    pattern.declare_seam(("placement-guide", "guide"), ("placement-guide", "guide"), tol=1.0)
    pattern.metadata = {
        "fc400_rank": 351, "family": "am_fashion", "lane": 5,
        "shoulder_width_mm": round(shoulder_width, 1), "back_length_mm": round(BACK_L, 1),
        "strap_width_mm": round(STRAP_W, 1), "spine_half_mm": round(SPINE_HALF, 1),
        "spine_len_mm": round(SPINE_LEN, 1), "spine_band_width_mm": round(spine_width, 1),
        "wall_mm": wall,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A) spine band; webbing straps",
        "hardware": "flexure spine band delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-flexure-cuff, straight band)",
        "note": "the strap width is floored below half the shoulder so the straps clear "
                "the centre spine; the spine band length is DERIVED from the back length",
    }
    return pattern


result = build()

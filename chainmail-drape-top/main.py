"""
Printed chainmail drape top — FC-400 rank #347, Lane 5 (am_fashion). Fashion Cabinet Cartridge.

A draped top made of printed TPU chainmail — interlocked printed rings that fall and pool
like woven maille but come off the bed already linked, no ring-by-ring assembly. The
chainmail field is Yantra4D territory (notion.hardware_ref → tpu-chainmail-panel); Fashion
Cabinet owns the drape FASHION: the top panel dimensions and the ring field (rows × cols)
DERIVED from the panel size and the ring inner diameter so the maille exactly fills the
sewn shape.

What this cartridge owns:
  - THE DRAPE panel placement guide: a wide rectangular front panel (cut on the fold) that
    falls from a shoulder seam to a low hem, sized from bust girth and top length.
  - THE RING FIELD: cols/rows DERIVED from the panel and the ring pitch (ring_id + wire_d).

Solving and clamps. The panel width and height are DERIVED and FLOORED; the field cols/rows
are floored at 1 so the maille is never empty. Match the manifest params_map exactly.

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

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
top_length = float(PARAM(lambda: top_length, 560.0))     # shoulder to hem
drape_ease = float(PARAM(lambda: drape_ease, 200.0))     # extra width for the pooling drape
ring_id = float(PARAM(lambda: ring_id, 10.0))            # ring inner diameter
wire_d = float(PARAM(lambda: wire_d, 2.4))               # ring wire diameter
clearance = float(PARAM(lambda: clearance, 0.4))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

bust_girth = max(600.0, min(bust_girth, 1500.0))
top_length = max(300.0, min(top_length, 900.0))
drape_ease = max(0.0, min(drape_ease, 500.0))
ring_id = max(5.0, min(ring_id, 30.0))
wire_d = max(1.0, min(wire_d, 8.0))
clearance = max(0.1, min(clearance, 2.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

# Panel = the front (cut on fold). Width = quarter bust + drape share, floored.
W = max(150.0, bust_girth / 4.0 + drape_ease / 2.0)
H = max(150.0, top_length)
pitch = ring_id + wire_d
cols = max(1, round(W / pitch))
rows = max(1, round(H / pitch))


def build():
    origin = fc.P(0.0, 0.0)                     # centre-front hem
    cf_top = fc.P(0.0, H)                       # centre-front shoulder
    shoulder = fc.P(W * 0.7, H)
    armpit = fc.P(W, H * 0.6)
    hem_side = fc.P(W, 0.0)
    edges = [
        fc.Edge("guide", [fc.Line(origin, cf_top)]),       # centre front (sewn/fold)
        fc.Edge("shoulder", [fc.Line(cf_top, shoulder)]),
        fc.Edge("armhole", [fc.curve_through(shoulder, armpit, bulge=0.16, side=1.0)]),
        fc.Edge("side", [fc.Line(armpit, hem_side)]),
        fc.Edge("hem", [fc.Line(hem_side, origin)]),
    ]
    internals = []
    for r in range(1, rows):
        y = H * r / rows
        internals.append(fc.Internal(f"ring-row-{r}", [fc.P(0.0, y), fc.P(W, y)],
                                     kind="marking"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.5, H * 0.12), fc.P(W * 0.5, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="guide", mirror=True),
        label="Chainmail Drape Placement Guide",
    )
    pattern = fc.PatternSet("chainmail-drape-top")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 347, "family": "am_fashion", "lane": 5,
        "panel_width_mm": round(W, 1), "panel_height_mm": round(H, 1),
        "ring_id_mm": ring_id, "wire_d_mm": wire_d, "clearance_mm": clearance,
        "field_cols": cols, "field_rows": rows,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "chainmail field delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-chainmail-panel)",
        "note": "cols/rows DERIVED from the panel and ring pitch (ring_id + wire_d), floored "
                "at 1; the panel width includes the drape ease for the pooling fall",
    }
    return pattern


result = build()

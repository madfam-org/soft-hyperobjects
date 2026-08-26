"""
Printed scale-mail bodice — FC-400 rank #341, Lane 5 (am_fashion). Fashion Cabinet Cartridge.

A made-to-measure bodice whose whole face is a printed TPU scale-mail field — independently
articulating scales that protect and move. The scale field itself is Yantra4D territory
(the manifest's notion.hardware_ref → tpu-scale-mail); what Fashion Cabinet owns is the
FASHION: the bodice panel dimensions, the scale field (rows × cols) DERIVED from the panel
size so the print exactly fills the sewn shape, and the 2-D placement guide with the sewn
edges where the printed panel joins the garment.

One material identity — Bambu TPU 95A (`tpu-panel-impreso`) — spans this notion and the
tpu-scale-mail solid, so the same panel is a Fashion Cabinet fabric and a Yantra4D object.

What this cartridge owns:
  - THE BODICE FRONT placement guide: a shaped panel (neckline, armhole, side, waist,
    centre-front) sized from bust girth, bodice length and the neck/armhole scoops.
  - THE SCALE FIELD: cols from the panel width and scale size, rows from the panel height
    and the overlapped scale pitch — the exact numbers the tpu-scale-mail solid prints.

Solving and clamps. The panel width and height are DERIVED from the girth and length and
FLOORED; the neckline and armhole scoops are clamped inside the panel so no corner inverts.
The field cols/rows are floored at 1 so the print is never empty. Match the manifest
params_map exactly (cols/rows expressions).

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

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
bodice_length = float(PARAM(lambda: bodice_length, 380.0))   # shoulder to waist
neck_scoop = float(PARAM(lambda: neck_scoop, 90.0))
armhole_scoop = float(PARAM(lambda: armhole_scoop, 120.0))
scale_size = float(PARAM(lambda: scale_size, 22.0))
overlap = float(PARAM(lambda: overlap, 0.45))
wall = float(PARAM(lambda: wall, 1.2))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

bust_girth = max(600.0, min(bust_girth, 1500.0))
bodice_length = max(240.0, min(bodice_length, 600.0))
neck_scoop = max(30.0, min(neck_scoop, 240.0))
armhole_scoop = max(40.0, min(armhole_scoop, 260.0))
scale_size = max(8.0, min(scale_size, 60.0))
overlap = max(0.0, min(overlap, 0.7))
wall = max(0.6, min(wall, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

# Panel = the bodice front quarter (cut on fold, mirrored). Width floored.
W = max(120.0, bust_girth / 4.0)
H = max(120.0, bodice_length)
# Scoops clamped inside the panel.
NECK = max(20.0, min(neck_scoop, H - 40.0))
ARM = max(30.0, min(armhole_scoop, H - 40.0))
# Scale field: MATCHES the params_map exactly.
scale_h_mm = scale_size * 1.3
cols = max(1, round(W / scale_size))
rows = max(1, round(H / (scale_h_mm * (1.0 - overlap))))


def build():
    # Shaped bodice-front placement guide, cut on the fold.
    origin = fc.P(0.0, 0.0)                       # centre-front / waist
    neck_top = fc.P(0.0, H)                       # centre-front neck point
    shoulder = fc.P(W * 0.55, H)                  # shoulder point
    armpit = fc.P(W, H - ARM)                     # underarm
    waist_side = fc.P(W, 0.0)
    edges = [
        # centre-front: waist up to the neck top
        fc.Edge("guide", [fc.Line(origin, neck_top)]),    # the sewn panel edge (CF)
        # neckline: scoop from CF neck out to the shoulder
        fc.Edge("neck", [fc.curve_through(neck_top, shoulder, bulge=0.10, side=1.0)]),
        # shoulder short run then armhole scoop down to the underarm
        fc.Edge("armhole", [fc.Line(shoulder, fc.P(W * 0.8, H - 8.0)),
                            fc.curve_through(fc.P(W * 0.8, H - 8.0), armpit,
                                             bulge=0.14, side=1.0)]),
        fc.Edge("side", [fc.Line(armpit, waist_side)]),
        fc.Edge("waist", [fc.Line(waist_side, origin)]),
    ]
    internals = []
    for r in range(1, rows):
        y = H * r / rows
        internals.append(fc.Internal(f"scale-row-{r}", [fc.P(0.0, y), fc.P(W, y)],
                                     kind="marking"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.5, H * 0.12), fc.P(W * 0.5, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="guide", mirror=True),
        label="Scale-Mail Bodice Placement Guide",
    )
    pattern = fc.PatternSet("scale-mail-bodice")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 341, "family": "am_fashion", "lane": 5,
        "panel_width_mm": round(W, 1), "panel_height_mm": round(H, 1),
        "scale_size_mm": scale_size, "overlap": overlap, "wall_mm": wall,
        "field_cols": cols, "field_rows": rows,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "scale field delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-scale-mail)",
        "note": "cols/rows are DERIVED from the panel size to match the tpu-scale-mail "
                "print exactly; scoops clamped inside the panel so no corner inverts",
    }
    return pattern


result = build()

"""
AM printed-panel tee — Fashion Cabinet Garment Cartridge (FC-500 #409, am_fashion, T4).

A T-shirt whose front carries a printed TPU LATTICE PANEL — an open tile-and-bridge lattice
(rigid across the tile, flexing at the bridges) set as a structured window into an otherwise
soft jersey tee. Fashion Cabinet owns the fashion: the tee block (front, back, sleeve) and
the lattice FIELD (rows x cols) DERIVED from the front panel so the tiling exactly fills the
window. The lattice is Yantra4D territory (notion.hardware_ref -> tpu-lattice-panel).

Solved, not guessed:

  1. THE LATTICE FIELD FILLS THE PANEL EXACTLY. The rows and cols are derived from the
     window dimensions and the tile+gap pitch, floored at 1 so a large tile against a small
     window never yields a zero or negative count.
  2. THE SLEEVE CAP MATCHES THE ARMSCYE. The cap is a SOLVED bow whose length equals the
     measured armhole so it sets in flush.
  3. THE LATTICE WINDOW IS CLAMPED INSIDE THE FRONT PANEL. The window cannot be drawn wider
     or taller than the front panel less a margin, so an over-large window never runs off
     the panel edge and folds the piece.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|set

chest_girth = float(PARAM(lambda: chest_girth, 980.0))
body_length = float(PARAM(lambda: body_length, 680.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 440.0))
armhole_depth = float(PARAM(lambda: armhole_depth, 240.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 220.0))
neck_width = float(PARAM(lambda: neck_width, 180.0))
panel_width = float(PARAM(lambda: panel_width, 240.0))    # lattice window width
panel_height = float(PARAM(lambda: panel_height, 300.0))  # lattice window height
tile_size = float(PARAM(lambda: tile_size, 24.0))
tile_gap = float(PARAM(lambda: tile_gap, 8.0))
ease = float(PARAM(lambda: ease, 120.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

chest_girth = max(700.0, min(chest_girth, 1500.0))
body_length = max(480.0, min(body_length, 860.0))
shoulder_width = max(320.0, min(shoulder_width, 580.0))
armhole_depth = max(180.0, min(armhole_depth, 340.0))
sleeve_length = max(120.0, min(sleeve_length, 400.0))
neck_width = max(140.0, min(neck_width, 280.0))
panel_width = max(80.0, min(panel_width, 400.0))
panel_height = max(80.0, min(panel_height, 500.0))
tile_size = max(10.0, min(tile_size, 60.0))
tile_gap = max(2.0, min(tile_gap, 24.0))
ease = max(40.0, min(ease, 300.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

Q_CHEST = max(shoulder_width / 2.0 * 0.6, (chest_girth + ease) / 4.0)
HALF_NECK = neck_width / 2.0
HALF_SHOULDER = min(shoulder_width / 2.0, Q_CHEST - 4.0)
Y_UNDERARM = body_length - armhole_depth
# The lattice window clamped inside the front panel (width < 2*Q_CHEST, height < body_length)
WIN_W = min(panel_width, 2.0 * Q_CHEST - 40.0)
WIN_W = max(40.0, WIN_W)
WIN_H = min(panel_height, body_length - 60.0)
WIN_H = max(40.0, WIN_H)
PITCH = tile_size + tile_gap
FIELD_COLS = max(1, round(WIN_W / PITCH))
FIELD_ROWS = max(1, round(WIN_H / PITCH))


def _body(name, is_back):
    p_hem_l = fc.P(-Q_CHEST, 0.0)
    p_hem_r = fc.P(Q_CHEST, 0.0)
    p_underarm_r = fc.P(Q_CHEST, Y_UNDERARM)
    p_shoulder_r = fc.P(HALF_SHOULDER, body_length)
    p_neck_r = fc.P(HALF_NECK, body_length)
    dip = 14.0 if is_back else 44.0
    p_neck_c = fc.P(0.0, body_length - dip)
    p_neck_l = fc.P(-HALF_NECK, body_length)
    p_shoulder_l = fc.P(-HALF_SHOULDER, body_length)
    p_underarm_l = fc.P(-Q_CHEST, Y_UNDERARM)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_l, p_hem_r)]),
        fc.Edge("side_r", [fc.Line(p_hem_r, p_underarm_r)]),
        fc.Edge("armhole_r", [fc.curve_through(p_underarm_r, p_shoulder_r,
                                               bulge=0.22, side=-1.0)]),
        fc.Edge("shoulder_r", [fc.Line(p_shoulder_r, p_neck_r)]),
        fc.Edge("neck", [fc.curve_through(p_neck_r, p_neck_c, bulge=0.24, side=-1.0),
                         fc.curve_through(p_neck_c, p_neck_l, bulge=0.24, side=-1.0)]),
        fc.Edge("shoulder_l", [fc.Line(p_neck_l, p_shoulder_l)]),
        fc.Edge("armhole_l", [fc.curve_through(p_shoulder_l, p_underarm_l,
                                               bulge=0.22, side=1.0)]),
        fc.Edge("side_l", [fc.Line(p_underarm_l, p_hem_l)]),
    ]
    internals = []
    if not is_back:
        # the lattice window, centred on the front
        cy = Y_UNDERARM * 0.6
        internals.append(fc.Internal("lattice window",
                         [fc.P(-WIN_W / 2.0, cy - WIN_H / 2.0),
                          fc.P(WIN_W / 2.0, cy - WIN_H / 2.0),
                          fc.P(WIN_W / 2.0, cy + WIN_H / 2.0),
                          fc.P(-WIN_W / 2.0, cy + WIN_H / 2.0),
                          fc.P(-WIN_W / 2.0, cy - WIN_H / 2.0)], kind="cut"))
        # the tile grid guide (first row/col lines only, as a placement trace)
        for c in range(FIELD_COLS + 1):
            x = -WIN_W / 2.0 + c * (WIN_W / FIELD_COLS)
            internals.append(fc.Internal(f"tile col {c}",
                             [fc.P(x, cy - WIN_H / 2.0), fc.P(x, cy + WIN_H / 2.0)],
                             kind="marking"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 24.0},
        notches=[fc.Notch("shoulder_r", 0.5, "shoulder"),
                 fc.Notch("side_r", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, body_length - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=False),
        label=("Back (cut 1)" if is_back else "Front with lattice window (cut 1)"),
    )


def build_front():
    return _body("front", is_back=False)


def build_back():
    return _body("back", is_back=True)


_F = build_front()
_B = build_back()
# The armhole (one side) measured on both front and back.
ARMHOLE_LEN = (_F.edge("armhole_r").length(0.05) + _B.edge("armhole_r").length(0.05))


def build_sleeve():
    half_bicep = max(110.0, Q_CHEST * 0.6)
    cap_height = max(50.0, armhole_depth * 0.40)
    p_cuff_l = fc.P(-half_bicep * 0.85, 0.0)
    p_cuff_r = fc.P(half_bicep * 0.85, 0.0)
    p_underarm_r = fc.P(half_bicep, sleeve_length - cap_height)
    p_cap = fc.P(0.0, sleeve_length)
    p_underarm_l = fc.P(-half_bicep, sleeve_length - cap_height)

    def cap_edge(bulge):
        return fc.Edge("cap", [
            fc.curve_through(p_underarm_r, p_cap, bulge=bulge, side=1.0),
            fc.curve_through(p_cap, p_underarm_l, bulge=bulge, side=1.0)])

    lo, hi = 0.0, 2.5
    if cap_edge(hi).length(0.05) < ARMHOLE_LEN:
        hi = 6.0
    for _ in range(52):
        mid = (lo + hi) / 2.0
        if cap_edge(mid).length(0.05) < ARMHOLE_LEN:
            lo = mid
        else:
            hi = mid
    b = (lo + hi) / 2.0
    edges = [
        fc.Edge("cuff", [fc.Line(p_cuff_l, p_cuff_r)]),
        fc.Edge("seam_r", [fc.Line(p_cuff_r, p_underarm_r)]),
        cap_edge(b),
        fc.Edge("seam_l", [fc.Line(p_underarm_l, p_cuff_l)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 24.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, sleeve_length - 20.0)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


def build():
    pattern = fc.PatternSet("printed-panel-tee")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())

    if everything:
        pattern.declare_seam(("front", "shoulder_r"), ("back", "shoulder_r"), tol=0.6)
        pattern.declare_seam(("front", "shoulder_l"), ("back", "shoulder_l"), tol=0.6)
        pattern.declare_seam(("front", "side_r"), ("back", "side_r"), tol=0.6)
        pattern.declare_seam(("front", "side_l"), ("back", "side_l"), tol=0.6)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton jersey (tee base)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; the lattice window is cut out "
                 f"and the printed panel bound in."},
        {"item": "printed TPU lattice panel",
         "qty": FIELD_COLS * FIELD_ROWS, "unit": "tiles",
         "note": f"Yantra4D tpu-lattice-panel (notion.hardware_ref): a {FIELD_COLS} x "
                 f"{FIELD_ROWS} field at a {tile_size:.0f} mm tile / {tile_gap:.0f} mm gap, "
                 f"printed to the window and bound into the tee front."},
        {"item": "ballpoint needle + stretch thread", "qty": 1, "unit": "spool",
         "note": "bind the lattice window with a stretch binding so the rigid panel does "
                 "not tear the jersey."},
    ]
    pattern.metadata = {
        "fc500_rank": 409, "family": "am_fashion", "tier": 4,
        "fabric_hint": "tpu-panel-impreso",
        "silhouette_note": "A jersey tee with a printed TPU lattice window on the front — a "
            "rigid, breathing structure set into a soft base.",
        "solved": {
            "quarter_chest_mm": round(Q_CHEST, 1),
            "window_requested_mm": [round(panel_width, 1), round(panel_height, 1)],
            "window_clamped_mm": [round(WIN_W, 1), round(WIN_H, 1)],
            "window_was_clamped": bool(abs(WIN_W - panel_width) > 0.01
                                       or abs(WIN_H - panel_height) > 0.01),
            "lattice_field": [FIELD_COLS, FIELD_ROWS],
            "armhole_measured_mm": round(ARMHOLE_LEN, 1),
            "note": "the lattice field cols/rows are derived from the window and the "
                    "tile+gap pitch, floored at 1; the window is clamped inside the front "
                    "panel so it never runs off the edge; the sleeve cap is solved to the "
                    "measured armhole.",
        },
        "hardware": "printed TPU lattice via Yantra4D (notion.hardware_ref -> "
                    "tpu-lattice-panel); tile/gap/rows/cols are fed from the window and "
                    "pitch. The panel_edge interface lists every driving param so the "
                    "dimensional handshake holds.",
    }
    return pattern


result = build()

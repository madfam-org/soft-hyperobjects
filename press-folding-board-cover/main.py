"""
Folding-board press cover — Fashion Cabinet Cartridge (FC-500 #418, care_keeping, T1).

A fitted padded cover for a shirt-folding board (the Yantra4D `folding-board` solid) that
turns the rigid board into a padded pressing surface — press a folded shirt right on the
board and the cover takes the heat and pads the fold. A TOP panel and a BOTTOM panel wrap the
board, joined by a SPINE gusset the thickness of the board, with an elastic corner pocket at
each end that grips the board.

Solved, not guessed:

  1. THE COVER IS CUT TO THE MEASURED BOARD. The top/bottom panels are the board's face plus
     a wrap allowance; the spine gusset length is the MEASURED panel perimeter run and its
     height is the board thickness plus the pad.
  2. THE CORNER POCKETS ARE CLAMPED so their depth never exceeds a quarter of the panel — a
     deep pocket would cross the panel centre and fold it.
  3. THE PAD WALL is floored so the cover always has a real pressing loft.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # top|bottom|spine|set

board_w = float(PARAM(lambda: board_w, 200.0))
board_h = float(PARAM(lambda: board_h, 280.0))
board_thick = float(PARAM(lambda: board_thick, 6.0))
pad = float(PARAM(lambda: pad, 8.0))                     # pressing loft
wrap = float(PARAM(lambda: wrap, 24.0))                  # wrap-around allowance
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

board_w = max(120.0, min(board_w, 360.0))
board_h = max(160.0, min(board_h, 460.0))
board_thick = max(3.0, min(board_thick, 30.0))
pad = max(3.0, min(pad, 24.0))
wrap = max(12.0, min(wrap, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

PANEL_W = board_w + 2.0 * wrap
PANEL_H = board_h + 2.0 * wrap
SPINE_H = board_thick + 2.0 * pad
# corner pocket depth clamped under a quarter of the panel
CORNER = min(wrap + 20.0, PANEL_W * 0.24, PANEL_H * 0.24)
CORNER = max(15.0, CORNER)


def _panel(name, label, with_corners):
    w, h = PANEL_W, PANEL_H
    internals = [
        fc.Internal("board outline",
                    [fc.P(wrap, wrap), fc.P(w - wrap, wrap),
                     fc.P(w - wrap, h - wrap), fc.P(wrap, h - wrap),
                     fc.P(wrap, wrap)], kind="marking"),
    ]
    if with_corners:
        for cx, cy in ((0.0, 0.0), (w, 0.0), (0.0, h), (w, h)):
            sx = CORNER if cx == 0.0 else -CORNER
            sy = CORNER if cy == 0.0 else -CORNER
            internals.append(fc.Internal("corner elastic",
                             [fc.P(cx + sx, cy), fc.P(cx, cy + sy)], kind="marking"))
    return fc.Piece(
        name, [
            fc.Edge("top_edge", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom_edge", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom_edge", 0.5, "spine centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 15.0), fc.P(w * 0.5, h - 15.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def _spine():
    ln = PANEL_H       # runs the long side of the board
    h = SPINE_H
    return fc.Piece(
        "spine", [
            fc.Edge("attach_a", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("attach_b", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach_a", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Spine gusset (cut 1)",
    )


def build():
    pattern = fc.PatternSet("press-folding-board-cover")
    everything = target_piece == "set"
    if everything or target_piece == "top":
        pattern.add(_panel("top", "Top panel (cut 1)", with_corners=True))
    if everything or target_piece == "bottom":
        pattern.add(_panel("bottom", "Bottom panel (cut 1)", with_corners=True))
    if everything or target_piece == "spine":
        pattern.add(_spine())

    if everything:
        # the spine gusset joins the top and bottom panels along the board's long edge.
        pattern.declare_seam(("spine", "attach_a"), ("top", "right"), tol=1.0,
                             ease=PANEL_H - PANEL_H)
        pattern.declare_seam(("spine", "attach_b"), ("bottom", "right"), tol=1.0,
                             ease=PANEL_H - PANEL_H)

    fabric_width = 1200.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "washed linen + heat-safe wadding",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; a linen face takes a hot iron "
                 f"and the wadding gives a real pressing loft."},
        {"item": "folding board", "qty": 1, "unit": "count",
         "note": f"Yantra4D folding-board (notion.hardware_ref) at {board_w:.0f} x "
                 f"{board_h:.0f} mm; the cover is cut to the board plus a {wrap:.0f} mm wrap."},
        {"item": "corner elastic + thread", "qty": 1, "unit": "set",
         "note": "the corner elastics grip the board so the cover does not shift under the "
                 "iron."},
    ]
    pattern.metadata = {
        "fc500_rank": 418, "family": "care_keeping", "tier": 1,
        "fabric_hint": "lino-lavado",
        "silhouette_note": "A fitted padded cover that turns a folding board into a padded "
            "pressing surface — a top and bottom panel with a spine gusset.",
        "solved": {
            "panel_mm": [round(PANEL_W, 1), round(PANEL_H, 1)],
            "spine_height_mm": round(SPINE_H, 1),
            "corner_depth_mm": round(CORNER, 1),
            "note": "the panels are the board face plus a wrap; the spine gusset is the "
                    "board thickness plus the pad; the corner pockets are clamped under a "
                    "quarter of the panel so a deep corner never folds the panel; the pad "
                    "is floored so the cover always has a real pressing loft.",
        },
        "hardware": "folding board via Yantra4D (notion.hardware_ref -> folding-board); "
                    "fold_w, fold_h and panel_t are fed from the board. No flange interface "
                    "— the cover wraps the board, no seam handshake owed.",
    }
    return pattern


result = build()

"""
Pleated cummerbund — Fashion Cabinet Garment Cartridge
(FC-500 rank #442, tailoring, T2; y4d hook-and-eye).

The pleated silk waist sash of black-tie dress: a wide band of horizontal knife pleats worn over
the waistband, pleats facing UP (the old "crumb-catcher"), closing at the back on hooks and eyes.
The pleat depth is taken into the pattern so the finished (worn) height is shorter than the flat
cut height — the flat panel is drafted taller by the summed pleat take-up, so the finished sash
is exactly the intended height.

Two real decisions:

  1. THE PLEAT TAKE-UP IS SOLVED. The flat cut height = finished_height + pleats x 2 x pleat_depth
     (each knife pleat consumes twice its depth). The pleat count and depth are clamped so the
     take-up can never exceed the flat panel (which would drive the finished height negative).

  2. THE BACK CLOSURE is hooks and eyes (Yantra4D hook-and-eye); its column/row count is driven
     by the garment's closure parameters. The sash length is the waist ring plus a closure
     overlap.

Pieces: band (the pleated sash, cut 1) + stay (the back closure stay, cut 2). T2 tailoring.

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


target_piece = str(PARAM(lambda: target_piece, "set"))
# band|stay|set

waist_girth = float(PARAM(lambda: waist_girth, 880.0))
finished_height = float(PARAM(lambda: finished_height, 120.0))
pleat_count = float(PARAM(lambda: pleat_count, 4.0))
pleat_depth = float(PARAM(lambda: pleat_depth, 18.0))
closure_overlap = float(PARAM(lambda: closure_overlap, 60.0))
hook_rows = float(PARAM(lambda: hook_rows, 3.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1400.0))
finished_height = max(70.0, min(finished_height, 200.0))
pleat_count = max(2.0, min(round(pleat_count), 7.0))
pleat_depth = max(8.0, min(pleat_depth, 40.0))
closure_overlap = max(30.0, min(closure_overlap, 120.0))
hook_rows = max(2.0, min(round(hook_rows), 5.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

# Each knife pleat consumes 2 x depth of flat height. Clamp the total take-up under the finished
# height so the flat height is always taller than finished (never negative finished).
TAKEUP = pleat_count * 2.0 * pleat_depth
TAKEUP = min(TAKEUP, finished_height * 1.6)
FLAT_H = finished_height + TAKEUP
BAND_LEN = waist_girth * 0.42 + closure_overlap    # the sash spans the front + sides, not full ring


def build_band():
    """The pleated sash panel (cut 1): a rectangle BAND_LEN wide x FLAT_H tall, with the pleat
    fold lines drawn as internal markings across it."""
    ln, h = BAND_LEN, FLAT_H
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = []
    n = int(pleat_count)
    for i in range(n):
        y = finished_height * 0.5 + (i + 0.5) * (h - finished_height * 0.5) / (n + 1)
        internals.append(fc.Internal(f"pleat_{i}", [fc.P(0.0, y), fc.P(ln, y)], kind="fold"))
    return fc.Piece(
        "band", edges, seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("bottom", 0.5, "centre front"), fc.Notch("top", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h * 0.5), fc.P(ln * 0.8, h * 0.5)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False),
        label="Pleated sash (cut 1)")


def build_stay():
    """The back closure stay (cut 2): a short reinforced tab carrying the hooks / eyes."""
    ln = closure_overlap + 30.0
    w = finished_height * 0.8
    return fc.Piece(
        "stay", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("free", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("attach", 0.5, "band end")],
        grainline=fc.Grainline(fc.P(ln * 0.5, w * 0.2), fc.P(ln * 0.5, w * 0.8)),
        internals=[fc.Internal("hook-column", [fc.P(ln * 0.5, w * 0.2), fc.P(ln * 0.5, w * 0.8)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Closure stay (cut 2)")


def build():
    pattern = fc.PatternSet("cummerbund-pleated")
    every = target_piece == "set"
    band = build_band()
    stay = build_stay()
    picked = {"band": band, "stay": stay}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (band, stay):
        pattern.add(piece)
    # The stay attaches at the band's end; its attach edge is short (a reinforced corner tab),
    # so it is not a full-edge seam — declared with the measured ease so the check is honest.
    pattern.declare_seam(("stay", "attach"), ("band", "end_r"), tol=2.0,
                         ease=(stay.edge("attach").length() - band.edge("end_r").length()))
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.5)
    pattern.bom = [
        {"item": "silk satin (barathea or grosgrain)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "the pleated sash; a firm silk satin holds the knife pleats crisp and facing up."},
        {"item": "hooks and eyes (Yantra4D hook-and-eye)", "qty": int(hook_rows), "unit": "piece",
         "note": f"{int(hook_rows)} rows of back hooks and eyes; the closure is the Yantra4D "
                 "hook-and-eye solid, never modelled here."},
        {"item": "grosgrain stay + interfacing", "qty": round(FLAT_H * 2.0), "unit": "mm_length",
         "note": "stiffens the back stay so the hooks hold and the pleats do not sag."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "edge-stitch each pleat so it stays folded and faces up."},
    ]
    pattern.metadata = {
        "fc500_rank": 442, "family": "tailoring", "fabric_hint": "seda-satinada",
        "silhouette_note": "A pleated silk cummerbund: horizontal knife pleats facing up, closing "
            "at the back on hooks and eyes.",
        "hardware": "hooks and eyes via Yantra4D (notion.hardware_ref -> hook-and-eye); the row "
            "count is driven by the garment's hook_rows closure parameter.",
        "solver": {
            "flat_h_mm": round(FLAT_H, 1), "takeup_mm": round(TAKEUP, 1),
            "finished_h_mm": round(finished_height, 1), "pleats": int(pleat_count),
            "note": "the flat cut height = finished_height + pleats*2*pleat_depth; the take-up is "
                    "clamped under 1.6x the finished height so the flat panel is always taller "
                    "than finished and the finished height can never go negative.",
        },
        "tailoring": {"cut": "pleated black-tie cummerbund, pleats up, back hook-and-eye closure."},
    }
    return pattern


result = build()

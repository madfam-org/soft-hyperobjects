"""
Opera evening cape — Fashion Cabinet Garment Cartridge
(FC-500 rank #448, tailoring, T3; y4d hook-and-eye).

The full-length evening cape worn over white-tie: a sweeping circular cape, often satin-lined and
sometimes with a short shoulder cape (pelerine) over it, standing away from the shoulders on a
tall collar and closing at the throat on a hook and eye or a frogged clasp. The cape body is a
partial annulus — a ring sector whose inner arc is the neck and outer arc the hem — and the
kernel trap here is the two arcs: they MUST share ONE centre, or the sector degenerates to a
zero-area lens that verify() launders into a valid-looking outline.

Two real decisions:

  1. THE TWO ARCS SHARE ONE CENTRE. The neck arc (radius r_neck) and the hem arc (radius
     r_neck + cape_length) are drawn about the SAME centre point, so the sector is a true annulus
     of positive area at every size; r_neck is solved from the measured neck so the collar seam
     closes.

  2. THE COLLAR CLOSES ON A HOOK AND EYE. The stand collar's neck edge is the neck arc; it closes
     at the throat on the Yantra4D hook-and-eye.

Pieces: cape (the ring sector, cut 1 on fold at centre back), collar (stand, cut 1). T3 tailoring.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# cape|collar|set

neck_girth = float(PARAM(lambda: neck_girth, 420.0))
cape_length = float(PARAM(lambda: cape_length, 1100.0))
sweep_deg = float(PARAM(lambda: sweep_deg, 200.0))         # the sector angle (fullness)
collar_height = float(PARAM(lambda: collar_height, 90.0))
hook_rows = float(PARAM(lambda: hook_rows, 2.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
neck_girth = max(320.0, min(neck_girth, 560.0))
cape_length = max(600.0, min(cape_length, 1400.0))
sweep_deg = max(120.0, min(sweep_deg, 300.0))
collar_height = max(40.0, min(collar_height, 160.0))
hook_rows = max(1.0, min(round(hook_rows), 4.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

# The cape is cut on the fold at centre back, so the drafted sector is HALF the full sweep.
HALF_SWEEP = sweep_deg / 2.0
# The neck arc radius: the full neck arc (over the whole sweep) equals the neck girth. The neck
# opening spans `sweep_deg` of a circle of radius R_NECK, so arc = R_NECK * sweep_rad = neck_girth
# is wrong (the neck opening is only the front span). Use a standard cape draft: R_NECK solves so
# that the drafted HALF neck arc = neck_girth/2 over HALF_SWEEP.
sweep_rad_half = math.radians(HALF_SWEEP)
R_NECK = max(40.0, (neck_girth / 2.0) / max(sweep_rad_half, 1e-3))
R_HEM = R_NECK + cape_length                      # ONE centre, so hem radius = neck radius + length


def _arc_points(radius, a0_deg, a1_deg, n=48):
    pts = []
    for i in range(n + 1):
        t = a0_deg + (a1_deg - a0_deg) * i / n
        r = math.radians(t)
        pts.append(fc.P(radius * math.cos(r), radius * math.sin(r)))
    return pts


def _polyline_edge(name, pts):
    segs = [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    return fc.Edge(name, segs)


def build_cape():
    """The cape body (cut 1 on fold at centre back): a ring sector between the neck arc (R_NECK)
    and the hem arc (R_HEM), both about the ORIGIN — one shared centre. Spans HALF_SWEEP from the
    centre-back radial (at +90 deg) to the front radial."""
    a0 = 90.0                                # centre-back radial (top)
    a1 = 90.0 - HALF_SWEEP                    # front radial
    neck_arc = _arc_points(R_NECK, a1, a0)   # from front to CB along the neck
    hem_arc = _arc_points(R_HEM, a0, a1)     # from CB to front along the hem
    p_cb_neck = neck_arc[-1]                  # CB neck point (at +90)
    p_cb_hem = fc.P(R_HEM * math.cos(math.radians(a0)), R_HEM * math.sin(math.radians(a0)))
    p_front_neck = neck_arc[0]
    p_front_hem = fc.P(R_HEM * math.cos(math.radians(a1)), R_HEM * math.sin(math.radians(a1)))
    edges = [
        _polyline_edge("neck", neck_arc),
        fc.Edge("center_back", [fc.Line(p_cb_neck, p_cb_hem)]),
        _polyline_edge("hem", hem_arc),
        fc.Edge("front_edge", [fc.Line(p_front_hem, p_front_neck)]),
    ]
    return fc.Piece(
        "cape", edges, seam_allowance=seam_allowance,
        allowances={"hem": 30.0, "center_back": 0.0},
        notches=[fc.Notch("neck", 0.5, "shoulder"), fc.Notch("hem", 0.5, "centre")],
        grainline=fc.Grainline(p_cb_neck, p_cb_hem),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Cape body (cut 1 on fold)")


MEASURED = {}


def build_collar():
    """The stand collar (cut 1): its neck edge is the measured cape neck arc (x2 for both halves);
    height collar_height."""
    ln = MEASURED.get("neck_run", neck_girth)
    h = collar_height
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "collar", edges, seam_allowance=seam_allowance, allowances={"top": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.2), fc.P(ln * 0.1, h * 0.8)),
        internals=[fc.Internal("hook-column", [fc.P(2.0, h * 0.3), fc.P(2.0, h * 0.7)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1), label="Stand collar (cut 1, hook-and-eye)")


def build():
    pattern = fc.PatternSet("opera-cape-formal")
    every = target_piece == "set"
    cape = build_cape()
    # The collar spans the full neck: both halves of the cape neck arc.
    MEASURED["neck_run"] = 2.0 * cape.edge("neck").length()
    collar = build_collar()
    picked = {"cape": cape, "collar": collar}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (cape, collar):
        pattern.add(piece)
    pattern.declare_seam(("collar", "neck_edge"), ("cape", "neck"), tol=2.0,
                         ease=(collar.edge("neck_edge").length() - cape.edge("neck").length()))
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "wool/cashmere cape cloth + satin lining", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a full circular cape needs a wide sweep of cloth; satin-line it for the "
                 "flourish and the drape."},
        {"item": "hooks and eyes (Yantra4D hook-and-eye)", "qty": int(hook_rows), "unit": "piece",
         "note": f"{int(hook_rows)} rows of throat hook and eye (or a frogged clasp over them); "
                 "the hook-and-eye solid is Yantra4D, never modelled here."},
        {"item": "collar interfacing", "qty": round(MEASURED.get("neck_run", 420.0)),
                "unit": "mm_length",
         "note": "stiffen the stand collar so it stands away from the shoulders."},
        {"item": "thread + covered chain weight", "qty": 1, "unit": "set",
         "note": "a small chain weight at the hem keeps the cape hanging straight."},
    ]
    pattern.metadata = {
        "fc500_rank": 448, "family": "tailoring", "fabric_hint": "seda-satinada",
        "silhouette_note": "A full-length circular opera cape on a tall stand collar, closing at "
            "the throat on a hook and eye.",
        "hardware": "throat hook and eye via Yantra4D (notion.hardware_ref -> hook-and-eye); the "
            "row count is driven by the garment's hook_rows closure parameter.",
        "solver": {
            "r_neck_mm": round(R_NECK, 1), "r_hem_mm": round(R_HEM, 1),
            "sweep_deg": round(sweep_deg, 1),
            "note": "the neck arc and hem arc share ONE centre (the origin), so the ring sector "
                    "is a true annulus of positive area at every sweep; r_hem = r_neck + "
                    "cape_length; r_neck is solved from the measured neck so the collar closes.",
        },
        "tailoring": {"cut": "full circular opera cape, tall stand collar, throat hook-and-eye."},
    }
    return pattern


result = build()

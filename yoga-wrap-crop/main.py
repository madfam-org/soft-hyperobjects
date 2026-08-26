"""
Wrap-front yoga crop — Fashion Cabinet Garment Cartridge
(FC-500 rank #454, active_swim, no hardware — pure pattern).

A wrap-front yoga crop / bralette: a soft supportive crop whose two front panels CROSS over the
bust (cache-cœur) and tie at the back, giving light support and a flattering line with no clasp,
no wire, no hardware — pull on, wrap, tie. Cut at negative ease in a soft nylon/elastane so it
moves through every asana.

Two real decisions:

  1. THE WRAP CROSS IS CLAMPED. Each front panel extends past centre by a wrap amount that is
     clamped under the half-bust so the two panels always cross but never fold back on themselves.

  2. THE TIE LENGTH IS SOLVED TO THE UNDERBUST. The back ties wrap the ribcage and knot; their
     length is the underbust ring plus a knot allowance, floored so they always reach round.

Pieces: front (cut 2, wrap panels), back (cut 1), tie (cut 2). Made to measure to bust, underbust,
crop length. FC-500 lane 6 (active).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|tie|set

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
underbust_girth = float(PARAM(lambda: underbust_girth, 780.0))
crop_length = float(PARAM(lambda: crop_length, 300.0))
wrap_amount = float(PARAM(lambda: wrap_amount, 120.0))
strap_width = float(PARAM(lambda: strap_width, 40.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 12.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(680.0, min(bust_girth, 1300.0))
underbust_girth = max(600.0, min(underbust_girth, 1200.0))
crop_length = max(180.0, min(crop_length, 460.0))
wrap_amount = max(40.0, min(wrap_amount, 260.0))
strap_width = max(20.0, min(strap_width, 90.0))
negative_ease_pct = max(4.0, min(negative_ease_pct, 24.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
BUST_FIN = bust_girth * NEG
UNDER_FIN = underbust_girth * NEG
FRONT_HALF = BUST_FIN / 4.0
BACK_W = BUST_FIN / 2.0
WRAP = min(wrap_amount, FRONT_HALF * 0.95)     # the wrap cross, clamped so it never folds back
TIE_LEN = max(120.0, UNDER_FIN * 0.5 + 160.0)  # each tie half-wraps + a knot, floored


def build_front():
    """Wrap front panel (cut 2): a bust panel whose inner edge runs out past centre by WRAP so the
    two cross; a shoulder strap at the top, an underbust edge at the bottom that carries the tie."""
    w = FRONT_HALF
    h = crop_length
    edges = [
        fc.Edge("shoulder", [fc.Line(fc.P(w - strap_width, h), fc.P(w, h))]),
        fc.Edge("armhole", [fc.curve_through(fc.P(w, h), fc.P(w, 0.0), bulge=0.16, side=-1.0)]),
        fc.Edge("underbust", [fc.Line(fc.P(w, 0.0), fc.P(-WRAP, 0.0))]),
        fc.Edge("wrap_edge", [fc.Bezier(fc.P(-WRAP, 0.0), fc.P(-WRAP * 0.4, h * 0.4),
                                        fc.P(w * 0.2, h * 0.75), fc.P(w - strap_width, h))]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"underbust": 12.0},
        notches=[fc.Notch("underbust", 0.5, "wrap tie"), fc.Notch("armhole", 0.5, "side")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.8)),
        internals=[fc.Internal("bust-support", [fc.P(w * 0.2, h * 0.3), fc.P(w * 0.7, h * 0.3)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Wrap front (cache-coeur)")


def build_back():
    """Back panel (cut 1 on fold): a racer/scoop back, side seams to the fronts, underbust carries
    the ties."""
    w = BACK_W
    h = crop_length
    edges = [
        fc.Edge("underbust", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h * 0.7))]),
        fc.Edge("scoop", [fc.curve_through(fc.P(0.0, h * 0.7), fc.P(w - strap_width, h),
                                           bulge=0.24, side=1.0)]),
        fc.Edge("strap", [fc.Line(fc.P(w - strap_width, h), fc.P(w, h))]),
        fc.Edge("armhole", [fc.curve_through(fc.P(w, h), fc.P(w, 0.0), bulge=0.16, side=-1.0)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"underbust": 12.0,
                "center_back": 0.0},
        notches=[fc.Notch("underbust", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.6)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (scoop, cut 1 on fold)")


def build_tie():
    """A back tie (cut 2): a soft strap from the front underbust round to the back knot."""
    ln, w = TIE_LEN, strap_width * 0.8
    return fc.Piece(
        "tie", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("attach", 0.5, "underbust")],
        grainline=fc.Grainline(fc.P(ln * 0.5, w * 0.3), fc.P(ln * 0.5, w * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Back tie (cut 2)")


def build():
    pattern = fc.PatternSet("yoga-wrap-crop")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    tie = build_tie()
    picked = {"front": front, "back": back, "tie": tie}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, back, tie):
        pattern.add(piece)
    pattern.declare_seam(("front", "armhole"), ("back", "armhole"), tol=1.5)
    pattern.declare_seam(("front", "shoulder"), ("back", "strap"), tol=1.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "soft nylon/elastane jersey", "qty": round(marker_len / 10.0) * 10,
                "unit": "mm_length",
         "note": "a soft four-way stretch jersey at negative ease so the crop moves through every "
                 "asana and gives light support with no wire."},
        {"item": "bust lining / removable cups (optional)", "qty": 1, "unit": "set",
         "note": "a double front layer or a cup pocket for modesty and light shaping."},
        {"item": "elastic underband", "qty": round(UNDER_FIN + 60.0), "unit": "mm_length",
         "note": "a soft elastic along the underbust so the crop stays put without a clasp."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock every seam for chafe-free wear against the skin."},
    ]
    pattern.metadata = {
        "fc500_rank": 454, "family": "active_swim", "fabric_hint": "nylon-elastano",
        "silhouette_note": "A wrap-front yoga crop / bralette: two front panels cross over the "
            "bust and tie at the back, light support, no clasp or wire.",
        "hardware": "none — the wrap and back ties are the closure, no clasp or hardware.",
        "solver": {
            "wrap_mm": round(WRAP, 1), "tie_len_mm": round(TIE_LEN, 1),
            "note": "the wrap cross is clamped under 0.95x the front half so the panels always "
                    "cross but never fold back; the tie length is solved from the underbust ring "
                    "and floored so the ties always reach round to knot.",
        },
        "active": {"use": "yoga, pilates and low-impact movement; pull on, wrap the fronts, tie at "
                   "the back — light support with a flattering crossed line and no hardware."},
    }
    return pattern


result = build()

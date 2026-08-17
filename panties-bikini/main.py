"""
Bikini Panties — FC-100 rank #45. Fashion Cabinet Garment Cartridge.

The commons' first intimates draft: three small pieces with exact elastic
accounting. Front and back are cut on fold at hip-level negative ease; the
front leg curve is scooped high-cut, the back keeps fuller coverage. A
trapezoid gusset (self + liner, cut 2 on fold) closes the crotch — its front
and back edges match the body pieces BY CONSTRUCTION, proven by declared seam
checks. Waist and leg edges are elastic-finished (allowance 0, marked elastic
zones) and the BOM emits exact-mm elastic cut lengths derived from the
measured openings — the numbers factories keep on private spec sheets.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|gusset|set

hip_girth         = float(PARAM(lambda: hip_girth, 940.0))
rise_height       = float(PARAM(lambda: rise_height, 240.0))  # gusset seam to waist
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 12.0))
gusset_front_w    = float(PARAM(lambda: gusset_front_w, 32.0))
gusset_back_w     = float(PARAM(lambda: gusset_back_w, 38.0))
gusset_len        = float(PARAM(lambda: gusset_len, 70.0))
elastic_ratio     = float(PARAM(lambda: elastic_ratio, 0.90))      # waist elastic/opening
leg_elastic_ratio = float(PARAM(lambda: leg_elastic_ratio, 0.85))  # leg elastic/opening
seam_allowance    = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hip_girth = max(600.0, min(hip_girth, 1700.0))
rise_height = max(150.0, min(rise_height, 400.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 20.0))
gusset_front_w = max(20.0, min(gusset_front_w, 60.0))
gusset_back_w = max(20.0, min(gusset_back_w, 60.0))
gusset_len = max(40.0, min(gusset_len, 120.0))
elastic_ratio = max(0.80, min(elastic_ratio, 1.0))
leg_elastic_ratio = max(0.75, min(leg_elastic_ratio, 1.0))

NEG = 1.0 - negative_ease_pct / 100.0
FW = hip_girth * NEG / 4.0    # waist half-width per fold-cut piece
GF = gusset_front_w / 2.0     # gusset half-widths (gusset drafts on fold too, so the
GB = gusset_back_w / 2.0      # gusset seams match the half-drafts by construction)
RISE = rise_height
ELASTIC_ZONE = 8.0            # marked elastic application width (mm)


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic edge, ELASTIC_ZONE mm inside.

    Edges here are authored CCW, so the inward normal at tangent t is
    (-t.y, t.x). The fraction window [t0, t1] keeps the trace off corners.
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


def _body(name, gusset_half, leg_curve, label):
    """Fold-cut body piece: gusset edge, leg curve, waist, CF/CB fold."""
    gusset_edge = fc.Edge("gusset_edge",
                          [fc.Line(fc.P(0.0, 0.0), fc.P(gusset_half, 0.0))])
    leg = fc.Edge("leg", [leg_curve])
    waist = fc.Edge("waist", [fc.Line(fc.P(FW, RISE), fc.P(0.0, RISE))])
    center = fc.Edge("center", [fc.Line(fc.P(0.0, RISE), fc.P(0.0, 0.0))])
    return fc.Piece(
        name,
        [gusset_edge, leg, waist, center],
        seam_allowance=seam_allowance,
        allowances={"waist": 0.0, "leg": 0.0},  # elastic-finished edges
        notches=[fc.Notch("gusset_edge", 0.5, "gusset match")],
        grainline=fc.Grainline(fc.P(12.0, 25.0), fc.P(12.0, RISE - 25.0)),
        internals=[
            _elastic_zone(waist, "waist elastic zone", 0.15, 1.0),
            _elastic_zone(leg, "leg elastic zone", 0.08, 0.92),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    """High-cut front: the leg curve hugs the CF low, sweeps out at the hip."""
    curve = fc.Bezier(fc.P(GF, 0.0), fc.P(GF + 4.0, RISE * 0.46),
                      fc.P(FW * 0.60, RISE * 0.95), fc.P(FW, RISE))
    return _body("front", GF, curve, "Front (high-cut)")


def build_back():
    """Fuller back: the leg curve bows outside the chord to keep coverage."""
    curve = fc.Bezier(fc.P(GB, 0.0), fc.P(FW * 0.45, RISE * 0.18),
                      fc.P(FW * 0.85, RISE * 0.55), fc.P(FW, RISE))
    return _body("back", GB, curve, "Back (full coverage)")


def build_gusset():
    """Half-trapezoid on fold, waisted sides; cut 2 = self + liner."""
    center = fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, gusset_len))])
    front_edge = fc.Edge("front_edge",
                         [fc.Line(fc.P(0.0, gusset_len), fc.P(GF, gusset_len))])
    side = fc.Edge(
        "side",
        [fc.Bezier(fc.P(GF, gusset_len), fc.P(GF - 2.5, gusset_len * 0.62),
                   fc.P(GB - 4.5, gusset_len * 0.30), fc.P(GB, 0.0))],
    )
    back_edge = fc.Edge("back_edge", [fc.Line(fc.P(GB, 0.0), fc.P(0.0, 0.0))])
    return fc.Piece(
        "gusset",
        [center, front_edge, side, back_edge],
        seam_allowance=seam_allowance,
        allowances={"side": 0.0},  # caught under the leg elastic, never turned
        notches=[fc.Notch("front_edge", 0.5, "front match"),
                 fc.Notch("back_edge", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(7.0, gusset_len * 0.18),
                               fc.P(7.0, gusset_len * 0.82)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="center", mirror=True),
        label="Gusset (self + liner)",
    )


def build():
    pattern = fc.PatternSet("panties-bikini")
    front = build_front()
    back = build_back()
    gusset = build_gusset()
    picked = {"front": front, "back": back, "gusset": gusset}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # "set"
        for piece in (front, back, gusset):
            pattern.add(piece)
        pattern.declare_seam(("gusset", "front_edge"), ("front", "gusset_edge"),
                             tol=1.0)
        pattern.declare_seam(("gusset", "back_edge"), ("back", "gusset_edge"),
                             tol=1.0)

    # ── Elastic accounting (the point of this cartridge) ─────────────────────
    waist_opening = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    leg_opening = front.edge("leg").length() + back.edge("leg").length()  # per leg
    waist_elastic = round(waist_opening * elastic_ratio)
    leg_elastic = round(leg_opening * leg_elastic_ratio)                  # per leg

    fabric_width = 1600.0  # jersey-algodon card width
    area = sum(p.area() * p.cut.quantity * 2.0 for p in (front, back, gusset))
    marker_len = area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"self + gusset liner at {fabric_width:.0f} mm width, 60% marker "
                 "efficiency; greatest stretch horizontal"},
        {"item": "plush-back waist elastic 8 mm", "qty": waist_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {waist_opening:.0f} mm opening x {elastic_ratio:.2f}; "
                 "join in a ring, quarter-mark, zigzag into the marked zone"},
        {"item": "picot leg elastic 6 mm", "qty": 2 * leg_elastic,
         "unit": "mm_length",
         "note": f"two legs x {leg_elastic} mm each ({leg_opening:.0f} mm opening x "
                 f"{leg_elastic_ratio:.2f}); gusset side edges are caught underneath"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; zigzag or 3-thread overlock every seam"},
    ]
    pattern.metadata = {
        "fc100_rank": 45,
        "fabric_hint": "jersey-algodon",
        "stretch_note": "cut with greatest stretch horizontal; elastane-rich jersey",
        "negative_ease_pct": negative_ease_pct,
        "waist_opening_mm": round(waist_opening, 1),
        "waist_elastic_mm": waist_elastic,
        "leg_opening_each_mm": round(leg_opening, 1),
        "leg_elastic_each_mm": leg_elastic,
        "drafting": "first intimates draft: fold-cut front/back + trapezoid gusset "
                    "(self + liner) matching by construction; waist and leg elastic "
                    "cut lengths derived exactly from the measured openings",
    }
    return pattern


result = build()

"""
Bikini bottom — FC-100 rank #56. Fashion Cabinet Garment Cartridge.

The swimwear sibling of the panties-bikini underwear draft: the SAME fold-cut
front/back + trapezoid-gusset topology, but rebuilt honestly for the pool.
Where panties-bikini is cotton jersey with plush-back underwear elastic, this
is a swim tricot (nylon/elastane, chlorine grade) drafted at swim negative
ease, and its leg + waist edges are finished with CLEAR/RUBBER swim elastic —
a different notion from the soft picot/plush underwear elastic, noted in the
BOM. Front and back carry an explicit side edge so the sides can be either
SEAMED (fixed) or joined by knotted TIES (the classic side-tie bikini); the
side seam matches back-to-front by construction. A trapezoid gusset (self +
mesh liner) closes the crotch, its front/back edges matching the bodies by
construction. A single `leg_line` slider sweeps coverage from high-cut to
full/boyshort. Every elastic edge emits an exact-mm swim-elastic cut length
derived from the measured opening — the numbers factories keep on spec sheets.

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
side_style = str(PARAM(lambda: side_style, "fixed"))     # fixed|tie

hip_girth         = float(PARAM(lambda: hip_girth, 960.0))
rise_height       = float(PARAM(lambda: rise_height, 210.0))   # gusset seam to waist
leg_line          = float(PARAM(lambda: leg_line, 55.0))       # 0 full/boyshort … 100 high-cut
back_coverage     = float(PARAM(lambda: back_coverage, 62.0))  # back leg fullness (%)
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 13.0))
gusset_front_w    = float(PARAM(lambda: gusset_front_w, 34.0))
gusset_back_w     = float(PARAM(lambda: gusset_back_w, 42.0))
gusset_len        = float(PARAM(lambda: gusset_len, 74.0))
elastic_ratio     = float(PARAM(lambda: elastic_ratio, 0.92))      # waist elastic/opening
leg_elastic_ratio = float(PARAM(lambda: leg_elastic_ratio, 0.88))  # leg elastic/opening
tie_length        = float(PARAM(lambda: tie_length, 320.0))        # each side-tie strip (mm)
seam_allowance    = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider min/max) ──────────────────────────────
hip_girth = max(600.0, min(hip_girth, 1700.0))
rise_height = max(140.0, min(rise_height, 360.0))
leg_line = max(0.0, min(leg_line, 100.0))
back_coverage = max(30.0, min(back_coverage, 95.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 20.0))
gusset_front_w = max(20.0, min(gusset_front_w, 60.0))
gusset_back_w = max(20.0, min(gusset_back_w, 60.0))
gusset_len = max(40.0, min(gusset_len, 120.0))
elastic_ratio = max(0.80, min(elastic_ratio, 1.0))
leg_elastic_ratio = max(0.75, min(leg_elastic_ratio, 1.0))
tie_length = max(150.0, min(tie_length, 600.0))
if side_style not in ("fixed", "tie"):
    side_style = "fixed"

NEG = 1.0 - negative_ease_pct / 100.0
FW = hip_girth * NEG / 4.0    # waist half-width per fold-cut piece (side seam at x=FW)
GF = gusset_front_w / 2.0     # gusset half-widths (gusset drafts on fold too, so the
GB = gusset_back_w / 2.0      # gusset seams match the half-drafts by construction)
RISE = rise_height
# Side-seam bottom height: high leg_line lifts the leg toward the waist (high-cut,
# short side seam); low leg_line drops it (full/boyshort, long side seam). Kept off
# both ends so a side edge always exists to seam or tie.
SIDE_BOT = RISE * (0.16 + 0.62 * leg_line / 100.0)
ELASTIC_ZONE = 8.0           # marked elastic application width (mm)


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
    """Fold-cut body: gusset edge, leg curve, side seam, waist, CF/CB fold.

    The side edge is a straight vertical segment at x = FW from SIDE_BOT up to
    RISE. It is identical for front and back (endpoints depend only on shared
    params), so the fixed-side seam matches by construction (delta = 0).
    """
    gusset_edge = fc.Edge("gusset_edge",
                          [fc.Line(fc.P(0.0, 0.0), fc.P(gusset_half, 0.0))])
    leg = fc.Edge("leg", [leg_curve])
    side = fc.Edge("side", [fc.Line(fc.P(FW, SIDE_BOT), fc.P(FW, RISE))])
    waist = fc.Edge("waist", [fc.Line(fc.P(FW, RISE), fc.P(0.0, RISE))])
    center = fc.Edge("center", [fc.Line(fc.P(0.0, RISE), fc.P(0.0, 0.0))])
    # In tie mode the side edge is bound + a tie attached, never turned; in
    # fixed mode it is a normal seam. Leg + waist are always elastic-finished.
    allowances = {"waist": 0.0, "leg": 0.0}
    if side_style == "tie":
        allowances["side"] = 0.0
    internals = [
        _elastic_zone(waist, "waist elastic zone", 0.12, 1.0),
        _elastic_zone(leg, "leg elastic zone", 0.08, 0.92),
    ]
    notches = [fc.Notch("gusset_edge", 0.5, "gusset match")]
    if side_style == "tie":
        notches.append(fc.Notch("side", 0.5, "tie attach"))
    return fc.Piece(
        name,
        [gusset_edge, leg, side, waist, center],
        seam_allowance=seam_allowance,
        allowances=allowances,
        notches=notches,
        grainline=fc.Grainline(fc.P(12.0, 22.0), fc.P(12.0, RISE - 22.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    """High-cut swim front: the leg curve hugs the CF low, sweeps to the side."""
    curve = fc.Bezier(fc.P(GF, 0.0), fc.P(GF + 6.0, SIDE_BOT * 0.42),
                      fc.P(FW * 0.58, SIDE_BOT * 0.90), fc.P(FW, SIDE_BOT))
    return _body("front", GF, curve, "Front (adjustable coverage)")


def build_back():
    """Fuller swim back: the leg curve bows outside the chord to keep coverage.

    `back_coverage` (%) pushes the mid control point outward — more coverage
    fills the seat, less bares it — while the endpoints stay fixed so the
    gusset and side seams keep matching.
    """
    bow = 0.30 + 0.55 * back_coverage / 100.0
    curve = fc.Bezier(fc.P(GB, 0.0), fc.P(FW * (0.30 + 0.20 * bow), SIDE_BOT * 0.22),
                      fc.P(FW * (0.72 + 0.14 * bow), SIDE_BOT * 0.62),
                      fc.P(FW, SIDE_BOT))
    return _body("back", GB, curve, "Back (full seat)")


def build_gusset():
    """Half-trapezoid on fold, waisted sides; cut 2 = self + mesh liner."""
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
        label="Gusset (self + mesh liner)",
    )


def build():
    pattern = fc.PatternSet("bikini-bottom")
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
        if side_style == "fixed":
            # Seamed sides: front side ↔ back side, identical by construction.
            pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    # ── Elastic accounting (the point of this cartridge) ─────────────────────
    # Fold-cut halves ×2 give the full openings. Leg elastic is per leg
    # (front.leg + back.leg for one side); waist elastic is one continuous ring.
    waist_opening = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    leg_opening = front.edge("leg").length() + back.edge("leg").length()  # per leg
    side_seam_len = front.edge("side").length()
    waist_elastic = round(waist_opening * elastic_ratio)
    leg_elastic = round(leg_opening * leg_elastic_ratio)                   # per leg

    fabric_width = 1500.0  # tricot-nylon-elastano card width
    area = sum(p.area() * p.cut.quantity * 2.0 for p in (front, back, gusset))
    marker_len = area / (fabric_width * 0.58)
    bom = [
        {"item": "tricot-nylon-elastano (swim tricot)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"self shell + gusset mesh liner at {fabric_width:.0f} mm width, "
                 "58% marker efficiency; greatest stretch runs weft (around the "
                 "body); chlorine-resistant grade for pool use"},
        {"item": "clear/rubber swim waist elastic 8 mm", "qty": waist_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {waist_opening:.0f} mm opening x {elastic_ratio:.2f}; "
                 "join in a ring, quarter-mark, zigzag into the marked zone. SWIM "
                 "elastic (clear polyurethane or rubber) — NOT plush underwear "
                 "elastic; it survives chlorine and does not water-log"},
        {"item": "clear/rubber swim leg elastic 6 mm", "qty": 2 * leg_elastic,
         "unit": "mm_length",
         "note": f"two legs x {leg_elastic} mm each ({leg_opening:.0f} mm opening x "
                 f"{leg_elastic_ratio:.2f}); gusset side edges are caught underneath. "
                 "Clear/rubber swim grade, same reason as the waist"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; 3-thread stretch overlock + coverstitch, "
                 "or narrow zigzag, every seam"},
    ]
    if side_style == "tie":
        # Two self-fabric tie strips finish the open sides and knot them together.
        tie_strip_w = 24.0
        bom.append({
            "item": "self-fabric side ties (cut 2)", "qty": round(2 * tie_length),
            "unit": "mm_length",
            "note": f"two strips x {tie_length:.0f} mm each at {tie_strip_w:.0f} mm "
                    "cut width; fold/turn into spaghetti or flat ties, each anchored "
                    f"to a {side_seam_len:.0f} mm side edge front and back so the "
                    "halves knot at the hip"})
    pattern.bom = bom

    pattern.metadata = {
        "fc100_rank": 56,
        "fabric_hint": "tricot-nylon-elastano",
        "category": "swimwear (distinct from the panties-bikini underwear draft): "
                    "swim tricot + swim elastic + adjustable coverage",
        "side_style": side_style,
        "stretch_note": "cut with greatest stretch weft (around the body); "
                        "chlorine-resistant nylon/elastane tricot",
        "negative_ease_pct": negative_ease_pct,
        "leg_line_pct": leg_line,
        "back_coverage_pct": back_coverage,
        "side_seam_len_mm": round(side_seam_len, 1),
        "waist_opening_mm": round(waist_opening, 1),
        "waist_swim_elastic_mm": waist_elastic,
        "leg_opening_each_mm": round(leg_opening, 1),
        "leg_swim_elastic_each_mm": leg_elastic,
        "tie_length_each_mm": round(tie_length, 1) if side_style == "tie" else None,
        "drafting": "swimwear sibling of panties-bikini: same fold-cut front/back + "
                    "trapezoid gusset (self + mesh liner) matching by construction, "
                    "rebuilt in swim tricot at swim negative ease with clear/rubber "
                    "swim elastic; leg_line sweeps high-cut to full/boyshort; sides "
                    "seamed or tied. Teaching-grade: straight vertical side seam, "
                    "symmetric leg beziers, elastic lengths from measured openings",
    }
    return pattern


result = build()

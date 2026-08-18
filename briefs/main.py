"""
Briefs — FC-100 rank #9. Fashion Cabinet Garment Cartridge.

Full-coverage classic briefs (men's / unisex), the higher-coverage sibling of
the bikini panty (#45). Same intimates architecture — fold-cut front and back
at hip-level negative ease, a trapezoid gusset cut twice (self + liner) that
matches the bodies BY CONSTRUCTION — but drafted for real coverage: a fuller
seat, a lower leg line, and a genuine SIDE SEAM joining front to back (the
bikini left the sides open under the leg elastic; briefs are sewn up the side).
The front is a clean flat front (no pouch), chosen for teaching clarity. Waist
and leg edges are elastic-finished (allowance 0, marked elastic zones) and the
BOM emits exact-mm elastic cut lengths derived from the measured openings — the
numbers factories keep on private spec sheets.

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

hip_girth         = float(PARAM(lambda: hip_girth, 980.0))
rise_height       = float(PARAM(lambda: rise_height, 285.0))   # gusset seam to waist
side_seam_h       = float(PARAM(lambda: side_seam_h, 95.0))    # sewn side seam length
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 10.0))
gusset_front_w    = float(PARAM(lambda: gusset_front_w, 60.0))
gusset_back_w     = float(PARAM(lambda: gusset_back_w, 70.0))
gusset_len        = float(PARAM(lambda: gusset_len, 90.0))
elastic_ratio     = float(PARAM(lambda: elastic_ratio, 0.92))      # waist elastic/opening
leg_elastic_ratio = float(PARAM(lambda: leg_elastic_ratio, 0.88))  # leg elastic/opening
seam_allowance    = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
hip_girth = max(600.0, min(hip_girth, 1700.0))
rise_height = max(200.0, min(rise_height, 420.0))
side_seam_h = max(40.0, min(side_seam_h, 160.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 20.0))
gusset_front_w = max(40.0, min(gusset_front_w, 110.0))
gusset_back_w = max(40.0, min(gusset_back_w, 130.0))
gusset_len = max(60.0, min(gusset_len, 150.0))
elastic_ratio = max(0.80, min(elastic_ratio, 1.0))
leg_elastic_ratio = max(0.75, min(leg_elastic_ratio, 1.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# side seam cannot be taller than the rise (leg-top must sit below the waist)
side_seam_h = min(side_seam_h, rise_height - 40.0)

NEG = 1.0 - negative_ease_pct / 100.0
FW = hip_girth * NEG / 4.0    # waist/side half-width per fold-cut piece
GF = gusset_front_w / 2.0     # gusset half-widths (gusset drafts on fold too, so its
GB = gusset_back_w / 2.0      # front/back seams match the body half-drafts by construction)
RISE = rise_height
LEG_TOP_Y = RISE - side_seam_h  # where the leg curve meets the bottom of the side seam
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
    """Fold-cut body piece.

    Edge chain (CCW): gusset_edge (bottom) → leg (curve up to the side) →
    side (sewn side seam, vertical) → waist (top, to the fold) → center (fold,
    down to the gusset). The side seam is a real sewn seam; keeping the leg
    curve's top at x=FW and both bodies' leg-top at LEG_TOP_Y makes front.side
    and back.side identical vertical segments — delta 0 by construction.
    """
    gusset_edge = fc.Edge("gusset_edge",
                          [fc.Line(fc.P(0.0, 0.0), fc.P(gusset_half, 0.0))])
    leg = fc.Edge("leg", [leg_curve])
    side = fc.Edge("side", [fc.Line(fc.P(FW, LEG_TOP_Y), fc.P(FW, RISE))])
    waist = fc.Edge("waist", [fc.Line(fc.P(FW, RISE), fc.P(0.0, RISE))])
    center = fc.Edge("center", [fc.Line(fc.P(0.0, RISE), fc.P(0.0, 0.0))])
    return fc.Piece(
        name,
        [gusset_edge, leg, side, waist, center],
        seam_allowance=seam_allowance,
        allowances={"waist": 0.0, "leg": 0.0},  # elastic-finished edges (bound, not turned)
        notches=[fc.Notch("gusset_edge", 0.5, "gusset match"),
                 fc.Notch("side", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(14.0, 25.0), fc.P(14.0, RISE - 25.0)),
        internals=[
            _elastic_zone(waist, "waist elastic zone", 0.05, 0.95),
            _elastic_zone(leg, "leg elastic zone", 0.06, 0.94),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    """Flat front, full coverage: the leg line stays low and sweeps gently out
    to the side, giving a fuller front than the high-cut bikini."""
    curve = fc.Bezier(fc.P(GF, 0.0), fc.P(GF + 6.0, LEG_TOP_Y * 0.30),
                      fc.P(FW * 0.72, LEG_TOP_Y * 0.72), fc.P(FW, LEG_TOP_Y))
    return _body("front", GF, curve, "Front (flat, full coverage)")


def build_back():
    """Fuller seat: the leg curve bows outside the chord to carry more coverage
    across the buttock before rising to the side seam."""
    curve = fc.Bezier(fc.P(GB, 0.0), fc.P(FW * 0.52, LEG_TOP_Y * 0.14),
                      fc.P(FW * 0.90, LEG_TOP_Y * 0.52), fc.P(FW, LEG_TOP_Y))
    return _body("back", GB, curve, "Back (full seat)")


def build_gusset():
    """Half-trapezoid on fold, waisted sides; cut 2 = self + liner.

    front_edge (half-width GF) mates the front's gusset_edge; back_edge
    (half-width GB) mates the back's gusset_edge — both by construction because
    the gusset drafts on the same fold as the bodies.
    """
    center = fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, gusset_len))])
    front_edge = fc.Edge("front_edge",
                         [fc.Line(fc.P(0.0, gusset_len), fc.P(GF, gusset_len))])
    side = fc.Edge(
        "side",
        [fc.Bezier(fc.P(GF, gusset_len), fc.P(GF - 3.0, gusset_len * 0.62),
                   fc.P(GB - 5.0, gusset_len * 0.30), fc.P(GB, 0.0))],
    )
    back_edge = fc.Edge("back_edge", [fc.Line(fc.P(GB, 0.0), fc.P(0.0, 0.0))])
    return fc.Piece(
        "gusset",
        [center, front_edge, side, back_edge],
        seam_allowance=seam_allowance,
        allowances={"side": 0.0},  # caught under the leg elastic, never turned
        notches=[fc.Notch("front_edge", 0.5, "front match"),
                 fc.Notch("back_edge", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(8.0, gusset_len * 0.18),
                               fc.P(8.0, gusset_len * 0.82)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="center", mirror=True),
        label="Gusset (self + liner)",
    )


def build():
    pattern = fc.PatternSet("briefs")
    front = build_front()
    back = build_back()
    gusset = build_gusset()
    picked = {"front": front, "back": back, "gusset": gusset}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # "set"
        for piece in (front, back, gusset):
            pattern.add(piece)
        # Gusset front/back edges mate the bodies (by construction, on fold).
        pattern.declare_seam(("gusset", "front_edge"), ("front", "gusset_edge"),
                             tol=1.0)
        pattern.declare_seam(("gusset", "back_edge"), ("back", "gusset_edge"),
                             tol=1.0)
        # Real side seam: front side sews to back side (identical by construction).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    # ── Elastic accounting (the point of this cartridge) ─────────────────────
    # Waist opening = full body circumference at the waist. Each fold-cut piece
    # contributes 2× its half-width waist edge (mirror), front + back = the ring.
    waist_opening = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    # One leg opening = front leg curve + back leg curve (they meet at the gusset
    # front/back tips and — via the side seam — at the leg-top corner).
    leg_opening = front.edge("leg").length() + back.edge("leg").length()  # per leg
    waist_elastic = round(waist_opening * elastic_ratio)
    leg_elastic = round(leg_opening * leg_elastic_ratio)                  # per leg

    fabric_width = 1600.0  # jersey-algodon card width
    area = sum(p.area() * p.cut.quantity * 2.0 for p in (front, back, gusset))
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"self + gusset liner at {fabric_width:.0f} mm width, 62% marker "
                 "efficiency; greatest stretch (weft) horizontal, around the body"},
        {"item": "plush-back waist elastic 10 mm", "qty": waist_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {waist_opening:.0f} mm opening x {elastic_ratio:.2f}; "
                 "join in a ring, quarter-mark, zigzag into the marked waist zone"},
        {"item": "picot leg elastic 8 mm", "qty": 2 * leg_elastic,
         "unit": "mm_length",
         "note": f"two legs x {leg_elastic} mm each ({leg_opening:.0f} mm opening x "
                 f"{leg_elastic_ratio:.2f}); gusset side edges are caught underneath"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; 4-thread overlock the side + gusset seams, "
                 "zigzag or coverstitch the elastic. No hardware — see the Yantra4D "
                 "commons if a decorative notion is ever added"},
    ]
    pattern.metadata = {
        "fc100_rank": 9,
        "fabric_hint": "jersey-algodon",
        "coverage": "full — flat front, full seat; lower leg line than the bikini panty",
        "fit_note": "close-fitting knit brief; negative ease tensions the jersey to the "
                    "body. Waist sits at/near the natural low-waist for the given rise",
        "stretch_note": "cut with greatest stretch (weft) horizontal; elastane-rich jersey",
        "negative_ease_pct": negative_ease_pct,
        "side_seam_mm": round(front.edge("side").length(), 1),
        "waist_opening_mm": round(waist_opening, 1),
        "waist_elastic_mm": waist_elastic,
        "leg_opening_each_mm": round(leg_opening, 1),
        "leg_elastic_each_mm": leg_elastic,
        "drafting": "full-coverage briefs: fold-cut flat front + full-seat back joined "
                    "by a real side seam, trapezoid gusset (self + liner) matching the "
                    "bodies by construction; waist and leg elastic cut lengths derived "
                    "exactly from the measured openings. Teaching-grade: a single hip "
                    "girth drives the widths (no separate seat/thigh measures yet), and "
                    "the front is flat (no shaped pouch)",
    }
    return pattern


result = build()

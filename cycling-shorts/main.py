"""
Cycling Shorts — FC-100 rank #58. Fashion Cabinet Garment Cartridge.

A compression cycling short: leggings cut to mid-thigh (longer than a running
short — cycling shorts run long to stop chafe) in athletic power-stretch, with
an anatomical crotch gusset and a placed chamois pad. Front and back are
fold-cut bodies (CF/CB on the fold) at deep negative ease (~15%, compression
grips hard), each carrying a long leg to mid-thigh. A diamond/anatomical gusset
(cut 1, on fold) closes the crotch; its front and back edges match the body
fork half-widths BY CONSTRUCTION, proven by declared seam checks. The chamois
insert (a purchased pad, never modelled here) is located by a placement marking
on the gusset/seat. The front fork is narrower than the deeper back seat, so the
shorter inseam is bowed outward by a SOLVED amount until it matches the longer —
the same numeric solve leggings uses. The wide flat waistband is a fold-over
casing whose attach edge equals the full measured waist opening (delta≈0), and
the leg openings carry SILICONE GRIPPER elastic cut to exact mm — the numbers
factories keep on private spec sheets.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|gusset|waistband|set

waist_girth       = float(PARAM(lambda: waist_girth, 800.0))
hip_girth         = float(PARAM(lambda: hip_girth, 960.0))
body_rise         = float(PARAM(lambda: body_rise, 250.0))     # crotch line to waist
inseam_length     = float(PARAM(lambda: inseam_length, 230.0))  # long mid-thigh leg
thigh_girth       = float(PARAM(lambda: thigh_girth, 560.0))   # girth at the leg hem
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 15.0))  # compression grip
back_rise_extra   = float(PARAM(lambda: back_rise_extra, 35.0))    # raised CB seat
gusset_front_w    = float(PARAM(lambda: gusset_front_w, 56.0))     # front fork width
gusset_back_w     = float(PARAM(lambda: gusset_back_w, 80.0))      # fuller back
gusset_len        = float(PARAM(lambda: gusset_len, 150.0))
waistband_height  = float(PARAM(lambda: waistband_height, 40.0))   # wide flat band
waistband_ratio   = float(PARAM(lambda: waistband_ratio, 0.90))    # band elastic/waist
leg_gripper_ratio = float(PARAM(lambda: leg_gripper_ratio, 0.94))  # gripper/opening
seam_allowance    = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (match the manifest sliders) ──────────────────────────────────────
waist_girth = max(500.0, min(waist_girth, 1500.0))
hip_girth = max(600.0, min(hip_girth, 1700.0))
body_rise = max(180.0, min(body_rise, 360.0))
inseam_length = max(180.0, min(inseam_length, 300.0))
thigh_girth = max(360.0, min(thigh_girth, 900.0))
negative_ease_pct = max(8.0, min(negative_ease_pct, 20.0))
back_rise_extra = max(0.0, min(back_rise_extra, 70.0))
gusset_front_w = max(40.0, min(gusset_front_w, 110.0))
gusset_back_w = max(40.0, min(gusset_back_w, 130.0))
gusset_len = max(90.0, min(gusset_len, 200.0))
waistband_height = max(25.0, min(waistband_height, 70.0))
waistband_ratio = max(0.82, min(waistband_ratio, 1.0))
leg_gripper_ratio = max(0.85, min(leg_gripper_ratio, 1.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# ── Derived geometry ─────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
RISE = body_rise                        # crotch line (y=0) to waist (y=RISE)
LEG = inseam_length                     # leg drops below the crotch line (y<0)
FWW = waist_girth * NEG / 4.0           # waist half-width per fold-cut half
HHW = hip_girth * NEG / 4.0             # hip half-width per fold-cut half (widest)
THW = thigh_girth * NEG / 4.0           # thigh (leg-hem) half-width per half
GF = gusset_front_w / 2.0               # front fork half-width (gusset on fold too, so
GB = gusset_back_w / 2.0                # gusset edges match the body forks by construction)
HIP_Y = RISE * 0.45                     # height of the hip (widest) point up the side
GRIPPER_ZONE = 12.0                     # marked silicone-gripper application width (mm)


def _gripper_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to a gripper-elastic edge, GRIPPER_ZONE mm inside.

    Pieces are authored CCW, so the inward normal at tangent t is (-t.y, t.x).
    The fraction window [t0, t1] keeps the trace off the corners.
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * GRIPPER_ZONE, p.y + tan.x * GRIPPER_ZONE))
    return fc.Internal(label, pts, kind="trace")


def _inseam(gusset_half, hem_inner_x, bulge):
    """Inseam from the leg-hem inner point up to the fork tip, bowed by `bulge`.

    A straight inseam when bulge≈0; a positive bulge bows it outward (toward the
    leg side) to gain length so the shorter front inseam can be solved to the
    longer back inseam.
    """
    return fc.Edge(
        "inseam",
        [fc.curve_through(fc.P(hem_inner_x, -LEG), fc.P(gusset_half, 0.0),
                          bulge=bulge, side=1.0)],
    )


def _body(name, gusset_half, seat_extra, bulge, hem_inner_x, hem_outer_x, label):
    """Fold-cut cycling-short body: waist, side, long leg, inseam, fork, fold."""
    waist = fc.Edge("waist", [fc.Line(fc.P(0.0, RISE + seat_extra), fc.P(FWW, RISE))])
    # Side (outseam): waist side point down over the hip curve to the leg-hem outer.
    outseam = fc.Edge(
        "outseam",
        [fc.Bezier(fc.P(FWW, RISE),
                   fc.P(HHW, RISE - HIP_Y * 0.5),
                   fc.P(HHW, HIP_Y),
                   fc.P(hem_outer_x, -LEG))],
    )
    leg_hem = fc.Edge("leg_hem", [fc.Line(fc.P(hem_outer_x, -LEG),
                                          fc.P(hem_inner_x, -LEG))])
    inseam = _inseam(gusset_half, hem_inner_x, bulge)
    gusset_edge = fc.Edge("gusset_edge",
                          [fc.Line(fc.P(gusset_half, 0.0), fc.P(0.0, 0.0))])
    center = fc.Edge("center", [fc.Line(fc.P(0.0, 0.0),
                                        fc.P(0.0, RISE + seat_extra))])

    # Leg opening carries silicone gripper elastic (bound, not turned).
    allowances = {"waist": 0.0, "leg_hem": 0.0}
    internals = [_gripper_zone(leg_hem, "silicone gripper zone", 0.06, 0.94)]

    return fc.Piece(
        name,
        [waist, outseam, leg_hem, inseam, gusset_edge, center],
        seam_allowance=seam_allowance,
        allowances=allowances,
        notches=[fc.Notch("inseam", 0.5, "inseam match"),
                 fc.Notch("outseam", 0.5, "side match"),
                 fc.Notch("gusset_edge", 0.5, "gusset match")],
        grainline=fc.Grainline(fc.P(THW * 0.5, -LEG * 0.4),
                               fc.P(THW * 0.5, RISE * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


# Front and back share one inner-hem x so the leg tube reads symmetric and the
# side seam (outseam) balances by construction. The two forks differ (narrow
# front fork GF, fuller back seat GB), so the two straight inseams differ; the
# SHORTER one is bowed outward until it matches the longer — leggings' solve.
HEM_INNER_X = GB + 4.0
HEM_OUTER_X = THW + HEM_INNER_X


def _solve_bulge(fork_half, target_len):
    """Bow an inseam (given fork half-width) outward until it reaches target_len."""
    lo, hi = 0.0, 0.60
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if _inseam(fork_half, HEM_INNER_X, mid).length(0.05) < target_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(_inseam(fork_half, HEM_INNER_X, bulge).length(0.05) - target_len) > 1.0:
        raise ValueError("inseam solver did not converge to the target inseam length")
    return bulge


def _inseam_solve():
    """Return (front_bulge, back_bulge, target_len). Shorter inseam is bowed."""
    front_straight = _inseam(GF, HEM_INNER_X, 0.0).length(0.05)
    back_straight = _inseam(GB, HEM_INNER_X, 0.0).length(0.05)
    target = max(front_straight, back_straight)
    front_bulge = 0.0 if front_straight >= back_straight else _solve_bulge(GF, target)
    back_bulge = 0.0 if back_straight >= front_straight else _solve_bulge(GB, target)
    return front_bulge, back_bulge, target


def build_back(back_bulge):
    """Fuller back: wider fork (GB), raised seat."""
    return _body("back", GB, back_rise_extra, back_bulge, HEM_INNER_X, HEM_OUTER_X,
                 "Back (full seat)")


def build_front(front_bulge):
    """Front: narrower fork (GF)."""
    return _body("front", GF, 0.0, front_bulge, HEM_INNER_X, HEM_OUTER_X,
                 "Front")


def build_gusset():
    """Anatomical crotch gusset on fold; cut 1 (self).

    Front edge half-width = GF, back edge half-width = GB — the exact fork
    half-widths of the bodies, so the crotch seams close by construction. The
    chamois pad (a purchased insert, never modelled) is located by a placement
    marking on the seat; its outline is a guide, not a cut line.
    """
    center = fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, gusset_len))])
    front_edge = fc.Edge("front_edge",
                         [fc.Line(fc.P(0.0, gusset_len), fc.P(GF, gusset_len))])
    side = fc.Edge(
        "side",
        [fc.Bezier(fc.P(GF, gusset_len), fc.P(GF + 3.0, gusset_len * 0.60),
                   fc.P(GB + 3.0, gusset_len * 0.28), fc.P(GB, 0.0))],
    )
    back_edge = fc.Edge("back_edge", [fc.Line(fc.P(GB, 0.0), fc.P(0.0, 0.0))])

    # Chamois placement marking (half-outline on the fold): a rounded pad centred
    # over the seat/crotch. Guide only — the pad is a purchased insert.
    pad_top = gusset_len * 0.86
    pad_bot = gusset_len * 0.16
    pad_w = min(GF, GB) * 0.82
    chamois = fc.Internal(
        "chamois pad placement",
        [
            fc.P(0.0, pad_top),
            fc.P(pad_w * 0.72, pad_top - gusset_len * 0.08),
            fc.P(pad_w, gusset_len * 0.55),
            fc.P(pad_w * 0.78, pad_bot + gusset_len * 0.06),
            fc.P(0.0, pad_bot),
        ],
        kind="marking",
    )
    return fc.Piece(
        "gusset",
        [center, front_edge, side, back_edge],
        seam_allowance=seam_allowance,
        allowances={"side": 0.0},  # caught under the leg gripper / inseam, not turned
        notches=[fc.Notch("front_edge", 0.5, "front match"),
                 fc.Notch("back_edge", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(8.0, gusset_len * 0.18),
                               fc.P(8.0, gusset_len * 0.82)),
        internals=[chamois],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Gusset + chamois placement",
    )


def build_waistband(front, back):
    """Wide flat fold-over band; attach edge = full measured waist opening.

    Front and back are fold-cut halves, so the full waist opening is
    2 * (front.waist + back.waist). The band's bottom (attach) edge equals that
    exactly (delta≈0); the wide flat band elastic threaded in the casing (or a
    bonded raw edge — see README) is cut to waist × ratio, emitted exact-mm.
    """
    attach = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    band_h = 2.0 * waistband_height  # fold-over: doubled, folds to a band of stand h
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(attach, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(attach, 0.0), fc.P(attach, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(attach, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"bottom": seam_allowance, "top": 0.0,
                    "end_a": seam_allowance, "end_b": seam_allowance},
        grainline=fc.Grainline(fc.P(attach * 0.2, band_h / 2.0),
                               fc.P(attach * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(attach, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Waistband (wide flat fold-over)",
    )


def build():
    pattern = fc.PatternSet("cycling-shorts")
    front_bulge, back_bulge, inseam_target = _inseam_solve()
    back = build_back(back_bulge)
    front = build_front(front_bulge)
    gusset = build_gusset()
    waistband = build_waistband(front, back)

    picked = {"front": front, "back": back, "gusset": gusset, "waistband": waistband}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # "set"
        for piece in (front, back, gusset, waistband):
            pattern.add(piece)
        # Inner-leg seam: front inseam bowed to the back inseam length.
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        # Side seam: front and back share the outseam block by construction.
        pattern.declare_seam(("front", "outseam"), ("back", "outseam"), tol=1.5)
        # Crotch: gusset front/back edges close onto the body forks by construction.
        pattern.declare_seam(("gusset", "front_edge"), ("front", "gusset_edge"), tol=1.0)
        pattern.declare_seam(("gusset", "back_edge"), ("back", "gusset_edge"), tol=1.0)
        # Waistband casing sews to the full waist opening (both fold halves twice).
        pattern.declare_seam(
            ("waistband", "bottom"),
            [("front", "waist"), ("front", "waist"),
             ("back", "waist"), ("back", "waist")],
            tol=1.5,
        )

    # ── Elastic accounting (the point of this cluster) ───────────────────────
    waist_opening = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    leg_opening = front.edge("leg_hem").length() + front.edge("inseam").length()
    waist_elastic = round(waist_opening * waistband_ratio)
    leg_gripper = round(leg_opening * leg_gripper_ratio)  # per leg

    fabric_width = 1550.0  # poliester-elastano-compresion card width
    area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
               for p in (front, back, gusset, waistband))
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "poliester-elastano-compresion", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"bodies + gusset + band at {fabric_width:.0f} mm width, 62% marker "
                 "efficiency; greatest stretch (weft) runs around the body"},
        {"item": "wide flat waistband elastic 40 mm", "qty": waist_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {waist_opening:.0f} mm waist x {waistband_ratio:.2f}; "
                 "thread inside the fold-over casing, join in a ring and quarter-mark. "
                 "Alternative: bond/raw-cut the band edge (no elastic) — see README"},
        {"item": "silicone gripper leg elastic 15 mm", "qty": 2 * leg_gripper,
         "unit": "mm_length",
         "note": f"two legs x {leg_gripper} mm each ({leg_opening:.0f} mm opening x "
                 f"{leg_gripper_ratio:.2f}); silicone-backed, zigzag into the marked leg "
                 "zone so the hem grips the thigh"},
        {"item": "chamois pad insert", "qty": 1, "unit": "count",
         "note": "purchased anatomical cycling pad (multi-density foam/gel), located by "
                 "the gusset placement marking; a component reference (federates to a "
                 "Yantra4D pad cartridge), never modelled as geometry here"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; flatlock/coverstitch every seam to avoid chafe "
                 "(compression card care: press cool or not at all)"},
    ]

    pattern.metadata = {
        "fc100_rank": 58,
        "fabric_hint": "poliester-elastano-compresion",
        "summary": "compression cycling short with anatomical gusset + chamois placement",
        "stretch_note": "cut with greatest stretch (weft) horizontal; power-stretch interlock",
        "negative_ease_pct": negative_ease_pct,
        "front_fork_half_mm": round(GF, 1),
        "back_fork_half_mm": round(GB, 1),
        "front_inseam_bulge": round(front_bulge, 4),
        "back_inseam_bulge": round(back_bulge, 4),
        "inseam_solved_side": "front" if front_bulge > back_bulge else "back",
        "inseam_len_mm": round(front.edge("inseam").length(), 1),
        "waist_opening_mm": round(waist_opening, 1),
        "waist_elastic_mm": waist_elastic,
        "leg_opening_each_mm": round(leg_opening, 1),
        "leg_gripper_each_mm": leg_gripper,
        "leg_finish": "silicone_gripper",
        "chamois": "purchased insert; placement marking on the gusset seat, not modelled",
        "drafting": "compression cycling short (leggings cut to a long mid-thigh + intimates "
                    "elastic accounting): front fork narrower than the fuller back seat, the "
                    "shorter inseam bowed to the longer by a solved amount; gusset front/back "
                    "edges match the body forks by construction; waistband casing attach edge "
                    "equals the full measured waist opening; leg openings carry silicone "
                    "gripper elastic cut to exact mm",
        "teaching_grade": "single snug thigh half-width front and back so the side seam "
                          "balances without a separate side-shaping solve; chamois pad and "
                          "any reflective trim are purchased components (BOM refs), not "
                          "drafted geometry",
    }
    return pattern


result = build()

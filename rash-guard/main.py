"""
Rash guard — FC-100 rank #57. Fashion Cabinet Garment Cartridge.

A second-skin UV surf top: the long-sleeve fitted knit block drafted with
NEGATIVE ease (the panties-bikini idiom) in a swimwear tricot, finished with
flatlock/coverstitch seams for chafe-free wear against bare skin. Front and
back are cut on fold; a long, tapered, cap-solved sleeve sets in flat (knits
take little to no cap ease); a crew neckline is BOUND with a stretched
self-fabric strip whose attach edge is solved to the neckline opening — the
seam balances by construction, and the BOM carries the exact-mm stretched
binding cut length the way factories keep it on a private spec sheet.

Flatlock is a seam TREATMENT, not geometry: the pieces are a normal fitted
tee. It shows up as (a) modest 7 mm allowances typical of a flatlock/coverstitch
foot, (b) the flatlock/wooly-nylon thread line in the BOM, and (c) the notes.

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


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|neck_binding|set

chest_girth       = float(PARAM(lambda: chest_girth, 980.0))
body_length       = float(PARAM(lambda: body_length, 680.0))    # nape to hem
neck_girth        = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length     = float(PARAM(lambda: sleeve_length, 600.0))  # shoulder to wrist
wrist_opening     = float(PARAM(lambda: wrist_opening, 165.0))  # flat width at cuff hem
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 10.0))  # second-skin fit
mock_neck_height  = float(PARAM(lambda: mock_neck_height, 0.0))  # 0 = crew; >0 raises CF/CB neck
binding_ratio     = float(PARAM(lambda: binding_ratio, 0.88))   # stretched cut / opening
binding_width     = float(PARAM(lambda: binding_width, 18.0))   # finished bound height
cap_ease          = float(PARAM(lambda: cap_ease, 0.0))         # sleeve cap ease (knits ~0)
seam_allowance    = float(PARAM(lambda: seam_allowance, 7.0))   # flatlock/coverstitch range
hem_allowance     = float(PARAM(lambda: hem_allowance, 20.0))   # coverstitched body/cuff hem

# ── Clamps (mirror the manifest sliders) ─────────────────────────────────────
chest_girth = max(600.0, min(chest_girth, 1600.0))
body_length = max(400.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(300.0, min(sleeve_length, 780.0))
wrist_opening = max(120.0, min(wrist_opening, 320.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 20.0))
mock_neck_height = max(0.0, min(mock_neck_height, 90.0))
binding_ratio = max(0.75, min(binding_ratio, 1.0))
binding_width = max(10.0, min(binding_width, 40.0))
cap_ease = max(0.0, min(cap_ease, 30.0))

# ── Negative ease: draft SMALLER than the body so the fabric tensions to fit ──
# Body girths stay full-body measurements; NEG reduces the girth-derived widths
# in the DRAFT (the swim tricot's cut_scale < 1.0 encodes the same idea).
NEG = 1.0 - negative_ease_pct / 100.0

W = chest_girth * NEG / 4.0                 # quarter body width (fold at CF/CB)
L = body_length
AH = max(150.0, min(chest_girth * NEG / 8.0 + 90.0, L - 110.0))  # armhole depth
NW = max(55.0, neck_girth * NEG / 5.0)      # half neck width on the fold
HPS_Y = L + 20.0                            # high point shoulder above the nape line
SHOULDER_DROP = 28.0                        # fitted set-in shoulder (less drop than a tee)
FRONT_NECK_DROP = 78.0
BACK_NECK_DROP = 18.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)


def _armhole_edge():
    """Fitted set-in armhole; front and back share it (knit block, sets flat)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.36),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.28), UNDERARM)],
    )


def _body_piece(name, neck_edge, neck_top_y, label):
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck_edge,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "neck": 0.0},  # neck is bound, not turned
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, f"{name} armhole")],
        grainline=fc.Grainline(fc.P(W * 0.60, 70.0), fc.P(W * 0.60, L - 110.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    cf_neck_y = HPS_Y - FRONT_NECK_DROP - mock_neck_height
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, cf_neck_y), fc.P(NW * 0.55, cf_neck_y),
                   fc.P(NW, cf_neck_y + (FRONT_NECK_DROP + mock_neck_height) * 0.42),
                   fc.P(NW, HPS_Y))],
    )
    return _body_piece("front", neck, cf_neck_y, "Front")


def build_back():
    cb_neck_y = HPS_Y - BACK_NECK_DROP - mock_neck_height
    neck = fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, cb_neck_y), fc.P(NW, HPS_Y), bulge=0.11, side=-1.0)],
    )
    return _body_piece("back", neck, cb_neck_y, "Back")


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.66, sl + ch * 0.10),
                      fc.P(hb * 0.30, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.30, sl + ch),
                     fc.P(-hb * 0.66, sl + ch * 0.10), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    """Long tapered sleeve; cap half-breadth solved so cap length == target.

    `cap_target` already includes any intentional cap ease, so the solved cap
    is the eased length and the declared cap↔armhole seam balances at that ease.
    """
    ch = max(42.0, AH * 0.32)                 # shallow knit cap
    sl = max(230.0, sleeve_length - ch)       # underarm-to-wrist run
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(56):                       # bisect: cap length grows with hb
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs target {cap_target:.1f}"
        )
    chw = max(60.0, min(wrist_opening / 2.0, hb))   # half wrist width, tapered
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
        fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
        _cap_curve(hb, sl, ch),
        fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
    ]
    return fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (long, tapered)",
    )


def build_neck_binding(half_opening):
    """Bound crew-neck strip, cut on the fold at center-back.

    Front and back necks are each drafted at HALF (they are cut on the fold), so
    their raw edge lengths sum to the HALF neckline. This strip mirrors that fold
    logic: its `neckline` (attach) edge is drafted to that same half-opening and
    cut on the fold at `end_a` (center-back), so the physical strip opens out to
    the full neck loop and the declared neckline seam balances at delta ~ 0.

    The strip is CUT shorter in fabric than the opening (opening x binding_ratio)
    and applied stretched — that exact-mm stretched length lives in the BOM /
    metadata, not in this flat pattern length. Folded lengthwise (finished
    height = binding_width) and coverstitched, so the long edges are not turned.
    """
    band_len = half_opening
    band_h = 2.0 * binding_width
    edges = [
        fc.Edge("neckline", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
        fc.Edge("fold", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "neck_binding",
        edges,
        seam_allowance=seam_allowance,
        allowances={"neckline": 0.0, "fold": 0.0},   # bound/folded, not turned
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal(
            "fold line",
            [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)],
        )],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="end_a", mirror=True),
        label="Neck binding (bound crew, cut on fold at CB)",
    )


def build():
    pattern = fc.PatternSet("rash-guard")
    front = build_front()
    back = build_back()
    half_opening = front.edge("neck").length() + back.edge("neck").length()
    neck_opening = 2.0 * half_opening
    # Cap sews into front + back armholes; add any intentional cap ease so the
    # solved cap length equals (armholes + ease) and the seam still balances.
    cap_target = (
        front.edge("armhole").length(0.05)
        + back.edge("armhole").length(0.05)
        + cap_ease
    )

    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "neck_binding": target_piece in ("neck_binding", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    if wanted["neck_binding"]:
        pattern.add(build_neck_binding(half_opening))

    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0, ease=cap_ease,
        )
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    if wanted["neck_binding"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("neck_binding", "neckline")],
            [("front", "neck"), ("back", "neck")],
            tol=1.5,
        )

    # ── Consumption + notions (swim tricot; flatlock/coverstitch) ────────────
    binding_cut = round(neck_opening * binding_ratio)   # exact stretched cut length
    fabric_width = 1500.0                               # tricot-nylon-elastano card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.68)     # 4-way stretch nests fairly tight
    pattern.bom = [
        {"item": "tricot-nylon-elastano", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"swim shell at {fabric_width:.0f} mm width, ~68% marker efficiency; "
                 "greatest stretch runs weft (around the body); chlorine-resistant grade "
                 "for pool use"},
        {"item": "neck binding strip (self fabric)", "qty": binding_cut, "unit": "mm_length",
         "note": f"cut {binding_cut} mm x {2.0 * binding_width:.0f} mm ({neck_opening:.0f} mm "
                 f"opening x {binding_ratio:.2f}); fold lengthwise, apply stretched, "
                 "coverstitch to finish"},
        {"item": "wooly-nylon / flatlock thread", "qty": 1, "unit": "set",
         "note": "flatlock or 3-thread coverstitch all seams for a flat, chafe-free "
                 "finish against skin; ballpoint 75/11 needle, textured looper thread"},
        {"item": "UPF note", "qty": 1, "unit": "spec",
         "note": "tightly-knit nylon/elastane at this gsm reads UPF 50+ when worn to fit; "
                 "negative ease keeps the knit stretched thin enough to stay UV-rated"},
    ]
    pattern.metadata = {
        "fc100_rank": 57,
        "fabric_hint": "tricot-nylon-elastano",
        "summary": "fitted UV rash guard, flatlock-seamed for chafe-free surf wear",
        "negative_ease_pct": negative_ease_pct,
        "quarter_body_width_mm": round(W, 1),
        "armhole_depth_mm": round(AH, 1),
        "neck_opening_mm": round(neck_opening, 1),
        "binding_cut_mm": binding_cut,
        "binding_ratio": binding_ratio,
        "armhole_each_mm": round((cap_target - cap_ease) / 2.0, 1),
        "cap_ease_mm": cap_ease,
        "mock_neck_height_mm": mock_neck_height,
        "flatlock_seams": ["shoulder", "side", "sleeve cap↔armhole", "sleeve underarm"],
        "upf_note": "tight nylon/elastane knit at fit reads UPF 50+; worn stretched by "
                    "negative ease",
        "drafting": "long-sleeve fitted knit block drafted at negative ease in swim tricot; "
                    "cap solved to armhole length; crew neckline bound with a stretched "
                    "self strip that matches the opening by construction (teaching-grade: "
                    "flatlock is modeled as a seam treatment, not as geometry)",
    }
    return pattern


result = build()

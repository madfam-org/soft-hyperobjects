"""
Wrap Dress — FC-100 rank #25 (Vestido cruzado).

The shift-dress body opened into a true wrap: ONE front piece cuts twice
mirrored, its center edge extended past CF by `wrap_extension` and drawn as a
single straight diagonal from the hem corner up to the shoulder-neck point —
the surplice "neck" edge IS the wrap edge, so the mirrored pair overlaps below
the CF crossing (notched at the computed arc fraction) and the V above it is
the neckline. The back cuts on fold with a shallow scoop. Both panels flare
`flare_mm` into an A-line below the waist; two straight waist ties close the
wrap, the inner one exiting through a side-seam opening notched on BOTH side
edges at the waist and marked internally on the front. Front and back share
one shoulder, armhole, and side construction so the declared seams match by
construction; the short sleeve cap is SOLVED numerically (bisection) to the
measured front + back armholes at zero ease.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|ties|set

bust_girth = float(PARAM(lambda: bust_girth, 940.0))
dress_length = float(PARAM(lambda: dress_length, 980.0))      # nape line to hem
neck_girth = float(PARAM(lambda: neck_girth, 385.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 200.0))    # cap apex to sleeve hem
wrap_ease = float(PARAM(lambda: wrap_ease, 110.0))            # total ease over the bust
wrap_extension = float(PARAM(lambda: wrap_extension, 240.0))  # hem-level cross past CF
flare_mm = float(PARAM(lambda: flare_mm, 100.0))              # A-line flare below the waist
tie_length = float(PARAM(lambda: tie_length, 900.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

bust_girth = max(600.0, min(bust_girth, 1700.0))
dress_length = max(700.0, min(dress_length, 1400.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(80.0, min(sleeve_length, 350.0))
wrap_ease = max(60.0, min(wrap_ease, 300.0))
wrap_extension = max(80.0, min(wrap_extension, bust_girth / 3.0))
flare_mm = max(0.0, min(flare_mm, 200.0))
tie_length = max(500.0, min(tie_length, 1400.0))

BACK_NECK_DROP = 25.0   # shallow back scoop
SHOULDER_DROP = 30.0    # HPS down to the shoulder point
NAPE_TO_WAIST = 400.0   # locates the tie exit and the flare break
TIE_WIDTH = 45.0

W = (bust_girth + wrap_ease) / 4.0                  # bust quarter
HPS_Y = dress_length + 20.0                         # nape line at y = dress_length
NECK_W = max(55.0, min(neck_girth / 5.0, 110.0))    # half neck width at HPS
AH = (bust_girth + wrap_ease) / 8.0 + 85.0          # armhole depth below the shoulder pt
AH = max(170.0, min(AH, 260.0))
SH_X = max(NECK_W + 20.0, min(NECK_W + 118.0, W - 30.0))
SH_END = fc.P(SH_X, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, SH_END.y - AH)
WAIST_Y = min(dress_length - NAPE_TO_WAIST, UNDERARM.y - 80.0)
WAIST_PT = fc.P(W, WAIST_Y)
HEM_OUT = fc.P(W + flare_mm, 0.0)                   # A-line hem corner

# The wrap edge is one straight line, so both fractions are exact by ratio:
# where the diagonal crosses CF (x = 0), and where the side edge passes the
# waist point (the joint between its two straight segments).
WRAP_CF_T = wrap_extension / (wrap_extension + NECK_W)
SIDE_DROP = UNDERARM.y - WAIST_Y
TIE_EXIT_T = SIDE_DROP / (SIDE_DROP + WAIST_PT.distance(HEM_OUT))


def _back_neck_edge():
    """Shallow scoop from the center top to the HPS point."""
    top_y = HPS_Y - BACK_NECK_DROP
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, top_y), fc.P(NECK_W * 0.55, top_y),
                   fc.P(NECK_W, top_y + BACK_NECK_DROP * 0.45), fc.P(NECK_W, HPS_Y))],
    )


def _shoulder_edge():
    return fc.Edge("shoulder", [fc.Line(fc.P(NECK_W, HPS_Y), SH_END)])


def _armhole_edge():
    """Set-in scoop shared by front and back — the solved sleeve cap depends on it."""
    c0 = fc.P(SH_X + 6.0, SH_END.y - AH * 0.45)
    c1 = fc.P(SH_X + (W - SH_X) * 0.35, UNDERARM.y + 14.0)
    return fc.Edge("armhole", [fc.Bezier(SH_END, c0, c1, UNDERARM)])


def _side_edge():
    """ONE construction for BOTH pieces: a straight run from the underarm to
    the waist, then the A-line flare to the hem — so front.side matches
    back.side exactly and the tie-exit fraction is identical on both."""
    return fc.Edge("side", [fc.Line(UNDERARM, WAIST_PT), fc.Line(WAIST_PT, HEM_OUT)])


def _grainline():
    return fc.Grainline(fc.P(W * 0.62, 90.0), fc.P(W * 0.62, UNDERARM.y - 60.0))


def _front():
    """Wrap front: the surplice neck edge runs straight from the hem corner
    `wrap_extension` past CF up to the shoulder-neck point. Cut 2 mirror —
    the pair is the overlap and underlap panels."""
    hem_in = fc.P(-wrap_extension, 0.0)
    edges = [
        fc.Edge("neck", [fc.Line(hem_in, fc.P(NECK_W, HPS_Y))]),
        _shoulder_edge(),
        _armhole_edge(),
        _side_edge(),
        fc.Edge("hem", [fc.Line(HEM_OUT, hem_in)]),
    ]
    # The inner tie passes through the side seam at waist level: a short
    # internal mark points at the opening from inside the panel.
    tie_mark = fc.Internal(
        "tie exit", [fc.P(W - 30.0, WAIST_Y), fc.P(W - 5.0, WAIST_Y)], kind="marking",
    )
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("neck", WRAP_CF_T, "CF crossing"),
                 fc.Notch("side", TIE_EXIT_T, "tie exit")],
        grainline=_grainline(),
        internals=[tie_mark],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Wrap Front",
    )


def _back():
    cb_len = HPS_Y - BACK_NECK_DROP
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, cb_len))]),
        _back_neck_edge(),
        _shoulder_edge(),
        _armhole_edge(),
        _side_edge(),
        fc.Edge("hem", [fc.Line(HEM_OUT, fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", TIE_EXIT_T, "tie exit")],
        grainline=_grainline(),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Dress Back",
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def _sleeve(cap_target):
    """Short cap sleeve; the cap half-width is bisected until the cap length
    matches the measured front + back armholes (zero ease — jersey sews the
    cap flat, no easing-in required)."""
    ch = max(50.0, AH * 0.38)                       # cap height
    sl = max(60.0, sleeve_length - ch)              # underarm-to-hem length
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(48):                             # bisect: cap length grows with hb
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
    chw = max(60.0, min(hb * 0.82, hb))             # gently tapered hem opening
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
        fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
        _cap_curve(hb, sl, ch),
        fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 25.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def _tie():
    w = TIE_WIDTH
    return fc.Piece(
        "tie",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(tie_length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(tie_length, 0.0), fc.P(tie_length, w))]),
            fc.Edge("top", [fc.Line(fc.P(tie_length, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(tie_length * 0.2, w / 2.0),
                               fc.P(tie_length * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Waist Tie",
    )


def build():
    pattern = fc.PatternSet("wrap-dress")
    front = _front()
    back = _back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "ties": target_piece in ("ties", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(_sleeve(cap_target))
    if wanted["ties"]:
        pattern.add(_tie())
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
        )
    if wanted["sleeve"]:
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    fabric_width = 1600.0                       # jersey-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0) for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.65)   # 65% marker efficiency
    pattern.bom = [
        {"item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 65% marker efficiency"},
        {"item": "sewing thread (poly)", "qty": 1, "unit": "spool",
         "note": "narrow-hem the wrap edge; bar-tack the side-seam tie exit"},
    ]
    overlap = max(0.0, 2.0 * (wrap_extension - (wrap_extension + NECK_W) * WAIST_Y / HPS_Y))
    pattern.metadata = {
        "fc100_rank": 25,
        "fabric_hint": "jersey-algodon",
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "cf_crossing_height_mm": round(HPS_Y * WRAP_CF_T, 1),
        "waist_overlap_mm": round(overlap, 1),
        "tie_exit_waist_y_mm": round(WAIST_Y, 1),
        "drafting": "true wrap from the shift-dress body: surplice neck = one straight wrap "
                    "diagonal wrap_extension past CF (CF crossing notched), back on fold, "
                    "A-flare below the waist, sleeve cap bisection-solved to the armholes, "
                    "tie exit notched at the waist on both side edges",
    }
    return pattern


result = build()

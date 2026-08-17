"""
Shirt Dress — FC-100 rank #26. Fashion Cabinet Garment Cartridge.

The casual button-down (rank #20) lengthened into a dress ("vestido
camisero"): the same drop-shoulder woven block — no yoke, no collar fall —
carried to body_length 1050 with a gentle A-flare below the waist (hem
half-width = chest quarter + flare_mm). Front cut 2 mirrored with the center
edge extended `button_stand` past CF and NINE buttonhole cross-marks down the
CF line; back cut 1 on fold with the CB box pleat marked; the sleeve cap is
SOLVED by bisection to the front + back armholes at zero ease (short 220
default, long 600 preset); the ONE-PIECE band collar is solved to the
measured neckline exactly like the parent — half on fold at CB, its neck edge
bisected to one front.neck + half back.neck (the front neck carries the 15 mm
overlap past CF, so the per-half seam check closes at delta ~0). The dress
adds a waist TIE BELT (cut 1) with two belt loops, and in-seam POCKET bags:
one rounded-pouch silhouette (~160x180) cut 2 mirrored whose straight
`opening` edge sews between the pocket notches placed on both side seams at
hip level.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|...|set

chest_girth    = float(PARAM(lambda: chest_girth, 1000.0))
body_length    = float(PARAM(lambda: body_length, 1050.0))   # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 395.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 220.0))  # cap apex to hem
dress_ease     = float(PARAM(lambda: dress_ease, 160.0))     # total; easy fit
button_stand   = float(PARAM(lambda: button_stand, 30.0))    # front edge past CF
collar_height  = float(PARAM(lambda: collar_height, 65.0))
flare_mm       = float(PARAM(lambda: flare_mm, 70.0))        # extra half-hem width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(800.0, min(body_length, 1400.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(100.0, min(sleeve_length, 660.0))
dress_ease = max(80.0, min(dress_ease, 400.0))
button_stand = max(20.0, min(button_stand, 40.0))
collar_height = max(40.0, min(collar_height, 90.0))
flare_mm = max(30.0, min(flare_mm, 250.0))

# ── Drop-shoulder dress block (rank #20 geometry, lengthened + flared) ───────
W = (chest_girth + dress_ease) / 4.0           # quarter body width at chest
L = body_length
AH = (chest_girth + dress_ease) / 8.0 + 95.0   # drop-shoulder armhole depth
AH = max(160.0, min(AH, 340.0))                # cap keeps the underarm above waist
NW = max(60.0, neck_girth / 5.0)               # half neck width at HPS
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 20.0
FRONT_NECK_DROP = max(65.0, neck_girth / 5.0 + 8.0)
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
CB_NECK_Y = HPS_Y - BACK_NECK_DROP
OVERLAP = 15.0                                 # collar end past CF (button line)
COLLAR_RISE = 14.0                             # band front-edge curl
COLLAR_POINT = 8.0                             # gentle forward lean of the band end
PLEAT_LINES_X = (15.0, 45.0)                   # box-pleat folds, 30 mm apart
PLEAT_LEN = 120.0
BUTTONHOLES = 9
BELT_W = 60.0                                  # tie-belt strip width
LOOP_L, LOOP_W = 50.0, 12.0                    # belt-loop strip
POCKET_W, POCKET_H = 160.0, 180.0              # rounded in-seam pocket bag
POCKET_MARGIN = 10.0                           # bag beyond the opening, each end
POCKET_OPEN = POCKET_H - 2.0 * POCKET_MARGIN   # opening span on the side seam
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
WAIST_Y = min(L - 390.0, UNDERARM.y - 35.0)    # nape-to-waist 410 below HPS
HEM_OUT = fc.P(W + flare_mm, 0.0)              # hem half-width = quarter + flare
HIP_Y = max(WAIST_Y - 200.0, 60.0 + POCKET_OPEN / 2.0)
OPEN_TOP_Y = HIP_Y + POCKET_OPEN / 2.0         # pocket opening ends on the side
OPEN_BOT_Y = HIP_Y - POCKET_OPEN / 2.0


def _armhole_edge():
    """Shared front/back armhole (drop-shoulder blocks keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _front_neck_edge():
    """Front neck: 15 mm overlap line past CF, then the scoop up to HPS.

    The straight run from (-OVERLAP, CF_NECK_Y) to CF is where the band collar
    ends (button line); including it in the neck edge makes the per-half seam
    check collar.neck == front.neck + back.neck close exactly.
    """
    cf = fc.P(0.0, CF_NECK_Y)
    scoop = fc.Bezier(cf, fc.P(NW * 0.55, CF_NECK_Y),
                      fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))
    return fc.Edge("neck", [fc.Line(fc.P(-OVERLAP, CF_NECK_Y), cf), scoop])


def _side_edge():
    """Fitted run underarm to waist, then the gentle A-flare to the hem.

    ONE construction for BOTH body pieces, so front.side == back.side exactly.
    The flare Bezier leaves the waist straight down (G1 with the fitted run)
    and arrives at the hem along the flare direction.
    """
    waist_pt = fc.P(W, WAIST_Y)
    flare_dir = (HEM_OUT - waist_pt).normalized()
    c0 = fc.P(W, WAIST_Y * 0.72)
    c1 = HEM_OUT - flare_dir * (WAIST_Y * 0.35)
    return fc.Edge("side", [fc.Line(UNDERARM, waist_pt),
                            fc.Bezier(waist_pt, c0, c1, HEM_OUT)])


def _side_t_at_y(y_target):
    """Arc-length fraction along the side edge where it crosses y_target.

    The side edge is authored underarm (t=0) to hem (t=1) and is monotonic in
    y, so the first crossing of the flattened polyline is the answer.
    """
    pts = _side_edge().flatten(0.05)
    total = fc.polyline_length(pts)
    run = 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        step = a.distance(b)
        if (a.y - y_target) * (b.y - y_target) <= 0.0 and abs(a.y - b.y) > 1e-9:
            return (run + step * (a.y - y_target) / (a.y - b.y)) / total
        run += step
    return 0.5


WAIST_T = _side_t_at_y(WAIST_Y)
OPEN_TOP_T = _side_t_at_y(OPEN_TOP_Y)
OPEN_BOT_T = _side_t_at_y(OPEN_BOT_Y)


def _side_notches(prefix):
    """Waist (belt-loop) mark + the two pocket-opening ends, both body pieces."""
    return [
        fc.Notch("side", WAIST_T, "waist / belt loop"),
        fc.Notch("side", OPEN_TOP_T, "pocket opening top"),
        fc.Notch("side", OPEN_BOT_T, "pocket opening bottom"),
        fc.Notch("armhole", 0.5, f"{prefix} armhole"),
    ]


def _buttonhole_marks():
    """Nine cross-marks on the CF line (x = 0), evenly spaced."""
    top = CF_NECK_Y - 60.0
    bottom = max(150.0, top - 800.0)
    arm = 4.0
    marks = []
    for i in range(BUTTONHOLES):
        y = top - (top - bottom) * i / (BUTTONHOLES - 1.0)
        marks.append(fc.Internal(
            f"buttonhole {i + 1}",
            [fc.P(-arm, y), fc.P(arm, y), fc.P(0.0, y),
             fc.P(0.0, y - arm), fc.P(0.0, y + arm)],
            kind="drill",
        ))
    return marks


def build_front():
    """Front, cut 2 mirrored: center edge extended button_stand past CF."""
    neck = _front_neck_edge()
    cf_t = max(0.02, min(0.5, OVERLAP / neck.length(0.05)))
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-button_stand, 0.0),
                                       fc.P(-button_stand, CF_NECK_Y))]),
            fc.Edge("stand_top", [fc.Line(fc.P(-button_stand, CF_NECK_Y),
                                          fc.P(-OVERLAP, CF_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            _side_edge(),
            fc.Edge("hem", [fc.Line(HEM_OUT, fc.P(-button_stand, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": hem_allowance},
        notches=[*_side_notches("front"), fc.Notch("neck", cf_t, "CF / collar end")],
        grainline=fc.Grainline(fc.P(W * 0.60, 80.0), fc.P(W * 0.60, L - 120.0)),
        internals=_buttonhole_marks(),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Dress Front",
    )


def build_back():
    """Back, cut 1 on fold at CB, box pleat marked as internal fold lines."""
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, CB_NECK_Y), fc.P(NW * 0.55, CB_NECK_Y),
                   fc.P(NW, CB_NECK_Y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    pleat_top = CB_NECK_Y - 6.0
    pleats = [
        fc.Internal(f"box pleat fold ({tag})",
                    [fc.P(x, pleat_top), fc.P(x, pleat_top - PLEAT_LEN)])
        for tag, x in zip(("inner", "outer"), PLEAT_LINES_X, strict=True)
    ]
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, CB_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            _side_edge(),
            fc.Edge("hem", [fc.Line(HEM_OUT, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=_side_notches("back"),
        grainline=fc.Grainline(fc.P(W * 0.60, 80.0), fc.P(W * 0.60, L - 120.0)),
        internals=pleats,
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


def build_sleeve(cap_target):
    """Cap solved by bisection to the front + back armholes, zero ease."""
    ch = max(45.0, AH * 0.33)                      # shallow relaxed cap
    sl = max(60.0, sleeve_length - ch)             # underarm-to-hem length
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(48):                            # cap length grows with hb
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs {cap_target:.1f}"
        )
    chw = max(70.0, hb * 0.72)                     # plain-hem opening half-width
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def _collar_neck_edge(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(half_target):
    """One-piece band collar, half on fold at CB, neck edge bisected to
    half_target = front.neck (one side, incl. overlap) + back.neck (half)."""
    lo, hi = half_target * 0.7, half_target * 1.05
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if _collar_neck_edge(mid).length(0.05) < half_target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(_collar_neck_edge(flat).length(0.05) - half_target) > 1.0:
        raise ValueError("collar neck-edge solver did not converge")
    point = fc.P(flat + COLLAR_POINT, COLLAR_RISE + collar_height)
    top_start = fc.P(0.0, collar_height)
    piece = fc.Piece(
        "collar",
        [
            _collar_neck_edge(flat),
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_RISE), point)]),
            fc.Edge("top", [fc.curve_through(point, top_start, bulge=0.04, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(flat * 0.20, collar_height * 0.55),
                               fc.P(flat * 0.75, collar_height * 0.55 + 7.0)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Band Collar (half, on fold)",
    )
    return piece, flat


def _strip(name, length, width, qty, label, notches=None):
    """Self-finished straight strip (tie belt, belt loops): sa 0, edge-turned."""
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
            fc.Edge("top", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=notches or [],
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0),
                               fc.P(length * 0.8, width / 2.0)),
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build_pocket():
    """In-seam pocket bag: rounded pouch with a straight opening edge.

    ONE symmetric bag silhouette cut 2 mirrored (one per side seam in v0;
    production doubles the layers from this same pattern — see docs). The
    straight `opening` edge sews into the side seam between the pocket
    notches; the bag clears the opening span by POCKET_MARGIN at each end,
    marked by the two notches on the opening edge.
    """
    w, h = POCKET_W, POCKET_H
    round_edge = fc.Edge("round", [
        fc.Bezier(fc.P(w * 0.44, 0.0), fc.P(w * 0.81, 0.0),
                  fc.P(w, h * 0.22), fc.P(w, h * 0.50)),
        fc.Bezier(fc.P(w, h * 0.50), fc.P(w, h * 0.78),
                  fc.P(w * 0.88, h), fc.P(w * 0.50, h)),
    ])
    return fc.Piece(
        "pocket",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w * 0.44, 0.0))]),
            round_edge,
            fc.Edge("top", [fc.Line(fc.P(w * 0.50, h), fc.P(0.0, h))]),
            fc.Edge("opening", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("opening", POCKET_MARGIN / h, "opening top match"),
                 fc.Notch("opening", 1.0 - POCKET_MARGIN / h, "opening bottom match")],
        grainline=fc.Grainline(fc.P(w * 0.28, 20.0), fc.P(w * 0.28, h - 20.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="In-Seam Pocket Bag",
    )


def build():
    pattern = fc.PatternSet("shirt-dress")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    half_neck = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "collar": target_piece in ("collar", "set"),
        "belt": target_piece in ("belt", "set"),
        "pocket": target_piece in ("pocket", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    collar_flat = None
    if wanted["collar"]:
        collar, collar_flat = build_collar(half_neck)
        pattern.add(collar)
    belt_len = chest_girth * 2.4                   # waist proxy: chest girth
    if wanted["belt"]:
        pattern.add(_strip("belt", belt_len, BELT_W, 1, "Tie Belt",
                           notches=[fc.Notch("top", 0.5, "center back")]))
        pattern.add(_strip("belt_loop", LOOP_L, LOOP_W, 2, "Belt Loop"))
    if wanted["pocket"]:
        pattern.add(build_pocket())
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
        )
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("collar", "neck")],
            [("front", "neck"), ("back", "neck")],
            tol=2.0,
        )
    fabric_width = 1450.0                          # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.65)
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 65% marker efficiency; the tie "
                 "belt is pieced at the center-back notch"},
        {"item": "fusible interfacing (collar band + button stands)", "qty": 1,
         "unit": "set", "note": "band cut doubled on fold; stands fused full length"},
        {"item": "shirt buttons Ø 10-12 mm", "qty": BUTTONHOLES + 1, "unit": "pieces",
         "note": "9 front + 1 spare; hard goods federate to Yantra4D (button family)"},
        {"item": "polyester thread + universal needle", "qty": 1, "unit": "set",
         "note": "sharp 80/12 for poplin"},
    ]
    pattern.metadata = {
        "fc100_rank": 26,
        "fabric_hint": "popelina-algodon",
        "collar_half_target_mm": round(half_neck, 1),
        "collar_flat_mm": None if collar_flat is None else round(collar_flat, 1),
        "neck_opening_full_mm": round(2.0 * half_neck, 1),
        "overlap_mm": OVERLAP,
        "button_stand_mm": button_stand,
        "buttonholes": BUTTONHOLES,
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "waist_y_mm": round(WAIST_Y, 1),
        "hem_half_width_mm": round(W + flare_mm, 1),
        "belt_mm": {"length": round(belt_len, 1), "width": BELT_W,
                    "loops": [LOOP_L, LOOP_W]},
        "pocket_mm": {"bag": [POCKET_W, POCKET_H], "opening_span": POCKET_OPEN,
                      "hip_y": round(HIP_Y, 1),
                      "side_t": [round(OPEN_TOP_T, 4), round(OPEN_BOT_T, 4)]},
        "box_pleat_mm": {"fold_lines_x": list(PLEAT_LINES_X), "length": PLEAT_LEN},
        "drafting": "casual-button-down (rank #20) lengthened to a dress: same "
                    "drop-shoulder block, A-flare below the waist, nine-button stand, "
                    "tie belt + loops, in-seam pocket bags notched at hip level; cap "
                    "and band collar both solved by bisection to measured openings",
    }
    return pattern


result = build()

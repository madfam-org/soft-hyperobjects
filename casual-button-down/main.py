"""
Casual Button-Down Shirt — FC-100 rank #20. Fashion Cabinet Garment Cartridge.

The relaxed everyday shirt ("camisa casual"), deliberately simpler than a
dress shirt: NO yoke and NO collar fall. Drop-shoulder woven block; front cut
2 mirrored with the center edge extended `button_stand` past CF (six
buttonhole cross-marks on the CF line, chest patch-pocket placement traced as
an internal); back cut 1 on fold with a box pleat marked as two internal fold
lines at CB top; a sleeve whose cap is SOLVED by bisection to the front + back
armholes at zero ease (short 240 default, long 600 preset, plain hem); and a
ONE-PIECE band collar solved to the measured neckline exactly like the
collar-band enabler — half on fold at CB, its neck edge bisected to one
front.neck + half back.neck (the front neck already carries the 15 mm overlap
past CF, so the per-half seam check closes at delta ~0).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|collar|set

chest_girth    = float(PARAM(lambda: chest_girth, 1040.0))
body_length    = float(PARAM(lambda: body_length, 740.0))    # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 240.0))  # cap apex to hem
woven_ease     = float(PARAM(lambda: woven_ease, 180.0))     # total; relaxed fit
button_stand   = float(PARAM(lambda: button_stand, 30.0))    # front edge past CF
collar_height  = float(PARAM(lambda: collar_height, 65.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(400.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(100.0, min(sleeve_length, 660.0))
woven_ease = max(80.0, min(woven_ease, 400.0))
button_stand = max(20.0, min(button_stand, 40.0))
collar_height = max(40.0, min(collar_height, 90.0))

# ── Drop-shoulder shirt block (rank #85 geometry family, shirt neckline) ─────
W = (chest_girth + woven_ease) / 4.0           # quarter body width
L = body_length
AH = (chest_girth + woven_ease) / 8.0 + 95.0   # drop-shoulder armhole depth
AH = max(160.0, min(AH, L - 120.0))
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
BUTTONHOLES = 6
POCKET_W, POCKET_H = 120.0, 135.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)


def _armhole_edge():
    """Shared front/back armhole (drop-shoulder shirts keep them equal)."""
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


def _buttonhole_marks():
    """Six cross-marks on the CF line (x = 0), evenly spaced."""
    top = CF_NECK_Y - 60.0
    bottom = max(110.0, top - 500.0)
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


def _pocket_trace():
    """Chest patch-pocket placement (wearer's left once mirrored)."""
    top = max(180.0, min(UNDERARM.y + 70.0, CF_NECK_Y - 40.0))
    bottom = max(top - POCKET_H, 40.0)
    left = W * 0.30
    right = min(left + POCKET_W, W * 0.92)
    return fc.Internal(
        "pocket placement",
        [fc.P(left, top), fc.P(right, top), fc.P(right, bottom),
         fc.P(left, bottom), fc.P(left, top)],
        kind="trace",
    )


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
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-button_stand, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole"),
                 fc.Notch("neck", cf_t, "CF / collar end")],
        grainline=fc.Grainline(fc.P(W * 0.60, 80.0), fc.P(W * 0.60, L - 120.0)),
        internals=[_pocket_trace(), *_buttonhole_marks()],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
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
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(W * 0.60, 80.0), fc.P(W * 0.60, L - 120.0)),
        internals=pleats,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
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


def build():
    pattern = fc.PatternSet("casual-button-down")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    half_neck = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "collar": target_piece in ("collar", "set"),
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
         "note": f"at {fabric_width:.0f} mm width, 65% marker efficiency"},
        {"item": "fusible interfacing (collar band + button stands)", "qty": 1,
         "unit": "set", "note": "band cut doubled on fold; stands fused full length"},
        {"item": "shirt buttons Ø 10-12 mm", "qty": BUTTONHOLES + 1, "unit": "pieces",
         "note": "6 front + 1 spare; hard goods federate to Yantra4D (button family)"},
        {"item": "polyester thread + universal needle", "qty": 1, "unit": "set",
         "note": "sharp 80/12 for poplin"},
    ]
    pattern.metadata = {
        "fc100_rank": 20,
        "fabric_hint": "popelina-algodon",
        "collar_half_target_mm": round(half_neck, 1),
        "collar_flat_mm": None if collar_flat is None else round(collar_flat, 1),
        "neck_opening_full_mm": round(2.0 * half_neck, 1),
        "overlap_mm": OVERLAP,
        "button_stand_mm": button_stand,
        "buttonholes": BUTTONHOLES,
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "box_pleat_mm": {"fold_lines_x": list(PLEAT_LINES_X), "length": PLEAT_LEN},
        "drafting": "drop-shoulder woven shirt; no yoke, no collar fall; cap and band "
                    "collar both solved by bisection to measured openings (ease 0)",
    }
    return pattern


result = build()

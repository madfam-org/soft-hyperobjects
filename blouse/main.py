"""
Blouse — FC-100 rank #21. Fashion Cabinet Garment Cartridge.

The darted woven top ("blusa"): fitted front and back cut on fold with a
scoop front neck and shallow back neck, side bust darts and back waist darts
kept as internal markings over a COMMON fitted side seam (skirt-block's
shared-side-point trick — the seam check passes by construction), a gently
curved shirttail-lite hem, a short sleeve whose gathered cap is SOLVED
numerically to the front + back armholes PLUS the gather ease (the multi-edge
seam check carries `ease=gather_ease`), a CB button-loop keyhole, and a neck
facing strip derived from the measured opening. Poplin draft: 110 mm ease.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `bust_girth`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr —
    they are not in the sandbox's allowed builtins.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|facing|set

bust_girth       = float(PARAM(lambda: bust_girth, 940.0))
body_length      = float(PARAM(lambda: body_length, 640.0))   # nape to hem at CB
neck_girth       = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length    = float(PARAM(lambda: sleeve_length, 180.0))  # cap apex to hem
woven_ease       = float(PARAM(lambda: woven_ease, 110.0))    # total; semi-fitted
bust_dart_intake = float(PARAM(lambda: bust_dart_intake, 25.0))
back_dart_intake = float(PARAM(lambda: back_dart_intake, 12.0))
gather_ease      = float(PARAM(lambda: gather_ease, 30.0))    # extra cap length
seam_allowance   = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance    = float(PARAM(lambda: hem_allowance, 15.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
bust_girth = max(600.0, min(bust_girth, 1800.0))
body_length = max(420.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(80.0, min(sleeve_length, 400.0))
woven_ease = max(40.0, min(woven_ease, 300.0))
bust_dart_intake = max(0.0, min(bust_dart_intake, 45.0))
back_dart_intake = max(0.0, min(back_dart_intake, 40.0))
gather_ease = max(0.0, min(gather_ease, 80.0))

W = (bust_girth + woven_ease) / 4.0           # quarter body width (fold at CF/CB)
L = body_length
HPS_Y = L + 20.0                              # high point shoulder above nape line
SHOULDER_DROP = 35.0
NW = max(60.0, neck_girth / 5.0)              # half neck width on the fold
FRONT_NECK_DROP = 100.0                       # scoop neck depth at CF
BACK_NECK_DROP = 30.0                         # shallow back neck at CB
AH_D = (bust_girth + woven_ease) / 8.0 + 75.0  # armhole depth below shoulder
AH_D = max(150.0, min(AH_D, 320.0, L - 240.0))
UA_Y = HPS_Y - SHOULDER_DROP - AH_D           # underarm level
WAIST_Y = min(max(140.0, L - 420.0), UA_Y - 90.0)
WAIST_SUPPRESS = 15.0                         # gentle in-curve at the waist
HEM_RISE = 25.0                               # side seam ends above CF/CB hem
BUST_DART_LEN = 110.0
BACK_DART_LEN = 100.0
FACING_HALF_WIDTH = 30.0                      # facing cut doubled: 2 × 30 mm strip
FACING_RATIO = 1.0                            # woven: facing length == opening
SH_END = fc.P(min(NW + 115.0, W - 40.0), HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, UA_Y)
WAIST_PT = fc.P(W - WAIST_SUPPRESS, WAIST_Y)
HEM_SIDE = fc.P(W - 5.0, HEM_RISE)


def _armhole_edge():
    """Shared front/back armhole curve (equal halves keep the cap solve simple)."""
    span = SH_END.y - UA_Y
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(SH_END.x + 6.0, SH_END.y - span * 0.38),
                   fc.P(W - 8.0, UA_Y + span * 0.30), UNDERARM)],
    )


def _side_edge():
    """Common fitted side seam for BOTH pieces (skirt-block's shared-point
    trick): identical geometry front/back, so the seam check passes by
    construction; per-piece dart intakes stay as internals. The upper bezier
    hugs x = W through the bust-dart zone before curving into the waist."""
    drop = UA_Y - WAIST_Y
    rise = WAIST_Y - HEM_RISE
    return fc.Edge(
        "side",
        [fc.Bezier(UNDERARM, fc.P(W, UA_Y - drop * 0.50),
                   fc.P(W - WAIST_SUPPRESS, WAIST_Y + drop * 0.28), WAIST_PT),
         fc.Bezier(WAIST_PT, fc.P(W - WAIST_SUPPRESS, WAIST_Y - rise * 0.35),
                   fc.P(W - 5.0, HEM_RISE + rise * 0.30), HEM_SIDE)],
    )


def _hem_edge():
    """Shirttail-lite hem: gentle curve from the raised side point to CF/CB."""
    return fc.Edge(
        "hem", [fc.curve_through(HEM_SIDE, fc.P(0.0, 0.0), bulge=0.03, side=1.0)]
    )


def _body_piece(name, neck_edge, neck_top_y, label, internals, armhole_label):
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck_edge,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        _side_edge(),
        _hem_edge(),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "waist line"),
                 fc.Notch("armhole", 0.5, armhole_label)],
        grainline=fc.Grainline(fc.P(W * 0.60, 70.0), fc.P(W * 0.60, L - 130.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    """Front on fold: scoop neck; side bust dart per side as an internal."""
    cf_neck_y = HPS_Y - FRONT_NECK_DROP
    cf_neck = fc.P(0.0, cf_neck_y)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(cf_neck, fc.P(NW * 0.55, cf_neck_y),
                   fc.P(NW, cf_neck_y + FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    internals = []
    if bust_dart_intake > 0.5:
        dart_y = UA_Y - 60.0                      # bust line on the side seam
        half = bust_dart_intake / 2.0
        internals.append(fc.Internal(
            "side bust dart",
            [fc.P(W - 1.0, dart_y + half), fc.P(W - 1.0 - BUST_DART_LEN, dart_y),
             fc.P(W - 1.0, dart_y - half)],
            kind="dart",
        ))
    return _body_piece("front", neck, cf_neck_y, "Front", internals, "front armhole")


def _keyhole(cb_neck_y):
    """CB button-loop keyhole: half-U on the fold; the mirror completes the U."""
    top = cb_neck_y - 2.0
    return fc.Internal(
        "CB keyhole slit",
        [fc.P(6.0, top), fc.P(6.0, top - 42.0), fc.P(4.0, top - 52.0),
         fc.P(0.0, top - 56.0)],
        kind="trace",
    )


def _loop_button(cb_neck_y):
    """Button cross-mark beside the keyhole (loop closes over it)."""
    bx, by = 11.0, cb_neck_y - 12.0
    return fc.Internal(
        "loop button",
        [fc.P(bx - 4.0, by), fc.P(bx + 4.0, by), fc.P(bx, by),
         fc.P(bx, by + 4.0), fc.P(bx, by - 4.0)],
        kind="drill",
    )


def build_back():
    """Back on fold: shallow neck, waist-dart pair (fold mirror), CB keyhole."""
    cb_neck_y = HPS_Y - BACK_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, cb_neck_y), fc.P(NW, HPS_Y),
                          bulge=0.12, side=-1.0)],
    )
    internals = []
    if back_dart_intake > 0.5:
        cx = (W - WAIST_SUPPRESS) * 0.5
        half = back_dart_intake / 2.0
        internals.append(fc.Internal(
            "back waist dart (pair on fold)",
            [fc.P(cx - half, WAIST_Y), fc.P(cx, WAIST_Y + BACK_DART_LEN),
             fc.P(cx + half, WAIST_Y)],
            kind="dart",
        ))
    internals.append(_keyhole(cb_neck_y))
    internals.append(_loop_button(cb_neck_y))
    return _body_piece("back", neck, cb_neck_y, "Back", internals, "back armhole")


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.60, sl + ch * 0.10),
                      fc.P(hb * 0.30, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.30, sl + ch),
                     fc.P(-hb * 0.60, sl + ch * 0.10), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    """Short gathered-cap sleeve: bisect the half-biceps width until the cap
    measures `cap_target` = front + back armholes + gather ease. The extra
    length is crowded into the gather zone between the t=0.35/0.65 notches."""
    ch = max(55.0, AH_D * 0.45)                     # tall crown: gathers need height
    sl = max(50.0, sleeve_length - ch)              # underarm-to-hem length
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
    cap = _cap_curve(hb, sl, ch)
    zone_pts = []
    for i in range(7):                              # gather-zone bar under the cap
        t = 0.35 + 0.05 * i
        pt, _tan = cap.point_at_fraction(t)
        zone_pts.append(fc.P(pt.x, pt.y - 7.0))
    chw = max(45.0, hb * 0.85)                      # slight taper to the hem
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
        fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
        cap,
        fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
    ]
    return fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match"),
                 fc.Notch("cap", 0.35, "gather start"),
                 fc.Notch("cap", 0.65, "gather stop")],
        grainline=fc.Grainline(fc.P(0.0, 25.0), fc.P(0.0, sl + ch * 0.6)),
        internals=[fc.Internal("gather zone", zone_pts, kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_facing(front_piece, back_piece):
    """Neck facing strip derived from the measured opening: full opening
    (front + back halves × 2) plus two joining allowances, cut 60 mm tall."""
    half_opening = front_piece.edge("neck").length() + back_piece.edge("neck").length()
    strip_len = 2.0 * half_opening * FACING_RATIO + 2.0 * seam_allowance
    strip_h = 2.0 * FACING_HALF_WIDTH
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(strip_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(strip_len, 0.0), fc.P(strip_len, strip_h))]),
        fc.Edge("top", [fc.Line(fc.P(strip_len, strip_h), fc.P(0.0, strip_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, strip_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "facing",
        edges,
        seam_allowance=0.0,                         # strip length already includes joins
        grainline=fc.Grainline(fc.P(strip_len * 0.2, strip_h / 2.0),
                               fc.P(strip_len * 0.8, strip_h / 2.0)),
        internals=[fc.Internal(
            "CB match",
            [fc.P(strip_len / 2.0, 0.0), fc.P(strip_len / 2.0, strip_h)],
        )],
        cut=fc.CutSpec(quantity=1),
        label="Neck facing",
    )


def build():
    pattern = fc.PatternSet("blouse")
    front = build_front()
    back = build_back()
    armholes = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    cap_target = armholes + gather_ease
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "facing": target_piece in ("facing", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    if wanted["facing"]:
        pattern.add(build_facing(front, back))
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
            ease=gather_ease,
        )
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    half_opening = front.edge("neck").length() + back.edge("neck").length()
    fabric_width = 1450.0                           # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.65)  # wovens nest looser than knits
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 65% marker efficiency"},
        {"item": "fusible interfacing for neck facing", "qty": 1, "unit": "strip",
         "note": "see facing piece dimensions; poplin card wants fused facings"},
        {"item": "small button + thread loop (CB keyhole)", "qty": 1, "unit": "set",
         "note": "hard notion: federate to a Yantra4D button ref, never redraft"},
        {"item": "polyester thread + universal needle", "qty": 1, "unit": "set",
         "note": "sharp 70/10-80/12 for poplin"},
    ]
    pattern.metadata = {
        "fc100_rank": 21,
        "fabric_hint": "popelina-algodon",
        "neck_opening_mm": round(2.0 * half_opening, 1),
        "armhole_each_mm": round(armholes / 2.0, 1),
        "cap_target_mm": round(cap_target, 1),
        "gather_ease_mm": gather_ease,
        "bust_dart": "side dart per side, pair by fold mirror; intake "
                     f"{bust_dart_intake:.0f} mm, length {BUST_DART_LEN:.0f} mm",
        "back_darts": "waist pair by fold mirror; intake "
                      f"{back_dart_intake:.0f} mm each, length {BACK_DART_LEN:.0f} mm",
        "facing_length_mm": round(
            2.0 * half_opening * FACING_RATIO + 2.0 * seam_allowance, 1
        ),
        "drafting": "darted woven top; common side seam; gathered cap solved "
                    "to armholes + gather ease; CB button-loop keyhole",
    }
    return pattern


result = build()

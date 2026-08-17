"""
Blazer — FC-100 rank #30. Fashion Cabinet Garment Cartridge.

The commons' first tailoring garment ("saco"): a teaching-grade single-breasted
blazer, honestly simplified. The front's center edge runs up the 20 mm button
stand to the ROLL LINE point at waist level, then breaks into the LAPEL — a
straight diagonal out to the lapel point 85 mm past CF at chest level — and a
gorge edge back in to the neck point. A fisheye dart shapes the waist, the back
carries a shaped CB seam (allowance 15) with vent markings, the one-piece
sleeve is solved to the armholes WITH 25 mm of declared cap ease (the commons'
first eased cap), the upper collar is solved to the gorge + back neck, and a
straight front facing is verified against the measured center + lapel + gorge
run. No lining or canvas in v0 — see docs/README.md.

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
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|collar|facing|set

chest_girth    = float(PARAM(lambda: chest_girth, 1020.0))
body_length    = float(PARAM(lambda: body_length, 700.0))    # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 620.0))  # cap apex to wrist
blazer_ease    = float(PARAM(lambda: blazer_ease, 140.0))    # total ease
button_stand   = float(PARAM(lambda: button_stand, 20.0))    # extension past CF
lapel_width    = float(PARAM(lambda: lapel_width, 85.0))     # lapel point past CF
roll_line_y    = float(PARAM(lambda: roll_line_y, 300.0))    # roll point above hem
collar_height  = float(PARAM(lambda: collar_height, 55.0))
cap_ease       = float(PARAM(lambda: cap_ease, 25.0))        # eased sleeve cap
vent_height    = float(PARAM(lambda: vent_height, 180.0))    # CB vent above hem
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(500.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(400.0, min(sleeve_length, 750.0))
blazer_ease = max(80.0, min(blazer_ease, 300.0))
button_stand = max(15.0, min(button_stand, 35.0))
lapel_width = max(60.0, min(lapel_width, 110.0))
roll_line_y = max(220.0, min(roll_line_y, 420.0))
collar_height = max(40.0, min(collar_height, 80.0))
cap_ease = max(0.0, min(cap_ease, 40.0))
vent_height = max(120.0, min(vent_height, 260.0))

# ── Tailored blazer block (dress-shirt frame, lapel front) ───────────────────
W = (chest_girth + blazer_ease) / 4.0          # quarter body width
L = body_length
NW = max(60.0, neck_girth / 5.0)               # half neck width at HPS
AH = (chest_girth + blazer_ease) / 8.0 + 120.0  # jacket-deep armhole (auto)
AH = max(180.0, min(AH, L - 260.0))            # chest line well above the waist
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 25.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y                           # chest level = lapel point level
ROLL_Y = max(120.0, min(roll_line_y, CHEST_Y - 60.0))  # roll point below chest
BS = button_stand
LW = lapel_width
ROLL_PT = fc.P(-BS, ROLL_Y)                    # center edge breaks here
LAPEL_PT = fc.P(-LW, CHEST_Y)                  # lapel point, past CF
NECK_PT = fc.P(NW, HPS_Y)                      # gorge lands on the neck point
CB_HEM_X, CB_WAIST_X = 8.0, 16.0               # CB seam waist shaping
CB_SA = 15.0                                   # CB seam allowance
VENT_W = 45.0                                  # vent underlap width
DART_INTAKE = 18.0                             # front fisheye dart
FACING_W = 90.0                                # straight front facing width
COLLAR_RISE = 14.0
BUTTONS = 2


def _cross(label, x, y, half=4.0):
    """Drill cross-mark as two internals (zipper-notion convention)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


def _solve_flat(edge_fn, target, what):
    """Bisect a monotonic flat-length → measured-curve-length edge builder."""
    lo, hi = target * 0.7, target * 1.05
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if edge_fn(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(edge_fn(flat).length(0.05) - target) > 1.0:
        raise ValueError(f"{what} solver did not converge on {target:.1f} mm")
    return flat


def _armhole(scoop):
    """Armhole from the shoulder end down to the underarm."""
    fah = SH_END.y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - scoop, SH_END.y - fah * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + fah * 0.30), UNDERARM)],
    )


def _fisheye_dart():
    """Front fisheye dart, waist to chest: a closed diamond, widest at the
    waist (roll-line level), intake 18 mm."""
    dx = W * 0.42
    half = DART_INTAKE / 2.0
    y_bot = max(ROLL_Y - 95.0, 60.0)
    y_top = CHEST_Y - 40.0
    return fc.Internal(
        "front fisheye dart",
        [fc.P(dx, y_bot), fc.P(dx - half, ROLL_Y), fc.P(dx, y_top),
         fc.P(dx + half, ROLL_Y), fc.P(dx, y_bot)],
        kind="dart",
    )


def _flap_pocket():
    """Hip flap-pocket markings: flap rectangle + attach line. Cut 2 mirror
    puts one on each front — markings only in v0, jetting is future work."""
    cx = W * 0.55
    attach = max(140.0, ROLL_Y - 110.0)
    fw, fh = 140.0, 55.0
    flap = [fc.P(cx - fw / 2.0, attach), fc.P(cx + fw / 2.0, attach),
            fc.P(cx + fw / 2.0, attach - fh), fc.P(cx - fw / 2.0, attach - fh),
            fc.P(cx - fw / 2.0, attach)]
    line = [fc.P(cx - fw / 2.0 - 6.0, attach), fc.P(cx + fw / 2.0 + 6.0, attach)]
    return [
        fc.Internal("hip flap", flap),
        fc.Internal("flap attach line", line),
    ]


def build_front():
    """Cut 2 mirror. Center edge = button stand up to the roll point; then the
    lapel diagonal out to the lapel point; then the gorge in to the neck
    point. The roll line is an internal from roll point to neck point."""
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, ROLL_Y)],
                    kind="marking"),
        fc.Internal("roll line", [ROLL_PT, NECK_PT], kind="marking"),
        _fisheye_dart(),
    ]
    internals += _flap_pocket()
    internals += _cross("buttonhole-1", 0.0, ROLL_Y)
    internals += _cross("buttonhole-2", 0.0, ROLL_Y - 90.0)
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, 0.0), ROLL_PT)]),
            fc.Edge("lapel", [fc.Line(ROLL_PT, LAPEL_PT)]),
            fc.Edge("gorge", [fc.Line(LAPEL_PT, NECK_PT)]),
            fc.Edge("shoulder", [fc.Line(NECK_PT, SH_END)]),
            _armhole(14.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-BS, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("center", 1.0, "roll point"),
                 fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.62, 80.0), fc.P(W * 0.62, L - 140.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Cut 2 mirror with a CB seam (allowance 15): gentle waist-shaping curve
    in to CB_WAIST_X at the roll-line level, straight above the chest. The CB
    vent is two internal marking lines, vent_height above the hem."""
    nape = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
    span = CHEST_Y - ROLL_Y
    cb = fc.Edge(
        "cb",
        [
            fc.Bezier(fc.P(CB_HEM_X, 0.0), fc.P(CB_HEM_X + 3.0, ROLL_Y * 0.45),
                      fc.P(CB_WAIST_X, ROLL_Y * 0.8), fc.P(CB_WAIST_X, ROLL_Y)),
            fc.Bezier(fc.P(CB_WAIST_X, ROLL_Y),
                      fc.P(CB_WAIST_X, ROLL_Y + span * 0.4),
                      fc.P(6.0, CHEST_Y - span * 0.2), fc.P(0.0, CHEST_Y)),
            fc.Line(fc.P(0.0, CHEST_Y), nape),
        ],
    )
    neck = fc.Edge(
        "neck",
        [fc.Bezier(nape, fc.P(NW * 0.55, nape.y),
                   fc.P(NW, nape.y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    vh = min(vent_height, ROLL_Y - 30.0)
    return fc.Piece(
        "back",
        [
            cb,
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole(10.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(CB_HEM_X, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": CB_SA, "hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(W * 0.6, 80.0), fc.P(W * 0.6, L - 140.0)),
        internals=[
            fc.Internal("CB vent underlap",
                        [fc.P(VENT_W, 0.0), fc.P(VENT_W, vh)], kind="marking"),
            fc.Internal("CB vent stop",
                        [fc.P(CB_HEM_X + 2.0, vh), fc.P(VENT_W, vh)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back",
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, back side first."""
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                  fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                  fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(front_ah, back_ah):
    """One-piece tailored sleeve: cap solved by bisection to the front + back
    armholes PLUS the declared cap ease (the eased tailored cap). Elbow
    shaping is a gentle outward bow on the back underarm edge — it adds well
    under 1 mm over the straight front underarm, inside the declared tol."""
    cap_target = front_ah + back_ah + cap_ease
    ch = max(70.0, AH * 0.32)
    sl = max(220.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(115.0, min(hb * 0.60, hb - 10.0))
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back",
                    [fc.curve_through(fc.P(chw, 0.0), fc.P(hb, sl),
                                      bulge=0.025, side=-1.0)]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", (back_ah + cap_ease / 2.0) / cap_target,
                          "cap match"),
                 fc.Notch("hem", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.8)),
        internals=[fc.Internal(
            "elbow line",
            [fc.P(-hb * 0.9, sl * 0.55), fc.P(hb * 0.9, sl * 0.55)],
            kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def _collar_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(gorge_len, back_neck_len):
    """Upper collar, half on fold at CB: neck edge solved by bisection to the
    measured front gorge + back neck per half (overlap 0, collar-band method).
    The classic 10 mm collar/lapel notch gap is a construction note — see
    docs/README.md."""
    target = gorge_len + back_neck_len
    flat = _solve_flat(_collar_neck, target, "upper-collar neck")
    neck = _collar_neck(flat)
    point = fc.P(flat + 15.0, COLLAR_RISE + collar_height)
    return fc.Piece(
        "collar",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_RISE), point)]),
            fc.Edge("top",
                    [fc.curve_through(point, fc.P(0.0, collar_height),
                                      bulge=0.03, side=1.0)]),
            fc.Edge("cb", [fc.Line(fc.P(0.0, collar_height), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", back_neck_len / target, "gorge seam match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, collar_height * 0.5),
                               fc.P(flat * 0.7,
                                    collar_height * 0.5 + COLLAR_RISE * 0.6)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Upper Collar (half, on fold)",
    )


def build_facing(center_len, lapel_len, gorge_len):
    """Straight front facing strip: length = the measured center + lapel +
    gorge run + end allowances (declared as seam ease), width 90. A shaped
    facing that mirrors the lapel is future work — see docs/README.md."""
    length = center_len + lapel_len + gorge_len + 2.0 * seam_allowance
    t_roll = (seam_allowance + center_len) / length
    return fc.Piece(
        "facing",
        [
            fc.Edge("long_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, FACING_W))]),
            fc.Edge("inner", [fc.Line(fc.P(length, FACING_W), fc.P(0.0, FACING_W))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, FACING_W), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                      # length already includes 2×sa
        notches=[fc.Notch("long_edge", t_roll, "roll point match")],
        grainline=fc.Grainline(fc.P(length * 0.2, FACING_W / 2.0),
                               fc.P(length * 0.8, FACING_W / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Facing",
    )


def build():
    pattern = fc.PatternSet("blazer")
    front = build_front()
    back = build_back()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    center_len = front.edge("center").length(0.05)
    lapel_len = front.edge("lapel").length(0.05)
    gorge_len = front.edge("gorge").length(0.05)
    back_neck_len = back.edge("neck").length(0.05)
    front_run = center_len + lapel_len + gorge_len
    names = ("front", "back", "sleeve", "collar", "facing")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(front_ah, back_ah))
    if wanted["collar"]:
        pattern.add(build_collar(gorge_len, back_neck_len))
    if wanted["facing"]:
        pattern.add(build_facing(center_len, lapel_len, gorge_len))
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")],
                             ease=cap_ease, tol=2.5)
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.5)
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front", "gorge"), ("back", "neck")], tol=2.5)
    if wanted["facing"] and wanted["front"]:
        pattern.declare_seam([("facing", "long_edge")],
                             [("front", "center"), ("front", "lapel"),
                              ("front", "gorge")],
                             tol=3.0, ease=2.0 * seam_allowance)
    fabric_width = 1450.0                        # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 60% marker efficiency"},
        {"item": "fusible interfacing (fronts, facing, upper collar)",
         "qty": 1, "unit": "set",
         "note": "teaching-grade fusible in place of a tailored canvas"},
        {"item": "suit buttons 20 mm", "qty": 2, "unit": "pcs",
         "note": "2 front; hardware is a Yantra4D cartridge (shank-button "
                 "guide), never re-implemented here"},
        {"item": "polyester thread + universal needle 80/12", "qty": 1,
         "unit": "set", "note": "press hard at every stage — pressing is half "
                                "the tailoring"},
    ]
    pattern.metadata = {
        "fc100_rank": 30,
        "fabric_hint": "popelina-algodon",
        "tailoring_note": "teaching-grade: one-piece sleeve, straight facing, "
                          "no lining/canvas — construction guide future",
        "lining": "not drafted in v0",
        "gorge_mm": round(gorge_len, 1),
        "back_neck_mm": round(back_neck_len, 1),
        "collar_neck_target_mm": round(gorge_len + back_neck_len, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_ease_mm": cap_ease,
        "cap_target_mm": round(front_ah + back_ah + cap_ease, 1),
        "front_edge_run_mm": round(front_run, 1),
        "facing_length_mm": round(front_run + 2.0 * seam_allowance, 1),
        "roll_line": {"roll_point_mm": [-BS, round(ROLL_Y, 1)],
                      "neck_point_mm": [round(NW, 1), round(HPS_Y, 1)]},
        "buttonholes": {"count": BUTTONS, "line": "CF (x=0)",
                        "stand_extension_mm": BS,
                        "top_button_at": "roll point"},
        "notch_gap": "classic 10 mm collar/lapel notch gap in construction — "
                     "see docs/README.md",
        "drafting": "single-breasted blazer on the dress-shirt frame: center "
                    "edge breaks at the roll point into a straight lapel and "
                    "gorge; shaped CB seam with vent markings; eased cap "
                    "solved to the armholes + 25 mm; upper collar solved to "
                    "gorge + back neck; straight facing verified against the "
                    "measured front edge run",
    }
    return pattern


result = build()

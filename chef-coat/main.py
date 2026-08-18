"""
Chef Coat (filipina de chef) — FC-100 rank #87. Fashion Cabinet Garment Cartridge.

The classic double-breasted chef's jacket, honestly simplified to teaching grade.
The signature is the WIDE CROSSOVER DOUBLE-BREASTED front: each front is cut 2
mirrored with its center edge extended a generous `crossover` past CF (default
110 mm), so the right front wraps well over the left. TWO columns of knotted
CLOTH/china buttons are marked on the front — an outer column near the wrap edge
(the functional closure) and an inner column near CF (the reversible/under-wrap
side) — ~2 columns × 5. A stand/band collar (mandarin) is solved to the measured
neckline exactly like the collar-band enabler; a one-piece sleeve is solved to
the front + back armholes with a small declared cap ease and carries a turn-back
cuff fold line + a sleeve-pocket trace; the body is roomy with side vents marked
and a straight hem; a chest thermometer-pocket is traced; and a straight
crossover front facing is verified against the measured center + neck run.
Reversible construction is a note — see docs/README.md. Cloth knot buttons are a
Yantra4D reference in the BOM, never re-implemented here.

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

chest_girth    = float(PARAM(lambda: chest_girth, 1080.0))
body_length    = float(PARAM(lambda: body_length, 780.0))    # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 410.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 610.0))  # cap apex to hem
coat_ease      = float(PARAM(lambda: coat_ease, 200.0))      # total; roomy fit
crossover      = float(PARAM(lambda: crossover, 110.0))      # wrap edge past CF
collar_height  = float(PARAM(lambda: collar_height, 55.0))   # band/mandarin
cap_ease       = float(PARAM(lambda: cap_ease, 15.0))        # small eased cap
cuff_turnback  = float(PARAM(lambda: cuff_turnback, 60.0))   # turn-back cuff depth
vent_height    = float(PARAM(lambda: vent_height, 160.0))    # side vent above hem
button_rows    = int(PARAM(lambda: button_rows, 5))          # buttons per column
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1800.0))
body_length = max(500.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(150.0, min(sleeve_length, 720.0))
coat_ease = max(120.0, min(coat_ease, 360.0))
crossover = max(70.0, min(crossover, 160.0))
collar_height = max(40.0, min(collar_height, 75.0))
cap_ease = max(0.0, min(cap_ease, 30.0))
cuff_turnback = max(0.0, min(cuff_turnback, 90.0))
vent_height = max(80.0, min(vent_height, 260.0))
button_rows = max(3, min(button_rows, 7))

# ── Roomy woven coat block (shirt frame, band-collar neckline) ───────────────
W = (chest_girth + coat_ease) / 4.0            # quarter body width
L = body_length
AH = (chest_girth + coat_ease) / 8.0 + 105.0   # roomy set-in armhole depth
AH = max(170.0, min(AH, L - 140.0))
NW = max(60.0, neck_girth / 5.0)               # half neck width at HPS
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 22.0
FRONT_NECK_DROP = max(70.0, neck_girth / 5.0 + 12.0)
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
CB_NECK_Y = HPS_Y - BACK_NECK_DROP
OVERLAP = 18.0                                 # collar end past CF (button line)
COLLAR_RISE = 12.0                             # band front-edge curl
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y
INNER_COL_X = 6.0                              # inner button column, just past CF
OUTER_COL_X = -(crossover - 26.0)             # outer column, near the wrap edge


def _armhole_edge():
    """Shared front/back armhole (roomy set-in; equal front/back for a clean
    solved cap — a chef coat sleeve is comfort-first, not a shaped tailored cap)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.36),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _front_neck_edge():
    """Front neck: OVERLAP line past CF, then the scoop up to HPS.

    The straight run from (-OVERLAP, CF_NECK_Y) to CF is where the band collar
    ends (button line); including it makes the per-half seam check
    collar.neck == front.neck + back.neck close exactly (casual-button-down idiom).
    """
    cf = fc.P(0.0, CF_NECK_Y)
    scoop = fc.Bezier(cf, fc.P(NW * 0.55, CF_NECK_Y),
                      fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))
    return fc.Edge("neck", [fc.Line(fc.P(-OVERLAP, CF_NECK_Y), cf), scoop])


def _button_column(label, x):
    """One vertical column of `button_rows` knot-button cross-marks."""
    top = CF_NECK_Y - 70.0
    bottom = max(150.0, CHEST_Y - 250.0)
    if button_rows > 1:
        bottom = min(bottom, top - 60.0 * (button_rows - 1))
    arm = 4.0
    marks = []
    for i in range(button_rows):
        y = top if button_rows == 1 else top - (top - bottom) * i / (button_rows - 1.0)
        marks.append(fc.Internal(
            f"{label} {i + 1}",
            [fc.P(x - arm, y), fc.P(x + arm, y), fc.P(x, y),
             fc.P(x, y - arm), fc.P(x, y + arm)],
            kind="drill",
        ))
    return marks


def _thermo_pocket_trace():
    """Chest thermometer / pen pocket placement (narrow patch, wearer's left)."""
    top = min(CHEST_Y + 30.0, CF_NECK_Y - 30.0)
    bottom = max(top - 150.0, 60.0)
    left = W * 0.34
    right = min(left + 55.0, W * 0.9)
    return fc.Internal(
        "thermometer pocket",
        [fc.P(left, top), fc.P(right, top), fc.P(right, bottom),
         fc.P(left, bottom), fc.P(left, top)],
        kind="trace",
    )


def build_front():
    """Front, cut 2 mirrored: center/wrap edge extended `crossover` past CF, two
    knot-button columns marked, chest thermometer pocket traced, side vent
    marked. Reversible construction (both fronts identical) is a note."""
    vh = min(vent_height, L - 60.0)
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, CF_NECK_Y)],
                    kind="marking"),
        fc.Internal("crossover edge guide",
                    [fc.P(-crossover, 0.0), fc.P(-crossover, CF_NECK_Y)],
                    kind="marking"),
        fc.Internal("side vent stop", [fc.P(W, vh), fc.P(W - 40.0, vh)],
                    kind="marking"),
        _thermo_pocket_trace(),
    ]
    internals += _button_column("outer button", OUTER_COL_X)
    internals += _button_column("inner button", INNER_COL_X)
    neck = _front_neck_edge()
    cf_t = max(0.02, min(0.5, OVERLAP / neck.length(0.05)))
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-crossover, 0.0),
                                       fc.P(-crossover, CF_NECK_Y))]),
            fc.Edge("stand_top", [fc.Line(fc.P(-crossover, CF_NECK_Y),
                                          fc.P(-OVERLAP, CF_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-crossover, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": hem_allowance},
        notches=[fc.Notch("side", 0.5, "side seam match"),
                 fc.Notch("armhole", 0.5, "front armhole"),
                 fc.Notch("neck", cf_t, "CF / collar end")],
        grainline=fc.Grainline(fc.P(W * 0.55, 80.0), fc.P(W * 0.55, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (double-breasted, cut 2)",
    )


def build_back():
    """Back, cut 1 on fold at CB: band-collar neckline, straight hem, side vent
    marked to match the front."""
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, CB_NECK_Y), fc.P(NW * 0.55, CB_NECK_Y),
                   fc.P(NW, CB_NECK_Y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    vh = min(vent_height, L - 60.0)
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
        grainline=fc.Grainline(fc.P(W * 0.55, 80.0), fc.P(W * 0.55, L - 120.0)),
        internals=[fc.Internal("side vent stop",
                               [fc.P(W, vh), fc.P(W - 40.0, vh)], kind="marking")],
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
    """One-piece sleeve: cap solved by bisection to the front + back armholes
    PLUS the small declared cap ease. Carries a turn-back cuff fold line and a
    sleeve-pocket trace (the chef's classic thermometer/pen sleeve pocket)."""
    ch = max(60.0, AH * 0.34)                      # comfortable cap height
    sl = max(80.0, sleeve_length - ch)             # underarm-to-hem length
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
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
    chw = max(80.0, hb * 0.74)                      # cuff opening half-width
    internals = []
    tb = min(cuff_turnback, sl - 40.0)
    if tb > 5.0:
        internals.append(fc.Internal(
            "turn-back cuff fold", [fc.P(-chw, tb), fc.P(chw, tb)], kind="marking"))
    # Sleeve pocket on the outer sleeve, above the cuff line.
    pk_bot = max(tb + 30.0, sl * 0.28)
    pk_top = min(pk_bot + 120.0, sl - 20.0)
    if pk_top > pk_bot + 20.0:
        internals.append(fc.Internal(
            "sleeve pocket",
            [fc.P(chw * 0.15, pk_bot), fc.P(chw * 0.75, pk_bot),
             fc.P(chw * 0.75, pk_top), fc.P(chw * 0.15, pk_top),
             fc.P(chw * 0.15, pk_bot)],
            kind="trace"))
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
        notches=[fc.Notch("cap", 0.5, "shoulder match"), fc.Notch("hem", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.6)),
        internals=internals,
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
    """Stand/band (mandarin) collar, half on fold at CB: neck edge bisected to
    half_target = front.neck (one side, incl. overlap) + back.neck (half). A
    small forward-leaning front edge; gently curved top. Turndown variant is a
    construction note — see docs/README.md."""
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
    point = fc.P(flat + 6.0, COLLAR_RISE + collar_height)
    top_start = fc.P(0.0, collar_height)
    piece = fc.Piece(
        "collar",
        [
            _collar_neck_edge(flat),
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_RISE), point)]),
            fc.Edge("top", [fc.curve_through(point, top_start, bulge=0.03, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(flat * 0.20, collar_height * 0.55),
                               fc.P(flat * 0.75, collar_height * 0.55 + 6.0)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Band Collar (half, on fold)",
    )
    return piece, flat


def build_facing(front):
    """Straight crossover-front facing strip: length = the measured center +
    front-neck run + end allowances (declared as seam ease), width 90. It backs
    the double-breasted wrap so the button columns have a clean under-layer. A
    shaped facing is future work — see docs/README.md."""
    center_len = front.edge("center").length(0.05)
    neck_len = front.edge("neck").length(0.05)
    run = center_len + neck_len
    width = 95.0
    length = run + 2.0 * seam_allowance
    t_hps = (seam_allowance + center_len) / length
    return fc.Piece(
        "facing",
        [
            fc.Edge("long_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
            fc.Edge("inner", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                          # length already includes 2×sa
        notches=[fc.Notch("long_edge", t_hps, "CF neck / stand corner match")],
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0),
                               fc.P(length * 0.8, width / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Crossover Front Facing",
    )


def build():
    pattern = fc.PatternSet("chef-coat")
    front = build_front()
    back = build_back()
    cap_target = (front.edge("armhole").length(0.05)
                  + back.edge("armhole").length(0.05) + cap_ease)
    half_neck = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    center_len = front.edge("center").length(0.05)
    front_neck_len = front.edge("neck").length(0.05)
    names = ("front", "back", "sleeve", "collar", "facing")
    wanted = {name: target_piece in (name, "set") for name in names}
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
    if wanted["facing"]:
        pattern.add(build_facing(front))
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
                             [("front", "neck"), ("back", "neck")], tol=2.0)
    if wanted["facing"] and wanted["front"]:
        pattern.declare_seam([("facing", "long_edge")],
                             [("front", "center"), ("front", "neck")],
                             tol=3.0, ease=2.0 * seam_allowance)
    fabric_width = 1450.0                            # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.62)
    n_buttons = button_rows * 2 * 2                  # two columns × two fronts
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"crisp white cotton poplin at {fabric_width:.0f} mm width, "
                 f"62% marker efficiency; heavier 'manta-cruda' is the alt card"},
        {"item": "fusible interfacing (collar band + crossover fronts/facings)",
         "qty": 1, "unit": "set",
         "note": "band cut doubled on fold; front stands + facings fused so the "
                 "double-breasted wrap holds its shape"},
        {"item": "cloth knot (china) buttons Ø 12-15 mm", "qty": n_buttons,
         "unit": "pieces",
         "note": f"{button_rows} per column × 2 columns × 2 fronts = {n_buttons}; "
                 "hand-knotted from cloth cord traditionally, or purchased — hard "
                 "goods federate to Yantra4D (knotted/china button family), never "
                 "re-implemented here"},
        {"item": "polyester/cotton thread + universal needle 80/12", "qty": 1,
         "unit": "set", "note": "press collar and front stands hard as you sew"},
    ]
    pattern.metadata = {
        "fc100_rank": 87,
        "fabric_hint": "popelina-algodon",
        "family": "workwear_uniforms",
        "double_breasted": {
            "crossover_past_cf_mm": round(crossover, 1),
            "note": "right front wraps over left; each front cut identical for "
                    "reversible construction — see docs/README.md",
            "button_columns": 2,
            "buttons_per_column": button_rows,
            "outer_column_x_mm": round(OUTER_COL_X, 1),
            "inner_column_x_mm": round(INNER_COL_X, 1),
        },
        "cloth_buttons": {
            "total": n_buttons,
            "kind": "knotted cloth / china buttons",
            "hardware_ref": "Yantra4D knotted-button cartridge (federated)",
        },
        "band_collar": {
            "kind": "stand / mandarin",
            "height_mm": round(collar_height, 1),
            "half_target_mm": round(half_neck, 1),
            "flat_mm": None if collar_flat is None else round(collar_flat, 1),
            "turndown_variant": "small turndown is a construction note",
        },
        "neck_opening_full_mm": round(2.0 * half_neck, 1),
        "overlap_mm": OVERLAP,
        "armhole_each_mm": round((cap_target - cap_ease) / 2.0, 1),
        "cap_ease_mm": cap_ease,
        "cap_target_mm": round(cap_target, 1),
        "cuff_turnback_mm": round(cuff_turnback, 1),
        "vent_height_mm": round(vent_height, 1),
        "facing_run_mm": round(center_len + front_neck_len, 1),
        "facing_length_mm": round(center_len + front_neck_len + 2.0 * seam_allowance, 1),
        "drafting": "roomy woven chef coat on the shirt frame; wide crossover "
                    "double-breasted front with two marked knot-button columns; "
                    "band/mandarin collar and sleeve cap both solved by bisection "
                    "to the measured openings (collar ease 0, cap ease declared); "
                    "straight crossover facing verified against the front run; "
                    "side vents + turn-back cuff + thermometer/sleeve pockets are "
                    "marked (teaching-grade, reversible note in the readme)",
    }
    return pattern


result = build()

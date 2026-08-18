"""
Lab coat — FC-100 rank #88. Fashion Cabinet Garment Cartridge.

The classic knee-length white lab coat ("bata de laboratorio"): a long,
relaxed single-breasted coat cut to layer over street clothes. It is the
overcoat's coat frame (rank #63) simplified to a workwear staple — read
overcoat/main.py and blazer/main.py first; the front's center→lapel→gorge
break and the collar/facing solves are theirs, the three patch pockets are the
chore-coat's (rank #65).

What the lab coat is, exactly:
  - A one-piece FRONT cut 2 mirrored whose center edge runs up the button stand
    to the ROLL POINT, then breaks into a MODEST NOTCH LAPEL — a straight
    diagonal out to the lapel point at chest level — then a straight GORGE back
    in to the neck point (the blazer's notch, kept small for a coat that mostly
    hangs open). CF buttonhole cross-marks (5 by default), the roll line, and
    the chest + hip patch-pocket placements are internals.
  - A BACK cut 2 mirrored with a gently shaped CB seam (allowance 15), a CB
    VENT so a seated wearer isn't bound, and a HALF-BELT marking at waist level
    (the lab coat's cinch-at-the-back detail).
  - A CONVERTIBLE two-piece NOTCH COLLAR: an upper collar whose neck edge is
    solved by bisection to the measured front gorge + back neck (collar-band
    method), half on fold at CB. The classic collar/lapel notch gap is a
    construction note (docs/README.md).
  - A one-piece set-in SLEEVE whose cap is solved by bisection to the front +
    back armholes plus a small declared cap ease, with a cuff-tab marking (the
    lab coat's optional wrist tab).
  - A straight FRONT FACING strip verified against the measured center + lapel
    + gorge run (carries the buttonholes and the lapel fold).
  - THREE real PATCH POCKET pieces — the signature: a CHEST pocket (patch_chest,
    cut 1) carrying a PEN SLOT division mark, and two large HIP pockets
    (patch_hip, cut 2). Each is a chamfered-corner pouch whose top edge is the
    opening (hem-facing allowance) with a topstitch attach guide. Pockets are
    topstitched appliqué: each outline is its own closed piece, its body
    placement an internal trace — never a balance seam.

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
# front|back|sleeve|collar|facing|patch_chest|patch_hip|set

chest_girth    = float(PARAM(lambda: chest_girth, 1040.0))
body_length    = float(PARAM(lambda: body_length, 1050.0))    # nape to hem (knee)
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 640.0))   # cap apex to wrist
coat_ease      = float(PARAM(lambda: coat_ease, 220.0))       # relaxed layering ease
button_stand   = float(PARAM(lambda: button_stand, 20.0))     # extension past CF
lapel_width    = float(PARAM(lambda: lapel_width, 72.0))      # notch lapel point past CF
roll_line_y    = float(PARAM(lambda: roll_line_y, 720.0))     # roll point above hem
collar_height  = float(PARAM(lambda: collar_height, 60.0))
cap_ease       = float(PARAM(lambda: cap_ease, 16.0))         # set-in cap ease
vent_height    = float(PARAM(lambda: vent_height, 280.0))     # CB vent above hem
buttons        = int(PARAM(lambda: buttons, 5))               # front closure buttons
pocket_width   = float(PARAM(lambda: pocket_width, 180.0))    # hip patch pocket
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 35.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1800.0))
body_length = max(880.0, min(body_length, 1250.0))
neck_girth = max(320.0, min(neck_girth, 540.0))
sleeve_length = max(480.0, min(sleeve_length, 760.0))
coat_ease = max(140.0, min(coat_ease, 360.0))
button_stand = max(15.0, min(button_stand, 35.0))
lapel_width = max(55.0, min(lapel_width, 100.0))
roll_line_y = max(520.0, min(roll_line_y, 900.0))
collar_height = max(45.0, min(collar_height, 80.0))
cap_ease = max(0.0, min(cap_ease, 35.0))
vent_height = max(180.0, min(vent_height, 420.0))
buttons = max(3, min(buttons, 7))
pocket_width = max(150.0, min(pocket_width, 240.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(20.0, min(hem_allowance, 55.0))

# ── Lab-coat block (overcoat coat frame, relaxed workwear proportions) ───────
W = (chest_girth + coat_ease) / 4.0            # quarter body width
L = body_length
NW = max(62.0, neck_girth / 5.0)               # half neck width at HPS
AH = (chest_girth + coat_ease) / 8.0 + 120.0   # coat-deep armhole (auto)
AH = max(210.0, min(AH, L - 460.0))            # chest line well above the waist
HPS_Y = L + 20.0
SHOULDER_DROP = 38.0                           # relaxed shoulder sits low
BACK_NECK_DROP = 26.0
SH_END = fc.P(W - 6.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y                           # chest line = lapel point level
ROLL_Y = max(260.0, min(roll_line_y, CHEST_Y - 70.0))  # roll point below chest
BS = button_stand
LW = lapel_width
ROLL_PT = fc.P(-BS, ROLL_Y)                    # center edge breaks here
LAPEL_PT = fc.P(-LW, CHEST_Y)                  # notch lapel point, past CF
NECK_PT = fc.P(NW, HPS_Y)                      # gorge lands on the neck point
CB_HEM_X, CB_WAIST_X = 8.0, 18.0               # CB seam waist shaping
CB_SA = 15.0                                   # CB seam allowance
VENT_W = 50.0                                  # CB vent underlap width
FACING_W = 100.0                               # straight front facing width
COLLAR_RISE = 15.0
# Chest patch pocket a touch smaller than the hip pockets (breast pocket).
CHEST_W = max(110.0, pocket_width - 55.0)
CHEST_H = CHEST_W + 20.0
HIP_H = pocket_width + 20.0                     # hip pockets slightly tall
POCKET_CHAMFER = 26.0                           # 45° bottom-corner chamfer
POCKET_HEM = 28.0                              # opening hem facing
TOPSTITCH_INSET = 10.0


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
    for _ in range(52):
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
                   fc.P(W - 7.0, UNDERARM.y + fah * 0.30), UNDERARM)],
    )


def _pocket_placement(label, cx, cy, w, h):
    """A patch-pocket placement rectangle (internal trace) on the body."""
    return fc.Internal(
        label,
        [fc.P(cx - w / 2.0, cy), fc.P(cx + w / 2.0, cy),
         fc.P(cx + w / 2.0, cy - h), fc.P(cx - w / 2.0, cy - h),
         fc.P(cx - w / 2.0, cy)],
        kind="trace",
    )


def _placements():
    """Chest + hip patch-pocket placement traces (wearer's side once mirrored).

    The chest pocket rides high on the wearer's left chest; the hip pocket sits
    low, well below the roll line, clear of the button stand and the armhole so
    the topstitch box lands on flat cloth."""
    chest_cx = W * 0.42
    chest_cy = min(CHEST_Y - 25.0, ROLL_Y + 150.0)
    hip_cx = W * 0.50
    hip_cy = min(ROLL_Y - 60.0, ROLL_Y - 40.0)
    hip_cy = max(hip_cy, HIP_H + 170.0)
    return [
        _pocket_placement("chest pocket placement", chest_cx, chest_cy,
                          CHEST_W, CHEST_H),
        _pocket_placement("hip pocket placement", hip_cx, hip_cy,
                          pocket_width, HIP_H),
    ]


def build_front():
    """Cut 2 mirror. Center edge = button stand up to the roll point; then the
    NOTCH lapel diagonal out to the lapel point at chest level; then a straight
    gorge in to the neck point. The roll line is an internal from roll point to
    neck point. Chest + hip patch-pocket placements are traced."""
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, ROLL_Y)],
                    kind="marking"),
        fc.Internal("roll line", [ROLL_PT, NECK_PT], kind="marking"),
    ]
    internals += _placements()
    # Evenly spaced buttons from the roll point downward.
    gap = min(110.0, (ROLL_Y - 100.0) / max(1, buttons - 1)) if buttons > 1 else 0.0
    for i in range(buttons):
        internals += _cross(f"buttonhole-{i + 1}", 0.0, ROLL_Y - i * gap)
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, 0.0), ROLL_PT)]),
            fc.Edge("lapel", [fc.Line(ROLL_PT, LAPEL_PT)]),
            fc.Edge("gorge", [fc.Line(LAPEL_PT, NECK_PT)]),
            fc.Edge("shoulder", [fc.Line(NECK_PT, SH_END)]),
            _armhole(15.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-BS, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("center", 1.0, "roll point"),
                 fc.Notch("side", 0.5),
                 fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.60, 120.0), fc.P(W * 0.60, L - 150.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Cut 2 mirror with a gently shaped CB seam (allowance 15) and a CB vent.
    The CB curves in to CB_WAIST_X at the roll-line level, straight above the
    chest. A half-belt marking sits at waist level on the back."""
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
    vh = min(vent_height, ROLL_Y - 40.0)
    belt_y = ROLL_Y - 10.0
    return fc.Piece(
        "back",
        [
            cb,
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole(11.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(CB_HEM_X, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": CB_SA, "hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(W * 0.58, 120.0), fc.P(W * 0.58, L - 150.0)),
        internals=[
            fc.Internal("CB vent underlap",
                        [fc.P(VENT_W, 0.0), fc.P(VENT_W, vh)], kind="marking"),
            fc.Internal("CB vent stop",
                        [fc.P(CB_HEM_X + 2.0, vh), fc.P(VENT_W, vh)],
                        kind="marking"),
            fc.Internal("half-belt (RH strap)",
                        [fc.P(W * 0.28, belt_y), fc.P(W * 0.80, belt_y)],
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
    """One-piece set-in sleeve: cap solved by bisection to the front + back
    armholes PLUS the declared cap ease. A gentle outward bow on the back
    underarm adds well under 1 mm over the straight front underarm (inside the
    declared tol). A cuff-tab marking is the lab coat's optional wrist tab."""
    cap_target = front_ah + back_ah + cap_ease
    ch = max(80.0, AH * 0.32)
    sl = max(240.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 70.0
    for _ in range(52):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs {cap_target:.1f}"
        )
    chw = max(120.0, min(hb * 0.62, hb - 10.0))
    tab_y = 90.0                                 # cuff-tab line above the hem
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
        grainline=fc.Grainline(fc.P(0.0, 50.0), fc.P(0.0, sl * 0.8)),
        internals=[
            fc.Internal("elbow line",
                        [fc.P(-hb * 0.9, sl * 0.54), fc.P(hb * 0.9, sl * 0.54)],
                        kind="marking"),
            fc.Internal("cuff tab line",
                        [fc.P(-chw * 0.55, tab_y), fc.P(chw * 0.55, tab_y)],
                        kind="marking"),
        ],
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
    measured front gorge + back neck per half (collar-band method). A modest
    forward point makes the convertible notch collar. The classic 10 mm
    collar/lapel notch gap is a construction note — see docs/README.md."""
    target = gorge_len + back_neck_len
    flat = _solve_flat(_collar_neck, target, "upper-collar neck")
    neck = _collar_neck(flat)
    point = fc.P(flat + 16.0, COLLAR_RISE + collar_height)
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
    """Straight front facing strip: length = the measured center + lapel + gorge
    run + end allowances (declared as seam ease), width 100. A shaped facing
    that mirrors the lapel is future work — see docs/README.md."""
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


def _patch_pocket(name, w, h, qty, label, pen_slot=False):
    """A real patch-pocket piece: a hexagon with 45° chamfered bottom corners,
    the top edge is the opening (hem-facing allowance), a topstitch guide traces
    the attach path inside the sides and bottom (patch-pocket enabler method).
    Cut `qty` — appliquéd to the body, not sewn as a balance seam. The chest
    pocket carries a PEN SLOT: a vertical division line partitioning the pouch
    so it holds pens upright (the lab coat's signature)."""
    c = min(POCKET_CHAMFER, min(w, h) / 3.0 - 0.5)
    inset = TOPSTITCH_INSET
    internals = [fc.Internal(
        "topstitch guide",
        [fc.P(w - inset, h), fc.P(w - inset, inset),
         fc.P(inset, inset), fc.P(inset, h)],
    )]
    if pen_slot:
        # Pen slot: a vertical topstitch division near the right third of the
        # pocket, from the opening down to just above the bottom.
        slot_x = w * 0.68
        internals.append(fc.Internal(
            "pen slot", [fc.P(slot_x, h - inset), fc.P(slot_x, inset + 6.0)],
            kind="marking"))
    return fc.Piece(
        name,
        [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, c))]),
            fc.Edge("chamfer_r", [fc.Line(fc.P(w, c), fc.P(w - c, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w - c, 0.0), fc.P(c, 0.0))]),
            fc.Edge("chamfer_l", [fc.Line(fc.P(c, 0.0), fc.P(0.0, c))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, c), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": POCKET_HEM},
        notches=[fc.Notch("top", 0.5, "center match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.15), fc.P(w / 2.0, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("lab-coat")
    front = build_front()
    back = build_back()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    center_len = front.edge("center").length(0.05)
    lapel_len = front.edge("lapel").length(0.05)
    gorge_len = front.edge("gorge").length(0.05)
    back_neck_len = back.edge("neck").length(0.05)
    front_run = center_len + lapel_len + gorge_len

    names = ("front", "back", "sleeve", "collar", "facing",
             "patch_chest", "patch_hip")
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
    if wanted["patch_chest"]:
        pattern.add(_patch_pocket("patch_chest", CHEST_W, CHEST_H, 1,
                                  "Chest Patch Pocket", pen_slot=True))
    if wanted["patch_hip"]:
        pattern.add(_patch_pocket("patch_hip", pocket_width, HIP_H, 2,
                                  "Hip Patch Pocket"))

    # ── Declared seams (every sewn relationship; all balance to delta ≈ 0) ────
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

    # ── BOM (white cotton shell + interfacing + buttons + thread) ────────────
    fabric_width = 1450.0                        # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"white cotton poplin at {fabric_width:.0f} mm width, 60% "
                 "marker efficiency; knee-length single-breasted lab coat with "
                 "3 patch pockets; manta-cruda is a heavier alternative"},
        {"item": "fusible interfacing (fronts, lapels, upper collar, facing)",
         "qty": 1, "unit": "set",
         "note": "shirt/coat-weight fusible: fuse the front edges and lapels, "
                 "the upper collar, and the facing before sewing"},
        {"item": "lab-coat buttons 18 mm", "qty": buttons, "unit": "pcs",
         "note": f"{buttons} CF closure; hardware is a Yantra4D cartridge "
                 "(shank-button guide), never re-implemented here"},
        {"item": "polyester thread + universal needle 80/12", "qty": 1,
         "unit": "set",
         "note": "topstitch every patch-pocket edge and the front/collar edges; "
                 "press crisp — poplin holds a hard press"},
    ]
    pattern.metadata = {
        "fc100_rank": 88,
        "fabric_hint": "popelina-algodon",
        "garment": "knee-length single-breasted white lab coat",
        "tailoring_note": "teaching-grade: one-piece set-in sleeve, straight "
                          "facing, fusible instead of canvas, single-layer "
                          "pocket bags, unlined — a shaped facing and cuff tabs "
                          "are future work",
        "coat_length_mm": round(L, 1),
        "layering_ease_mm": round(coat_ease, 1),
        "quarter_width_mm": round(W, 1),
        "lapel_style": "notch",
        "lapel_point_mm": [round(-LW, 1), round(CHEST_Y, 1)],
        "gorge_mm": round(gorge_len, 1),
        "back_neck_mm": round(back_neck_len, 1),
        "collar_neck_target_mm": round(gorge_len + back_neck_len, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_ease_mm": cap_ease,
        "cap_target_mm": round(front_ah + back_ah + cap_ease, 1),
        "front_edge_run_mm": round(front_run, 1),
        "facing_length_mm": round(front_run + 2.0 * seam_allowance, 1),
        "roll_line": {"roll_point_mm": [round(-BS, 1), round(ROLL_Y, 1)],
                      "neck_point_mm": [round(NW, 1), round(HPS_Y, 1)]},
        "buttonholes": {"count": buttons, "line": "CF (x=0)",
                        "stand_extension_mm": round(BS, 1),
                        "top_button_at": "roll point"},
        "vent": {"style": "CB vent", "height_mm": round(min(vent_height,
                 ROLL_Y - 40.0), 1), "underlap_mm": VENT_W},
        "half_belt": {"style": "back half-belt marking at waist level",
                      "y_mm": round(ROLL_Y - 10.0, 1)},
        "patch_pockets": {
            "count": 3, "layout": "2 hip + 1 chest (chest carries a pen slot)",
            "chest_mm": [round(CHEST_W, 1), round(CHEST_H, 1)],
            "hip_mm": [round(pocket_width, 1), round(HIP_H, 1)],
            "chamfer_mm": POCKET_CHAMFER, "hem_facing_mm": POCKET_HEM,
            "pen_slot": "vertical topstitch division on the chest pocket, near "
                        "the right third, so it holds pens upright",
            "attach": "topstitched appliqué — placement traced on the body, the "
                      "pocket outline is its own closed piece (not a balance seam)",
        },
        "seam_allowance_mm": round(seam_allowance, 1),
        "hem_allowance_mm": round(hem_allowance, 1),
        "notch_gap": "classic 10 mm collar/lapel notch gap in construction — "
                     "see docs/README.md",
        "drafting": "knee-length single-breasted lab coat on the overcoat coat "
                    "frame, relaxed for layering: center edge breaks at the roll "
                    "point into a modest NOTCH lapel and a straight gorge; shaped "
                    "CB seam with a vent and a half-belt marking; a one-piece "
                    "set-in sleeve solved to the summed armholes + 16 mm cap "
                    "ease with a cuff-tab marking; an upper collar solved to "
                    "gorge + back neck; a straight facing verified against the "
                    "measured front edge run; and three real patch pockets "
                    "(2 hip + 1 chest with a pen slot) appliquéd to marked "
                    "placements",
    }
    return pattern


result = build()

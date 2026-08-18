"""
Chore coat — FC-100 rank #65. Fashion Cabinet Garment Cartridge.

The classic French workwear chore coat ("chamarra de trabajo"): boxy,
hip-length, a CF button placket, a flat spread collar, a set-in sleeve, and —
the signature — three big PATCH POCKETS (two hip + one chest). Drafted as a
boxy woven jacket: a ONE-PIECE front cut 2 mirrored whose center edge extends
`button_stand` past CF (four buttonhole cross-marks on the CF line, chest +
hip patch-pocket placements traced as internals); a BACK split at the shoulder
line into a yoke (cut 1 on fold) over a back body (cut 1 on fold), the
workwear yoke seam; a set-in SLEEVE whose cap is solved by bisection to the
front + back armholes plus a small ease and closed at the wrist by a simple
button cuff band; a flat SPREAD COLLAR solved to the measured neckline + the
button overlap (collar-band bisection method), half on fold at CB; and three
real PATCH POCKET pieces (patch_chest cut 1, patch_hip cut 2) — each a
chamfered-corner pouch whose top edge is the opening, carrying a hem facing
and a topstitch attach guide. The pockets are topstitched appliqué: their
outline is its own closed piece and their body placements are internal traces,
never a balance seam.

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
# front|back_yoke|back_body|sleeve|cuff|collar|patch_chest|patch_hip|set

chest_girth    = float(PARAM(lambda: chest_girth, 1040.0))
body_length    = float(PARAM(lambda: body_length, 720.0))    # nape to hem (hip)
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 620.0))  # cap apex to wrist
woven_ease     = float(PARAM(lambda: woven_ease, 220.0))     # boxy workwear ease
yoke_depth     = float(PARAM(lambda: yoke_depth, 120.0))     # HPS to back-yoke seam
button_stand   = float(PARAM(lambda: button_stand, 35.0))    # extension past CF
collar_height  = float(PARAM(lambda: collar_height, 75.0))   # spread-collar fall
wrist_opening  = float(PARAM(lambda: wrist_opening, 250.0))
pocket_width   = float(PARAM(lambda: pocket_width, 175.0))   # hip patch pocket
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1800.0))
body_length = max(560.0, min(body_length, 950.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
sleeve_length = max(420.0, min(sleeve_length, 760.0))
woven_ease = max(140.0, min(woven_ease, 420.0))
yoke_depth = max(90.0, min(yoke_depth, 190.0))
button_stand = max(24.0, min(button_stand, 55.0))
collar_height = max(55.0, min(collar_height, 100.0))
wrist_opening = max(200.0, min(wrist_opening, 320.0))
pocket_width = max(140.0, min(pocket_width, 240.0))

# ── Boxy chore-coat block (drop-shoulder-ish, deep set-in armhole) ───────────
W = (chest_girth + woven_ease) / 4.0            # quarter body width
L = body_length
NW = max(60.0, neck_girth / 5.0)                # half neck width at HPS
AH = (chest_girth + woven_ease) / 8.0 + 120.0   # jacket-deep armhole (auto)
AH = max(200.0, min(AH, L - 150.0))
HPS_Y = L + 20.0
SHOULDER_DROP = 32.0
BACK_NECK_DROP = 22.0                           # HPS to CB nape
FRONT_NECK_DROP = max(70.0, NW + 8.0)
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
CB_NECK_Y = HPS_Y - BACK_NECK_DROP
YOKE_Y = HPS_Y - yoke_depth                     # back yoke seam height
YOKE_Y = min(YOKE_Y, CB_NECK_Y - 40.0)          # keep the yoke clear of the neck
YOKE_Y = max(YOKE_Y, HPS_Y - AH - 20.0)         # and clear of the underarm
BS = button_stand
OVERLAP = 15.0                                  # collar end past CF (button line)
COLLAR_RISE = 16.0
COLLAR_POINT = 22.0                             # forward spread of the collar tip
CAP_EASE = 18.0                                 # set-in sleeve cap ease
CUFF_H = 2.0 * 55.0                             # cut doubled, folded at mid
CUFF_OVERLAP = 25.0
BUTTONS = 4                                     # CF chore-coat buttons
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
# Chest patch pocket a touch smaller than the hip pockets (breast pocket).
CHEST_W = max(120.0, pocket_width - 45.0)
CHEST_H = CHEST_W + 15.0
HIP_H = pocket_width + 25.0                      # hip pockets slightly tall
POCKET_CHAMFER = 28.0
POCKET_HEM = 28.0                               # opening hem facing
TOPSTITCH_INSET = 10.0


def _cross(label, x, y, half=4.0):
    """Drill cross-mark as two internals (denim-jacket / zipper-notion idiom)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


def _solve_flat(edge_fn, target, what):
    """Bisect a monotonic flat-length → measured-curve-length edge builder."""
    lo, hi = target * 0.65, target * 1.05
    for _ in range(56):
        mid = (lo + hi) / 2.0
        if edge_fn(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(edge_fn(flat).length(0.05) - target) > 1.0:
        raise ValueError(f"{what} solver did not converge on {target:.1f} mm")
    return flat


def _front_armhole():
    """Deep set-in front armhole: HPS shoulder end down to the underarm."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 16.0, SH_END.y - AH * 0.34),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _back_armhole():
    """Back body armhole: shoulder end down to the underarm, shallower scoop.

    The shoulder end sits at the yoke seam corner? No — the back is split at
    the shoulder LINE only on the yoke; the armhole is carried fully on the
    back BODY from the yoke's side corner. We reproduce the shoulder end on
    the body so front and back caps still meet at the shoulder point.
    """
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.36),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _buttonhole_marks():
    """CF line + four buttonhole crosses on x = 0, evenly spaced."""
    marks = [fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, CF_NECK_Y)],
                         kind="marking")]
    top = CF_NECK_Y - 65.0
    bottom = max(140.0, top - 460.0)
    step = (top - bottom) / (BUTTONS - 1)
    for i in range(BUTTONS):
        y = top - i * step
        marks += _cross(f"buttonhole-{i + 1}", 0.0, y)
    return marks


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

    The chest pocket rides high on the wearer's left chest; the hip pocket
    sits low toward the side seam. Both are drawn clear of the button stand
    and the armhole so the topstitch box lands on flat cloth.
    """
    chest_cx = W * 0.40
    chest_cy = min(UNDERARM.y - 20.0, CF_NECK_Y - 55.0)
    hip_cx = W * 0.52
    hip_cy = min(0.0 + 150.0 + HIP_H, UNDERARM.y - HIP_H - 60.0)
    hip_cy = max(hip_cy, 150.0 + HIP_H)
    return [
        _pocket_placement("chest pocket placement", chest_cx, chest_cy,
                          CHEST_W, CHEST_H),
        _pocket_placement("hip pocket placement", hip_cx, hip_cy,
                          pocket_width, HIP_H),
    ]


def build_front():
    """Front, cut 2 mirrored: center edge extended button_stand past CF, four
    buttonhole crosses, chest + hip patch-pocket placements, full armhole."""
    neck = fc.Edge(
        "neck",
        [fc.Line(fc.P(-OVERLAP, CF_NECK_Y), fc.P(0.0, CF_NECK_Y)),
         fc.Bezier(fc.P(0.0, CF_NECK_Y), fc.P(NW * 0.55, CF_NECK_Y),
                   fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    cf_t = max(0.02, min(0.5, OVERLAP / neck.length(0.05)))
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, 0.0), fc.P(-BS, CF_NECK_Y))]),
            fc.Edge("stand_top",
                    [fc.Line(fc.P(-BS, CF_NECK_Y), fc.P(-OVERLAP, CF_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _front_armhole(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-BS, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": 25.0, "center": 25.0},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole"),
                 fc.Notch("neck", cf_t, "CF / collar end"),
                 fc.Notch("hem", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(W * 0.66, 80.0), fc.P(W * 0.66, L - 120.0)),
        internals=[*_placements(), *_buttonhole_marks()],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back_yoke():
    """Back yoke, cut 1 on fold at CB: carries the back neck + both shoulders,
    straight lower edge at the yoke seam (workwear back-yoke precedent)."""
    nape = fc.P(0.0, CB_NECK_Y)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(nape, fc.P(NW * 0.55, nape.y),
                   fc.P(NW, nape.y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "back_yoke",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, YOKE_Y), nape)]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            fc.Edge("side", [fc.Line(SH_END, fc.P(W - 5.0, YOKE_Y))]),
            fc.Edge("bottom",
                    [fc.Line(fc.P(W - 5.0, YOKE_Y), fc.P(0.0, YOKE_Y))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "body match")],
        grainline=fc.Grainline(fc.P(W * 0.45, YOKE_Y + 15.0),
                               fc.P(W * 0.45, YOKE_Y + yoke_depth * 0.6)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back Yoke",
    )


def build_back_body():
    """Back body, cut 1 on fold at CB: yoke seam at the top, full back armhole
    below it, straight side and hem."""
    return fc.Piece(
        "back_body",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, YOKE_Y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, YOKE_Y), fc.P(W - 5.0, YOKE_Y))]),
            fc.Edge("yoke_side", [fc.Line(fc.P(W - 5.0, YOKE_Y), SH_END)]),
            _back_armhole(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": 25.0},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("top", 0.5, "yoke match"),
                 fc.Notch("hem", 0.5, "front match")],
        grainline=fc.Grainline(fc.P(W * 0.6, 60.0), fc.P(W * 0.6, YOKE_Y - 40.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back Body",
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
    """Set-in sleeve; cap solved by bisection to front + back armholes plus a
    small ease (CAP_EASE). Wrist closed by the cuff band; a placket is marked."""
    cap_target = front_ah + back_ah + CAP_EASE
    ch = max(90.0, AH * 0.32)
    sl = max(240.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    for _ in range(56):
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
    chw = max(110.0, min(wrist_opening / 2.0 + 40.0, hb - 12.0))
    px = chw * 0.55                              # wrist placket, back of the sleeve
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},      # wrist is cuffed, not hemmed
        notches=[fc.Notch("cap", back_ah / (front_ah + back_ah), "shoulder match"),
                 fc.Notch("hem", 0.5, "cuff match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.8)),
        internals=[
            fc.Internal("sleeve placket", [fc.P(px, 0.0), fc.P(px, 120.0)],
                        kind="marking"),
            fc.Internal("placket stop", [fc.P(px - 4.0, 120.0), fc.P(px + 4.0, 120.0)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_cuff():
    """Rectangular buttoned cuff, cut doubled in height and folded at mid."""
    length = wrist_opening + CUFF_OVERLAP + 2.0 * seam_allowance
    internals = [fc.Internal("fold line",
                             [fc.P(0.0, CUFF_H / 2.0), fc.P(length, CUFF_H / 2.0)],
                             kind="marking")]
    internals += _cross("cuff buttonhole", seam_allowance + 14.0, CUFF_H * 0.25)
    internals += _cross("cuff button", length - seam_allowance - 14.0,
                        CUFF_H * 0.25)
    return fc.Piece(
        "cuff",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, CUFF_H))]),
            fc.Edge("top", [fc.Line(fc.P(length, CUFF_H), fc.P(0.0, CUFF_H))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, CUFF_H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                      # length already includes 2×sa
        grainline=fc.Grainline(fc.P(length * 0.2, CUFF_H / 2.0 + 14.0),
                               fc.P(length * 0.8, CUFF_H / 2.0 + 14.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Cuff",
    )


def _collar_neck(flat):
    """Flat spread-collar neck edge (gentle curve, collar-band method)."""
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_RISE),
                          bulge=0.06, side=-1.0)],
    )


def build_collar(half_neck):
    """Flat spread collar, half on fold at CB: neck edge solved by bisection to
    the half neckline + button overlap. A forward point gives the spread."""
    target = half_neck + OVERLAP
    flat = _solve_flat(_collar_neck, target, "collar neck")
    neck = _collar_neck(flat)
    point = fc.P(flat + COLLAR_POINT, COLLAR_RISE + collar_height)
    top_start = fc.P(0.0, collar_height)
    t_cf = half_neck / target                    # CF button line along the neck
    return fc.Piece(
        "collar",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_RISE), point)]),
            fc.Edge("top",
                    [fc.curve_through(point, top_start, bulge=0.05, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match"),
                 fc.Notch("neck", t_cf, "CF / button line")],
        grainline=fc.Grainline(fc.P(flat * 0.2, collar_height * 0.5),
                               fc.P(flat * 0.75,
                                    collar_height * 0.5 + COLLAR_RISE * 0.7)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Spread Collar (half, on fold)",
    )


def _patch_pocket(name, w, h, qty, label):
    """A real patch-pocket piece: a hexagon with 45° chamfered bottom corners,
    the top edge is the opening (hem-facing allowance), a topstitch guide
    traces the attach path inside the sides and bottom (patch-pocket enabler
    method). Cut `qty` — appliquéd to the body, not sewn as a balance seam."""
    c = min(POCKET_CHAMFER, min(w, h) / 3.0 - 0.5)
    inset = TOPSTITCH_INSET
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
        internals=[fc.Internal(
            "topstitch guide",
            [fc.P(w - inset, h), fc.P(w - inset, inset),
             fc.P(inset, inset), fc.P(inset, h)],
        )],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("chore-coat")
    front = build_front()
    back_yoke = build_back_yoke()
    back_body = build_back_body()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back_body.edge("armhole").length(0.05)
    half_neck = (front.edge("neck").length(0.05)
                 + back_yoke.edge("neck").length(0.05))
    names = ("front", "back_yoke", "back_body", "sleeve", "cuff", "collar",
             "patch_chest", "patch_hip")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back_yoke"]:
        pattern.add(back_yoke)
    if wanted["back_body"]:
        pattern.add(back_body)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(front_ah, back_ah))
    if wanted["cuff"]:
        pattern.add(build_cuff())
    if wanted["collar"]:
        pattern.add(build_collar(half_neck))
    if wanted["patch_chest"]:
        pattern.add(_patch_pocket("patch_chest", CHEST_W, CHEST_H, 1,
                                  "Chest Patch Pocket"))
    if wanted["patch_hip"]:
        pattern.add(_patch_pocket("patch_hip", pocket_width, HIP_H, 2,
                                  "Hip Patch Pocket"))

    # ── Declared seams (all balance to delta ≈ 0) ────────────────────────────
    if wanted["front"] and wanted["back_body"]:
        pattern.declare_seam(("front", "side"), ("back_body", "side"), tol=1.5)
    if wanted["front"] and wanted["back_yoke"]:
        pattern.declare_seam(("front", "shoulder"), ("back_yoke", "shoulder"),
                             tol=1.5)
    if wanted["back_yoke"] and wanted["back_body"]:
        pattern.declare_seam(("back_yoke", "bottom"), ("back_body", "top"),
                             tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back_body"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back_body", "armhole")],
                             tol=2.0, ease=CAP_EASE)
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
    if wanted["collar"] and wanted["front"] and wanted["back_yoke"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front", "neck"), ("back_yoke", "neck")],
                             tol=2.0, ease=OVERLAP)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1500.0                        # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "mezclilla-denim", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 60% marker efficiency; "
                 "boxy hip-length chore coat with 3 patch pockets"},
        {"item": "jean tack buttons 17 mm", "qty": BUTTONS + 2, "unit": "pcs",
         "note": f"{BUTTONS} CF placket + 2 cuffs; hardware is a Yantra4D "
                 "cartridge (tack-button / shank-button guide), never "
                 "re-implemented here"},
        {"item": "heavy topstitch thread (contrast) + jeans needle 100/16",
         "qty": 1, "unit": "set",
         "note": "workwear topstitch: fell the load-bearing side and armhole "
                 "seams; double-topstitch the placket, yoke, collar, and every "
                 "patch-pocket edge (3 mm gauge)"},
        {"item": "fusible interfacing (collar + button stand)", "qty": 1,
         "unit": "set",
         "note": "spread collar cut doubled on fold; the CF stand fused full "
                 "length under the buttonholes"},
    ]
    pattern.metadata = {
        "fc100_rank": 65,
        "fabric_hint": "mezclilla-denim",
        "half_neckline_mm": round(half_neck, 1),
        "collar_neck_target_mm": round(half_neck + OVERLAP, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_target_mm": round(front_ah + back_ah + CAP_EASE, 1),
        "cap_ease_mm": CAP_EASE,
        "yoke_seam_y_mm": round(YOKE_Y, 1),
        "buttons": {"count": BUTTONS, "line": "CF (x=0)",
                    "stand_extension_mm": BS},
        "patch_pockets": {
            "count": 3, "layout": "2 hip + 1 chest",
            "chest_mm": [round(CHEST_W, 1), round(CHEST_H, 1)],
            "hip_mm": [round(pocket_width, 1), round(HIP_H, 1)],
            "chamfer_mm": POCKET_CHAMFER, "hem_facing_mm": POCKET_HEM,
            "attach": "topstitched appliqué — placement traced on the body, "
                      "the pocket outline is its own closed piece (not a "
                      "balance seam)",
        },
        "topstitch": "heavy contrast, 3 mm gauge: placket, back yoke, collar, "
                     "pocket edges, and felled structural seams",
        "drafting": "boxy hip-length French workwear chore coat: one-piece "
                    "button-stand front, back split at the shoulder line into "
                    "a yoke over a back body (the workwear yoke seam), a flat "
                    "spread collar solved to the half neckline + overlap, a "
                    "set-in sleeve solved to the summed armholes + 18 mm cap "
                    "ease and closed by a buttoned cuff, and three real patch "
                    "pockets appliquéd to marked placements — teaching-grade: "
                    "collar fall and pocket bag are single-layer in v0",
    }
    return pattern


result = build()

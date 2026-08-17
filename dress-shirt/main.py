"""
Dress shirt — FC-100 rank #4. Fashion Cabinet Garment Cartridge.

The commons' first multi-solve chain ("camisa de vestir"): button-stand fronts
cut 2 with seven buttonhole cross-marks; a back cut on fold whose top edge ends
at the yoke seam; a yoke on fold carrying the back neck and both shoulders
(doubled in construction); a long sleeve whose cap is solved by bisection to
the front + back armholes, with a placket slit marking and a rectangular cuff;
a collar STAND whose neck edge is solved to the half neckline + overlap
(collar-band method); and a collar FALL whose neck edge is solved to the
stand's measured top edge — the second solve chained off the first.

Simplifications (docs/README.md): the full back armhole is drafted on the back
piece (real shirts split it across back + yoke); straight hem v0; slit placket.

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
# front|back|yoke|sleeve|cuff|stand|fall|set

chest_girth    = float(PARAM(lambda: chest_girth, 1020.0))
body_length    = float(PARAM(lambda: body_length, 760.0))    # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 620.0))  # cap apex to wrist
woven_ease     = float(PARAM(lambda: woven_ease, 140.0))     # total ease
button_stand   = float(PARAM(lambda: button_stand, 32.0))    # extension past CF
yoke_drop      = float(PARAM(lambda: yoke_drop, 100.0))      # HPS to yoke seam
wrist_opening  = float(PARAM(lambda: wrist_opening, 240.0))  # finished-ish girth
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(500.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(400.0, min(sleeve_length, 750.0))
woven_ease = max(60.0, min(woven_ease, 320.0))
button_stand = max(20.0, min(button_stand, 50.0))
yoke_drop = max(60.0, min(yoke_drop, 160.0))
wrist_opening = max(180.0, min(wrist_opening, 320.0))

# ── Woven shirt block (drop-shoulder rank #85 constants, yoke split) ─────────
W = (chest_girth + woven_ease) / 4.0          # quarter body width
L = body_length
AH = (chest_girth + woven_ease) / 8.0 + 95.0  # armhole depth (auto)
AH = max(AH, yoke_drop + 60.0)                # keep the armhole below the yoke
AH = max(160.0, min(AH, L - 120.0))
NW = max(60.0, neck_girth / 5.0)              # half neck width at HPS
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 25.0                         # HPS to CB nape (on the yoke)
FRONT_NECK_DROP = NW + 5.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
YOKE_Y = HPS_Y - yoke_drop                    # yoke seam height on the body
FNY = HPS_Y - FRONT_NECK_DROP                 # CF neck point height
BS = button_stand
OVERLAP = 15.0                                # collar-stand button extension
STAND_H, STAND_RISE = 30.0, 12.0
FALL_H, FALL_RISE, FALL_POINT = 60.0, 10.0, 45.0
CUFF_H = 2.0 * 65.0                           # cut doubled, folded at mid
CUFF_OVERLAP = 25.0
SLEEVE_FULLNESS = 1.15                        # pleated into the cuff
PLACKET_LEN = 130.0
BUTTONS = 7


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


def _front_armhole():
    fah = SH_END.y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - fah * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + fah * 0.30), UNDERARM)],
    )


def _back_armhole():
    """FULL back armhole on the back piece, from the yoke-seam end down."""
    top = fc.P(W - 5.0, YOKE_Y)
    bah = YOKE_Y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(top, fc.P(W - 14.0, YOKE_Y - bah * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + bah * 0.30), UNDERARM)],
    )


def build_front():
    """Cut 2 mirror; the center edge extends `button_stand` past CF (x=0)."""
    bh_top = FNY - 70.0
    bh_bottom = 150.0
    step = (bh_top - bh_bottom) / (BUTTONS - 1)
    internals = [fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, FNY)],
                             kind="marking")]
    for i in range(BUTTONS):
        internals += _cross(f"buttonhole-{i + 1}", 0.0, bh_top - i * step)
    neck = fc.Edge(
        "neck",
        [fc.Line(fc.P(-BS, FNY), fc.P(0.0, FNY)),
         fc.Bezier(fc.P(0.0, FNY), fc.P(NW * 0.55, FNY),
                   fc.P(NW, FNY + (HPS_Y - FNY) * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, 0.0), fc.P(-BS, FNY))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _front_armhole(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-BS, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.6, 80.0), fc.P(W * 0.6, L - 140.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Cut 1 on fold; the top edge ends at the yoke seam (back neck = yoke)."""
    origin = fc.P(0.0, 0.0)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(origin, fc.P(0.0, YOKE_Y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, YOKE_Y), fc.P(W - 5.0, YOKE_Y))]),
            _back_armhole(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("top", 0.5, "yoke match")],
        grainline=fc.Grainline(fc.P(W * 0.62, 80.0), fc.P(W * 0.62, YOKE_Y - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_yoke():
    """Cut 1 on fold, DOUBLED in construction. Own frame: bottom edge at y=0.

    Carries the back neck curve and the shoulder edges. Its side edge is
    straight and clear of the armhole — the full back armhole lives on the
    back piece (v0 simplification, see docs/README.md).
    """
    cb_h = yoke_drop - BACK_NECK_DROP            # CB height above the yoke seam
    hps = fc.P(NW, yoke_drop)
    sh_end = fc.P(W - 5.0, yoke_drop - SHOULDER_DROP)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, cb_h), fc.P(NW * 0.55, cb_h),
                   fc.P(NW, cb_h + BACK_NECK_DROP * 0.45), hps)],
    )
    return fc.Piece(
        "yoke",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, cb_h))]),
            neck,
            fc.Edge("shoulder", [fc.Line(hps, sh_end)]),
            fc.Edge("side", [fc.Line(sh_end, fc.P(W - 5.0, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(W - 5.0, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(W * 0.5, 12.0), fc.P(W * 0.5, cb_h * 0.75)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Yoke (doubled)",
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
    """Long sleeve; cap solved by bisection to front + back armholes (ease 0)."""
    cap_target = front_ah + back_ah
    ch = max(70.0, AH * 0.33)
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
    chw = max(100.0, min(wrist_opening * SLEEVE_FULLNESS / 2.0, hb - 10.0))
    px = chw * 0.55                              # placket slit, back of the wrist
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
        notches=[fc.Notch("cap", back_ah / cap_target, "shoulder match"),
                 fc.Notch("hem", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.8)),
        internals=[
            fc.Internal("sleeve placket slit",
                        [fc.P(px, 0.0), fc.P(px, PLACKET_LEN)], kind="marking"),
            fc.Internal("placket stop",
                        [fc.P(px - 4.0, PLACKET_LEN), fc.P(px + 4.0, PLACKET_LEN)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_cuff():
    """Rectangular cuff, cut doubled in height and folded at mid."""
    length = wrist_opening * 0.9 + CUFF_OVERLAP + 2.0 * seam_allowance
    internals = [fc.Internal("fold line",
                             [fc.P(0.0, CUFF_H / 2.0), fc.P(length, CUFF_H / 2.0)],
                             kind="marking")]
    internals += _cross("cuff buttonhole", seam_allowance + 12.0, CUFF_H * 0.25)
    internals += _cross("cuff button", length - seam_allowance - 12.0,
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


def _stand_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, STAND_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_stand(half_neck):
    """Collar stand, half on fold at CB — the collar-band method verbatim:
    neck edge solved to the half neckline + button overlap."""
    target = half_neck + OVERLAP
    flat = _solve_flat(_stand_neck, target, "collar-stand neck")
    neck = _stand_neck(flat)
    top_start = fc.P(0.0, STAND_H)
    top_end = fc.P(flat, STAND_RISE + STAND_H)
    t_cf = half_neck / target                    # CF button line along the neck
    return fc.Piece(
        "stand",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, STAND_RISE), top_end)]),
            fc.Edge("top",
                    [fc.curve_through(top_end, top_start, bulge=0.05, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match"),
                 fc.Notch("neck", t_cf, "CF / button line")],
        grainline=fc.Grainline(fc.P(flat * 0.2, STAND_H * 0.5),
                               fc.P(flat * 0.75, STAND_H * 0.5 + STAND_RISE * 0.7)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Collar Stand (half, on fold)",
    )


def _fall_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, FALL_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_fall(stand_top_len):
    """Collar fall, half on fold: neck edge solved to the stand's measured TOP
    edge — the second solve, chained off the first. Pointed front."""
    flat = _solve_flat(_fall_neck, stand_top_len, "collar-fall neck")
    neck = _fall_neck(flat)
    point = fc.P(flat + FALL_POINT, FALL_RISE + FALL_H)
    return fc.Piece(
        "fall",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, FALL_RISE), point)]),
            fc.Edge("top",
                    [fc.curve_through(point, fc.P(0.0, FALL_H),
                                      bulge=0.03, side=1.0)]),
            fc.Edge("cb", [fc.Line(fc.P(0.0, FALL_H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "stand match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, FALL_H * 0.55),
                               fc.P(flat * 0.7, FALL_H * 0.55)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Collar Fall (half, on fold)",
    )


def build():
    pattern = fc.PatternSet("dress-shirt")
    front = build_front()
    back = build_back()
    yoke = build_yoke()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    half_neck = front.edge("neck").length(0.05) + yoke.edge("neck").length(0.05)
    stand = build_stand(half_neck)
    stand_top_len = stand.edge("top").length(0.05)
    wanted = {
        name: target_piece in (name, "set")
        for name in ("front", "back", "yoke", "sleeve", "cuff", "stand", "fall")
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["yoke"]:
        pattern.add(yoke)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(front_ah, back_ah))
    if wanted["cuff"]:
        pattern.add(build_cuff())
    if wanted["stand"]:
        pattern.add(stand)
    if wanted["fall"]:
        pattern.add(build_fall(stand_top_len))
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    if wanted["front"] and wanted["yoke"]:
        pattern.declare_seam(("front", "shoulder"), ("yoke", "shoulder"), tol=1.5)
    if wanted["yoke"] and wanted["back"]:
        pattern.declare_seam(("yoke", "bottom"), ("back", "top"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
    if wanted["stand"] and wanted["front"] and wanted["yoke"]:
        pattern.declare_seam([("stand", "neck")],
                             [("front", "neck"), ("yoke", "neck")],
                             tol=2.0, ease=OVERLAP)
    if wanted["fall"] and wanted["stand"]:
        pattern.declare_seam([("fall", "neck")], [("stand", "top")], tol=2.0)
    fabric_width = 1450.0                        # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.65)
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 65% marker efficiency"},
        {"item": "fusible interfacing (stand, fall, cuffs, front stands)",
         "qty": 1, "unit": "set", "note": "shirt-weight; fuse before sewing"},
        {"item": "shirt buttons 11.5 mm", "qty": 10, "unit": "pcs",
         "note": "7 front + 2 cuffs + 1 collar stand; hardware is a Yantra4D "
                 "cartridge (shank-button), never re-implemented here"},
        {"item": "polyester thread + universal needle", "qty": 1, "unit": "set",
         "note": "sharp 80/12 for poplin"},
    ]
    pattern.metadata = {
        "fc100_rank": 4,
        "fabric_hint": "popelina-algodon",
        "half_neckline_mm": round(half_neck, 1),
        "stand_neck_mm": round(half_neck + OVERLAP, 1),
        "stand_top_mm": round(stand_top_len, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_target_mm": round(front_ah + back_ah, 1),
        "buttonholes": {"count": BUTTONS, "line": "CF (x=0)",
                        "stand_extension_mm": BS},
        "drafting": "woven yoke-split shirt block; full back armhole drafted on "
                    "the back piece; cap, stand neck, and fall neck solved by "
                    "bisection — fall chained to the stand's measured top edge",
    }
    return pattern


result = build()

"""
Flannel shirt — FC-100 rank #76. Fashion Cabinet Garment Cartridge.

The classic brushed-cotton casual flannel button-up ("camisa de franela"): a
relaxed woven shirt whose signature is that the cloth is PLAID and the craft is
matching the pattern across every seam. Structurally it is the dress-shirt
family solved for a soft, roomy flannel:

  - a CF button-stand FRONT cut 2 mirrored (center edge extended `button_stand`
    past CF, seven buttonhole cross-marks on the CF line), with a CURVED
    SHIRTTAIL hem (bezier) and a real CHEST PATCH POCKET whose placement is
    snapped to the plaid grid;
  - a BACK cut 1 on fold whose top edge ends at the yoke seam and whose hem is
    a deeper curved shirttail;
  - a YOKE cut 1 on fold (doubled in construction) carrying the back neck and
    both shoulders;
  - a set-in SLEEVE whose cap is SOLVED by bisection to the front + back
    armholes at zero ease, closed at the wrist by a barrel CUFF with a marked
    placket slit;
  - a two-piece TURNDOWN collar — a collar STAND solved to the measured
    neckline + the button overlap (collar-band bisection), and a collar FALL
    solved to the stand's measured top edge (the second solve chained off the
    first), the classic flannel collar;
  - a real chest PATCH POCKET (chamfered-corner pouch, patch-pocket enabler
    method) and its POCKET FLAP.

PLAID MATCHING (the signature, teaching-grade): flannel is a tartan grid of
repeat `plaid_repeat`. Pattern-matching across seams is modelled three ways —
(a) MATCH-POINT notches placed at whole plaid repeats down the side seams (both
body pieces share the side construction, so their match notches coincide when
sewn) and a repeat-spaced match notch on the back/yoke seam and the sleeve cap;
(b) the chest pocket + flap placement snapped so their top-left corner lands on
a plaid grid line (x,y multiples of `plaid_repeat`), so the pocket plaid reads
continuous with the body; (c) a BOM yardage MATCHING ALLOWANCE — one extra
plaid repeat per major seam is added to the fabric quantity, because plaid
matching wastes cloth. The `plaid_repeat` parameter drives the match-notch
spacing.

Simplifications (docs/README.md): the full back armhole is drafted on the back
piece (real shirts split it across back + yoke); the pocket bag and flap are
single-layer in v0; the curved shirttail is a symmetric bezier, not a drafted
sweep. Plaid MATCHING is expressed as notches + a grid-snapped placement +
a yardage allowance; the tartan itself is a fabric/render property, not drafted
thread-by-thread here.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import math

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
# front|back|yoke|sleeve|cuff|stand|fall|pocket|flap|set

chest_girth    = float(PARAM(lambda: chest_girth, 1060.0))
body_length    = float(PARAM(lambda: body_length, 760.0))    # nape to CB hem
neck_girth     = float(PARAM(lambda: neck_girth, 410.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 620.0))  # cap apex to wrist
woven_ease     = float(PARAM(lambda: woven_ease, 200.0))     # total; relaxed fit
button_stand   = float(PARAM(lambda: button_stand, 32.0))    # extension past CF
yoke_drop      = float(PARAM(lambda: yoke_drop, 105.0))      # HPS to yoke seam
wrist_opening  = float(PARAM(lambda: wrist_opening, 250.0))
collar_height  = float(PARAM(lambda: collar_height, 68.0))   # fall depth at CB
plaid_repeat   = float(PARAM(lambda: plaid_repeat, 40.0))    # tartan block (mm)
shirttail_drop = float(PARAM(lambda: shirttail_drop, 70.0))  # CB hem curve depth
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 15.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(500.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(400.0, min(sleeve_length, 750.0))
woven_ease = max(80.0, min(woven_ease, 400.0))
button_stand = max(20.0, min(button_stand, 50.0))
yoke_drop = max(60.0, min(yoke_drop, 160.0))
wrist_opening = max(180.0, min(wrist_opening, 320.0))
collar_height = max(45.0, min(collar_height, 90.0))
plaid_repeat = max(10.0, min(plaid_repeat, 120.0))
shirttail_drop = max(0.0, min(shirttail_drop, 140.0))

# ── Woven shirt block (dress-shirt yoke-split; casual flannel proportions) ───
W = (chest_girth + woven_ease) / 4.0          # quarter body width
L = body_length
AH = (chest_girth + woven_ease) / 8.0 + 95.0  # armhole depth (auto)
AH = max(AH, yoke_drop + 60.0)                # keep the armhole below the yoke
AH = max(170.0, min(AH, L - 120.0))
NW = max(60.0, neck_girth / 5.0)              # half neck width at HPS
HPS_Y = L + 20.0
SHOULDER_DROP = 34.0
BACK_NECK_DROP = 24.0                         # HPS to CB nape (on the yoke)
FRONT_NECK_DROP = max(70.0, NW + 6.0)
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
BS = button_stand
OVERLAP = 15.0                               # collar-stand button extension
STAND_H, STAND_RISE = 32.0, 12.0
FALL_RISE, FALL_POINT = 10.0, 40.0
CUFF_H = 2.0 * 62.0                           # cut doubled, folded at mid
CUFF_OVERLAP = 25.0
SLEEVE_FULLNESS = 1.15                        # eased/pleated into the cuff
PLACKET_LEN = 130.0
BUTTONS = 7
YOKE_Y = HPS_Y - yoke_drop                    # yoke seam height on the body
HEM_CORNER_Y = 0.0                            # side-seam / hem corner at the hip
FRONT_TAIL_Y = -shirttail_drop * 0.6          # CF hem hangs below the hip corner
BACK_TAIL_Y = -shirttail_drop                 # CB hem hangs deepest (shirttail)
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
# Chest patch pocket + flap (breast pocket, wearer's left once mirrored).
POCKET_W = max(115.0, min(W * 0.40, 150.0))
POCKET_H = POCKET_W + 15.0
POCKET_CHAMFER = 28.0
POCKET_HEM = 26.0                             # opening hem facing
FLAP_H = 55.0                                 # flap depth
TOPSTITCH_INSET = 8.0


def _snap(value, grid):
    """Snap a coordinate down to the nearest lower plaid grid line."""
    return grid * math.floor(value / grid)


def _cross(label, x, y, half=4.0):
    """Drill cross-mark as two internals (shirt-family convention)."""
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


def _side_edge():
    """Straight side seam, underarm → hip hem-corner. ONE construction for BOTH
    body pieces, so front.side == back.side exactly (the balance seam)."""
    return fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, HEM_CORNER_Y))])


SIDE_LEN = _side_edge().length(0.05)


def _plaid_side_notches(prefix):
    """MATCH-POINT notches down the side seam at whole plaid repeats.

    Both body pieces share `_side_edge`, so identical arc-fractions land on the
    same physical points — the plaid lines meet when the side seam is sewn.
    Placed from the underarm (t=0) downward every `plaid_repeat` mm.
    """
    marks = [fc.Notch("side", 0.5, f"{prefix} side")]
    n = 1
    while n * plaid_repeat < SIDE_LEN - plaid_repeat * 0.5:
        marks.append(fc.Notch("side", (n * plaid_repeat) / SIDE_LEN,
                              f"plaid match {n}"))
        n += 1
    return marks


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


def _front_hem():
    """Curved shirttail hem: from the hip side-corner (W, 0) sweeping DOWN to the
    front tail low point at CF. Closes onto the CF `center` bottom at
    (-BS, FRONT_TAIL_Y). Single smooth bezier — the classic rounded tail."""
    start = fc.P(W, HEM_CORNER_Y)
    end = fc.P(-BS, FRONT_TAIL_Y)
    return fc.Edge("hem", [
        fc.Bezier(start, fc.P(W * 0.66, FRONT_TAIL_Y),
                  fc.P(W * 0.30, FRONT_TAIL_Y), end),
    ])


def _back_hem():
    """Deeper curved shirttail on the back: hip side-corner down to the CB low
    point at (0, BACK_TAIL_Y), closing onto the CB `center` bottom."""
    start = fc.P(W, HEM_CORNER_Y)
    end = fc.P(0.0, BACK_TAIL_Y)
    return fc.Edge("hem", [
        fc.Bezier(start, fc.P(W * 0.70, BACK_TAIL_Y * 0.55),
                  fc.P(W * 0.34, BACK_TAIL_Y), end),
    ])


def _pocket_origin():
    """Top-left corner of the chest pocket, SNAPPED to the plaid grid.

    Snapping both x and y to whole `plaid_repeat` multiples (measured from the
    body origin) makes the pocket's tartan read continuous with the body cloth
    when it is cut on-grid — the plaid-matching craft for patch pockets.
    """
    raw_left = W * 0.30
    raw_top = min(UNDERARM.y - 25.0, CF_NECK_Y - 45.0)
    left = _snap(raw_left, plaid_repeat)
    top = _snap(raw_top, plaid_repeat)
    return fc.P(left, top)


def build_front():
    """Front, cut 2 mirrored: center edge extends `button_stand` past CF, seven
    buttonhole cross-marks, curved shirttail hem, plaid-matched pocket trace."""
    bh_top = CF_NECK_Y - 65.0
    bh_bottom = max(90.0, bh_top - 520.0)
    step = (bh_top - bh_bottom) / (BUTTONS - 1)
    internals = [fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, CF_NECK_Y)],
                             kind="marking")]
    for i in range(BUTTONS):
        internals += _cross(f"buttonhole-{i + 1}", 0.0, bh_top - i * step)
    # Chest-pocket placement trace, snapped to the plaid grid.
    po = _pocket_origin()
    internals.append(fc.Internal(
        "chest pocket placement (plaid-snapped)",
        [fc.P(po.x, po.y), fc.P(po.x + POCKET_W, po.y),
         fc.P(po.x + POCKET_W, po.y - POCKET_H), fc.P(po.x, po.y - POCKET_H),
         fc.P(po.x, po.y)],
        kind="trace",
    ))
    neck = fc.Edge(
        "neck",
        [fc.Line(fc.P(-BS, CF_NECK_Y), fc.P(0.0, CF_NECK_Y)),
         fc.Bezier(fc.P(0.0, CF_NECK_Y), fc.P(NW * 0.55, CF_NECK_Y),
                   fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    cf_t = max(0.02, min(0.5, OVERLAP / neck.length(0.05)))
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, FRONT_TAIL_Y),
                                       fc.P(-BS, CF_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _front_armhole(),
            _side_edge(),
            _front_hem(),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": hem_allowance},
        notches=[*_plaid_side_notches("front"),
                 fc.Notch("armhole", 0.5, "front armhole"),
                 fc.Notch("neck", cf_t, "CF / collar end")],
        grainline=fc.Grainline(fc.P(W * 0.60, 80.0), fc.P(W * 0.60, L - 140.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Back, cut 1 on fold at CB: top edge ends at the yoke seam (back neck is
    carried on the yoke), deeper curved shirttail hem, plaid match notches."""
    origin = fc.P(0.0, BACK_TAIL_Y)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(origin, fc.P(0.0, YOKE_Y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, YOKE_Y), fc.P(W - 5.0, YOKE_Y))]),
            _back_armhole(),
            _side_edge(),
            _back_hem(),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[*_plaid_side_notches("back"),
                 fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("top", 0.5, "yoke match")],
        grainline=fc.Grainline(fc.P(W * 0.62, 40.0), fc.P(W * 0.62, YOKE_Y - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_yoke():
    """Yoke, cut 1 on fold, DOUBLED in construction. Own frame: bottom at y=0.

    Carries the back neck curve and both shoulder edges. Straight side clear of
    the armhole — the full back armhole lives on the back piece (v0). A repeat-
    spaced match notch on the bottom edge lets the yoke plaid meet the back."""
    cb_h = yoke_drop - BACK_NECK_DROP            # CB height above the yoke seam
    hps = fc.P(NW, yoke_drop)
    sh_end = fc.P(W - 5.0, yoke_drop - SHOULDER_DROP)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, cb_h), fc.P(NW * 0.55, cb_h),
                   fc.P(NW, cb_h + BACK_NECK_DROP * 0.45), hps)],
    )
    bottom_len = W - 5.0
    yoke_matches = [fc.Notch("bottom", 0.5, "back match")]
    if plaid_repeat < bottom_len:
        yoke_matches.append(fc.Notch("bottom", plaid_repeat / bottom_len,
                                     "plaid match"))
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
        notches=yoke_matches,
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
    """Set-in sleeve; cap solved by bisection to front + back armholes (ease 0).
    Placket slit marked at the back of the wrist; a plaid match notch sits one
    repeat in from the underarm seam so the sleeve plaid meets the body."""
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
    underarm_len = fc.P(chw, 0.0).distance(fc.P(hb, sl))
    sleeve_notches = [fc.Notch("cap", back_ah / cap_target, "shoulder match"),
                      fc.Notch("hem", 0.5, "cuff match")]
    if plaid_repeat < underarm_len:
        sleeve_notches.append(
            fc.Notch("underarm_back", plaid_repeat / underarm_len, "plaid match"))
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
        notches=sleeve_notches,
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
    """Barrel cuff, cut doubled in height and folded at mid; a placket-side and
    a button-side buttonhole/button cross are marked."""
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
    """Collar stand, half on fold at CB — collar-band method: neck edge solved
    to the half neckline + button overlap."""
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
    edge — the second solve, chained off the first. Soft flannel point."""
    flat = _solve_flat(_fall_neck, stand_top_len, "collar-fall neck")
    neck = _fall_neck(flat)
    point = fc.P(flat + FALL_POINT, FALL_RISE + collar_height)
    return fc.Piece(
        "fall",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, FALL_RISE), point)]),
            fc.Edge("top",
                    [fc.curve_through(point, fc.P(0.0, collar_height),
                                      bulge=0.03, side=1.0)]),
            fc.Edge("cb", [fc.Line(fc.P(0.0, collar_height), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "stand match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, collar_height * 0.55),
                               fc.P(flat * 0.7, collar_height * 0.55)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Collar Fall (half, on fold)",
    )


def build_pocket():
    """Real chest patch pocket: a hexagon with 45° chamfered bottom corners
    (patch-pocket enabler method). Top edge is the opening (hem facing); a
    topstitch guide traces the attach path inside the sides and bottom. Cut on
    the plaid grid so its tartan matches the body at the snapped placement."""
    w, h = POCKET_W, POCKET_H
    c = min(POCKET_CHAMFER, min(w, h) / 3.0 - 0.5)
    inset = TOPSTITCH_INSET
    return fc.Piece(
        "pocket",
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
        notches=[fc.Notch("top", 0.5, "center / plaid match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.15), fc.P(w / 2.0, h * 0.85)),
        internals=[fc.Internal(
            "topstitch guide",
            [fc.P(w - inset, h), fc.P(w - inset, inset),
             fc.P(inset, inset), fc.P(inset, h)],
        )],
        cut=fc.CutSpec(quantity=1),
        label="Chest Patch Pocket",
    )


def build_flap():
    """Chest-pocket FLAP: a shallow rectangle with a chamfered lower edge that
    echoes the pocket, wider than the pocket by 2 mm each side to cover it. Top
    edge sews above the pocket; a buttonhole cross marks the closure."""
    w = POCKET_W + 4.0
    h = FLAP_H
    c = min(22.0, min(w, h) / 3.0 - 0.5)
    internals = _cross("flap buttonhole", w / 2.0, h * 0.30)
    return fc.Piece(
        "flap",
        [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, c))]),
            fc.Edge("chamfer_r", [fc.Line(fc.P(w, c), fc.P(w - c, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w - c, 0.0), fc.P(c, 0.0))]),
            fc.Edge("chamfer_l", [fc.Line(fc.P(c, 0.0), fc.P(0.0, c))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, c), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 0.5, "center match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.2), fc.P(w / 2.0, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Pocket Flap",
    )


def build():
    pattern = fc.PatternSet("flannel-shirt")
    front = build_front()
    back = build_back()
    yoke = build_yoke()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    half_neck = (front.edge("neck").length(0.05)
                 + yoke.edge("neck").length(0.05))
    stand = build_stand(half_neck)
    stand_top_len = stand.edge("top").length(0.05)
    names = ("front", "back", "yoke", "sleeve", "cuff", "stand", "fall",
             "pocket", "flap")
    wanted = {name: target_piece in (name, "set") for name in names}
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
    if wanted["pocket"]:
        pattern.add(build_pocket())
    if wanted["flap"]:
        pattern.add(build_flap())

    # ── Declared seams (all balance to delta ≈ 0) ────────────────────────────
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

    # ── BOM (flannel yardage + plaid-matching allowance) ─────────────────────
    fabric_width = 1700.0                        # felpa-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    base_len = total_area / (fabric_width * 0.62)
    # Plaid-matching allowance: one extra plaid repeat of length per major seam
    # that must match (side ×2, yoke/back, armholes ×2, collar), because every
    # match costs cloth. Expressed as a % uplift on the base marker length.
    matched_seams = 6
    match_allowance_mm = matched_seams * plaid_repeat
    match_pct = round(100.0 * match_allowance_mm / max(base_len, 1.0), 1)
    marker_len = base_len + match_allowance_mm
    pattern.bom = [
        {"item": "felpa-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 62% marker efficiency; "
                 f"INCLUDES a plaid-matching allowance of {match_allowance_mm:.0f} mm "
                 f"(+{match_pct}%): one {plaid_repeat:.0f} mm repeat per matched seam "
                 f"({matched_seams} seams). Cut every piece on-grain on the SAME "
                 "plaid grid; match the side, yoke, armhole, and collar notches."},
        {"item": "fusible interfacing (collar stand + fall, cuffs, front stands)",
         "qty": 1, "unit": "set",
         "note": "shirt-weight; keeps the soft flannel collar and cuffs crisp"},
        {"item": "shirt buttons Ø 11-12 mm", "qty": BUTTONS + 4, "unit": "pieces",
         "note": f"{BUTTONS} front + 2 cuffs + 1 collar stand + 1 pocket flap "
                 "(+ spare); hardware federates to Yantra4D (shank-button family), "
                 "never re-implemented here"},
        {"item": "all-purpose polyester thread + universal needle 80/12",
         "qty": 1, "unit": "set",
         "note": "match thread to the dominant plaid ground; brushed nap sheds — "
                 "clean the bobbin race often"},
    ]
    pattern.metadata = {
        "fc100_rank": 76,
        "fabric_hint": "felpa-algodon",
        "half_neckline_mm": round(half_neck, 1),
        "stand_neck_mm": round(half_neck + OVERLAP, 1),
        "stand_top_mm": round(stand_top_len, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_target_mm": round(front_ah + back_ah, 1),
        "yoke_seam_y_mm": round(YOKE_Y, 1),
        "buttonholes": {"count": BUTTONS, "line": "CF (x=0)",
                        "stand_extension_mm": BS},
        "collar": "two-piece turndown: stand solved to half neckline + overlap, "
                  "fall chained to the stand's measured top edge",
        "curved_hem_mm": {"cb_shirttail_drop": round(shirttail_drop, 1),
                          "front_tail_drop": round(shirttail_drop * 0.6, 1),
                          "note": "symmetric bezier shirttail; side/hem corner at "
                                  "the hip so front.side == back.side"},
        "plaid_matching": {
            "plaid_repeat_mm": round(plaid_repeat, 1),
            "side_match_notches": "whole-repeat notches down the shared side seam "
                                  "(front & back land on the same points)",
            "seam_match_notches": ["yoke.bottom↔back.top", "sleeve.cap↔armholes",
                                   "collar stand & fall CB"],
            "pocket": {
                "placement_origin_mm": [round(_pocket_origin().x, 1),
                                        round(_pocket_origin().y, 1)],
                "snapped_to_grid": True,
                "size_mm": [round(POCKET_W, 1), round(POCKET_H, 1)],
                "flap_mm": [round(POCKET_W + 4.0, 1), FLAP_H],
                "note": "top-left corner snapped to whole plaid repeats so the "
                        "pocket tartan reads continuous with the body",
            },
            "yardage_allowance_mm": round(match_allowance_mm, 1),
            "yardage_allowance_pct": match_pct,
        },
        "drafting": "casual brushed-flannel button-up on the dress-shirt yoke-split "
                    "block: seven-button CF stand, back ending at the yoke seam, "
                    "yoke carrying the back neck + shoulders, set-in sleeve solved "
                    "to the summed armholes, barrel cuff, two-piece turndown collar "
                    "(stand solved to the neckline, fall chained to the stand top), "
                    "curved shirttail hem, and a plaid-matched chest patch pocket + "
                    "flap. Teaching-grade: full back armhole on the back piece; "
                    "pocket/flap single-layer; plaid matching as notches + grid-"
                    "snapped placement + a yardage allowance, not drafted threads",
    }
    return pattern


result = build()

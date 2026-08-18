"""
Suit jacket — FC-100 rank #67. Fashion Cabinet Garment Cartridge.

The blazer's refined sibling ("saco de traje"): a teaching-grade two-button
single-breasted suit jacket drafted as the classic tailored THREE-PANEL body
(front + side body + back) with a TWO-PIECE sleeve (upper + under). Like the
blazer, the front's center edge climbs the button stand to the ROLL POINT at
waist level, then breaks into a straight notch LAPEL out to the lapel point and
a gorge edge back to the neck point; the roll line is marked from roll point to
neck point. Beyond the blazer it adds the tailored refinements a real suit
carries: the armhole is split three ways across front + side-body + back panels
(side-body seam gives the chest its shape without a visible princess line on
the front), the sleeve is a proper two-piece (upper sleeve carries the eased
cap, under sleeve tucks under at the forearm/hindarm seams), a breast welt and
two jetted-flap hip pockets are marked, the shoulder is lightly extended and
carries a pad + canvas placement note, and the jacket is drafted to be fully
lined (lining noted, BOM-costed, not drafted in v0).

Three seams are solved so every declared relationship balances to delta ~ 0:
the upper-sleeve cap is bisected to the measured front + side-body + back
armholes PLUS the declared cap ease (15-35 mm tailored cap), the upper collar
is bisected to the gorge + back neck, and the straight front facing length is
derived from the measured center + lapel + gorge run. No full canvas or drafted
lining in v0 — see docs/README.md.

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
# front|side_body|back|upper_sleeve|under_sleeve|collar|facing|set

chest_girth    = float(PARAM(lambda: chest_girth, 1020.0))
body_length    = float(PARAM(lambda: body_length, 730.0))    # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 630.0))  # cap apex to wrist
jacket_ease    = float(PARAM(lambda: jacket_ease, 130.0))    # total ease
button_stand   = float(PARAM(lambda: button_stand, 20.0))    # extension past CF
lapel_width    = float(PARAM(lambda: lapel_width, 90.0))     # lapel point past CF
roll_line_y    = float(PARAM(lambda: roll_line_y, 300.0))    # roll point above hem
collar_height  = float(PARAM(lambda: collar_height, 58.0))
cap_ease       = float(PARAM(lambda: cap_ease, 28.0))        # eased two-piece cap
shoulder_ext   = float(PARAM(lambda: shoulder_ext, 10.0))    # structured extension
vent_height    = float(PARAM(lambda: vent_height, 260.0))    # CB vent above hem
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 45.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1500.0))
body_length = max(560.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(420.0, min(sleeve_length, 760.0))
jacket_ease = max(90.0, min(jacket_ease, 260.0))
button_stand = max(15.0, min(button_stand, 35.0))
lapel_width = max(65.0, min(lapel_width, 115.0))
roll_line_y = max(230.0, min(roll_line_y, 430.0))
collar_height = max(45.0, min(collar_height, 85.0))
cap_ease = max(0.0, min(cap_ease, 40.0))
shoulder_ext = max(0.0, min(shoulder_ext, 25.0))
vent_height = max(150.0, min(vent_height, 320.0))
seam_allowance = max(8.0, min(seam_allowance, 20.0))
hem_allowance = max(25.0, min(hem_allowance, 60.0))

# ── Tailored suit-jacket block (dress-shirt frame, three-panel body) ─────────
W = (chest_girth + jacket_ease) / 4.0          # quarter body width
L = body_length
NW = max(60.0, neck_girth / 5.0)               # half neck width at HPS
AH = (chest_girth + jacket_ease) / 8.0 + 125.0  # jacket-deep armhole (auto)
AH = max(185.0, min(AH, L - 260.0))            # chest line well above the waist
HPS_Y = L + 20.0
SHOULDER_DROP = 38.0
BACK_NECK_DROP = 25.0
# Slightly extended, structured shoulder end (padded suit shoulder).
SH_END = fc.P(W - 5.0 + shoulder_ext, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y                           # chest level = lapel point level
ROLL_Y = max(120.0, min(roll_line_y, CHEST_Y - 60.0))  # roll point below chest
BS = button_stand
LW = lapel_width
ROLL_PT = fc.P(-BS, ROLL_Y)                    # center edge breaks here
LAPEL_PT = fc.P(-LW, CHEST_Y)                  # lapel point, past CF
NECK_PT = fc.P(NW, HPS_Y)                      # gorge lands on the neck point

# Three-panel split: the front-panel side seam sits inboard of the underarm;
# the side body is the panel between the front seam and the back seam and
# carries the underarm point. SEAM_X is the shared x of the two vertical
# body seams at the hem; the side body straddles the underarm at chest level.
SEAM_X = W * 0.62                              # front|side-body seam at the hem
SB_HALF = W - SEAM_X                           # side-body half-width at hem
CB_HEM_X, CB_WAIST_X = 8.0, 18.0              # CB seam waist shaping
CB_SA = 15.0                                   # CB seam allowance (inlay)
VENT_W = 48.0                                  # vent underlap width
DART_INTAKE = 16.0                             # front fisheye dart
FACING_W = 95.0                                # straight front facing width
COLLAR_RISE = 15.0
BUTTONS = 2
SLEEVE_BUTTONS = 4


def _cross(label, x, y, half=4.0):
    """Drill cross-mark as two internals (zipper-notion convention)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


def _solve_flat(edge_fn, target, what):
    """Bisect a monotonic flat-length -> measured-curve-length edge builder."""
    lo, hi = target * 0.55, target * 1.10
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


# ── Armholes (split across the three body panels) ────────────────────────────
def _front_armhole():
    """Front-panel armhole: shoulder end down to the front-seam top at chest."""
    top = SH_END
    bot = fc.P(SEAM_X, CHEST_Y + 12.0)          # front-seam top, just above chest
    span = top.y - bot.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(top, fc.P(top.x - 20.0, top.y - span * 0.42),
                   fc.P(SEAM_X + 22.0, bot.y + span * 0.30), bot)],
    )


def _sidebody_armhole():
    """Side-body armhole scoop: front-seam top over the underarm to back-seam
    top. This is the deep bottom of the scye."""
    a = fc.P(-SB_HALF, CHEST_Y + 12.0)          # front-seam top (side-body frame)
    u = fc.P(0.0, CHEST_Y - 6.0)                # underarm (deepest)
    b = fc.P(SB_HALF, CHEST_Y + 12.0)           # back-seam top
    return fc.Edge(
        "armhole",
        [fc.curve_through(a, u, bulge=0.16, side=1.0),
         fc.curve_through(u, b, bulge=0.16, side=1.0)],
    )


def _back_armhole():
    """Back-panel armhole: shoulder end down to the back-seam top at chest."""
    top = SH_END
    bot = fc.P(SEAM_X, CHEST_Y + 12.0)
    span = top.y - bot.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(top, fc.P(top.x - 16.0, top.y - span * 0.40),
                   fc.P(SEAM_X + 18.0, bot.y + span * 0.28), bot)],
    )


# ── Front-panel side seam (inboard princess-adjacent seam, hip to armhole) ───
def _front_side_seam():
    """Front-panel side seam: hem up to the front-armhole start at chest+12,
    with a gentle waist suppression bow. Mirrored on the side body's front
    seam so the two match to well under tol."""
    bot = fc.P(SEAM_X, 0.0)
    top = fc.P(SEAM_X, CHEST_Y + 12.0)
    return fc.Edge(
        "side_seam",
        [fc.curve_through(bot, top, bulge=0.02, side=1.0)],
    )


def _fisheye_dart():
    """Front fisheye dart, waist to chest: a closed diamond, widest at the
    roll-line level, intake 16 mm."""
    dx = SEAM_X * 0.52
    half = DART_INTAKE / 2.0
    y_bot = max(ROLL_Y - 100.0, 60.0)
    y_top = CHEST_Y - 45.0
    return fc.Internal(
        "front fisheye dart",
        [fc.P(dx, y_bot), fc.P(dx - half, ROLL_Y), fc.P(dx, y_top),
         fc.P(dx + half, ROLL_Y), fc.P(dx, y_bot)],
        kind="dart",
    )


def _breast_welt():
    """Left-chest breast-welt pocket marking: welt rectangle + placement line
    (slightly tilted outward, tailoring convention). Markings only in v0."""
    cx = SEAM_X * 0.46
    y = CHEST_Y - 18.0
    ww, wh = 105.0, 22.0
    tilt = 8.0
    welt = [fc.P(cx - ww / 2.0, y), fc.P(cx + ww / 2.0, y + tilt),
            fc.P(cx + ww / 2.0, y + tilt - wh), fc.P(cx - ww / 2.0, y - wh),
            fc.P(cx - ww / 2.0, y)]
    line = [fc.P(cx - ww / 2.0 - 6.0, y - wh / 2.0),
            fc.P(cx + ww / 2.0 + 6.0, y + tilt - wh / 2.0)]
    return [fc.Internal("breast welt", welt),
            fc.Internal("breast welt line", line)]


def _jetted_hip_pocket():
    """Jetted-flap hip-pocket markings: flap rectangle + jetted mouth line.
    Cut 2 mirror puts one on each front — markings only in v0."""
    cx = SEAM_X * 0.60
    attach = max(150.0, ROLL_Y - 120.0)
    fw, fh = 150.0, 55.0
    flap = [fc.P(cx - fw / 2.0, attach), fc.P(cx + fw / 2.0, attach),
            fc.P(cx + fw / 2.0, attach - fh), fc.P(cx - fw / 2.0, attach - fh),
            fc.P(cx - fw / 2.0, attach)]
    mouth = [fc.P(cx - fw / 2.0 - 6.0, attach), fc.P(cx + fw / 2.0 + 6.0, attach)]
    return [fc.Internal("hip jetted flap", flap),
            fc.Internal("hip pocket mouth", mouth)]


def build_front():
    """Cut 2 mirror. Center edge = button stand up to the roll point; then the
    lapel diagonal out to the lapel point; then the gorge in to the neck point;
    shoulder to the extended shoulder end; front armhole down to the front-seam
    top; front side seam down to the hem. The roll line is an internal from
    roll point to neck point."""
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, ROLL_Y)],
                    kind="marking"),
        fc.Internal("roll line", [ROLL_PT, NECK_PT], kind="marking"),
        _fisheye_dart(),
    ]
    internals += _breast_welt()
    internals += _jetted_hip_pocket()
    internals += _cross("buttonhole-1", 0.0, ROLL_Y)
    internals += _cross("buttonhole-2", 0.0, ROLL_Y - 95.0)
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, 0.0), ROLL_PT)]),
            fc.Edge("lapel", [fc.Line(ROLL_PT, LAPEL_PT)]),
            fc.Edge("gorge", [fc.Line(LAPEL_PT, NECK_PT)]),
            fc.Edge("shoulder", [fc.Line(NECK_PT, SH_END)]),
            _front_armhole(),
            _front_side_seam().reversed(),        # chest -> hem (CCW continues)
            fc.Edge("hem", [fc.Line(fc.P(SEAM_X, 0.0), fc.P(-BS, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("center", 1.0, "roll point"),
                 fc.Notch("side_seam", 0.5, "front waist"),
                 fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(SEAM_X * 0.55, 80.0),
                               fc.P(SEAM_X * 0.55, L - 150.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_side_body():
    """Cut 2 mirror. The tailored side panel: front seam (matches front side
    seam) up the left, side-body armhole scoop across the top over the
    underarm, back seam (matches back side seam) down the right, hem across the
    bottom. Frame centered on the underarm (x=0)."""
    fs_bot = fc.P(-SB_HALF, 0.0)
    fs_top = fc.P(-SB_HALF, CHEST_Y + 12.0)
    bs_top = fc.P(SB_HALF, CHEST_Y + 12.0)
    bs_bot = fc.P(SB_HALF, 0.0)
    return fc.Piece(
        "side_body",
        [
            # front seam: hem -> chest (bowed to mirror the front side seam)
            fc.Edge("front_seam",
                    [fc.curve_through(fs_bot, fs_top, bulge=0.02, side=-1.0)]),
            _sidebody_armhole(),
            # back seam: chest -> hem (bowed to mirror the back side seam)
            fc.Edge("back_seam",
                    [fc.curve_through(bs_top, bs_bot, bulge=0.02, side=-1.0)]),
            fc.Edge("hem", [fc.Line(bs_bot, fs_bot)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("front_seam", 0.5, "front waist"),
                 fc.Notch("back_seam", 0.5, "back waist")],
        grainline=fc.Grainline(fc.P(0.0, 60.0), fc.P(0.0, CHEST_Y - 40.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side Body",
    )


def build_back():
    """Cut 2 mirror with a CB seam (inlay 15): gentle waist-shaping curve in to
    CB_WAIST_X at the roll-line level, straight above the chest. Back side seam
    (matches side-body back seam) from hem up to the back-armhole top. The CB
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
    # Back side seam bowed to match the side-body back seam (mirror of it).
    side = fc.Edge(
        "side_seam",
        [fc.curve_through(fc.P(SEAM_X, CHEST_Y + 12.0), fc.P(SEAM_X, 0.0),
                          bulge=0.02, side=1.0)],
    )
    vh = min(vent_height, ROLL_Y - 30.0)
    return fc.Piece(
        "back",
        [
            cb,
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _back_armhole(),
            side,
            fc.Edge("hem", [fc.Line(fc.P(SEAM_X, 0.0), fc.P(CB_HEM_X, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": CB_SA, "hem": hem_allowance},
        notches=[fc.Notch("side_seam", 0.5, "back waist"),
                 fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(SEAM_X * 0.5, 80.0),
                               fc.P(SEAM_X * 0.5, L - 150.0)),
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


# ── Two-piece sleeve ─────────────────────────────────────────────────────────
def _cap_curve(hb, sl, ch):
    """Upper-sleeve cap edge: two mirrored beziers over the apex, back side
    first. Spans the whole armhole (classic two-piece: the cap lives on the
    upper sleeve)."""
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.66, sl + ch * 0.12),
                  fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                  fc.P(-hb * 0.66, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def _solve_cap_hb(cap_target, sl, ch):
    """Bisect the cap half-base so the cap length equals the armhole target."""
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    for _ in range(52):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    return hb


def _sleeve_dims(arm_target):
    """Shared two-piece sleeve dimensions so both pieces solve to the SAME cap
    half-base, cap height, seam length, and hem width — the forearm and hindarm
    seams are then identical curves on both pieces and balance by construction.
    Returns (hb, sl, ch, chw)."""
    cap_target = arm_target + cap_ease
    ch = max(72.0, AH * 0.32)
    sl = max(230.0, sleeve_length - ch)
    hb = _solve_cap_hb(cap_target, sl, ch)
    chw = max(120.0, min(hb * 0.62, hb - 10.0))
    return hb, sl, ch, chw


def _forearm_seg(chw, hb, sl):
    """Forearm (front) seam segment, cap-corner -> hem-corner. Shared by both
    sleeve pieces so their forearm seams are the same length."""
    return fc.curve_through(fc.P(-hb, sl), fc.P(-chw, 0.0), bulge=0.03, side=-1.0)


def _hindarm_seg(chw, hb, sl):
    """Hindarm (back) seam segment, hem-corner -> cap-corner. Shared by both
    sleeve pieces so their hindarm seams are the same length."""
    return fc.curve_through(fc.P(chw, 0.0), fc.P(hb, sl), bulge=0.03, side=-1.0)


def build_upper_sleeve(arm_target):
    """Upper sleeve (outer, cut 2 mirror). Carries the eased cap solved by
    bisection to the whole armhole (front + side-body + back) PLUS the declared
    cap ease. The forearm (front) and hindarm (back) seams are the SHARED seam
    curves, so they equal the under sleeve's exactly."""
    cap_target = arm_target + cap_ease
    hb, sl, ch, chw = _sleeve_dims(arm_target)
    return fc.Piece(
        "upper_sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("hindarm", [_hindarm_seg(chw, hb, sl)]),
            _cap_curve(hb, sl, ch),
            fc.Edge("forearm", [_forearm_seg(chw, hb, sl)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", (arm_target * 0.55 + cap_ease / 2.0) / cap_target,
                          "cap back match"),
                 fc.Notch("hem", 0.5),
                 fc.Notch("forearm", 0.5, "forearm match"),
                 fc.Notch("hindarm", 0.5, "hindarm match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.8)),
        internals=[
            fc.Internal("elbow line",
                        [fc.P(-hb * 0.9, sl * 0.55), fc.P(hb * 0.9, sl * 0.55)],
                        kind="marking"),
            # Four sleeve-button placement drills near the hindarm hem (vent).
            fc.Internal("sleeve buttons",
                        [fc.P(chw - 20.0 - i * 24.0, 22.0 + i * 2.0)
                         for i in range(SLEEVE_BUTTONS)] +
                        [fc.P(chw - 20.0, 22.0)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Upper Sleeve",
    )


def build_under_sleeve(arm_target):
    """Under sleeve (inner, cut 2 mirror). The inner panel that joins the upper
    sleeve along the forearm and hindarm seams and forms the underarm of a
    two-piece sleeve. It carries the SAME shared forearm/hindarm seam curves as
    the upper sleeve (so both vertical seams balance exactly) and the same hem
    width, but instead of the full cap its top is a shallow scye scoop that
    tucks under the armhole at the underarm — a teaching-grade two-piece: the
    whole cap seam lives on the upper sleeve, the under scoop is NOT part of the
    cap↔armhole seam (see the honest note in metadata)."""
    hb, sl, ch, chw = _sleeve_dims(arm_target)
    scoop = ch * 0.45                            # shallow underarm scye depth
    return fc.Piece(
        "under_sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("hindarm", [_hindarm_seg(chw, hb, sl)]),
            # shallow underarm scye scoop (dips below the seam tops, tucks under)
            fc.Edge("scye",
                    [fc.curve_through(fc.P(hb, sl), fc.P(-hb, sl),
                                      bulge=scoop / max(1.0, 2.0 * hb),
                                      side=1.0)]),
            fc.Edge("forearm", [_forearm_seg(chw, hb, sl)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("forearm", 0.5, "forearm match"),
                 fc.Notch("hindarm", 0.5, "hindarm match"),
                 fc.Notch("hem", 0.5),
                 fc.Notch("scye", 0.5, "underarm")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Under Sleeve",
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
    """Straight front facing strip: length = the measured center + lapel +
    gorge run + end allowances (declared as seam ease), width 95. A shaped
    facing that mirrors the lapel blade is future work — see docs/README.md."""
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
    pattern = fc.PatternSet("suit-jacket")
    front = build_front()
    side_body = build_side_body()
    back = build_back()

    front_ah = front.edge("armhole").length(0.05)
    sb_ah = side_body.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    arm_target = front_ah + sb_ah + back_ah
    center_len = front.edge("center").length(0.05)
    lapel_len = front.edge("lapel").length(0.05)
    gorge_len = front.edge("gorge").length(0.05)
    back_neck_len = back.edge("neck").length(0.05)
    front_run = center_len + lapel_len + gorge_len

    names = ("front", "side_body", "back", "upper_sleeve", "under_sleeve",
             "collar", "facing")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["side_body"]:
        pattern.add(side_body)
    if wanted["back"]:
        pattern.add(back)
    if wanted["upper_sleeve"]:
        pattern.add(build_upper_sleeve(arm_target))
    if wanted["under_sleeve"]:
        pattern.add(build_under_sleeve(arm_target))
    if wanted["collar"]:
        pattern.add(build_collar(gorge_len, back_neck_len))
    if wanted["facing"]:
        pattern.add(build_facing(center_len, lapel_len, gorge_len))

    # ── Declared seams (all balance to delta ~ 0) ────────────────────────────
    # Three-panel body: front side seam ↔ side-body front seam;
    # side-body back seam ↔ back side seam; shoulders.
    if wanted["front"] and wanted["side_body"]:
        pattern.declare_seam(("front", "side_seam"),
                             ("side_body", "front_seam"), tol=1.5)
    if wanted["side_body"] and wanted["back"]:
        pattern.declare_seam(("side_body", "back_seam"),
                             ("back", "side_seam"), tol=1.5)
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"),
                             tol=1.5)
    # Eased two-piece cap into the whole (front + side-body + back) armhole.
    if (wanted["upper_sleeve"] and wanted["front"] and wanted["side_body"]
            and wanted["back"]):
        pattern.declare_seam([("upper_sleeve", "cap")],
                             [("front", "armhole"), ("side_body", "armhole"),
                              ("back", "armhole")],
                             ease=cap_ease, tol=2.5)
    # Two-piece sleeve vertical seams: forearm ↔ forearm, hindarm ↔ hindarm.
    if wanted["upper_sleeve"] and wanted["under_sleeve"]:
        pattern.declare_seam(("upper_sleeve", "forearm"),
                             ("under_sleeve", "forearm"), tol=1.5)
        pattern.declare_seam(("upper_sleeve", "hindarm"),
                             ("under_sleeve", "hindarm"), tol=1.5)
    # Upper collar neck ↔ gorge + back neck.
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front", "gorge"), ("back", "neck")], tol=2.5)
    # Straight facing ↔ front center + lapel + gorge run.
    if wanted["facing"] and wanted["front"]:
        pattern.declare_seam([("facing", "long_edge")],
                             [("front", "center"), ("front", "lapel"),
                              ("front", "gorge")],
                             tol=3.0, ease=2.0 * seam_allowance)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1500.0                        # lana-peinada-traje card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.58)  # worsted, tighter marker
    lining_area = total_area * 0.85                  # body + sleeves lined
    lining_len = lining_area / (1400.0 * 0.62)
    pattern.bom = [
        {"item": "lana-peinada-traje", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"worsted suiting at {fabric_width:.0f} mm width, 58% marker; "
                 "pre-shrink (steam) and leave the CB/side/sleeve inlays"},
        {"item": "lining (bemberg/viscose twill)",
         "qty": round(lining_len / 10.0) * 10, "unit": "mm_length",
         "note": "fully lined jacket — body + two-piece sleeves; lining pieces "
                 "noted-not-drafted in v0 (mirror the shells, less the facing "
                 "at the front). At ~1400 mm width, 62% marker"},
        {"item": "fusible interfacing + chest canvas (fronts, lapels, "
                 "undercollar)", "qty": 1, "unit": "set",
         "note": "teaching-grade fusible front + a floating chest canvas panel; "
                 "a full hand-padded canvas is future work"},
        {"item": "shoulder pads (10-12 mm) + sleeve heads", "qty": 1, "unit":
         "pair", "note": "structured suit shoulder; pads set at the shoulder/"
                 "armhole marks. A 3D-printed pad former is a Yantra4D cartridge "
                 "reference, never re-implemented here"},
        {"item": "suit buttons 22 mm (front)", "qty": BUTTONS, "unit": "pcs",
         "note": "2 front on the CF line at the roll point + 95 mm below; "
                 "hardware is a Yantra4D cartridge (shank-button guide), never "
                 "re-implemented here"},
        {"item": "sleeve buttons 15 mm", "qty": 2 * SLEEVE_BUTTONS, "unit":
         "pcs", "note": "4 per sleeve at the hindarm cuff (working or mock "
                 "vent); Yantra4D shank-button cartridge reference"},
        {"item": "silk buttonhole twist + polyester thread + needle 90/14",
         "qty": 1, "unit": "set",
         "note": "press hard at every stage — pressing and steaming the roll "
                 "line, cap ease, and chest is half the tailoring"},
    ]

    # ── Metadata ───────────────────────────────────────────────────────────────
    pattern.metadata = {
        "fc100_rank": 67,
        "fabric_hint": "lana-peinada-traje",
        "tailoring_note": "teaching-grade tailored suit jacket: three-panel body "
                          "(front + side body + back), two-piece sleeve (upper "
                          "carries the eased cap, under tucks at the forearm/"
                          "hindarm seams), fusible + floating chest canvas in "
                          "place of a full hand-padded canvas, fully lined "
                          "(lining noted-not-drafted).",
        "body_structure": "three-panel (front + side_body + back)",
        "sleeve_structure": "two-piece (upper_sleeve + under_sleeve)",
        "lining": "fully lined; pieces noted-not-drafted in v0 (BOM-costed)",
        "canvas": "fusible front + floating chest canvas panel (note); full "
                  "pad-stitched canvas is future work",
        "shoulder": f"lightly extended {shoulder_ext:.0f} mm, padded/structured",
        "armhole_front_mm": round(front_ah, 1),
        "armhole_side_body_mm": round(sb_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "armhole_total_mm": round(arm_target, 1),
        "cap_ease_mm": cap_ease,
        "cap_target_mm": round(arm_target + cap_ease, 1),
        "gorge_mm": round(gorge_len, 1),
        "back_neck_mm": round(back_neck_len, 1),
        "collar_neck_target_mm": round(gorge_len + back_neck_len, 1),
        "front_edge_run_mm": round(front_run, 1),
        "facing_length_mm": round(front_run + 2.0 * seam_allowance, 1),
        "roll_line": {"roll_point_mm": [-BS, round(ROLL_Y, 1)],
                      "neck_point_mm": [round(NW, 1), round(HPS_Y, 1)]},
        "buttonholes": {"count": BUTTONS, "line": "CF (x=0)",
                        "stand_extension_mm": BS,
                        "top_button_at": "roll point"},
        "pockets": "breast welt (left chest) + two jetted-flap hip pockets — "
                   "markings only; jetting/flap construction pieces are future "
                   "work",
        "sleeve_buttons": SLEEVE_BUTTONS,
        "notch_gap": "classic 10 mm collar/lapel notch gap in construction — "
                     "see docs/README.md",
        "drafting": "single-breasted two-button suit jacket on the dress-shirt "
                    "frame: center edge breaks at the roll point into a straight "
                    "notch lapel and gorge; three-panel body splits the armhole "
                    "across front + side body + back; shaped CB seam with vent "
                    "markings; two-piece sleeve with the eased cap solved to the "
                    "whole armhole + cap ease; upper collar solved to gorge + "
                    "back neck; straight facing verified against the measured "
                    "front-edge run",
    }
    return pattern


result = build()

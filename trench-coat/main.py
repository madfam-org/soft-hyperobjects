"""
Trench coat — FC-100 rank #60. Fashion Cabinet Garment Cartridge.

The commons' most detailed coat ("gabardina"): a teaching-grade DOUBLE-BREASTED
trench on the blazer's lapel-front architecture, lengthened to a coat, widened
for layering, and dressed with every iconic trench detail as verified geometry.

The front's center edge climbs a WIDE button stand — the double-breasted wrap
extends the extension ~140 mm past CF so two columns of buttons cross the chest
— up to the ROLL POINT, then breaks into a broad LAPEL out to the lapel point
and a GORGE edge back to the neck point. The back splits into a storm-shield
CAPE (back yoke, cut 2) over a back body carrying a shaped CB seam with a DEEP
vent; the one-piece set-in sleeve cap is solved by bisection to the measured
armholes PLUS declared cap ease; the upper collar is solved to the gorge + back
cape neck; a straight front facing is verified against the measured center +
lapel + gorge run. The signature GUN FLAP (storm flap) is a shaped right-front
panel caught in the shoulder seam and hanging free; the BELT is a real long
strap, the EPAULETTES real shoulder straps, cuff straps + D-ring hardware are
BOM (Yantra4D). Wider melton allowances (14 mm) and a generous hem throughout.

A real trench is cut in gabardine/cotton-twill; the commons' closest heavyweight
woven is lana-melton-abrigo (the coat cloth) — used here, with wider seam room
for its bulk (see docs/README.md and metadata).

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
# front|back|back_yoke|sleeve|collar|gun_flap|belt|epaulette|facing|set

chest_girth    = float(PARAM(lambda: chest_girth, 1020.0))
body_length    = float(PARAM(lambda: body_length, 1120.0))    # nape to coat hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 640.0))   # cap apex to wrist
coat_ease      = float(PARAM(lambda: coat_ease, 260.0))       # total layering ease
button_stand   = float(PARAM(lambda: button_stand, 140.0))    # DB wrap past CF
lapel_width    = float(PARAM(lambda: lapel_width, 110.0))     # lapel point past CF
roll_line_y    = float(PARAM(lambda: roll_line_y, 620.0))     # roll point above hem
collar_height  = float(PARAM(lambda: collar_height, 80.0))
cap_ease       = float(PARAM(lambda: cap_ease, 30.0))         # eased sleeve cap
vent_height    = float(PARAM(lambda: vent_height, 420.0))     # deep CB vent
belt_width     = float(PARAM(lambda: belt_width, 60.0))       # finished belt width
seam_allowance = float(PARAM(lambda: seam_allowance, 14.0))   # melton-wide
hem_allowance  = float(PARAM(lambda: hem_allowance, 55.0))    # generous coat hem

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1800.0))
body_length = max(900.0, min(body_length, 1400.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(500.0, min(sleeve_length, 780.0))
coat_ease = max(160.0, min(coat_ease, 420.0))
button_stand = max(90.0, min(button_stand, 180.0))
lapel_width = max(80.0, min(lapel_width, 150.0))
roll_line_y = max(420.0, min(roll_line_y, 820.0))
collar_height = max(55.0, min(collar_height, 100.0))
cap_ease = max(0.0, min(cap_ease, 45.0))
vent_height = max(250.0, min(vent_height, 620.0))
belt_width = max(40.0, min(belt_width, 80.0))
seam_allowance = max(10.0, min(seam_allowance, 18.0))
hem_allowance = max(35.0, min(hem_allowance, 75.0))

# ── Double-breasted coat block (blazer frame, lengthened + widened) ──────────
W = (chest_girth + coat_ease) / 4.0            # quarter body width
L = body_length
NW = max(65.0, neck_girth / 5.0)               # half neck width at HPS
AH = (chest_girth + coat_ease) / 8.0 + 150.0   # coat-deep armhole (auto)
AH = max(210.0, min(AH, L - 520.0))            # chest line well above the waist
HPS_Y = L + 20.0
SHOULDER_DROP = 40.0                           # coat shoulder sits lower
BACK_NECK_DROP = 28.0
YOKE_DROP = 210.0                              # HPS to storm-shield / body seam
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y                           # chest level = lapel point level
YOKE_Y = HPS_Y - YOKE_DROP                     # storm-shield seam height
YOKE_Y = max(YOKE_Y, CHEST_Y + 40.0)           # keep cape above the chest/armhole
ROLL_Y = max(220.0, min(roll_line_y, CHEST_Y - 60.0))  # roll point below chest
BS = button_stand
LW = lapel_width
ROLL_PT = fc.P(-BS, ROLL_Y)                    # center edge breaks here
LAPEL_PT = fc.P(-LW, CHEST_Y)                  # lapel point, past CF
NECK_PT = fc.P(NW, HPS_Y)                      # gorge lands on the neck point
CB_HEM_X, CB_WAIST_X = 10.0, 20.0              # CB seam waist shaping
CB_SA = 16.0                                   # CB seam allowance (melton)
VENT_W = 60.0                                  # deep vent underlap width
FACING_W = 150.0                               # wide DB front facing
COLLAR_RISE = 16.0
BUTTON_COLS_DX = 90.0                          # half-distance between button rows
BUTTONS_PER_COL = 3
GUN_W = 190.0                                  # gun flap width at the chest
GUN_DROP = 150.0                               # gun flap hang below the shoulder


def _cross(label, x, y, half=4.5):
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


def _armhole(top, scoop):
    """Armhole from a shoulder/yoke top corner down to the underarm."""
    span = top.y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(top, fc.P(W - scoop, top.y - span * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + span * 0.30), UNDERARM)],
    )


def _button_columns():
    """Two columns of button cross-marks: the buttoning column near CF and the
    dead (anchor) column out toward the button-stand edge — the double-breasted
    signature."""
    marks = []
    cf_col_x = -BS * 0.30                       # buttoning column
    far_col_x = -BS * 0.30 - 2.0 * BUTTON_COLS_DX  # decorative/anchor column
    top_y = min(ROLL_Y, CHEST_Y - 20.0)
    step = 150.0
    for i in range(BUTTONS_PER_COL):
        y = top_y - i * step
        if y < 120.0:
            break
        marks += _cross(f"button-R{i + 1}", cf_col_x, y)
        marks += _cross(f"button-L{i + 1}", far_col_x, y)
    return marks


def _flap_pocket():
    """Slanted hip flap-pocket markings (welt/jetting is future work)."""
    cx = W * 0.52
    attach = max(160.0, ROLL_Y - 140.0)
    fw, fh = 175.0, 62.0
    flap = [fc.P(cx - fw / 2.0, attach), fc.P(cx + fw / 2.0, attach + 12.0),
            fc.P(cx + fw / 2.0, attach + 12.0 - fh),
            fc.P(cx - fw / 2.0, attach - fh), fc.P(cx - fw / 2.0, attach)]
    line = [fc.P(cx - fw / 2.0 - 6.0, attach),
            fc.P(cx + fw / 2.0 + 6.0, attach + 12.0)]
    return [
        fc.Internal("hip flap", flap),
        fc.Internal("flap attach line", line),
    ]


def build_front():
    """Cut 2 mirror. Double-breasted: the center edge climbs the WIDE button
    stand to the roll point, then the lapel diagonal to the lapel point, then
    the gorge in to the neck point. Two button columns, roll line, hip flap."""
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, ROLL_Y)],
                    kind="marking"),
        fc.Internal("roll line", [ROLL_PT, NECK_PT], kind="marking"),
    ]
    internals += _flap_pocket()
    internals += _button_columns()
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, 0.0), ROLL_PT)]),
            fc.Edge("lapel", [fc.Line(ROLL_PT, LAPEL_PT)]),
            fc.Edge("gorge", [fc.Line(LAPEL_PT, NECK_PT)]),
            fc.Edge("shoulder", [fc.Line(NECK_PT, SH_END)]),
            _armhole(SH_END, 16.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-BS, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("center", 1.0, "roll point"),
                 fc.Notch("side", 0.5),
                 fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.55, 90.0), fc.P(W * 0.55, L - 160.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (double-breasted)",
    )


def build_back():
    """Cut 2 mirror. Back BODY below the storm-shield seam: a shaped CB seam
    (allowance 16) with a DEEP vent, up to the yoke seam, then the armhole to
    the underarm. The vent is two internal marking lines, vent_height above the
    hem."""
    span = YOKE_Y - ROLL_Y
    cb = fc.Edge(
        "cb",
        [
            fc.Bezier(fc.P(CB_HEM_X, 0.0), fc.P(CB_HEM_X + 3.0, ROLL_Y * 0.45),
                      fc.P(CB_WAIST_X, ROLL_Y * 0.8), fc.P(CB_WAIST_X, ROLL_Y)),
            fc.Bezier(fc.P(CB_WAIST_X, ROLL_Y),
                      fc.P(CB_WAIST_X, ROLL_Y + span * 0.4),
                      fc.P(8.0, YOKE_Y - span * 0.2), fc.P(0.0, YOKE_Y)),
        ],
    )
    vh = min(vent_height, ROLL_Y - 30.0)
    top = fc.P(W - 5.0, YOKE_Y)
    return fc.Piece(
        "back",
        [
            cb,
            fc.Edge("top", [fc.Line(fc.P(0.0, YOKE_Y), top)]),
            _armhole(top, 12.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(CB_HEM_X, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": CB_SA, "hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("top", 0.5, "yoke match")],
        grainline=fc.Grainline(fc.P(W * 0.55, 90.0), fc.P(W * 0.55, YOKE_Y - 60.0)),
        internals=[
            fc.Internal("CB vent underlap",
                        [fc.P(VENT_W, 0.0), fc.P(VENT_W, vh)], kind="marking"),
            fc.Internal("CB vent stop",
                        [fc.P(CB_HEM_X + 2.0, vh), fc.P(VENT_W, vh)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Body (CB seam + vent)",
    )


def build_back_yoke():
    """Cut 2 mirror — the back storm-shield / cape yoke. Carries the back neck
    and shoulders; its straight bottom edge sews to the back body top. In wear
    the cape sheds rain off the shoulders; here it is a functional yoke seam
    (see docs/README.md). Cut 2 mirror gives the CB cape seam."""
    nape = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
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
            fc.Edge("bottom", [fc.Line(fc.P(W - 5.0, YOKE_Y), fc.P(0.0, YOKE_Y))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "body match"),
                 fc.Notch("shoulder", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.4, YOKE_Y + 20.0),
                               fc.P(W * 0.4, YOKE_Y + YOKE_DROP * 0.5)),
        internals=[fc.Internal(
            "storm-shield free edge (styling)",
            [fc.P(W - 20.0, YOKE_Y + 8.0), fc.P(20.0, YOKE_Y + 8.0)],
            kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Storm-Shield Yoke",
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
    """One-piece set-in coat sleeve: cap solved by bisection to the front +
    back armholes PLUS the declared cap ease (a trench sleeve is set-in and
    eased; a raglan is equally authentic — noted in docs/README.md). Elbow
    shaping is a gentle outward bow on the back underarm edge, well under 1 mm
    over the straight front underarm and inside the declared tol. A buckled
    CUFF STRAP is marked at the wrist (hardware in BOM)."""
    cap_target = front_ah + back_ah + cap_ease
    ch = max(75.0, AH * 0.32)
    sl = max(240.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(125.0, min(hb * 0.62, hb - 10.0))
    strap_y = 95.0
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
                        [fc.P(-hb * 0.9, sl * 0.55), fc.P(hb * 0.9, sl * 0.55)],
                        kind="marking"),
            fc.Internal("cuff strap line",
                        [fc.P(-chw * 0.85, strap_y), fc.P(chw * 0.85, strap_y)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (set-in, eased)",
    )


def _collar_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(gorge_len, back_neck_len):
    """Upper collar, half on fold at CB: neck edge solved by bisection to the
    measured front gorge + back cape neck per half (overlap 0, collar-band
    method). The classic trench throat-latch tab is a BOM note; the collar/lapel
    notch gap is a construction note — see docs/README.md."""
    target = gorge_len + back_neck_len
    flat = _solve_flat(_collar_neck, target, "upper-collar neck")
    neck = _collar_neck(flat)
    point = fc.P(flat + 18.0, COLLAR_RISE + collar_height)
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


def build_gun_flap(shoulder_len):
    """The trench's signature STORM/GUN FLAP: a shaped panel on the RIGHT front
    upper chest, caught in the shoulder seam and hanging free over the chest to
    shed rain off the shooting shoulder. Its `attach` edge is solved to the
    measured front shoulder length so it sews into that seam with delta ≈ 0
    (declared). Cut 1 (right front only)."""
    # attach edge runs along the shoulder from neck side to armhole side; build
    # it as a straight line of exactly the front shoulder length.
    a0 = fc.P(0.0, 0.0)
    a1 = fc.P(shoulder_len, 0.0)          # attach edge, length = front shoulder
    outer = fc.P(shoulder_len + 12.0, -GUN_DROP)   # armhole-side lower corner
    inner = fc.P(-8.0, -GUN_DROP + 40.0)           # neck-side lower corner
    hem_mid = fc.P((shoulder_len) * 0.45, -GUN_DROP - 18.0)  # shaped free hem
    return fc.Piece(
        "gun_flap",
        [
            fc.Edge("attach", [fc.Line(a0, a1)]),
            fc.Edge("armhole_edge", [fc.Line(a1, outer)]),
            fc.Edge("free_hem",
                    [fc.curve_through(outer, inner, bulge=0.06, side=1.0)]),
            fc.Edge("front_edge", [fc.Line(inner, a0)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(shoulder_len * 0.4, -20.0),
                               fc.P(shoulder_len * 0.4, -GUN_DROP + 10.0)),
        internals=[fc.Internal(
            "hem_mid guide", [hem_mid, fc.P(hem_mid.x, hem_mid.y - 1.0)],
            kind="drill")],
        cut=fc.CutSpec(quantity=1),
        label="Gun Flap (storm flap, right front)",
    )


def build_belt():
    """The waist BELT — a real long strap, cut 2 and seamed at CB (or cut on a
    long fold). Length = full waist wrap + generous buckle tail; folded lengthwise
    to the finished belt width. Belt loops + D-ring buckle are BOM (Yantra4D)."""
    waist = (chest_girth + coat_ease) * 0.62      # belt rides the coat waist
    length = waist / 2.0 + 260.0                   # half + buckle tail (cut 2)
    bh = 2.0 * (belt_width + seam_allowance)       # cut doubled, folded lengthwise
    cy = bh / 2.0
    internals = [fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)])]
    internals += _cross("belt eyelet 1", length - 60.0, cy)
    internals += _cross("belt eyelet 2", length - 120.0, cy)
    internals += _cross("belt eyelet 3", length - 180.0, cy)
    return fc.Piece(
        "belt",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, bh))]),
            fc.Edge("top", [fc.Line(fc.P(length, bh), fc.P(0.0, bh))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, bh), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                        # ends/edges include the sa
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Belt (strap, cut 2 + CB seam)",
    )


def build_epaulette():
    """Shoulder EPAULETTE strap — cut 2 mirror, folded lengthwise. Buttons at
    the neck end (BOM); the armhole end is caught in the shoulder seam or tacked
    (construction note). A real trench detail, drafted as a real piece."""
    length = 150.0
    ew = 2.0 * (28.0 + seam_allowance)             # cut doubled, folded
    cy = ew / 2.0
    pt = length - 22.0                             # pointed button end
    internals = [fc.Internal("fold line", [fc.P(0.0, cy), fc.P(pt, cy)])]
    internals += _cross("epaulette button", pt - 18.0, cy)
    return fc.Piece(
        "epaulette",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(pt, 0.0))]),
            fc.Edge("point_b", [fc.Line(fc.P(pt, 0.0), fc.P(length, cy))]),
            fc.Edge("point_t", [fc.Line(fc.P(length, cy), fc.P(pt, ew))]),
            fc.Edge("top", [fc.Line(fc.P(pt, ew), fc.P(0.0, ew))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, ew), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                        # edges include the sa
        grainline=fc.Grainline(fc.P(length * 0.15, cy), fc.P(pt * 0.85, cy)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Epaulette (shoulder strap)",
    )


def build_facing(center_len, lapel_len, gorge_len):
    """Wide double-breasted front facing strip: length = the measured center +
    lapel + gorge run + end allowances (declared as seam ease), width 150 to
    cover the deep DB button stand. A shaped facing mirroring the lapel blade is
    future work — see docs/README.md."""
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
        seam_allowance=0.0,                        # length already includes 2×sa
        notches=[fc.Notch("long_edge", t_roll, "roll point match")],
        grainline=fc.Grainline(fc.P(length * 0.2, FACING_W / 2.0),
                               fc.P(length * 0.8, FACING_W / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Facing (double-breasted)",
    )


def build():
    pattern = fc.PatternSet("trench-coat")
    front = build_front()
    back = build_back()
    back_yoke = build_back_yoke()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    center_len = front.edge("center").length(0.05)
    lapel_len = front.edge("lapel").length(0.05)
    gorge_len = front.edge("gorge").length(0.05)
    back_neck_len = back_yoke.edge("neck").length(0.05)
    shoulder_len = front.edge("shoulder").length(0.05)
    front_run = center_len + lapel_len + gorge_len
    names = ("front", "back", "back_yoke", "sleeve", "collar", "gun_flap",
             "belt", "epaulette", "facing")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["back_yoke"]:
        pattern.add(back_yoke)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(front_ah, back_ah))
    if wanted["collar"]:
        pattern.add(build_collar(gorge_len, back_neck_len))
    if wanted["gun_flap"]:
        pattern.add(build_gun_flap(shoulder_len))
    if wanted["belt"]:
        pattern.add(build_belt())
    if wanted["epaulette"]:
        pattern.add(build_epaulette())
    if wanted["facing"]:
        pattern.add(build_facing(center_len, lapel_len, gorge_len))
    # ── Declared seams (every sewn relationship; free straps are not seams) ──
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    if wanted["front"] and wanted["back_yoke"]:
        pattern.declare_seam(("front", "shoulder"), ("back_yoke", "shoulder"),
                             tol=1.5)
    if wanted["back_yoke"] and wanted["back"]:
        pattern.declare_seam(("back_yoke", "bottom"), ("back", "top"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")],
                             ease=cap_ease, tol=2.5)
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.5)
    if wanted["collar"] and wanted["front"] and wanted["back_yoke"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front", "gorge"), ("back_yoke", "neck")],
                             tol=2.5)
    if wanted["gun_flap"] and wanted["front"]:
        # gun flap is caught in the right-front shoulder seam
        pattern.declare_seam(("gun_flap", "attach"), ("front", "shoulder"),
                             tol=1.5)
    if wanted["facing"] and wanted["front"]:
        pattern.declare_seam([("facing", "long_edge")],
                             [("front", "center"), ("front", "lapel"),
                              ("front", "gorge")],
                             tol=3.0, ease=2.0 * seam_allowance)
    fabric_width = 1500.0                           # lana-melton-abrigo card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.55)  # coat marker, lower efficiency
    pattern.bom = [
        {"item": "lana-melton-abrigo", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 55% marker efficiency; a real "
                 f"trench is gabardine/cotton-twill — melton is the commons' "
                 f"closest heavyweight woven (grade allowances for its bulk)"},
        {"item": "coat lining (viscose/twill)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "full body + sleeve lining; lining pieces are noted-not-drafted "
                 "in v0 (cut from the shell fronts/back/sleeves less facings)"},
        {"item": "fusible interfacing (fronts, facing, collar, gun flap, "
                 "epaulettes, belt, cuff straps)",
         "qty": 1, "unit": "set",
         "note": "teaching-grade fusible in place of a tailored canvas"},
        {"item": "coat buttons 24 mm (double-breasted front)", "qty": 10,
         "unit": "pcs",
         "note": "2 columns × 3 buttoning + 4 anchor/decorative; hardware is a "
                 "Yantra4D cartridge (shank-button guide), never re-implemented"},
        {"item": "belt buckle + 2 D-rings", "qty": 1, "unit": "set",
         "note": "trench D-ring belt buckle; hardware is a Yantra4D cartridge, "
                 "never re-implemented here"},
        {"item": "strap sliders / buckles (2 cuff straps + 2 epaulettes)",
         "qty": 4, "unit": "pcs",
         "note": "cuff-strap sliders + epaulette buttons; hardware is a Yantra4D "
                 "cartridge reference, never re-implemented here"},
        {"item": "buttons 15 mm (epaulettes, gun-flap, throat latch)", "qty": 4,
         "unit": "pcs", "note": "Yantra4D shank-button guide reference"},
        {"item": "heavy polyester thread + jeans/topstitch needle 90/14", "qty": 1,
         "unit": "set", "note": "press hard with heavy steam and a clapper — "
                                "melton needs it; trim undercollar layer to reduce bulk"},
    ]
    pattern.metadata = {
        "fc100_rank": 60,
        "fabric_hint": "lana-melton-abrigo",
        "fabric_note": "a real trench is cut in gabardine / tightly-woven cotton "
                       "twill; the commons' closest heavyweight woven is "
                       "lana-melton-abrigo (the coat cloth) — used here with "
                       "wider 14 mm seam allowances and a 55 mm hem for its bulk",
        "silhouette": "double-breasted trench coat",
        "tailoring_note": "teaching-grade: one-piece set-in sleeve (raglan is "
                          "equally authentic), storm-shield cape as a functional "
                          "yoke seam, straight facing, fusible not canvas",
        "lining": "full lining noted-not-drafted in v0 (BOM line); cut from the "
                  "shell fronts/back/sleeves less the facings",
        "double_breasted": {"button_stand_mm": round(BS, 1),
                            "columns": 2,
                            "buttons_per_column": BUTTONS_PER_COL,
                            "column_gap_mm": round(2.0 * BUTTON_COLS_DX, 1)},
        "gun_flap": {"attach": "right-front shoulder seam (declared)",
                     "width_at_chest_mm": round(GUN_W, 1),
                     "hang_mm": round(GUN_DROP, 1),
                     "note": "storm/gun flap hangs free over the chest"},
        "belt": {"finished_width_mm": round(belt_width, 1),
                 "cut": "cut 2 + CB seam, folded lengthwise",
                 "hardware": "D-ring buckle (Yantra4D)"},
        "epaulette": {"cut": "cut 2 mirror, folded", "hardware": "button (Yantra4D)"},
        "gorge_mm": round(gorge_len, 1),
        "back_neck_mm": round(back_neck_len, 1),
        "collar_neck_target_mm": round(gorge_len + back_neck_len, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_ease_mm": cap_ease,
        "cap_target_mm": round(front_ah + back_ah + cap_ease, 1),
        "shoulder_mm": round(shoulder_len, 1),
        "front_edge_run_mm": round(front_run, 1),
        "facing_length_mm": round(front_run + 2.0 * seam_allowance, 1),
        "yoke_seam_y_mm": round(YOKE_Y, 1),
        "vent": {"underlap_mm": VENT_W, "height_mm": round(min(vent_height, ROLL_Y - 30.0), 1),
                 "cb_allowance_mm": CB_SA},
        "roll_line": {"roll_point_mm": [-BS, round(ROLL_Y, 1)],
                      "neck_point_mm": [round(NW, 1), round(HPS_Y, 1)]},
        "seam_allowance_mm": seam_allowance,
        "hem_allowance_mm": hem_allowance,
        "drafting": "double-breasted trench on the blazer lapel-front frame, "
                    "lengthened to a coat and widened for layering: wide DB "
                    "button stand with two button columns; storm-shield cape "
                    "yoke over a back body with a shaped CB seam + deep vent; "
                    "set-in cap solved to the armholes + declared ease; upper "
                    "collar solved to gorge + back-cape neck; gun flap caught in "
                    "the shoulder seam; belt + epaulettes as real straps; "
                    "straight facing verified against the front-edge run",
    }
    return pattern


result = build()

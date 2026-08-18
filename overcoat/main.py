"""
Overcoat — FC-100 rank #63. Fashion Cabinet Garment Cartridge.

A classic single-breasted tailored overcoat ("abrigo") in the Chesterfield
idiom: a long, roomy coat cut to layer over a suit. It is the blazer (rank #30)
grown to full length with a coat's proportions — read blazer/main.py first; this
mirrors its every technique and scales it up.

What the overcoat adds over the blazer:
  - COAT LENGTH: nape-to-hem ~1150 mm (knee-to-calf), not 700.
  - LAYERING EASE: ~260 mm of total ease so it sits over a jacket, not skin.
  - A PEAK LAPEL (upgrade over the blazer's notch): the center edge breaks at
    the roll point into a lapel that rises PAST the gorge to a peak point, then a
    short gorge runs back in to the neck point. Solved the same way — straight
    diagonals, verified against the facing and collar.
  - A TWO-PIECE SLEEVE (upper + under), the coat-appropriate sleeve: the combined
    cap is eased into the armholes, the upper and under sleeves join along an
    exact forearm and an exact hindarm seam (shared line endpoints → delta 0),
    and the upper-cap breadth is bisection-solved so upper.cap + under.cap hits
    the measured front + back armholes PLUS the declared cap ease.
  - A DEEP CB VENT and a half-belt marking on the back.
  - WELT breast pocket + FLAP hip pockets as markings (jetting is future work).
  - MELTON ALLOWANCES: wider seam allowances (13 mm) and a generous 50 mm hem,
    because the 420 gsm fulled coating eats seam room (see the fabric card).

Fully lined: the coat is drafted as the shell (self + facing + upper collar);
the lining pieces are derived from the shell and their yardage is in the BOM —
a rich lining note, undercollar-trim note, and canvas note are in the metadata,
honest teaching-grade in the blazer's tradition (no full canvas drafted in v0).

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
# front|back|sleeve_upper|sleeve_under|collar|facing|set

chest_girth   = float(PARAM(lambda: chest_girth, 1040.0))
body_length   = float(PARAM(lambda: body_length, 1150.0))    # nape to hem
neck_girth    = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 660.0))    # cap apex to wrist
coat_ease     = float(PARAM(lambda: coat_ease, 260.0))        # total layering ease
button_stand  = float(PARAM(lambda: button_stand, 22.0))      # extension past CF
lapel_width   = float(PARAM(lambda: lapel_width, 95.0))       # peak point past CF
peak_rise     = float(PARAM(lambda: peak_rise, 55.0))         # peak above gorge line
roll_line_y   = float(PARAM(lambda: roll_line_y, 720.0))      # roll point above hem
collar_height = float(PARAM(lambda: collar_height, 70.0))
cap_ease      = float(PARAM(lambda: cap_ease, 28.0))          # eased two-piece cap
vent_height   = float(PARAM(lambda: vent_height, 320.0))      # deep CB vent above hem
buttons       = int(PARAM(lambda: buttons, 4))                # front closure buttons
seam_allowance = float(PARAM(lambda: seam_allowance, 13.0))   # melton: wide
hem_allowance  = float(PARAM(lambda: hem_allowance, 50.0))    # melton: generous

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1800.0))
body_length = max(950.0, min(body_length, 1350.0))
neck_girth = max(320.0, min(neck_girth, 540.0))
sleeve_length = max(500.0, min(sleeve_length, 780.0))
coat_ease = max(160.0, min(coat_ease, 360.0))
button_stand = max(18.0, min(button_stand, 40.0))
lapel_width = max(70.0, min(lapel_width, 130.0))
peak_rise = max(0.0, min(peak_rise, 90.0))
roll_line_y = max(560.0, min(roll_line_y, 900.0))
collar_height = max(55.0, min(collar_height, 95.0))
cap_ease = max(0.0, min(cap_ease, 45.0))
vent_height = max(220.0, min(vent_height, 480.0))
buttons = max(2, min(buttons, 6))
seam_allowance = max(10.0, min(seam_allowance, 18.0))
hem_allowance = max(35.0, min(hem_allowance, 70.0))

# ── Overcoat block (blazer frame grown to a coat) ────────────────────────────
W = (chest_girth + coat_ease) / 4.0            # quarter body width (roomy)
L = body_length
NW = max(65.0, neck_girth / 5.0)               # half neck width at HPS
AH = (chest_girth + coat_ease) / 8.0 + 130.0   # coat-deep armhole (auto)
AH = max(220.0, min(AH, L - 520.0))            # chest line well above the waist
HPS_Y = L + 22.0
SHOULDER_DROP = 40.0                           # coat shoulder sits lower
BACK_NECK_DROP = 28.0
SH_END = fc.P(W - 6.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y                           # chest line = gorge/peak level
ROLL_Y = max(240.0, min(roll_line_y, CHEST_Y - 80.0))  # roll point below chest
BS = button_stand
LW = lapel_width
PEAK_PT = fc.P(-LW, CHEST_Y + peak_rise)       # peak lapel point, above gorge line
NECK_PT = fc.P(NW, HPS_Y)                       # gorge lands on the neck point
GORGE_PT = fc.P(NW * 0.30, CHEST_Y + peak_rise * 0.55)  # peak notch inner corner
CB_HEM_X, CB_WAIST_X = 10.0, 22.0              # CB seam waist shaping
CB_SA = 15.0                                   # CB seam allowance (melton bulk)
VENT_W = 60.0                                  # deep vent underlap width
FACING_W = 120.0                               # straight front facing width (coat)
COLLAR_RISE = 16.0


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
                   fc.P(W - 8.0, UNDERARM.y + fah * 0.30), UNDERARM)],
    )


def _flap_pocket():
    """Hip flap-pocket markings: flap rectangle + attach line. Cut mirrored
    puts one on each front — markings only in v0, jetting is future work."""
    cx = W * 0.52
    attach = max(300.0, ROLL_Y - 210.0)
    fw, fh = 175.0, 62.0
    flap = [fc.P(cx - fw / 2.0, attach), fc.P(cx + fw / 2.0, attach),
            fc.P(cx + fw / 2.0, attach - fh), fc.P(cx - fw / 2.0, attach - fh),
            fc.P(cx - fw / 2.0, attach)]
    line = [fc.P(cx - fw / 2.0 - 8.0, attach), fc.P(cx + fw / 2.0 + 8.0, attach)]
    return [
        fc.Internal("hip flap", flap),
        fc.Internal("flap attach line", line),
    ]


def _welt_breast():
    """Left-chest welt breast-pocket marking (a slim rectangle)."""
    cx = W * 0.44
    cy = CHEST_Y - 70.0
    ww, wh = 115.0, 22.0
    return fc.Internal(
        "breast welt",
        [fc.P(cx - ww / 2.0, cy), fc.P(cx + ww / 2.0, cy),
         fc.P(cx + ww / 2.0, cy + wh), fc.P(cx - ww / 2.0, cy + wh),
         fc.P(cx - ww / 2.0, cy)],
    )


def build_front():
    """Cut 2 mirror. Center edge = button stand up to the roll point; then the
    PEAK lapel diagonal out and up to the peak point; then a short gorge in to
    the neck point (a peak notch, not the blazer's notch). The roll line is an
    internal from roll point to neck point. Welt breast + flap hip pockets."""
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, ROLL_Y)],
                    kind="marking"),
        fc.Internal("roll line", [fc.P(-BS, ROLL_Y), NECK_PT], kind="marking"),
        _welt_breast(),
    ]
    internals += _flap_pocket()
    # Evenly spaced buttons from the roll point downward.
    gap = min(115.0, (ROLL_Y - 90.0) / max(1, buttons - 1)) if buttons > 1 else 0.0
    for i in range(buttons):
        internals += _cross(f"buttonhole-{i + 1}", 0.0, ROLL_Y - i * gap)
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, 0.0), fc.P(-BS, ROLL_Y))]),
            fc.Edge("lapel", [fc.Line(fc.P(-BS, ROLL_Y), PEAK_PT)]),
            fc.Edge("gorge", [fc.Line(PEAK_PT, GORGE_PT), fc.Line(GORGE_PT, NECK_PT)]),
            fc.Edge("shoulder", [fc.Line(NECK_PT, SH_END)]),
            _armhole(16.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-BS, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("center", 1.0, "roll point"),
                 fc.Notch("side", 0.5),
                 fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.60, 120.0), fc.P(W * 0.60, L - 160.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Cut 2 mirror with a shaped CB seam (allowance 15) and a DEEP vent. The
    CB curves in to CB_WAIST_X at the roll-line level, straight above the chest.
    A half-belt marking sits at waist level on the back."""
    nape = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
    span = CHEST_Y - ROLL_Y
    cb = fc.Edge(
        "cb",
        [
            fc.Bezier(fc.P(CB_HEM_X, 0.0), fc.P(CB_HEM_X + 4.0, ROLL_Y * 0.45),
                      fc.P(CB_WAIST_X, ROLL_Y * 0.8), fc.P(CB_WAIST_X, ROLL_Y)),
            fc.Bezier(fc.P(CB_WAIST_X, ROLL_Y),
                      fc.P(CB_WAIST_X, ROLL_Y + span * 0.4),
                      fc.P(8.0, CHEST_Y - span * 0.2), fc.P(0.0, CHEST_Y)),
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
            _armhole(12.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(CB_HEM_X, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": CB_SA, "hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(W * 0.58, 120.0), fc.P(W * 0.58, L - 160.0)),
        internals=[
            fc.Internal("CB vent underlap",
                        [fc.P(VENT_W, 0.0), fc.P(VENT_W, vh)], kind="marking"),
            fc.Internal("CB vent stop",
                        [fc.P(CB_HEM_X + 2.0, vh), fc.P(VENT_W, vh)],
                        kind="marking"),
            fc.Internal("half-belt (RH strap)",
                        [fc.P(W * 0.30, belt_y), fc.P(W * 0.82, belt_y)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back",
    )


# ── Two-piece sleeve ─────────────────────────────────────────────────────────
# The sleeve tube is split into an UPPER (top) sleeve and an UNDER sleeve. Both
# pieces share the SAME two vertical seams — the FOREARM seam (front) and the
# HINDARM seam (back) — and the SAME two cap junction points: the hindarm top
# H = (hb, sl) and the forearm top F = (-hb, sl). Each cap arc runs H↔F:
#   • upper.cap goes the LONG way, over the crown apex — the visible sleeve head;
#   • under.cap goes the SHORT way, a shallow bow dipping below the H–F chord —
#     the underarm.
# Together upper.cap + under.cap trace the full armscye ellipse, so the ARMHOLE
# seam sums both arcs. The vertical seams are built from IDENTICAL curve_through
# calls with identical endpoints on both pieces, so each vertical seam's length
# delta is 0 by construction. The crown breadth `hb` is bisection-solved so the
# combined cap equals front_ah + back_ah + cap_ease.
#
# Solve order: the under cap depends only on hb (its chord H–F) and a fixed
# under-dip, so for a given hb both arcs are determined and their sum is
# monotonic in hb — a single bisection on hb closes the whole two-piece cap.

def _under_cap(hb, sl, dip):
    """Under-sleeve cap: shallow bow from H=(hb, sl) to F=(-hb, sl) dipping
    `dip` mm below the chord (into the tube) — the underarm curve."""
    chord = 2.0 * hb
    return fc.Edge("cap", [
        fc.curve_through(fc.P(hb, sl), fc.P(-hb, sl), bulge=dip / chord, side=1.0),
    ])


def _upper_cap(hb, sl, ch):
    """Upper-sleeve cap: the crown. Two mirrored beziers rise from the hindarm
    top H=(hb, sl) over the apex down to the forearm top F=(-hb, sl). Back
    (hindarm) side first."""
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.66, sl + ch * 0.14),
                  fc.P(hb * 0.30, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.30, sl + ch),
                  fc.P(-hb * 0.66, sl + ch * 0.14), fc.P(-hb, sl)),
    ])


def _combined_cap_len(hb, sl, ch, dip):
    return _upper_cap(hb, sl, ch).length(0.05) + _under_cap(hb, sl, dip).length(0.05)


def _solve_sleeve(front_ah, back_ah):
    """Bisection-solve the crown breadth `hb` so upper.cap + under.cap equals the
    measured armholes + cap ease. Returns the solved dims."""
    total_cap = front_ah + back_ah + cap_ease
    ch = max(90.0, AH * 0.34)                  # crown height
    sl = max(300.0, sleeve_length - ch)        # cap base line (apex at sl+ch)
    dip = ch * 0.16                            # underarm bow depth (fixed)
    lo, hi = 40.0, total_cap / 2.0 + ch + 80.0
    for _ in range(56):
        hb = (lo + hi) / 2.0
        if _combined_cap_len(hb, sl, ch, dip) < total_cap:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    got = _combined_cap_len(hb, sl, ch, dip)
    if abs(got - total_cap) > 1.0:
        raise ValueError("two-piece sleeve cap solver did not converge")
    return {"total_cap": total_cap, "ch": ch, "sl": sl, "dip": dip, "hb": hb,
            "upper_cap_len": _upper_cap(hb, sl, ch).length(0.05),
            "under_cap_len": _under_cap(hb, sl, dip).length(0.05)}


def _forearm_edge(hb, sl, wrist):
    """Forearm (front) vertical seam: F=(-hb, sl) down to the wrist (-wrist, 0).
    Identical call on both sleeve pieces → shared, so seam delta is 0."""
    return fc.Edge("forearm",
                   [fc.curve_through(fc.P(-hb, sl), fc.P(-wrist, 0.0),
                                     bulge=0.03, side=-1.0)])


def _hindarm_edge(hb, sl, wrist):
    """Hindarm (back) vertical seam: wrist (wrist, 0) up to H=(hb, sl).
    Identical call on both sleeve pieces → shared, so seam delta is 0."""
    return fc.Edge("hindarm",
                   [fc.curve_through(fc.P(wrist, 0.0), fc.P(hb, sl),
                                     bulge=0.03, side=-1.0)])


def _sleeve_wrist(hb):
    return max(150.0, min(hb * 0.72, hb - 12.0))


def build_sleeve_upper(s):
    """Upper (top) sleeve, cut 2 mirror. Crown cap H↔F over the apex; hem across
    the wrist; forearm and hindarm the shared vertical seams."""
    hb, sl, ch = s["hb"], s["sl"], s["ch"]
    wrist = _sleeve_wrist(hb)
    return fc.Piece(
        "sleeve_upper",
        [
            fc.Edge("hem", [fc.Line(fc.P(-wrist, 0.0), fc.P(wrist, 0.0))]),
            _hindarm_edge(hb, sl, wrist),
            _upper_cap(hb, sl, ch),
            _forearm_edge(hb, sl, wrist),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "apex / shoulder match"),
                 fc.Notch("hem", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, 60.0), fc.P(0.0, sl * 0.8)),
        internals=[fc.Internal(
            "elbow line",
            [fc.P(-hb * 0.85, sl * 0.52), fc.P(hb * 0.85, sl * 0.52)],
            kind="marking"),
            fc.Internal("cuff buttons",
                        [fc.P(-wrist + 26.0, 34.0), fc.P(-wrist + 26.0, 82.0)],
                        kind="drill")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Upper Sleeve",
    )


def build_sleeve_under(s):
    """Under sleeve, cut 2 mirror. The SAME hindarm/forearm seams as the upper
    sleeve (identical endpoints, delta 0) plus the shallow underarm cap H↔F."""
    hb, sl, dip = s["hb"], s["sl"], s["dip"]
    wrist = _sleeve_wrist(hb)
    return fc.Piece(
        "sleeve_under",
        [
            fc.Edge("hem", [fc.Line(fc.P(-wrist, 0.0), fc.P(wrist, 0.0))]),
            _hindarm_edge(hb, sl, wrist),
            _under_cap(hb, sl, dip),
            _forearm_edge(hb, sl, wrist),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "underarm match"),
                 fc.Notch("hem", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, 60.0), fc.P(0.0, sl * 0.75)),
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
    measured front gorge + back neck per half (collar-band method). The melton
    undercollar is trimmed and felled — see docs/README.md; the classic
    collar/lapel notch gap is a construction note."""
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


def build_facing(center_len, lapel_len, gorge_len):
    """Straight front facing strip: length = the measured center + lapel + gorge
    run + end allowances (declared as seam ease), width 120 (a coat facing runs
    wide to carry the breast-pocket bag and the buttonholes). A shaped facing
    that mirrors the peak is future work — see docs/README.md."""
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
    pattern = fc.PatternSet("overcoat")
    front = build_front()
    back = build_back()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    center_len = front.edge("center").length(0.05)
    lapel_len = front.edge("lapel").length(0.05)
    gorge_len = front.edge("gorge").length(0.05)
    back_neck_len = back.edge("neck").length(0.05)
    front_run = center_len + lapel_len + gorge_len
    sol = _solve_sleeve(front_ah, back_ah)

    names = ("front", "back", "sleeve_upper", "sleeve_under", "collar", "facing")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve_upper"]:
        pattern.add(build_sleeve_upper(sol))
    if wanted["sleeve_under"]:
        pattern.add(build_sleeve_under(sol))
    if wanted["collar"]:
        pattern.add(build_collar(gorge_len, back_neck_len))
    if wanted["facing"]:
        pattern.add(build_facing(center_len, lapel_len, gorge_len))

    # ── Declared seams (every sewn relationship) ─────────────────────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve_upper"] and wanted["sleeve_under"]:
        # Vertical sleeve seams: identical straight/curve runs → delta 0.
        pattern.declare_seam(("sleeve_upper", "forearm"),
                             ("sleeve_under", "forearm"), tol=1.5)
        pattern.declare_seam(("sleeve_upper", "hindarm"),
                             ("sleeve_under", "hindarm"), tol=1.5)
    if (wanted["sleeve_upper"] and wanted["sleeve_under"]
            and wanted["front"] and wanted["back"]):
        # Combined two-piece cap eased into the armholes.
        pattern.declare_seam(
            [("sleeve_upper", "cap"), ("sleeve_under", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            ease=cap_ease, tol=2.5)
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front", "gorge"), ("back", "neck")], tol=2.5)
    if wanted["facing"] and wanted["front"]:
        pattern.declare_seam([("facing", "long_edge")],
                             [("front", "center"), ("front", "lapel"),
                              ("front", "gorge")],
                             tol=3.0, ease=2.0 * seam_allowance)

    # ── BOM (melton shell + full lining + interfacing + notions) ─────────────
    shell_width = 1500.0                         # lana-melton-abrigo card width
    lining_width = 1400.0                         # tricot/twill lining width
    shell_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    # Lining ≈ body + sleeves less the facing overlap; approximate at 82% of the
    # self-fabric marker (facings are self, collar is self) plus sleeve linings.
    marker_len = shell_area / (shell_width * 0.58)   # coats mark less efficiently
    lining_len = marker_len * 0.82
    pattern.bom = [
        {"item": "lana-melton-abrigo", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"shell at {shell_width:.0f} mm width, 58% marker efficiency "
                 "(a long coat marks low); press with heavy steam + clapper, "
                 "trim the undercollar layer to shed melton bulk"},
        {"item": "coat lining (twill/tricot, e.g. cupro or viscose)",
         "qty": round(lining_len / 10.0) * 10, "unit": "mm_length",
         "note": f"full lining at {lining_width:.0f} mm width — front lining = "
                 "front minus the facing, back lining = back with a CB ease "
                 "pleat, two sleeve linings from the upper+under sleeves; lining "
                 "pieces derived from the shell, not separately drafted in v0"},
        {"item": "fusible interfacing (fronts, lapels, undercollar, hems)",
         "qty": 1, "unit": "set",
         "note": "teaching-grade fusible in place of a full haircloth chest "
                 "canvas; a pad-stitched canvas front is future work"},
        {"item": "shoulder pads (coat weight) + sleeve heads", "qty": 1,
         "unit": "pair",
         "note": "coat-weight pads support the layered shoulder; sleeve heads "
                 "fill the eased cap so it rolls smoothly"},
        {"item": "coat buttons 30 mm (horn or corozo)", "qty": buttons,
         "unit": "pcs",
         "note": f"{buttons} front closure; hardware is a Yantra4D cartridge "
                 "(shank-button guide), never re-implemented here"},
        {"item": "coat buttons 20 mm (cuffs)", "qty": 2 * 3, "unit": "pcs",
         "note": "3 per cuff (decorative), 2 cuffs; Yantra4D shank-button ref"},
        {"item": "polyester/silk thread + jeans needle 90/14", "qty": 1,
         "unit": "set", "note": "press hard at every stage — pressing is half "
                                "the tailoring, doubly so in melton"},
    ]
    pattern.metadata = {
        "fc100_rank": 63,
        "fabric_hint": "lana-melton-abrigo",
        "garment": "single-breasted tailored overcoat (Chesterfield idiom)",
        "tailoring_note": "teaching-grade: two-piece sleeve, straight facing, "
                          "fusible instead of a full canvas, lining derived "
                          "from the shell (not separately drafted) — a "
                          "pad-stitched canvas + drafted lining are future work",
        "coat_length_mm": round(L, 1),
        "layering_ease_mm": round(coat_ease, 1),
        "quarter_width_mm": round(W, 1),
        "lapel_style": "peak",
        "peak_point_mm": [round(-LW, 1), round(CHEST_Y + peak_rise, 1)],
        "peak_rise_mm": round(peak_rise, 1),
        "gorge_mm": round(gorge_len, 1),
        "back_neck_mm": round(back_neck_len, 1),
        "collar_neck_target_mm": round(gorge_len + back_neck_len, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_ease_mm": cap_ease,
        "cap_target_mm": round(sol["total_cap"], 1),
        "sleeve_two_piece": {
            "upper_cap_mm": round(sol["upper_cap_len"], 1),
            "under_cap_mm": round(sol["under_cap_len"], 1),
            "sum_cap_mm": round(sol["upper_cap_len"] + sol["under_cap_len"], 1),
            "crown_half_breadth_mm": round(sol["hb"], 1),
            "underarm_dip_mm": round(sol["dip"], 1),
            "note": "upper+under cap solved to the armholes + cap ease; the "
                    "forearm and hindarm seams share exact endpoints so their "
                    "length deltas are 0",
        },
        "front_edge_run_mm": round(front_run, 1),
        "facing_length_mm": round(front_run + 2.0 * seam_allowance, 1),
        "roll_line": {"roll_point_mm": [round(-BS, 1), round(ROLL_Y, 1)],
                      "neck_point_mm": [round(NW, 1), round(HPS_Y, 1)]},
        "buttonholes": {"count": buttons, "line": "CF (x=0)",
                        "stand_extension_mm": round(BS, 1),
                        "top_button_at": "roll point"},
        "vent": {"style": "deep CB vent", "height_mm": round(min(vent_height,
                 ROLL_Y - 40.0), 1), "underlap_mm": VENT_W},
        "melton_note": "wider seam allowances (13 mm) + a 50 mm hem because the "
                       "420 gsm fulled coating eats seam room; the fulled face "
                       "barely frays, so some edges may be bound not turned",
        "seam_allowance_mm": round(seam_allowance, 1),
        "hem_allowance_mm": round(hem_allowance, 1),
        "notch_gap": "classic collar/lapel notch gap in construction — see "
                     "docs/README.md",
        "drafting": "single-breasted overcoat on the blazer frame grown to a "
                    "coat: center edge breaks at the roll point into a PEAK "
                    "lapel and a short gorge; shaped CB seam with a deep vent "
                    "and a half-belt marking; a TWO-PIECE sleeve whose combined "
                    "cap is eased into the armholes + 28 mm; upper collar solved "
                    "to gorge + back neck; straight facing verified against the "
                    "measured front edge run; full lining noted in the BOM",
    }
    return pattern


result = build()

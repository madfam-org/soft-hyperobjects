"""
Morning coat — FC-300 rank #294. Fashion Cabinet Garment Cartridge.

The morning coat (chaqué, jaquette): formal daywear, and the last surviving
descendant of the nineteenth-century riding coat. It is the tailoring block the
commons did not hold, because its front is not a front at all in the usual
sense — below the single fastening button the centre-front edge SWEEPS AWAY in
a continuous curve to the side seam, and the coat continues behind as long
tails. That cutaway curve is the garment.

The commons holds `suit-jacket`, `blazer`, `overcoat`, `trench-coat` and
`waistcoat`, all of them coats whose fronts drop straight to a horizontal hem.
None of them can be parameterised into a morning coat, because the cutaway is
not a hem variant — it changes which edges exist, where the button sits
relative to the hem, and what the back panel is (a skirt, not a body).

Three things are the garment, and all three solve:

  - THE CUTAWAY CURVE (the signature): a single continuous sweep from the
    fastening point down and back to the side seam at the tail break. It is
    drafted as two chained arcs — a shallow one leaving the button (so the coat
    does not look chopped) and a deeper one running back — over a SOLVED span,
    so the curve is derived from the button height and the tail break rather
    than sketched. Both its rise and its run are floored: at parameter extremes
    the derived span goes to zero or NEGATIVE, and a negative span does not
    fail, it inverts the panel into geometry the kernel's CCW normalization
    launders into a valid-LOOKING outline.
  - THE TAILS: the back below the waist seam is a separate SKIRT piece, not a
    continuation of the body. That is how the coat is really made — waist-seamed,
    so the tails can be cut on their own grain and hang.
  - THE PEAK LAPEL: the front's centre edge climbs the button stand to the roll
    point, then breaks out to the lapel point and back along the gorge to the
    neck point. The collar is bisected to the measured gorge plus back neck.

Hardware: the single fastening button and the sleeve-cuff buttons bridge to the
Yantra4D `sew-through-button` solid. `button_ligne` drives the printed button
and the drilled buttonhole marks together.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
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
# front|back|tail|sleeve|collar|facing|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 890.0))
back_length = float(PARAM(lambda: back_length, 430.0))    # nape to the waist seam
tail_length = float(PARAM(lambda: tail_length, 480.0))    # waist seam to tail hem
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 630.0))
coat_ease = float(PARAM(lambda: coat_ease, 120.0))
button_stand = float(PARAM(lambda: button_stand, 22.0))
lapel_width = float(PARAM(lambda: lapel_width, 100.0))    # peak point past CF
button_rise = float(PARAM(lambda: button_rise, 40.0))     # button above the waist seam
cutaway_sweep = float(PARAM(lambda: cutaway_sweep, 210.0))  # how far back the curve runs
collar_height = float(PARAM(lambda: collar_height, 60.0))
cap_ease = float(PARAM(lambda: cap_ease, 26.0))
button_ligne = float(PARAM(lambda: button_ligne, 30.0))   # ligne (1 ligne = 0.635 mm)
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps (match the manifest slider bounds exactly) ────────────────────────
chest_girth = max(780.0, min(chest_girth, 1500.0))
waist_girth = max(620.0, min(waist_girth, 1450.0))
back_length = max(340.0, min(back_length, 560.0))
tail_length = max(280.0, min(tail_length, 720.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(420.0, min(sleeve_length, 760.0))
coat_ease = max(80.0, min(coat_ease, 240.0))
button_stand = max(15.0, min(button_stand, 35.0))
lapel_width = max(70.0, min(lapel_width, 130.0))
button_rise = max(0.0, min(button_rise, 140.0))
cutaway_sweep = max(60.0, min(cutaway_sweep, 380.0))
collar_height = max(45.0, min(collar_height, 90.0))
cap_ease = max(0.0, min(cap_ease, 40.0))
button_ligne = max(18.0, min(button_ligne, 44.0))
seam_allowance = max(8.0, min(seam_allowance, 20.0))
hem_allowance = max(25.0, min(hem_allowance, 60.0))

# ── The tailored body block above the waist seam ─────────────────────────────
W = (chest_girth + coat_ease) / 4.0            # quarter chest width
WW = max(80.0, (waist_girth + coat_ease * 0.75) / 4.0)   # quarter waist width
L = back_length                                # nape → waist seam
NW = max(60.0, neck_girth / 5.0)               # half neck width at HPS
# The armhole depth. NOTE the difference from the commons' full-length coats
# (`suit-jacket`, `blazer`): those measure `body_length` nape-to-HEM, so a deep
# armhole still leaves most of the panel below the chest. Here `back_length` is
# nape-to-WAIST-SEAM — a much shorter run — so the same formula would drive the
# chest line down almost onto the waist. It is scaled to the waist length and
# then capped to leave a real chest-to-waist run below it.
AH = (chest_girth + coat_ease) / 8.0 + 45.0    # coat armhole, waist-referenced
AH = max(160.0, min(AH, L * 0.52))             # ≥ 48% of the bodice stays below
HPS_Y = L + 20.0
SHOULDER_DROP = 36.0
BACK_NECK_DROP = 25.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y
BS = button_stand
LW = lapel_width
SEAM_X = W * 0.66                              # side seam at the waist
CB_WAIST_X = 16.0                              # CB waist suppression
CUFF_BUTTONS = 4

# ── The cutaway: a SOLVED span, floored twice ────────────────────────────────
# The fastening button sits `button_rise` above the waist seam, on the button
# stand at x = -BS. From there the cutaway sweeps down and BACK to the side
# seam. Its rise is the button height; its run is the sweep, capped so the curve
# cannot travel past the side seam and turn the front panel inside out.
#
# Both are DERIVED, and a derived dimension that goes negative does not fail —
# it inverts the panel, and the kernel's CCW normalization then hands verify()
# a valid-LOOKING outline. So both are floored here, before any point is built.
BUTTON_Y = max(25.0, min(button_rise, max(30.0, CHEST_Y - 60.0)))
BUTTON_CLAMPED = (button_rise < 25.0) or (button_rise > max(30.0, CHEST_Y - 60.0))

# The sweep's room is the whole horizontal run available on the front panel:
# from the button stand at x = -BS out to the side seam. The curve may consume
# all of it (a full cutaway that meets the side seam exactly) but never more,
# which would put the break outboard of the panel and invert it.
_sweep_room = SEAM_X + BS
CUTAWAY_RUN = max(50.0, min(cutaway_sweep, _sweep_room))
SWEEP_CLAMPED = (cutaway_sweep > _sweep_room) or (cutaway_sweep < 50.0)

# Where the cutaway lands — the TAIL BREAK. The short horizontal `break` edge
# runs from the side seam in to this point, and it must stay a REAL edge: a
# zero-length edge is a degenerate vertex the outline cannot close on. So the
# break is held at least BREAK_MIN inboard of the side seam even when the sweep
# asks for the whole panel.
BREAK_MIN = 25.0
BREAK_X = min(SEAM_X - BREAK_MIN, -BS + CUTAWAY_RUN)
BREAK_X = max(-BS + 40.0, BREAK_X)             # and never back at the button
BREAK_Y = 0.0                                  # the front's own hem level
# The run the curve ACTUALLY spans, re-derived from the clamped break so the
# arcs are drawn over the real span rather than the requested one.
CUTAWAY_SPAN = BREAK_X - (-BS)                 # > 0 by the BREAK_X floors
CUTAWAY_RISE = BUTTON_Y - BREAK_Y              # ≥ 25 by the BUTTON_Y floor


def _cross(label, x, y, half=5.0):
    """Drill cross-mark as two internals (the commons' buttonhole convention)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


def _solve_flat(edge_fn, target, what):
    """Bisect a monotonic flat-length -> measured-curve-length edge builder."""
    lo, hi = target * 0.55, target * 1.15
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


def _cutaway_edge():
    """THE SIGNATURE PIECE: the continuous cutaway sweep.

    Two chained arcs from the tail break on the side seam up to the fastening
    button on the button stand:

      - the LOWER arc runs back nearly horizontally along the break, which is
        what keeps the tail root looking like a coat rather than a chopped hem;
      - the UPPER arc turns up into the button, so the edge meets the button
        stand cleanly instead of arriving at an angle.

    Both arcs are drawn over the SOLVED span (CUTAWAY_SPAN × CUTAWAY_RISE), so
    the curve is derived from the button height and the sweep rather than
    sketched — change either parameter and the whole curve re-solves.
    """
    start = fc.P(BREAK_X, BREAK_Y)
    mid = fc.P(BREAK_X - CUTAWAY_SPAN * 0.45, BREAK_Y + CUTAWAY_RISE * 0.22)
    end = fc.P(-BS, BUTTON_Y)
    return fc.Edge("cutaway", [
        fc.curve_through(start, mid, bulge=0.10, side=1.0),
        fc.curve_through(mid, end, bulge=0.14, side=-1.0),
    ])


def build_front():
    """Front (cut 2, mirrored). Centre edge from the button up to the roll point,
    peak lapel out to the lapel point, gorge back to the neck point, shoulder,
    armhole down to the underarm, side seam down to the tail break, and then the
    CUTAWAY back to the button. There is NO hem edge: the cutaway curve replaces
    it, which is exactly what makes this a morning coat."""
    roll_y = min(CHEST_Y - 40.0, BUTTON_Y + max(60.0, (CHEST_Y - BUTTON_Y) * 0.55))
    roll_y = max(BUTTON_Y + 20.0, roll_y)      # the roll point is above the button
    roll_pt = fc.P(-BS, roll_y)
    lapel_pt = fc.P(-LW, CHEST_Y)
    neck_pt = fc.P(NW, HPS_Y)
    internals = [
        fc.Internal("CF line", [fc.P(-BS + BS, BUTTON_Y), fc.P(0.0, roll_y)],
                    kind="marking"),
        fc.Internal("roll line", [roll_pt, neck_pt], kind="marking"),
        fc.Internal("waist line", [fc.P(-BS, BUTTON_Y), fc.P(SEAM_X, BUTTON_Y)],
                    kind="marking"),
    ]
    internals += _cross("buttonhole", 0.0, BUTTON_Y)
    # Front waist dart: the suppression that lets a cutaway front lie flat.
    dart_x = SEAM_X * 0.5
    intake = max(4.0, min(16.0, (W - WW) * 0.5))
    internals.append(fc.Internal(
        "front waist dart",
        [fc.P(dart_x, max(BUTTON_Y - 10.0, 8.0)),
         fc.P(dart_x - intake / 2.0, (BUTTON_Y + CHEST_Y) * 0.5),
         fc.P(dart_x, CHEST_Y - 30.0),
         fc.P(dart_x + intake / 2.0, (BUTTON_Y + CHEST_Y) * 0.5),
         fc.P(dart_x, max(BUTTON_Y - 10.0, 8.0))],
        kind="dart"))
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, BUTTON_Y), roll_pt)]),
            fc.Edge("lapel", [fc.Line(roll_pt, lapel_pt)]),
            fc.Edge("gorge", [fc.Line(lapel_pt, neck_pt)]),
            fc.Edge("shoulder", [fc.Line(neck_pt, SH_END)]),
            fc.Edge("armhole", [fc.Bezier(
                SH_END, fc.P(SH_END.x - 22.0, SH_END.y - AH * 0.40),
                fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)]),
            fc.Edge("side_seam", [fc.curve_through(
                UNDERARM, fc.P(SEAM_X, BREAK_Y), bulge=0.03, side=1.0)]),
            fc.Edge("break", [fc.Line(fc.P(SEAM_X, BREAK_Y),
                                      fc.P(BREAK_X, BREAK_Y))]),
            _cutaway_edge(),
        ],
        seam_allowance=seam_allowance,
        allowances={"cutaway": hem_allowance, "break": hem_allowance},
        notches=[fc.Notch("center", 0.0, "fastening button"),
                 fc.Notch("side_seam", 0.5, "waist match"),
                 fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(SEAM_X * 0.55, BUTTON_Y + 20.0),
                               fc.P(SEAM_X * 0.55, CHEST_Y + 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cutaway)",
    )


def build_back():
    """Back bodice (cut 2, mirrored, CB seam) — it ends at the WAIST SEAM.

    This is the second thing that makes a morning coat: the back is not one
    panel to the hem. It is a bodice seamed at the waist, so the tails below can
    be cut on their own grain and hang instead of being dragged by the bodice.
    """
    nape = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
    cb = fc.Edge("cb", [
        fc.Bezier(fc.P(CB_WAIST_X, 0.0), fc.P(CB_WAIST_X, CHEST_Y * 0.45),
                  fc.P(6.0, CHEST_Y * 0.85), fc.P(0.0, CHEST_Y)),
        fc.Line(fc.P(0.0, CHEST_Y), nape),
    ])
    neck = fc.Edge("neck", [fc.Bezier(
        nape, fc.P(NW * 0.55, nape.y),
        fc.P(NW, nape.y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))])
    return fc.Piece(
        "back",
        [
            cb,
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            fc.Edge("armhole", [fc.Bezier(
                SH_END, fc.P(SH_END.x - 18.0, SH_END.y - AH * 0.38),
                fc.P(W - 4.0, UNDERARM.y + AH * 0.28), UNDERARM)]),
            fc.Edge("side_seam", [fc.curve_through(
                UNDERARM, fc.P(SEAM_X, 0.0), bulge=0.03, side=1.0)]),
            fc.Edge("waist", [fc.Line(fc.P(SEAM_X, 0.0), fc.P(CB_WAIST_X, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side_seam", 0.5, "waist match"),
                 fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("waist", 0.5, "tail match")],
        grainline=fc.Grainline(fc.P(SEAM_X * 0.5, 30.0),
                               fc.P(SEAM_X * 0.5, CHEST_Y - 20.0)),
        internals=[fc.Internal("back waist dart",
                               [fc.P(SEAM_X * 0.55, 6.0),
                                fc.P(SEAM_X * 0.55 - 6.0, CHEST_Y * 0.45),
                                fc.P(SEAM_X * 0.55, CHEST_Y - 40.0),
                                fc.P(SEAM_X * 0.55 + 6.0, CHEST_Y * 0.45),
                                fc.P(SEAM_X * 0.55, 6.0)],
                               kind="dart")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back bodice",
    )


def build_tail(waist_target):
    """The TAIL skirt (cut 2, mirrored) — the coat below the waist seam.

    Its waist edge is SOLVED by bisection to the back bodice's measured waist
    edge, so the waist seam balances rather than being trusted to arithmetic.
    It flares toward the hem (a tail that hangs must be wider at the bottom
    than at the waist) and its front edge is where the cutaway has already
    swept the front away — so the tail's front edge is a finished edge, not a
    seam.
    """
    h = tail_length
    flare = max(0.0, min(h * 0.25, 160.0))     # derived, therefore capped
    top_w = _solve_flat(
        lambda w: fc.Edge("waist", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        waist_target, "tail waist")
    bot_w = top_w + flare
    return fc.Piece(
        "tail",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, h), fc.P(top_w, h))]),
            fc.Edge("front_edge", [fc.curve_through(
                fc.P(top_w, h), fc.P(bot_w, 0.0), bulge=0.04, side=-1.0)]),
            fc.Edge("hem", [fc.Line(fc.P(bot_w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "front_edge": hem_allowance},
        notches=[fc.Notch("waist", 0.5, "bodice match")],
        grainline=fc.Grainline(fc.P(top_w * 0.45, h * 0.12),
                               fc.P(top_w * 0.45, h * 0.85)),
        internals=[fc.Internal("tail vent",
                               [fc.P(6.0, 0.0), fc.P(6.0, min(h * 0.55, h - 20.0))],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Tail (skirt)",
    )


# ── Two-piece sleeve (the tailoring convention this family uses) ─────────────
def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.66, sl + ch * 0.12),
                  fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                  fc.P(-hb * 0.66, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def _sleeve_dims(arm_target):
    """Shared dimensions so the upper and under sleeves carry IDENTICAL forearm
    and hindarm seam curves — the two vertical seams then balance by
    construction rather than by tolerance."""
    cap_target = arm_target + cap_ease
    ch = max(70.0, AH * 0.32)
    sl = max(220.0, sleeve_length - ch)
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
    chw = max(110.0, min(hb * 0.60, hb - 10.0))
    return hb, sl, ch, chw


def _forearm(chw, hb, sl):
    return fc.curve_through(fc.P(-hb, sl), fc.P(-chw, 0.0), bulge=0.03, side=-1.0)


def _hindarm(chw, hb, sl):
    return fc.curve_through(fc.P(chw, 0.0), fc.P(hb, sl), bulge=0.03, side=-1.0)


def build_upper_sleeve(arm_target):
    """Upper sleeve (cut 2, mirrored): carries the whole eased cap, and the four
    cuff-button drills that bridge to the Yantra4D button."""
    cap_target = arm_target + cap_ease
    hb, sl, ch, chw = _sleeve_dims(arm_target)
    bd = button_ligne * 0.635                  # button diameter in mm
    pitch = max(bd + 4.0, 22.0)
    return fc.Piece(
        "upper_sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("hindarm", [_hindarm(chw, hb, sl)]),
            _cap_curve(hb, sl, ch),
            fc.Edge("forearm", [_forearm(chw, hb, sl)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", (arm_target * 0.55 + cap_ease / 2.0) / cap_target,
                          "cap back match"),
                 fc.Notch("forearm", 0.5, "forearm match"),
                 fc.Notch("hindarm", 0.5, "hindarm match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.8)),
        internals=[fc.Internal(
            "cuff buttons",
            [fc.P(chw - 18.0 - i * pitch, 26.0) for i in range(CUFF_BUTTONS)]
            + [fc.P(chw - 18.0, 26.0)], kind="drill")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Upper Sleeve",
    )


def build_under_sleeve(arm_target):
    """Under sleeve (cut 2, mirrored): the same shared forearm and hindarm
    curves as the upper sleeve, with a shallow underarm scye scoop instead of a
    cap. Teaching-grade two-piece — the whole cap seam lives on the upper
    sleeve (see the honest note in docs/README.md)."""
    hb, sl, ch, chw = _sleeve_dims(arm_target)
    scoop = ch * 0.45
    return fc.Piece(
        "under_sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("hindarm", [_hindarm(chw, hb, sl)]),
            fc.Edge("scye", [fc.curve_through(
                fc.P(hb, sl), fc.P(-hb, sl),
                bulge=scoop / max(1.0, 2.0 * hb), side=1.0)]),
            fc.Edge("forearm", [_forearm(chw, hb, sl)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("forearm", 0.5, "forearm match"),
                 fc.Notch("hindarm", 0.5, "hindarm match"),
                 fc.Notch("scye", 0.5, "underarm")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Under Sleeve",
    )


def _collar_neck(flat):
    return fc.Edge("neck", [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, 14.0),
                                             bulge=0.05, side=-1.0)])


def build_collar(gorge_len, back_neck_len):
    """Upper collar, half on the CB fold: its neck edge is bisected to the
    measured gorge plus back neck per half."""
    target = gorge_len + back_neck_len
    flat = _solve_flat(_collar_neck, target, "upper-collar neck")
    point = fc.P(flat + 18.0, 14.0 + collar_height)
    return fc.Piece(
        "collar",
        [
            _collar_neck(flat),
            fc.Edge("front_edge", [fc.Line(fc.P(flat, 14.0), point)]),
            fc.Edge("top", [fc.curve_through(point, fc.P(0.0, collar_height),
                                             bulge=0.03, side=1.0)]),
            fc.Edge("cb", [fc.Line(fc.P(0.0, collar_height), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", back_neck_len / target, "gorge seam match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, collar_height * 0.5),
                               fc.P(flat * 0.7, collar_height * 0.6)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Upper Collar (half, on fold)",
    )


def build_facing(center_len, lapel_len, gorge_len, cutaway_len):
    """Front facing (cut 2, mirrored): a straight strip whose length is the
    MEASURED centre + lapel + gorge + cutaway run. On a morning coat the facing
    must continue around the cutaway curve — that is the edge that shows when
    the coat swings, so it is the edge that has to be faced."""
    length = center_len + lapel_len + gorge_len + cutaway_len + 2.0 * seam_allowance
    width = 100.0
    t_button = seam_allowance / length
    return fc.Piece(
        "facing",
        [
            fc.Edge("long_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
            fc.Edge("inner", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                    # length already carries 2×sa
        notches=[fc.Notch("long_edge", t_button, "button / cutaway start")],
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0),
                               fc.P(length * 0.8, width / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Facing",
    )


def build():
    pattern = fc.PatternSet("morning-coat")
    front = build_front()
    back = build_back()

    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    arm_target = front_ah + back_ah
    center_len = front.edge("center").length(0.05)
    lapel_len = front.edge("lapel").length(0.05)
    gorge_len = front.edge("gorge").length(0.05)
    cutaway_len = front.edge("cutaway").length(0.05)
    back_neck_len = back.edge("neck").length(0.05)
    waist_target = back.edge("waist").length(0.05)

    names = ("front", "back", "tail", "upper_sleeve", "under_sleeve",
             "collar", "facing")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["tail"]:
        pattern.add(build_tail(waist_target))
    if wanted["upper_sleeve"]:
        pattern.add(build_upper_sleeve(arm_target))
    if wanted["under_sleeve"]:
        pattern.add(build_under_sleeve(arm_target))
    if wanted["collar"]:
        pattern.add(build_collar(gorge_len, back_neck_len))
    if wanted["facing"]:
        pattern.add(build_facing(center_len, lapel_len, gorge_len, cutaway_len))

    # ── Declared seams ───────────────────────────────────────────────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"),
                             tol=1.5)
    # THE WAIST SEAM — the join that makes the tails hang. Solved by bisection.
    if wanted["tail"] and wanted["back"]:
        pattern.declare_seam(("tail", "waist"), ("back", "waist"), tol=1.5)
    # Eased two-piece cap into front + back armhole.
    if wanted["upper_sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("upper_sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")],
                             ease=cap_ease, tol=2.5)
    if wanted["upper_sleeve"] and wanted["under_sleeve"]:
        pattern.declare_seam(("upper_sleeve", "forearm"),
                             ("under_sleeve", "forearm"), tol=1.5)
        pattern.declare_seam(("upper_sleeve", "hindarm"),
                             ("under_sleeve", "hindarm"), tol=1.5)
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front", "gorge"), ("back", "neck")], tol=2.5)
    # The facing runs the whole visible front edge INCLUDING the cutaway.
    if wanted["facing"] and wanted["front"]:
        pattern.declare_seam([("facing", "long_edge")],
                             [("front", "center"), ("front", "lapel"),
                              ("front", "gorge"), ("front", "cutaway")],
                             tol=3.0, ease=2.0 * seam_allowance)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1500.0                      # lana-peinada-traje card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.55)   # curved pieces waste more
    lining_len = (total_area * 0.90) / (1400.0 * 0.60)
    bd = button_ligne * 0.635
    pattern.bom = [
        {"item": "lana-peinada-traje", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"worsted at {fabric_width:.0f} mm width, 55% marker — the "
                 "cutaway curve and the flared tails nest badly, which is why "
                 "a morning coat has always been an expensive garment to cut. "
                 "Leave the CB, side and sleeve inlays"},
        {"item": "lining (bemberg/viscose twill)",
         "qty": round(lining_len / 10.0) * 10, "unit": "mm_length",
         "note": "fully lined body, tails and two-piece sleeves; lining pieces "
                 "noted-not-drafted in v0"},
        {"item": "fusible interfacing + chest canvas (fronts, lapels, "
                 "undercollar)", "qty": 1, "unit": "set",
         "note": "the cutaway edge and the peak lapel both need a firm edge or "
                 "the curve ripples in wear"},
        {"item": "shoulder pads + sleeve heads", "qty": 1, "unit": "pair",
         "note": "a formal-coat shoulder. A printed pad former is a Yantra4D "
                 "cartridge reference, never re-implemented here"},
        {"item": f"sew-through button {bd:.1f} mm ({button_ligne:.0f} ligne), "
                 "front", "qty": 1, "unit": "pcs",
         "note": "the SINGLE fastening button — the morning coat closes at one "
                 "point and cuts away below it (see notion.hardware_ref)"},
        {"item": f"sew-through button {bd:.1f} mm, cuffs", "qty": 2 * CUFF_BUTTONS,
         "unit": "pcs", "note": f"{CUFF_BUTTONS} per cuff, same Yantra4D solid"},
        {"item": "thread + buttonhole twist", "qty": 1, "unit": "set",
         "note": "the single front buttonhole is worked, not machined, on a "
                 "coat at this level"},
    ]
    pattern.metadata = {
        "fc300_rank": 294,
        "family": "tailoring",
        "fabric_hint": "lana-peinada-traje",
        "signature": "the CUTAWAY: below the single fastening button the front "
                     "edge sweeps away in a continuous curve to the side seam, "
                     "and the coat continues behind as waist-seamed tails. The "
                     "front has no hem edge at all — the cutaway replaces it",
        "why_not_a_variant": "the commons' other coats (suit-jacket, blazer, "
                             "overcoat, trench-coat) all drop straight to a "
                             "horizontal hem; a cutaway is not a hem option, it "
                             "changes which edges exist and makes the back a "
                             "waist-seamed skirt rather than a body panel",
        "finished_mm": {"nape_to_waist": round(back_length, 1),
                        "waist_to_tail_hem": round(tail_length, 1),
                        "total_back_length": round(back_length + tail_length, 1)},
        "solved": {
            "button_y_mm": round(BUTTON_Y, 2),
            "cutaway_requested_run_mm": round(CUTAWAY_RUN, 2),
            "cutaway_span_mm": round(CUTAWAY_SPAN, 2),
            "cutaway_rise_mm": round(CUTAWAY_RISE, 2),
            "cutaway_len_mm": round(cutaway_len, 2),
            "break_x_mm": round(BREAK_X, 2),
            "side_seam_x_mm": round(SEAM_X, 2),
            "waist_target_mm": round(waist_target, 2),
            "armhole_target_mm": round(arm_target, 2),
            "button_clamped": BUTTON_CLAMPED,
            "sweep_clamped": SWEEP_CLAMPED,
            "note": "the cutaway's rise (button height) and run (sweep) are "
                    "both DERIVED and both floored before any point is built. "
                    "A negative span does not fail — it inverts the front panel, "
                    "and the kernel's CCW normalization then launders it into a "
                    "valid-LOOKING outline. The tail's waist edge and the "
                    "collar's neck edge are bisected to measured targets.",
        },
        "hardware": "single front button + cuff buttons via Yantra4D "
                    "(notion.hardware_ref -> sew-through-button); button_ligne "
                    "drives the printed button and the drilled marks together",
        "scope": "teaching-grade: fusible front plus a floating chest canvas; a "
                 "full hand-padded canvas and a drafted lining are future work",
    }
    return pattern


result = build()

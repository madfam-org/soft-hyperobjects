"""
Denim Western Shirt — Fashion Cabinet Garment Cartridge (FC-300 #290, denim, T2).

The western shirt: pointed SAWTOOTH yokes front and back, a snap-fastened centre
front placket, snap cuffs, and heavy contrast topstitching throughout. Two of its
three signature features are geometry problems that a formula gets wrong, and
both are solved here by measurement:

  1. THE SAWTOOTH YOKE SEAM IS LONGER THAN THE SHIRT IS WIDE. A western yoke's
     lower edge is not a line — it is a run of Vs. Every tooth adds length to the
     seam in proportion to its depth, and the amount it adds is NOT linear in
     either the tooth count or the tooth depth. So the sawtooth is generated once
     as a real polyline, its length is MEASURED, and the body panel below it is
     drafted against THAT SAME generated polyline rather than against a straight
     yoke line. Drafting the two independently and trusting a tooth-length
     formula is how a western yoke ends up 20 mm long on a 500 mm seam, which on
     denim is a pucker no amount of pressing removes.

  2. THE SNAP PLACKET IS PITCHED OVER A MEASURED RUN. Snaps hold only if the stud
     lands on the socket, and unlike buttons they cannot be nudged. The placket
     run is measured off the built front, both ends are held clear (the collar
     seam at the top, the hem turn at the bottom), and whole intervals are fitted
     across what is left with the pitch RECOMPUTED. A requested pitch is a
     target, never a result.

  3. THE TOOTH DEPTH IS CLAMPED AGAINST THE YOKE'S OWN HEIGHT. A tooth deeper
     than the yoke is a yoke that has been cut through. Because the kernel
     CCW-normalizes an inverted outline and area() takes an absolute value, that
     piece renders and passes verify() looking entirely healthy — so the depth is
     clamped explicitly, and the clamp is reported.

DENIM CONVENTIONS, per the family's existing cartridges (jeans-5-pocket,
denim-jacket, bib-overalls): a 7 mm twin-needle topstitch gauge carried on
out-seams, yoke seams and the placket box; flat-felled side and armhole seams
declared with the wider allowance they need; a deep hem; and every hard good a
Yantra4D reference rather than a re-implementation.

The SNAP SOLID is Yantra4D territory (`sew-on-snap`; see notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body measurements) ──────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|front_yoke|back_yoke|sleeve|cuff|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
shirt_length = float(PARAM(lambda: shirt_length, 740.0))     # HPS to hem
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))   # HPS to cuff
yoke_drop = float(PARAM(lambda: yoke_drop, 130.0))           # HPS to yoke point
tooth_count = float(PARAM(lambda: tooth_count, 3.0))         # sawtooth Vs per yoke
tooth_depth = float(PARAM(lambda: tooth_depth, 34.0))        # REQUESTED V depth
snap_diameter = float(PARAM(lambda: snap_diameter, 17.0))
snap_pitch = float(PARAM(lambda: snap_pitch, 95.0))          # REQUESTED pitch
placket_width = float(PARAM(lambda: placket_width, 34.0))
cuff_height = float(PARAM(lambda: cuff_height, 65.0))
wear_ease = float(PARAM(lambda: wear_ease, 160.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps (mirror the manifest slider bounds exactly) ───────────────────────
chest_girth = max(800.0, min(chest_girth, 1400.0))
shirt_length = max(560.0, min(shirt_length, 940.0))
shoulder_width = max(360.0, min(shoulder_width, 580.0))
neck_girth = max(320.0, min(neck_girth, 500.0))
sleeve_length = max(300.0, min(sleeve_length, 780.0))
yoke_drop = max(80.0, min(yoke_drop, 220.0))
tooth_count = max(1.0, min(tooth_count, 6.0))
tooth_depth = max(10.0, min(tooth_depth, 70.0))
snap_diameter = max(11.0, min(snap_diameter, 24.0))
snap_pitch = max(55.0, min(snap_pitch, 150.0))
placket_width = max(24.0, min(placket_width, 50.0))
cuff_height = max(40.0, min(cuff_height, 100.0))
wear_ease = max(80.0, min(wear_ease, 300.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(15.0, min(hem_allowance, 45.0))

N_TEETH = int(round(tooth_count))

# ── Derived block dimensions ─────────────────────────────────────────────────
QUARTER_CHEST = (chest_girth + wear_ease) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = neck_girth / 6.0 + 10.0             # half front neck width at the HPS
NECK_DROP_F = neck_girth / 6.0 + 18.0
NECK_DROP_B = 22.0
SHOULDER_SLOPE = 42.0
ARMHOLE_DEPTH = (chest_girth + wear_ease) / 8.0 + 100.0
TOP_Y = shirt_length                         # HPS line; hem at y = 0
YOKE_Y = TOP_Y - yoke_drop                   # the yoke's point line on the body
# Keep the armhole below the yoke point by a real margin, or the sawtooth runs
# into the armscye and the yoke seam has nowhere to land.
ARMHOLE_DEPTH = max(ARMHOLE_DEPTH, yoke_drop + tooth_depth + 70.0)
ARMHOLE_DEPTH = min(ARMHOLE_DEPTH, TOP_Y - 120.0)
UNDERARM_Y = TOP_Y - ARMHOLE_DEPTH

PW = placket_width
TOPSTITCH = 7.0                              # denim twin-needle gauge, family std

# THE TOOTH DEPTH, CLAMPED. A tooth deeper than the yoke cuts the yoke in half;
# a tooth deeper than the space between the yoke line and the underarm runs the
# sawtooth into the armhole. Both are clamped, and the clamp is reported —
# because an inverted piece is CCW-normalized by the kernel and passes verify().
_TOOTH_D_RAW = tooth_depth
TOOTH_D = max(6.0, min(_TOOTH_D_RAW,
                       yoke_drop * 0.55,
                       (YOKE_Y - UNDERARM_Y) * 0.60 if YOKE_Y > UNDERARM_Y else 6.0))


def _sawtooth(x_from, x_to, y_line, depth, teeth, dip_down):
    """The sawtooth run as a REAL polyline, generated once and reused.

    Returns the ordered points from (x_from, y_line) to (x_to, y_line) with
    `teeth` Vs of `depth` between them. `dip_down` chooses whether the points of
    the Vs go down (the yoke's lower edge) or up (the body panel's upper edge) —
    the SAME polyline, walked so that both pieces carry identical geometry.

    This is the whole trick of the cartridge: the two pieces are not drafted
    independently and reconciled by a formula, they are generated from one
    function, so their seam lengths are equal by construction and the declared
    seam proves it.
    """
    pts = [fc.P(x_from, y_line)]
    span = (x_to - x_from) / teeth
    sign = -1.0 if dip_down else 1.0
    for i in range(teeth):
        x0 = x_from + span * i
        pts.append(fc.P(x0 + span * 0.5, y_line + sign * depth))
        pts.append(fc.P(x0 + span, y_line))
    return pts


def _sawtooth_segments(pts):
    """A polyline's points → the fc.Line segments of one edge."""
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# The sawtooth spans from the centre-front placket edge out to the armhole side.
# Generated ONCE, here, at module level, and consumed by both the yoke and the
# body below it.
SAW_X_FROM = 0.0
SAW_X_TO = QUARTER_CHEST
_SAW_PTS_DOWN = _sawtooth(SAW_X_FROM, SAW_X_TO, YOKE_Y, TOOTH_D, N_TEETH, True)
_SAW_PTS_UP = list(reversed(_SAW_PTS_DOWN))


def build_front():
    """Shirt front BELOW the yoke, cut 2 mirrored, with the placket extension.

    Its top edge is the SAME generated sawtooth polyline the yoke's lower edge
    is, walked in the opposite direction — which is what makes the two seam
    lengths equal by construction rather than by arithmetic.
    """
    p_hem_cf = fc.P(-PW, 0.0)
    p_hem_side = fc.P(QUARTER_CHEST, 0.0)
    p_under = fc.P(QUARTER_CHEST, UNDERARM_Y)
    saw = _SAW_PTS_UP                       # from (QUARTER_CHEST, YOKE_Y) inwards
    p_saw_in = saw[-1]                      # (0, YOKE_Y) — the CF end of the saw
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_under)]),
        # Armhole below the yoke only — the upper armhole lives on the yoke.
        fc.Edge("armhole", [fc.Bezier(
            p_under,
            fc.P(QUARTER_CHEST - 4.0, UNDERARM_Y + (YOKE_Y - UNDERARM_Y) * 0.45),
            fc.P(QUARTER_CHEST - 9.0, YOKE_Y - 12.0),
            fc.P(saw[0].x, saw[0].y))]),
        fc.Edge("yoke_seam", _sawtooth_segments(saw)),
        fc.Edge("cf_placket", [fc.Line(p_saw_in, fc.P(-PW, YOKE_Y)),
                               fc.Line(fc.P(-PW, YOKE_Y), p_hem_cf)]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        # Flat-felled side and armhole take the wider allowance the family uses.
        allowances={"hem": hem_allowance, "side": seam_allowance + 6.0,
                    "armhole": seam_allowance + 6.0, "cf_placket": 0.0},
        notches=[fc.Notch("yoke_seam", 0.5, "yoke centre match"),
                 fc.Notch("side", 0.45, "waist level")],
        grainline=fc.Grainline(fc.P(QUARTER_CHEST * 0.45, 40.0),
                               fc.P(QUARTER_CHEST * 0.45, YOKE_Y - TOOTH_D - 30.0)),
        internals=[
            # The topstitched placket box: two lines flanking the CF, the family
            # denim convention at the 7 mm gauge.
            fc.Internal("placket box",
                        [fc.P(-PW + TOPSTITCH, 0.0), fc.P(-PW + TOPSTITCH, YOKE_Y),
                         fc.P(-TOPSTITCH, YOKE_Y), fc.P(-TOPSTITCH, 0.0)],
                        kind="trace"),
            fc.Internal("yoke topstitch",
                        [fc.P(p.x, p.y - TOPSTITCH) for p in saw],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shirt front below yoke (cut 2, mirrored)",
    )


def build_back():
    """Shirt back BELOW the yoke, cut 1 on the fold at centre back."""
    saw = _SAW_PTS_UP
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(QUARTER_CHEST, 0.0)
    p_under = fc.P(QUARTER_CHEST, UNDERARM_Y)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_under)]),
        fc.Edge("armhole", [fc.Bezier(
            p_under,
            fc.P(QUARTER_CHEST - 4.0, UNDERARM_Y + (YOKE_Y - UNDERARM_Y) * 0.45),
            fc.P(QUARTER_CHEST - 9.0, YOKE_Y - 12.0),
            fc.P(saw[0].x, saw[0].y))]),
        fc.Edge("yoke_seam", _sawtooth_segments(saw)),
        fc.Edge("cb_fold", [fc.Line(fc.P(0.0, YOKE_Y), p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "side": seam_allowance + 6.0,
                    "armhole": seam_allowance + 6.0, "cb_fold": 0.0},
        notches=[fc.Notch("yoke_seam", 0.5, "yoke centre match"),
                 fc.Notch("side", 0.45, "waist level")],
        grainline=fc.Grainline(fc.P(QUARTER_CHEST * 0.45, 40.0),
                               fc.P(QUARTER_CHEST * 0.45, YOKE_Y - TOOTH_D - 30.0)),
        internals=[
            fc.Internal("yoke topstitch",
                        [fc.P(p.x, p.y - TOPSTITCH) for p in saw],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Shirt back below yoke (cut on fold)",
    )


def _yoke(name, neck_drop, label, on_fold, placket_ext):
    """One yoke, carrying the neck, the shoulder and the upper armhole.

    Its lower edge is the generated sawtooth, walked in the OPPOSITE direction to
    the body panel's — the same polyline, so the two seam lengths are equal by
    construction. Everything a formula would have had to reconcile is simply the
    same list of points.
    """
    saw = _SAW_PTS_DOWN                     # from (0, YOKE_Y) outwards
    x_in = -placket_ext
    p_saw_in = saw[0]
    p_saw_out = saw[-1]
    p_shoulder_out = fc.P(HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE)
    p_neck_sh = fc.P(NECK_W, TOP_Y)
    p_neck_c = fc.P(x_in, TOP_Y - neck_drop)

    edges = [
        fc.Edge("yoke_seam", _sawtooth_segments(saw)),
        # Upper armhole: from the sawtooth's outer end up to the shoulder tip.
        fc.Edge("armhole", [fc.Bezier(
            p_saw_out,
            fc.P(QUARTER_CHEST - 8.0, YOKE_Y + (TOP_Y - YOKE_Y) * 0.34),
            fc.P(HALF_SHOULDER + 14.0, p_shoulder_out.y - 30.0),
            p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_sh)]),
        fc.Edge("neck", [fc.Bezier(
            p_neck_sh,
            fc.P(NECK_W * 0.55, TOP_Y - neck_drop * 0.22),
            fc.P(max(x_in, NECK_W * 0.18), p_neck_c.y),
            p_neck_c)]),
        fc.Edge("center", [fc.Line(p_neck_c, fc.P(x_in, YOKE_Y)),
                           fc.Line(fc.P(x_in, YOKE_Y), p_saw_in)]),
    ]
    cut = (fc.CutSpec(quantity=1, on_fold=True, fold_edge="center")
           if on_fold else fc.CutSpec(quantity=2, mirror=True))
    allowances = {"armhole": seam_allowance + 6.0}
    if on_fold:
        allowances["center"] = 0.0
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances=allowances,
        notches=[fc.Notch("yoke_seam", 0.5, "body centre match"),
                 fc.Notch("armhole", 0.5, "sleeve cap match")],
        grainline=fc.Grainline(fc.P(NECK_W * 0.9, YOKE_Y + 16.0),
                               fc.P(NECK_W * 0.9, TOP_Y - neck_drop - 12.0)),
        internals=[
            fc.Internal("yoke seam topstitch",
                        [fc.P(p.x, p.y + TOPSTITCH) for p in saw],
                        kind="trace"),
        ],
        cut=cut,
        label=label,
    )


def build_front_yoke():
    # The front yoke carries the placket extension, so it is cut 2 mirrored.
    return _yoke("front_yoke", NECK_DROP_F, "Front sawtooth yoke (cut 2, mirrored)",
                 False, PW)


def build_back_yoke():
    return _yoke("back_yoke", NECK_DROP_B, "Back sawtooth yoke (cut on fold)",
                 True, 0.0)


# ── Solve the sleeve cap against the MEASURED armholes ───────────────────────
_F = build_front()
_B = build_back()
_FY = build_front_yoke()
_BY = build_back_yoke()
# ONE armscye ring is four measured edges: the front body's armhole, the front
# yoke's, the back body's and the back yoke's — because the yoke split each
# armhole in two. The front and back pieces are each ONE SIDE of the shirt (front
# is cut 2 mirrored; back is cut on the fold and its `armhole` edge is one side's
# worth), so this sum is a single armhole, not both.
ARMSCYE = (_F.edge("armhole").length(0.1) + _FY.edge("armhole").length(0.1)
           + _B.edge("armhole").length(0.1) + _BY.edge("armhole").length(0.1))
# A woven shirt sleeve is set with real cap ease — denim takes less than a
# poplin shirt because it will not shrink in, so this is the low end.
CAP_EASE = 18.0
CAP_TARGET = ARMSCYE + CAP_EASE


def _cap_curve(half_b, under_y, cap_h):
    """A symmetric two-Bézier sleeve cap of height cap_h over width 2·half_b."""
    apex = fc.P(0.0, under_y + cap_h)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(half_b, under_y),
                  fc.P(half_b * 0.68, under_y + cap_h * 0.10),
                  fc.P(half_b * 0.30, under_y + cap_h), apex),
        fc.Bezier(apex,
                  fc.P(-half_b * 0.30, under_y + cap_h),
                  fc.P(-half_b * 0.68, under_y + cap_h * 0.10),
                  fc.P(-half_b, under_y)),
    ])


def _solve_half_biceps(cap_h):
    """Bisect the half-biceps until the MEASURED cap equals CAP_TARGET."""
    lo, hi = 60.0, CAP_TARGET
    half = hi
    for _ in range(64):
        half = (lo + hi) / 2.0
        if _cap_curve(half, 0.0, cap_h).length(0.05) < CAP_TARGET:
            lo = half
        else:
            hi = half
    return half


CAP_H = max(60.0, ARMHOLE_DEPTH * 0.42)
HALF_BICEPS = _solve_half_biceps(CAP_H)

# The cuff opening: the sleeve's hem is pleated down to the cuff, so the cuff is
# the finished wrist circumference, not the sleeve's flat width.
CUFF_OPENING = max(180.0, HALF_BICEPS * 1.30)


def build_sleeve():
    """Sleeve, cut 2 mirrored, with a marked placket slit and two hem pleats."""
    under_y = max(120.0, sleeve_length - CAP_H - cuff_height)
    hem_half = CUFF_OPENING / 2.0 + 26.0     # the pleats take up the 26 mm ×2
    edges = [
        fc.Edge("sleeve_hem", [fc.Line(fc.P(-hem_half, 0.0), fc.P(hem_half, 0.0))]),
        fc.Edge("under_back", [fc.Line(fc.P(hem_half, 0.0),
                                       fc.P(HALF_BICEPS, under_y))]),
        _cap_curve(HALF_BICEPS, under_y, CAP_H),
        fc.Edge("under_front", [fc.Line(fc.P(-HALF_BICEPS, under_y),
                                        fc.P(-hem_half, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"under_back": seam_allowance + 6.0,
                    "under_front": seam_allowance + 6.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point match"),
                 fc.Notch("cap", 0.25, "back cap match"),
                 fc.Notch("cap", 0.75, "front cap match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, under_y + CAP_H * 0.5)),
        internals=[
            fc.Internal("placket slit",
                        [fc.P(hem_half * 0.45, 0.0),
                         fc.P(hem_half * 0.45, min(130.0, under_y * 0.42))],
                        kind="marking"),
            fc.Internal("hem pleat 1",
                        [fc.P(hem_half * 0.20, 0.0), fc.P(hem_half * 0.20, 42.0)],
                        kind="marking"),
            fc.Internal("hem pleat 2",
                        [fc.P(hem_half * 0.20 + 26.0, 0.0),
                         fc.P(hem_half * 0.20 + 26.0, 42.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


# ── Solve the snap column across the MEASURED placket run ───────────────────
# The run the snaps actually occupy: the front's centre-front placket edge from
# the yoke seam down to the hem. MEASURED off the built front — the edge is two
# segments (the CF run and the turn onto the hem), and only the vertical run
# carries snaps, so the measured total is reduced by the placket's own width.
PLACKET_EDGE_RUN = _F.edge("cf_placket").length(0.05)
CF_RUN = max(snap_diameter * 3.0, PLACKET_EDGE_RUN - PW)
TOP_CLEAR = max(26.0, snap_diameter * 1.5)    # clear of the yoke seam
BOT_CLEAR = max(hem_allowance + 12.0, snap_diameter * 1.6)   # clear of the hem turn
SNAP_RUN = max(snap_diameter * 2.0, CF_RUN - TOP_CLEAR - BOT_CLEAR)
N_INTERVALS = max(1, int(round(SNAP_RUN / snap_pitch)))
N_SNAPS_CF = N_INTERVALS + 1
PITCH_SOLVED = SNAP_RUN / N_INTERVALS
# Two more per cuff, and one on each sleeve placket.
N_SNAPS_CUFF = 2
N_SNAPS_TOTAL = N_SNAPS_CF + 2 * (N_SNAPS_CUFF + 1)


def build_cuff():
    """Barrel cuff, cut 2 (each doubled and folded in construction)."""
    w = CUFF_OPENING + 2.0 * seam_allowance + 22.0    # + the snap overlap
    h = cuff_height * 2.0                             # folded lengthwise
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("end_over", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("upper", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("end_under", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("fold line", [fc.P(0.0, h / 2.0), fc.P(w, h / 2.0)],
                    kind="marking"),
        fc.Internal("cuff topstitch",
                    [fc.P(TOPSTITCH, TOPSTITCH), fc.P(w - TOPSTITCH, TOPSTITCH)],
                    kind="trace"),
    ]
    # Two snaps per cuff, on the overlap, spaced by the snap's own diameter so
    # the pair sits square rather than in a diagonal.
    for i in range(N_SNAPS_CUFF):
        x = w - 16.0 - snap_diameter * 1.5 * i
        internals.append(fc.Internal(
            f"cuff snap {i + 1}",
            [fc.P(x - snap_diameter / 2.0, h * 0.25),
             fc.P(x + snap_diameter / 2.0, h * 0.25)],
            kind="drill"))
    return fc.Piece(
        "cuff", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.0, "under end"),
                 fc.Notch("lower", 1.0, "over end")],
        grainline=fc.Grainline(fc.P(w * 0.12, h / 2.0), fc.P(w * 0.88, h / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Barrel cuff (cut 2)",
    )


def build():
    pattern = fc.PatternSet("denim-western-shirt")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "front_yoke": everything or target_piece == "front_yoke",
        "back_yoke": everything or target_piece == "back_yoke",
        "sleeve": everything or target_piece == "sleeve",
        "cuff": everything or target_piece == "cuff",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        f = pattern.add(build_front())
        # The CF snap column, drilled onto the built front at the SOLVED pitch.
        for i in range(N_SNAPS_CF):
            y = BOT_CLEAR + PITCH_SOLVED * i
            f.internals.append(fc.Internal(
                f"cf snap {i + 1}",
                [fc.P(-PW / 2.0 - snap_diameter / 2.0, y),
                 fc.P(-PW / 2.0 + snap_diameter / 2.0, y)],
                kind="drill"))
    if want["back"]:
        pattern.add(build_back())
    if want["front_yoke"]:
        pattern.add(build_front_yoke())
    if want["back_yoke"]:
        pattern.add(build_back_yoke())
    if want["sleeve"]:
        pattern.add(build_sleeve())
    if want["cuff"]:
        pattern.add(build_cuff())

    # ── Declared seams ───────────────────────────────────────────────────────
    # THE sawtooth check: yoke lower edge vs body upper edge. Both are the same
    # generated polyline, so this closes at delta = 0 — and it is declared at a
    # tight tolerance precisely so it would go red the day somebody redrafts one
    # of the two by formula instead of from the shared generator.
    if want["front"] and want["front_yoke"]:
        pattern.declare_seam(("front_yoke", "yoke_seam"), ("front", "yoke_seam"),
                             tol=0.3)
    if want["back"] and want["back_yoke"]:
        pattern.declare_seam(("back_yoke", "yoke_seam"), ("back", "yoke_seam"),
                             tol=0.3)
    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    if want["front_yoke"] and want["back_yoke"]:
        pattern.declare_seam(("front_yoke", "shoulder"), ("back_yoke", "shoulder"),
                             tol=1.0)
    if all(want[k] for k in ("sleeve", "front", "back", "front_yoke", "back_yoke")):
        # One cap sews to ONE armscye ring, which the yoke split into four
        # measured edges: front body + front yoke + back body + back yoke. The
        # declared ease is the real cap ease the sleeve is set with.
        pattern.declare_seam(
            ("sleeve", "cap"),
            [("front", "armhole"), ("front_yoke", "armhole"),
             ("back", "armhole"), ("back_yoke", "armhole")],
            tol=2.0, ease=CAP_EASE)
    if want["sleeve"]:
        pattern.declare_seam(("sleeve", "under_front"), ("sleeve", "under_back"),
                             tol=1.0)

    fabric_width = 1500.0                       # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "mezclilla-denim, 12 oz (407 gsm)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 76% marker; a lighter 8–10 oz "
                 f"denim or a chambray suits this shirt better in warm weather — "
                 f"the draft is unchanged, only the hand."},
        {"item": "sew-on snap", "qty": N_SNAPS_TOTAL, "unit": "pair",
         "note": f"Yantra4D sew-on-snap (notion.hardware_ref) at "
                 f"{snap_diameter:.0f} mm: {N_SNAPS_CF} on the front placket at a "
                 f"SOLVED pitch of {PITCH_SOLVED:.1f} mm across a MEASURED "
                 f"{CF_RUN:.0f} mm run (requested {snap_pitch:.0f} mm), plus "
                 f"{N_SNAPS_CUFF} per cuff and one per sleeve placket."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 2, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm: both yoke seams, the "
                 f"placket box, cuffs and flat-felled side seams. Two spools — "
                 f"a western shirt is mostly topstitch."},
        {"item": "shirt-weight fusible interfacing",
         "qty": round(CF_RUN * 2.2 + CUFF_OPENING * 2.4), "unit": "mm_length",
         "note": "both placket edges and both cuffs. A sew-on snap through "
                 "unbacked denim works its own hole open over a season."},
    ]
    pattern.metadata = {
        "fc300_rank": 290,
        "family": "denim",
        "tier": 2,
        "fabric_hint": "mezclilla-denim",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "shirt_length": round(shirt_length, 1),
            "yoke_drop": round(yoke_drop, 1),
            "armhole_depth": round(ARMHOLE_DEPTH, 1),
            "sleeve_length": round(sleeve_length, 1),
            "cuff_opening": round(CUFF_OPENING, 1),
            "placket_width": round(PW, 1),
        },
        "solved": {
            "tooth_count": N_TEETH,
            "tooth_depth_requested_mm": round(_TOOTH_D_RAW, 2),
            "tooth_depth_clamped_mm": round(TOOTH_D, 2),
            "tooth_depth_was_clamped": bool(abs(TOOTH_D - _TOOTH_D_RAW) > 0.01),
            "sawtooth_span_mm": round(SAW_X_TO - SAW_X_FROM, 2),
            "sawtooth_run_measured_mm": round(_FY.edge("yoke_seam").length(0.05), 2),
            "sawtooth_added_over_straight_mm": round(
                _FY.edge("yoke_seam").length(0.05) - (SAW_X_TO - SAW_X_FROM), 2),
            "placket_edge_measured_mm": round(PLACKET_EDGE_RUN, 2),
            "cf_snap_run_mm": round(CF_RUN, 2),
            "snap_count_cf": N_SNAPS_CF,
            "snap_count_total": N_SNAPS_TOTAL,
            "snap_pitch_requested_mm": round(snap_pitch, 2),
            "snap_pitch_solved_mm": round(PITCH_SOLVED, 3),
            "armscye_measured_mm": round(ARMSCYE, 2),
            "cap_ease_mm": round(CAP_EASE, 2),
            "cap_target_mm": round(CAP_TARGET, 2),
            "half_biceps_solved_mm": round(HALF_BICEPS, 2),
            "cap_height_mm": round(CAP_H, 2),
            "note": "the sawtooth is generated ONCE as a real polyline and both the "
                    "yoke's lower edge and the body panel's upper edge are built "
                    "from it — walked in opposite directions — so their seam lengths "
                    "are equal BY CONSTRUCTION rather than reconciled by a "
                    "tooth-length formula, which is not linear in either the tooth "
                    "count or the depth. The declared seam sits at tol=0.3 so it "
                    "goes red the day somebody redrafts one side independently. The "
                    "snap pitch is a TARGET: whole intervals are fitted to the "
                    "MEASURED placket run less both clearances and the pitch "
                    "recomputed. The tooth depth is clamped against the yoke drop "
                    "AND against the space above the underarm, because a tooth "
                    "deeper than its yoke inverts the piece — and an inverted piece "
                    "is CCW-normalized by the kernel and passes verify() looking "
                    "healthy.",
        },
        "topstitch": f"twin-needle heavy contrast (gold) at {TOPSTITCH:.0f} mm, the "
                     f"denim-family gauge: both sawtooth yoke seams, the placket "
                     f"box, both cuffs; side and armhole seams flat-felled at "
                     f"{seam_allowance + 6.0:.0f} mm",
        "denim_conventions": {
            "flat_felled": f"side, armhole and sleeve underarm seams carry "
                           f"{seam_allowance + 6.0:.0f} mm — the family convention "
                           f"for a felled seam on 12 oz",
            "gauge": f"{TOPSTITCH:.0f} mm twin-needle throughout, matching "
                     f"jeans-5-pocket, denim-jacket and bib-overalls",
            "hard_goods": "every snap is a Yantra4D reference, never re-implemented",
        },
        "hardware": "sew-on snaps via Yantra4D (notion.hardware_ref -> sew-on-snap); "
                    "the solid's snap_dia — the parameter driving its sew_face "
                    "flange, i.e. the sewn mating face — is fed from this garment's "
                    "snap_diameter, which is also what sizes the placket the column "
                    "runs on and every drilled snap mark on the cuffs.",
    }
    return pattern


result = build()

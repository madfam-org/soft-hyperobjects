"""
Post-Surgical Access Tee — Fashion Cabinet Garment Cartridge (FC-300 #249, adaptive II).

A tee whose shoulder and upper sleeve open on a column of snaps, so a chest port,
a PICC line, a shoulder wound, a pacemaker site or a drain can be reached, dressed
and flushed WITHOUT the garment coming off over the head or over the affected arm.

The problem this is drafted against is specific. Someone with a chest port comes in
for a flush; someone with a shoulder repair has a dressing changed; someone on
telemetry needs leads moved. In each case the standard instruction is "take your
top off", which for a person with a fresh surgical shoulder, a drain pinned to
their waistband, or an arm that will not abduct means being undressed by somebody
else in a cold room, or wearing a hospital gown that opens at the back and covers
nothing. This tee is an ordinary tee from a metre away and opens along its own
shoulder seam from neck to mid-sleeve on one straight run of snaps.

The drafting problems that had to be solved, not assumed:

  1. SNAP COLUMN REGISTER. A snap pair holds only if the stud lands on the socket.
     The access run is not one seam but TWO joined seams (shoulder, then the upper
     sleeve seam), so its length is MEASURED across both pieces and the snap pitch
     is then recomputed from WHOLE intervals across that measured run — a requested
     pitch is a target, never a result, or the column drifts and the last snap
     lands in a seam allowance.

  2. SHOULDER SEAM EQUALITY. The back neck sits higher than the front neck, so
     drafting both at the same neck width leaves the back shoulder ~23 mm long.
     The back neck WIDTH is solved by Pythagoras from the front's MEASURED
     shoulder length against the vertical offset between the two neck points. On
     an ordinary tee that mismatch is a wrinkle; on this one it puts every snap
     in the column out of register, which is a garment that will not shut.

  3. ACCESS PANEL SIZE. The opening has to be big enough to admit a gloved hand
     and a dressing tray, not just a cannula. The panel's clear span is measured
     from the built pieces and reported, so the maker can see the actual number
     rather than trusting that "the shoulder opens".

Pieces:
  - front       : tee front (cut 1 on fold at CF), snap stand along the shoulder.
  - back        : tee back (cut 1 on fold at CB), matching snap stand.
  - sleeve      : sleeve (cut 2 mirrored), split along its upper seam, snap stands
                  on both halves of the split so the access run carries on.
  - snap_facing : the reinforcing facing strip that backs every snap (cut 4).

The snap SOLID is Yantra4D territory (`sew-on-snap`; see notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|snap_facing|set

chest_girth = float(PARAM(lambda: chest_girth, 980.0))
tee_length = float(PARAM(lambda: tee_length, 680.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 440.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 240.0))
snap_diameter = float(PARAM(lambda: snap_diameter, 15.0))
snap_pitch = float(PARAM(lambda: snap_pitch, 45.0))
access_extent = float(PARAM(lambda: access_extent, 0.70))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (sane garment ranges) ─────────────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1500.0))
tee_length = max(520.0, min(tee_length, 880.0))
shoulder_width = max(320.0, min(shoulder_width, 560.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(100.0, min(sleeve_length, 620.0))
snap_diameter = max(9.0, min(snap_diameter, 24.0))
snap_pitch = max(25.0, min(snap_pitch, 90.0))
access_extent = max(0.35, min(access_extent, 0.95))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE_CHEST = 130.0                    # a tee pulled on past a drain wants room
QUARTER_CHEST = (chest_girth + EASE_CHEST) / 4.0
HALF_SHOULDER = shoulder_width / 2.0

NECK_W = neck_girth / 6.0 + 12.0      # half front neck width at the shoulder
NECK_DROP_F = neck_girth / 6.0 + 26.0 # a wide, low crew — the head still has to pass
NECK_DROP_B = 24.0
SHOULDER_SLOPE = 38.0
ARMHOLE_DROP = 235.0                  # dropped: an arm that will not abduct
TOP_Y = tee_length - NECK_DROP_F      # y of the front neck point (the piece top)

# The snap STAND: the extension added along the shoulder edge that carries the
# snaps. Both stands are the same width, mirrored about the finished shoulder
# line, which is what puts stud and socket on top of each other.
STAND = snap_diameter / 2.0 + 11.0


def _armhole(p_side_top, p_shoulder_out):
    """The armhole scoop, drafted identically on front and back."""
    return fc.Bezier(
        p_side_top,
        fc.P(p_side_top.x - 5.0, p_side_top.y + ARMHOLE_DROP * 0.45),
        fc.P(p_shoulder_out.x + 14.0, p_shoulder_out.y - 42.0),
        p_shoulder_out)


def build_front():
    """Tee front, cut 1 on fold at centre front.

    The shoulder edge carries the snap stand as a cut-on extension: the edge is
    drafted STAND mm above the finished shoulder line, so folding the stand back
    on itself puts the snap column exactly on the seam.
    """
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(QUARTER_CHEST, 0.0)
    p_side_top = fc.P(QUARTER_CHEST, TOP_Y - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, TOP_Y)
    p_neck_cf = fc.P(0.0, TOP_Y - NECK_DROP_F * 0.10)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [_armhole(p_side_top, p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.54, TOP_Y - 12.0),
                                   fc.P(NECK_W * 0.20, p_neck_cf.y),
                                   p_neck_cf)]),
        fc.Edge("cf_fold", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        # The shoulder takes the STAND instead of a plain seam allowance: that
        # extension IS the snap carrier, folded back and topstitched.
        allowances={"hem": 24.0, "cf_fold": 0.0, "shoulder": STAND},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap front match"),
                 fc.Notch("side", 0.60, "waist level")],
        grainline=fc.Grainline(fc.P(QUARTER_CHEST * 0.45, 50.0),
                               fc.P(QUARTER_CHEST * 0.45, TOP_Y - 60.0)),
        internals=[
            # Where a chest port usually sits: upper chest, below the clavicle,
            # a hand's width off centre. Marked so the maker can check the open
            # panel actually clears it before cutting.
            fc.Internal("port-site-check",
                        [fc.P(70.0, TOP_Y - 150.0), fc.P(150.0, TOP_Y - 150.0),
                         fc.P(150.0, TOP_Y - 70.0), fc.P(70.0, TOP_Y - 70.0),
                         fc.P(70.0, TOP_Y - 150.0)],
                        kind="marking"),
            fc.Internal("shoulder-stitch-line",
                        [fc.P(NECK_W, TOP_Y),
                         fc.P(HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Tee front (cut on fold)",
    )


# ── Solve the back neck width so the shoulder seams MATCH ────────────────────
# The snap column runs down this seam. If front and back shoulders differ in
# length, every snap after the first is out of register — on an ordinary tee the
# same error is only a wrinkle, here it is a garment that will not shut. So the
# back neck WIDTH is solved from the front's MEASURED shoulder length.
_F_PROBE = build_front()
_SHOULDER_LEN = _F_PROBE.edge("shoulder").length(0.2)
_BACK_NECK_Y_OFF = NECK_DROP_F - NECK_DROP_B - SHOULDER_SLOPE * 0.10
_dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
if _SHOULDER_LEN <= abs(_dy):
    # Degenerate: the vertical run alone exceeds the shoulder length. Flatten the
    # back neck rise until a real horizontal run is left.
    _dy = _SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = TOP_Y + _BACK_NECK_Y_OFF


def build_back():
    """Tee back, cut 1 on fold at centre back, with the matching snap stand."""
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(QUARTER_CHEST, 0.0)
    p_side_top = fc.P(QUARTER_CHEST, TOP_Y - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, BACK_NECK_Y + 7.0)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [_armhole(p_side_top, p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.56, p_neck_shoulder.y + 3.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y),
                                   p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 24.0, "cb_fold": 0.0, "shoulder": STAND},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match"),
                 fc.Notch("side", 0.60, "waist level")],
        grainline=fc.Grainline(fc.P(QUARTER_CHEST * 0.45, 50.0),
                               fc.P(QUARTER_CHEST * 0.45, BACK_NECK_Y - 60.0)),
        internals=[
            fc.Internal("shoulder-stitch-line",
                        [fc.P(NECK_W_BACK, BACK_NECK_Y),
                         fc.P(HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Tee back (cut on fold)",
    )


# ── Solve the sleeve cap against the MEASURED armholes ───────────────────────
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 12.0                       # a dropped cap in jersey takes very little
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
BICEPS = max(320.0, (ARMHOLE_F + ARMHOLE_B) * 0.76)


def _cap_segments(cap_h, top_y):
    """A symmetric two-Bézier cap of height cap_h, left underarm to right."""
    half = BICEPS / 2.0
    p_l = fc.P(-half, top_y - cap_h)
    p_top = fc.P(0.0, top_y)
    p_r = fc.P(half, top_y - cap_h)
    return [
        fc.Bezier(p_l, fc.P(-half * 0.71, top_y - cap_h * 0.94),
                  fc.P(-half * 0.33, top_y - cap_h * 0.06), p_top),
        fc.Bezier(p_top, fc.P(half * 0.33, top_y - cap_h * 0.06),
                  fc.P(half * 0.71, top_y - cap_h * 0.94), p_r),
    ]


def _solve_cap_height():
    """Bisect the cap height until the MEASURED cap equals CAP_TARGET."""
    lo, hi = 20.0, BICEPS * 0.95
    def f(ch):
        return sum(s.length(0.2) for s in _cap_segments(ch, 0.0)) - CAP_TARGET
    f_lo, f_hi = f(lo), f(hi)
    if f_lo * f_hi > 0.0:
        return lo if abs(f_lo) < abs(f_hi) else hi
    for _ in range(80):
        mid = (lo + hi) / 2.0
        f_mid = f(mid)
        if abs(f_mid) < 0.02:
            return mid
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


CAP_H = _solve_cap_height()

# How far along the sleeve the access split runs, as a fraction of sleeve length.
SPLIT_RUN = sleeve_length * access_extent


def build_sleeve():
    """Sleeve, cut 2 mirrored, SPLIT along its upper seam for SPLIT_RUN.

    Drafted as ONE piece whose upper edge is the split: the two halves of the
    split are the same edge walked from opposite ends, so this piece is cut twice
    (mirrored) and the mirrored pair forms the sleeve. Cutting the split as a
    real edge rather than a slash is what lets both sides carry a snap stand and
    a facing — a slashed sleeve frays at the very point that is handled most.
    """
    half = BICEPS / 2.0
    hem_half = max(85.0, half * 0.80)
    top_y = sleeve_length + CAP_H
    cap = _cap_segments(CAP_H, top_y)
    p_l_under = fc.P(-half, top_y - CAP_H)
    p_r_under = fc.P(half, top_y - CAP_H)
    p_l_hem = fc.P(-hem_half, 0.0)
    p_r_hem = fc.P(hem_half, 0.0)

    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r_under, p_r_hem)]),
        fc.Edge("sleeve_hem", [fc.Line(p_r_hem, p_l_hem)]),
        fc.Edge("under_l", [fc.Line(p_l_hem, p_l_under)]),
    ]
    # The split line: down the sleeve's centre (which is the shoulder line when
    # the sleeve is set in) for SPLIT_RUN from the cap point.
    split = fc.Internal(
        "access-split",
        [fc.P(0.0, top_y), fc.P(0.0, max(0.0, top_y - SPLIT_RUN))],
        kind="marking")
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"sleeve_hem": 26.0},
        notches=[fc.Notch("cap", 0.50, "shoulder point / split head"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, top_y - CAP_H - 20.0)),
        internals=[
            split,
            fc.Internal("split-stand-front",
                        [fc.P(-STAND, top_y - 10.0),
                         fc.P(-STAND, max(0.0, top_y - SPLIT_RUN))],
                        kind="marking"),
            fc.Internal("split-stand-back",
                        [fc.P(STAND, top_y - 10.0),
                         fc.P(STAND, max(0.0, top_y - SPLIT_RUN))],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (split for access)",
    )


# ── Solve the snap column across the MEASURED access run ─────────────────────
# The access run is TWO seams end to end: the shoulder seam, then the sleeve
# split. Measure the shoulder from the built front (not from HALF_SHOULDER minus
# NECK_W — that ignores the curve of nothing but happens to be a line today, and
# would silently go wrong the day the shoulder is redrafted as a curve).
_S = build_sleeve()
SHOULDER_RUN = _F.edge("shoulder").length(0.2)
ACCESS_RUN = SHOULDER_RUN + SPLIT_RUN

# Both ends are held clear: the neck end so the first snap never fouls the neck
# binding, the sleeve end so the last snap is not sitting on the bar-tack that
# stops the split.
NECK_CLEAR = max(18.0, snap_diameter * 1.1)
TIP_CLEAR = max(20.0, snap_diameter * 1.3)
SNAP_RUN = max(snap_diameter * 2.0, ACCESS_RUN - NECK_CLEAR - TIP_CLEAR)

# Whole intervals at (or just under) the requested pitch, then the pitch
# RECOMPUTED so the column lands exactly on both clearances instead of drifting.
N_INTERVALS = max(1, int(round(SNAP_RUN / snap_pitch)))
N_SNAPS = N_INTERVALS + 1
PITCH_SOLVED = SNAP_RUN / N_INTERVALS

# How many of them fall on the shoulder vs on the sleeve split — reported so the
# maker knows how many facings go where.
_S_ON_SHOULDER = sum(
    1 for i in range(N_SNAPS)
    if NECK_CLEAR + PITCH_SOLVED * i <= SHOULDER_RUN)
N_SNAPS_SHOULDER = _S_ON_SHOULDER
N_SNAPS_SLEEVE = N_SNAPS - _S_ON_SHOULDER

# The clear span of the opened panel: the access run is the hinge, and the panel
# swings open to roughly the armhole depth. Reported as a real number so nobody
# has to trust the phrase "the shoulder opens".
ACCESS_SPAN = min(ARMHOLE_F, ARMHOLE_B) * 0.80


def build_snap_facing():
    """The reinforcing facing strip that backs the snap column (cut 4).

    Four: one behind each of the four stands (front shoulder, back shoulder, and
    the two sides of the sleeve split). A sew-on snap pulled through unbacked
    jersey tears a hole on the second or third use; this strip is the difference
    between a garment that survives daily port access and one that does not.
    """
    w = STAND * 2.0
    ln = ACCESS_RUN
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, w)
    p3 = fc.P(0.0, w)
    edges = [
        fc.Edge("lower", [fc.Line(p0, p1)]),
        fc.Edge("end_tip", [fc.Line(p1, p2)]),
        fc.Edge("upper", [fc.Line(p2, p3)]),
        fc.Edge("end_neck", [fc.Line(p3, p0)]),
    ]
    internals = []
    # Every snap centre, drilled on the facing's own centreline. Because the
    # facing is cut to the MEASURED access run, these marks transfer 1:1 to the
    # stands — the facing is the registration jig for the whole column.
    for i in range(N_SNAPS):
        x = NECK_CLEAR + PITCH_SOLVED * i
        internals.append(fc.Internal(
            f"snap-{i + 1}",
            [fc.P(x - snap_diameter / 2.0, w / 2.0),
             fc.P(x + snap_diameter / 2.0, w / 2.0)],
            kind="drill"))
    internals.append(fc.Internal(
        "shoulder-sleeve-junction",
        [fc.P(SHOULDER_RUN, 0.0), fc.P(SHOULDER_RUN, w)],
        kind="marking"))
    return fc.Piece(
        "snap_facing", edges,
        seam_allowance=seam_allowance,
        allowances={"end_neck": 0.0, "end_tip": 0.0},
        notches=[fc.Notch("lower", 0.0, "neck end"),
                 fc.Notch("lower", min(0.99, SHOULDER_RUN / ln),
                          "shoulder / sleeve junction")],
        grainline=fc.Grainline(fc.P(25.0, w / 2.0), fc.P(ln - 25.0, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=4),
        label="Snap facing strip",
    )


def build():
    pattern = fc.PatternSet("post-surgical-access-tee")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "snap_facing":
        pattern.add(build_snap_facing())

    if everything:
        # The load-bearing check: the two shoulder edges the snap column runs
        # down must measure the same, or every snap after the first is out of
        # register. tol=0.5 — tighter than a normal shoulder, because this one
        # carries hardware.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=0.5)
        # Side seams sew closed conventionally.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        # Sleeve cap takes one front armhole plus one back armhole, with ease.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "cotton/elastane jersey, 180 gsm", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1600 mm width, 78% marker; a soft jersey lies flat under a "
                 "dressing and does not print a seam into a fresh scar."},
        {"item": "sew-on snap", "qty": N_SNAPS * 2, "unit": "count",
         "note": f"Yantra4D sew-on-snap (notion.hardware_ref) at "
                 f"{snap_diameter:.0f} mm: {N_SNAPS} pairs = {N_SNAPS * 2} halves, "
                 f"{N_SNAPS_SHOULDER} on the shoulder and {N_SNAPS_SLEEVE} on the "
                 f"sleeve split, at a SOLVED pitch of {PITCH_SOLVED:.1f} mm."},
        {"item": "lightweight knit interfacing", "qty": round(ACCESS_RUN * 4.2),
         "unit": "mm_length",
         "note": "behind all four snap facings; an unbacked snap tears jersey on "
                 "about the third use."},
        {"item": "neck binding, 22 mm folded", "qty": round(neck_girth * 1.35),
         "unit": "mm_length",
         "note": "applied AFTER the snap stands, so the first snap is never "
                 "trapped under the binding."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "bar-tack the head of the sleeve split — that is where the "
                 "opening stops and where it will tear if it does not."},
    ]
    pattern.metadata = {
        "fc300_rank": 249,
        "family": "adaptive",
        "fabric_hint": "jersey-algodon",
        "finished_mm": {
            "tee_length": round(tee_length, 1),
            "quarter_chest": round(QUARTER_CHEST, 1),
            "sleeve_length": round(sleeve_length, 1),
            "stand_width": round(STAND, 1),
        },
        "solved": {
            "shoulder_run_measured_mm": round(SHOULDER_RUN, 2),
            "sleeve_split_run_mm": round(SPLIT_RUN, 2),
            "access_run_total_mm": round(ACCESS_RUN, 2),
            "snap_count": N_SNAPS,
            "snap_pitch_requested_mm": round(snap_pitch, 2),
            "snap_pitch_solved_mm": round(PITCH_SOLVED, 3),
            "snaps_on_shoulder": N_SNAPS_SHOULDER,
            "snaps_on_sleeve": N_SNAPS_SLEEVE,
            "access_clear_span_mm": round(ACCESS_SPAN, 1),
            "back_neck_half_width_mm": round(NECK_W_BACK, 2),
            "front_shoulder_measured_mm": round(_SHOULDER_LEN, 2),
            "sleeve_cap_height_mm": round(CAP_H, 2),
            "note": "the snap pitch is a TARGET: whole intervals are fitted to the "
                    "MEASURED access run (shoulder + sleeve split) and the pitch "
                    "recomputed, so the column lands on both clearances instead of "
                    "drifting. The back neck width is solved by Pythagoras from the "
                    "front's MEASURED shoulder, because an unequal shoulder puts every "
                    "snap after the first out of register.",
        },
        "adaptive": {
            "clinical_access": "shoulder and upper sleeve open neck-to-mid-sleeve on one "
                               "straight snap run — chest port, PICC line, shoulder "
                               "dressing, pacemaker site, telemetry leads, all reachable "
                               "with the garment still on",
            "no_overhead": "nothing has to pass over the head or over the affected arm",
            "dignity": "reads as an ordinary crew tee from a metre away; the opening is a "
                       "shoulder seam, which is where a seam belongs anyway",
            "access_span_mm": round(ACCESS_SPAN, 1),
        },
        "hardware": "sew-on snaps via Yantra4D (notion.hardware_ref -> sew-on-snap); the "
                    "solid's sew_face flange is driven by this tee's snap_diameter, which "
                    "is also what sizes the stand the column is carried on",
    }
    return pattern


result = build()

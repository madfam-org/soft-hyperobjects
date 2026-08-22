"""
Regency Spencer — Fashion Cabinet Costume Cartridge (FC-300 rank #276, y4d hook bridged).

The short high-waisted jacket of c. 1800–1825. A spencer is a garment defined by what it
LACKS: it is a coat bodice with the skirts cut off entirely, ending at the high Empire
waistline directly under the bust. It is worn over a gown of the same period, and its whole
job is to be short enough that the gown's waistline continues uninterrupted underneath.

The documented construction this draft reproduces:

  - a body ending at the HIGH waist — directly under the bust, not at the natural waist. A
    spencer cut to the natural waist is not a spencer; it is a short jacket, and it fights
    the Empire line of the gown it is worn over instead of completing it;
  - shaping taken at the SIDE and back seams and by the curve of the underbust seam, not by
    modern bust darts — the period bodice is small-scale and seamed, and a dart in it reads
    immediately as modern;
  - a TWO-PIECE sleeve (an upper sleeve and a narrower under sleeve), which is what gives
    the period sleeve its forward curve at the elbow. A one-piece sleeve hangs straight and
    is the commonest tell of a modern draft;
  - a long sleeve set high and close, often with a small puff or gathering at the head;
  - a front closed with hooks and eyes, which the period prefers to visible buttons on a
    woman's spencer.

Drafting note — the seam that must SOLVE, and it is a SUM this time. On a two-piece sleeve
the cap is split between two separate pieces: the upper sleeve carries most of it and the
under sleeve the rest. Neither piece's cap means anything on its own — what must equal the
armscye plus ease is their SUM:

    upper cap  +  under cap   =   armscye  +  ease

This cartridge measures the armscye off the built body pieces and then solves the cap
HEIGHT by bisection until that sum matches, driving both pieces' caps from the one solved
height (the under sleeve's stays a fixed shallow fraction of the upper's, which is what
lets it sit under the arm). Height is the right variable: the sleeve's width at the biceps
is already fixed by the armscye, so it is how far the cap rises that decides its length.
An earlier revision tried to solve the CURVATURE instead and hit a wall — at zero bulge the
cap was already 318.7 mm against a 256.7 mm target, so no curvature could reach it and the
bisection silently returned its ceiling, leaving a 62 mm mismatch the verifier caught.

The two long sleeve seams must solve too, and initially did not. The upper and under
sleeves are seamed to each other down both sides, so those edges are ONE seam — but the
first revision tapered each piece from its own width to its own wrist share, giving
different insets and a genuine 4.2 mm mismatch per side. Both pieces now share a single
seam profile: the same curve, reversed rather than redrawn for the side of the ring that
runs upward, so the two edges are equal by construction.

Pieces:
  - front       : spencer front (cut 2, mirrored) — hook stand, underbust curve.
  - back        : spencer back (cut 2, mirrored) — CB seam, the period's narrow back.
  - upper_sleeve: the outer, larger sleeve piece, at the SOLVED cap height (cut 2, mirrored).
  - under_sleeve: the inner, narrower sleeve piece (cut 2, mirrored).
  - collar      : small standing collar, half-width SOLVED (cut 1 on fold).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

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
# front|back|upper_sleeve|under_sleeve|collar|set

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
underbust_girth = float(PARAM(lambda: underbust_girth, 760.0))
back_length = float(PARAM(lambda: back_length, 250.0))     # nape to the HIGH waist
shoulder_width = float(PARAM(lambda: shoulder_width, 122.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 580.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 165.0))
under_sleeve_frac = float(PARAM(lambda: under_sleeve_frac, 0.34))  # under sleeve's share
sleeve_ease = float(PARAM(lambda: sleeve_ease, 22.0))      # eased into the cap
collar_height = float(PARAM(lambda: collar_height, 34.0))
hook_pitch = float(PARAM(lambda: hook_pitch, 42.0))        # front hook-and-eye spacing
seam_allowance = float(PARAM(lambda: seam_allowance, 11.0))

# ── Clamps (sane Regency spencer ranges) ─────────────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1400.0))
underbust_girth = max(600.0, min(underbust_girth, 1250.0))
back_length = max(150.0, min(back_length, 380.0))
shoulder_width = max(90.0, min(shoulder_width, 180.0))
sleeve_length = max(420.0, min(sleeve_length, 720.0))
wrist_girth = max(130.0, min(wrist_girth, 300.0))
under_sleeve_frac = max(0.20, min(under_sleeve_frac, 0.45))
sleeve_ease = max(0.0, min(sleeve_ease, 60.0))
collar_height = max(15.0, min(collar_height, 70.0))
hook_pitch = max(20.0, min(hook_pitch, 80.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The underbust must be smaller than the bust, or there is nothing for the seam to shape.
underbust_girth = min(underbust_girth, bust_girth - 30.0)

BL = back_length
# A spencer's armhole is HIGH and small — the period sleeve is set close into the shoulder,
# and a modern low armhole immediately loses the line.
ARMHOLE_DEPTH = BL * 0.62
Y_BUST = BL - ARMHOLE_DEPTH

# The spencer is worn over a gown, so it takes real ease over the bust.
BUST_4 = (bust_girth + 70.0) / 4.0
UNDERBUST_4 = (underbust_girth + 55.0) / 4.0

NECK_W_FRONT = shoulder_width * 0.44
NECK_W_BACK = shoulder_width * 0.50
SHOULDER_SLOPE = 16.0

# Both panels' shoulder edges are sewn to each other, so they must measure the same. The
# reference is chosen so the WIDER-necked panel still has a real solution — its shoulder
# can never be shorter than its own horizontal run — and each drop is solved from it.
_DX_F = shoulder_width - NECK_W_FRONT
_DX_B = shoulder_width - NECK_W_BACK
SHOULDER_LEN = max((_DX_F ** 2 + SHOULDER_SLOPE ** 2) ** 0.5,
                   (_DX_B ** 2 + SHOULDER_SLOPE ** 2) ** 0.5)


def _shoulder_drop_for(neck_w):
    """Solve this panel's shoulder-point drop so its shoulder measures SHOULDER_LEN."""
    dx = shoulder_width - neck_w
    return max(0.0, SHOULDER_LEN ** 2 - dx ** 2) ** 0.5


# Hooks and eyes up the centre front.
N_HOOKS = max(3, int((BL - 26.0) / hook_pitch))


def build_front():
    """Spencer front (cut 2, mirrored). Ends at the HIGH waist, directly under the bust."""
    sh_drop = _shoulder_drop_for(NECK_W_FRONT)
    internals = []
    for i in range(N_HOOKS):
        y = 18.0 + i * hook_pitch
        if y < BL - 22.0:
            internals.append(fc.Internal("front-hook", [fc.P(9.0, y), fc.P(9.0, y + 1.0)],
                                         kind="drill"))
    return fc.Piece(
        "front",
        [
            fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BL - 42.0))]),
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, BL - 42.0),
                                              fc.P(NECK_W_FRONT, BL), 0.16, -1.0)]),
            fc.Edge("shoulder", [fc.Line(fc.P(NECK_W_FRONT, BL),
                                         fc.P(shoulder_width, BL - sh_drop))]),
            fc.Edge("armhole", [fc.curve_through(fc.P(shoulder_width, BL - sh_drop),
                                                 fc.P(BUST_4, Y_BUST), 0.24, -1.0)]),
            fc.Edge("side", [fc.curve_through(fc.P(BUST_4, Y_BUST),
                                              fc.P(UNDERBUST_4, 0.0), 0.09, -1.0)]),
            # The underbust edge: the spencer's defining line. Curved UP toward the centre
            # front, which is what lifts the hem clear of the gown's own waistline.
            fc.Edge("underbust", [fc.curve_through(fc.P(UNDERBUST_4, 0.0), fc.P(0.0, 0.0),
                                                   0.09, -1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cf": 22.0, "underbust": 14.0, "neck": 7.0},
        notches=[fc.Notch("armhole", 0.5, "front armhole balance"),
                 fc.Notch("side", 0.5, "side balance")],
        grainline=fc.Grainline(fc.P(BUST_4 * 0.4, 18.0), fc.P(BUST_4 * 0.4, BL - 18.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2 mirrored, hook stand)",
    )


def build_back():
    """Spencer back (cut 2, mirrored). The period back is NARROW — a wide back is a tell."""
    sh_drop = _shoulder_drop_for(NECK_W_BACK)
    return fc.Piece(
        "back",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BL - 12.0))]),
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, BL - 12.0),
                                              fc.P(NECK_W_BACK, BL), 0.09, -1.0)]),
            fc.Edge("shoulder", [fc.Line(fc.P(NECK_W_BACK, BL),
                                         fc.P(shoulder_width, BL - sh_drop))]),
            fc.Edge("armhole", [fc.curve_through(fc.P(shoulder_width, BL - sh_drop),
                                                 fc.P(BUST_4, Y_BUST), 0.15, -1.0)]),
            fc.Edge("side", [fc.curve_through(fc.P(BUST_4, Y_BUST),
                                              fc.P(UNDERBUST_4, 0.0), 0.09, -1.0)]),
            fc.Edge("underbust", [fc.curve_through(fc.P(UNDERBUST_4, 0.0), fc.P(0.0, 0.0),
                                                   0.05, -1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"underbust": 14.0, "neck": 7.0},
        notches=[fc.Notch("armhole", 0.5, "back armhole balance (double)"),
                 fc.Notch("side", 0.5, "side balance")],
        grainline=fc.Grainline(fc.P(BUST_4 * 0.4, 18.0), fc.P(BUST_4 * 0.4, BL - 18.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (cut 2 mirrored, CB seam)",
    )


FRONT = build_front()
BACK = build_back()

# One armhole = one front armhole + one back armhole; both are cut 2 mirrored, so each
# drafted edge is one whole side of one armhole.
ARMSCYE = FRONT.edge("armhole").length() + BACK.edge("armhole").length()
CAP_TARGET = ARMSCYE + sleeve_ease

# ── The two-piece sleeve ─────────────────────────────────────────────────────
SL = sleeve_length
SLEEVE_TOP_W = ARMSCYE * 0.46          # the sleeve's width at the biceps
UNDER_W = SLEEVE_TOP_W * under_sleeve_frac
UPPER_W = SLEEVE_TOP_W - UNDER_W
WRIST_TOTAL = (wrist_girth + 30.0) / 2.0
UNDER_WRIST = WRIST_TOTAL * under_sleeve_frac
UPPER_WRIST = WRIST_TOTAL - UNDER_WRIST
UNDER_BULGE = 0.16
UPPER_BULGE = 0.20      # a modest, period-plausible cap curvature, held fixed


def _under_cap_segments(cap_h):
    """The under sleeve's cap: a shallow curve at the given height."""
    return [fc.curve_through(fc.P(0.0, 0.0), fc.P(UNDER_W, cap_h), UNDER_BULGE, 1.0),
            fc.curve_through(fc.P(UNDER_W, cap_h), fc.P(UNDER_W * 2.0, 0.0),
                             UNDER_BULGE, 1.0)]


def _upper_cap_segments(cap_h):
    """The upper sleeve's two-lobe cap at the given height."""
    return [fc.curve_through(fc.P(0.0, 0.0), fc.P(UPPER_W, cap_h), UPPER_BULGE * 0.62, 1.0),
            fc.curve_through(fc.P(UPPER_W, cap_h), fc.P(UPPER_W * 2.0, 0.0),
                             UPPER_BULGE, 1.0)]


def _seg_len(segs):
    return sum(fc.polyline_length(s.flatten(0.2)) for s in segs)


# ── Solving the cap ──────────────────────────────────────────────────────────
# The variable that actually governs cap length here is the cap HEIGHT, not the curvature:
# the sleeve's width at the biceps is already fixed by the armscye, so the cap's two lobes
# span a known horizontal run and it is how far they rise that decides their length. An
# earlier revision tried to solve the CURVATURE instead and ran into a wall — at zero bulge
# the cap was already 318.7 mm against a 256.7 mm target, so no curvature could reach it and
# the bisection silently returned its ceiling, leaving a 62 mm mismatch the verifier caught.
#
# So the height is what gets solved, and BOTH pieces are driven from it in proportion: the
# under sleeve's cap stays shallow (a fixed fraction of the upper's) because that is what
# lets it sit under the arm. The seam is checked against the SUM of the two caps.
UNDER_CAP_FRAC = 0.30


def _cap_sum_at(cap_h):
    """Total cap length — upper plus under — at a given upper-cap height."""
    return (_seg_len(_upper_cap_segments(cap_h))
            + _seg_len(_under_cap_segments(cap_h * UNDER_CAP_FRAC)))


def _solve_cap_height(target):
    """Bisect the cap height until upper + under MEASURES armscye + ease.

    Neither piece's cap means anything on its own; their SUM is what sets into the armscye,
    so the sum is what is solved and what the declared seam checks. Computing both from
    formulas and hoping the total lands is what leaves a two-piece sleeve that will not
    set in.

    The bracket is checked at both ends rather than assumed: if even a flat cap overshoots
    the target, the solver says so through the reported residual instead of quietly
    returning a bound.
    """
    lo, hi = 0.0, ARMHOLE_DEPTH * 2.5
    if _cap_sum_at(hi) < target:
        return hi, _cap_sum_at(hi)
    if _cap_sum_at(lo) > target:
        return lo, _cap_sum_at(lo)
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if _cap_sum_at(mid) < target:
            lo = mid
        else:
            hi = mid
    h = (lo + hi) / 2.0
    return h, _cap_sum_at(h)


CAP_H, CAP_SUM = _solve_cap_height(CAP_TARGET)
UNDER_CAP_H = CAP_H * UNDER_CAP_FRAC
UNDER_CAP_MEASURED = _seg_len(_under_cap_segments(UNDER_CAP_H))
UPPER_CAP_MEASURED = _seg_len(_upper_cap_segments(CAP_H))
CAP_RESIDUAL = CAP_SUM - CAP_TARGET


# ── The sleeve's long seams ──────────────────────────────────────────────────
# The upper and under sleeves are seamed to each other down BOTH sides, so those edges are
# one seam and must be the same length. An earlier revision drafted each piece's seam from
# its own width down to its own wrist share — different insets, so genuinely different
# lengths, and the verifier caught a 4.2 mm mismatch on each side.
#
# The fix is to give both pieces the SAME seam profile: one shared taper, applied to each
# piece from its own starting width. The pieces still differ in width (that is what makes
# one the upper and one the under); what they now share is the seam that joins them.
SEAM_INSET = (SLEEVE_TOP_W - WRIST_TOTAL) / 2.0
SEAM_BULGE = 0.045


def _sleeve_seam_down(x_top, x_bottom):
    """One long sleeve seam drawn DOWNWARD, biceps line to wrist.

    The curve bows forward — the forward curve at the elbow is what a two-piece sleeve is
    FOR, and it is what a one-piece sleeve cannot do.
    """
    return [fc.curve_through(fc.P(x_top, 0.0), fc.P(x_bottom, -SL), SEAM_BULGE, 1.0)]


def _sleeve_seam_up(x_bottom, x_top):
    """The same seam drawn UPWARD, wrist to biceps line.

    A piece's outline must be continuous, so the two long seams are traversed in opposite
    directions round the ring. Reversing the identical curve — rather than drawing a
    second one — is what keeps both sides of the sleeve the same length by construction.
    """
    return [fc.curve_through(fc.P(x_top, 0.0), fc.P(x_bottom, -SL),
                             SEAM_BULGE, 1.0).reversed()]


def build_upper_sleeve():
    """The outer, larger sleeve piece, drafted at the SOLVED cap height (cut 2, mirrored)."""
    w = UPPER_W * 2.0
    inset = SEAM_INSET
    return fc.Piece(
        "upper_sleeve",
        [
            fc.Edge("back_seam", _sleeve_seam_down(w, w - inset)),
            fc.Edge("wrist", [fc.Line(fc.P(w - inset, -SL), fc.P(inset, -SL))]),
            fc.Edge("front_seam", _sleeve_seam_up(inset, 0.0)),
            fc.Edge("cap", _upper_cap_segments(CAP_H)),
        ],
        seam_allowance=seam_allowance,
        allowances={"wrist": 8.0},
        notches=[fc.Notch("cap", 0.25, "front cap notch"),
                 fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.75, "back cap notch (double)"),
                 fc.Notch("back_seam", 0.55, "elbow")],
        grainline=fc.Grainline(fc.P(w * 0.5, -26.0), fc.P(w * 0.5, -SL + 26.0)),
        internals=[fc.Internal("elbow-line", [fc.P(inset * 0.5, -SL * 0.55),
                                              fc.P(w - inset * 0.5, -SL * 0.55)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Upper sleeve (cut 2 mirrored, cap bulge SOLVED)",
    )


def build_under_sleeve():
    """The inner, narrower sleeve piece (cut 2, mirrored). Its shallow cap sits under the arm."""
    w = UNDER_W * 2.0
    inset = SEAM_INSET
    return fc.Piece(
        "under_sleeve",
        [
            fc.Edge("back_seam", _sleeve_seam_down(w, w - inset)),
            fc.Edge("wrist", [fc.Line(fc.P(w - inset, -SL), fc.P(inset, -SL))]),
            fc.Edge("front_seam", _sleeve_seam_up(inset, 0.0)),
            fc.Edge("cap", _under_cap_segments(UNDER_CAP_H)),
        ],
        seam_allowance=seam_allowance,
        allowances={"wrist": 8.0},
        notches=[fc.Notch("cap", 0.5, "underarm point"),
                 fc.Notch("back_seam", 0.55, "elbow")],
        grainline=fc.Grainline(fc.P(w * 0.5, -26.0), fc.P(w * 0.5, -SL + 26.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Under sleeve (cut 2 mirrored)",
    )


# The neck run the collar is cut to: MEASURED off the built necklines.
NECK_RUN = FRONT.edge("neck").length() * 2.0 + BACK.edge("neck").length() * 2.0
COLLAR_BULGE = 0.04


def _collar_edge_length(half_w):
    """MEASURED length of the collar's curved neck edge at a given half-width."""
    c = fc.curve_through(fc.P(half_w, 0.0), fc.P(0.0, 0.0), COLLAR_BULGE, -1.0)
    return fc.polyline_length(c.flatten(0.2))


def _solve_collar_half(target):
    """Bisect the collar's half-width so its CURVED neck edge measures `target`.

    A curve is longer than the chord it spans, so setting the half-width to half the neck
    run makes the collar overshoot the neckline it is sewn to. Solving it is the fix.
    """
    lo, hi = 1.0, target * 1.5
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if _collar_edge_length(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


COLLAR_HALF = _solve_collar_half(NECK_RUN / 2.0)


def build_collar():
    """Small standing collar, SOLVED against the measured neck run (cut 1 on fold)."""
    half, h = COLLAR_HALF, collar_height
    return fc.Piece(
        "collar",
        [
            fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("upper", [fc.curve_through(fc.P(0.0, h), fc.P(half, h),
                                               COLLAR_BULGE, -1.0)]),
            fc.Edge("front_end", [fc.Line(fc.P(half, h), fc.P(half, 0.0))]),
            fc.Edge("neck_seam", [fc.curve_through(fc.P(half, 0.0), fc.P(0.0, 0.0),
                                                   COLLAR_BULGE, -1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_seam", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(half * 0.2, h * 0.5), fc.P(half * 0.8, h * 0.5)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Standing collar (cut 1 on fold, SOLVED to the measured neck run)",
    )


def build():
    pattern = fc.PatternSet("regency-spencer")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(FRONT)
    if everything or target_piece == "back":
        pattern.add(BACK)
    if everything or target_piece == "upper_sleeve":
        pattern.add(build_upper_sleeve())
    if everything or target_piece == "under_sleeve":
        pattern.add(build_under_sleeve())
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        # THE seam. Neither sleeve piece's cap means anything alone — their SUM is what
        # sets into the armscye, so the check is declared against the sum.
        pattern.declare_seam(
            [("upper_sleeve", "cap"), ("under_sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=1.0, ease=sleeve_ease)
        # The two sleeve pieces are seamed to each other down both sides.
        pattern.declare_seam(("upper_sleeve", "front_seam"),
                             ("under_sleeve", "front_seam"), tol=1.5)
        pattern.declare_seam(("upper_sleeve", "back_seam"),
                             ("under_sleeve", "back_seam"), tol=1.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # The collar takes the whole measured neck run; cut on the fold, so counted twice.
        pattern.declare_seam(
            [("collar", "neck_seam"), ("collar", "neck_seam")],
            [("front", "neck"), ("front", "neck"), ("back", "neck"), ("back", "neck")],
            tol=1.5)

    fabric_width = 1200.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "fine wool, silk, or velvet",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1200 mm width, 74% marker. A spencer is a SMALL garment and takes "
                 "little cloth — which is exactly why it was often made from a good remnant "
                 "or cut down from a worn-out gown."},
        {"item": "hooks and eyes (Yantra4D trouser-hook-bar)", "qty": N_HOOKS, "unit": "count",
         "note": f"{N_HOOKS} up the centre front at {hook_pitch:.0f} mm pitch. The period "
                 f"prefers hooks and eyes to visible buttons on a woman's spencer."},
        {"item": "lining (silk or fine cotton)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a spencer is fully lined — it is a tailored garment, and the lining is "
                 "what makes the small seamed shaping hold."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "the two-piece sleeve's curved seams want careful, short stitching."},
    ]
    pattern.metadata = {
        "fc300_rank": 276,
        "family": "costume_historical",
        "period": "c. 1800–1825 (Regency / Empire)",
        "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "The hem sits at the HIGH waist, directly under the bust, so the "
            "gown's Empire waistline continues uninterrupted underneath. A spencer cut to the "
            "natural waist is not a spencer — it is a short jacket, and it fights the line of "
            "the gown it is worn over instead of completing it.",
        "construction_note": "Shaping taken at the side and back seams and by the curve of "
            "the underbust edge, never by a modern bust dart. Two-piece sleeve for the "
            "period's forward elbow curve. Front closed with hooks and eyes.",
        "hardware": "front hooks via Yantra4D (notion.hardware_ref -> trouser-hook-bar); the "
            "hook pitch drives plate_len — the dimensional handshake.",
        "solved": {
            "armscye_measured_mm": round(ARMSCYE, 2),
            "sleeve_ease_mm": round(sleeve_ease, 1),
            "cap_target_mm": round(CAP_TARGET, 2),
            "under_cap_measured_mm": round(UNDER_CAP_MEASURED, 2),
            "upper_cap_measured_mm": round(UPPER_CAP_MEASURED, 2),
            "cap_sum_mm": round(CAP_SUM, 2),
            "cap_residual_mm": round(CAP_RESIDUAL, 4),
            "cap_height_solved_mm": round(CAP_H, 3),
            "under_cap_height_mm": round(UNDER_CAP_H, 3),
            "neck_run_measured_mm": round(NECK_RUN, 2),
            "collar_half_width_solved_mm": round(COLLAR_HALF, 2),
            "collar_edge_residual_mm": round(
                _collar_edge_length(COLLAR_HALF) * 2.0 - NECK_RUN, 4),
            "shoulder_seam_mm": round(SHOULDER_LEN, 2),
            "note": "on a two-piece sleeve neither cap means anything on its own — their SUM "
                    "is what sets into the armscye. The under sleeve's shallow cap is built "
                    "first and MEASURED, the upper sleeve's bulge is then solved by bisection "
                    "against what remains, and the seam is declared against the SUM of the "
                    "two. The collar's curved neck edge is likewise solved, because a curve "
                    "is longer than the chord it spans and a collar cut to half the neck run "
                    "overshoots the neckline it is sewn to.",
        },
    }
    return pattern


result = build()

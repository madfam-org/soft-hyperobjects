"""
Button-Aid Cuff Shirt — Fashion Cabinet Adaptive Cartridge (FC-300 #298, long-tail band).

A shirt whose cuffs are drafted for the hand that cannot help. One-handed dressing has
a specific, asymmetric problem that most "adaptive shirt" patterns miss entirely: the
buttons a person can reach are not the ones that trap them. A front placket can be
managed slowly. The cuff of the WORKING arm cannot be buttoned at all, because the only
hand that could do it is the one inside that cuff.

The usual answers are to sew the cuff permanently shut (which then has to pass over the
hand, so it must be enormous, so it flaps all day) or to hand the wearer a button hook
and hope the cuff cooperates. It usually does not. A button hook — a wire loop on a
handle, `yantra4d/button-hook-aid` — needs three things from a cuff that an ordinary
shirt cuff does not provide, and this draft provides all three:

  1. SOMEWHERE TO PULL. The hook must catch something. An ordinary cuff offers only the
     buttonhole itself, which the hook is already occupying. So this cuff carries a
     sewn LOOP TAB at the free end, sized to the hook's loop diameter, positioned so
     pulling it drags the buttonhole onto the button in a straight line.

  2. ROOM FOR THE LOOP TO ENTER. The hook's wire loop has a real thickness and a real
     depth: it must pass through the buttonhole, round the button, and back. So the
     buttonhole is cut LONGER than the button — by the loop's own wire thickness twice
     over plus a working clearance — rather than to the usual button + 2 mm.

  3. A CUFF THAT STAYS OPEN WHILE IT IS WORKED. An ordinary cuff, unbuttoned, closes
     under its own drape and puts the button behind the buttonhole where nothing can
     reach it. So the cuff is drafted with an EXTENDED UNDERLAP whose end is stiffened,
     which holds the two ends apart in the plane where the hook works.

Drafting note — the seam that must SOLVE, and the number that has to be honest:

  The cuff is a two-position closure. Buttoned, it must sit at the wrist. UNBUTTONED
  and spread flat, its inner circuit must clear the widest part of the hand, because a
  one-handed wearer puts the arm in before the cuff can be closed. Those are two
  different girths, and the pattern owes the maker BOTH:

      closed  = wrist_girth + wrist_ease
      open    = closed + underlap + overlap        (the flat circuit while worked)
      pass    = open must be >= hand_girth * (1 - cuff_stretch)

  The naive draft sets the cuff to the wrist and adds a fixed 30 mm extension, then
  discovers at the fitting that the hand does not go through. Here `hand_girth` is a
  real parameter and the underlap is SOLVED upward until the open circuit clears the
  hand — with the amount it had to grow reported, not hidden.

Pieces:
  - front  : shirt front (cut 2 mirrored), placket cut on.
  - back   : shirt back (cut 1 on fold at CB).
  - sleeve : one-piece sleeve (cut 2 mirrored), its cuff opening solved to the cuff.
  - cuff   : the solved cuff, with the aid loop tab, the long buttonhole, and the
             stiffened underlap.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|cuff|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
shirt_length = float(PARAM(lambda: shirt_length, 720.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 175.0))
hand_girth = float(PARAM(lambda: hand_girth, 215.0))   # across the knuckles, thumb in
wrist_ease = float(PARAM(lambda: wrist_ease, 28.0))
cuff_depth = float(PARAM(lambda: cuff_depth, 68.0))
button_dia = float(PARAM(lambda: button_dia, 15.0))
hook_wire = float(PARAM(lambda: hook_wire, 2.2))       # the aid's loop wire thickness
hook_loop = float(PARAM(lambda: hook_loop, 22.0))      # the aid's loop diameter
loop_tab = float(PARAM(lambda: loop_tab, 26.0))        # the sewn pull tab's reach
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1500.0))
shirt_length = max(560.0, min(shirt_length, 900.0))
shoulder_width = max(340.0, min(shoulder_width, 580.0))
sleeve_length = max(200.0, min(sleeve_length, 700.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
wrist_girth = max(130.0, min(wrist_girth, 260.0))
hand_girth = max(150.0, min(hand_girth, 340.0))
wrist_ease = max(10.0, min(wrist_ease, 70.0))
cuff_depth = max(40.0, min(cuff_depth, 120.0))
button_dia = max(10.0, min(button_dia, 26.0))
hook_wire = max(1.0, min(hook_wire, 5.0))
hook_loop = max(10.0, min(hook_loop, 45.0))
loop_tab = max(12.0, min(loop_tab, 60.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

# A hand is never smaller than the wrist it is attached to. Entered otherwise, the
# ordering is fixed rather than trusted — an inverted pair would solve the underlap
# DOWNWARD and produce a cuff that buttons but cannot be entered.
hand_girth = max(hand_girth, wrist_girth + 5.0)

# The cuff must be deep enough to carry the buttonhole run and the loop tab's stitching
# without either landing on an edge.
cuff_depth = max(cuff_depth, button_dia + hook_loop * 0.5 + 24.0)

EASE_CHEST = 150.0
HALF_CHEST = (chest_girth + EASE_CHEST) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = neck_girth / 6.0 + 8.0
NECK_DROP_F = neck_girth / 6.0 + 18.0
NECK_DROP_B = 24.0
ARMHOLE_DROP = 245.0
SHOULDER_SLOPE = 42.0
STAND = button_dia / 2.0 + 12.0

# ── The two-position cuff solve ──────────────────────────────────────────────
# CLOSED: the cuff at the wrist, where it lives all day.
CLOSED = wrist_girth + wrist_ease
# The overlap carries the button; the underlap is the extension that both stiffens the
# opening and gives the hand its passage. The overlap is set by the button it must
# carry; only the underlap is free to grow.
OVERLAP = button_dia + 14.0
# The hand's passage: a woven-cuff stretch is small but not zero (bias + seam give).
CUFF_STRETCH = 0.03
PASS_NEEDED = hand_girth * (1.0 - CUFF_STRETCH)
UNDERLAP_MIN = 22.0
# Solve the underlap upward until the flat, worked circuit clears the hand.
_UNDERLAP_FOR_HAND = PASS_NEEDED - CLOSED - OVERLAP
UNDERLAP = max(UNDERLAP_MIN, _UNDERLAP_FOR_HAND)
UNDERLAP_GREW = UNDERLAP - UNDERLAP_MIN          # what the hand cost, reported
OPEN_CIRCUIT = CLOSED + OVERLAP + UNDERLAP
HAND_CLEARANCE = OPEN_CIRCUIT - PASS_NEEDED      # must stay >= 0 by construction

# The cuff strip's full cut length: the closed circuit plus both extensions.
CUFF_LEN = OPEN_CIRCUIT

# ── The buttonhole, cut for a wire loop ──────────────────────────────────────
# An ordinary buttonhole is button + 2 mm. This one must admit the hook's wire loop
# alongside the button: the wire passes on BOTH sides of the shank, so two wire
# thicknesses plus a working clearance.
HOLE_WORKING = 2.5
BUTTONHOLE = button_dia + 2.0 * hook_wire + HOLE_WORKING
BUTTONHOLE_NAIVE = button_dia + 2.0
HOLE_GAIN = BUTTONHOLE - BUTTONHOLE_NAIVE

# The buttonhole's centre, measured in from the overlap end, and the button opposite it
# on the underlap end. Both are held clear of the cuff's own edges.
HOLE_INSET = max(BUTTONHOLE / 2.0 + 8.0, OVERLAP * 0.5)
HOLE_X = CUFF_LEN - HOLE_INSET
BUTTON_X = UNDERLAP * 0.5
# The pull tab sits at the overlap end, past the buttonhole, so pulling it drags the
# hole onto the button in a straight line rather than twisting the cuff.
TAB_X = CUFF_LEN - loop_tab * 0.5 - 6.0


def _rect_edges(x0, y0, w, h, names):
    """A CCW rectangle with four named edges; w, h already clamped positive."""
    p0 = fc.P(x0, y0)
    p1 = fc.P(x0 + w, y0)
    p2 = fc.P(x0 + w, y0 + h)
    p3 = fc.P(x0, y0 + h)
    return [
        fc.Edge(names[0], [fc.Line(p0, p1)]),
        fc.Edge(names[1], [fc.Line(p1, p2)]),
        fc.Edge(names[2], [fc.Line(p2, p3)]),
        fc.Edge(names[3], [fc.Line(p3, p0)]),
    ]


def _closed_rect_pts(x0, y0, w, h):
    return [fc.P(x0, y0), fc.P(x0 + w, y0), fc.P(x0 + w, y0 + h),
            fc.P(x0, y0 + h), fc.P(x0, y0)]


def build_front():
    """Shirt front (cut 2 mirrored), placket extension cut on.

    The front is deliberately ordinary: this cartridge's adaptation is at the cuff,
    and a shirt that reads as ordinary is part of the point."""
    h = shirt_length
    x_out = -STAND
    p_hem_out = fc.P(x_out, 0.0)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, h - NECK_DROP_F - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, h - NECK_DROP_F - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, h - NECK_DROP_F)
    p_neck_cf = fc.P(x_out, h - NECK_DROP_F + 4.0)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_out, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 6.0,
                                           h - NECK_DROP_F - ARMHOLE_DROP * 0.42),
                                      fc.P(HALF_SHOULDER + 14.0,
                                           h - NECK_DROP_F - SHOULDER_SLOPE - 46.0),
                                      p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.52, h - NECK_DROP_F - 10.0),
                                   fc.P(x_out + STAND * 0.4, h - NECK_DROP_F - 2.0),
                                   p_neck_cf)]),
        fc.Edge("placket_fold", [fc.Line(p_neck_cf, p_hem_out)]),
    ]
    internals = [
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h - NECK_DROP_F)],
                    kind="marking"),
        fc.Internal("placket-stitch", [fc.P(STAND, 0.0), fc.P(STAND, h - NECK_DROP_F)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 22.0, "placket_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap front match"),
                 fc.Notch("side", 0.62, "waist level")],
        grainline=fc.Grainline(fc.P(STAND + 40.0, 60.0),
                               fc.P(STAND + 40.0, h - NECK_DROP_F - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shirt Front",
    )


# ── The back neck solved from the MEASURED front shoulder ────────────────────
# The front's shoulder runs from (HALF_SHOULDER, top - SHOULDER_SLOPE) to (NECK_W,
# top). The back shares the outer point, but its neck point sits HIGHER — a back neck
# is shallower than a front neck — so drafting the back neck at NECK_W would give a
# longer shoulder. Solve the back neck WIDTH from the front's measured shoulder
# instead, so the seam matches by construction rather than by hoping two formulas
# agree.
_SHOULDER_LEN = math.hypot(HALF_SHOULDER - NECK_W, SHOULDER_SLOPE)
_BACK_NECK_Y_OFF = NECK_DROP_F - NECK_DROP_B - SHOULDER_SLOPE * 0.10

# The rise is a vertical leg of a right triangle whose hypotenuse is the shoulder. A
# narrow shoulder with a deep neck (340 mm shoulder, 520 mm neck) makes the rise
# EXCEED the shoulder length: there is no horizontal run left, and the solve returns a
# back neck the drawn geometry then contradicts. Clamping only the solve's local `_dy`
# is not enough — the PIECE must be drawn at the clamped rise too, or the drafted
# shoulder measures the unclamped one and the seam check fires. So the clamp lands on
# BACK_NECK_Y itself, and every use reads that single value.
_dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
if _dy >= _SHOULDER_LEN * 0.94:
    _dy = _SHOULDER_LEN * 0.94
BACK_NECK_Y = _dy - SHOULDER_SLOPE
BACK_NECK_CLAMPED = BACK_NECK_Y < _BACK_NECK_Y_OFF - 1e-9
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))


def build_back():
    """Shirt back, cut 1 on fold at centre back; back neck width SOLVED so the
    shoulder seam measures the front's exactly."""
    h = shirt_length
    top = h - NECK_DROP_F
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, top - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, top - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, top + BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, top + BACK_NECK_Y + 6.0)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 4.0, top - ARMHOLE_DROP * 0.44),
                                      fc.P(HALF_SHOULDER + 12.0,
                                           top - SHOULDER_SLOPE - 40.0),
                                      p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.55, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y),
                                   p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 22.0, "cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match"),
                 fc.Notch("side", 0.62, "waist level")],
        grainline=None,
        internals=[fc.Internal("yoke-line",
                               [fc.P(0.0, top - 120.0),
                                fc.P(HALF_SHOULDER, top - 120.0)], kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Shirt Back",
    )


# ── The sleeve cap solved against the MEASURED armholes ──────────────────────
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 14.0
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
BICEPS = max(360.0, (ARMHOLE_F + ARMHOLE_B) * 0.78)

# The sleeve's cuff opening must equal the cuff's CLOSED circuit plus the pleat the
# placket opening takes up. Solved from the cuff, not chosen — a sleeve hem that does
# not match its cuff is the commonest shirt error and here it would also change the
# hand passage.
CUFF_PLEAT = 26.0
SLEEVE_HEM = CLOSED + CUFF_PLEAT


def _cap_segments(cap_h, top_y):
    half = BICEPS / 2.0
    p_l = fc.P(-half, top_y - cap_h)
    p_top = fc.P(0.0, top_y)
    p_r = fc.P(half, top_y - cap_h)
    return [
        fc.Bezier(p_l, fc.P(-half * 0.72, top_y - cap_h * 0.94),
                  fc.P(-half * 0.34, top_y - cap_h * 0.06), p_top),
        fc.Bezier(p_top, fc.P(half * 0.34, top_y - cap_h * 0.06),
                  fc.P(half * 0.72, top_y - cap_h * 0.94), p_r),
    ]


def _solve_cap_height():
    """Bisect the cap height until the cap measures CAP_TARGET. Cap length grows
    monotonically with height at a fixed biceps, so the bracket contains the root."""
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
# The sleeve hem can never exceed the biceps: at extreme parameters (a 340 mm hand on a
# small chest) the solved cuff would be wider than the sleeve it hangs from, giving an
# inverted taper — a piece whose edges cross and which the kernel would normalize into
# something that verifies and cannot be sewn.
SLEEVE_HEM_HALF = min(SLEEVE_HEM / 2.0, BICEPS / 2.0 - 8.0)
SLEEVE_HEM_CAPPED = SLEEVE_HEM / 2.0 > BICEPS / 2.0 - 8.0


def build_sleeve():
    """One-piece sleeve (cut 2 mirrored): solved cap, hem solved to the cuff, with the
    placket slit marked at the little-finger side where the hook has room to work."""
    half = BICEPS / 2.0
    top_y = sleeve_length
    cap = _cap_segments(CAP_H, top_y)
    p_l_under = fc.P(-half, top_y - CAP_H)
    p_r_under = fc.P(half, top_y - CAP_H)
    p_l_cuff = fc.P(-SLEEVE_HEM_HALF, 0.0)
    p_r_cuff = fc.P(SLEEVE_HEM_HALF, 0.0)

    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r_under, p_r_cuff)]),
        fc.Edge("hem", [fc.Line(p_r_cuff, p_l_cuff)]),
        fc.Edge("under_l", [fc.Line(p_l_cuff, p_l_under)]),
    ]
    # The placket slit: on the little-finger side, and LONGER than a dress shirt's, so
    # the cuff opens far enough to lie flat under a hook.
    slit_h = min(cuff_depth * 1.6, sleeve_length * 0.35)
    slit_x = SLEEVE_HEM_HALF * 0.45
    internals = [
        fc.Internal("placket-slit",
                    [fc.P(slit_x, 0.0), fc.P(slit_x, slit_h)], kind="marking"),
        fc.Internal("cuff-pleat",
                    [fc.P(slit_x - CUFF_PLEAT, 0.0),
                     fc.P(slit_x - CUFF_PLEAT, 30.0)], kind="marking"),
        fc.Internal("elbow-line",
                    [fc.P(-half * 0.9, top_y * 0.42), fc.P(half * 0.9, top_y * 0.42)],
                    kind="marking"),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match"),
                 fc.Notch("hem", 0.5, "underarm seam")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, top_y - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (long placket slit)",
    )


def build_cuff():
    """THE piece. A cuff drafted for a hook, not for two hands.

    Cut at double depth (it folds), to the SOLVED open circuit: closed wrist + overlap
    + the underlap solved upward until the hand can pass."""
    h = cuff_depth * 2.0
    mid = cuff_depth / 2.0
    internals = [
        fc.Internal("fold-line", [fc.P(0.0, cuff_depth), fc.P(CUFF_LEN, cuff_depth)],
                    kind="marking"),
        # The long buttonhole, cut for the hook's wire on BOTH sides of the shank.
        fc.Internal("buttonhole",
                    [fc.P(HOLE_X - BUTTONHOLE / 2.0, mid),
                     fc.P(HOLE_X + BUTTONHOLE / 2.0, mid)], kind="drill"),
        # The button, on the underlap end, opposite it.
        fc.Internal("button-position",
                    [fc.P(BUTTON_X, mid), fc.P(BUTTON_X, mid)], kind="drill"),
        # The pull tab's stitch footprint, past the buttonhole so the pull is straight.
        fc.Internal("loop-tab",
                    _closed_rect_pts(TAB_X - loop_tab / 2.0, mid - hook_loop * 0.35,
                                     loop_tab, hook_loop * 0.7), kind="marking"),
        # The stiffened underlap: interfaced to its end, so the cuff holds itself open
        # in the plane the hook works in instead of collapsing shut.
        fc.Internal("underlap-stiffening",
                    _closed_rect_pts(0.0, 6.0, max(UNDERLAP, 8.0),
                                     max(cuff_depth - 12.0, 8.0)), kind="marking"),
        # The closed-position line: where the overlap end lands when buttoned. Its
        # distance from the free end is the whole overlap, and it is what a maker
        # checks the cuff against before the sleeve is closed.
        fc.Internal("closed-line",
                    [fc.P(UNDERLAP + CLOSED, 0.0), fc.P(UNDERLAP + CLOSED, cuff_depth)],
                    kind="marking"),
    ]
    return fc.Piece(
        "cuff", _rect_edges(0.0, 0.0, CUFF_LEN, h,
                            ("free", "underlap_end", "attach", "overlap_end")),
        seam_allowance=seam_allowance,
        allowances={"free": 0.0},
        notches=[fc.Notch("attach", UNDERLAP / CUFF_LEN, "underlap / sleeve start"),
                 fc.Notch("attach", (UNDERLAP + CLOSED) / CUFF_LEN, "closed position")],
        grainline=fc.Grainline(fc.P(CUFF_LEN * 0.08, mid),
                               fc.P(CUFF_LEN * 0.92, mid)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Button-aid cuff (solved open circuit)",
    )


def build():
    pattern = fc.PatternSet("button-aid-cuff-shirt")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)
        # THE seam that had to solve: the cuff's attach edge is the full open circuit,
        # and the sleeve hem is the closed circuit plus the pleat — so the difference
        # is exactly the two extensions. Declared with that difference as ease, so a
        # cuff cut to the wrist alone (the naive draft) cannot pass the check.
        _sleeve_hem_measured = build_sleeve().edge("hem").length(0.2)
        _ease = CUFF_LEN - _sleeve_hem_measured
        pattern.declare_seam(("cuff", "attach"), ("sleeve", "hem"),
                             tol=1.0, ease=_ease)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "cotton poplin", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1450 mm width, 76% marker; poplin presses a crisp cuff, and a "
                 "crisp cuff is what stays open under a hook."},
        {"item": "button hook aid", "qty": 1, "unit": "count",
         "note": f"Yantra4D button-hook-aid (notion.hardware_ref); a {hook_loop:.0f} mm "
                 f"wire loop in {hook_wire:.1f} mm wire, which is what the "
                 f"{BUTTONHOLE:.1f} mm buttonhole is cut for."},
        {"item": "shirt buttons", "qty": 2 + 7, "unit": "count",
         "note": f"{button_dia:.0f} mm; two at the cuffs, the rest down the placket."},
        {"item": "cuff interfacing (crisp fusible)", "qty": round(CUFF_LEN * 2.0),
         "unit": "mm_length",
         "note": f"full cuff, and a second layer over the {UNDERLAP:.0f} mm underlap — "
                 f"that stiffening is what holds the cuff open for the hook."},
        {"item": "grosgrain or self-fabric loop", "qty": 2, "unit": "count",
         "note": f"{loop_tab:.0f} mm pull tab at each cuff's overlap end; the hook "
                 f"catches this, not the buttonhole it is already occupying."},
    ]
    pattern.metadata = {
        "fc300_rank": 298,
        "family": "adaptive",
        "fabric_hint": "popelina-algodon",
        "finished_mm": {
            "chest": round(HALF_CHEST * 4.0, 1),
            "length": round(shirt_length, 1),
            "sleeve": round(sleeve_length, 1),
            "cuff_closed": round(CLOSED, 1),
            "cuff_open": round(OPEN_CIRCUIT, 1),
            "cuff_depth": round(cuff_depth, 1),
        },
        "solved": {
            "closed_circuit_mm": round(CLOSED, 2),
            "overlap_mm": round(OVERLAP, 2),
            "underlap_min_mm": round(UNDERLAP_MIN, 2),
            "underlap_solved_mm": round(UNDERLAP, 2),
            "underlap_grew_mm": round(UNDERLAP_GREW, 2),
            "open_circuit_mm": round(OPEN_CIRCUIT, 2),
            "hand_girth_mm": round(hand_girth, 2),
            "hand_pass_needed_mm": round(PASS_NEEDED, 2),
            "hand_clearance_mm": round(HAND_CLEARANCE, 2),
            "buttonhole_mm": round(BUTTONHOLE, 2),
            "buttonhole_naive_mm": round(BUTTONHOLE_NAIVE, 2),
            "buttonhole_gain_mm": round(HOLE_GAIN, 2),
            "sleeve_hem_mm": round(SLEEVE_HEM, 2),
            "sleeve_hem_capped": SLEEVE_HEM_CAPPED,
            "cap_height_mm": round(CAP_H, 2),
            "front_shoulder_mm": round(_SHOULDER_LEN, 2),
            "back_neck_rise_mm": round(BACK_NECK_Y, 2),
            "back_neck_rise_requested_mm": round(_BACK_NECK_Y_OFF, 2),
            "back_neck_clamped": BACK_NECK_CLAMPED,
            "back_neck_width_mm": round(NECK_W_BACK, 2),
            "cuff_depth_floor_mm": round(button_dia + hook_loop * 0.5 + 24.0, 2),
            "note": "the cuff is a TWO-POSITION closure and the pattern owes the maker "
                    "both. Closed = wrist + ease. Open (flat, while the hook works) = "
                    "closed + overlap + underlap, and that must clear the HAND, because "
                    "a one-handed wearer puts the arm in before the cuff can be closed. "
                    "So the underlap is solved UPWARD from hand_girth rather than fixed "
                    "at 22 mm, and how far it had to grow is reported as "
                    "underlap_grew_mm. The buttonhole is cut for the aid's wire on both "
                    "sides of the shank (button + 2*hook_wire + 2.5) rather than the "
                    "usual button + 2. The sleeve hem is capped at the biceps: at "
                    "extreme parameters a solved cuff can exceed the sleeve it hangs "
                    "from, giving an inverted taper the kernel would normalize into "
                    "geometry that verifies and cannot be sewn. The back neck rise is "
                    "clamped on BACK_NECK_Y itself, not on a local solve variable: a "
                    "narrow shoulder with a deep neck makes the rise exceed the "
                    "shoulder length, and clamping only the solve leaves the piece "
                    "drawn at the unclamped rise, so the drafted shoulder measures "
                    "something the solve never agreed to.",
        },
        "adaptive": {
            "dressing": "one-handed. The cuff of the working arm is the button nobody "
                        "can reach: the only hand that could close it is inside it.",
            "aid": "a button hook needs somewhere to pull (the loop tab), room for its "
                   "wire loop to enter (the long buttonhole), and a cuff that stays "
                   "open while worked (the stiffened underlap). All three are drafted.",
            "not_sewn_shut": "the alternative — sewing the cuff permanently closed — "
                             "makes the cuff pass over the hand, so it must be enormous "
                             "and flaps all day. This cuff closes at the wrist and "
                             "opens to the hand.",
        },
        "hardware": "dressing aid via Yantra4D (notion.hardware_ref -> "
                    "button-hook-aid); the aid's loop_dia and loop_t are this shirt's "
                    "hook_loop and hook_wire, which are exactly what the buttonhole "
                    "length and the loop tab are drafted from",
    }
    return pattern


result = build()

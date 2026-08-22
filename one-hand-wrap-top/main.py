"""
One-Hand Wrap Top — Fashion Cabinet Garment Cartridge (FC-300 #248, adaptive II).

A wrap top that a person with one working hand can put on, close, and take off
without help, without teeth, and without pinning anything against their body.

An ordinary wrap top defeats one hand twice. First, both wrap edges must be held
at once while a tie is knotted — two hands, or a chin. Second, the classic inner
tie exits through a hole in the side seam and must be found blind behind the
body. This top removes both. The UNDER front's tie is short and terminates in a
sewn-in D-ring; the OVER front's tie is long and is simply threaded through that
ring and pulled back on itself, so a single hand does the whole closure in one
straight motion and the ring holds the tension while the hand lets go. The ring
SOLID is Yantra4D territory (`d-ring`; see the manifest's notion.hardware_ref) —
its bar takes this top's own `tie_width`, so the tie is not "a strap that
probably fits" but the same dimension on both sides of the bridge.

The drafting problem that actually has to be solved:

  1. UNEQUAL WRAP RUNS. The two fronts are NOT mirror images. The under front
     wraps only as far as the opposite side seam; the over front must travel
     across the body, past that side seam, and around to the back tie slot.
     Both wrap edges are drafted as real curves, MEASURED, and the two tie
     lengths are then solved from those measured runs plus the body girth they
     must still cross — never from a rise-plus-girth formula.

  2. RING REGISTER. The ring sits where the over front's wrap edge crosses the
     under front's tie. Both anchors are placed at ONE common height above the
     hem, measured on each piece's own wrap edge, so the closed top pulls level
     instead of cocking one shoulder down.

  3. BACK SHOULDER. The back neck is shallower than the front neck, so drafting
     both at the same neck width leaves the back shoulder seam longer than the
     front's. The back neck WIDTH is solved from the front's MEASURED shoulder
     length by Pythagoras against the vertical offset between the two neck
     points, so the two shoulder seams are equal by construction.

Pieces:
  - under_front : the front that wraps first (cut 1), short tie, ring anchor.
  - over_front  : the front that wraps over (cut 1), long tie, crosses the body.
  - back        : cut 1 on fold at centre back.
  - sleeve      : short kimono-ish set-in sleeve (cut 2 mirrored), solved cap.
  - tie         : the two ties as one strip pattern (cut 2, different lengths
                  marked on it), so a maker cuts both from one shape.

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
# under_front|over_front|back|sleeve|tie|set

bust_girth = float(PARAM(lambda: bust_girth, 940.0))
waist_girth = float(PARAM(lambda: waist_girth, 800.0))
top_length = float(PARAM(lambda: top_length, 560.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 400.0))
neck_girth = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 220.0))
tie_width = float(PARAM(lambda: tie_width, 32.0))
wrap_depth = float(PARAM(lambda: wrap_depth, 0.62))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (sane garment ranges) ─────────────────────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1400.0))
waist_girth = max(560.0, min(waist_girth, 1300.0))
top_length = max(420.0, min(top_length, 760.0))
shoulder_width = max(300.0, min(shoulder_width, 540.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(80.0, min(sleeve_length, 420.0))
tie_width = max(18.0, min(tie_width, 60.0))
wrap_depth = max(0.42, min(wrap_depth, 0.88))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE_BUST = 110.0            # a wrap that must be swung on wants room
EASE_WAIST = 90.0
QUARTER_BUST = (bust_girth + EASE_BUST) / 4.0
QUARTER_WAIST = (waist_girth + EASE_WAIST) / 4.0
HALF_SHOULDER = shoulder_width / 2.0

NECK_W = neck_girth / 6.0 + 10.0     # half front neck width at the shoulder
NECK_DROP_F = neck_girth / 6.0 + 14.0
NECK_DROP_B = 22.0
SHOULDER_SLOPE = 40.0
ARMHOLE_DROP = 215.0                  # generous: an arm that cannot lift far
TOP_Y = top_length - NECK_DROP_F      # y of the front neck point (the piece top)

# The V of the wrap: how far down centre front the wrap edge starts its travel.
# `wrap_depth` is the fraction of the bodice height the V descends to.
V_Y = TOP_Y * (1.0 - wrap_depth)

# The ring anchor height, common to BOTH fronts — this is what keeps the closed
# top level. Placed at the natural waist, clear of the V and clear of the hem.
WAIST_Y = top_length * 0.34
RING_Y = max(WAIST_Y, V_Y * 0.55)


def _bodice_common(quarter_bust, quarter_waist):
    """The side/armhole/shoulder skeleton shared by all three body pieces."""
    return {
        "p_side_hem": fc.P(quarter_waist, 0.0),
        "p_side_top": fc.P(quarter_bust, TOP_Y - ARMHOLE_DROP),
        "p_shoulder_out": fc.P(HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE),
    }


SK = _bodice_common(QUARTER_BUST, QUARTER_WAIST)


def _armhole(p_side_top, p_shoulder_out):
    """The armhole scoop, drafted the same way on every body piece."""
    return fc.Bezier(
        p_side_top,
        fc.P(p_side_top.x - 5.0, p_side_top.y + ARMHOLE_DROP * 0.44),
        fc.P(p_shoulder_out.x + 15.0, p_shoulder_out.y - 44.0),
        p_shoulder_out)


def _side_edge(p_hem, p_top):
    """The side seam: slightly curved in at the waist, out at the bust."""
    return fc.Bezier(p_hem,
                     fc.P(p_hem.x - 6.0, p_hem.y + (p_top.y - p_hem.y) * 0.34),
                     fc.P(p_top.x - 3.0, p_top.y - (p_top.y - p_hem.y) * 0.30),
                     p_top)


# ── The wrap edge, drafted once and reused with a different extension ────────
# Both fronts share the SAME wrap curve from the neck down to the V; below the V
# they run to the hem at different x, because the under front stops at its own
# hem corner while the over front carries a wider hem extension so it can travel
# across the body before the tie takes over.

def _wrap_edge(x_hem):
    """Wrap edge from the neck/shoulder point down to the hem at x_hem.

    A single Bézier from the shoulder neck point through the V to the hem: the
    control points put the V's flatness where the bust needs coverage and let
    the lower run straighten out into the tie's line of pull.
    """
    p_neck = fc.P(NECK_W, TOP_Y)
    p_hem = fc.P(x_hem, 0.0)
    return fc.Bezier(
        p_neck,
        fc.P(NECK_W * 0.30, V_Y + (TOP_Y - V_Y) * 0.30),
        fc.P(x_hem * 0.42, V_Y * 0.52),
        p_hem)


def _front_piece(name, x_hem, label, extra_internals, notches):
    """One wrap front. x_hem is where the wrap edge lands on the hem line.

    x_hem < 0 means the front crosses centre front and keeps travelling — that is
    exactly what the over front does.
    """
    p_hem_wrap = fc.P(x_hem, 0.0)
    p_hem_side = SK["p_side_hem"]
    p_side_top = SK["p_side_top"]
    p_shoulder_out = SK["p_shoulder_out"]
    p_neck = fc.P(NECK_W, TOP_Y)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_wrap, p_hem_side)]),
        fc.Edge("side", [_side_edge(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [_armhole(p_side_top, p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck)]),
        # The wrap edge is drafted neck→hem, so it is REVERSED here to close the
        # ring hem→…→shoulder→neck→(wrap back down to hem).
        fc.Edge("wrap", [_wrap_edge(x_hem)]),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 20.0, "wrap": 14.0},
        notches=notches,
        grainline=fc.Grainline(fc.P(QUARTER_WAIST * 0.55, 40.0),
                               fc.P(QUARTER_WAIST * 0.55, TOP_Y - 60.0)),
        internals=extra_internals,
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def _ring_anchor_x(x_hem):
    """x where the wrap edge sits at RING_Y — the ring/tie anchor point.

    Found by walking the MEASURED flattened wrap curve rather than inverting the
    Bézier: the same polygon the seam checker measures is the one the anchor is
    placed on, so mark and measurement can never disagree.
    """
    pts = _wrap_edge(x_hem).flatten(0.2)
    for a, b in zip(pts, pts[1:], strict=False):
        lo, hi = min(a.y, b.y), max(a.y, b.y)
        if lo - 1e-9 <= RING_Y <= hi + 1e-9:
            span = b.y - a.y
            t = 0.5 if abs(span) < 1e-9 else (RING_Y - a.y) / span
            return a.x + (b.x - a.x) * t
    # RING_Y outside the curve's span (a very shallow V): clamp to the hem end.
    return pts[-1].x


UNDER_X_HEM = QUARTER_WAIST * 0.10          # stops just past centre front
OVER_X_HEM = -QUARTER_WAIST * 0.72          # crosses well over to the other side


def build_under_front():
    """The front that wraps FIRST (cut 1). Carries the D-ring on a short tab.

    Because it lies against the body, its wrap edge is only asked to reach the
    opposite side; the ring anchored on it is the fixed point the over front's
    long tie is threaded through.
    """
    ax = _ring_anchor_x(UNDER_X_HEM)
    internals = [
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, TOP_Y - 30.0)],
                    kind="marking"),
        # The ring tab footprint: a bar-tacked rectangle at the anchor, sized to
        # the tie so the sewn D-ring bar and the tie are the same width.
        fc.Internal("ring-tab",
                    [fc.P(ax - 6.0, RING_Y - tie_width / 2.0 - 4.0),
                     fc.P(ax + tie_width + 6.0, RING_Y - tie_width / 2.0 - 4.0),
                     fc.P(ax + tie_width + 6.0, RING_Y + tie_width / 2.0 + 4.0),
                     fc.P(ax - 6.0, RING_Y + tie_width / 2.0 + 4.0),
                     fc.P(ax - 6.0, RING_Y - tie_width / 2.0 - 4.0)],
                    kind="marking"),
        fc.Internal("ring-anchor",
                    [fc.P(ax - tie_width / 2.0, RING_Y),
                     fc.P(ax + tie_width / 2.0, RING_Y)],
                    kind="drill"),
        fc.Internal("bust-line",
                    [fc.P(0.0, TOP_Y - ARMHOLE_DROP + 40.0),
                     fc.P(QUARTER_BUST - 20.0, TOP_Y - ARMHOLE_DROP + 40.0)],
                    kind="marking"),
    ]
    return _front_piece(
        "under_front", UNDER_X_HEM, "Under front (D-ring side)", internals,
        [fc.Notch("armhole", 0.55, "sleeve cap front match"),
         fc.Notch("side", 0.50, "waist level"),
         fc.Notch("wrap", 0.50, "ring height check")])


def build_over_front():
    """The front that wraps OVER (cut 1). Carries the long tie.

    Its wrap edge lands past centre front on the far side (negative x), which is
    why its hem and its wrap edge both measure longer than the under front's —
    and why the two ties cannot be the same length.
    """
    ax = _ring_anchor_x(OVER_X_HEM)
    internals = [
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, TOP_Y - 30.0)],
                    kind="marking"),
        fc.Internal("tie-anchor",
                    [fc.P(ax - tie_width / 2.0, RING_Y),
                     fc.P(ax + tie_width / 2.0, RING_Y)],
                    kind="drill"),
        # Where the over front crosses the under front's ring — marked so the
        # maker can check the two anchors meet before the tie is stitched on.
        fc.Internal("ring-crossing",
                    [fc.P(ax, RING_Y - 30.0), fc.P(ax, RING_Y + 30.0)],
                    kind="marking"),
        fc.Internal("bust-line",
                    [fc.P(-QUARTER_WAIST * 0.30, TOP_Y - ARMHOLE_DROP + 40.0),
                     fc.P(QUARTER_BUST - 20.0, TOP_Y - ARMHOLE_DROP + 40.0)],
                    kind="marking"),
    ]
    return _front_piece(
        "over_front", OVER_X_HEM, "Over front (long tie)", internals,
        [fc.Notch("armhole", 0.55, "sleeve cap front match"),
         fc.Notch("side", 0.50, "waist level"),
         fc.Notch("wrap", 0.50, "ring height check")])


# ── Solve the back neck width so the shoulder seams MATCH ────────────────────
# Front shoulder runs (HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE) → (NECK_W, TOP_Y).
# The back neck point sits HIGHER than the front's by _BACK_NECK_Y_OFF, so a back
# drafted at the same NECK_W would give a longer shoulder seam. Solve the back
# neck width from the front's MEASURED shoulder length instead.
_F_PROBE = build_under_front()
_SHOULDER_LEN = _F_PROBE.edge("shoulder").length(0.2)
_BACK_NECK_Y_OFF = NECK_DROP_F - NECK_DROP_B - SHOULDER_SLOPE * 0.12
_dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
if _SHOULDER_LEN <= abs(_dy):
    # Degenerate: the vertical run alone exceeds the shoulder. Flatten the back
    # neck rise until a real horizontal run is left.
    _dy = _SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = TOP_Y + _BACK_NECK_Y_OFF


def build_back():
    """Back, cut 1 on fold at centre back.

    Two tie slots are marked at RING_Y on the side seam allowance: the long tie
    passes through one of them on its way round, so the wrap cannot ride up.
    """
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = SK["p_side_hem"]
    p_side_top = SK["p_side_top"]
    p_shoulder_out = SK["p_shoulder_out"]
    p_neck_shoulder = fc.P(NECK_W_BACK, BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, BACK_NECK_Y + 8.0)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [_side_edge(p_hem_side, p_side_top)]),
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
        allowances={"hem": 20.0, "cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match"),
                 fc.Notch("side", 0.50, "waist level")],
        grainline=fc.Grainline(fc.P(QUARTER_WAIST * 0.42, 40.0),
                               fc.P(QUARTER_WAIST * 0.42, BACK_NECK_Y - 60.0)),
        internals=[
            fc.Internal("tie-slot",
                        [fc.P(QUARTER_WAIST - 14.0, RING_Y - tie_width / 2.0 - 3.0),
                         fc.P(QUARTER_WAIST - 14.0, RING_Y + tie_width / 2.0 + 3.0)],
                        kind="drill"),
            fc.Internal("waist-line",
                        [fc.P(0.0, WAIST_Y), fc.P(QUARTER_WAIST - 10.0, WAIST_Y)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold)",
    )


# ── Solve the sleeve cap against the MEASURED armholes ───────────────────────
_U = build_under_front()
_O = build_over_front()
_B = build_back()
# The armhole a sleeve is set into is ONE front armhole plus ONE back armhole;
# both fronts are drafted on the same skeleton, so either front measures the
# same — averaged here so a future asymmetric front cannot silently break it.
ARMHOLE_F = (_U.edge("armhole").length(0.2) + _O.edge("armhole").length(0.2)) / 2.0
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 16.0
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
BICEPS = max(300.0, (ARMHOLE_F + ARMHOLE_B) * 0.74)


def _cap_segments(cap_h, top_y):
    """A symmetric two-Bézier cap of height cap_h, left underarm to right."""
    half = BICEPS / 2.0
    p_l = fc.P(-half, top_y - cap_h)
    p_top = fc.P(0.0, top_y)
    p_r = fc.P(half, top_y - cap_h)
    return [
        fc.Bezier(p_l, fc.P(-half * 0.70, top_y - cap_h * 0.95),
                  fc.P(-half * 0.32, top_y - cap_h * 0.05), p_top),
        fc.Bezier(p_top, fc.P(half * 0.32, top_y - cap_h * 0.05),
                  fc.P(half * 0.70, top_y - cap_h * 0.95), p_r),
    ]


def _solve_cap_height():
    """Bisect cap height until the MEASURED cap equals CAP_TARGET.

    Cap length is monotone in cap height at fixed biceps width, so a bracket
    from nearly flat to nearly semicircular always contains the root.
    """
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


def build_sleeve():
    """Short set-in sleeve (cut 2 mirrored): solved cap, open hem, no cuff."""
    half = BICEPS / 2.0
    hem_half = max(80.0, half * 0.86)     # barely tapered: an arm goes in easily
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
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"sleeve_hem": 26.0},
        notches=[fc.Notch("cap", 0.50, "shoulder point"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, top_y - 30.0)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Short sleeve",
    )


# ── Solve the two tie lengths from the MEASURED wrap edges ───────────────────
# The SHORT tie only has to reach from its anchor on the under front round to
# where the over front will cross it — a short hop, plus the bar-tack tails.
# The LONG tie has to leave the over front's anchor, travel the rest of the way
# round the body, pass the back tie slot, thread the ring, and come back with
# enough left in hand to grip. Both are computed from what the pieces MEASURE.
_UNDER_WRAP = _U.edge("wrap").length(0.2)
_OVER_WRAP = _O.edge("wrap").length(0.2)
_BACK_HALF_WAIST = _B.edge("hem").length(0.2)

TIE_TAIL = 180.0            # what a single hand needs left over to pull on
TIE_TACK = 45.0             # sewn into the anchor at each end
# Short tie: anchor → ring, i.e. the horizontal offset between the two anchors,
# taken as the difference of the two measured wrap runs plus a working margin.
TIE_SHORT = max(120.0, abs(_OVER_WRAP - _UNDER_WRAP) + tie_width * 2.0 + TIE_TACK)
# Long tie: round the remaining body (two back half-waists + one front quarter),
# through the slot and the ring, and back with a tail.
TIE_LONG = (2.0 * _BACK_HALF_WAIST + QUARTER_WAIST + TIE_TAIL + TIE_TACK)


def build_tie():
    """The tie strip pattern (cut 2 — see the marked cut lines for the two
    lengths). One shape, two cuts: a maker cuts the long tie at full length and
    the short tie at the marked line, so there is no second pattern piece to
    lose and no chance of cutting two of the same length by accident.
    """
    w = tie_width
    ln = TIE_LONG
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, w)
    p3 = fc.P(0.0, w)
    edges = [
        fc.Edge("lower", [fc.Line(p0, p1)]),
        fc.Edge("end_far", [fc.Line(p1, p2)]),
        fc.Edge("upper", [fc.Line(p2, p3)]),
        fc.Edge("end_anchor", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "tie", edges,
        seam_allowance=seam_allowance,
        allowances={"end_far": 16.0, "end_anchor": 0.0},
        notches=[fc.Notch("lower", 0.0, "anchor end"),
                 fc.Notch("lower", min(0.98, TIE_SHORT / ln), "SHORT tie cut line")],
        grainline=fc.Grainline(fc.P(30.0, w / 2.0), fc.P(ln - 30.0, w / 2.0)),
        internals=[
            fc.Internal("short-tie-cut",
                        [fc.P(TIE_SHORT, 0.0), fc.P(TIE_SHORT, w)],
                        kind="marking"),
            fc.Internal("ring-bar-width",
                        [fc.P(TIE_SHORT * 0.5, 0.0), fc.P(TIE_SHORT * 0.5, w)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Tie strip (long + short, marked)",
    )


def build():
    pattern = fc.PatternSet("one-hand-wrap-top")
    everything = target_piece == "set"
    if everything or target_piece == "under_front":
        pattern.add(build_under_front())
    if everything or target_piece == "over_front":
        pattern.add(build_over_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "tie":
        pattern.add(build_tie())

    if everything:
        # Both fronts join the back at the side seams — drafted on one skeleton,
        # so this is the check that a future edit has not broken that.
        pattern.declare_seam(("under_front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("over_front", "side"), ("back", "side"), tol=1.0)
        # Shoulder seams: the point of the NECK_W_BACK solve.
        pattern.declare_seam(("under_front", "shoulder"), ("back", "shoulder"), tol=0.5)
        pattern.declare_seam(("over_front", "shoulder"), ("back", "shoulder"), tol=0.5)
        # The sleeve cap takes one front armhole plus one back armhole, with ease.
        pattern.declare_seam(("sleeve", "cap"),
                             [("under_front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cotton jersey, medium weight", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 70% marker (the over front is a wide, "
                 "poorly-nesting shape); a jersey forgives a wrap that is pulled "
                 "a little tighter on a bad day."},
        {"item": "D-ring", "qty": 1, "unit": "count",
         "note": f"Yantra4D d-ring (notion.hardware_ref), bar for {tie_width:.0f} mm "
                 f"webbing — the same tie_width this pattern cuts the tie at."},
        {"item": "twill tape / interfacing", "qty": round(tie_width * 6.0),
         "unit": "mm_length",
         "note": "behind the ring tab and behind the back tie slot; both take the "
                 "whole closing load of the garment."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "bar-tack the ring tab and both tie anchors — those three points "
                 "are the only things holding the top shut."},
    ]
    pattern.metadata = {
        "fc300_rank": 248,
        "family": "adaptive",
        "fabric_hint": "jersey-algodon",
        "finished_mm": {
            "top_length": round(top_length, 1),
            "quarter_bust": round(QUARTER_BUST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "wrap_v_height": round(V_Y, 1),
            "ring_height": round(RING_Y, 1),
        },
        "solved": {
            "under_wrap_measured_mm": round(_UNDER_WRAP, 2),
            "over_wrap_measured_mm": round(_OVER_WRAP, 2),
            "wrap_run_delta_mm": round(_OVER_WRAP - _UNDER_WRAP, 2),
            "tie_short_mm": round(TIE_SHORT, 2),
            "tie_long_mm": round(TIE_LONG, 2),
            "back_neck_half_width_mm": round(NECK_W_BACK, 2),
            "front_shoulder_measured_mm": round(_SHOULDER_LEN, 2),
            "sleeve_cap_height_mm": round(CAP_H, 2),
            "armhole_front_mm": round(ARMHOLE_F, 2),
            "armhole_back_mm": round(ARMHOLE_B, 2),
            "note": "the two ties are sized from the MEASURED wrap-edge runs, not from a "
                    "girth formula; the back neck width is solved by Pythagoras from the "
                    "front's MEASURED shoulder length, because the back neck sits higher "
                    "and an equal neck width would leave the back shoulder ~23 mm long.",
        },
        "adaptive": {
            "one_handed_closure": "the under front's tie ends in a fixed D-ring; the over "
                                  "front's long tie threads it and pulls back on itself, so "
                                  "one hand closes the top in a single straight motion and "
                                  "the ring holds tension while the hand lets go",
            "no_blind_reach": "the back tie slot is at the side seam within reach of the "
                              "working hand — nothing has to be found behind the back",
            "ring_register": "both tie anchors sit at ONE height above the hem, measured on "
                             "each front's own wrap edge, so the closed top pulls level",
            "dressing": "swing on like a cardigan; no overhead motion, no buttons",
        },
        "hardware": "D-ring via Yantra4D (notion.hardware_ref -> d-ring); the ring's "
                    "webbing bar is driven by this top's tie_width, which is also the "
                    "width the tie strip is cut at",
    }
    return pattern


result = build()

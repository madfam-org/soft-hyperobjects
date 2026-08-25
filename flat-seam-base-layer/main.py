"""
Flat-Seam Base Layer — Fashion Cabinet Garment Cartridge (FC-300 #250, adaptive II).

A long-sleeved base layer drafted so that NO seam crosses a pressure point. It
carries no hardware at all — the whole adaptive claim is in where the seams are
and are not, which is why this cartridge is pattern-only by design rather than
for want of a solid on the shelf.

Who this is for: autistic and otherwise sensory-sensitive wearers for whom a
shoulder seam under a backpack strap or a side seam under a waistband is not a
mild annoyance but the reason a day ends early; people with fragile or
hypersensitive skin — epidermolysis bullosa, graft sites, radiotherapy fields,
neuropathy, allodynia after shingles; wheelchair users whose whole body weight
rests on the ischial tuberosities and the shoulder blades for hours; and anyone
in a prosthetic socket or a brace, where a seam under the liner becomes a
pressure sore.

The conventional answers do not work. «Seamless» knitwear still has a bound neck,
a closing seam somewhere, and a heat-set label. Turning a normal tee inside out
moves the allowance outward but leaves the seam LINE in exactly the same place.
So this is drafted the other way round: the seams are moved off the body's
loaded lines first, and the pattern is solved to whatever that costs.

The drafting problems that had to be solved, not assumed:

  1. ROTATED SIDE SEAM. The side seam is rotated FORWARD off the body's lateral
     pressure line (the line an armrest, a wheelchair side guard, a waistband
     seam and a bra band all load). That makes the front narrower and the back
     wider — the two pieces are no longer symmetric. The back's rotation is
     therefore BISECTED until its measured side edge equals the front's, because
     two edges of unequal length cannot be joined in a flat, ridge-free seam,
     which is the entire point of the garment.

  2. FORWARD-ROTATED SHOULDER. The shoulder seam is likewise rotated forward off
     the trapezius crest, where a strap, a seatbelt and a sling all bear. Front
     and back shoulders then start from different neck points, so the back neck
     width is solved by Pythagoras from the front's MEASURED shoulder length —
     drafting both at one neck width mismatches by roughly 23 mm.

  3. SPINE AND SEAT CLEAR. Centre back is cut on the fold, so the spine has no
     seam at all; the hem is cut LONG and level at the back, so the garment
     stays under a seated wearer without the hem edge itself becoming the ridge.

Pieces:
  - front       : cut 1 on fold at CF (no centre-front seam).
  - back        : cut 1 on fold at CB (no spine seam), wider by the rotation.
  - sleeve      : cut 2 mirrored, one-piece, underarm seam only.
  - neck_band   : the flatlock neck band (cut 1), cut to the MEASURED neckline.

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
# front|back|sleeve|neck_band|set

chest_girth = float(PARAM(lambda: chest_girth, 920.0))
body_length = float(PARAM(lambda: body_length, 700.0))
back_hem_extra = float(PARAM(lambda: back_hem_extra, 90.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 420.0))
neck_girth = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 560.0))
seam_rotation = float(PARAM(lambda: seam_rotation, 55.0))
negative_ease = float(PARAM(lambda: negative_ease, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (sane garment ranges) ─────────────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1450.0))
body_length = max(540.0, min(body_length, 900.0))
back_hem_extra = max(0.0, min(back_hem_extra, 220.0))
shoulder_width = max(300.0, min(shoulder_width, 550.0))
neck_girth = max(290.0, min(neck_girth, 540.0))
sleeve_length = max(300.0, min(sleeve_length, 720.0))
seam_rotation = max(0.0, min(seam_rotation, 110.0))
negative_ease = max(0.0, min(negative_ease, 110.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

# A base layer is cut SMALLER than the body: it is held against the skin by the
# knit's own stretch, because a garment that can shift is a garment that abrades.
QUARTER_CHEST = (chest_girth - negative_ease) / 4.0
HALF_SHOULDER = shoulder_width / 2.0

NECK_W = neck_girth / 6.0 + 9.0
NECK_DROP_F = neck_girth / 6.0 + 16.0
NECK_DROP_B = 20.0
SHOULDER_SLOPE = 36.0
ARMHOLE_DROP = 225.0
TOP_Y = body_length - NECK_DROP_F     # y of the front neck point

# The rotation cannot eat more than the front has to give, or the front becomes
# a strip and the "seam off the pressure line" turns into "seam at centre front".
ROT = min(seam_rotation, QUARTER_CHEST * 0.42)

# Front loses the rotation, back gains it — the seam moves forward around the
# body while the total girth stays put.
FRONT_HALF = QUARTER_CHEST - ROT
BACK_HALF_NOMINAL = QUARTER_CHEST + ROT

# The shoulder is rotated forward by the same idea, scaled to the shoulder's own
# width: the seam leaves the trapezius crest and sits on the front deltoid.
SHOULDER_ROT = min(ROT * 0.45, HALF_SHOULDER * 0.30)


def _side_edge(p_hem, p_top, bow):
    """The side seam, as a gentle curve. `bow` is the inward pull at the waist.

    Front and back use the same generator so the two edges are the same KIND of
    curve; what differs between them is solved, not hand-tuned.
    """
    dy = p_top.y - p_hem.y
    return fc.Bezier(
        p_hem,
        fc.P(p_hem.x - bow, p_hem.y + dy * 0.36),
        fc.P(p_top.x - bow * 0.45, p_top.y - dy * 0.30),
        p_top)


def _armhole(p_side_top, p_shoulder_out, depth_bias):
    """The armhole scoop. depth_bias shifts the low control point so the front
    and back scoops differ the way real armholes do."""
    return fc.Bezier(
        p_side_top,
        fc.P(p_side_top.x - 4.0, p_side_top.y + ARMHOLE_DROP * depth_bias),
        fc.P(p_shoulder_out.x + 13.0, p_shoulder_out.y - 40.0),
        p_shoulder_out)


SIDE_BOW = 7.0


def build_front():
    """Front, cut 1 on fold at centre front. Narrowed by the seam rotation.

    The shoulder's outer point is pulled FORWARD-shortened by SHOULDER_ROT: on
    the flat pattern the front shoulder is the shorter of the two, which is what
    puts the finished seam in front of the trapezius crest rather than on it.
    """
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(FRONT_HALF, 0.0)
    p_side_top = fc.P(FRONT_HALF, TOP_Y - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER - SHOULDER_ROT, TOP_Y - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, TOP_Y)
    p_neck_cf = fc.P(0.0, TOP_Y - NECK_DROP_F * 0.12)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [_side_edge(p_hem_side, p_side_top, SIDE_BOW)]),
        fc.Edge("armhole", [_armhole(p_side_top, p_shoulder_out, 0.46)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.54, TOP_Y - 11.0),
                                   fc.P(NECK_W * 0.20, p_neck_cf.y),
                                   p_neck_cf)]),
        fc.Edge("cf_fold", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        # Every allowance is small: this garment is flatlocked, and a flatlock
        # seam is trimmed to the stitch width. A wide allowance folded back IS
        # the ridge the garment exists to avoid.
        allowances={"hem": 12.0, "cf_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap front match"),
                 fc.Notch("side", 0.58, "waist level")],
        grainline=fc.Grainline(fc.P(FRONT_HALF * 0.45, 40.0),
                               fc.P(FRONT_HALF * 0.45, TOP_Y - 50.0)),
        internals=[
            # The lateral pressure line the seam has been moved OFF. Marked so a
            # maker can see the clearance they bought and check it on a body.
            fc.Internal("pressure-line-cleared",
                        [fc.P(QUARTER_CHEST, 0.0),
                         fc.P(QUARTER_CHEST, TOP_Y - ARMHOLE_DROP)],
                        kind="marking"),
            # No woven label anywhere: the size goes here, printed on the fabric.
            fc.Internal("printed-size-mark",
                        [fc.P(18.0, TOP_Y - 90.0), fc.P(78.0, TOP_Y - 90.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Front (cut on fold, no CF seam)",
    )


# ── Solve the back neck width so the shoulder seams MATCH ────────────────────
# The back neck sits higher than the front's, AND the back shoulder starts from a
# different outer x than the front's (the shoulder rotation). Drafting both at
# one neck width would leave the back shoulder roughly 23 mm long — on a
# flatlocked base layer an eased-in shoulder is a pucker, and a pucker under a
# strap is the exact ridge this garment exists to avoid.
_F_PROBE = build_front()
_SHOULDER_LEN = _F_PROBE.edge("shoulder").length(0.2)
_BACK_NECK_Y_OFF = NECK_DROP_F - NECK_DROP_B - SHOULDER_SLOPE * 0.10
_dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
if _SHOULDER_LEN <= abs(_dy):
    _dy = _SHOULDER_LEN * 0.85
    _BACK_NECK_Y_OFF = _dy - SHOULDER_SLOPE  # the drawn rise must track the flattened run
# The back's shoulder OUTER point sits further out by SHOULDER_ROT (the seam has
# rotated forward, so the back panel carries more of the shoulder).
_BACK_SHOULDER_OUT = HALF_SHOULDER + SHOULDER_ROT
NECK_W_BACK = _BACK_SHOULDER_OUT - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = TOP_Y + _BACK_NECK_Y_OFF


# ── Solve the back's side edge to EQUAL the front's ──────────────────────────
# The rotation makes the back wider, and the back hem is also dropped by
# back_hem_extra so it stays under a seated wearer. Both of those change the
# back's side-edge LENGTH. Two side edges of unequal length cannot be joined in
# a flat, ridge-free flatlock seam — easing one into the other is precisely the
# pucker this garment must not have. So the back's half-width at the HEM is
# BISECTED until its measured side edge equals the front's.
FRONT_SIDE_LEN = _F_PROBE.edge("side").length(0.2)


def _back_side_edge(hem_half):
    """The back side edge for a trial hem half-width.

    The back's side hem point sits at the SAME height as the front's (y = 0).
    The extra back length is taken entirely at centre back, as a hem that sweeps
    down from this shared side point — see build_back's `hem` edge. Dropping the
    whole back hem line instead would lengthen this edge by the full drop, and no
    hem width could then bring it back to the front's: the side seam would be
    over-constrained and could only be closed by easing, i.e. by a pucker.
    """
    p_hem = fc.P(hem_half, 0.0)
    p_top = fc.P(BACK_HALF_NOMINAL, TOP_Y - ARMHOLE_DROP)
    return _side_edge(p_hem, p_top, SIDE_BOW)


def _solve_back_hem_half():
    """Bisect the back's hem half-width until its side edge measures the front's.

    Careful: this length is NOT monotone in the hem half-width. It falls to a
    minimum where the hem point sits directly below the side-top point (the edge
    is then as near vertical as the waist bow allows) and rises again on either
    side. A naive bracket spanning that minimum has the SAME sign at both ends
    whenever the target is above the minimum, and sign-based bisection would
    silently fall back to an endpoint — which is how this seam ends up 38 mm out.

    So: locate the minimum first (it is at x = the side-top x), then bisect on
    the single monotone branch that can actually reach the target. The TAPERED
    branch is preferred, because a base layer wants the hem drawn in to the body
    rather than flared away from it.

    If the front's edge is shorter than the back's achievable minimum, the
    minimum itself is returned — the closest a flat seam can get — and the
    residual is reported in metadata rather than hidden.
    """
    def f(x):
        return _back_side_edge(x).length(0.2) - FRONT_SIDE_LEN
    x_min = BACK_HALF_NOMINAL          # the near-vertical edge: the minimum
    if f(x_min) >= 0.0:
        # The target is at or below the minimum — nothing to solve toward.
        return x_min
    # Walk DOWN (tapered branch) until the edge is long enough to bracket.
    lo = x_min
    hi = x_min
    for _ in range(60):
        lo *= 0.94
        if f(lo) > 0.0:
            break
    if f(lo) <= 0.0:
        # The tapered branch never gets there; try the flared branch instead.
        lo = x_min
        hi = x_min
        for _ in range(60):
            hi *= 1.06
            if f(hi) > 0.0:
                break
        if f(hi) <= 0.0:
            return x_min
        lo, hi = x_min, hi
    else:
        lo, hi = lo, x_min
    # Now f(lo) and f(hi) straddle zero on ONE monotone branch.
    f_lo = f(lo)
    for _ in range(90):
        mid = (lo + hi) / 2.0
        f_mid = f(mid)
        if abs(f_mid) < 0.02:
            return mid
        if f_lo * f_mid <= 0.0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


BACK_HEM_HALF = _solve_back_hem_half()
BACK_SIDE_LEN = _back_side_edge(BACK_HEM_HALF).length(0.2)


def build_back():
    """Back, cut 1 on fold at centre back — the spine has no seam at all.

    Wider than the front by the rotation, hem dropped by back_hem_extra, and the
    hem half-width SOLVED so the side edge measures the front's.
    """
    p_hem_cb = fc.P(0.0, -back_hem_extra)
    p_hem_side = fc.P(BACK_HEM_HALF, 0.0)
    p_side_top = fc.P(BACK_HALF_NOMINAL, TOP_Y - ARMHOLE_DROP)
    p_shoulder_out = fc.P(_BACK_SHOULDER_OUT, TOP_Y - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, BACK_NECK_Y + 6.0)

    edges = [
        # The hem SWEEPS: level with the front at the shared side point, falling
        # to back_hem_extra below it at centre back. All of the extra back length
        # is taken here, at CB, and none of it on the side seam — which is what
        # lets the side seam be solved to the front's length at all.
        fc.Edge("hem", [fc.Bezier(p_hem_cb,
                                  fc.P(BACK_HEM_HALF * 0.34, -back_hem_extra * 0.94),
                                  fc.P(BACK_HEM_HALF * 0.70, -back_hem_extra * 0.42),
                                  p_hem_side)]),
        fc.Edge("side", [_side_edge(p_hem_side, p_side_top, SIDE_BOW)]),
        fc.Edge("armhole", [_armhole(p_side_top, p_shoulder_out, 0.44)]),
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
        allowances={"hem": 12.0, "cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match"),
                 fc.Notch("side", 0.58, "waist level")],
        grainline=fc.Grainline(fc.P(BACK_HALF_NOMINAL * 0.42, 40.0),
                               fc.P(BACK_HALF_NOMINAL * 0.42, BACK_NECK_Y - 50.0)),
        internals=[
            fc.Internal("pressure-line-cleared",
                        [fc.P(QUARTER_CHEST, 20.0),
                         fc.P(QUARTER_CHEST, TOP_Y - ARMHOLE_DROP)],
                        kind="marking"),
            # The scapula band: where a wheelchair backrest and a rucksack both
            # bear. Nothing may be seamed, printed or bar-tacked inside it.
            fc.Internal("scapula-keep-clear",
                        [fc.P(0.0, TOP_Y - 250.0), fc.P(BACK_HALF_NOMINAL - 20.0, TOP_Y - 250.0),
                         fc.P(BACK_HALF_NOMINAL - 20.0, TOP_Y - 110.0),
                         fc.P(0.0, TOP_Y - 110.0), fc.P(0.0, TOP_Y - 250.0)],
                        kind="marking"),
            # The seat line: level with the front's hem and with the shared side
            # point. Everything BELOW it is the swept tail the wearer sits on.
            fc.Internal("seat-line",
                        [fc.P(0.0, 0.0), fc.P(BACK_HEM_HALF - 10.0, 0.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold, no spine seam, dropped hem)",
    )


# ── Solve the sleeve cap against the MEASURED armholes ───────────────────────
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
# A base layer takes essentially NO cap ease: ease is fabric eased into a shorter
# edge, i.e. a gathered ripple, i.e. a ridge under a sleeve. Zero here is a
# deliberate choice, not an oversight.
CAP_EASE = 0.0
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
BICEPS = max(260.0, (ARMHOLE_F + ARMHOLE_B) * 0.70)


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
    """Bisect the cap height until the MEASURED cap equals CAP_TARGET."""
    lo, hi = 15.0, BICEPS * 0.95
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
    """One-piece long sleeve (cut 2 mirrored): ONE underarm seam, nothing else.

    The cuff is a fold-back, not an applied band: an applied cuff means a seam
    ring right where a watch, a splint, a cannula dressing or a walking-frame
    grip sits.
    """
    half = BICEPS / 2.0
    cuff_half = max(62.0, half * 0.52)
    top_y = sleeve_length + CAP_H
    cap = _cap_segments(CAP_H, top_y)
    p_l_under = fc.P(-half, top_y - CAP_H)
    p_r_under = fc.P(half, top_y - CAP_H)
    p_l_cuff = fc.P(-cuff_half, 0.0)
    p_r_cuff = fc.P(cuff_half, 0.0)

    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r_under, p_r_cuff)]),
        fc.Edge("cuff", [fc.Line(p_r_cuff, p_l_cuff)]),
        fc.Edge("under_l", [fc.Line(p_l_cuff, p_l_under)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        # A deep fold-back cuff: turned twice and flatlocked, so the wrist meets
        # folded fabric rather than a seam ring.
        allowances={"cuff": 46.0},
        notches=[fc.Notch("cap", 0.50, "shoulder point"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, top_y - 30.0)),
        internals=[
            fc.Internal("elbow-keep-clear",
                        [fc.P(-half * 0.85, top_y * 0.42),
                         fc.P(half * 0.85, top_y * 0.42)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Long sleeve (single underarm seam)",
    )


# ── The neck band, cut to the MEASURED neckline ──────────────────────────────
# Front neck ×2 plus back neck ×2 (both pieces are on the fold). A band cut to a
# neck-girth formula either strangles or gapes; here it is cut to what the two
# pieces actually present, then shortened by a stretch factor so it holds without
# needing to be stretched hard enough to roll — a rolled band is a cord across
# the collarbones, which for this wearer is worse than no band at all.
NECKLINE = 2.0 * _F.edge("neck").length(0.2) + 2.0 * _B.edge("neck").length(0.2)
BAND_STRETCH = 0.90
BAND_LEN = NECKLINE * BAND_STRETCH
BAND_H = 44.0                # folded double to 22 mm finished


def build_neck_band():
    """The neck band (cut 1), folded double lengthwise and flatlocked on."""
    ln = BAND_LEN
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, BAND_H)
    p3 = fc.P(0.0, BAND_H)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),
        fc.Edge("join_b", [fc.Line(p1, p2)]),
        fc.Edge("fold", [fc.Line(p2, p3)]),
        fc.Edge("join_a", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "neck_band", edges,
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("attach", 0.25, "shoulder seam match"),
                 fc.Notch("attach", 0.50, "centre back"),
                 fc.Notch("attach", 0.75, "shoulder seam match")],
        grainline=fc.Grainline(fc.P(25.0, BAND_H / 2.0), fc.P(ln - 25.0, BAND_H / 2.0)),
        internals=[
            fc.Internal("lengthwise-fold",
                        [fc.P(0.0, BAND_H / 2.0), fc.P(ln, BAND_H / 2.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Neck band (cut to measured neckline)",
    )


def build():
    pattern = fc.PatternSet("flat-seam-base-layer")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "neck_band":
        pattern.add(build_neck_band())

    if everything:
        # THE load-bearing check. A flatlock seam cannot ease one edge into a
        # shorter one without puckering, and a pucker is the ridge this whole
        # garment exists to avoid. tol=0.5 — far tighter than a normal side seam.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=0.5)
        # Shoulders: the point of the NECK_W_BACK solve, likewise tight.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=0.5)
        # Sleeve cap takes one front armhole plus one back armhole at ZERO ease.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)
        # The band is deliberately SHORT of the neckline by the stretch factor.
        pattern.declare_seam(("neck_band", "attach"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")],
                             tol=1.0, ease=BAND_LEN - NECKLINE)

    fabric_width = 1700.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "merino/tencel jersey, 150 gsm, flat-knit", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1700 mm width, 80% marker. Choose the softest hand available "
                 "and pre-wash: a finish that softens after three washes has already "
                 "cost this wearer three days."},
        {"item": "woolly nylon / textured thread", "qty": 4, "unit": "cone",
         "note": "flatlock (coverstitch) EVERY seam, stitch-side against the skin. "
                 "A textured thread lies flatter than a spun one; on this garment "
                 "the thread is the surface the body touches."},
        {"item": "printed size/care mark", "qty": 1, "unit": "count",
         "note": "printed directly on the fabric at the marked location. NO woven "
                 "label anywhere — a label is the single most-reported reason a "
                 "sensory-sensitive wearer refuses a garment."},
    ]
    pattern.metadata = {
        "fc300_rank": 250,
        "family": "adaptive",
        "fabric_hint": "jersey-algodon",
        "finished_mm": {
            "body_length_front": round(body_length, 1),
            "body_length_back": round(body_length + back_hem_extra, 1),
            "quarter_chest_nominal": round(QUARTER_CHEST, 1),
            "front_half_width": round(FRONT_HALF, 1),
            "back_half_width_chest": round(BACK_HALF_NOMINAL, 1),
            "seam_rotation_applied": round(ROT, 1),
        },
        "solved": {
            "front_side_mm": round(FRONT_SIDE_LEN, 2),
            "back_side_mm": round(BACK_SIDE_LEN, 2),
            "side_delta_mm": round(BACK_SIDE_LEN - FRONT_SIDE_LEN, 3),
            "back_hem_half_solved_mm": round(BACK_HEM_HALF, 2),
            "back_neck_half_width_mm": round(NECK_W_BACK, 2),
            "front_shoulder_measured_mm": round(_SHOULDER_LEN, 2),
            "shoulder_rotation_mm": round(SHOULDER_ROT, 2),
            "neckline_measured_mm": round(NECKLINE, 2),
            "band_length_mm": round(BAND_LEN, 2),
            "sleeve_cap_height_mm": round(CAP_H, 2),
            "cap_ease_mm": CAP_EASE,
            "note": "the back's hem half-width was BISECTED until its measured side edge "
                    "equalled the front's, because the seam rotation widens the back and "
                    "the dropped hem lengthens its side edge — and two edges of unequal "
                    "length cannot be flatlocked without a pucker, which is the ridge "
                    "this garment exists to avoid. Cap ease is ZERO for the same reason.",
        },
        "adaptive": {
            "no_hardware": "there is none: the entire adaptive claim is WHERE the seams "
                           "are and are not, which is why this cartridge is pattern-only "
                           "by design rather than for want of a solid on the shelf",
            "seams_moved_off": "side seam rotated forward off the lateral pressure line "
                               "(armrest, wheelchair side guard, waistband, bra band); "
                               "shoulder seam rotated forward off the trapezius crest "
                               "(strap, seatbelt, sling)",
            "seams_absent": "no centre-front seam, no spine seam (both pieces on the fold), "
                            "no applied cuff band, no woven label anywhere",
            "seated_hem": f"back hem dropped {back_hem_extra:.0f} mm so the garment stays "
                          f"under a seated wearer without the hem edge becoming the ridge",
            "construction": "flatlock every seam with the stitch side against the skin; "
                            "allowances are deliberately small because a folded allowance "
                            "IS a ridge",
            "who": "autistic and sensory-sensitive wearers; fragile or hypersensitive skin "
                   "(epidermolysis bullosa, graft sites, radiotherapy fields, neuropathy, "
                   "allodynia); wheelchair users; prosthetic socket and brace liners",
        },
        "hardware": "none — pattern-only by design; see adaptive.no_hardware",
    }
    return pattern


result = build()

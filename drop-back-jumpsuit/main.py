"""
Drop-Back Jumpsuit — Fashion Cabinet Garment Cartridge (FC-300 #251, adaptive II).

A jumpsuit whose entire seat drops away on two webbing straps, so a seated wearer
can use a toilet without taking the garment off, without standing, and without a
second person in the room.

The problem is not comfort, it is autonomy and time. A one-piece garment is the
warmest, tidiest, least-riding-up thing a wheelchair user can wear, and it is
also the one that turns a five-minute toilet transfer into a twenty-minute
undressing that needs help. So the usual advice is: do not wear a jumpsuit. This
one keeps the jumpsuit and removes the reason.

The seat panel hangs from two D-rings at the waist. Unhook them and the panel
falls forward between the legs, still attached along its front edge — it cannot
be dropped, lost, or land on a wet floor, which is what happens with a fully
detachable panel. Rehooking is a one-handed upward pull against a ring that holds
tension while the hand lets go. The ring SOLID is Yantra4D territory (`d-ring`;
see notion.hardware_ref), and its webbing bar takes this jumpsuit's own strap
width, so the strap is the same dimension on both sides of the bridge.

The drafting problems that had to be solved, not assumed:

  1. THE DROP OPENING MUST CLOSE. The panel's three attached edges and the hole
     it leaves in the bodice+legs are the same seam seen from two sides. Both are
     MEASURED off the built pieces and declared, so the panel cannot come up
     short — the classic failure when a "drop seat" is drafted as a rectangle
     against a curved rise.

  2. SEATED RISE, OPEN AT THE SIDE. The back rise is lengthened and the front
     rise shortened by `seat_rise_extra`, so the waistband sits level on a body
     flexed at 90 degrees. The two side edges then start at different heights,
     which would make them unequal — and they are the seam the whole garment
     hangs from. So front and back SHARE ONE side-waist point at a common
     height, the rise tilt is taken at CF/CB where it belongs, and the back's
     hem half-width is then BISECTED to close whatever residual is left.

  3. STRAP LENGTH FROM MEASUREMENT. The straps run from the panel's top corners
     up to the waistband rings. Their length is taken from the MEASURED rise
     difference between the panel edge and the band, plus the ring wrap — never
     from a rise formula, because the rise here is the one thing that has just
     been deliberately tilted.

Pieces:
  - front : jumpsuit front (cut 2 mirrored), bodice + leg in one, shortened rise.
  - back  : jumpsuit back (cut 2 mirrored), lengthened rise, seat opening cut out.
  - seat  : the drop panel (cut 1 on fold at CF), hinged at the front crotch.
  - band  : the waistband (cut 1 on fold), carrying both D-ring anchors.
  - strap : the webbing-facing strap (cut 2), panel corner to ring.

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
# front|back|seat|band|strap|set

chest_girth = float(PARAM(lambda: chest_girth, 980.0))
waist_girth = float(PARAM(lambda: waist_girth, 860.0))
hip_girth = float(PARAM(lambda: hip_girth, 1020.0))
bodice_length = float(PARAM(lambda: bodice_length, 420.0))
inseam_length = float(PARAM(lambda: inseam_length, 740.0))
front_rise = float(PARAM(lambda: front_rise, 290.0))
hem_width = float(PARAM(lambda: hem_width, 210.0))
seat_rise_extra = float(PARAM(lambda: seat_rise_extra, 55.0))
strap_width = float(PARAM(lambda: strap_width, 30.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (sane garment ranges) ─────────────────────────────────────────────
chest_girth = max(720.0, min(chest_girth, 1500.0))
waist_girth = max(600.0, min(waist_girth, 1400.0))
hip_girth = max(700.0, min(hip_girth, 1550.0))
bodice_length = max(320.0, min(bodice_length, 560.0))
inseam_length = max(520.0, min(inseam_length, 950.0))
front_rise = max(220.0, min(front_rise, 400.0))
hem_width = max(140.0, min(hem_width, 320.0))
seat_rise_extra = max(0.0, min(seat_rise_extra, 130.0))
strap_width = max(18.0, min(strap_width, 50.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

EASE_CHEST = 150.0            # a one-piece must admit a whole body at once
EASE_WAIST = 90.0
EASE_HIP = 110.0
QUARTER_CHEST = (chest_girth + EASE_CHEST) / 4.0
QUARTER_WAIST = (waist_girth + EASE_WAIST) / 4.0
QUARTER_HIP = (hip_girth + EASE_HIP) / 4.0
HEM_Q = hem_width / 2.0

# ── The seated rise tilt ─────────────────────────────────────────────────────
# The back rise gains what the front loses. This is the whole seated correction:
# a level waistband on a body flexed at 90 degrees instead of one that gapes at
# the back and cuts in at the front.
RISE_F = front_rise - seat_rise_extra * 0.45
RISE_B = front_rise + seat_rise_extra

# CRUCIAL (and the trap this cartridge was written around): the tilt is taken at
# CENTRE FRONT and CENTRE BACK, not at the side. Front and back therefore SHARE
# one side-waist point at a common height. If the tilt were applied at the side
# too, the two side edges would differ by the full seat_rise_extra and no hem
# width could bring them back — the seam the garment hangs from would only close
# by easing.
SIDE_WAIST_Y = inseam_length + front_rise      # the shared side-waist height
CROTCH_Y = inseam_length                        # both crotch points sit here
BAND_TOP_Y = SIDE_WAIST_Y + bodice_length       # shoulder/top of the bodice


def _leg_side(p_hem, p_waist):
    """The outer leg line, hem to waist: a gentle curve over the hip."""
    dy = p_waist.y - p_hem.y
    return fc.Bezier(
        p_hem,
        fc.P(p_hem.x + (p_waist.x - p_hem.x) * 0.42, p_hem.y + dy * 0.46),
        fc.P(p_waist.x + 10.0, p_waist.y - dy * 0.26),
        p_waist)


def _inseam(p_hem, p_crotch):
    """The inner leg line, hem to crotch."""
    dy = p_crotch.y - p_hem.y
    return fc.Bezier(
        p_hem,
        fc.P(p_hem.x * 0.72, p_hem.y + dy * 0.44),
        fc.P(p_crotch.x * 0.80, p_crotch.y - dy * 0.22),
        p_crotch)


# The seat opening: how far up the back rise the drop panel reaches, and how wide
# it is at the waist. Below/behind this line the back piece simply is not there —
# the seat panel fills it.
SEAT_TOP_FRAC = 0.74            # of the back rise above the crotch
SEAT_TOP_Y = CROTCH_Y + (SIDE_WAIST_Y + seat_rise_extra - CROTCH_Y) * SEAT_TOP_FRAC
# The panel top must finish BELOW the band's lower edge, or there is no rise left
# for the strap to span and the strap collapses onto its floor. Held clear by a
# strap's own width plus a working margin.
SEAT_TOP_Y = min(SEAT_TOP_Y, SIDE_WAIST_Y - (strap_width + 55.0))
SEAT_HALF_W = QUARTER_HIP * 0.78


def build_front():
    """Jumpsuit front (cut 2 mirrored): bodice and leg in one, shortened rise.

    The front is a normal jumpsuit front. All the adaptive geometry lives on the
    back and in the panel; the front's only job here is to present a side edge
    the back can be solved against, and a crotch point the panel hinges on.
    """
    p_hem_in = fc.P(0.0, 0.0)
    p_hem_out = fc.P(HEM_Q, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, SIDE_WAIST_Y)
    p_top_side = fc.P(QUARTER_CHEST, BAND_TOP_Y)
    p_top_cf = fc.P(0.0, BAND_TOP_Y)
    p_crotch = fc.P(-QUARTER_HIP * 0.22, CROTCH_Y)
    # Centre front runs from the crotch up to the top; the rise is SHORTENED, so
    # the CF waist point sits below the shared side-waist height.
    p_cf_waist = fc.P(0.0, CROTCH_Y + RISE_F)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_in, p_hem_out)]),
        fc.Edge("out_leg", [_leg_side(p_hem_out, p_waist_side)]),
        fc.Edge("side", [fc.Line(p_waist_side, p_top_side)]),
        fc.Edge("shoulder_top", [fc.Line(p_top_side, p_top_cf)]),
        fc.Edge("cf", [fc.Bezier(p_top_cf,
                                 fc.P(0.0, p_cf_waist.y + 40.0),
                                 fc.P(p_crotch.x * 0.35, p_cf_waist.y - 30.0),
                                 p_crotch)]),
        fc.Edge("inseam", [_inseam(p_hem_in, p_crotch).reversed()]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 34.0},
        notches=[fc.Notch("out_leg", 0.55, "knee level"),
                 fc.Notch("side", 0.0, "shared side-waist point"),
                 fc.Notch("inseam", 0.50, "inseam match")],
        grainline=fc.Grainline(fc.P(HEM_Q * 0.7, 50.0),
                               fc.P(HEM_Q * 0.7, CROTCH_Y - 60.0)),
        internals=[
            fc.Internal("waist-line",
                        [fc.P(0.0, p_cf_waist.y),
                         fc.P(QUARTER_WAIST - 12.0, SIDE_WAIST_Y)],
                        kind="marking"),
            # The front crotch: where the drop panel stays hinged. It never
            # detaches here, which is why the panel cannot be dropped or lost.
            fc.Internal("panel-hinge",
                        [fc.P(p_crotch.x, CROTCH_Y), fc.P(0.0, CROTCH_Y)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Jumpsuit front (shortened rise)",
    )


_F = build_front()
FRONT_SIDE_LEN = _F.edge("side").length(0.2)
FRONT_OUTLEG_LEN = _F.edge("out_leg").length(0.2)


# ── Solve the back's hem half-width so the outer leg edges MATCH ─────────────
# The back is wider at the hip (it carries the seat) and its rise is longer, so
# its outer-leg edge is not automatically the front's. That edge is the seam the
# whole garment hangs from. BISECT the back's hem half-width until the measured
# edges agree.
#
# Note the same non-monotonicity as the base-layer cartridge: this length falls
# to a minimum where the hem point sits below the waist point and rises on either
# side, so the minimum is located FIRST and the bisection then runs on the single
# monotone branch that can reach the target. A naive bracket across the minimum
# has the same sign at both ends and would silently return an endpoint.
BACK_WAIST_X = QUARTER_WAIST + 14.0     # the back takes a little more waist


def _back_out_leg(hem_half):
    return _leg_side(fc.P(hem_half, 0.0), fc.P(BACK_WAIST_X, SIDE_WAIST_Y))


def _solve_back_hem_half():
    """Bisect the back hem half-width until its outer leg equals the front's."""
    def f(x):
        return _back_out_leg(x).length(0.2) - FRONT_OUTLEG_LEN
    x_min = BACK_WAIST_X                 # near-vertical edge: the minimum
    if f(x_min) >= 0.0:
        return x_min                     # target at/below the minimum
    lo = x_min
    for _ in range(80):
        lo *= 0.95
        if f(lo) > 0.0:
            break
        if lo < 1.0:
            break
    if f(lo) <= 0.0:
        hi = x_min
        for _ in range(80):
            hi *= 1.05
            if f(hi) > 0.0:
                break
        if f(hi) <= 0.0:
            return x_min
        lo, hi = x_min, hi
    else:
        hi = x_min
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


HEM_Q_BACK = _solve_back_hem_half()


def build_back():
    """Jumpsuit back (cut 2 mirrored): lengthened rise, SEAT CUT AWAY.

    The back stops at the seat opening. Its centre-back edge runs from the top
    down to SEAT_TOP_Y and then turns out along the opening's top edge to the
    inner leg — the hole that shape leaves is what the drop panel fills.
    """
    p_hem_in = fc.P(0.0, 0.0)
    p_hem_out = fc.P(HEM_Q_BACK, 0.0)
    # The BODICE side seam runs between the two points the front also uses — the
    # shared side-waist point and the top corner — so it is equal to the front's
    # by construction. The back's extra hip width lives only on the outer LEG
    # edge below the waist, where the bisection can still reach it.
    p_waist_side = fc.P(QUARTER_WAIST, SIDE_WAIST_Y)
    p_leg_waist = fc.P(BACK_WAIST_X, SIDE_WAIST_Y)
    p_top_side = fc.P(QUARTER_CHEST, BAND_TOP_Y)
    p_top_cb = fc.P(0.0, BAND_TOP_Y)
    # CB comes down to the seat opening's top, NOT to the crotch.
    p_seat_top_cb = fc.P(0.0, SEAT_TOP_Y)
    p_seat_out = fc.P(SEAT_HALF_W, CROTCH_Y + 40.0)
    p_crotch_in = fc.P(-QUARTER_HIP * 0.10, CROTCH_Y)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_in, p_hem_out)]),
        fc.Edge("out_leg", [_back_out_leg(HEM_Q_BACK)]),
        # The hip step: the back's outer leg finishes wider than the shared
        # side-waist point, so this short edge brings it back in. It is a dart
        # taken at the waist in all but name, and it is what lets the bodice side
        # seam be equal to the front's while the leg still carries a wider hip.
        fc.Edge("hip_step", [fc.Line(p_leg_waist, p_waist_side)]),
        fc.Edge("side", [fc.Line(p_waist_side, p_top_side)]),
        fc.Edge("shoulder_top", [fc.Line(p_top_side, p_top_cb)]),
        fc.Edge("cb", [fc.Line(p_top_cb, p_seat_top_cb)]),
        # The seat opening's edge: from CB out and down to the inner leg. This is
        # one half of the seam the drop panel closes.
        fc.Edge("seat_opening", [fc.Bezier(p_seat_top_cb,
                                           fc.P(SEAT_HALF_W * 0.52, SEAT_TOP_Y - 20.0),
                                           fc.P(SEAT_HALF_W * 0.92, CROTCH_Y + 130.0),
                                           p_seat_out),
                                 fc.Bezier(p_seat_out,
                                           fc.P(SEAT_HALF_W * 0.58, CROTCH_Y + 8.0),
                                           fc.P(SEAT_HALF_W * 0.20, CROTCH_Y + 2.0),
                                           p_crotch_in)]),
        fc.Edge("inseam", [_inseam(p_hem_in, p_crotch_in).reversed()]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 34.0, "seat_opening": 16.0},
        notches=[fc.Notch("out_leg", 0.55, "knee level"),
                 fc.Notch("side", 0.0, "shared side-waist point"),
                 fc.Notch("seat_opening", 0.5, "panel edge match"),
                 fc.Notch("inseam", 0.50, "inseam match")],
        grainline=fc.Grainline(fc.P(HEM_Q_BACK * 0.7, 50.0),
                               fc.P(HEM_Q_BACK * 0.7, CROTCH_Y - 60.0)),
        internals=[
            fc.Internal("waist-line",
                        [fc.P(0.0, CROTCH_Y + RISE_B),
                         fc.P(BACK_WAIST_X - 12.0, SIDE_WAIST_Y)],
                        kind="marking"),
            # Where the ring strap lands on the band above this point.
            fc.Internal("ring-column",
                        [fc.P(SEAT_HALF_W * 0.55, SEAT_TOP_Y),
                         fc.P(SEAT_HALF_W * 0.55, SEAT_TOP_Y + 60.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Jumpsuit back (lengthened rise, seat cut away)",
    )


_B = build_back()
BACK_SIDE_LEN = _B.edge("side").length(0.2)
BACK_OUTLEG_LEN = _B.edge("out_leg").length(0.2)
# The opening the panel must fill: the back's seat_opening edge, taken TWICE
# because the back is cut as a mirrored pair and the panel spans both halves.
OPENING_RUN = 2.0 * _B.edge("seat_opening").length(0.2)


def build_seat():
    """The drop panel, cut 1 on fold at centre front of the crotch.

    Drafted as ONE half over the same span the back's opening covers, with its
    `hinge` edge on the fold: the cut piece is the mirrored pair, which is why
    the opening is counted twice above. Its `attach` edge is solved to measure
    the back's opening edge by BISECTING the panel's own bulge, because a drop
    seat drafted as a rectangle against a curved rise always comes up short.
    """
    # The panel spans from the front crotch hinge back and up to the ring corners.
    span = SEAT_HALF_W
    top = SEAT_TOP_Y - CROTCH_Y          # panel height above the hinge line
    p_hinge_cf = fc.P(0.0, 0.0)
    p_hinge_out = fc.P(span, 20.0)
    p_top_out = fc.P(span * 0.96, top)
    p_top_cf = fc.P(0.0, top + 12.0)

    target = OPENING_RUN / 2.0           # one half-panel matches one half-opening

    def attach_edge(bulge):
        """The panel's attached edge, hinge-out corner up to the top corner.

        Bowed OUTWARD (side=-1), away from centre front: the panel has to carry
        the volume of a seat, and an inward bow would scoop that volume out while
        still measuring the right length — a panel that matches the opening on
        paper and has no seat in it.
        """
        return fc.curve_through(p_hinge_out, p_top_out, bulge=bulge, side=-1.0)

    # Bisect the bulge until the MEASURED attach edge equals the measured opening
    # half. Bulge raises length monotonically, so the bracket always contains it.
    lo, hi = 0.0, 3.2
    def f(b):
        return attach_edge(b).length(0.2) - target
    f_lo, f_hi = f(lo), f(hi)
    if f_lo * f_hi > 0.0:
        bulge = lo if abs(f_lo) < abs(f_hi) else hi
    else:
        for _ in range(90):
            mid = (lo + hi) / 2.0
            f_mid = f(mid)
            if abs(f_mid) < 0.02:
                lo = hi = mid
                break
            if f_lo * f_mid <= 0.0:
                hi, f_hi = mid, f_mid
            else:
                lo, f_lo = mid, f_mid
        bulge = (lo + hi) / 2.0

    edges = [
        fc.Edge("hinge", [fc.Line(p_hinge_cf, p_hinge_out)]),
        fc.Edge("attach", [attach_edge(bulge)]),
        fc.Edge("panel_top", [fc.Line(p_top_out, p_top_cf)]),
        fc.Edge("cf_fold", [fc.Line(p_top_cf, p_hinge_cf)]),
    ]
    return fc.Piece(
        "seat", edges,
        seam_allowance=seam_allowance,
        allowances={"cf_fold": 0.0, "hinge": 0.0, "panel_top": 18.0},
        notches=[fc.Notch("attach", 0.5, "back opening match"),
                 fc.Notch("panel_top", 0.25, "strap corner")],
        grainline=fc.Grainline(fc.P(span * 0.45, 30.0), fc.P(span * 0.45, top - 25.0)),
        internals=[
            fc.Internal("strap-anchor",
                        [fc.P(span * 0.62, top - 14.0),
                         fc.P(span * 0.62 + strap_width, top - 14.0)],
                        kind="drill"),
            fc.Internal("hinge-line",
                        [fc.P(0.0, 0.0), fc.P(span, 20.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Drop seat panel (hinged at front crotch)",
    )


_SEAT = build_seat()
PANEL_ATTACH = 2.0 * _SEAT.edge("attach").length(0.2)

# ── Solve the strap length from the MEASURED rise difference ─────────────────
# The strap runs from the panel's top corner up to its ring on the waistband. Its
# length is the vertical gap between the panel's top and the band, taken from the
# built geometry, plus enough to wrap the ring and be sewn back on itself. NOT
# from a rise formula — the rise is the one thing that has just been tilted.
PANEL_TOP_ABS_Y = CROTCH_Y + (SEAT_TOP_Y - CROTCH_Y)
BAND_LOWER_Y = SIDE_WAIST_Y
STRAP_RISE = max(40.0, BAND_LOWER_Y - PANEL_TOP_ABS_Y)
RING_WRAP = strap_width * 2.2 + 30.0
STRAP_LEN = STRAP_RISE + RING_WRAP + 60.0    # +60: adjustment range at the ring

BAND_H = 62.0
# The band wraps the whole waist: four quarter-waists plus a CF overlap.
BAND_RUN = 4.0 * QUARTER_WAIST
BAND_OVERLAP = 70.0


def build_band():
    """The waistband (cut 1 on fold at its lower edge), carrying both rings.

    Drafted at the MEASURED waist run rather than at waist_girth: the pieces have
    ease in them, and a band cut to the body measurement would not reach.
    """
    ln = BAND_RUN + BAND_OVERLAP
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, BAND_H)
    p3 = fc.P(0.0, BAND_H)
    edges = [
        fc.Edge("lower", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("fold", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    # The two ring anchors, placed symmetrically about centre BACK. Centre back
    # is at the band's midpoint; the rings sit either side of it at the same
    # offset the panel's strap corners sit at, so both straps pull straight up.
    cb = BAND_RUN / 2.0
    off = SEAT_HALF_W * 0.62
    internals = [
        fc.Internal("centre-back", [fc.P(cb, 0.0), fc.P(cb, BAND_H)], kind="marking"),
        fc.Internal("ring-anchor-l",
                    [fc.P(cb - off - strap_width / 2.0, BAND_H * 0.5),
                     fc.P(cb - off + strap_width / 2.0, BAND_H * 0.5)],
                    kind="drill"),
        fc.Internal("ring-anchor-r",
                    [fc.P(cb + off - strap_width / 2.0, BAND_H * 0.5),
                     fc.P(cb + off + strap_width / 2.0, BAND_H * 0.5)],
                    kind="drill"),
        fc.Internal("elastic-channel",
                    [fc.P(cb - BAND_RUN * 0.22, BAND_H * 0.78),
                     fc.P(cb + BAND_RUN * 0.22, BAND_H * 0.78)],
                    kind="marking"),
    ]
    return fc.Piece(
        "band", edges,
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("lower", 0.25, "side seam match"),
                 fc.Notch("lower", 0.50, "centre back"),
                 fc.Notch("lower", 0.75, "side seam match")],
        grainline=fc.Grainline(fc.P(30.0, BAND_H / 2.0), fc.P(ln - 30.0, BAND_H / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="fold"),
        label="Waistband (carries both D-ring anchors)",
    )


def build_strap():
    """The strap facing (cut 2): panel corner up to the ring, at the SOLVED length.

    Cut in the shell fabric and bagged over webbing — a raw webbing strap against
    the small of the back on a body that sits on it all day is an abrasion.
    """
    w = strap_width
    ln = STRAP_LEN
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, w)
    p3 = fc.P(0.0, w)
    edges = [
        fc.Edge("lower", [fc.Line(p0, p1)]),
        fc.Edge("end_ring", [fc.Line(p1, p2)]),
        fc.Edge("upper", [fc.Line(p2, p3)]),
        fc.Edge("end_panel", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "strap", edges,
        seam_allowance=seam_allowance,
        allowances={"end_panel": 0.0, "end_ring": 20.0},
        notches=[fc.Notch("lower", 0.0, "panel corner"),
                 fc.Notch("lower", min(0.97, STRAP_RISE / ln), "band level")],
        grainline=fc.Grainline(fc.P(25.0, w / 2.0), fc.P(ln - 25.0, w / 2.0)),
        internals=[
            fc.Internal("ring-wrap-fold",
                        [fc.P(ln - RING_WRAP, 0.0), fc.P(ln - RING_WRAP, w)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Ring strap facing",
    )


def build():
    pattern = fc.PatternSet("drop-back-jumpsuit")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "seat":
        pattern.add(build_seat())
    if everything or target_piece == "band":
        pattern.add(build_band())
    if everything or target_piece == "strap":
        pattern.add(build_strap())

    if everything:
        # The seam the whole garment hangs from: shared side-waist point, so
        # these must be equal by construction.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=0.5)
        # The outer legs: the target of the hem-width bisection.
        pattern.declare_seam(("front", "out_leg"), ("back", "out_leg"), tol=1.0)
        # Inseams sew closed conventionally.
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=6.0)
        # THE drop-seat check: the panel's attached edge (×2, cut on fold) must
        # measure the opening the back leaves (×2, cut mirrored).
        pattern.declare_seam([("seat", "attach"), ("seat", "attach")],
                             [("back", "seat_opening"), ("back", "seat_opening")],
                             tol=1.5)
        # The band takes all four side-waist runs plus its overlap.
        pattern.declare_seam(("band", "lower"),
                             [("front", "side"), ("front", "side"),
                              ("back", "side"), ("back", "side")],
                             tol=2.0,
                             ease=BAND_RUN + BAND_OVERLAP
                                  - 2.0 * (FRONT_SIDE_LEN + BACK_SIDE_LEN))

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton/elastane twill, 240 gsm", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker. A little elastane is not for fit, "
                 "it is so the seat panel does not fight the transfer."},
        {"item": "D-ring", "qty": 2, "unit": "count",
         "note": f"Yantra4D d-ring (notion.hardware_ref), bar for {strap_width:.0f} mm "
                 f"webbing — the same strap_width this pattern cuts the strap at."},
        {"item": "webbing", "qty": round(2.0 * STRAP_LEN), "unit": "mm_length",
         "note": f"{strap_width:.0f} mm, {STRAP_LEN:.0f} mm per strap, bagged inside "
                 f"the shell-fabric facing — raw webbing against the small of the "
                 f"back abrades a body that sits on it all day."},
        {"item": "waistband elastic", "qty": round(BAND_RUN * 0.45), "unit": "mm_length",
         "note": "in the FRONT half of the band only; the back half must stay flat "
                 "and stable, because it is what the two rings pull against."},
        {"item": "thread", "qty": 2, "unit": "spool",
         "note": "box-and-cross both ring anchors and both panel corners — four "
                 "points carry the entire weight of the dropped panel."},
    ]
    pattern.metadata = {
        "fc300_rank": 251,
        "family": "adaptive",
        "fabric_hint": "mezclilla-denim",
        "finished_mm": {
            "inseam": round(inseam_length, 1),
            "front_rise": round(RISE_F, 1),
            "back_rise": round(RISE_B, 1),
            "bodice_length": round(bodice_length, 1),
            "hem_width_front": round(HEM_Q * 2.0, 1),
            "hem_width_back": round(HEM_Q_BACK * 2.0, 1),
            "seat_panel_height": round(SEAT_TOP_Y - CROTCH_Y, 1),
        },
        "solved": {
            "front_side_mm": round(FRONT_SIDE_LEN, 2),
            "back_side_mm": round(BACK_SIDE_LEN, 2),
            "side_delta_mm": round(BACK_SIDE_LEN - FRONT_SIDE_LEN, 3),
            "front_out_leg_mm": round(FRONT_OUTLEG_LEN, 2),
            "back_out_leg_mm": round(BACK_OUTLEG_LEN, 2),
            "out_leg_delta_mm": round(BACK_OUTLEG_LEN - FRONT_OUTLEG_LEN, 3),
            "back_hem_half_solved_mm": round(HEM_Q_BACK, 2),
            "seat_opening_run_mm": round(OPENING_RUN, 2),
            "panel_attach_run_mm": round(PANEL_ATTACH, 2),
            "panel_delta_mm": round(PANEL_ATTACH - OPENING_RUN, 3),
            "strap_rise_measured_mm": round(STRAP_RISE, 2),
            "strap_length_mm": round(STRAP_LEN, 2),
            "band_run_mm": round(BAND_RUN + BAND_OVERLAP, 2),
            "note": "the seated rise tilt is taken at CF/CB, never at the side, so front "
                    "and back SHARE one side-waist point — applying it at the side too "
                    "would make the two side edges differ by the full seat_rise_extra and "
                    "no hem width could close them. The back hem half-width is then "
                    "BISECTED (on the monotone branch below the length minimum) so the "
                    "outer legs measure equal, and the panel's attach edge is bisected "
                    "against the MEASURED seat opening, because a drop seat drafted as a "
                    "rectangle against a curved rise always comes up short.",
        },
        "adaptive": {
            "independent_toileting": "unhook two D-rings and the whole seat drops forward "
                                     "between the legs; no standing, no undressing, no "
                                     "second person in the room",
            "panel_stays_attached": "the panel is hinged at the front crotch and never "
                                    "detaches, so it cannot be dropped, lost, or land on a "
                                    "wet floor — the failure mode of a detachable panel",
            "one_handed_rehook": "an upward pull against a ring that holds tension while "
                                 "the hand lets go",
            "seated_rise_extra_mm": round(seat_rise_extra, 1),
            "why_a_jumpsuit": "a one-piece is the warmest, tidiest, least-riding-up thing "
                              "a wheelchair user can wear, and normally the one that costs "
                              "the most time; this keeps the jumpsuit and removes the cost",
        },
        "hardware": "D-rings via Yantra4D (notion.hardware_ref -> d-ring); the ring's "
                    "webbing bar is driven by this jumpsuit's strap_width, which is also "
                    "the width the strap facing is cut at",
    }
    return pattern


result = build()

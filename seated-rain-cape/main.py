"""
Seated Rain Cape — Fashion Cabinet Garment Cartridge (FC-300 #247, adaptive II).

A rain cape cut for a body that is sitting down. A standing cape hangs from the
shoulders and falls to a hem that is level all round; on a wheelchair user the same
cape rides up over the thighs, leaves the knees bare in the rain, and pools a long
tail of wet fabric under the seat where it drags into the wheels. This one inverts
that: the FRONT is long enough to fall over the knees to the footplate, the BACK is
cut short to clear the seat and the push rims entirely, and the two are joined by a
side panel that transitions between the two lengths without a step in the hem.

The closure is a webbing chest strap on a side-release buckle — one hand, one click,
no overhead motion. The buckle SOLID is Yantra4D territory (`side-release-buckle`;
see the manifest's notion.hardware_ref).

The drafting problem: a cape is a partial annulus. The neck edge and the hem are
concentric arcs, and the panel angles must sum to a full turn (less the front
opening) or the cape will not close on the body. The neck RADIUS is solved from the
measured neck girth and the swept angle, and the three panels' angles are solved to
fill exactly the remaining turn — measured, then checked as declared seams.

Pieces:
  - front : the long front panel (cut 2 mirrored), knee-length, with the opening edge.
  - side  : the transition panel (cut 2 mirrored), hem stepping front-length to back.
  - back  : the short back panel (cut 1 on fold at CB), clear of the seat.
  - hood  : a two-piece hood half (cut 2 mirrored), drafted to the measured neckline.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|side|back|hood|set

neck_girth = float(PARAM(lambda: neck_girth, 420.0))
front_length = float(PARAM(lambda: front_length, 780.0))
back_length = float(PARAM(lambda: back_length, 420.0))
sweep_deg = float(PARAM(lambda: sweep_deg, 320.0))
strap_webbing = float(PARAM(lambda: strap_webbing, 25.0))
hood_height = float(PARAM(lambda: hood_height, 340.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
neck_girth = max(320.0, min(neck_girth, 560.0))
front_length = max(500.0, min(front_length, 1000.0))
back_length = max(260.0, min(back_length, 620.0))
sweep_deg = max(240.0, min(sweep_deg, 350.0))
strap_webbing = max(16.0, min(strap_webbing, 50.0))
hood_height = max(260.0, min(hood_height, 420.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

# The back must stay SHORTER than the front — that is the whole adaptive point.
back_length = min(back_length, front_length - 120.0)

ARC_SEGS = 40           # polygon resolution for every arc; measured, never assumed
NECK_EASE = 60.0        # a rain cape's neck rides over a coat collar

# ── Solve the neck radius from the swept angle ───────────────────────────────
# The cape's neck edge is an arc of `sweep_deg` at radius R_NECK. Its arc LENGTH
# must equal the eased neck girth, so R_NECK follows from the sweep, not the other
# way round. Solved against the MEASURED polygon arc (not R*theta), because every
# other length in this cartridge is measured the same way and the two must agree.
SWEEP = math.radians(sweep_deg)
NECK_TARGET = neck_girth + NECK_EASE


def _arc_pts(r, a0, a1, n=ARC_SEGS):
    """n+1 points along the arc from a0 to a1 (radians) at radius r about origin."""
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _pts_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _solve_neck_radius():
    """Bisect the neck radius until the MEASURED polygon arc equals NECK_TARGET.

    Arc length is exactly linear in radius at fixed sweep, so this converges in a
    handful of steps; bisecting rather than dividing keeps the measured-polygon
    convention consistent with every other length here.
    """
    lo, hi = 10.0, 400.0
    def f(r):
        return _pts_len(_arc_pts(r, 0.0, SWEEP)) - NECK_TARGET
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if f(mid) > 0.0:
            hi = mid
        else:
            lo = mid
        if hi - lo < 1e-6:
            break
    return (lo + hi) / 2.0


R_NECK = _solve_neck_radius()
NECK_ARC = _pts_len(_arc_pts(R_NECK, 0.0, SWEEP))

# ── Solve the panel angle split ──────────────────────────────────────────────
# The swept angle is divided among four fronts... no: two fronts, two sides, one
# back-on-fold (which is two half-backs). Angles are apportioned by the share of
# the body each panel covers, then the LAST share is taken as the remainder so the
# four sum to SWEEP exactly rather than to SWEEP ± rounding.
SHARE_FRONT = 0.30      # each front panel: the long, knee-covering half
SHARE_SIDE = 0.13       # each side panel: the hem transition
ANG_FRONT = SWEEP * SHARE_FRONT
ANG_SIDE = SWEEP * SHARE_SIDE
ANG_BACK_HALF = SWEEP / 2.0 - ANG_FRONT - ANG_SIDE   # remainder — closes the turn
if ANG_BACK_HALF < math.radians(6.0):
    # Degenerate share: fall back to an even split so the back keeps real width.
    ANG_FRONT = SWEEP * 0.26
    ANG_SIDE = SWEEP * 0.10
    ANG_BACK_HALF = SWEEP / 2.0 - ANG_FRONT - ANG_SIDE
ANG_TOTAL = 2.0 * (ANG_FRONT + ANG_SIDE + ANG_BACK_HALF)

R_FRONT = R_NECK + front_length
R_BACK = R_NECK + back_length


def _panel(name, a0, a1, r_hem_start, r_hem_end, label, cut, extra_internals=None,
           notches=None):
    """One annulus panel between angles a0..a1, whose hem radius ramps from
    r_hem_start at a0 to r_hem_end at a1.

    A ramping hem radius is what lets the side panel step from front length to
    back length without a notch in the finished hem. Edges: neck (inner arc),
    seam_b (radial), hem (outer, reversed), seam_a (radial).
    """
    neck = _arc_pts(R_NECK, a0, a1)
    hem = []
    for i in range(ARC_SEGS + 1):
        t = i / ARC_SEGS
        a = a0 + (a1 - a0) * t
        r = r_hem_start + (r_hem_end - r_hem_start) * t
        hem.append(fc.P(r * math.cos(a), r * math.sin(a)))
    edges = [
        fc.Edge("neck", [fc.Line(neck[i], neck[i + 1]) for i in range(ARC_SEGS)]),
        fc.Edge("seam_b", [fc.Line(neck[-1], hem[-1])]),
        fc.Edge("hem", [fc.Line(hem[i + 1], hem[i]) for i in reversed(range(ARC_SEGS))]),
        fc.Edge("seam_a", [fc.Line(hem[0], neck[0])]),
    ]
    mid_a = (a0 + a1) / 2.0
    grain = fc.Grainline(
        fc.P((R_NECK + 30.0) * math.cos(mid_a), (R_NECK + 30.0) * math.sin(mid_a)),
        fc.P((min(r_hem_start, r_hem_end) - 30.0) * math.cos(mid_a),
             (min(r_hem_start, r_hem_end) - 30.0) * math.sin(mid_a)))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 25.0},
        notches=notches or [fc.Notch("neck", 0.5, "panel centre")],
        grainline=grain,
        internals=list(extra_internals or []),
        cut=cut,
        label=label,
    )


def build_front():
    """The long front panel (cut 2 mirrored). Its seam_a is the cape's front
    opening edge; the chest strap crosses from one front to the other."""
    a0 = 0.0
    a1 = ANG_FRONT
    # Chest-strap anchor: a webbing tab at chest height on the opening edge.
    strap_r = R_NECK + 190.0
    tab = [fc.P(strap_r * math.cos(a0 + 0.012), strap_r * math.sin(a0 + 0.012)),
           fc.P((strap_r + strap_webbing) * math.cos(a0 + 0.012),
                (strap_r + strap_webbing) * math.sin(a0 + 0.012))]
    internals = [
        fc.Internal("strap-anchor", tab, kind="drill"),
        # Hand-slit: a vertical opening so a hand can reach the push rim without
        # lifting the whole cape. Marked, cut by the maker.
        fc.Internal("hand-slit",
                    [fc.P((R_NECK + 300.0) * math.cos(a1 * 0.75),
                          (R_NECK + 300.0) * math.sin(a1 * 0.75)),
                     fc.P((R_NECK + 470.0) * math.cos(a1 * 0.75),
                          (R_NECK + 470.0) * math.sin(a1 * 0.75))],
                    kind="marking"),
    ]
    return _panel("front", a0, a1, R_FRONT, R_FRONT,
                  "Front panel (knee length)",
                  fc.CutSpec(quantity=2, mirror=True),
                  internals,
                  notches=[fc.Notch("neck", 0.5, "front panel centre"),
                           fc.Notch("hem", 0.5, "knee level")])


def build_side():
    """The transition panel (cut 2 mirrored): hem radius ramps from the front's
    down to the back's, so the finished hem sweeps up without a step."""
    a0 = ANG_FRONT
    a1 = ANG_FRONT + ANG_SIDE
    internals = [
        fc.Internal("wheel-clearance",
                    [fc.P(R_BACK * math.cos(a1), R_BACK * math.sin(a1)),
                     fc.P(R_FRONT * math.cos(a0), R_FRONT * math.sin(a0))],
                    kind="marking"),
    ]
    return _panel("side", a0, a1, R_FRONT, R_BACK,
                  "Side panel (hem transition)",
                  fc.CutSpec(quantity=2, mirror=True),
                  internals,
                  notches=[fc.Notch("neck", 0.0, "front panel join"),
                           fc.Notch("neck", 1.0, "back panel join")])


def build_back():
    """The short back panel, cut 1 on fold at centre back.

    Drafted as ONE half-back over ANG_BACK_HALF with seam_a as the fold: the cut
    piece is the mirrored pair, which is why the back's neck arc counts twice in
    the neckline seam check.
    """
    a0 = ANG_FRONT + ANG_SIDE
    a1 = a0 + ANG_BACK_HALF
    internals = [
        fc.Internal("seat-clearance-line",
                    [fc.P(R_BACK * math.cos(a0), R_BACK * math.sin(a0)),
                     fc.P(R_BACK * math.cos(a1), R_BACK * math.sin(a1))],
                    kind="marking"),
    ]
    piece = _panel("back", a0, a1, R_BACK, R_BACK,
                   "Back panel (seat clearance)",
                   fc.CutSpec(quantity=1, on_fold=True, fold_edge="seam_b"),
                   internals,
                   notches=[fc.Notch("neck", 1.0, "centre back fold")])
    return piece


# The full measured neckline: two fronts + two sides + two half-backs.
_F, _S, _B = build_front(), build_side(), build_back()
NECKLINE = (2.0 * _F.edge("neck").length(0.2)
            + 2.0 * _S.edge("neck").length(0.2)
            + 2.0 * _B.edge("neck").length(0.2))


def build_hood():
    """A hood half (cut 2 mirrored), drafted to the MEASURED neckline.

    Its neck edge takes half the neckline less the front opening allowance, so the
    two halves together match what the cape actually presents — a hood cut to a
    neck-girth formula is the classic source of a hood that will not sit down.
    """
    # Each half hood covers half the neckline, minus the front opening the hood
    # does not cross (the cape opens at the front; the hood meets it there).
    neck_run = NECKLINE / 2.0 - strap_webbing
    h = hood_height
    depth = neck_run * 0.92

    p_front_low = fc.P(0.0, 0.0)
    p_back_low = fc.P(depth, 0.0)
    p_back_top = fc.P(depth - 30.0, h)
    p_front_top = fc.P(0.0, h - 60.0)

    # The neck edge is drafted as a curve whose MEASURED length is solved to
    # neck_run by bisecting its bulge — a straight neck edge of length `depth`
    # would be short, and a hood short at the neck strangles.
    def neck_edge(bulge):
        return fc.curve_through(p_front_low, p_back_low, bulge=bulge, side=-1.0)

    lo, hi = 0.0, 0.9
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if neck_edge(mid).length(0.2) > neck_run:
            hi = mid
        else:
            lo = mid
        if hi - lo < 1e-7:
            break
    bulge = (lo + hi) / 2.0

    edges = [
        fc.Edge("hood_neck", [neck_edge(bulge)]),
        fc.Edge("back_seam", [fc.Line(p_back_low, p_back_top)]),
        # The crown: the seam that joins the two hood halves over the head.
        fc.Edge("crown", [fc.Bezier(p_back_top,
                                    fc.P(depth * 0.62, h + 34.0),
                                    fc.P(depth * 0.24, h + 20.0),
                                    p_front_top)]),
        fc.Edge("face_edge", [fc.Line(p_front_top, p_front_low)]),
    ]
    return fc.Piece(
        "hood", edges,
        seam_allowance=seam_allowance,
        allowances={"face_edge": 28.0},
        notches=[fc.Notch("hood_neck", 0.5, "shoulder match"),
                 fc.Notch("crown", 0.5, "crown centre")],
        grainline=fc.Grainline(fc.P(depth * 0.5, 30.0), fc.P(depth * 0.5, h - 30.0)),
        internals=[fc.Internal("drawcord-channel",
                               [fc.P(0.0 + 22.0, 20.0), fc.P(22.0, h - 70.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood half",
    )


def build():
    pattern = fc.PatternSet("seated-rain-cape")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "side":
        pattern.add(build_side())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "hood":
        pattern.add(build_hood())

    if everything:
        # Front joins side, side joins back — the radial seams of the annulus.
        pattern.declare_seam(("front", "seam_b"), ("side", "seam_a"), tol=1.5)
        pattern.declare_seam(("side", "seam_b"), ("back", "seam_a"), tol=1.5)
        # The hood takes the whole measured neckline, less the two front-opening
        # allowances the hood does not cross.
        pattern.declare_seam([("hood", "hood_neck"), ("hood", "hood_neck")],
                             [("front", "neck"), ("front", "neck"),
                              ("side", "neck"), ("side", "neck"),
                              ("back", "neck"), ("back", "neck")],
                             tol=1.5, ease=-2.0 * strap_webbing)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)   # radial panels nest poorly
    pattern.bom = [
        {"item": "coated ripstop nylon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 62% marker (radial panels nest poorly); "
                 "seam-seal every radial seam."},
        {"item": "side-release buckle", "qty": 1, "unit": "count",
         "note": f"Yantra4D side-release-buckle (notion.hardware_ref) for "
                 f"{strap_webbing:.0f} mm webbing; one-handed, one click, at chest height."},
        {"item": "webbing", "qty": round(neck_girth * 1.6), "unit": "mm_length",
         "note": f"{strap_webbing:.0f} mm chest strap plus both anchor tabs."},
        {"item": "hood drawcord", "qty": round(hood_height * 2.2), "unit": "mm_length",
         "note": "in the marked face channel; a cord lock is optional."},
        {"item": "reflective tape", "qty": round(NECKLINE * 1.2), "unit": "mm_length",
         "note": "along the back hem — the back is short and sits at driver eye height."},
    ]
    pattern.metadata = {
        "fc300_rank": 247,
        "family": "adaptive",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {
            "front_length": round(front_length, 1),
            "back_length": round(back_length, 1),
            "hem_drop": round(front_length - back_length, 1),
            "sweep_deg": round(sweep_deg, 1),
        },
        "solved": {
            "neck_radius_mm": round(R_NECK, 2),
            "neck_arc_measured_mm": round(NECK_ARC, 2),
            "neck_target_mm": round(NECK_TARGET, 2),
            "neckline_total_mm": round(NECKLINE, 2),
            "angles_deg": {
                "front": round(math.degrees(ANG_FRONT), 2),
                "side": round(math.degrees(ANG_SIDE), 2),
                "back_half": round(math.degrees(ANG_BACK_HALF), 2),
                "sum": round(math.degrees(ANG_TOTAL), 2),
                "sweep": round(sweep_deg, 2),
            },
            "note": "the neck radius is BISECTED until the measured 40-gon arc equals the "
                    "eased neck girth, and the back's half-angle is taken as the REMAINDER "
                    "of the sweep so the panel angles close the turn exactly.",
        },
        "adaptive": {
            "seated_geometry": "front falls to the footplate, back stops clear of the seat "
                               "and the push rims; the side panel ramps between the two hem "
                               "radii so the hem sweeps up with no step",
            "closure": "one-handed side-release buckle at chest height — no overhead motion",
            "hand_slit": "marked on each front so a hand reaches the push rim without "
                         "lifting the cape",
        },
        "hardware": "chest-strap buckle via Yantra4D (notion.hardware_ref -> "
                    "side-release-buckle); the buckle's webbing channel takes this cape's "
                    "strap_webbing",
    }
    return pattern


result = build()

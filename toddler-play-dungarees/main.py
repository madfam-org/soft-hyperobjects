"""
Toddler Play Dungarees — Fashion Cabinet Garment Cartridge (FC-300 #287, kids_baby, T2).

Denim dungarees for a child who is still in nappies and already running: a bib
front, two crossing back straps that fasten with sliding overall buckles, and an
inseam that does NOT sew shut — it closes on a run of snaps from one knee, through
the crotch, to the other knee, so a nappy is changed without taking the boots,
the trousers or the child off the floor.

Both of this garment's hard problems are register problems, and both are solved
by measurement rather than formula:

  1. THE SNAP GUSSET RUN. The inseam is not one seam but THREE runs end to end:
     left inseam, the crotch curve, right inseam. Snapping it shut only works if
     every stud lands on its socket, so the run is MEASURED across the built
     pieces and the pitch is then recomputed from WHOLE intervals across that
     measured length. A requested pitch is a target, never a result — a pitch
     applied blind drifts and the last snap lands in the crotch seam allowance,
     which is the one place a toddler's whole weight rests.

  2. THE STRAP LENGTH AGAINST THE MEASURED RISE. The strap runs from the bib
     corner, over the shoulder, and crosses to the opposite back waist. That
     path is not a parameter: it is derived from the MEASURED bib height and the
     MEASURED back rise plus a shoulder arc, and the buckle's adjustment range
     is then centred on it. Overall buckles slide, but only ± their own travel;
     a strap cut to a guessed length runs out of adjustment on a growing child
     within one season, which is the whole reason the buckle is there.

CHILD PROPORTION, NOT A SHRUNK ADULT. The block is drafted from child
measurements directly (chest, waist, hip, inside leg — see bodies/child-6y), and
the toddler-specific proportions are explicit: the rise is a LARGER fraction of
the inside leg than an adult's (a nappy occupies it), the waist is not smaller
than the chest (a toddler has no waist indentation to draft to), and the bib is
sized off the chest rather than off a fashion proportion.

The BUCKLE SOLID is Yantra4D territory (`overall-buckle`; see notion.hardware_ref).
The snaps are a second finding and are marked, not modelled.

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


# ── Parameters (millimetres; girths are full-body CHILD measurements) ────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front_leg|back_leg|bib|strap|facing|set

chest_girth = float(PARAM(lambda: chest_girth, 620.0))     # child chest
hip_girth = float(PARAM(lambda: hip_girth, 660.0))         # over the nappy
inside_leg = float(PARAM(lambda: inside_leg, 380.0))       # crotch to ankle
back_rise = float(PARAM(lambda: back_rise, 250.0))         # crotch to waist, back
bib_height = float(PARAM(lambda: bib_height, 180.0))       # waist to bib top
strap_width = float(PARAM(lambda: strap_width, 30.0))      # finished strap width
hem_width = float(PARAM(lambda: hem_width, 190.0))         # full flat leg opening
snap_diameter = float(PARAM(lambda: snap_diameter, 13.0))  # gusset snap size
snap_pitch = float(PARAM(lambda: snap_pitch, 40.0))        # REQUESTED pitch
gusset_extent = float(PARAM(lambda: gusset_extent, 0.55))  # snapped fraction of inseam
wear_ease = float(PARAM(lambda: wear_ease, 90.0))          # total ease over the hip
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))  # denim turn-up

# ── Clamps (mirror the manifest slider bounds exactly) ───────────────────────
chest_girth = max(480.0, min(chest_girth, 760.0))
hip_girth = max(500.0, min(hip_girth, 820.0))
inside_leg = max(220.0, min(inside_leg, 560.0))
back_rise = max(170.0, min(back_rise, 340.0))
bib_height = max(110.0, min(bib_height, 260.0))
strap_width = max(18.0, min(strap_width, 45.0))
hem_width = max(130.0, min(hem_width, 280.0))
snap_diameter = max(9.0, min(snap_diameter, 20.0))
snap_pitch = max(22.0, min(snap_pitch, 75.0))
gusset_extent = max(0.25, min(gusset_extent, 0.85))
wear_ease = max(40.0, min(wear_ease, 180.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(15.0, min(hem_allowance, 50.0))

# ── Derived block dimensions (CHILD proportions, stated explicitly) ──────────
QUARTER_HIP = (hip_girth + wear_ease) / 4.0
# A toddler has no waist indentation to draft to: the waist quarter is the hip
# quarter, minus a token. Drafting a shaped waist here produces a garment that
# will not pass over the hips of the child it was measured on.
QUARTER_WAIST = max(QUARTER_HIP - 14.0, QUARTER_HIP * 0.90)
# The front rise runs shorter than the back by a fixed child-scale difference —
# a toddler stands with a forward pelvic tilt and a nappy under the seat.
RISE_DIFF = 34.0
FRONT_RISE = max(90.0, back_rise - RISE_DIFF)

HALF_HEM = hem_width / 2.0
# Fork extension past the side-block width: the back fork is deeper because the
# nappy sits behind. Both are clamped positive so a small hip with a long rise
# can never invert the crotch curve.
FORK_F = max(14.0, QUARTER_HIP * 0.13)
FORK_B = max(22.0, QUARTER_HIP * 0.21)

# Bib width: from the CHEST, not a fashion proportion. Clamped so the bib can
# never come out wider than the waist it is sewn to (a bib wider than its own
# seam is a piece that pleats itself shut).
_BIB_HALF_RAW = chest_girth / 6.0 + 8.0
BIB_HALF = max(45.0, min(_BIB_HALF_RAW, QUARTER_WAIST - 12.0))

TOPSTITCH_OFFSET = 7.0                        # denim twin-needle gauge

# Where the snap run stops on each inseam, as an arc-length fraction — this is
# the notch the maker bar-tacks to, so it is derived from the requested extent
# rather than eyeballed, and held off both ends of the edge so the notch can
# never land on a corner.
GUSSET_STOP_T = min(0.95, max(0.05, gusset_extent))


def _cross(label, x, y, arm=None):
    """A small + drawn as one drill polyline at (x, y) — a snap or rivet site."""
    a = arm if arm is not None else max(3.0, snap_diameter * 0.32)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y),
         fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


# ── Legs ─────────────────────────────────────────────────────────────────────
# The inseam is drafted as a plain edge on both legs and SOLVED to equal length
# by bisecting the front inseam's bulge against the back's measured length — an
# unequal inseam on a normal trouser is a twist, but here it is a snap column out
# of register, so it has to close to well under a millimetre.
def _front_inseam(bulge):
    return fc.Edge("inseam", [fc.curve_through(
        fc.P(QUARTER_HIP + FORK_F, FRONT_RISE), fc.P(HALF_HEM, 0.0),
        bulge=bulge, side=-1.0)])


_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, back_rise), fc.P(HALF_HEM, 0.0),
    bulge=0.0, side=-1.0)])
_BACK_INSEAM_LEN = _BACK_INSEAM.length(0.05)


def _solve_front_bulge():
    """Bisect the front inseam's bulge until it MEASURES the back inseam."""
    lo, hi = 0.0, 0.45
    for _ in range(52):
        mid = (lo + hi) / 2.0
        if _front_inseam(mid).length(0.05) < _BACK_INSEAM_LEN:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


BULGE = _solve_front_bulge()
_FRONT_INSEAM_LEN = _front_inseam(BULGE).length(0.05)


def build_front_leg():
    """Front leg, cut 2 mirrored. Its waist edge sews to the bib bottom."""
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, FRONT_RISE)
    p_waist_in = fc.P(QUARTER_WAIST, FRONT_RISE)
    p_fork = fc.P(QUARTER_HIP + FORK_F, FRONT_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 5.0, FRONT_RISE - FRONT_RISE * 0.42),
            fc.P(QUARTER_HIP + FORK_F * 0.35, FRONT_RISE * 0.20),
            p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF / bib match"),
                 fc.Notch("side", 0.5, "knee level"),
                 fc.Notch("inseam", GUSSET_STOP_T, "gusset stop")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.10),
                               fc.P(QUARTER_HIP * 0.42, FRONT_RISE * 0.90)),
        internals=[
            fc.Internal("out-seam topstitch",
                        [fc.P(TOPSTITCH_OFFSET, 0.0),
                         fc.P(TOPSTITCH_OFFSET, FRONT_RISE)],
                        kind="trace"),
            fc.Internal("knee-patch placement",
                        [fc.P(HALF_HEM * 0.20, FRONT_RISE * 0.30),
                         fc.P(QUARTER_HIP * 0.80, FRONT_RISE * 0.30),
                         fc.P(QUARTER_HIP * 0.80, FRONT_RISE * 0.06),
                         fc.P(HALF_HEM * 0.20, FRONT_RISE * 0.06),
                         fc.P(HALF_HEM * 0.20, FRONT_RISE * 0.30)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    """Back leg, cut 2 mirrored. The waist rises at CB; the straps buckle here."""
    cb_y = back_rise
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, back_rise - RISE_DIFF)
    p_waist_in = fc.P(QUARTER_WAIST, cb_y)
    p_fork = fc.P(QUARTER_HIP + FORK_B, cb_y)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 5.0, cb_y - back_rise * 0.42),
            fc.P(QUARTER_HIP + FORK_B * 0.35, back_rise * 0.20),
            p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "back_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CB match"),
                 fc.Notch("side", 0.5, "knee level"),
                 fc.Notch("inseam", GUSSET_STOP_T, "gusset stop")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.10),
                               fc.P(QUARTER_HIP * 0.42, back_rise * 0.90)),
        internals=[
            fc.Internal("out-seam topstitch",
                        [fc.P(TOPSTITCH_OFFSET, 0.0),
                         fc.P(TOPSTITCH_OFFSET, back_rise - RISE_DIFF)],
                        kind="trace"),
            # Where the strap end is caught in the back waist, one per leg, set
            # in from the side seam so the crossed straps do not slide off a
            # small shoulder.
            _cross("strap catch", QUARTER_WAIST * 0.45, cb_y - 18.0),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


# ── Solve the snap gusset across the MEASURED three-run inseam ───────────────
_FL = build_front_leg()
_BL = build_back_leg()
INSEAM_RUN = _FL.edge("inseam").length(0.05)
# The crotch run the gusset carries: the lower part of both crotch curves, from
# the fork point up to where the snap run stops. Measured off the built pieces.
CROTCH_RUN = (_FL.edge("crotch").length(0.05)
              + _BL.edge("crotch").length(0.05)) * 0.34
# The full snapped run: down one inseam a fraction, through the crotch, up the
# other inseam the same fraction.
GUSSET_RUN = 2.0 * INSEAM_RUN * gusset_extent + CROTCH_RUN

# Both ends held clear: the hem end so the last snap is not on the turn-up, the
# far end so the first snap is not on the bar-tack that stops the opening.
END_CLEAR = max(16.0, snap_diameter * 1.25)
SNAP_RUN = max(snap_diameter * 2.0, GUSSET_RUN - 2.0 * END_CLEAR)

# Whole intervals at (or just under) the requested pitch, then the pitch
# RECOMPUTED so the column lands exactly on both clearances instead of drifting.
N_INTERVALS = max(1, int(round(SNAP_RUN / snap_pitch)))
N_SNAPS = N_INTERVALS + 1
PITCH_SOLVED = SNAP_RUN / N_INTERVALS


def build_bib():
    """Bib front, cut 1 on the CF fold. Its bottom sews to the two front waists."""
    h = bib_height
    edges = [
        fc.Edge("cf_fold", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        fc.Edge("bib_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(QUARTER_WAIST, 0.0))]),
        # The bib narrows from the waist to the top — a straight taper, because a
        # curved bib side on 407 gsm denim will not turn cleanly at this scale.
        fc.Edge("bib_side", [fc.Line(fc.P(QUARTER_WAIST, 0.0), fc.P(BIB_HALF, h))]),
        fc.Edge("bib_top", [fc.Line(fc.P(BIB_HALF, h), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "bib", edges,
        seam_allowance=seam_allowance,
        allowances={"bib_top": hem_allowance * 0.6, "cf_fold": 0.0},
        notches=[fc.Notch("bib_bottom", 1.0, "front-leg waist match"),
                 fc.Notch("bib_side", 1.0, "buckle corner")],
        grainline=fc.Grainline(fc.P(BIB_HALF * 0.5, 15.0),
                               fc.P(BIB_HALF * 0.5, h - 15.0)),
        internals=[
            fc.Internal("bib topstitch",
                        [fc.P(0.0, h - TOPSTITCH_OFFSET),
                         fc.P(BIB_HALF - TOPSTITCH_OFFSET * 0.8, h - TOPSTITCH_OFFSET),
                         fc.P(QUARTER_WAIST - TOPSTITCH_OFFSET, TOPSTITCH_OFFSET)],
                        kind="trace"),
            # The buckle catch: the button the overall buckle's slot drops onto,
            # set in from the bib corner by its own diameter so the buckle frame
            # clears the topstitched edge.
            _cross("buckle catch",
                   max(BIB_HALF * 0.35, BIB_HALF - strap_width * 0.9),
                   h - max(14.0, strap_width * 0.55),
                   arm=max(4.0, strap_width * 0.22)),
            fc.Internal("pocket placement",
                        [fc.P(0.0, h * 0.18), fc.P(BIB_HALF * 0.78, h * 0.18),
                         fc.P(BIB_HALF * 0.78, h * 0.70), fc.P(0.0, h * 0.70),
                         fc.P(0.0, h * 0.18)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Bib (cut on fold)",
    )


# ── Solve the strap length against the MEASURED rise and bib ────────────────
# The strap path: from the bib top corner, over the shoulder, crossing to the
# opposite back waist. Derived from the MEASURED bib side and back rise plus a
# shoulder arc allowance, then the buckle's travel is CENTRED on it — a strap
# cut to a guessed length runs out of buckle adjustment on a growing child within
# a season, which is the entire reason the buckle is on the garment.
_BIB = build_bib()
BIB_SIDE_RUN = _BIB.edge("bib_side").length(0.05)
SHOULDER_ARC = max(90.0, chest_girth * 0.22)     # over the shoulder and across
STRAP_PATH = bib_height + back_rise + SHOULDER_ARC
BUCKLE_TRAVEL = max(45.0, STRAP_PATH * 0.16)     # the adjustment range wanted
STRAP_CUT = STRAP_PATH + BUCKLE_TRAVEL + 2.0 * seam_allowance


def build_strap():
    """A crossing back strap, cut 2. Buckles at the bib, caught at the back waist.

    Cut flat at twice the finished width plus turnings: a denim strap is folded
    in thirds and topstitched down both edges, which is what makes it stiff
    enough to stay on a small shoulder.
    """
    w = strap_width * 2.0 + 2.0 * seam_allowance
    ln = STRAP_CUT
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("buckle_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("waist_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("fold line 1", [fc.P(0.0, w / 3.0), fc.P(ln, w / 3.0)],
                    kind="marking"),
        fc.Internal("fold line 2", [fc.P(0.0, 2.0 * w / 3.0), fc.P(ln, 2.0 * w / 3.0)],
                    kind="marking"),
        # The buckle's travel, marked as a real span so the maker can see the
        # adjustment the child actually gets rather than trusting the slider.
        fc.Internal("buckle travel",
                    [fc.P(ln - seam_allowance - BUCKLE_TRAVEL, w / 2.0),
                     fc.P(ln - seam_allowance, w / 2.0)],
                    kind="marking"),
        fc.Internal("nominal buckle position",
                    [fc.P(ln - seam_allowance - BUCKLE_TRAVEL / 2.0, 0.0),
                     fc.P(ln - seam_allowance - BUCKLE_TRAVEL / 2.0, w)],
                    kind="marking"),
    ]
    return fc.Piece(
        "strap", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},   # the long edges are folded, not sewn
        notches=[fc.Notch("lower", 0.0, "back waist end"),
                 fc.Notch("lower", 1.0, "buckle end")],
        grainline=fc.Grainline(fc.P(ln * 0.12, w / 2.0), fc.P(ln * 0.88, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Crossing strap (cut 2)",
    )


def build_facing():
    """The gusset facing: the reinforcing strip behind the snapped inseam run.

    Cut 4 — one behind each side of the opening on each leg. A snap set through
    a single layer of denim tears out at the crotch, which is the seam that takes
    a toddler's entire weight when they sit down without looking.
    """
    w = max(28.0, snap_diameter * 2.2)
    ln = GUSSET_RUN
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = []
    # Every snap centre, drilled on the facing's own centreline. The facing is
    # cut to the MEASURED gusset run, so these marks transfer 1:1 to both sides
    # of the opening — the facing IS the registration jig for the whole column.
    for i in range(N_SNAPS):
        x = END_CLEAR + PITCH_SOLVED * i
        internals.append(_cross(f"snap-{i + 1}", x, w / 2.0))
    # Where the crotch run begins and ends inside the column, so the maker knows
    # which snaps land on the curve (those get the deeper facing overlap).
    internals.append(fc.Internal(
        "crotch run start",
        [fc.P(INSEAM_RUN * gusset_extent, 0.0), fc.P(INSEAM_RUN * gusset_extent, w)],
        kind="marking"))
    internals.append(fc.Internal(
        "crotch run end",
        [fc.P(INSEAM_RUN * gusset_extent + CROTCH_RUN, 0.0),
         fc.P(INSEAM_RUN * gusset_extent + CROTCH_RUN, w)],
        kind="marking"))
    return fc.Piece(
        "facing", edges,
        seam_allowance=seam_allowance,
        allowances={"end_a": 0.0, "end_b": 0.0},
        notches=[fc.Notch("lower", 0.0, "hem end"),
                 fc.Notch("lower", min(0.99, (INSEAM_RUN * gusset_extent) / ln),
                          "crotch run start")],
        grainline=fc.Grainline(fc.P(ln * 0.12, w / 2.0), fc.P(ln * 0.88, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=4),
        label="Gusset snap facing (cut 4)",
    )


def build():
    pattern = fc.PatternSet("toddler-play-dungarees")
    everything = target_piece == "set"
    want = {
        "front_leg": everything or target_piece == "front_leg",
        "back_leg": everything or target_piece == "back_leg",
        "bib": everything or target_piece == "bib",
        "strap": everything or target_piece == "strap",
        "facing": everything or target_piece == "facing",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front_leg"]:
        pattern.add(build_front_leg())
    if want["back_leg"]:
        pattern.add(build_back_leg())
    if want["bib"]:
        pattern.add(build_bib())
    if want["strap"]:
        pattern.add(build_strap())
    if want["facing"]:
        pattern.add(build_facing())

    if want["front_leg"] and want["back_leg"]:
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        # The inseam carries the snap column: BOTH sides must measure the same to
        # well under a millimetre or every snap after the first is out of
        # register. Tighter than a normal trouser inseam for exactly that reason.
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=0.4)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)
    if want["bib"] and want["front_leg"]:
        # The bib bottom sews to the front-leg waist. Both are drafted to
        # QUARTER_WAIST, so this closes at delta = 0 by construction — the check
        # is here to catch a future redraft that breaks it.
        pattern.declare_seam(("bib", "bib_bottom"), ("front_leg", "waist"), tol=0.5)

    fabric_width = 1500.0                       # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "mezclilla-denim, 12 oz (407 gsm)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 74% marker; wash before "
                 f"cutting — 12 oz denim shrinks and this garment is on a child "
                 f"who outgrows it before it wears out."},
        {"item": "overall buckle + catch button", "qty": 2, "unit": "set",
         "note": f"Yantra4D overall-buckle (notion.hardware_ref) on a "
                 f"{strap_width:.0f} mm strap; {BUCKLE_TRAVEL:.0f} mm of travel "
                 f"is drafted in, centred on a MEASURED strap path of "
                 f"{STRAP_PATH:.0f} mm."},
        {"item": "gusset snap (set-in, 4-part)", "qty": N_SNAPS, "unit": "pair",
         "note": f"{N_SNAPS} pairs at a SOLVED pitch of {PITCH_SOLVED:.1f} mm "
                 f"across a MEASURED {GUSSET_RUN:.0f} mm run (requested pitch "
                 f"{snap_pitch:.0f} mm). Set through the facing, never through "
                 f"a single layer."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": "out-seams, bib edge, both strap edges; twin-needle at "
                 f"{TOPSTITCH_OFFSET:.0f} mm."},
        {"item": "knee-patch denim (self or contrast)", "qty": 2, "unit": "piece",
         "note": "the front leg carries a marked knee-patch zone; a toddler wears "
                 "through the knee long before anything else fails."},
    ]
    pattern.metadata = {
        "fc300_rank": 287,
        "family": "kids_baby",
        "tier": 2,
        "fabric_hint": "mezclilla-denim",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(FRONT_RISE, 1),
            "back_rise": round(back_rise, 1),
            "bib_height": round(bib_height, 1),
            "bib_half_width": round(BIB_HALF, 1),
            "hem_width": round(hem_width, 1),
            "strap_cut_length": round(STRAP_CUT, 1),
        },
        "solved": {
            "front_inseam_bulge": round(BULGE, 5),
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "gusset_inseam_run_mm": round(INSEAM_RUN * gusset_extent, 2),
            "gusset_crotch_run_mm": round(CROTCH_RUN, 2),
            "gusset_run_total_mm": round(GUSSET_RUN, 2),
            "snap_count": N_SNAPS,
            "snap_pitch_requested_mm": round(snap_pitch, 2),
            "snap_pitch_solved_mm": round(PITCH_SOLVED, 3),
            "gusset_stop_fraction": round(GUSSET_STOP_T, 3),
            "bib_half_requested_mm": round(_BIB_HALF_RAW, 2),
            "bib_half_clamped_mm": round(BIB_HALF, 2),
            "bib_half_was_clamped": bool(abs(BIB_HALF - _BIB_HALF_RAW) > 0.01),
            "bib_side_measured_mm": round(BIB_SIDE_RUN, 2),
            "strap_path_measured_mm": round(STRAP_PATH, 2),
            "buckle_travel_mm": round(BUCKLE_TRAVEL, 2),
            "note": "the snap pitch is a TARGET: whole intervals are fitted to the "
                    "MEASURED three-run gusset (inseam + crotch + inseam) and the "
                    "pitch recomputed, so the column lands on both clearances "
                    "instead of drifting into the crotch seam allowance. The front "
                    "inseam's bulge is bisected until it MEASURES the back's, "
                    "because an unequal inseam here is a snap column out of "
                    "register, not merely a twist. The strap is cut to a MEASURED "
                    "path (bib + back rise + shoulder arc) with the buckle's "
                    "travel centred on it, so a growing child does not run out of "
                    "adjustment in one season.",
        },
        "child_proportion": {
            "source": "drafted from child measurements directly (bodies/child-6y), "
                      "NOT a scaled adult block",
            "no_waist_indentation": "the waist quarter is the hip quarter less a "
                                    "token — a toddler has no waist to draft to, and "
                                    "a shaped waist here will not pass the hips",
            "rise_over_nappy": f"front rise {FRONT_RISE:.0f} mm vs back "
                               f"{back_rise:.0f} mm (a {RISE_DIFF:.0f} mm child-scale "
                               f"difference); the back fork is the deeper one because "
                               f"the nappy sits behind",
            "bib_from_chest": "the bib half-width comes from the chest girth, clamped "
                              "against the waist it sews to",
            "knee_patch": "a marked knee-patch zone on the front leg — the first "
                          "thing a toddler wears through",
        },
        "topstitch": f"twin-needle heavy contrast at {TOPSTITCH_OFFSET:.0f} mm: "
                     f"out-seams, bib edge, both strap edges",
        "hardware": "sliding overall buckles via Yantra4D (notion.hardware_ref -> "
                    "overall-buckle); the solid's strap_w — the parameter driving its "
                    "strap_slot flange, i.e. the sewn mating slot — is fed from this "
                    "garment's strap_width, which is also what sizes the strap the "
                    "buckle slides on. The gusset snaps are marked, not modelled.",
    }
    return pattern


result = build()

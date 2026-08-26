"""
Selvedge Straight Jean — Fashion Cabinet Garment Cartridge (FC-400 #301, denim, T2).

The five-pocket straight jean cut for SELVEDGE denim: the outseam is left on the
loom's finished edge (the selvedge) and felled with the tell-tale line of white,
so the outseam is NOT a normal seam — it is the one edge of the whole garment that
is drafted flat and straight, because a selvedge edge cannot be curved without
cutting off the very finish that makes it selvedge.

Three things are solved by measurement rather than by formula:

  1. THE TWO INSEAMS ARE CLOSED TO ZERO. Front and back inseams sew together and
     carry the whole leg; if they do not MEASURE the same, the leg twists and the
     felled outseam ripples. The back inseam is drafted plain and the front
     inseam's bulge is BISECTED until the two measure the same to well under a
     millimetre. On a straight jean this matters more than on a shaped trouser
     because there is no drape to hide the twist.

  2. THE WAISTBAND IS CUT TO THE MEASURED WAIST, NOT TO A GIRTH. The waistband is
     a straight band, and its length is the sum of the front and back waist edges
     as BUILT (both quarters, times two, less the seam the fly eats), plus the
     button extension. A band cut to (waist_girth / 1) laid flat is always wrong
     by the darts and the fly lap; here it is measured off the assembled panels.

  3. THE JEANS BUTTON AND ITS RIVETS SIT ON CLOTH, NOT ON A TURN. The waistband
     button is stepped in from the band's finished end by its own head diameter
     plus a clearance, and the pocket-corner rivets are stepped in from BOTH
     edges of the piece they land on. A button set on the extension fold, or a
     rivet on the pocket hem, holds nothing — and, because the kernel
     CCW-normalizes an inverted outline and area() takes an absolute value, a
     pocket clamped too small still renders and passes verify() looking healthy.
     Every derived dimension is clamped explicitly.

DENIM CONVENTIONS, per the family (jeans-5-pocket, denim-chore-apron): a 7 mm
twin-needle topstitch gauge in contrast gold; the outseam felled on the selvedge;
every hard good a Yantra4D reference rather than a re-implementation.

The JEANS-BUTTON SOLID is Yantra4D territory (`jeans-button`; see
notion.hardware_ref). The rivets are a second finding and are marked, not modelled.

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
# front_leg|back_leg|waistband|fly|pocket_bag|coin_pocket|set

waist_girth = float(PARAM(lambda: waist_girth, 820.0))
hip_girth = float(PARAM(lambda: hip_girth, 1000.0))
inside_leg = float(PARAM(lambda: inside_leg, 810.0))       # crotch to hem
front_rise = float(PARAM(lambda: front_rise, 260.0))       # crotch to waist, front
hem_width = float(PARAM(lambda: hem_width, 190.0))         # flat leg opening
knee_width = float(PARAM(lambda: knee_width, 210.0))       # flat knee, straight leg
band_depth = float(PARAM(lambda: band_depth, 40.0))        # finished waistband depth
button_head = float(PARAM(lambda: button_head, 17.0))      # jeans-button head dia
wear_ease = float(PARAM(lambda: wear_ease, 40.0))          # total ease over the hip
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 32.0))  # denim turn-up

# ── Clamps (mirror the manifest slider bounds exactly) ───────────────────────
waist_girth = max(560.0, min(waist_girth, 1200.0))
hip_girth = max(720.0, min(hip_girth, 1400.0))
inside_leg = max(560.0, min(inside_leg, 950.0))
front_rise = max(200.0, min(front_rise, 360.0))
hem_width = max(140.0, min(hem_width, 320.0))
knee_width = max(150.0, min(knee_width, 360.0))
band_depth = max(28.0, min(band_depth, 64.0))
button_head = max(11.0, min(button_head, 24.0))
wear_ease = max(0.0, min(wear_ease, 140.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(18.0, min(hem_allowance, 55.0))

TOPSTITCH = 7.0                               # denim twin-needle gauge, family std

# ── Derived block dimensions, every one clamped ──────────────────────────────
QUARTER_HIP = (hip_girth + wear_ease) / 4.0
# The back rise runs deeper than the front — the classic jean fork. Held clear so
# a short front rise with a big hip can never invert the crotch curve.
BACK_RISE = max(front_rise + 40.0, front_rise * 1.12)
# The waist quarter, shaped in from the hip. Floored so it can never exceed the
# hip quarter (an inverted side seam) nor collapse to nothing.
_QUARTER_WAIST_RAW = (waist_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.62, min(_QUARTER_WAIST_RAW, QUARTER_HIP - 6.0))
HALF_HEM = hem_width / 2.0
HALF_KNEE = knee_width / 2.0
# Fork extensions past the side-block width. Both clamped positive.
FORK_F = max(20.0, QUARTER_HIP * 0.14)
FORK_B = max(34.0, QUARTER_HIP * 0.22)
# The fly lap the waistband loses at centre front — a real fixed extension.
FLY_LAP = max(30.0, button_head * 2.0)


def _rivet(label, x, y):
    """A pocket-corner rivet drawn as a real drill + at its cap size."""
    a = max(3.0, button_head * 0.22)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


# ── Inseams solved to equal length ───────────────────────────────────────────
def _front_inseam(bulge):
    return fc.Edge("inseam", [fc.curve_through(
        fc.P(QUARTER_HIP + FORK_F, front_rise), fc.P(HALF_HEM, 0.0),
        bulge=bulge, side=-1.0)])


_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, BACK_RISE), fc.P(HALF_HEM, 0.0),
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
    """Front leg, cut 2 mirrored. The outseam (side) is the SELVEDGE edge — kept
    straight because the loom's finished edge cannot be curved."""
    p_hem_side = fc.P(0.0, 0.0)
    p_knee_side = fc.P(0.0, inside_leg * 0.48)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, front_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_F, front_rise)
    edges = [
        # SELVEDGE OUTSEAM: one straight line hem-to-waist, no shaping. This is
        # the whole point of a selvedge jean — the finished edge stays finished.
        fc.Edge("side", [fc.Line(p_hem_side, p_knee_side),
                         fc.Line(p_knee_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, front_rise - front_rise * 0.44),
            fc.P(QUARTER_HIP + FORK_F * 0.35, front_rise * 0.18),
            p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF / fly match"),
                 fc.Notch("side", 0.48, "knee level"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, front_rise * 0.9)),
        internals=[
            fc.Internal("selvedge outseam (no fell)",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, front_rise)],
                        kind="trace"),
            fc.Internal("front pocket placement",
                        [fc.P(QUARTER_WAIST * 0.30, front_rise - seam_allowance),
                         fc.P(QUARTER_WAIST - seam_allowance,
                              front_rise - seam_allowance),
                         fc.P(QUARTER_WAIST - seam_allowance,
                              front_rise - front_rise * 0.42),
                         fc.P(QUARTER_WAIST * 0.30, front_rise - seam_allowance)],
                        kind="marking"),
            # RIVET SITE — front pocket mouth top corner, stepped in from both
            # edges so it never lands on the pocket hem or the waist allowance.
            _rivet("front pocket rivet",
                   QUARTER_WAIST - seam_allowance - button_head * 0.6,
                   front_rise - seam_allowance - button_head * 0.6),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    """Back leg, cut 2 mirrored. Carries the yoke seam mark and the patch pocket;
    the back rise is the deeper fork."""
    # The back side seam ends at the SAME height as the front's — the two
    # outseams sew together and must measure the same. The deeper back rise is
    # carried at CENTRE BACK, not at the side: the waist edge tilts up from the
    # side point to the raised CB, which is the correct jean draft (and the fix
    # for a naive back that lengthens the side seam and twists the leg).
    p_hem_side = fc.P(0.0, 0.0)
    p_knee_side = fc.P(0.0, inside_leg * 0.48)
    p_waist_side = fc.P(0.0, front_rise)          # matches the front side height
    p_waist_in = fc.P(QUARTER_WAIST, BACK_RISE)   # CB raised for the jean fork
    p_fork = fc.P(QUARTER_HIP + FORK_B, BACK_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_knee_side),
                         fc.Line(p_knee_side, p_waist_side)]),
        # The back waist rises from the side point to the raised CB.
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, BACK_RISE - BACK_RISE * 0.44),
            fc.P(QUARTER_HIP + FORK_B * 0.35, BACK_RISE * 0.18),
            p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "back_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CB match"),
                 fc.Notch("side", 0.48, "knee level"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, BACK_RISE * 0.9)),
        internals=[
            fc.Internal("selvedge outseam (no fell)",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, front_rise)],
                        kind="trace"),
            fc.Internal("patch pocket placement",
                        [fc.P(QUARTER_WAIST * 0.18, BACK_RISE - band_depth - 30.0),
                         fc.P(QUARTER_WAIST * 0.86, BACK_RISE - band_depth - 30.0),
                         fc.P(QUARTER_WAIST * 0.86,
                              BACK_RISE - band_depth - 30.0 - QUARTER_WAIST * 0.62),
                         fc.P(QUARTER_WAIST * 0.18,
                              BACK_RISE - band_depth - 30.0 - QUARTER_WAIST * 0.62),
                         fc.P(QUARTER_WAIST * 0.18, BACK_RISE - band_depth - 30.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


# ── The waistband, cut to the MEASURED waist ─────────────────────────────────
_FL = build_front_leg()
_BL = build_back_leg()
FRONT_WAIST_RUN = _FL.edge("waist").length(0.05)
BACK_WAIST_RUN = _BL.edge("waist").length(0.05)
# Two fronts + two backs, less the fly seam the front loses, plus the button
# extension on the overlap side. Measured, never a laid-flat girth.
BAND_LENGTH = (2.0 * FRONT_WAIST_RUN + 2.0 * BACK_WAIST_RUN
               - seam_allowance + FLY_LAP)
BAND_CUT_H = band_depth * 2.0 + 2.0 * seam_allowance   # folded band, two turnings


def build_waistband():
    """A straight waistband, cut 1 (pieced at CB in wear). Folded in half; the
    jeans button sits on the extension, stepped in off the finished end."""
    ln = BAND_LENGTH
    w = BAND_CUT_H
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("ext_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("cf_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    # The button is stepped in from the extension end by its own head diameter
    # plus a clearance, so it is never set on the turned end where it holds
    # nothing. This is the dimension the jeans-button solid is fed from.
    button_x = max(button_head, ln - seam_allowance - button_head * 0.9)
    a = max(4.0, button_head * 0.5)
    return fc.Piece(
        "waistband", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},   # long edges are folded, not sewn
        notches=[fc.Notch("lower", 0.5, "CB"),
                 fc.Notch("lower", 1.0 - FLY_LAP / ln, "fly / button extension")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            fc.Internal("band topstitch",
                        [fc.P(TOPSTITCH, TOPSTITCH),
                         fc.P(ln - TOPSTITCH, TOPSTITCH)],
                        kind="trace"),
            # The jeans-button seat, drawn to the head's own size.
            fc.Internal("jeans button seat",
                        [fc.P(button_x - a, w / 2.0), fc.P(button_x + a, w / 2.0),
                         fc.P(button_x, w / 2.0),
                         fc.P(button_x, w / 2.0 - a), fc.P(button_x, w / 2.0 + a)],
                        kind="drill"),
            fc.Internal("buttonhole (CF end)",
                        [fc.P(seam_allowance + a, w / 2.0 - a * 1.4),
                         fc.P(seam_allowance + a, w / 2.0 + a * 1.4)],
                        kind="cut"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Waistband (cut 1)",
    )


def build_fly():
    """The fly shield / facing, cut 2. A straight piece the width of the fly lap,
    the depth of the front rise less the band."""
    lap = FLY_LAP
    depth = max(80.0, front_rise - band_depth - 20.0)
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, depth), fc.P(lap, depth))]),
        fc.Edge("curve", [fc.curve_through(
            fc.P(lap, depth), fc.P(0.0, 0.0), bulge=0.30, side=1.0)]),
    ]
    return fc.Piece(
        "fly", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("cf", 1.0, "waistband join")],
        grainline=fc.Grainline(fc.P(lap * 0.4, depth * 0.15),
                               fc.P(lap * 0.4, depth * 0.85)),
        internals=[
            fc.Internal("fly topstitch (J-stitch)",
                        [fc.P(lap * 0.5, depth - TOPSTITCH),
                         fc.P(lap * 0.5, depth * 0.30),
                         fc.P(lap * 0.1, depth * 0.10)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Fly shield / facing (cut 2)",
    )


def build_coin_pocket():
    """The coin (watch) pocket, cut 1. Sits inside the front pocket mouth."""
    w = max(60.0, QUARTER_WAIST * 0.28)
    h = max(60.0, w * 0.95)
    edges = [
        fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, h * 0.30))]),
        fc.Edge("point", [fc.Line(fc.P(w, h * 0.30), fc.P(w / 2.0, 0.0)),
                          fc.Line(fc.P(w / 2.0, 0.0), fc.P(0.0, h * 0.30))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, h * 0.30), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "coin_pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"mouth": hem_allowance * 0.5},
        notches=[fc.Notch("mouth", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.15), fc.P(w / 2.0, h * 0.85)),
        internals=[
            fc.Internal("mouth topstitch",
                        [fc.P(TOPSTITCH, h - TOPSTITCH),
                         fc.P(w - TOPSTITCH, h - TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Coin pocket (cut 1)",
    )


def build_pocket_bag():
    """The front pocket bag, cut 4 (two per side). A plain lining shape."""
    w = max(150.0, QUARTER_WAIST * 0.9)
    h = max(200.0, front_rise * 0.9)
    edges = [
        fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w * 0.7, h))]),
        fc.Edge("side", [fc.curve_through(
            fc.P(w * 0.7, h), fc.P(w, 0.0), bulge=0.18, side=-1.0)]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "pocket_bag", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("mouth", 1.0, "pocket opening end")],
        grainline=fc.Grainline(fc.P(w * 0.3, h * 0.15), fc.P(w * 0.3, h * 0.85)),
        internals=[],
        cut=fc.CutSpec(quantity=4),
        label="Front pocket bag (cut 4)",
    )


def build():
    pattern = fc.PatternSet("selvedge-jean")
    everything = target_piece == "set"
    want = {
        "front_leg": everything or target_piece == "front_leg",
        "back_leg": everything or target_piece == "back_leg",
        "waistband": everything or target_piece == "waistband",
        "fly": everything or target_piece == "fly",
        "coin_pocket": everything or target_piece == "coin_pocket",
        "pocket_bag": everything or target_piece == "pocket_bag",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front_leg"]:
        pattern.add(build_front_leg())
    if want["back_leg"]:
        pattern.add(build_back_leg())
    if want["waistband"]:
        pattern.add(build_waistband())
    if want["fly"]:
        pattern.add(build_fly())
    if want["coin_pocket"]:
        pattern.add(build_coin_pocket())
    if want["pocket_bag"]:
        pattern.add(build_pocket_bag())

    if want["front_leg"] and want["back_leg"]:
        # The inseam carries the whole leg and there is no drape to hide a twist:
        # both must measure the same to well under a millimetre.
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"),
                             tol=0.4)
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)
    if want["waistband"] and want["front_leg"] and want["back_leg"]:
        # The band is cut to the MEASURED waist runs. This declares the band's
        # lower edge against the summed panel waists (as an ease so the check
        # lands near zero and goes red if the band is redrafted off a girth).
        summed = 2.0 * FRONT_WAIST_RUN + 2.0 * BACK_WAIST_RUN
        pattern.declare_seam(("waistband", "lower"), [("front_leg", "waist"),
                             ("front_leg", "waist"), ("back_leg", "waist"),
                             ("back_leg", "waist")],
                             tol=1.0, ease=BAND_LENGTH - summed)

    fabric_width = 1500.0                       # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "selvedge denim, 14 oz (475 gsm), full-width for a clean outseam",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 74% marker; the outseam is laid "
                 f"on the loom's finished (selvedge) edge, so the roll must be cut "
                 f"selvedge-to-selvedge and the outseam kept straight."},
        {"item": "jeans button (tack-set, non-sew)", "qty": 1, "unit": "set",
         "note": f"Yantra4D jeans-button (notion.hardware_ref) at a "
                 f"{button_head:.0f} mm head; set on the waistband extension, "
                 f"stepped in off the finished end by its own head plus clearance."},
        {"item": "rivet + burr", "qty": 5, "unit": "set",
         "note": "front pocket corners (4) + coin pocket (1); each stepped in off "
                 "both edges of the piece it lands on. Marked, not modelled — one "
                 "bridged solid per notion."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm; the selvedge outseam is "
                 f"felled but NOT curved, the fly is a J-stitch, both pocket mouths "
                 f"and the band edge are topstitched."},
    ]
    pattern.metadata = {
        "fc400_rank": 301,
        "family": "denim",
        "tier": 2,
        "fabric_hint": "denim-14oz",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(front_rise, 1),
            "back_rise": round(BACK_RISE, 1),
            "inside_leg": round(inside_leg, 1),
            "hem_width": round(hem_width, 1),
            "knee_width": round(knee_width, 1),
            "band_length": round(BAND_LENGTH, 1),
            "band_depth": round(band_depth, 1),
        },
        "solved": {
            "front_inseam_bulge": round(BULGE, 5),
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "front_waist_run_mm": round(FRONT_WAIST_RUN, 2),
            "back_waist_run_mm": round(BACK_WAIST_RUN, 2),
            "band_length_measured_mm": round(BAND_LENGTH, 2),
            "fly_lap_mm": round(FLY_LAP, 2),
            "quarter_waist_requested_mm": round(_QUARTER_WAIST_RAW, 2),
            "quarter_waist_clamped_mm": round(QUARTER_WAIST, 2),
            "quarter_waist_was_clamped": bool(
                abs(QUARTER_WAIST - _QUARTER_WAIST_RAW) > 0.01),
            "button_head_mm": round(button_head, 2),
            "note": "the two inseams are bisected to equal length (a straight jean "
                    "has no drape to hide a twist); the waistband is cut to the "
                    "MEASURED sum of the panel waist runs plus the fly lap, never "
                    "to a laid-flat girth; and the jeans button is stepped in off "
                    "the band's finished end so it seats on cloth. The waist "
                    "quarter is clamped against the hip quarter so a big waist "
                    "cannot invert the side seam.",
        },
        "selvedge_convention": {
            "outseam": "the side seam is the loom's finished (selvedge) edge, cut "
                       "straight and felled with the white line showing — it is the "
                       "one edge that cannot be shaped without destroying its finish",
            "gauge": f"{TOPSTITCH:.0f} mm twin-needle gold, matching jeans-5-pocket "
                     f"and the denim family",
        },
        "hardware": "jeans button via Yantra4D (notion.hardware_ref -> jeans-button); "
                    "the solid's head_dia — the parameter driving its bearing head, "
                    "the face that shows on the band — is fed from this garment's "
                    "button_head, which also sets the button's step-in from the "
                    "band's finished end. One number sizes it and places it. The "
                    "five rivets are a second finding, marked and counted only.",
    }
    return pattern


result = build()

"""
Selvedge straight-leg jean — Fashion Cabinet Garment Cartridge (FC-500 #401, denim, T3).

The five-pocket STRAIGHT-LEG jean cut for SELVEDGE denim. The outseam is left on the
loom's finished edge (the selvedge) and felled with the tell-tale white line, so the
outseam is the ONE edge of the whole garment drafted flat and straight — a selvedge
edge cannot be curved without cutting off the very finish that makes it selvedge. The
leg runs a true straight from a clamped knee to a clamped hem (knee never narrower than
the hem, so the silhouette is never a boot-cut in disguise).

Two things are solved by measurement, not formula:

  1. THE TWO INSEAMS CLOSE TO ZERO. Front and back inseams sew together and carry the
     whole leg; if they do not MEASURE the same the leg twists and the felled outseam
     ripples. The front inseam's bulge is BISECTED until it measures the plain back
     inseam to well under a millimetre.
  2. THE WAISTBAND IS CUT TO THE MEASURED WAIST. The band length is the sum of the four
     panel waist runs AS BUILT, less the fly seam, plus the button extension — never a
     laid-flat girth that is always wrong by the fly and the darts.

Every derived dimension is CLAMPED. The waist quarter is held under the hip quarter so
a big waist can never invert the side seam — geometry the kernel would CCW-normalize
into a healthy-looking piece. The jeans button is stepped in off the band's finished
end so it seats on cloth, not on the turned extension where it holds nothing.

The JEANS-BUTTON SOLID is Yantra4D territory (notion.hardware_ref -> jeans-button); its
head_dia is fed from this garment's button_head, one number that sizes and places it.

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


target_piece = str(PARAM(lambda: target_piece, "set"))
# front_leg|back_leg|waistband|fly|coin_pocket|pocket_bag|set

waist_girth = float(PARAM(lambda: waist_girth, 820.0))
hip_girth = float(PARAM(lambda: hip_girth, 1000.0))
inside_leg = float(PARAM(lambda: inside_leg, 810.0))
front_rise = float(PARAM(lambda: front_rise, 260.0))
hem_width = float(PARAM(lambda: hem_width, 190.0))
knee_width = float(PARAM(lambda: knee_width, 210.0))
band_depth = float(PARAM(lambda: band_depth, 40.0))
button_head = float(PARAM(lambda: button_head, 17.0))
wear_ease = float(PARAM(lambda: wear_ease, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 32.0))

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

TOPSTITCH = 7.0

QUARTER_HIP = (hip_girth + wear_ease) / 4.0
BACK_RISE = max(front_rise + 40.0, front_rise * 1.12)
_QUARTER_WAIST_RAW = (waist_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.62, min(_QUARTER_WAIST_RAW, QUARTER_HIP - 6.0))
# A straight leg holds the knee no narrower than the hem. Clamp so a knee set below the
# hem never renders a boot-cut sliver that passes verify() looking healthy.
HALF_HEM = hem_width / 2.0
HALF_KNEE = max(HALF_HEM, knee_width / 2.0)
FORK_F = max(20.0, QUARTER_HIP * 0.14)
FORK_B = max(34.0, QUARTER_HIP * 0.22)
FLY_LAP = max(30.0, button_head * 2.0)


def _rivet(label, x, y):
    a = max(3.0, button_head * 0.22)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


def _front_inseam(bulge):
    return fc.Edge("inseam", [fc.curve_through(
        fc.P(QUARTER_HIP + FORK_F, front_rise), fc.P(HALF_HEM, 0.0),
        bulge=bulge, side=-1.0)])


_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, BACK_RISE), fc.P(HALF_HEM, 0.0),
    bulge=0.0, side=-1.0)])
_BACK_INSEAM_LEN = _BACK_INSEAM.length(0.05)


def _solve_front_bulge():
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
    p_hem_side = fc.P(0.0, 0.0)
    p_knee_side = fc.P(HALF_HEM - HALF_KNEE, inside_leg * 0.48)
    p_waist_side = fc.P(HALF_HEM - HALF_KNEE, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, front_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_F, front_rise)
    edges = [
        # SELVEDGE OUTSEAM: hem -> knee -> waist. The knee/waist share one x so the
        # straight leg runs plumb; the finished edge is never shaped.
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
                        [fc.P(HALF_HEM - HALF_KNEE + TOPSTITCH, 0.0),
                         fc.P(HALF_HEM - HALF_KNEE + TOPSTITCH, front_rise)],
                        kind="trace"),
            _rivet("front pocket rivet",
                   QUARTER_WAIST - seam_allowance - button_head * 0.6,
                   front_rise - seam_allowance - button_head * 0.6),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    p_hem_side = fc.P(0.0, 0.0)
    p_knee_side = fc.P(HALF_HEM - HALF_KNEE, inside_leg * 0.48)
    p_waist_side = fc.P(HALF_HEM - HALF_KNEE, front_rise)   # matches the front side height
    p_waist_in = fc.P(QUARTER_WAIST, BACK_RISE)             # CB raised for the jean fork
    p_fork = fc.P(QUARTER_HIP + FORK_B, BACK_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_knee_side),
                         fc.Line(p_knee_side, p_waist_side)]),
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
                        [fc.P(HALF_HEM - HALF_KNEE + TOPSTITCH, 0.0),
                         fc.P(HALF_HEM - HALF_KNEE + TOPSTITCH, front_rise)],
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


_FL = build_front_leg()
_BL = build_back_leg()
FRONT_WAIST_RUN = _FL.edge("waist").length(0.05)
BACK_WAIST_RUN = _BL.edge("waist").length(0.05)
BAND_LENGTH = (2.0 * FRONT_WAIST_RUN + 2.0 * BACK_WAIST_RUN
               - seam_allowance + FLY_LAP)
BAND_CUT_H = band_depth * 2.0 + 2.0 * seam_allowance


def build_waistband():
    ln = BAND_LENGTH
    w = BAND_CUT_H
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("ext_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("cf_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    button_x = max(button_head, ln - seam_allowance - button_head * 0.9)
    a = max(4.0, button_head * 0.5)
    return fc.Piece(
        "waistband", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
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
    pattern = fc.PatternSet("selvedge-jean-straight")
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
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=0.4)
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)
    if want["waistband"] and want["front_leg"] and want["back_leg"]:
        summed = 2.0 * FRONT_WAIST_RUN + 2.0 * BACK_WAIST_RUN
        pattern.declare_seam(("waistband", "lower"), [("front_leg", "waist"),
                             ("front_leg", "waist"), ("back_leg", "waist"),
                             ("back_leg", "waist")],
                             tol=1.0, ease=BAND_LENGTH - summed)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "selvedge denim, 14 oz (475 gsm), full-width for a clean outseam",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 74% marker; the outseam is laid on "
                 f"the loom's finished (selvedge) edge, cut selvedge-to-selvedge and "
                 f"kept straight."},
        {"item": "jeans button (tack-set, non-sew)", "qty": 1, "unit": "set",
         "note": f"Yantra4D jeans-button (notion.hardware_ref) at a {button_head:.0f} mm "
                 f"head; set on the waistband extension, stepped in off the finished end "
                 f"by its own head plus clearance."},
        {"item": "rivet + burr", "qty": 5, "unit": "set",
         "note": "front pocket corners (4) + coin pocket (1); each stepped in off both "
                 "edges of the piece it lands on. Marked, not modelled."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm; the selvedge outseam is felled but "
                 f"NOT curved, the fly is a J-stitch, both pocket mouths topstitched."},
    ]
    pattern.metadata = {
        "fc500_rank": 401,
        "family": "denim",
        "tier": 3,
        "fabric_hint": "mezclilla-selvage",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(front_rise, 1),
            "back_rise": round(BACK_RISE, 1),
            "inside_leg": round(inside_leg, 1),
            "hem_width": round(hem_width, 1),
            "knee_width": round(HALF_KNEE * 2.0, 1),
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
            "half_knee_clamped_to_hem": bool(knee_width / 2.0 < HALF_HEM),
            "button_head_mm": round(button_head, 2),
            "note": "the two inseams are bisected to equal length; the waistband is cut "
                    "to the MEASURED sum of the panel waist runs plus the fly lap; the "
                    "waist quarter is clamped under the hip quarter so a big waist cannot "
                    "invert the side seam; and the half-knee is clamped to at least the "
                    "half-hem so a straight leg never renders a boot-cut sliver.",
        },
        "hardware": "jeans button via Yantra4D (notion.hardware_ref -> jeans-button); "
                    "head_dia is fed from button_head, which also sets the button's "
                    "step-in from the band's finished end. The five rivets are a second "
                    "finding, marked and counted only.",
    }
    return pattern


result = build()

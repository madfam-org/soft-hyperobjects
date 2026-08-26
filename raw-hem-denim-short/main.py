"""
Raw-hem denim short — Fashion Cabinet Garment Cartridge (FC-500 #411, denim, T2).

The cut-off denim short with a RAW (unfinished) hem — the leg chopped short and left to
fray, no turn-up. Because there is no hem allowance to hide behind, the raw edge is drawn
at its FINISHED length and the fray depth is marked as a distress zone, not sewn. A
five-pocket block scaled to the short leg: front and back legs, a measured waistband, a
fly, a coin pocket and pocket bags.

Solved by measurement, not formula:

  1. THE TWO INSEAMS CLOSE TO ZERO. Even a short leg twists if the inseams do not measure
     the same; the front inseam's bulge is BISECTED to the plain back inseam.
  2. THE WAISTBAND IS CUT TO THE MEASURED WAIST — the summed panel waist runs plus the
     fly lap, never a laid-flat girth.

CLAMPS. The waist quarter is held under the hip quarter (a big waist cannot invert the
side seam). The short leg length is clamped to a floor so a raw hem set too high never
collapses the leg into the crotch curve. The jeans button is stepped in off the band's
finished end. Bridges to the Yantra4D `jeans-button` solid.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front_leg|back_leg|waistband|fly|coin_pocket|pocket_bag|set

waist_girth = float(PARAM(lambda: waist_girth, 820.0))
hip_girth = float(PARAM(lambda: hip_girth, 1000.0))
short_length = float(PARAM(lambda: short_length, 300.0))   # crotch to raw hem
front_rise = float(PARAM(lambda: front_rise, 255.0))
hem_width = float(PARAM(lambda: hem_width, 280.0))         # flat thigh opening
band_depth = float(PARAM(lambda: band_depth, 40.0))
button_head = float(PARAM(lambda: button_head, 17.0))
wear_ease = float(PARAM(lambda: wear_ease, 50.0))
fray_depth = float(PARAM(lambda: fray_depth, 14.0))       # distress zone, marked
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

waist_girth = max(560.0, min(waist_girth, 1200.0))
hip_girth = max(720.0, min(hip_girth, 1400.0))
short_length = max(140.0, min(short_length, 480.0))
front_rise = max(200.0, min(front_rise, 360.0))
hem_width = max(180.0, min(hem_width, 420.0))
band_depth = max(28.0, min(band_depth, 64.0))
button_head = max(11.0, min(button_head, 24.0))
wear_ease = max(0.0, min(wear_ease, 160.0))
fray_depth = max(4.0, min(fray_depth, 30.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

TOPSTITCH = 7.0

QUARTER_HIP = (hip_girth + wear_ease) / 4.0
BACK_RISE = max(front_rise + 40.0, front_rise * 1.12)
_QUARTER_WAIST_RAW = (waist_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.62, min(_QUARTER_WAIST_RAW, QUARTER_HIP - 6.0))
# The thigh opening cannot be narrower than the hip quarter or the leg pinches; and the
# short length is floored well clear of the crotch depth so a raw hem set high never folds
# the leg into the fork curve.
HALF_HEM = max(QUARTER_HIP * 0.9, hem_width / 2.0)
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
        fc.P(QUARTER_HIP + FORK_F, front_rise), fc.P(HALF_HEM, front_rise - short_length),
        bulge=bulge, side=-1.0)])


# The back hem sits on the SAME hemline as the front (y = front_rise - short_length),
# so the two side seams — front and back — measure the same and sew without a twist.
_HEMLINE_Y = front_rise - short_length
_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, BACK_RISE), fc.P(HALF_HEM, _HEMLINE_Y),
    bulge=0.0, side=-1.0)])
_BACK_INSEAM_LEN = _BACK_INSEAM.length(0.05)


def _solve_front_bulge():
    # Grow the search ceiling until the front inseam can reach the back's length — the
    # front fork sits lower than the back (a shallower rise) so the chord is shorter and
    # a fixed ceiling can leave the target unreachable at the short-rise extreme.
    lo, hi = 0.0, 0.6
    for _ in range(24):
        if _front_inseam(hi).length(0.05) >= _BACK_INSEAM_LEN:
            break
        hi *= 1.5
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if _front_inseam(mid).length(0.05) < _BACK_INSEAM_LEN:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


BULGE = _solve_front_bulge()
_FRONT_INSEAM_LEN = _front_inseam(BULGE).length(0.05)


def build_front_leg():
    y_hem = front_rise - short_length
    p_hem_side = fc.P(0.0, y_hem)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, front_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_F, front_rise)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, front_rise - front_rise * 0.44),
            fc.P(QUARTER_HIP + FORK_F * 0.35, front_rise * 0.18 + y_hem),
            p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, y_hem), p_hem_side)]),
    ]
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 0.0},   # a RAW hem has no turn-up
        notches=[fc.Notch("waist", 1.0, "CF / fly match"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, y_hem + 20.0),
                               fc.P(QUARTER_HIP * 0.42, front_rise * 0.9)),
        internals=[
            fc.Internal("raw-hem fray zone",
                        [fc.P(0.0, y_hem + fray_depth),
                         fc.P(HALF_HEM, y_hem + fray_depth)],
                        kind="marking"),
            _rivet("front pocket rivet",
                   QUARTER_WAIST - seam_allowance - button_head * 0.6,
                   front_rise - seam_allowance - button_head * 0.6),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    y_hem = _HEMLINE_Y                       # same hemline as the front
    p_hem_side = fc.P(0.0, y_hem)
    p_waist_side = fc.P(0.0, front_rise)     # front side height — sides sew equal
    p_waist_in = fc.P(QUARTER_WAIST, BACK_RISE)
    p_fork = fc.P(QUARTER_HIP + FORK_B, BACK_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, BACK_RISE - BACK_RISE * 0.44),
            fc.P(QUARTER_HIP + FORK_B * 0.35, BACK_RISE * 0.18),
            p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, y_hem), p_hem_side)]),
    ]
    return fc.Piece(
        "back_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 0.0},
        notches=[fc.Notch("waist", 1.0, "CB match"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, y_hem + 20.0),
                               fc.P(QUARTER_HIP * 0.42, BACK_RISE * 0.9)),
        internals=[
            fc.Internal("raw-hem fray zone",
                        [fc.P(0.0, y_hem + fray_depth),
                         fc.P(HALF_HEM, y_hem + fray_depth)],
                        kind="marking"),
            fc.Internal("patch pocket placement",
                        [fc.P(QUARTER_WAIST * 0.18, BACK_RISE - band_depth - 30.0),
                         fc.P(QUARTER_WAIST * 0.86, BACK_RISE - band_depth - 30.0),
                         fc.P(QUARTER_WAIST * 0.86,
                              BACK_RISE - band_depth - 30.0 - QUARTER_WAIST * 0.55),
                         fc.P(QUARTER_WAIST * 0.18,
                              BACK_RISE - band_depth - 30.0 - QUARTER_WAIST * 0.55),
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
        allowances={"mouth": 20.0},
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
    h = max(180.0, front_rise * 0.85)
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
    pattern = fc.PatternSet("raw-hem-denim-short")
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
        {"item": "denim, 14 oz (475 gsm)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 74% marker; the leg is cut at its "
                 f"finished (raw) length — no turn-up allowance below the fray zone."},
        {"item": "jeans button (tack-set, non-sew)", "qty": 1, "unit": "set",
         "note": f"Yantra4D jeans-button (notion.hardware_ref) at a {button_head:.0f} mm "
                 f"head; stepped in off the band's finished end."},
        {"item": "rivet + burr", "qty": 5, "unit": "set",
         "note": "front pocket corners (4) + coin pocket (1); marked, not modelled."},
        {"item": "topstitch thread (gold) + jeans needle", "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm; the raw hem is left unstitched and "
                 f"the marked fray zone is distressed after wash, not sewn."},
    ]
    pattern.metadata = {
        "fc500_rank": 411,
        "family": "denim",
        "tier": 2,
        "fabric_hint": "mezclilla-14oz",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(front_rise, 1),
            "back_rise": round(BACK_RISE, 1),
            "short_length": round(short_length, 1),
            "thigh_opening_flat": round(HALF_HEM * 2.0, 1),
            "band_length": round(BAND_LENGTH, 1),
            "fray_depth": round(fray_depth, 1),
        },
        "solved": {
            "front_inseam_bulge": round(BULGE, 5),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "band_length_measured_mm": round(BAND_LENGTH, 2),
            "quarter_waist_was_clamped": bool(
                abs(QUARTER_WAIST - _QUARTER_WAIST_RAW) > 0.01),
            "thigh_opening_clamped_to_hip": bool(hem_width / 2.0 < QUARTER_HIP * 0.9),
            "note": "the two inseams are bisected to equal length; the band is cut to the "
                    "MEASURED panel waist runs; the waist quarter is clamped under the hip "
                    "quarter; the short length is floored and the thigh opening is clamped "
                    "to the hip quarter so a raw hem set high never folds the leg into the "
                    "crotch curve; the raw hem carries NO turn-up allowance.",
        },
        "hardware": "jeans button via Yantra4D (notion.hardware_ref -> jeans-button); "
                    "head_dia is fed from button_head. Rivets marked and counted only.",
    }
    return pattern


result = build()

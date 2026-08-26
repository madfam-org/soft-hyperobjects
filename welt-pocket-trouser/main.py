"""
Welt-pocket dress trouser — Fashion Cabinet Garment Cartridge (FC-500 #405, tailoring, T3).

A tailored dress trouser in worsted wool: a shaped FRONT with a slant pocket and a single
front pleat, a shaped BACK with a bound WELT pocket, a straight WAISTBAND closed at centre
front with a trouser hook-and-bar (no visible button), and the WELT strip itself. The
closure bridges to the Yantra4D `trouser-hook-bar` solid.

Solved, not guessed:

  1. THE TWO INSEAMS CLOSE TO ZERO. The front inseam's bulge is BISECTED to the plain back
     inseam so the leg does not twist — the same discipline a jean needs, and a dress
     trouser needs it more because the crease must hang plumb.
  2. THE WAISTBAND IS CUT TO THE MEASURED WAIST plus the hook-bar underlap, never a girth.
  3. THE WELT MOUTH IS CLAMPED. The welt opening cannot be drawn wider than the back panel
     waist run less a margin, so an over-wide welt request can never run off the panel edge
     and fold the piece into a self-crossing outline.

Every derived dimension is clamped; the waist quarter is held under the hip quarter so a big
waist cannot invert the side seam (geometry the kernel would CCW-normalize).

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
# front_leg|back_leg|waistband|welt|set

waist_girth = float(PARAM(lambda: waist_girth, 840.0))
hip_girth = float(PARAM(lambda: hip_girth, 1020.0))
inside_leg = float(PARAM(lambda: inside_leg, 800.0))
front_rise = float(PARAM(lambda: front_rise, 275.0))
hem_width = float(PARAM(lambda: hem_width, 210.0))
knee_width = float(PARAM(lambda: knee_width, 240.0))
band_depth = float(PARAM(lambda: band_depth, 38.0))
welt_width = float(PARAM(lambda: welt_width, 130.0))     # back welt-pocket mouth
hook_plate = float(PARAM(lambda: hook_plate, 55.0))      # drives trouser-hook-bar plate_len
wear_ease = float(PARAM(lambda: wear_ease, 60.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

waist_girth = max(600.0, min(waist_girth, 1300.0))
hip_girth = max(760.0, min(hip_girth, 1500.0))
inside_leg = max(600.0, min(inside_leg, 950.0))
front_rise = max(220.0, min(front_rise, 380.0))
hem_width = max(140.0, min(hem_width, 300.0))
knee_width = max(160.0, min(knee_width, 340.0))
band_depth = max(28.0, min(band_depth, 55.0))
welt_width = max(90.0, min(welt_width, 180.0))
hook_plate = max(35.0, min(hook_plate, 80.0))
wear_ease = max(20.0, min(wear_ease, 160.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

QUARTER_HIP = (hip_girth + wear_ease) / 4.0
BACK_RISE = max(front_rise + 34.0, front_rise * 1.10)
_QUARTER_WAIST_RAW = (waist_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.60, min(_QUARTER_WAIST_RAW, QUARTER_HIP - 6.0))
HALF_HEM = hem_width / 2.0
HALF_KNEE = max(HALF_HEM, knee_width / 2.0)
FORK_F = max(20.0, QUARTER_HIP * 0.13)
FORK_B = max(34.0, QUARTER_HIP * 0.20)
UNDERLAP = max(30.0, hook_plate * 0.9)     # the hook-bar underlap at CF


def _front_inseam(bulge):
    return fc.Edge("inseam", [fc.curve_through(
        fc.P(QUARTER_HIP + FORK_F, front_rise), fc.P(HALF_HEM, 0.0),
        bulge=bulge, side=-1.0)])


_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, BACK_RISE), fc.P(HALF_HEM, 0.0),
    bulge=0.0, side=-1.0)])
_BACK_INSEAM_LEN = _BACK_INSEAM.length(0.05)


def _solve_front_bulge():
    lo, hi = 0.0, 0.6
    for _ in range(24):
        if _front_inseam(hi).length(0.05) >= _BACK_INSEAM_LEN:
            break
        hi *= 1.5
    for _ in range(56):
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
    p_knee_side = fc.P(HALF_HEM - HALF_KNEE, inside_leg * 0.46)
    p_waist_side = fc.P(HALF_HEM - HALF_KNEE, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, front_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_F, front_rise)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_knee_side),
                         fc.Line(p_knee_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, front_rise - front_rise * 0.42),
            fc.P(QUARTER_HIP + FORK_F * 0.35, front_rise * 0.18),
            p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0},
        notches=[fc.Notch("waist", 1.0, "CF"),
                 fc.Notch("side", 0.46, "knee"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.44, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.44, front_rise * 0.9)),
        internals=[
            fc.Internal("front crease",
                        [fc.P(QUARTER_HIP * 0.44, 0.0),
                         fc.P(QUARTER_HIP * 0.44, front_rise)], kind="trace"),
            fc.Internal("front pleat",
                        [fc.P(QUARTER_WAIST * 0.5, front_rise),
                         fc.P(QUARTER_WAIST * 0.5, front_rise - 80.0)], kind="dart"),
            fc.Internal("slant pocket mouth",
                        [fc.P(QUARTER_WAIST, front_rise - 10.0),
                         fc.P(QUARTER_WAIST * 0.55, front_rise - front_rise * 0.30)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    p_hem_side = fc.P(0.0, 0.0)
    p_knee_side = fc.P(HALF_HEM - HALF_KNEE, inside_leg * 0.46)
    p_waist_side = fc.P(HALF_HEM - HALF_KNEE, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, BACK_RISE)
    p_fork = fc.P(QUARTER_HIP + FORK_B, BACK_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_knee_side),
                         fc.Line(p_knee_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, BACK_RISE - BACK_RISE * 0.42),
            fc.P(QUARTER_HIP + FORK_B * 0.35, BACK_RISE * 0.18),
            p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    # The welt mouth is clamped to sit inside the back panel waist run.
    back_waist_run = fc.P(QUARTER_WAIST, BACK_RISE).distance(p_waist_side)
    welt = min(welt_width, back_waist_run - 40.0)
    welt = max(50.0, welt)
    wy = BACK_RISE - band_depth - 55.0
    wx0 = QUARTER_WAIST * 0.5 - welt / 2.0
    return fc.Piece(
        "back_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0},
        notches=[fc.Notch("waist", 1.0, "CB"),
                 fc.Notch("side", 0.46, "knee"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.44, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.44, BACK_RISE * 0.9)),
        internals=[
            fc.Internal("back crease",
                        [fc.P(QUARTER_HIP * 0.44, 0.0),
                         fc.P(QUARTER_HIP * 0.44, BACK_RISE)], kind="trace"),
            fc.Internal("back dart",
                        [fc.P(QUARTER_WAIST * 0.55, BACK_RISE),
                         fc.P(QUARTER_WAIST * 0.55, BACK_RISE - 110.0)], kind="dart"),
            fc.Internal("welt pocket mouth",
                        [fc.P(wx0, wy), fc.P(wx0 + welt, wy)], kind="cut"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


_FL = build_front_leg()
_BL = build_back_leg()
FRONT_WAIST_RUN = _FL.edge("waist").length(0.05)
BACK_WAIST_RUN = _BL.edge("waist").length(0.05)
BAND_LENGTH = (2.0 * FRONT_WAIST_RUN + 2.0 * BACK_WAIST_RUN
               - seam_allowance + UNDERLAP)
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
    bar_x = max(hook_plate, ln - UNDERLAP * 0.5)
    return fc.Piece(
        "waistband", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.5, "CB"),
                 fc.Notch("lower", 1.0 - UNDERLAP / ln, "hook-bar underlap")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            fc.Internal("hook-bar plate (underlap end)",
                        [fc.P(bar_x, w / 2.0),
                         fc.P(bar_x - hook_plate / 2.0, w / 2.0),
                         fc.P(bar_x + hook_plate / 2.0, w / 2.0)], kind="drill"),
            fc.Internal("hook (overlap end)",
                        [fc.P(seam_allowance, w / 2.0),
                         fc.P(seam_allowance + hook_plate * 0.4, w / 2.0)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Waistband (cut 1)",
    )


def build_welt():
    """The welt strip, cut 2 (upper + lower welt). A rectangle the mouth width plus fold."""
    ln = min(welt_width, BACK_WAIST_RUN - 40.0)
    ln = max(50.0, ln) + 2.0 * seam_allowance
    w = max(24.0, band_depth * 0.7) * 2.0
    return fc.Piece(
        "welt", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[fc.Internal("welt fold", [fc.P(0.0, w * 0.5), fc.P(ln, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Welt strip (cut 2)",
    )


def build():
    pattern = fc.PatternSet("welt-pocket-trouser")
    everything = target_piece == "set"
    want = {
        "front_leg": everything or target_piece == "front_leg",
        "back_leg": everything or target_piece == "back_leg",
        "waistband": everything or target_piece == "waistband",
        "welt": everything or target_piece == "welt",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front_leg"]:
        pattern.add(build_front_leg())
    if want["back_leg"]:
        pattern.add(build_back_leg())
    if want["waistband"]:
        pattern.add(build_waistband())
    if want["welt"]:
        pattern.add(build_welt())

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
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "worsted wool suiting", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; press a hard front and back "
                 f"crease along the marked crease line."},
        {"item": "trouser hook-and-bar (no-sew / prong)", "qty": 1, "unit": "set",
         "note": f"Yantra4D trouser-hook-bar (notion.hardware_ref) at a {hook_plate:.0f} mm "
                 f"plate; the bar sits on the underlap end, the hook on the overlap."},
        {"item": "pocketing + welt interfacing", "qty": 1, "unit": "set",
         "note": "the back welt mouth is bound with the two welt strips over a pocket bag."},
        {"item": "silk thread + fine needle", "qty": 1, "unit": "spool",
         "note": "a tailored trouser: hand-finish the welt corners and the fly."},
    ]
    pattern.metadata = {
        "fc500_rank": 405, "family": "tailoring", "tier": 3,
        "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "A pleated dress trouser with a slant front pocket, a bound back "
            "welt pocket and a hidden trouser hook-and-bar closure.",
        "solved": {
            "front_inseam_bulge": round(BULGE, 5),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "band_length_measured_mm": round(BAND_LENGTH, 2),
            "welt_requested_mm": round(welt_width, 1),
            "welt_clamped_mm": round(max(50.0, min(welt_width, BACK_WAIST_RUN - 40.0)), 1),
            "quarter_waist_was_clamped": bool(
                abs(QUARTER_WAIST - _QUARTER_WAIST_RAW) > 0.01),
            "note": "the two inseams are bisected to equal length so the crease hangs plumb; "
                    "the band is cut to the MEASURED waist plus the hook-bar underlap; the "
                    "welt mouth is clamped inside the back waist run so an over-wide welt "
                    "never runs off the panel; the waist quarter is clamped under the hip.",
        },
        "hardware": "trouser hook-and-bar via Yantra4D (notion.hardware_ref -> "
                    "trouser-hook-bar); plate_len is fed from hook_plate. The sewn-plate "
                    "params are left unmapped — the hook-bar is set on the band underlap, "
                    "no dimensional handshake owed.",
    }
    return pattern


result = build()

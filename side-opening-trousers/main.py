"""
Side-Opening Trousers — Fashion Cabinet Garment Cartridge (FC-300 #245, adaptive II).

Trousers whose OUTSEAM does not exist as a seam: both side edges run open from
waistband to hem and close on hook-and-loop tape, so the garment can be laid flat
across a bed or a wheelchair seat, the wearer transferred onto it, and the sides
pressed shut — no standing, no stepping in, no reaching a fly. The tape SOLID is
Yantra4D territory (`hook-loop-tape`; see the manifest's notion.hardware_ref); what
Fashion Cabinet owns is the trouser and where the tape runs.

Two adaptive geometries are drafted in, not bolted on:

  1. SEATED CUT. `seat_rise_extra` lengthens the back rise and shortens the front
     rise by the same amount, so the waistband sits level when the hip is flexed at
     90 degrees instead of gaping at the back and cutting in at the front.
  2. OPEN OUTSEAM. The closure only lies flat if the two tape carriers measure the
     same. That is drafted, not asserted: front and back share ONE side-waist point
     at a common height (the seated rise tilt lives at CF/CB, not at the side), and
     the back's hem half-width is then BISECTED until its measured side edge equals
     the front's to within 0.02 mm. The hook-loop strip length is taken FROM that
     measured length, not from a rise+inseam formula.

Pieces:
  - front : trouser front (cut 2, mirrored), flat-front, seated-shortened rise.
  - back  : trouser back (cut 2, mirrored), seated-lengthened rise, one dart.
  - band  : straight waistband (cut 1 on fold at the lower edge), overlap at CF.
  - placket : the hook-and-loop tape carrier strip that backs the open outseam.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|band|placket|set

waist_girth = float(PARAM(lambda: waist_girth, 840.0))
hip_girth = float(PARAM(lambda: hip_girth, 1000.0))
outseam_length = float(PARAM(lambda: outseam_length, 1020.0))
front_rise = float(PARAM(lambda: front_rise, 280.0))
hem_width = float(PARAM(lambda: hem_width, 200.0))
seat_rise_extra = float(PARAM(lambda: seat_rise_extra, 45.0))
tape_width = float(PARAM(lambda: tape_width, 25.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (sane garment ranges) ─────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1400.0))
hip_girth = max(700.0, min(hip_girth, 1600.0))
outseam_length = max(700.0, min(outseam_length, 1250.0))
front_rise = max(200.0, min(front_rise, 380.0))
hem_width = max(140.0, min(hem_width, 320.0))
seat_rise_extra = max(0.0, min(seat_rise_extra, 90.0))
tape_width = max(16.0, min(tape_width, 50.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))

EASE_WAIST = 40.0          # a seated waist needs slack, not a fitted band
EASE_HIP = 80.0            # sitting spreads the seat; ease is functional here

# Quarter measures. The back takes the larger share of the seat.
Q_WAIST_F = (waist_girth + EASE_WAIST) / 4.0 - 10.0
Q_WAIST_B = (waist_girth + EASE_WAIST) / 4.0 + 10.0
Q_HIP_F = (hip_girth + EASE_HIP) / 4.0 - 12.0
Q_HIP_B = (hip_girth + EASE_HIP) / 4.0 + 12.0

# Seated rise split: the back gains what the front loses, so the total rise girth
# is unchanged while the waistline TILTS to a seated posture. The tilt is taken at
# centre front / centre back; the SIDE point is common to both pieces, because a
# split side height would make the two tape carriers structurally unequal.
RISE_F = front_rise - seat_rise_extra * 0.35   # CF rise (shortened: no belly cut-in)
RISE_B = front_rise + seat_rise_extra          # CB rise (raised: covers the seat)
RISE_SIDE = (RISE_F + RISE_B) / 2.0            # the shared side height
CROTCH_Y = outseam_length - RISE_SIDE          # the common crotch level (leg length)
LEG_F = CROTCH_Y
HIP_DROP = RISE_SIDE * 0.62   # hipline below the side waist
TOP_SIDE = RISE_SIDE + LEG_F  # y of the shared side-waist point
HEM_Q = hem_width / 2.0


def _side_curve(hip_x, hem_x, waist_x=None):
    """The open outseam edge, from the SHARED side-waist point down to the hem.

    Drafted as two Béziers: waist→hip (the hip spring) and hip→hem (the leg
    taper). Both pieces use the same top y (TOP_SIDE) and the same crotch level,
    so only the hip and hem x's differ — which is what makes an equal-length
    solve possible at all. Returned as a segment list so the caller can measure it.
    """
    wx = hip_x if waist_x is None else waist_x
    p_waist = fc.P(wx, TOP_SIDE)
    p_hip = fc.P(hip_x, TOP_SIDE - HIP_DROP)
    p_hem = fc.P(hem_x, 0.0)
    return [
        fc.Bezier(p_waist,
                  fc.P(wx + (hip_x - wx) * 0.55, TOP_SIDE - HIP_DROP * 0.30),
                  fc.P(hip_x, TOP_SIDE - HIP_DROP * 0.72),
                  p_hip),
        fc.Bezier(p_hip,
                  fc.P(hip_x - (hip_x - hem_x) * 0.18, LEG_F * 0.62),
                  fc.P(hem_x + (hip_x - hem_x) * 0.12, LEG_F * 0.26),
                  p_hem),
    ]


def _seg_len(segs):
    return sum(s.length(0.2) for s in segs)


# ── Solve the open outseam: front and back side edges must MEASURE equal ─────
# Both sides carry a hook-and-loop strip; unequal carriers buckle the closure.
# The front is drafted first and fixed; the back's hem half-width is then
# bisected until its side edge length matches the front's.
_FRONT_SIDE = _side_curve(Q_HIP_F, HEM_Q, Q_WAIST_F)
FRONT_SIDE_LEN = _seg_len(_FRONT_SIDE)


def _back_side(hem_q_back):
    return _side_curve(Q_HIP_B, hem_q_back, Q_WAIST_B)


def _solve_back_hem():
    """Bisect the back hem half-width so the back side edge equals the front's.

    Widening the back hem lengthens its side edge (the taper gets shallower is
    false — a wider hem shortens the horizontal run of the taper, so the curve
    shortens); the relation is monotone over the bracket, which is what bisection
    needs. Bracket generously and clamp the result to a wearable hem.
    """
    lo, hi = HEM_Q * 0.45, HEM_Q * 2.4
    f_lo = _seg_len(_back_side(lo)) - FRONT_SIDE_LEN
    f_hi = _seg_len(_back_side(hi)) - FRONT_SIDE_LEN
    if f_lo * f_hi > 0.0:
        # No sign change in the bracket — fall back to the nearer endpoint.
        return lo if abs(f_lo) < abs(f_hi) else hi
    for _ in range(80):
        mid = (lo + hi) / 2.0
        f_mid = _seg_len(_back_side(mid)) - FRONT_SIDE_LEN
        if abs(f_mid) < 0.02:
            return mid
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


HEM_Q_BACK = _solve_back_hem()
_BACK_SIDE = _back_side(HEM_Q_BACK)
BACK_SIDE_LEN = _seg_len(_BACK_SIDE)
# The tape run is the MEASURED open edge, less the waistband seam and a hem turn-up.
TAPE_RUN = FRONT_SIDE_LEN - seam_allowance - 30.0

# The waist edges are SLOPED (the seated tilt), so their true lengths exceed the
# flat quarter-widths. Measure them so the waistband is drafted to what it sews to.
WAIST_F_LEN = fc.P(0.0, LEG_F + RISE_F).distance(fc.P(Q_WAIST_F, TOP_SIDE))
WAIST_B_LEN = fc.P(0.0, LEG_F + RISE_B).distance(fc.P(Q_WAIST_B, TOP_SIDE))
BAND_OVERLAP = 60.0    # CF wrap so the band closes without a button
BAND_LEN = 2.0 * (WAIST_F_LEN + WAIST_B_LEN) + BAND_OVERLAP


def build_front():
    """Trouser front (cut 2 mirrored): open side edge, CF rise, inseam, hem.

    The CF waist sits at LEG_F + RISE_F — BELOW the shared side point — so the
    waist edge slopes down toward centre front. That slope is the seated tilt.
    """
    leg = LEG_F
    cf_top = leg + RISE_F
    p_side_waist = fc.P(Q_WAIST_F, TOP_SIDE)
    p_side_hem = fc.P(HEM_Q, 0.0)
    p_in_hem = fc.P(0.0, 0.0)
    p_crotch = fc.P(-14.0, leg)
    p_cf_waist = fc.P(0.0, cf_top)

    edges = [
        fc.Edge("side_open", _FRONT_SIDE),
        fc.Edge("hem", [fc.Line(p_side_hem, p_in_hem)]),
        # Inseam: a slight inward bow so the leg hangs clean when the knee is bent.
        fc.Edge("inseam", [fc.Bezier(p_in_hem,
                                     fc.P(-2.0, leg * 0.42),
                                     fc.P(-16.0, leg * 0.80),
                                     p_crotch)]),
        # Front rise (fly-free — there is no fly on this trouser, by design).
        fc.Edge("rise_cf", [fc.Bezier(p_crotch,
                                      fc.P(-4.0, leg + RISE_F * 0.30),
                                      fc.P(6.0, leg + RISE_F * 0.62),
                                      p_cf_waist)]),
        fc.Edge("waist", [fc.Line(p_cf_waist, p_side_waist)]),
    ]
    internals = [
        fc.Internal("hook-tape-run",
                    [fc.P(Q_WAIST_F - tape_width, TOP_SIDE - seam_allowance),
                     fc.P(HEM_Q - tape_width, 30.0)],
                    kind="marking"),
        fc.Internal("hipline", [fc.P(0.0, TOP_SIDE - HIP_DROP),
                                fc.P(Q_HIP_F, TOP_SIDE - HIP_DROP)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0},
        notches=[fc.Notch("side_open", 0.5, "hip match"),
                 fc.Notch("inseam", 0.55, "knee match")],
        grainline=fc.Grainline(fc.P(HEM_Q * 0.6, 60.0), fc.P(HEM_Q * 0.6, cf_top - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Trouser Front",
    )


def build_back():
    """Trouser back (cut 2 mirrored): seated-raised rise, one waist dart, open side."""
    leg = LEG_F
    cb_top = leg + RISE_B     # ABOVE the shared side point: the seated back extension
    p_side_waist = fc.P(Q_WAIST_B, TOP_SIDE)
    p_side_hem = fc.P(HEM_Q_BACK, 0.0)
    p_in_hem = fc.P(0.0, 0.0)
    p_crotch = fc.P(-46.0, leg)
    p_cb_waist = fc.P(0.0, cb_top)

    edges = [
        fc.Edge("side_open", _BACK_SIDE),
        fc.Edge("hem", [fc.Line(p_side_hem, p_in_hem)]),
        fc.Edge("inseam", [fc.Bezier(p_in_hem,
                                     fc.P(-4.0, leg * 0.42),
                                     fc.P(-30.0, leg * 0.80),
                                     p_crotch)]),
        # Back rise: deeper hook, and the seated extension is already in RISE_B.
        fc.Edge("rise_cb", [fc.Bezier(p_crotch,
                                      fc.P(-18.0, leg + RISE_B * 0.26),
                                      fc.P(4.0, leg + RISE_B * 0.66),
                                      p_cb_waist)]),
        fc.Edge("waist", [fc.Line(p_cb_waist, p_side_waist)]),
    ]
    # A single seat dart takes the back waist-to-hip difference out of the band.
    dart_x = Q_WAIST_B * 0.52
    dart_intake = max(8.0, min((Q_HIP_B - Q_WAIST_B) * 0.45, 26.0))
    dart_y = TOP_SIDE + (cb_top - TOP_SIDE) * (1.0 - dart_x / max(Q_WAIST_B, 1.0))
    internals = [
        fc.Internal("seat-dart",
                    [fc.P(dart_x - dart_intake / 2.0, dart_y),
                     fc.P(dart_x, dart_y - 130.0),
                     fc.P(dart_x + dart_intake / 2.0, dart_y)],
                    kind="dart"),
        fc.Internal("loop-tape-run",
                    [fc.P(Q_WAIST_B - tape_width, TOP_SIDE - seam_allowance),
                     fc.P(HEM_Q_BACK - tape_width, 30.0)],
                    kind="marking"),
        fc.Internal("hipline", [fc.P(0.0, TOP_SIDE - HIP_DROP),
                                fc.P(Q_HIP_B, TOP_SIDE - HIP_DROP)],
                    kind="marking"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0},
        notches=[fc.Notch("side_open", 0.5, "hip match"),
                 fc.Notch("inseam", 0.55, "knee match")],
        grainline=fc.Grainline(fc.P(HEM_Q_BACK * 0.6, 60.0),
                               fc.P(HEM_Q_BACK * 0.6, leg - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Trouser Back (seated rise)",
    )


def build_band():
    """Waistband, cut 1 on fold at its lower edge.

    Its length is the MEASURED sum of the four sloped waist edges plus a front
    overlap — measured, because the seated tilt makes each waist edge longer than
    its flat quarter-width, and a band cut to the flat width would come up short.
    """
    length = BAND_LEN
    h = 45.0
    return fc.Piece(
        "band",
        [
            fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, h))]),
            fc.Edge("upper", [fc.Line(fc.P(length, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0},
        notches=[fc.Notch("lower", 0.25, "side opening"),
                 fc.Notch("lower", 0.75, "side opening")],
        grainline=fc.Grainline(fc.P(length * 0.2, h / 2.0), fc.P(length * 0.8, h / 2.0)),
        internals=[fc.Internal("band-fold",
                               [fc.P(0.0, h / 2.0), fc.P(length, h / 2.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="lower"),
        label="Waistband",
    )


def build_placket():
    """Tape carrier strip: backs the open outseam so the hooks never touch skin.

    Cut 2 (one per leg). Its length is the solved TAPE_RUN; its width carries the
    tape plus a sew margin either side, which is exactly what the Yantra4D
    hook-loop-tape's `sew_margin` describes on the solid.
    """
    ln = TAPE_RUN
    w = tape_width + 24.0
    return fc.Piece(
        "placket",
        [
            fc.Edge("outer", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("top_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("tape_edge", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("bottom_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("tape_edge", 0.0, "waistband end"),
                 fc.Notch("tape_edge", 0.5, "mid-tape segment break")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=[fc.Internal("tape-footprint",
                               [fc.P(12.0, w - 12.0), fc.P(ln - 12.0, w - 12.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hook-and-loop carrier placket",
    )


def build():
    pattern = fc.PatternSet("side-opening-trousers")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "band":
        pattern.add(build_band())
    if everything or target_piece == "placket":
        pattern.add(build_placket())

    if everything:
        # The load-bearing solve: the two open side edges are the tape carriers.
        pattern.declare_seam(("front", "side_open"), ("back", "side_open"), tol=1.0)
        # Inseams sew closed conventionally.
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=6.0)
        # Waistband takes all four waist edges plus its overlap extension.
        pattern.declare_seam(
            ("band", "lower"),
            [("front", "waist"), ("front", "waist"),
             ("back", "waist"), ("back", "waist")],
            tol=1.0, ease=BAND_OVERLAP)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "mid-weight cotton twill", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 74% marker; a soft twill presses flat under the tape."},
        {"item": "hook-and-loop tape", "qty": round(2.0 * TAPE_RUN),
         "unit": "mm_length",
         "note": f"{tape_width:.0f} mm wide, {TAPE_RUN:.0f} mm per side; hooks on the "
                 f"BACK carrier, loops on the front, so an open leg never abrades skin."},
        {"item": "waistband elastic", "qty": round(waist_girth * 0.45), "unit": "mm_length",
         "note": "in the back half of the band only — the front stays flat under a lap belt."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "bar-tack both ends of every tape run; the tape peels there first."},
    ]
    pattern.metadata = {
        "fc300_rank": 245,
        "family": "adaptive",
        "fabric_hint": "popelina-algodon",
        "finished_mm": {
            "outseam": round(outseam_length, 1),
            "front_rise": round(RISE_F, 1),
            "back_rise": round(RISE_B, 1),
            "hem_width_front": round(HEM_Q * 2.0, 1),
            "hem_width_back": round(HEM_Q_BACK * 2.0, 1),
        },
        "solved": {
            "front_side_mm": round(FRONT_SIDE_LEN, 2),
            "back_side_mm": round(BACK_SIDE_LEN, 2),
            "side_delta_mm": round(BACK_SIDE_LEN - FRONT_SIDE_LEN, 3),
            "back_hem_half_solved_mm": round(HEM_Q_BACK, 2),
            "tape_run_mm": round(TAPE_RUN, 2),
            "note": "the back hem half-width was BISECTED until the back's open side "
                    "edge measured equal to the front's, because two tape carriers of "
                    "unequal length cannot lie flat when pressed shut.",
        },
        "adaptive": {
            "dressing": "lay flat, transfer on, press the sides shut — no standing, "
                        "no stepping in, no fly, no button",
            "seated_rise_extra_mm": round(seat_rise_extra, 1),
        },
        "hardware": "hook-and-loop tape via Yantra4D (notion.hardware_ref -> hook-loop-tape); "
                    "the solid's strip_length is driven by this trouser's measured open "
                    "outseam and its strip_width by tape_width",
    }
    return pattern


result = build()

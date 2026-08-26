"""
Wide-Leg Jean — Fashion Cabinet Garment Cartridge (FC-400 #304, denim, T2).

The wide straight jean: a single front pleat off the waist, a full leg that falls
straight from the hip, and a deep turn-up. The wide leg is not a scaled straight
jean — the extra width is added AT THE HEM AND KNEE, not at the hip, so the seat
still fits while the leg falls clean; and the front pleat's depth is taken out of
the waist so the waistband still closes at the measured girth.

Three things are solved by measurement rather than by formula:

  1. THE PLEAT DEPTH IS RECONCILED WITH THE WAISTBAND. A front pleat adds cloth at
     the waist edge of the leg, but the waistband is cut to the MEASURED waist —
     so the pleat is FOLDED OUT before the waist run is measured, and the band is
     cut to the folded (finished) waist, not the flat one. A band cut to the flat
     waist is loose by the whole pleat depth on both fronts.

  2. THE TWO INSEAMS ARE BALANCED TO ZERO. As on any straight jean, front and
     back inseams must MEASURE the same or the wide leg twists and its felled
     outseam ripples — worse here, because there is more leg to twist. The front
     inseam's bulge is bisected until it measures the back's.

  3. THE HEM WIDTH IS CLAMPED ABOVE THE KNEE. A wide-leg jean whose hem is drafted
     narrower than the knee is a peg-leg by accident; and a hem taken absurdly
     wide past the fabric width is a piece that will not lay flat. Both the hem
     and the knee are clamped and reported.

DENIM CONVENTIONS, per the family (jeans-5-pocket, selvedge-jean): a 7 mm
twin-needle topstitch gauge; the outseam felled; every hard good a Yantra4D
reference. The JEANS-BUTTON SOLID is Yantra4D territory (`jeans-button`; see
notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres) ─────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front_leg|back_leg|waistband|fly|pocket_bag|set

waist_girth = float(PARAM(lambda: waist_girth, 840.0))
hip_girth = float(PARAM(lambda: hip_girth, 1020.0))
inside_leg = float(PARAM(lambda: inside_leg, 820.0))
front_rise = float(PARAM(lambda: front_rise, 300.0))
hem_width = float(PARAM(lambda: hem_width, 300.0))       # wide flat leg opening
knee_width = float(PARAM(lambda: knee_width, 300.0))
pleat_depth = float(PARAM(lambda: pleat_depth, 40.0))    # front pleat, folded out
band_depth = float(PARAM(lambda: band_depth, 42.0))
button_head = float(PARAM(lambda: button_head, 17.0))
wear_ease = float(PARAM(lambda: wear_ease, 60.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 45.0))  # deep turn-up

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(560.0, min(waist_girth, 1200.0))
hip_girth = max(720.0, min(hip_girth, 1400.0))
inside_leg = max(560.0, min(inside_leg, 950.0))
front_rise = max(220.0, min(front_rise, 380.0))
hem_width = max(220.0, min(hem_width, 460.0))
knee_width = max(200.0, min(knee_width, 440.0))
pleat_depth = max(0.0, min(pleat_depth, 90.0))
band_depth = max(28.0, min(band_depth, 64.0))
button_head = max(11.0, min(button_head, 24.0))
wear_ease = max(0.0, min(wear_ease, 160.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(28.0, min(hem_allowance, 75.0))

TOPSTITCH = 7.0

# ── Derived block dimensions, clamped ────────────────────────────────────────
QUARTER_HIP = (hip_girth + wear_ease) / 4.0
BACK_RISE = max(front_rise + 45.0, front_rise * 1.13)
_QUARTER_WAIST_RAW = (waist_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.62, min(_QUARTER_WAIST_RAW, QUARTER_HIP - 6.0))
# The hem is clamped no narrower than the knee (else it is a peg-leg by accident).
HALF_HEM = max(knee_width, hem_width) / 2.0
HALF_KNEE = min(knee_width, hem_width) / 2.0
FORK_F = max(20.0, QUARTER_HIP * 0.14)
FORK_B = max(34.0, QUARTER_HIP * 0.22)
FLY_LAP = max(30.0, button_head * 2.0)
# The pleat adds to the flat front-waist run; folded out, the finished waist run
# is the quarter waist. So the flat waist edge is quarter + pleat, and the band
# is measured off the FOLDED (finished) waist. Clamped so it can't exceed the hip.
FLAT_FRONT_WAIST = min(QUARTER_WAIST + pleat_depth, QUARTER_HIP + FORK_F - 10.0)


def _button_ring(label, x, y):
    r = button_head / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


# ── Inseams solved to equal length ───────────────────────────────────────────
def _front_inseam(bulge):
    return fc.Edge("inseam", [fc.curve_through(
        fc.P(QUARTER_HIP + FORK_F, front_rise), fc.P(HALF_HEM, 0.0),
        bulge=bulge, side=-1.0)])


_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, BACK_RISE), fc.P(HALF_HEM, 0.0), bulge=0.0, side=-1.0)])
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
    """Front leg, cut 2 mirrored. Wide straight leg, one waist pleat folded out."""
    p_hem_side = fc.P(0.0, 0.0)
    p_knee_side = fc.P((HALF_HEM - HALF_KNEE), inside_leg * 0.48)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(FLAT_FRONT_WAIST, front_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_F, front_rise)
    edges = [
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
    # The pleat, folded out at the waist. Marked as a fold pair so the finished
    # waist run equals the quarter waist and the band closes.
    pleat_x = FLAT_FRONT_WAIST * 0.55
    internals = [
        fc.Internal("outseam topstitch",
                    [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, front_rise)],
                    kind="trace"),
        fc.Internal("front pleat (fold out)",
                    [fc.P(pleat_x, front_rise),
                     fc.P(pleat_x, front_rise - front_rise * 0.30)],
                    kind="marking"),
        fc.Internal("front pleat (fold to)",
                    [fc.P(pleat_x + pleat_depth, front_rise),
                     fc.P(pleat_x + pleat_depth, front_rise - front_rise * 0.30)],
                    kind="marking"),
        fc.Internal("front pocket placement",
                    [fc.P(FLAT_FRONT_WAIST * 0.30, front_rise - seam_allowance),
                     fc.P(FLAT_FRONT_WAIST - seam_allowance, front_rise - seam_allowance),
                     fc.P(FLAT_FRONT_WAIST - seam_allowance,
                          front_rise - front_rise * 0.42),
                     fc.P(FLAT_FRONT_WAIST * 0.30, front_rise - seam_allowance)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF / fly match"),
                 fc.Notch("side", 0.48, "knee level"),
                 fc.Notch("inseam", 0.5, "inseam balance"),
                 fc.Notch("waist", 0.55, "pleat")],
        grainline=fc.Grainline(fc.P(HALF_HEM * 0.7, inside_leg * 0.08),
                               fc.P(HALF_HEM * 0.7, front_rise * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    """Back leg, cut 2 mirrored. Rise at CB; both side seams equal length."""
    p_hem_side = fc.P(0.0, 0.0)
    p_knee_side = fc.P((HALF_HEM - HALF_KNEE), inside_leg * 0.48)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, BACK_RISE)
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
        grainline=fc.Grainline(fc.P(HALF_HEM * 0.7, inside_leg * 0.08),
                               fc.P(HALF_HEM * 0.7, BACK_RISE * 0.9)),
        internals=[
            fc.Internal("outseam topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, front_rise)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


_FL = build_front_leg()
_BL = build_back_leg()
# The FINISHED front waist run is the flat run less the pleat depth (the pleat is
# folded out). The band is cut to the finished waist, never the flat one.
FLAT_FRONT_RUN = _FL.edge("waist").length(0.05)
FINISHED_FRONT_RUN = FLAT_FRONT_RUN - pleat_depth
BACK_WAIST_RUN = _BL.edge("waist").length(0.05)
BAND_LENGTH = (2.0 * FINISHED_FRONT_RUN + 2.0 * BACK_WAIST_RUN
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
                        [fc.P(TOPSTITCH, TOPSTITCH), fc.P(ln - TOPSTITCH, TOPSTITCH)],
                        kind="trace"),
            _button_ring("jeans button seat", button_x, w / 2.0),
            fc.Internal("buttonhole (CF end)",
                        [fc.P(seam_allowance + a, w / 2.0 - a * 1.4),
                         fc.P(seam_allowance + a, w / 2.0 + a * 1.4)], kind="cut"),
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
                         fc.P(lap * 0.1, depth * 0.10)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Fly shield / facing (cut 2)",
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
    pattern = fc.PatternSet("wide-leg-jean")
    everything = target_piece == "set"
    want = {
        "front_leg": everything or target_piece == "front_leg",
        "back_leg": everything or target_piece == "back_leg",
        "waistband": everything or target_piece == "waistband",
        "fly": everything or target_piece == "fly",
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
    if want["pocket_bag"]:
        pattern.add(build_pocket_bag())

    if want["front_leg"] and want["back_leg"]:
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=0.4)
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "mezclilla-denim, 12 oz (407 gsm)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; a wide leg is a "
                 f"cloth-hungry cut — mind the marker."},
        {"item": "jeans button (tack-set, non-sew)", "qty": 1, "unit": "set",
         "note": f"Yantra4D jeans-button (notion.hardware_ref) at a "
                 f"{button_head:.0f} mm head, stepped in off the band's finished end."},
        {"item": "rivet + burr", "qty": 4, "unit": "set",
         "note": "front pocket corners; marked, not modelled."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm; deep turn-up hem."},
    ]
    pattern.metadata = {
        "fc400_rank": 304,
        "family": "denim",
        "tier": 2,
        "fabric_hint": "denim-12oz",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(front_rise, 1),
            "back_rise": round(BACK_RISE, 1),
            "hem_width": round(HALF_HEM * 2.0, 1),
            "knee_width": round(HALF_KNEE * 2.0, 1),
            "band_length": round(BAND_LENGTH, 1),
            "pleat_depth": round(pleat_depth, 1),
        },
        "solved": {
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "flat_front_waist_run_mm": round(FLAT_FRONT_RUN, 2),
            "pleat_depth_mm": round(pleat_depth, 2),
            "finished_front_waist_run_mm": round(FINISHED_FRONT_RUN, 2),
            "band_length_measured_mm": round(BAND_LENGTH, 2),
            "hem_clamped_above_knee": bool(HALF_HEM >= HALF_KNEE),
            "quarter_waist_requested_mm": round(_QUARTER_WAIST_RAW, 2),
            "quarter_waist_clamped_mm": round(QUARTER_WAIST, 2),
            "quarter_waist_was_clamped": bool(
                abs(QUARTER_WAIST - _QUARTER_WAIST_RAW) > 0.01),
            "note": "the pleat is FOLDED OUT before the waist run is measured, so "
                    "the band is cut to the finished (folded) waist, not the flat "
                    "one — a band cut flat is loose by the whole pleat depth on "
                    "both fronts. The two inseams are bisected to equal length "
                    "(more leg to twist here), and the hem is clamped no narrower "
                    "than the knee so a wide-leg jean cannot become a peg-leg by "
                    "accident.",
        },
        "topstitch": f"twin-needle heavy contrast (gold) at {TOPSTITCH:.0f} mm",
        "hardware": "jeans button via Yantra4D (notion.hardware_ref -> jeans-button); "
                    "the solid's head_dia is fed from this garment's button_head, "
                    "which also sets the button's step-in from the band's finished "
                    "end. The four rivets are marked; one bridged solid per notion.",
    }
    return pattern


result = build()

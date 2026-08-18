"""
Bermuda Shorts — FC-100 rank #83. Fashion Cabinet Garment Cartridge.

Tailored woven shorts on the chino trouser block, cut to just-above-the-knee:
front/back legs (cut 2 each) with the front inseam bowed by a solved amount to
match the deeper back fork, a grown-on fly extension on the upper front crotch
edge with a fly J-topstitch guide and a fly-stop notch, a diagonal slash-pocket
opening from waist to side, pressed front/back crease lines, two back waist
darts plus a back-pocket placement rectangle, a two-piece waistband
(left/right halves) whose bottom edge carries the closure overlap as declared
seam ease, five belt-loop strips, and an optional turn-up cuff carried as a
hem allowance with a fold-line marking on each leg.

Bermudas are essentially chinos cropped to bermuda length (inseam ~180–280 mm),
so the front-inseam solver, grown-on fly and two-piece waistband are mirrored
straight from the chinos cartridge; the turn-up cuff convention is borrowed
from the denim-shorts cartridge.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
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


target_piece = str(PARAM(lambda: target_piece, "set"))

hip_girth      = float(PARAM(lambda: hip_girth, 1000.0))
waist_girth    = float(PARAM(lambda: waist_girth, 860.0))
inseam_length  = float(PARAM(lambda: inseam_length, 230.0))   # bermuda length
front_rise     = float(PARAM(lambda: front_rise, 265.0))
back_rise      = float(PARAM(lambda: back_rise, 305.0))
woven_ease     = float(PARAM(lambda: woven_ease, 100.0))
hem_width      = float(PARAM(lambda: hem_width, 175.0))        # front half-hem, flat
fly_width      = float(PARAM(lambda: fly_width, 38.0))
fly_depth      = float(PARAM(lambda: fly_depth, 200.0))
cuff_depth     = float(PARAM(lambda: cuff_depth, 0.0))         # turn-up cuff fold
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 35.0))

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(500.0, min(waist_girth, hip_girth))
inseam_length = max(180.0, min(inseam_length, 320.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
woven_ease = max(40.0, min(woven_ease, 400.0))
hem_width = max(140.0, min(hem_width, 300.0))
fly_width = max(20.0, min(fly_width, 60.0))
fly_depth = max(80.0, min(fly_depth, front_rise - 30.0))
cuff_depth = max(0.0, min(cuff_depth, 60.0))

HIP_E = hip_girth + woven_ease
WAIST_E = waist_girth + 40.0                 # waist wearing ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
HIP_LINE_Y = CROTCH_Y + front_rise * 0.4
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
# Bermuda length crops the leg to just above the knee, so the fork is a much
# larger fraction of the (short) inseam than on a full trouser. A full-trouser
# back fork (HIP_E/8) would throw the back tip far out in x; a shorts-scaled
# fork keeps both tips close and the inseams short enough to match.
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 16.0 + 40.0
FHW = hem_width                              # front half-hem (flat); back solved
FRONT_BULGE = 0.12                           # gentle chino-style front-inseam bow

DART_INTAKE, DART_LEN = 12.0, 80.0
OVERLAP = 40.0                               # waistband closure underlap/overlap
BAND_H = 40.0                                # finished waistband height (folded)
LOOP_W, LOOP_H = 12.0, 55.0
POCKET_W, POCKET_H = 130.0, 140.0


def _fly_j(fw_in):
    """Fly J-topstitch guide: vertical run inside CF hooking toward the fly stop."""
    jx = fw_in - fly_width
    cy = WAIST_Y - fly_depth + fly_width + 10.0
    pts = [fc.P(jx, WAIST_Y), fc.P(jx, cy)]
    for step in range(1, 7):
        a = math.radians(180.0 + 15.0 * step)
        pts.append(fc.P(fw_in + fly_width * math.cos(a), cy + fly_width * math.sin(a)))
    return fc.Internal("fly J topstitch", pts, kind="trace")


def _slash_pocket():
    """Slash-pocket opening: ~150 mm diagonal from the waist to the side seam."""
    return fc.Internal(
        "slash pocket opening",
        [fc.P(55.0, WAIST_Y), fc.P(0.0, WAIST_Y - 140.0)],
    )


def _crease(hem_half, label):
    """Pressed crease: vertical at leg center, hem to hip line."""
    x = hem_half / 2.0
    return fc.Internal(label, [fc.P(x, 0.0), fc.P(x, HIP_LINE_Y)])


def _cuff_fold(hem_half, label):
    """Turn-up cuff fold line, parallel to the hem, only when cuff_depth > 0."""
    return fc.Internal(
        label,
        [fc.P(0.0, cuff_depth), fc.P(hem_half, cuff_depth)],
        kind="trace",
    )


def _back_dart(bw_run, rise_delta, frac, label):
    """Back waist dart as an internal: legs on the waist line, apex below."""
    slope = rise_delta / bw_run
    cx = bw_run * frac
    half = DART_INTAKE / 2.0
    return fc.Internal(
        label,
        [fc.P(cx - half, WAIST_Y + (cx - half) * slope),
         fc.P(cx, WAIST_Y + cx * slope - DART_LEN),
         fc.P(cx + half, WAIST_Y + (cx + half) * slope)],
        kind="dart",
    )


def _back_pocket():
    """Back-pocket placement rectangle, set below the darts."""
    cx = BW * 0.5
    top = WAIST_Y - 90.0
    corners = [
        fc.P(cx - POCKET_W / 2.0, top - POCKET_H),
        fc.P(cx + POCKET_W / 2.0, top - POCKET_H),
        fc.P(cx + POCKET_W / 2.0, top),
        fc.P(cx - POCKET_W / 2.0, top),
    ]
    return fc.Internal("back pocket placement", corners + corners[:1])


def build_legs():
    fw_in = max(FW * 0.55, min(WAIST_E / 4.0, FW * 0.95))
    bw_run = max(BW * 0.55, min(WAIST_E / 4.0 + 2.0 * DART_INTAKE, BW * 0.95))
    rise_delta = back_rise - front_rise
    cb_y = WAIST_Y + rise_delta
    f_tip = fc.P(FW + FORK_F, CROTCH_Y)
    b_tip = fc.P(BW + FORK_B, CROTCH_Y)

    # Front inseam: a gentle chino-style bow (fixed, modest) toward the front
    # hem. Its length is the target the back inseam must match.
    bulge = FRONT_BULGE
    f_inseam = fc.Edge(
        "inseam",
        [fc.curve_through(f_tip, fc.P(FHW, 0.0), bulge=bulge, side=-1.0)],
    )
    front_len = f_inseam.length(0.05)

    # Back inseam: solve the back hem width so the straighter, deeper back fork
    # matches the front inseam length exactly (shorts method). A narrower back
    # hem lengthens the diagonal, so length grows monotonically as BHW shrinks.
    def b_inseam_of(bhw):
        return fc.Edge(
            "inseam",
            [fc.curve_through(b_tip, fc.P(bhw, 0.0), bulge=0.0, side=-1.0)],
        )

    lo, hi = 90.0, FHW + 60.0
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if b_inseam_of(mid).length(0.05) > front_len:
            lo = mid
        else:
            hi = mid
    BHW = (lo + hi) / 2.0
    b_inseam = b_inseam_of(BHW)
    if abs(b_inseam.length(0.05) - front_len) > 1.0:
        raise ValueError("back-hem inseam solver did not converge")
    if BHW < 120.0:
        raise ValueError("solved back hem width degenerate; widen hem_width")

    # Front crotch: line down the grown-on fly extension, then a bezier that
    # rejoins the fork curve smoothly (tangent-continuous at the fly stop).
    fx = fw_in + fly_width
    fly_knee = fc.P(fx, WAIST_Y - fly_depth)
    fork_drop = (WAIST_Y - fly_depth) - CROTCH_Y
    front_crotch = fc.Edge(
        "crotch",
        [
            fc.Line(fc.P(fx, WAIST_Y), fly_knee),
            fc.Bezier(
                fly_knee,
                fc.P(fx, fly_knee.y - fork_drop * 0.5),
                fc.P(fx + (f_tip.x - fx) * 0.4, CROTCH_Y + fork_drop * 0.38),
                f_tip,
            ),
        ],
    )
    fly_frac = fly_depth / front_crotch.length(0.05)

    f_internals = [_fly_j(fw_in), _slash_pocket(), _crease(FHW, "front crease")]
    if cuff_depth > 0.0:
        f_internals.append(_cuff_fold(FHW, "front cuff fold"))
    front = fc.Piece(
        "front",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(fx, WAIST_Y))]),
            front_crotch,
            f_inseam,
            fc.Edge("hem", [fc.Line(fc.P(FHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[
            fc.Notch("crotch", fly_frac, "fly stop"),
            fc.Notch("side", 0.5),
            fc.Notch("inseam", 0.5),
        ],
        grainline=fc.Grainline(fc.P(FW * 0.45, WAIST_Y * 0.12),
                               fc.P(FW * 0.45, WAIST_Y * 0.92)),
        internals=f_internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Leg",
    )

    back_crotch = fc.Edge(
        "crotch",
        [fc.Bezier(fc.P(bw_run, cb_y), fc.P(BW - 4.0, cb_y - front_rise * 0.45),
                   fc.P(BW + (b_tip.x - BW) * 0.35, CROTCH_Y + 55.0), b_tip)],
    )
    b_internals = [_back_dart(bw_run, rise_delta, 0.35, "back dart 1"),
                   _back_dart(bw_run, rise_delta, 0.62, "back dart 2"),
                   _back_pocket(), _crease(BHW, "back crease")]
    if cuff_depth > 0.0:
        b_internals.append(_cuff_fold(BHW, "back cuff fold"))
    back = fc.Piece(
        "back",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(bw_run, cb_y))]),
            back_crotch,
            b_inseam,
            fc.Edge("hem", [fc.Line(fc.P(BHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(BW * 0.45, WAIST_Y * 0.12),
                               fc.P(BW * 0.45, WAIST_Y * 0.92)),
        internals=b_internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Leg",
    )
    return front, back, bulge, BHW


def build_waistband(front, back):
    """Straight waistband half: fronts+backs waists plus overlap and closures."""
    waists = front.edge("waist").length() + back.edge("waist").length()
    length = waists + OVERLAP + 2.0 * seam_allowance
    band_h = 2.0 * (BAND_H + seam_allowance)
    cy = band_h / 2.0
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        internals=[fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)])],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Waistband (half)",
    )


def build_belt_loop():
    """Belt-loop strip, cut five."""
    return fc.Piece(
        "belt_loop",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(LOOP_W, 0.0))]),
            fc.Edge("side_b", [fc.Line(fc.P(LOOP_W, 0.0), fc.P(LOOP_W, LOOP_H))]),
            fc.Edge("top", [fc.Line(fc.P(LOOP_W, LOOP_H), fc.P(0.0, LOOP_H))]),
            fc.Edge("side_a", [fc.Line(fc.P(0.0, LOOP_H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(LOOP_W / 2.0, LOOP_H * 0.15),
                               fc.P(LOOP_W / 2.0, LOOP_H * 0.85)),
        cut=fc.CutSpec(quantity=5),
        label="Belt Loop",
    )


def build():
    pattern = fc.PatternSet("bermuda-shorts")
    front, back, inseam_bulge, back_hem_half = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "waistband":
        pattern.add(build_waistband(front, back))
    if everything or target_piece == "belt_loop":
        pattern.add(build_belt_loop())
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        # The front/back fork seams are NOT declared as a single balanced edge:
        # the front "crotch" edge carries the grown-on fly extension, which folds
        # back as the fly facing rather than being sewn to the back fork. Only the
        # fork below the fly-stop notch joins the back crotch, and the kernel's
        # seam check compares whole named edges, so declaring front.crotch ↔
        # back.crotch would assert a false balance (the fly extension length).
        pattern.declare_seam(
            [("waistband", "bottom")],
            [("front", "waist"), ("back", "waist")],
            tol=2.5,
            ease=OVERLAP + 2.0 * seam_allowance,
        )

    # Fabric estimate: two legs side by side on a 1450 mm poplin width, plus the
    # waistband strip and loops. Height ~ waist rise + hem allowance + margins.
    leg_len_m = (WAIST_Y + hem_allowance + 60.0) / 1000.0
    band_len_m = (2.0 * (front.edge("waist").length() + back.edge("waist").length())
                  + OVERLAP + 4.0 * seam_allowance + 40.0) / 1000.0
    yardage_m = round(leg_len_m + band_len_m + 0.15, 2)
    pattern.bom = [
        {"item": "Cotton poplin (popelina-algodon), 1450 mm face width",
         "qty": yardage_m, "unit": "m",
         "note": "two legs side by side + waistband strip + belt loops; add nap/shrinkage margin"},
        {"item": "Fusible waistband interfacing", "qty": round(band_len_m, 2), "unit": "m",
         "note": "one strip along the two-piece waistband"},
        {"item": "Trouser hook-and-bar closure", "qty": 1, "unit": "set",
         "note": "hardware = Yantra4D ref (hardware_ref: trouser-hook-bar); not modelled here"},
        {"item": "Fly zipper, ~150 mm brass trouser tape", "qty": 1, "unit": "ea",
         "note": "hardware = Yantra4D ref (hardware_ref: trouser-fly-zip); or a fly button"},
        {"item": "Waistband closure button", "qty": 1, "unit": "ea",
         "note": "hardware = Yantra4D ref (hardware_ref: trouser-waist-button); on the overlap"},
        {"item": "All-purpose polyester thread", "qty": 1, "unit": "spool",
         "note": "construction + edgestitch; topstitch thread optional for the fly J and loops"},
    ]

    pattern.metadata = {
        "fc100_rank": 83,
        "fabric_hint": "popelina-algodon",
        "inseam_length_mm": round(inseam_length, 1),
        "front_hem_half_mm": round(FHW, 1),
        "back_hem_half_mm": round(back_hem_half, 1),
        "front_inseam_bulge": round(inseam_bulge, 4),
        "waistband_overlap_mm": OVERLAP,
        "cuff_depth_mm": round(cuff_depth, 1),
        "drafting": (
            "bermuda = chino block cropped to just-above-the-knee; grown-on fly; "
            "gentle front bow with a solved back hem; optional turn-up cuff"
        ),
        "teaching_grade": (
            "front inseam takes a fixed gentle chino bow; the back hem width is solved by "
            "bisection so the back inseam matches the front within 1 mm; the fly extension "
            "folds back as facing (not a declared seam); darts/pockets/creases/cuff are "
            "placement markings, not cut; hardware federated to Yantra4D"
        ),
    }
    return pattern


result = build()

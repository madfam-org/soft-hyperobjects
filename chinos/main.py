"""
Chinos — FC-100 rank #17. Fashion Cabinet Garment Cartridge.

Tailored woven trouser on the scrubs-pants side-seamed block: front/back legs
(cut 2 each) with the front inseam bowed by a solved amount to match the
deeper back fork, a grown-on fly extension on the upper front crotch edge
with a fly J-topstitch guide and a fly-stop notch, a diagonal slash-pocket
opening from waist to side, pressed front/back crease lines, two back waist
darts plus a back-pocket placement rectangle, a two-piece waistband
(left/right halves) whose bottom edge carries the closure overlap as declared
seam ease, and five belt-loop strips.

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

hip_girth     = float(PARAM(lambda: hip_girth, 1000.0))
waist_girth   = float(PARAM(lambda: waist_girth, 860.0))
inseam_length = float(PARAM(lambda: inseam_length, 760.0))
front_rise    = float(PARAM(lambda: front_rise, 265.0))
back_rise     = float(PARAM(lambda: back_rise, 305.0))
woven_ease    = float(PARAM(lambda: woven_ease, 100.0))
hem_width     = float(PARAM(lambda: hem_width, 105.0))     # front half-hem, flat
fly_width     = float(PARAM(lambda: fly_width, 38.0))
fly_depth     = float(PARAM(lambda: fly_depth, 200.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 35.0))

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(500.0, min(waist_girth, hip_girth))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
woven_ease = max(40.0, min(woven_ease, 400.0))
hem_width = max(80.0, min(hem_width, 260.0))
fly_width = max(20.0, min(fly_width, 60.0))
fly_depth = max(80.0, min(fly_depth, front_rise - 30.0))

HIP_E = hip_girth + woven_ease
WAIST_E = waist_girth + 40.0                 # waist wearing ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
HIP_LINE_Y = CROTCH_Y + front_rise * 0.4
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0

DART_INTAKE, DART_LEN = 12.0, 90.0
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
    """Pressed crease: vertical at leg center, hip line to hem."""
    x = hem_half / 2.0
    return fc.Internal(label, [fc.P(x, 0.0), fc.P(x, HIP_LINE_Y)])


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

    def f_inseam(bulge):
        return fc.Edge(
            "inseam",
            [fc.curve_through(f_tip, fc.P(FHW, 0.0), bulge=bulge, side=-1.0)],
        )

    b_inseam = fc.Edge(
        "inseam",
        [fc.curve_through(b_tip, fc.P(BHW, 0.0), bulge=0.0, side=-1.0)],
    )
    back_len = b_inseam.length(0.05)
    lo, hi = 0.0, 0.35
    for _ in range(44):
        mid = (lo + hi) / 2.0
        if f_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(f_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge")

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

    front = fc.Piece(
        "front",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(fx, WAIST_Y))]),
            front_crotch,
            f_inseam(bulge),
            fc.Edge("hem", [fc.Line(fc.P(FHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[
            fc.Notch("crotch", fly_frac, "fly stop"),
            fc.Notch("side", 0.5),
            fc.Notch("inseam", 0.5),
        ],
        grainline=fc.Grainline(fc.P(FW * 0.45, inseam_length * 0.12),
                               fc.P(FW * 0.45, inseam_length * 0.92)),
        internals=[_fly_j(fw_in), _slash_pocket(), _crease(FHW, "front crease")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Leg",
    )

    back_crotch = fc.Edge(
        "crotch",
        [fc.Bezier(fc.P(bw_run, cb_y), fc.P(BW - 4.0, cb_y - front_rise * 0.45),
                   fc.P(BW + (b_tip.x - BW) * 0.35, CROTCH_Y + 55.0), b_tip)],
    )
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
        grainline=fc.Grainline(fc.P(BW * 0.45, inseam_length * 0.12),
                               fc.P(BW * 0.45, inseam_length * 0.92)),
        internals=[_back_dart(bw_run, rise_delta, 0.35, "back dart 1"),
                   _back_dart(bw_run, rise_delta, 0.62, "back dart 2"),
                   _back_pocket(), _crease(BHW, "back crease")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Leg",
    )
    return front, back


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
    pattern = fc.PatternSet("chinos")
    front, back = build_legs()
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
        pattern.declare_seam(
            [("waistband", "bottom")],
            [("front", "waist"), ("back", "waist")],
            tol=2.5,
            ease=OVERLAP + 2.0 * seam_allowance,
        )
    pattern.metadata = {
        "fc100_rank": 17,
        "fabric_hint": "popelina-algodon",
        "drafting": "chino trouser on the scrubs-pants block; grown-on fly; solved inseam bow",
    }
    return pattern


result = build()

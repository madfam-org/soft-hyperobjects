"""
Athletic Shorts — FC-100 rank #18. Fashion Cabinet Garment Cartridge.

Short-inseam technical shorts with an elastic casing waist. Instead of
bowing the front inseam (the gap is too large at short lengths), the BACK
HEM WIDTH is solved analytically so the straight back inseam equals the
straight front inseam exactly — a third seam-matching strategy in the
commons after bisected curves and derived bands.

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
inseam_length = float(PARAM(lambda: inseam_length, 130.0))
front_rise    = float(PARAM(lambda: front_rise, 260.0))
back_rise     = float(PARAM(lambda: back_rise, 295.0))
sport_ease    = float(PARAM(lambda: sport_ease, 120.0))
hem_width     = float(PARAM(lambda: hem_width, 240.0))    # front half-hem, flat
elastic_width = float(PARAM(lambda: elastic_width, 35.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

hip_girth = max(650.0, min(hip_girth, 1800.0))
inseam_length = max(70.0, min(inseam_length, 350.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 80.0))
sport_ease = max(60.0, min(sport_ease, 350.0))
hem_width = max(160.0, min(hem_width, 340.0))

HIP_E = hip_girth + sport_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0, HIP_E / 12.0


def build_legs():
    f_tip_x = FW + FORK_F
    b_tip_x = BW + FORK_B
    front_len = math.hypot(f_tip_x - hem_width, CROTCH_Y)
    run = math.sqrt(max(front_len**2 - CROTCH_Y**2, 25.0))
    bhw = b_tip_x - run                              # back hem solved analytically
    if bhw < 100.0:
        raise ValueError("solved back hem width degenerate; widen hem_width")

    def make(name, width, tip_x, hem_w, cb_y, label):
        waist_in = width * 0.92
        edges = [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
            fc.Edge(
                "crotch",
                [fc.Bezier(fc.P(waist_in, cb_y), fc.P(width - 4.0, cb_y - front_rise * 0.45),
                           fc.P(width + (tip_x - width) * 0.35, CROTCH_Y + 40.0),
                           fc.P(tip_x, CROTCH_Y))],
            ),
            fc.Edge("inseam", [fc.Line(fc.P(tip_x, CROTCH_Y), fc.P(hem_w, 0.0))]),
            fc.Edge("hem", [fc.curve_through(fc.P(hem_w, 0.0), fc.P(0.0, 0.0),
                                             bulge=0.04, side=-1.0)]),
        ]
        return fc.Piece(
            name, edges,
            seam_allowance=seam_allowance,
            allowances={"hem": hem_allowance},
            notches=[fc.Notch("side", 0.5)],
            grainline=fc.Grainline(fc.P(width * 0.45, WAIST_Y * 0.15),
                                   fc.P(width * 0.45, WAIST_Y * 0.8)),
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("front", FW, f_tip_x, hem_width, WAIST_Y, "Front")
    back = make("back", BW, b_tip_x, bhw, WAIST_Y + (back_rise - front_rise), "Back")
    return front, back


def build_casing(front, back):
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    band_h = 2.0 * (elastic_width + seam_allowance)
    length = circ + 2.0 * seam_allowance
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0), fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Waistband Casing",
    )


def build():
    pattern = fc.PatternSet("athletic-shorts")
    front, back = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "waistband":
        pattern.add(build_casing(front, back))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 18,
        "fabric_hint": "jersey-algodon",
        "drafting": "short technical block; back hem width solved so inseams match",
    }
    return pattern


result = build()

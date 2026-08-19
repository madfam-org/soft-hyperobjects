"""
Painter Pant — Fashion Cabinet Garment Cartridge (FC-200 #167, workwear gap).

The utility painter's trouser: a straight, roomy work pant with the trade's signature
details marked for the maker — a hammer/tool loop on the outer thigh, a double-knee
reinforcement zone, and a long thigh tool pocket — on a side-seamed bottom block. Distinct
from chinos (slim) and cargo-pants (bellows leg pockets) in FC-100: the painter cut is
straight and the marks are the trade's tool carry, not fashion pockets.

Built on the commons' side-seamed bottom block: separate front + back legs (cut 2 each), the
front inseam bow SOLVED by bisection to match the deeper back inseam so the inseam balances,
equal side seams by construction, straight open hem, and a flat waistband from the waist edges.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|waistband|set

hip_girth     = float(PARAM(lambda: hip_girth, 1020.0))
waist_girth   = float(PARAM(lambda: waist_girth, 880.0))
inseam_length = float(PARAM(lambda: inseam_length, 780.0))
front_rise    = float(PARAM(lambda: front_rise, 280.0))
back_rise     = float(PARAM(lambda: back_rise, 320.0))
work_ease     = float(PARAM(lambda: work_ease, 120.0))     # roomy but straight
hem_width     = float(PARAM(lambda: hem_width, 210.0))     # straight leg opening (half)
band_height   = float(PARAM(lambda: band_height, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hip_girth     = max(760.0, min(hip_girth, 1600.0))
waist_girth   = max(600.0, min(waist_girth, 1400.0))
inseam_length = max(500.0, min(inseam_length, 950.0))
front_rise    = max(210.0, min(front_rise, 380.0))
back_rise     = max(240.0, min(back_rise, 430.0))
work_ease     = max(60.0, min(work_ease, 280.0))
hem_width     = max(150.0, min(hem_width, 300.0))
band_height   = max(25.0, min(band_height, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 70.0))

HIP_E = hip_girth + work_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 10.0
KNEE_Y = inseam_length * 0.42                    # double-knee zone centre


def _inseam_edge(width, fork, hem_w):
    fork_tip = fc.P(width + fork, CROTCH_Y)

    def inseam(bulge):
        return fc.Edge("inseam", [fc.curve_through(fork_tip, fc.P(hem_w, 0.0),
                                                   bulge=bulge, side=-1.0)])
    return fork_tip, inseam


def build_legs():
    f_tip, f_inseam = _inseam_edge(FW, FORK_F, FHW)
    b_tip, b_inseam = _inseam_edge(BW, FORK_B, BHW)
    back_len = b_inseam(0.0).length(0.05)
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

    def make(name, width, tip, inseam_edge, hem_w, cb_y, is_front, label):
        waist_in = width * 0.92
        internals = []
        # double-knee reinforcement zone (both legs)
        internals.append(fc.Internal("double-knee",
                                     [fc.P(20.0, KNEE_Y + 90.0), fc.P(width * 0.9, KNEE_Y + 90.0),
                                      fc.P(width * 0.9, KNEE_Y - 90.0), fc.P(20.0, KNEE_Y - 90.0),
                                      fc.P(20.0, KNEE_Y + 90.0)], kind="marking"))
        if is_front:
            # hammer/tool loop on the outer thigh + long tool pocket
            ty = WAIST_Y - front_rise - 60.0
            internals.append(fc.Internal("hammer-loop",
                                         [fc.P(6.0, ty), fc.P(6.0, ty - 120.0)], kind="marking"))
            x0, x1 = width * 0.5, width * 0.9
            y0, y1 = ty - 20.0, ty - 210.0
            internals.append(fc.Internal("tool-pocket",
                                         [fc.P(x0, y0), fc.P(x1, y0), fc.P(x1, y1),
                                          fc.P(x0, y1), fc.P(x0, y0)], kind="marking"))
        edges = [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
            fc.Edge("crotch",
                    [fc.Bezier(fc.P(waist_in, cb_y), fc.P(width - 4.0, cb_y - front_rise * 0.45),
                               fc.P(width + (tip.x - width) * 0.35, CROTCH_Y + 55.0), tip)]),
            inseam_edge,
            fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))]),
        ]
        return fc.Piece(
            name, edges,
            seam_allowance=seam_allowance,
            allowances={"hem": hem_allowance},
            notches=[fc.Notch("inseam", 0.5), fc.Notch("side", 0.5)],
            grainline=fc.Grainline(fc.P(width * 0.45, inseam_length * 0.12),
                                   fc.P(width * 0.45, inseam_length * 0.92)),
            internals=internals,
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("front", FW, f_tip, f_inseam(bulge), FHW, WAIST_Y, True, "Front Leg")
    back = make("back", BW, b_tip, b_inseam(0.0), BHW,
                WAIST_Y + (back_rise - front_rise), False, "Back Leg")
    return front, back


def build_waistband(front, back):
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    length = circ + 60.0                             # + underlap/extension for the closure
    h = band_height * 2.0
    return fc.Piece(
        "waistband",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, h))]),
            fc.Edge("fold", [fc.Line(fc.P(length, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(length * 0.2, h / 2.0), fc.P(length * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Waistband",
    )


def build():
    pattern = fc.PatternSet("painter-pant")
    front, back = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "waistband":
        pattern.add(build_waistband(front, back))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "cotton duck / drill (10-12 oz)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 78% marker; sturdy painter's duck, straight leg."},
        {"item": "double-knee reinforcement fabric", "qty": 1, "unit": "as marked",
         "note": "self or contrast patches over the marked knee zones."},
        {"item": "waistband closure (button + hook)", "qty": 1, "unit": "set",
         "note": "the flat waistband closes at CF; belt loops are the maker's option."},
        {"item": "topstitch + all-purpose thread", "qty": 1, "unit": "set",
         "note": "flat-felled seams and topstitched pockets for wear."},
    ]
    pattern.metadata = {
        "fc200_rank": 167, "family": "workwear_uniforms", "fabric_hint": "lona-algodon",
        "silhouette_note": "A straight, roomy painter's trouser with the trade's marks: a "
            "hammer/tool loop on the outer thigh, a double-knee reinforcement zone, and a long "
            "thigh tool pocket. Front inseam bow solved to the deeper back.",
        "solved": {"hip_ease_total_mm": round(HIP_E, 1), "hem_half_mm": round(hem_width, 1),
                   "knee_y_mm": round(KNEE_Y, 1)},
    }
    return pattern


result = build()

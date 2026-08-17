"""
Scrubs Pants — FC-100 rank #86. Fashion Cabinet Garment Cartridge.

Straight woven pant on the sweatpants block for the workwear/uniforms family:
separate front and back legs (cut 2 each), deeper back fork with the front
inseam bowed outward by a solved amount to match, equal side seams by
construction, wide straight open hems, a drawstring waistband casing with a
drawstring-exit cross mark at its center, and a back patch-pocket placement
marking set high on the back leg.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
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

hip_girth     = float(PARAM(lambda: hip_girth, 1000.0))
inseam_length = float(PARAM(lambda: inseam_length, 740.0))
front_rise    = float(PARAM(lambda: front_rise, 275.0))
back_rise     = float(PARAM(lambda: back_rise, 315.0))
woven_ease    = float(PARAM(lambda: woven_ease, 160.0))
hem_width     = float(PARAM(lambda: hem_width, 140.0))     # front half-hem, flat
elastic_width = float(PARAM(lambda: elastic_width, 30.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

hip_girth = max(650.0, min(hip_girth, 1800.0))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
woven_ease = max(60.0, min(woven_ease, 400.0))
hem_width = max(90.0, min(hem_width, 260.0))

HIP_E = hip_girth + woven_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0

POCKET_W, POCKET_H = 140.0, 150.0


def _leg(name, width, fork, hem_w, waist_y_cb, label):
    waist_in_x = width * 0.92
    fork_tip = fc.P(width + fork, CROTCH_Y)

    def inseam(bulge):
        return fc.Edge(
            "inseam",
            [fc.curve_through(fork_tip, fc.P(hem_w, 0.0), bulge=bulge, side=-1.0)],
        )

    return waist_in_x, fork_tip, inseam


def _back_pocket():
    """Patch-pocket placement rectangle, set high on the back leg."""
    cx = BW * 0.5
    top = WAIST_Y - 80.0
    corners = [
        fc.P(cx - POCKET_W / 2.0, top - POCKET_H),
        fc.P(cx + POCKET_W / 2.0, top - POCKET_H),
        fc.P(cx + POCKET_W / 2.0, top),
        fc.P(cx - POCKET_W / 2.0, top),
    ]
    return fc.Internal("back pocket placement", corners + corners[:1])


def build_legs():
    fw_in, f_tip, f_inseam = _leg("front", FW, FORK_F, FHW, WAIST_Y, "Front Leg")
    bw_in, b_tip, b_inseam = _leg("back", BW, FORK_B, BHW, WAIST_Y + (back_rise - front_rise),
                                  "Back Leg")
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

    def make(name, width, waist_in, tip, inseam_edge, hem_w, cb_y, label, internals=None):
        edges = [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
            fc.Edge(
                "crotch",
                [fc.Bezier(fc.P(waist_in, cb_y), fc.P(width - 4.0, cb_y - front_rise * 0.45),
                           fc.P(width + (tip.x - width) * 0.35, CROTCH_Y + 55.0), tip)],
            ),
            inseam_edge,
            fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))]),
        ]
        return fc.Piece(
            name,
            edges,
            seam_allowance=seam_allowance,
            allowances={"hem": hem_allowance},
            notches=[fc.Notch("inseam", 0.5), fc.Notch("side", 0.5)],
            grainline=fc.Grainline(fc.P(width * 0.45, inseam_length * 0.12),
                                   fc.P(width * 0.45, inseam_length * 0.92)),
            internals=internals,
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("front", FW, fw_in, f_tip, f_inseam(bulge), FHW, WAIST_Y, "Front Leg")
    back = make("back", BW, bw_in, b_tip, b_inseam(0.0), BHW,
                WAIST_Y + (back_rise - front_rise), "Back Leg",
                internals=[_back_pocket()])
    return front, back


def build_casing(front, back):
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    band_h = 2.0 * (elastic_width + seam_allowance)
    length = circ + 2.0 * seam_allowance
    cx, cy, half = length / 2.0, band_h / 2.0, 4.0
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
        internals=[
            fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)]),
            fc.Internal("drawstring-exit-h", [fc.P(cx - half, cy), fc.P(cx + half, cy)],
                        kind="drill"),
            fc.Internal("drawstring-exit-v", [fc.P(cx, cy - half), fc.P(cx, cy + half)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Waistband Casing (drawstring)",
    )


def build():
    pattern = fc.PatternSet("scrubs-pants")
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
        "fc100_rank": 86,
        "fabric_hint": "popelina-algodon",
        "drafting": "straight woven scrub pant on the sweatpants block; solved inseam bow",
    }
    return pattern


result = build()

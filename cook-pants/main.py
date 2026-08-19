"""
Cook Pants — Fashion Cabinet Garment Cartridge (FC-200 #166, workwear gap).

The baggy pull-on kitchen trouser: a roomy, straight, elastic-waist pant cut for long shifts
on your feet — generous through the hip and thigh, a full straight leg (no athletic taper),
an elastic (optionally drawcord) waistband casing, and a marked deep side patch pocket for a
side-towel. Distinct from the athletic joggers/sweatpants (tapered, ribbed cuff) in FC-100.

Built on the commons' side-seamed bottom block: separate front + back legs (cut 2 each), the
front inseam bow SOLVED by bisection to match the deeper back inseam so the inseam balances,
equal side seams by construction, straight open hem, and an elastic casing from the measured
waist edges.

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

hip_girth     = float(PARAM(lambda: hip_girth, 1040.0))    # seat
waist_girth   = float(PARAM(lambda: waist_girth, 860.0))   # (stretched elastic sits here)
inseam_length = float(PARAM(lambda: inseam_length, 740.0))
front_rise    = float(PARAM(lambda: front_rise, 285.0))
back_rise     = float(PARAM(lambda: back_rise, 330.0))
cook_ease     = float(PARAM(lambda: cook_ease, 220.0))     # generous baggy ease
hem_width     = float(PARAM(lambda: hem_width, 230.0))     # full straight leg opening (half)
elastic_width = float(PARAM(lambda: elastic_width, 45.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hip_girth     = max(760.0, min(hip_girth, 1600.0))
waist_girth   = max(600.0, min(waist_girth, 1400.0))
inseam_length = max(500.0, min(inseam_length, 950.0))
front_rise    = max(210.0, min(front_rise, 380.0))
back_rise     = max(240.0, min(back_rise, 430.0))
cook_ease     = max(100.0, min(cook_ease, 400.0))
hem_width     = max(150.0, min(hem_width, 320.0))
elastic_width = max(25.0, min(elastic_width, 80.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 70.0))

HIP_E = hip_girth + cook_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0


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

    def make(name, width, tip, inseam_edge, hem_w, cb_y, pocket, label):
        waist_in = width * 0.92
        internals = []
        if pocket:
            # deep side-towel patch pocket marked on the outer thigh
            px, py = 20.0, WAIST_Y - front_rise - 120.0
            internals.append(fc.Internal("side-pocket",
                                         [fc.P(px, py), fc.P(px + 170.0, py),
                                          fc.P(px + 170.0, py - 200.0), fc.P(px, py - 200.0),
                                          fc.P(px, py)], kind="marking"))
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
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)]),
                   fc.Internal("drawcord-eyelets", [fc.P(length * 0.46, band_h * 0.75),
                                                    fc.P(length * 0.54, band_h * 0.75)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Waistband Casing",
    )


def build():
    pattern = fc.PatternSet("cook-pants")
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

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "poly-cotton twill or houndstooth kitchen cloth",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 78% marker; durable, washable, full straight leg."},
        {"item": "waistband elastic", "qty": round(waist_girth * 1.05 / 10.0) * 10,
         "unit": "mm_length", "note": "flat elastic in the casing; sits at the natural waist."},
        {"item": "drawcord (optional)", "qty": 1, "unit": "length",
         "note": "through the marked front eyelets for extra hold."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "flat-felled inseam/side for durability."},
    ]
    pattern.metadata = {
        "fc200_rank": 166, "family": "workwear_uniforms", "fabric_hint": "sarga-poli-algodon",
        "silhouette_note": "A roomy, straight, elastic-waist kitchen trouser cut for long "
            "shifts — full leg (no athletic taper), generous ease, and a deep side-towel patch "
            "pocket marked on the thigh. Front inseam bow solved to the deeper back.",
        "solved": {"hip_ease_total_mm": round(HIP_E, 1), "hem_half_mm": round(hem_width, 1)},
    }
    return pattern


result = build()

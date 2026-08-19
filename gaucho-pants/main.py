"""
Gaucho Pants — Fashion Cabinet Garment Cartridge (FC-200 #183, bottoms gap).

The gaucho: a wide, cropped, mid-calf trouser cut so full and straight it reads almost as a
divided skirt — the 1970s riding-inspired wide leg. This cartridge drafts a very wide straight
leg on the side-seamed block, cropped at mid-calf, with a fitted waistband. Distinct from FC-100's
culottes (shorter, more skirt-like) and palazzo pants (full-length) and wide-leg athletic pants —
the gaucho is the specific cropped mid-calf wide cut. The front inseam bow is solved to the back
so the inseam balances.

Pieces:
  - front / back : very wide cropped legs (cut 2 each).
  - waistband    : fitted band solved to the waist.

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

hip_girth     = float(PARAM(lambda: hip_girth, 1000.0))
waist_girth   = float(PARAM(lambda: waist_girth, 780.0))
inseam_length = float(PARAM(lambda: inseam_length, 480.0))  # cropped mid-calf
front_rise    = float(PARAM(lambda: front_rise, 290.0))
back_rise     = float(PARAM(lambda: back_rise, 330.0))
gaucho_ease   = float(PARAM(lambda: gaucho_ease, 140.0))
hem_width     = float(PARAM(lambda: hem_width, 330.0))      # very wide leg opening (half)
band_height   = float(PARAM(lambda: band_height, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hip_girth     = max(760.0, min(hip_girth, 1600.0))
waist_girth   = max(600.0, min(waist_girth, 1400.0))
inseam_length = max(300.0, min(inseam_length, 650.0))
front_rise    = max(220.0, min(front_rise, 400.0))
back_rise     = max(260.0, min(back_rise, 450.0))
gaucho_ease   = max(60.0, min(gaucho_ease, 320.0))
hem_width     = max(230.0, min(hem_width, 460.0))
band_height   = max(25.0, min(band_height, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 70.0))

HIP_E = hip_girth + gaucho_ease
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

    def make(name, width, tip, inseam_edge, hem_w, cb_y, label):
        waist_in = width * 0.92
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
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("front", FW, f_tip, f_inseam(bulge), FHW, WAIST_Y, "Front Leg")
    back = make("back", BW, b_tip, b_inseam(0.0), BHW,
                WAIST_Y + (back_rise - front_rise), "Back Leg")
    return front, back


def build_waistband(front, back):
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    length = circ + 60.0
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
    pattern = fc.PatternSet("gaucho-pants")
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

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "fluid woven with drape (twill, gabardine, linen)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 74% marker; drape gives the wide leg its swing."},
        {"item": "side or back zip + waistband closure", "qty": 1, "unit": "set",
         "note": "the fitted waistband closes at a side or back seam."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "flat, clean seams; a deep hem weights the wide leg."},
    ]
    pattern.metadata = {
        "fc200_rank": 183, "family": "bottoms", "fabric_hint": "gabardina-lino",
        "silhouette_note": "A very wide, cropped mid-calf trouser so full it reads almost as a "
            "divided skirt (1970s gaucho line). Cut on the side-seamed block; the front inseam "
            "bow is solved to the deeper back so the inseam balances.",
        "solved": {"hip_ease_total_mm": round(HIP_E, 1), "hem_half_mm": round(hem_width, 1),
                   "inseam_mm": round(inseam_length, 1)},
    }
    return pattern


result = build()

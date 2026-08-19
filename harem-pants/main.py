"""
Harem Pants — Fashion Cabinet Garment Cartridge (FC-200 #182, bottoms gap).

The dropped-crotch harem pant: a very full, low-crotch trouser gathered onto an elastic waist
and gathered again into narrow ankle cuffs, so the leg blouses dramatically between. Worn across
many cultures (şalvar, harem, patiala). This cartridge drafts a very deep-rise, wide leg on the
side-seamed block with the crotch dropped far below the true fork, an elastic waist casing, and a
narrow ankle cuff solved to the ankle. Distinct from FC-100's joggers/track pants — the dropped
crotch and blousing are the point. The front inseam bow is solved to the back so the inseam
balances.

Pieces:
  - front / back : very full dropped-crotch legs (cut 2 each).
  - waistband    : elastic casing from the measured waist.
  - cuff         : narrow ankle cuff solved to the ankle.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|waistband|cuff|set

hip_girth     = float(PARAM(lambda: hip_girth, 1000.0))
waist_girth   = float(PARAM(lambda: waist_girth, 820.0))
ankle_girth   = float(PARAM(lambda: ankle_girth, 280.0))   # snug cuff
inseam_length = float(PARAM(lambda: inseam_length, 680.0))
front_rise    = float(PARAM(lambda: front_rise, 320.0))
back_rise     = float(PARAM(lambda: back_rise, 380.0))
crotch_drop   = float(PARAM(lambda: crotch_drop, 220.0))   # how far the crotch drops below fork
harem_ease    = float(PARAM(lambda: harem_ease, 400.0))    # very full
elastic_width = float(PARAM(lambda: elastic_width, 45.0))
cuff_height   = float(PARAM(lambda: cuff_height, 60.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hip_girth     = max(760.0, min(hip_girth, 1600.0))
waist_girth   = max(600.0, min(waist_girth, 1400.0))
ankle_girth   = max(200.0, min(ankle_girth, 460.0))
inseam_length = max(450.0, min(inseam_length, 900.0))
front_rise    = max(240.0, min(front_rise, 420.0))
back_rise     = max(280.0, min(back_rise, 480.0))
crotch_drop   = max(80.0, min(crotch_drop, 380.0))
harem_ease    = max(200.0, min(harem_ease, 620.0))
elastic_width = max(25.0, min(elastic_width, 80.0))
cuff_height   = max(30.0, min(cuff_height, 120.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

HIP_E = hip_girth + harem_ease
CROTCH_Y = inseam_length + crotch_drop               # crotch dropped BELOW the natural fork
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 14.0 + 15.0, HIP_E / 7.0 + 20.0
AHW = ankle_girth / 2.0 + 30.0                        # leg pre-gather width at the cuff (half)


def _inseam_edge(width, fork):
    fork_tip = fc.P(width + fork, CROTCH_Y)

    def inseam(bulge):
        return fc.Edge("inseam", [fc.curve_through(fork_tip, fc.P(AHW, 0.0),
                                                   bulge=bulge, side=-1.0)])
    return fork_tip, inseam


def build_legs():
    f_tip, f_inseam = _inseam_edge(FW, FORK_F)
    b_tip, b_inseam = _inseam_edge(BW, FORK_B)
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

    def make(name, width, tip, inseam_edge, cb_y, label):
        waist_in = width * 0.9
        internals = [fc.Internal("ankle-gather", [fc.P(0.0, 20.0), fc.P(AHW, 20.0)],
                                 kind="marking")]
        edges = [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
            fc.Edge("crotch",
                    [fc.Bezier(fc.P(waist_in, cb_y), fc.P(width - 4.0, cb_y - front_rise * 0.4),
                               fc.P(width + (tip.x - width) * 0.3, CROTCH_Y + 70.0), tip)]),
            inseam_edge,
            fc.Edge("hem", [fc.Line(fc.P(AHW, 0.0), fc.P(0.0, 0.0))]),
        ]
        return fc.Piece(
            name, edges,
            seam_allowance=seam_allowance,
            notches=[fc.Notch("inseam", 0.5), fc.Notch("side", 0.5)],
            grainline=fc.Grainline(fc.P(width * 0.4, inseam_length * 0.12),
                                   fc.P(width * 0.4, inseam_length * 0.9)),
            internals=internals,
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("front", FW, f_tip, f_inseam(bulge), WAIST_Y, "Front Leg")
    back = make("back", BW, b_tip, b_inseam(0.0), WAIST_Y + (back_rise - front_rise), "Back Leg")
    return front, back


def build_waistband(front, back):
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
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)])],
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0), fc.P(length * 0.8, band_h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Waistband Casing",
    )


def build_cuff():
    ln = ankle_girth + 30.0
    h = cuff_height * 2.0
    return fc.Piece(
        "cuff",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Ankle cuff",
    )


def build():
    pattern = fc.PatternSet("harem-pants")
    front, back = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "waistband":
        pattern.add(build_waistband(front, back))
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "drapey rayon, challis, or soft cotton",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 76% marker; drape is essential for the blousing."},
        {"item": "waistband + optional cuff elastic", "qty": 1, "unit": "set",
         "note": "elastic at the waist; the ankle cuffs can be elastic or a fitted band."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "gather the wide leg into the narrow ankle cuff."},
    ]
    pattern.metadata = {
        "fc200_rank": 182, "family": "bottoms", "fabric_hint": "rayon-challis",
        "silhouette_note": "A very full dropped-crotch trouser gathered onto an elastic waist and "
            "into narrow ankle cuffs so the leg blouses between (şalvar/harem/patiala line). The "
            "crotch drops below the true fork; the front inseam bow is solved to the back.",
        "solved": {"hip_ease_total_mm": round(HIP_E, 1), "crotch_drop_mm": round(crotch_drop, 1),
                   "ankle_girth_mm": round(ankle_girth, 1)},
    }
    return pattern


result = build()

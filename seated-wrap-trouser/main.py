"""
Seated-wear wrap trouser — Fashion Cabinet Garment Cartridge
(FC-500 rank #437, adaptive, Yantra4D-bridged magnetic-clasp).

A trouser that dresses from a seated position without standing: instead of pulling a waistband
over the hips, the whole front wraps open flat and closes with magnetic clasps, so a wearer who
cannot stand or bear weight lays the trouser under themselves, brings the wrap fronts across, and
the clasps snap shut. The rise is drafted for sitting (taller back, lower front) so the waist
stays level. The clasps are the Yantra4D `magnetic-clasp` solid (notion.hardware_ref); their disc
diameter is driven by the same clasp_diameter that drives the garment's wrap-closure interface —
the dimensional handshake.

Drafting note — the seam that must SOLVE: the front and back SIDE seams must be equal length even
though the front and back rises differ, or the leg twists. The rise difference is taken at the
CENTRE seams; both panels share one measured SIDE_LEN so the side seam matches by construction.
The extra back rise is clamped under the leg-below-waist so the waistline can never invert.

Pieces: front-wrap (cut 2, the overlapping wrap fronts) + back (cut 2 mirrored) + waistband
(cut 1, carries the clasps). Made to measure to waist, hip girths and outseam.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|waistband|set

waist_girth = float(PARAM(lambda: waist_girth, 880.0))
hip_girth = float(PARAM(lambda: hip_girth, 1060.0))
outseam = float(PARAM(lambda: outseam, 980.0))
front_rise = float(PARAM(lambda: front_rise, 240.0))
back_rise_extra = float(PARAM(lambda: back_rise_extra, 90.0))
wrap_overlap = float(PARAM(lambda: wrap_overlap, 150.0))
clasp_diameter = float(PARAM(lambda: clasp_diameter, 24.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1400.0))
hip_girth = max(760.0, min(hip_girth, 1560.0))
outseam = max(700.0, min(outseam, 1200.0))
front_rise = max(180.0, min(front_rise, 340.0))
back_rise_extra = max(30.0, min(back_rise_extra, 160.0))
wrap_overlap = max(80.0, min(wrap_overlap, 260.0))
clasp_diameter = max(14.0, min(clasp_diameter, 40.0))
seam_allowance = max(6.0, min(seam_allowance, 18.0))

hip_girth = max(hip_girth, waist_girth + 40.0)
LEG_BELOW = outseam - front_rise
back_rise_extra = min(back_rise_extra, LEG_BELOW * 0.35)

QUARTER_HIP = hip_girth / 4.0
QUARTER_WAIST = waist_girth / 4.0
WB_DEPTH = 60.0
SIDE_LEN = outseam - WB_DEPTH
HEM_HALF = max(150.0, QUARTER_HIP * 0.62)
FRONT_CENTRE_DROP = front_rise
BACK_CENTRE_RISE = back_rise_extra
CROTCH_Y = SIDE_LEN - front_rise - 50.0
CROTCH_X = -QUARTER_HIP * 0.13
# The wrap adds the overlap to the front centre width so the fronts cross; clamp it under a
# quarter hip so the overlap can never exceed the panel and fold back on itself.
WRAP = min(wrap_overlap, QUARTER_HIP * 0.9)


def build_front():
    """Wrap front (cut 2). Like a trouser front but the centre-front runs out past centre by WRAP
    so the two fronts overlap and close on the clasps. Lower front rise."""
    # The wrap adds width at the WAIST (the front centre runs out past centre by WRAP), but the
    # inseam and crotch are IDENTICAL to the back so the leg cannot twist — the overlap is taken
    # entirely above the crotch, at the wrap_edge, never on the inseam.
    p_hem_in = fc.P(0.0, 0.0)
    p_hem_out = fc.P(HEM_HALF, 0.0)
    p_side_waist = fc.P(HEM_HALF, SIDE_LEN)
    p_cf_waist = fc.P(-WRAP, SIDE_LEN - FRONT_CENTRE_DROP)
    p_crotch = fc.P(CROTCH_X, CROTCH_Y)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_in, p_hem_out)]),
        fc.Edge("side", [fc.Line(p_hem_out, p_side_waist)]),
        fc.Edge("waist", [fc.Line(p_side_waist, p_cf_waist)]),
        fc.Edge("wrap_edge",
                [fc.Bezier(p_cf_waist,
                           fc.P(-WRAP * 0.4, SIDE_LEN - FRONT_CENTRE_DROP - 30.0),
                           fc.P(CROTCH_X - 6.0, CROTCH_Y + 18.0), p_crotch)]),
        fc.Edge("inseam", [fc.Line(p_crotch, p_hem_in)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"hem": 40.0},
        notches=[fc.Notch("side", 0.5, "knee level"), fc.Notch("inseam", 0.5, "knee match")],
        grainline=fc.Grainline(fc.P(HEM_HALF * 0.4, 40.0), fc.P(HEM_HALF * 0.4, SIDE_LEN - 40.0)),
        internals=[fc.Internal("wrap-clasp-line",
                               [fc.P(-WRAP * 0.7, SIDE_LEN - FRONT_CENTRE_DROP - 20.0),
                                fc.P(-WRAP * 0.7, SIDE_LEN - FRONT_CENTRE_DROP - 20.0
                                     - WRAP * 0.6)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Wrap front (low rise)")


def build_back():
    """Trouser back (cut 2 mirrored). Side seam SAME SIDE_LEN; raised centre-back rise."""
    back_hem_half = HEM_HALF
    p_hem_in = fc.P(0.0, 0.0)
    p_hem_out = fc.P(back_hem_half, 0.0)
    p_side_waist = fc.P(back_hem_half, SIDE_LEN)
    p_cb_waist = fc.P(0.0, SIDE_LEN + BACK_CENTRE_RISE)
    p_crotch = fc.P(CROTCH_X, CROTCH_Y)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_in, p_hem_out)]),
        fc.Edge("side", [fc.Line(p_hem_out, p_side_waist)]),
        fc.Edge("waist", [fc.Line(p_side_waist, p_cb_waist)]),
        fc.Edge("centre_back",
                [fc.Bezier(p_cb_waist,
                           fc.P(QUARTER_HIP * 0.24, SIDE_LEN - 20.0),
                           fc.P(QUARTER_HIP * 0.10, CROTCH_Y + 40.0), p_crotch)]),
        fc.Edge("inseam", [fc.Line(p_crotch, p_hem_in)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"hem": 40.0},
        notches=[fc.Notch("side", 0.5, "knee level"), fc.Notch("inseam", 0.5, "knee match")],
        grainline=fc.Grainline(fc.P(back_hem_half * 0.5, 40.0),
                               fc.P(back_hem_half * 0.5, SIDE_LEN - 40.0)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Trouser back (raised rise)")


_FW = build_front().edge("waist").length(0.2)
_BW = build_back().edge("waist").length(0.2)
WAIST_EDGE_SUM = 2.0 * _FW + 2.0 * _BW
WB_OVERLAP = WRAP * 2.0
WB_LENGTH = WAIST_EDGE_SUM + WB_OVERLAP


def build_waistband():
    """The waistband (cut 1, folded) carrying the magnetic clasps at each wrap end."""
    ln, w = WB_LENGTH, WB_DEPTH * 2.0
    return fc.Piece(
        "waistband", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.25, "left side seam"),
                 fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("attach", 0.75, "right side seam")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=[
            fc.Internal("clasp-left", [fc.P(clasp_diameter, w * 0.5),
                                       fc.P(clasp_diameter + WRAP, w * 0.5)], kind="marking"),
            fc.Internal("clasp-right", [fc.P(ln - clasp_diameter - WRAP, w * 0.5),
                                        fc.P(ln - clasp_diameter, w * 0.5)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1), label="Waistband (magnetic clasps)")


def build():
    pattern = fc.PatternSet("seated-wrap-trouser")
    every = target_piece == "set"
    if every or target_piece == "front":
        pattern.add(build_front())
    if every or target_piece == "back":
        pattern.add(build_back())
    if every or target_piece == "waistband":
        pattern.add(build_waistband())
    if every:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.0)
        pattern.declare_seam(("waistband", "attach"),
                             [("front", "waist"), ("front", "waist"),
                              ("back", "waist"), ("back", "waist")],
                             tol=2.0, ease=WB_OVERLAP)
    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton jersey (soft, four-way stretch)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a soft stretch jersey moves with a seated body and lays flat to wrap under."},
        {"item": "magnetic clasps (Yantra4D magnetic-clasp)", "qty": 4, "unit": "piece",
         "note": f"four magnetic clasps, disc_dia {clasp_diameter:.0f} mm = the clasp_diameter "
                 "that drives the wrap-closure interface; the wrap fronts snap shut without a "
                 "button or zip to fumble, closing one-handed from a seated position."},
        {"item": "waistband elastic (back only)", "qty": round(waist_girth * 0.4),
         "unit": "mm_length",
         "note": "a soft elastic across the raised back keeps it level without a hard band."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "flat-fell the inseam so it does not chafe a seated wearer."},
    ]
    pattern.metadata = {
        "fc500_rank": 437, "family": "adaptive", "fabric_hint": "jersey-algodon",
        "finished_mm": {"waist": round(waist_girth, 1), "hip": round(hip_girth, 1),
                        "outseam": round(outseam, 1),
                        "front_rise": round(front_rise, 1),
                        "back_rise": round(front_rise + back_rise_extra, 1)},
        "solved": {
            "side_len_mm": round(SIDE_LEN, 2), "wrap_mm": round(WRAP, 2),
            "back_rise_extra_clamped_mm": round(back_rise_extra, 2),
            "note": "the front and back share ONE measured SIDE_LEN so the side seam matches "
                    "despite the differing rises; the wrap overlap is clamped under 90% of a "
                    "quarter-hip so it can never fold back on itself; the extra back rise is "
                    "clamped under 35% of the leg-below-waist so the waistline can never invert.",
        },
        "adaptive": {
            "dressing": "the whole front wraps open flat and closes on magnetic clasps, so the "
                        "trouser dresses from a seated position without standing or pulling a "
                        "waistband over the hips",
            "posture": "the back rise is taller than the front so the waist stays level seated",
        },
        "hardware": "magnetic clasp closure via Yantra4D (notion.hardware_ref -> magnetic-clasp); "
                    "disc_dia = clasp_diameter, the same parameter that drives this trouser's "
                    "wrap-closure interface (the dimensional handshake).",
    }
    return pattern


result = build()

"""
Braid-side formal trouser — Fashion Cabinet Garment Cartridge
(FC-500 rank #446, tailoring, T3; y4d trouser-hook-bar).

The dress trouser of evening and morning wear: a plain-front (or single-pleat) trouser with a
GALLOON braid down the outside seam — one row of silk braid for morning dress, two for white-tie
— no belt loops, no turn-ups, closing at the waist on a trouser hook and bar. The braid is the
defining feature and is drafted as a marking down the outside seam; the hook-bar is the closure.

Two real decisions:

  1. THE FRONT AND BACK SIDE SEAMS MATCH BY CONSTRUCTION. Both panels share one measured SIDE_LEN
     (the outside seam, where the braid runs), so the braid lands on a seam that closes; the rise
     difference between front and back is taken at the centre seams, and the crotch is ONE shared
     point so the inseams are identical and the leg cannot twist.

  2. THE HOOK-BAR IS SOLVED TO THE WAISTBAND. The trouser hook and bar closes the waistband; its
     hook width is the drafted hook_width that drives the garment's waistband-closure interface
     AND the Yantra4D trouser-hook-bar sew plate.

Pieces: front (cut 2), back (cut 2), waistband (cut 1). T3 tailoring.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|waistband|set

waist_girth = float(PARAM(lambda: waist_girth, 860.0))
hip_girth = float(PARAM(lambda: hip_girth, 1020.0))
outseam = float(PARAM(lambda: outseam, 1080.0))
front_rise = float(PARAM(lambda: front_rise, 280.0))
back_rise_extra = float(PARAM(lambda: back_rise_extra, 40.0))
hem_width = float(PARAM(lambda: hem_width, 210.0))
braid_width = float(PARAM(lambda: braid_width, 25.0))
hook_width = float(PARAM(lambda: hook_width, 32.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1400.0))
hip_girth = max(760.0, min(hip_girth, 1560.0))
outseam = max(900.0, min(outseam, 1260.0))
front_rise = max(220.0, min(front_rise, 360.0))
back_rise_extra = max(10.0, min(back_rise_extra, 120.0))
hem_width = max(150.0, min(hem_width, 300.0))
braid_width = max(8.0, min(braid_width, 50.0))
hook_width = max(20.0, min(hook_width, 50.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

hip_girth = max(hip_girth, waist_girth + 40.0)
LEG_BELOW = outseam - front_rise
back_rise_extra = min(back_rise_extra, LEG_BELOW * 0.35)

QUARTER_HIP = hip_girth / 4.0
QUARTER_WAIST = waist_girth / 4.0
WB_DEPTH = 55.0
SIDE_LEN = outseam - WB_DEPTH
HEM_HALF = max(120.0, hem_width / 2.0)
FRONT_CENTRE_DROP = front_rise
BACK_CENTRE_RISE = back_rise_extra
CROTCH_Y = SIDE_LEN - front_rise - 50.0
CROTCH_X = -QUARTER_HIP * 0.13


def build_front():
    p_hem_in = fc.P(0.0, 0.0)
    p_hem_out = fc.P(HEM_HALF, 0.0)
    p_side_waist = fc.P(HEM_HALF, SIDE_LEN)
    p_cf_waist = fc.P(0.0, SIDE_LEN - FRONT_CENTRE_DROP)
    p_crotch = fc.P(CROTCH_X, CROTCH_Y)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_in, p_hem_out)]),
        fc.Edge("side", [fc.Line(p_hem_out, p_side_waist)]),
        fc.Edge("waist", [fc.Line(p_side_waist, p_cf_waist)]),
        fc.Edge("centre_front",
                [fc.Bezier(p_cf_waist,
                           fc.P(QUARTER_WAIST * 0.14, SIDE_LEN - FRONT_CENTRE_DROP - 30.0),
                           fc.P(QUARTER_WAIST * 0.02, CROTCH_Y + 18.0), p_crotch)]),
        fc.Edge("inseam", [fc.Line(p_crotch, p_hem_in)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"hem": 40.0},
        notches=[fc.Notch("side", 0.5, "knee level"), fc.Notch("inseam", 0.5, "knee match")],
        grainline=fc.Grainline(fc.P(HEM_HALF * 0.5, 40.0), fc.P(HEM_HALF * 0.5, SIDE_LEN - 40.0)),
        internals=[fc.Internal("galloon-braid",
                               [fc.P(HEM_HALF - braid_width * 0.5, 20.0),
                                fc.P(HEM_HALF - braid_width * 0.5, SIDE_LEN - 20.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Front (braid outseam)")


def build_back():
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
        internals=[fc.Internal("galloon-braid",
                               [fc.P(back_hem_half - braid_width * 0.5, 20.0),
                                fc.P(back_hem_half - braid_width * 0.5, SIDE_LEN - 20.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Back (braid outseam, raised rise)")


_FW = build_front().edge("waist").length(0.2)
_BW = build_back().edge("waist").length(0.2)
WB_LENGTH = 2.0 * _FW + 2.0 * _BW + hook_width * 2.0


def build_waistband():
    ln, w = WB_LENGTH, WB_DEPTH * 2.0
    return fc.Piece(
        "waistband", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.25, "left side"), fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("attach", 0.75, "right side")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=[fc.Internal("hook-bar",
                               [fc.P(ln - hook_width, w * 0.5), fc.P(ln, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1), label="Waistband (hook and bar)")


def build():
    pattern = fc.PatternSet("formal-tailcoat-trouser")
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
                             tol=2.0, ease=hook_width * 2.0)
    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "worsted dress trousering", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a fine worsted for evening or morning dress; no belt loops, no turn-ups."},
        {"item": "silk galloon braid", "qty": round(SIDE_LEN * 2.0 + 40.0), "unit": "mm_length",
         "note": f"the {braid_width:.0f} mm braid down each outside seam — one row for morning "
                 "dress, two for white-tie."},
        {"item": "trouser hook and bar (Yantra4D trouser-hook-bar)", "qty": 1, "unit": "piece",
         "note": f"the waistband closure, hook width {hook_width:.0f} mm = the hook_width that "
                 "drives the waistband-closure interface AND the sew plate; the hook-bar solid "
                 "is Yantra4D, never modelled here."},
        {"item": "waistband curtain + lining", "qty": round(WB_LENGTH * 1.2), "unit": "mm_length",
         "note": "a proper curtained waistband so the shirt stays tucked."},
    ]
    pattern.metadata = {
        "fc500_rank": 446, "family": "tailoring", "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "A braid-side formal dress trouser: a galloon braid down each outside "
            "seam, no belt loops or turn-ups, closing on a trouser hook and bar.",
        "hardware": "trouser hook and bar via Yantra4D (notion.hardware_ref -> trouser-hook-bar); "
            "hook_width drives the waistband-closure interface AND the sew plate — the handshake.",
        "solved": {
            "side_len_mm": round(SIDE_LEN, 2), "wb_length_mm": round(WB_LENGTH, 1),
            "note": "the front and back share ONE measured SIDE_LEN so the braided outside seam "
                    "matches; the crotch is ONE shared point so the inseams are identical and the "
                    "leg cannot twist; the extra back rise is clamped under 35% of the leg-below-"
                    "waist so the waistline can never invert.",
        },
        "tailoring": {"cut": "braid-side dress trouser, plain front, no loops/turn-ups, hook-bar."},
    }
    return pattern


result = build()

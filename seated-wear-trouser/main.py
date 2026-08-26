"""
Seated-wear Rise-adjusted Trouser — Fashion Cabinet Garment Cartridge
(FC-400 rank #372, adaptive, Yantra4D-bridged hook-loop-tape).

A trouser cut for a body that sits: the BACK rise is drafted genuinely taller than a standing
trouser and the FRONT rise lower, so the waistband stays level when seated instead of gaping
at the back and cutting at the front. The seat is fuller, the back has no pockets to sit on,
and the side waist closes on hook-and-loop tape so it adjusts one-handed without a button or a
fly to fumble. The tape is the Yantra4D `hook-loop-tape` solid (notion.hardware_ref); its sewn
strip length is driven by the same side_adjust run that drives the garment's waistband
interface — the dimensional handshake.

Drafting note — the seam that must SOLVE: the front and back SIDE seams must be equal length
even though the front and back rises differ, or the leg twists. The rise difference is taken
entirely at the CENTRE seams (front centre lower, back centre higher); both panels share one
measured SIDE_LEN so the side seam matches by construction. The extra back rise is clamped so
it can never exceed the leg below the waist (which would invert the waistline above the hem).

Pieces:
  - front : trouser front (cut 2 mirrored), lower front rise.
  - back  : trouser back (cut 2 mirrored), raised rise + fuller seat.
  - waistband : the hook-loop side-adjust band (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|waistband|set

waist_girth = float(PARAM(lambda: waist_girth, 880.0))
hip_girth = float(PARAM(lambda: hip_girth, 1060.0))
outseam = float(PARAM(lambda: outseam, 1000.0))
front_rise = float(PARAM(lambda: front_rise, 240.0))
back_rise_extra = float(PARAM(lambda: back_rise_extra, 90.0))
side_adjust = float(PARAM(lambda: side_adjust, 120.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1400.0))
hip_girth = max(760.0, min(hip_girth, 1560.0))
outseam = max(700.0, min(outseam, 1200.0))
front_rise = max(180.0, min(front_rise, 340.0))
back_rise_extra = max(30.0, min(back_rise_extra, 160.0))
side_adjust = max(60.0, min(side_adjust, 220.0))
seam_allowance = max(6.0, min(seam_allowance, 18.0))

hip_girth = max(hip_girth, waist_girth + 40.0)
LEG_BELOW = outseam - front_rise
back_rise_extra = min(back_rise_extra, LEG_BELOW * 0.35)

QUARTER_HIP = hip_girth / 4.0
QUARTER_WAIST = waist_girth / 4.0
WB_DEPTH = 60.0
# SIDE_LEN is the outside seam below the waistband; both panels share it. The side
# seam runs vertically from the hem to the side waist, so its length is SIDE_LEN.
SIDE_LEN = outseam - WB_DEPTH
HEM_HALF = max(150.0, QUARTER_HIP * 0.62)

# The side waist sits at y = SIDE_LEN. Centre-front waist sits FRONT_CENTRE_DROP below
# the side waist; centre-back waist sits BACK_CENTRE_RISE above it.
FRONT_CENTRE_DROP = front_rise            # centre front waist below the side waist
BACK_CENTRE_RISE = back_rise_extra        # centre back waist ABOVE the side waist

# The crotch is placed at ONE shared y and ONE shared x-offset magnitude, so the front
# and back inseams (crotch -> hem-inseam at the origin) are identical by construction
# and the leg cannot twist. The scoop depth below the crotch differs only in the
# curve control points, which do not touch the inseam edge.
CROTCH_Y = SIDE_LEN - front_rise - 50.0
CROTCH_X = -QUARTER_HIP * 0.13


def build_front():
    """Trouser front (cut 2 mirrored). Side seam vertical (length SIDE_LEN); centre
    front drops FRONT_CENTRE_DROP below the side waist; crotch scoop at the base of CF."""
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
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0},
        notches=[fc.Notch("side", 0.5, "knee level"),
                 fc.Notch("inseam", 0.5, "knee match")],
        grainline=fc.Grainline(fc.P(HEM_HALF * 0.5, 40.0),
                               fc.P(HEM_HALF * 0.5, SIDE_LEN - 40.0)),
        internals=[fc.Internal("no-front-pocket",
                               [fc.P(HEM_HALF * 0.35, SIDE_LEN - 70.0),
                                fc.P(HEM_HALF * 0.75, SIDE_LEN - 70.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Trouser front (low rise)",
    )


def build_back():
    """Trouser back (cut 2 mirrored). Side seam vertical (SAME SIDE_LEN); centre back
    rises BACK_CENTRE_RISE above the side waist; fuller seat via a wider back hip; no
    back pocket to sit on."""
    back_hem_half = HEM_HALF                       # SAME hem width; the seat fullness is
    # taken at the centre-back curve, not by widening the leg (which would unbalance the
    # side seam). The side seam stays SIDE_LEN so it matches the front.
    p_hem_in = fc.P(0.0, 0.0)
    p_hem_out = fc.P(back_hem_half, 0.0)
    p_side_waist = fc.P(back_hem_half, SIDE_LEN)
    p_cb_waist = fc.P(0.0, SIDE_LEN + BACK_CENTRE_RISE)
    # SAME shared crotch point as the front, so the inseams are identical. The fuller
    # seat is expressed by a deeper centre-back scoop (control points), not by moving
    # the crotch or the inseam.
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
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0},
        notches=[fc.Notch("side", 0.5, "knee level"),
                 fc.Notch("inseam", 0.5, "knee match")],
        grainline=fc.Grainline(fc.P(back_hem_half * 0.5, 40.0),
                               fc.P(back_hem_half * 0.5, SIDE_LEN - 40.0)),
        internals=[fc.Internal("raised-rise-note",
                               [fc.P(0.0, SIDE_LEN), fc.P(0.0, SIDE_LEN + BACK_CENTRE_RISE)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Trouser back (raised rise)",
    )


# The waistband length is the MEASURED sum of the four waist edges (two fronts, two
# backs) plus the hook-loop overlap at each end for the one-handed adjust. Measuring
# the built panels means the band can never come up short of the diagonal waist edges,
# whatever the rise difference does to their length.
_FW = build_front().edge("waist").length(0.2)
_BW = build_back().edge("waist").length(0.2)
WAIST_EDGE_SUM = 2.0 * _FW + 2.0 * _BW
WB_OVERLAP = side_adjust * 2.0
WB_LENGTH = WAIST_EDGE_SUM + WB_OVERLAP


def build_waistband():
    """The hook-loop side-adjust band, folded lengthwise. `attach` sews to the panels'
    waist edges; the hook-loop tape runs the last side_adjust of each end."""
    ln, w = WB_LENGTH, WB_DEPTH * 2.0
    return fc.Piece(
        "waistband", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.25, "left side seam"),
                 fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("attach", 0.75, "right side seam")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=[
            fc.Internal("hook-loop-left",
                        [fc.P(0.0, w * 0.5), fc.P(side_adjust, w * 0.5)], kind="marking"),
            fc.Internal("hook-loop-right",
                        [fc.P(ln - side_adjust, w * 0.5), fc.P(ln, w * 0.5)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Hook-loop waistband",
    )


def build():
    pattern = fc.PatternSet("seated-wear-trouser")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "waistband":
        pattern.add(build_waistband())

    if everything:
        # THE solving seam: front and back SIDE seams are equal (both SIDE_LEN), so the
        # leg cannot twist despite the differing rises.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.0)
        # The waistband attaches to the two fronts' and two backs' waist edges; its
        # length is the MEASURED sum of those edges plus the hook-loop overlap, declared
        # as the seam's ease so the band lands on the measured waist, not a girth guess.
        pattern.declare_seam(("waistband", "attach"),
                             [("front", "waist"), ("front", "waist"),
                              ("back", "waist"), ("back", "waist")],
                             tol=2.0, ease=WB_OVERLAP)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "stretch cotton twill", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 74% marker; a little stretch lets the raised back "
                 "rise move with the wearer sitting down and standing up."},
        {"item": "hook-and-loop tape", "qty": round(side_adjust * 2.0 + 40.0),
         "unit": "mm_length",
         "note": f"Yantra4D hook-loop-tape (notion.hardware_ref): {side_adjust:.0f} mm of "
                 "adjust run per side seam; the strip length is driven by side_adjust."},
        {"item": "waistband elastic (back only)", "qty": round(waist_girth * 0.4),
         "unit": "mm_length",
         "note": "a soft elastic across the raised back keeps it level without a hard band."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "flat-fell the inseam so it does not chafe a seated wearer."},
    ]
    pattern.metadata = {
        "fc400_rank": 372,
        "family": "adaptive",
        "fabric_hint": "poliester-elastano-compresion",
        "finished_mm": {"waist": round(waist_girth, 1), "hip": round(hip_girth, 1),
                        "outseam": round(outseam, 1),
                        "front_rise": round(front_rise, 1),
                        "back_rise": round(front_rise + back_rise_extra, 1)},
        "solved": {
            "side_len_mm": round(SIDE_LEN, 2),
            "front_centre_drop_mm": round(FRONT_CENTRE_DROP, 2),
            "back_centre_rise_mm": round(BACK_CENTRE_RISE, 2),
            "back_rise_extra_clamped_mm": round(back_rise_extra, 2),
            "note": "the front and back share ONE measured SIDE_LEN so the side seam "
                    "matches despite the differing rises; the rise difference is taken "
                    "at the centre seams (front lower, back higher); the extra back rise "
                    "is clamped under 35% of the leg-below-waist so the back waistline "
                    "can never invert above the hem.",
        },
        "adaptive": {
            "dressing": "no button, no fly; the side waist closes on hook-loop so it "
                        "adjusts one-handed from a seated position",
            "posture": "the back rise is genuinely taller than the front, so the waistband "
                       "stays level when seated instead of gaping at the back and cutting "
                       "at the front; no back pockets to sit on",
        },
        "hardware": "hook-and-loop side adjust via Yantra4D (notion.hardware_ref -> "
                    "hook-loop-tape); strip_length = side_adjust, the same parameter that "
                    "drives this trouser's waistband interface (the dimensional handshake).",
    }
    return pattern


result = build()

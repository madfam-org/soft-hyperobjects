"""
Quilter's thimble cot — Fashion Cabinet Care & Keeping Cartridge (FC-500 #416, care_keeping, T1).

A padded fabric finger cot that wears OVER a quilter's thimble (or in place of a metal one) —
a soft tapered sleeve for the pushing finger, quilted at the tip where the needle bears, so a
hand-quilter can work a long session without a bruised fingertip. Drafted to a KNOWN thimble —
the Yantra4D `thimble` solid (notion.hardware_ref) — so the cot's girth and length track the
finger the thimble already fits.

Solved, not guessed:

  1. THE COT IS A TRUE TAPERED TUBE. The flat SIDE panel is a trapezoid whose two arc edges
     are the MEASURED base and tip circumferences (finger girth and tip girth); rolled, it is
     a cone, and the seam is declared to the panel's straight sides.
  2. THE TIP CAP IS CUT TO THE MEASURED TIP. The cap disc radius is the tip girth over 2*pi,
     so the cap closes the cone exactly.
  3. THE TAPER IS CLAMPED so the tip girth is always smaller than the base but never a
     hairline — a tip drawn to zero would fold the cap into a point the kernel would close.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # side|cap|set

finger_girth = float(PARAM(lambda: finger_girth, 62.0))   # around the finger base
tip_girth = float(PARAM(lambda: tip_girth, 46.0))         # around the fingertip
cot_length = float(PARAM(lambda: cot_length, 55.0))
wall = float(PARAM(lambda: wall, 3.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

finger_girth = max(40.0, min(finger_girth, 90.0))
tip_girth = max(28.0, min(tip_girth, 80.0))
cot_length = max(30.0, min(cot_length, 90.0))
wall = max(1.0, min(wall, 8.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# the cot wraps the finger plus the wall; the tip girth is clamped smaller than the base but
# never below a floor so the cap never folds to a point.
# The tip cap disc must never be a degenerate sliver — a real fingertip cap needs a sane
# radius (>= ~9 mm), so the tip circumference is floored and the base is floored above it.
TIP_C_FLOOR = 2.0 * math.pi * 9.0
BASE_C = max(finger_girth + wall * 2.0 * math.pi, TIP_C_FLOOR + 16.0)
_tip_want = max(tip_girth + wall * 2.0 * math.pi, BASE_C * 0.45, TIP_C_FLOOR)
TIP_C = min(_tip_want, BASE_C - 6.0)     # always smaller than the base
TIP_R = TIP_C / (2.0 * math.pi)
SEGS = 28


def _side():
    """The tapered side panel: a trapezoid, base edge = BASE_C, tip edge = TIP_C, height =
    cot_length. Rolled into a cone; the two straight sides are the back seam."""
    hb = BASE_C / 2.0
    ht = TIP_C / 2.0
    p_bl = fc.P(-hb, 0.0)
    p_br = fc.P(hb, 0.0)
    p_tr = fc.P(ht, cot_length)
    p_tl = fc.P(-ht, cot_length)
    return fc.Piece(
        "side", [
            fc.Edge("base", [fc.Line(p_bl, p_br)]),
            fc.Edge("seam_r", [fc.Line(p_br, p_tr)]),
            fc.Edge("tip", [fc.Line(p_tr, p_tl)]),
            fc.Edge("seam_l", [fc.Line(p_tl, p_bl)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"base": 10.0},
        notches=[fc.Notch("base", 0.5, "underside"),
                 fc.Notch("tip", 0.5, "underside")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, cot_length - 8.0)),
        internals=[fc.Internal("tip quilting",
                               [fc.P(-ht * 0.6, cot_length - 8.0),
                                fc.P(ht * 0.6, cot_length - 8.0)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Side panel (cut 1)",
    )


def _cap():
    pts = [fc.P(TIP_R * math.cos(2.0 * math.pi * i / SEGS),
                TIP_R * math.sin(2.0 * math.pi * i / SEGS)) for i in range(SEGS)]
    edges = [fc.Edge(f"arc{i}", [fc.Line(pts[i], pts[(i + 1) % SEGS])])
             for i in range(SEGS)]
    return fc.Piece(
        "cap", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("arc0", 0.5, "quarter")],
        grainline=fc.Grainline(fc.P(-TIP_R * 0.5, 0.0), fc.P(TIP_R * 0.5, 0.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Tip cap (cut 1)",
    )


def build():
    pattern = fc.PatternSet("thimble-finger-cot")
    everything = target_piece == "set"
    if everything or target_piece == "side":
        pattern.add(_side())
    if everything or target_piece == "cap":
        pattern.add(_cap())

    if everything:
        # rolled, the two straight sides meet as the back seam (equal length).
        pattern.declare_seam(("side", "seam_r"), ("side", "seam_l"), tol=0.5)

    fabric_width = 700.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.45)
    pattern.bom = [
        {"item": "soft leather / suede + fine batting",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 45% marker (tiny pieces); a leather face "
                 f"at the tip takes the needle, a fabric back breathes."},
        {"item": "thimble core (optional)", "qty": 1, "unit": "count",
         "note": f"Yantra4D thimble (notion.hardware_ref): the cot is cut to the finger the "
                 f"thimble fits ({finger_girth:.0f} mm base girth)."},
        {"item": "thread + fine needle", "qty": 1, "unit": "spool",
         "note": "roll the side into a cone, set the tip cap, quilt the tip."},
    ]
    pattern.metadata = {
        "fc500_rank": 416, "family": "care_keeping", "tier": 1,
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A soft tapered finger cot quilted at the tip — worn over a "
            "thimble or in place of a metal one.",
        "solved": {
            "base_circumference_mm": round(BASE_C, 1),
            "tip_circumference_mm": round(TIP_C, 1),
            "tip_cap_radius_mm": round(TIP_R, 1),
            "tip_was_clamped": bool(
                abs(TIP_C - (tip_girth + wall * 2.0 * math.pi)) > 0.01),
            "note": "the side panel is a trapezoid whose base and tip edges are the MEASURED "
                    "base and tip circumferences; the cap radius is the tip circumference "
                    "over 2*pi so the cone closes exactly; the taper is clamped so the tip "
                    "is smaller than the base but never a hairline that folds the cap.",
        },
        "hardware": "thimble core via Yantra4D (notion.hardware_ref -> thimble); "
                    "finger_girth and thimble_h are fed from the finger and length. No "
                    "flange interface — the cot wears over the thimble, no seam handshake owed.",
    }
    return pattern


result = build()

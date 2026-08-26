"""
Aerial-Silk Unitard — Fashion Cabinet Costume Cartridge (FC-500 #479; y4d invisible-zipper).

The full-body unitard of the aerial-silk and static-trapeze artist: a single stretch skin from
neck to ankle with no waist seam to dig in under a hip-key, closing at a centre-back Yantra4D
`invisible-zipper` so nothing catches the silk or the rigging. It is cut at a firm negative ease
over the whole body so it moves as a second skin, with the leg and torso in one continuous panel
and reinforced friction zones marked where the silk wraps (hips, backs of knees, insteps).

The one-piece SOLVE. A unitard has no waist seam, so the front and back are each a single panel
from neck to ankle whose width tracks the body girth AT EACH LEVEL — chest, waist, hip, thigh,
calf, ankle — all at the same negative ease. Cut the leg and torso as separate blocks and the
waist join is a weak line exactly where an aerialist folds over the silk; drawn as one continuous
side seam, the skin is unbroken. The side seam (front to back) is drafted to match by
construction.

The DIMENSIONAL HANDSHAKE. The centre back closes on an `invisible-zipper`; `zip_length` drives
the zip tape AND the drafted CB opening AND the unitard's own `cb_zip` interface, so the concealed
tape is exactly as long as the opening.

Made to measure to the body girths and lengths. FC-500 lane 9 (costume, dance & performance).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 900.0))
waist_girth = float(PARAM(lambda: waist_girth, 720.0))
hip_girth = float(PARAM(lambda: hip_girth, 940.0))
thigh_girth = float(PARAM(lambda: thigh_girth, 560.0))
ankle_girth = float(PARAM(lambda: ankle_girth, 240.0))
torso_length = float(PARAM(lambda: torso_length, 600.0))
leg_length = float(PARAM(lambda: leg_length, 900.0))
stretch = float(PARAM(lambda: stretch, 0.14))
zip_length = float(PARAM(lambda: zip_length, 500.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

chest_bust_girth = max(680.0, min(chest_bust_girth, 1400.0))
waist_girth = max(520.0, min(waist_girth, 1200.0))
hip_girth = max(700.0, min(hip_girth, 1500.0))
thigh_girth = max(380.0, min(thigh_girth, 850.0))
ankle_girth = max(160.0, min(ankle_girth, 400.0))
torso_length = max(440.0, min(torso_length, 820.0))
leg_length = max(600.0, min(leg_length, 1200.0))
stretch = max(0.06, min(stretch, 0.28))
zip_length = min(max(300.0, min(zip_length, 800.0)), torso_length - 20.0)
seam_allowance = max(0.0, min(seam_allowance, 12.0))

NEG = 1.0 - stretch
CHEST_Q = (chest_bust_girth * NEG) / 4.0
WAIST_Q = (waist_girth * NEG) / 4.0
HIP_Q = (hip_girth * NEG) / 4.0
THIGH_Q = (thigh_girth * NEG) / 4.0
ANKLE_Q = (ankle_girth * NEG) / 4.0
TL = torso_length
LL = leg_length
TOTAL = TL + LL
# y-levels (0 at ankle, TOTAL at neck)
Y_HIP = LL
Y_WAIST = LL + TL * 0.5
Y_CHEST = LL + TL * 0.85
Y_THIGH = LL * 0.62
Y_KNEE = LL * 0.42
Y_CALF = LL * 0.25


def _half_panel(is_front):
    """A neck-to-ankle half panel. x=0 is CF/CB; the side edge tracks the body girth at each
    level. Inner leg (crotch to ankle) is the inseam side. Built as a chained polyline of
    body-tracking points, so front and back use the SAME level widths -> matching side seam."""
    neck_w = max(60.0, CHEST_Q * 0.6)
    # outer (side) profile from ankle up to the shoulder
    outer = [
        fc.P(ANKLE_Q, 0.0),
        fc.P(THIGH_Q * 0.9, Y_CALF),
        fc.P(THIGH_Q, Y_KNEE),
        fc.P(HIP_Q * 0.96, Y_THIGH),
        fc.P(HIP_Q, Y_HIP),
        fc.P(WAIST_Q, Y_WAIST),
        fc.P(CHEST_Q, Y_CHEST),
        fc.P(neck_w + (CHEST_Q - neck_w) * 0.5, TOTAL - 6.0),
    ]
    p_neck = fc.P(neck_w, TOTAL)
    p_cf_neck = fc.P(0.0, TOTAL - (neck_w * (0.9 if is_front else 0.3)))
    p_cf_crotch = fc.P(0.0, Y_HIP)          # centre front/back at the crotch level
    p_inner_ankle = fc.P(0.0, 0.0)          # inseam runs down CF from crotch to ankle
    # Build edges: outseam (ankle -> shoulder), shoulder, neck, centre (neck->crotch),
    # inseam (crotch -> inner ankle), hem (inner ankle -> outer ankle).
    outseam_segs = [fc.Line(outer[i], outer[i + 1]) for i in range(len(outer) - 1)]
    edges = [
        fc.Edge("hem", [fc.Line(p_inner_ankle, outer[0])]),
        fc.Edge("outseam", outseam_segs),
        fc.Edge("shoulder", [fc.Line(outer[-1], p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck, fc.P(neck_w * 0.6, TOTAL - 4.0),
                                   fc.P(neck_w * 0.2, p_cf_neck.y + 4.0), p_cf_neck)]),
        fc.Edge("center", [fc.Line(p_cf_neck, p_cf_crotch)]),
        fc.Edge("inseam", [fc.Line(p_cf_crotch, p_inner_ankle)]),
    ]
    name = "unitard_front" if is_front else "unitard_back"
    internals = []
    if is_front:
        _fz = ((Y_KNEE, "friction-knee"), (Y_HIP, "friction-hip"), (30.0, "friction-instep"))
        for ny, lbl in _fz:
            internals.append(fc.Internal(lbl, [fc.P(0.0, ny), fc.P(HIP_Q * 0.7, ny)],
                kind="marking"))
    else:
        internals.append(fc.Internal("cb-zip", [fc.P(0.0, TOTAL - 10.0),
                                                fc.P(0.0, TOTAL - 10.0 - zip_length)],
                                                    kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"neck": 0.0},
        notches=[fc.Notch("outseam", 0.5, "side match"), fc.Notch("inseam", 0.5, "inseam match")],
        grainline=fc.Grainline(fc.P(HIP_Q * 0.4, TOTAL * 0.2), fc.P(HIP_Q * 0.4, TOTAL * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=(1 if is_front else 2), mirror=(not is_front),
                       on_fold=is_front, fold_edge=("center" if is_front else None)),
        label=("Unitard front (cut 1 on fold)" if is_front else "Unitard back (cut 2, CB zip)"),
    )


def build():
    pattern = fc.PatternSet("circus-aerial-unitard")
    front = _half_panel(True)
    back = _half_panel(False)

    picked = {"unitard_front": front, "unitard_back": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back):
            pattern.add(piece)
        # Outseam (side) and inseam join front to back; both use identical level widths.
        pattern.declare_seam(("unitard_front", "outseam"), ("unitard_back", "outseam"), tol=2.0)
        pattern.declare_seam(("unitard_front", "inseam"), ("unitard_back", "inseam"), tol=2.0)
        pattern.declare_seam(("unitard_front", "shoulder"), ("unitard_back", "shoulder"), tol=2.0)

    fabric_width = 1500.0
    area = front.area() * 2.0 + back.area() * 2.0
    marker_len = area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "4-way stretch performance knit (nylon/spandex, matte)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"matte so stage light does not flare; at {fabric_width:.0f} mm width."},
        {"item": "invisible zipper (Yantra4D invisible-zipper)", "qty": 1, "unit": "piece",
         "note": f"concealed CB zip, {zip_length:.0f} mm (hardware_ref -> invisible-zipper) — "
                 "nothing proud to catch the silk or the rigging."},
        {"item": "reinforcement (friction zones)", "qty": round((front.area()) * 0.15 / 100.0),
         "unit": "cm2",
         "note": "power-mesh backing at the marked hip, knee and instep friction zones where the "
                 "silk wraps and abrades."},
        {"item": "coverstitch + wooly nylon + gusset", "qty": 1, "unit": "set",
         "note": "flatlock every seam so nothing digs in under a hip-key or a foot-lock."},
    ]
    pattern.metadata = {
        "fc500_rank": 479, "family": "costume_historical", "fabric_hint": "nylon-elastano",
        "provenance": "The aerial unitard is the working costume of the silk, static-trapeze and "
            "corde-lisse artist: a full stretch skin with no seam or hardware that could catch the "
            "apparatus, a concern that separates it from a fashion catsuit. The friction zones and "
            "the concealed closure are the craft.",
        "silhouette_note": "A one-piece neck-to-ankle stretch skin, front and back each a single "
            "panel (no waist seam), reinforced at the silk-wrap friction zones, closing at a "
            "concealed centre-back invisible zip.",
        "hardware": "concealed CB zip via Yantra4D (hardware_ref -> invisible-zipper); zip_length "
            "drives the tape AND the drafted CB opening.",
        "solved": {
            "stretch": round(stretch, 3),
            "chest_quarter_mm": round(CHEST_Q, 1),
            "hip_quarter_mm": round(HIP_Q, 1),
            "ankle_quarter_mm": round(ANKLE_Q, 1),
            "total_length_mm": round(TOTAL, 1),
            "zip_length_mm": round(zip_length, 1),
            "note": "front and back are each one continuous neck-to-ankle panel with no waist "
                    "seam; the outseam and inseam use identical level widths so they match, and "
                    "the skin is unbroken exactly where an aerialist folds over the silk.",
        },
        "closure": "concealed centre-back invisible zipper",
        "drafting": "Made to measure to the body girths and lengths; firm negative-ease stretch.",
    }
    return pattern


result = build()

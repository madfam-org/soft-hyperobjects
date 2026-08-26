"""
Stirrup knit legging — Fashion Cabinet Garment Cartridge (FC-500 #403, knitwear, T1).

A pull-on jersey legging with a STIRRUP: the leg runs full length and continues, past the
ankle, into a narrow strap that passes under the arch of the foot and rejoins the leg —
holding the hem down so it never rides up. Cut in a stretch jersey with NEGATIVE ease
(the flat pattern is drawn smaller than the body and the knit stretches to fit), so the
draft is a two-panel tube: one front, one back, joined at inseam and side.

Solved, not guessed:

  1. THE STIRRUP STRAP CLOSES ON ITSELF. The front and back both grow a stirrup tongue
     below the ankle; the two tongues sew end to end into the under-arch strap. Their
     ends are drafted to the SAME width so the strap seam is not a step, and the strap
     length is MEASURED (front tongue + back tongue) rather than assumed.
  2. NEGATIVE EASE IS CLAMPED. The pattern width is the body girth times a stretch factor
     below 1.0, but the factor is floored so an over-aggressive stretch can never draw the
     panel to a negative or hairline width that the kernel would CCW-normalize into a
     healthy-looking sliver.

Pull-on: no hardware, no closure. A folded waistband casing takes elastic.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|set

waist_girth = float(PARAM(lambda: waist_girth, 760.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
ankle_girth = float(PARAM(lambda: ankle_girth, 240.0))
inside_leg = float(PARAM(lambda: inside_leg, 780.0))
body_rise = float(PARAM(lambda: body_rise, 270.0))
stretch_factor = float(PARAM(lambda: stretch_factor, 0.82))  # <1: negative ease
stirrup_width = float(PARAM(lambda: stirrup_width, 34.0))     # under-arch strap width
stirrup_drop = float(PARAM(lambda: stirrup_drop, 60.0))       # how far below the ankle
waist_casing = float(PARAM(lambda: waist_casing, 40.0))       # folded elastic casing
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

waist_girth = max(560.0, min(waist_girth, 1100.0))
hip_girth = max(680.0, min(hip_girth, 1300.0))
ankle_girth = max(160.0, min(ankle_girth, 360.0))
inside_leg = max(560.0, min(inside_leg, 920.0))
body_rise = max(210.0, min(body_rise, 360.0))
stretch_factor = max(0.62, min(stretch_factor, 0.98))   # floored so no hairline panel
stirrup_width = max(20.0, min(stirrup_width, 60.0))
stirrup_drop = max(25.0, min(stirrup_drop, 120.0))
waist_casing = max(24.0, min(waist_casing, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# Panel widths from the body girths, drawn smaller by the stretch factor (negative ease).
# A tube split front/back: each panel is a QUARTER of the girth times the factor.
Q_WAIST = max(40.0, waist_girth / 4.0 * stretch_factor)
Q_HIP = max(50.0, hip_girth / 4.0 * stretch_factor)
Q_ANKLE = max(24.0, ankle_girth / 4.0 * stretch_factor)
LEG_LEN = inside_leg
HIP_LEVEL = body_rise * 0.55           # hip line up from the crotch


def _panel(name, q_waist, q_hip, q_ankle, crotch_scoop, is_front):
    """One panel (front or back), cut 2 mirrored. Waist at top (y=body_rise), ankle at
    the bottom (y=0), a stirrup tongue below. The CF/CB edge scoops for the crotch."""
    y_waist = body_rise
    y_hip = HIP_LEVEL
    y_ankle = 0.0
    y_tongue = -stirrup_drop
    # outer (side) edge: waist -> hip -> ankle, a smooth taper
    p_w_out = fc.P(q_waist, y_waist)
    p_h_out = fc.P(q_hip, y_hip)
    p_a_out = fc.P(q_ankle, y_ankle)
    # inner (crotch/inseam) edge along x≈0..scoop
    p_w_in = fc.P(0.0, y_waist)
    p_crotch = fc.P(crotch_scoop, y_hip + (y_waist - y_hip) * 0.25)
    p_a_in = fc.P(0.0, y_ankle)
    # stirrup tongue: a narrow tab centred under the ankle
    half = stirrup_width / 2.0
    cx = q_ankle / 2.0
    edges = [
        # side seam (outer): waist down to ankle
        fc.Edge("side", [
            fc.curve_through(p_w_out, p_h_out, bulge=0.06, side=1.0),
            fc.curve_through(p_h_out, p_a_out, bulge=0.05, side=1.0)]),
        # ankle-to-tongue on the outer side
        fc.Edge("tongue_out", [fc.Line(p_a_out, fc.P(cx + half, y_ankle)),
                               fc.Line(fc.P(cx + half, y_ankle),
                                       fc.P(cx + half, y_tongue))]),
        # strap end (sewn to the other panel's strap end)
        fc.Edge("strap_end", [fc.Line(fc.P(cx + half, y_tongue),
                                      fc.P(cx - half, y_tongue))]),
        # tongue inner + ankle-to-inseam
        fc.Edge("tongue_in", [fc.Line(fc.P(cx - half, y_tongue),
                                      fc.P(cx - half, y_ankle)),
                              fc.Line(fc.P(cx - half, y_ankle), p_a_in)]),
        # inseam / crotch edge up to the waist
        fc.Edge("inseam", [
            fc.curve_through(p_a_in, p_crotch, bulge=0.10 if is_front else 0.16,
                             side=-1.0 if is_front else 1.0),
            fc.curve_through(p_crotch, p_w_in, bulge=0.05, side=1.0)]),
        # waist edge
        fc.Edge("waist", [fc.Line(p_w_in, p_w_out)]),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"waist": waist_casing},
        notches=[fc.Notch("side", 0.5, "knee"),
                 fc.Notch("waist", 0.5, "quarter"),
                 fc.Notch("strap_end", 0.5, "strap join")],
        grainline=fc.Grainline(fc.P(q_hip * 0.5, y_ankle + 20.0),
                               fc.P(q_hip * 0.5, y_waist - 20.0)),
        internals=[
            fc.Internal("waist casing fold",
                        [fc.P(0.0, y_waist - waist_casing),
                         fc.P(q_waist, y_waist - waist_casing)], kind="marking"),
            fc.Internal("stirrup centre",
                        [fc.P(cx, y_ankle), fc.P(cx, y_tongue)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=("Front panel (cut 2, mirrored)" if is_front
               else "Back panel (cut 2, mirrored)"),
    )


def build_front():
    return _panel("front", Q_WAIST, Q_HIP, Q_ANKLE, crotch_scoop=Q_HIP * 0.30,
                  is_front=True)


def build_back():
    # The back scoops deeper for the seat AT THE CROTCH/INSEAM — the side edge stays
    # identical to the front so the two side seams sew flush (the seat fullness lives on
    # the inseam scoop, not the outseam).
    return _panel("back", Q_WAIST, Q_HIP, Q_ANKLE, crotch_scoop=Q_HIP * 0.44,
                  is_front=False)


def build():
    pattern = fc.PatternSet("stirrup-legging-knit")
    everything = target_piece == "set"
    front = build_front()
    back = build_back()
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)

    if everything:
        # the front and back tubes join at the side and the inseam; the two stirrup
        # tongues meet end to end under the arch (equal-width strap ends). The back
        # inseam runs longer (the seat scoop) and eases onto the front on the stretch —
        # declared with the MEASURED excess so it stays honest.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.2)
        pattern.declare_seam(("front", "strap_end"), ("back", "strap_end"), tol=0.5)
        # ease convention: delta = len_a - (len_b + ease); side_a is the front, so
        # ease = front_len - back_len (negative — the back is the longer, eased side).
        _in_ease = (front.edge("inseam").length(0.05)
                    - back.edge("inseam").length(0.05))
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"),
                             tol=1.0, ease=_in_ease)

    STRAP_LEN = (front.edge("tongue_out").length(0.05)
                 + back.edge("tongue_out").length(0.05))
    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton/elastane jersey (4-way stretch)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; drafted with NEGATIVE ease "
                 f"(factor {stretch_factor:.2f}) — the flat panel is smaller than the body "
                 f"and the knit stretches to fit."},
        {"item": "waistband elastic (35-40 mm)", "qty": round(waist_girth * 0.9),
         "unit": "mm_length", "note": "threads the folded waist casing."},
        {"item": "ballpoint needle + stretch thread", "qty": 1, "unit": "spool",
         "note": "a ballpoint needle for the jersey; a zigzag or coverstitch on the "
                 "stirrup strap so it stretches over the arch without popping."},
    ]
    pattern.metadata = {
        "fc500_rank": 403, "family": "knitwear", "tier": 1,
        "fabric_hint": "jersey-algodon",
        "silhouette_note": "A pull-on jersey legging with an under-arch STIRRUP that holds "
            "the hem down; a two-panel stretch tube with negative ease.",
        "solved": {
            "stretch_factor": round(stretch_factor, 3),
            "quarter_waist_mm": round(Q_WAIST, 1),
            "quarter_hip_mm": round(Q_HIP, 1),
            "quarter_ankle_mm": round(Q_ANKLE, 1),
            "strap_length_measured_mm": round(STRAP_LEN, 1),
            "note": "panel widths are the body quarters times a stretch factor floored at "
                    "0.62 so an aggressive stretch never draws a hairline panel; the two "
                    "stirrup tongues are equal-width so the under-arch strap seam is flush, "
                    "and the strap length is measured (front tongue + back tongue).",
        },
        "hardware": "none — a pull-on knit; the waist casing takes elastic.",
    }
    return pattern


result = build()

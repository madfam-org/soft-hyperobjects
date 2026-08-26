"""
Six-Button Tailored Waistcoat — Fashion Cabinet Garment Cartridge
(FC-400 #313, tailoring, T3).

The tailored waistcoat: a six-button front with a pointed hem, welted pockets,
a bust-and-waist dart, a satin or lining back, and a back cinch buckle. The
signature is the SIX-BUTTON RUN down to a pointed hem, and the number that has to
be right is the button pitch — the bottom button is worn undone, so it must sit
ABOVE the point where the front edges diverge, or it lands on air.

Three things are solved by measurement rather than by formula:

  1. THE SIX BUTTONS ARE PITCHED ACROSS THE MEASURED FRONT RUN, ABOVE THE POINT.
     The button run is MEASURED from the top button (below the gorge) to the last
     button ABOVE the hem point where the fronts diverge — and the pitch is
     recomputed across whole intervals, so the traditionally-undone bottom button
     sits on cloth just above the divergence, never on the open point.

  2. THE FRONT POINT AND ITS DIVERGENCE ARE SOLVED, NOT DRAWN. Below the waist the
     two front edges angle apart to the two points; the divergence is derived
     from a MEASURED point drop, floored so at extremes the point cannot invert
     above the waist (a negative drop that the kernel CCW-normalizes into a
     valid-looking crossed hem).

  3. THE WELT POCKETS ARE CLAMPED AGAINST THE FRONT. A welt wider than the panel
     folds it over — CCW-normalized by the kernel into a healthy-looking piece —
     so both welt lengths and the dart intakes are clamped and reported.

TAILORING CONVENTIONS: fine edge-stitch; a lined back; a back cinch. The
SEW-THROUGH BUTTON SOLID is Yantra4D territory (`sew-through-button`; see
notion.hardware_ref).

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


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|welt|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
front_length = float(PARAM(lambda: front_length, 560.0))    # shoulder to hem point
neck_width = float(PARAM(lambda: neck_width, 170.0))
shoulder_slope = float(PARAM(lambda: shoulder_slope, 45.0))
button_count = float(PARAM(lambda: button_count, 6.0))
button_ligne = float(PARAM(lambda: button_ligne, 24.0))
point_drop = float(PARAM(lambda: point_drop, 60.0))         # how far the point drops
welt_length = float(PARAM(lambda: welt_length, 110.0))
vest_ease = float(PARAM(lambda: vest_ease, 60.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))

chest_girth = max(820.0, min(chest_girth, 1400.0))
waist_girth = max(640.0, min(waist_girth, 1300.0))
front_length = max(440.0, min(front_length, 700.0))
neck_width = max(140.0, min(neck_width, 220.0))
shoulder_slope = max(25.0, min(shoulder_slope, 70.0))
button_count = max(3.0, min(round(button_count), 8.0))
button_ligne = max(18.0, min(button_ligne, 34.0))
point_drop = max(0.0, min(point_drop, 140.0))
welt_length = max(70.0, min(welt_length, 200.0))
vest_ease = max(20.0, min(vest_ease, 140.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(12.0, min(hem_allowance, 35.0))

EDGESTITCH = 5.0
N_BUTTONS = int(button_count)
BUTTON_MM = button_ligne * 0.635

QUARTER_CHEST = (chest_girth + vest_ease) / 4.0
QUARTER_WAIST = max(QUARTER_CHEST * 0.72,
                    min((waist_girth + vest_ease) / 4.0, QUARTER_CHEST - 6.0))
HALF_NECK = neck_width / 2.0
NECK_DROP_F = max(90.0, HALF_NECK * 1.2)

# The point drop, floored so the point cannot invert above the waist.
POINT_DROP = max(20.0, min(point_drop, front_length * 0.4))
# The waist line (where the fronts begin to diverge to the points).
WAIST_Y = POINT_DROP + hem_allowance + 30.0

# The button run: from the top button (below the gorge) to the last button ABOVE
# the divergence point.
BUTTON_TOP_Y = front_length - NECK_DROP_F - BUTTON_MM
BUTTON_BOTTOM_Y = WAIST_Y + BUTTON_MM
BUTTON_RUN = max(BUTTON_MM * 2.0, BUTTON_TOP_Y - BUTTON_BOTTOM_Y)
N_INTERVALS = max(1, N_BUTTONS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS

TOTAL_SUPPRESS = max(0.0, QUARTER_CHEST - QUARTER_WAIST)
_DART_RAW = TOTAL_SUPPRESS * 0.6
WAIST_DART = max(0.0, min(_DART_RAW, QUARTER_CHEST * 0.24))

_WELT_RAW = welt_length
WELT_LEN = max(50.0, min(_WELT_RAW, QUARTER_CHEST - 2.0 * seam_allowance))


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    """Front, cut 2 mirrored. Pointed hem; six-button run; welt pockets; dart."""
    hw = QUARTER_CHEST
    # The front edge runs down the centre to the waist, then angles out to the
    # point at the hem. The point sits below the waist by POINT_DROP.
    p_point = fc.P(-POINT_DROP * 0.35, 0.0)               # the lowest point
    p_hem_side = fc.P(hw, WAIST_Y * 0.4)
    p_waist_side = fc.P(QUARTER_WAIST, WAIST_Y)
    p_armhole = fc.P(hw, front_length - QUARTER_CHEST * 0.42)
    p_shoulder_pt = fc.P(hw * 0.5, front_length - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, front_length)
    p_neck_cf = fc.P(0.0, front_length - NECK_DROP_F)
    edges = [
        # Pointed hem: from the point up the side.
        fc.Edge("hem", [fc.Line(p_point, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.curve_through(
            p_armhole, p_shoulder_pt, bulge=0.22, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.30, side=1.0)]),
        # Front edge: down the centre to the waist, then angles out to the point.
        fc.Edge("front_edge", [fc.Line(p_neck_cf, fc.P(0.0, WAIST_Y)),
                               fc.Line(fc.P(0.0, WAIST_Y), p_point)]),
    ]
    internals = [
        fc.Internal("edge-stitch",
                    [fc.P(EDGESTITCH, WAIST_Y),
                     fc.P(EDGESTITCH, front_length - NECK_DROP_F)], kind="trace"),
        fc.Internal("waist dart",
                    [fc.P(hw * 0.5, WAIST_Y + 60.0),
                     fc.P(hw * 0.5 - WAIST_DART / 2.0, WAIST_Y),
                     fc.P(hw * 0.5, WAIST_Y - 50.0),
                     fc.P(hw * 0.5 + WAIST_DART / 2.0, WAIST_Y),
                     fc.P(hw * 0.5, WAIST_Y + 60.0)], kind="marking"),
        fc.Internal("lower welt pocket",
                    [fc.P(hw * 0.22, WAIST_Y - 10.0),
                     fc.P(hw * 0.22 + WELT_LEN, WAIST_Y - 10.0)], kind="marking"),
        fc.Internal("upper welt pocket",
                    [fc.P(hw * 0.30, front_length - QUARTER_CHEST * 0.5),
                     fc.P(hw * 0.30 + WELT_LEN * 0.6,
                          front_length - QUARTER_CHEST * 0.5)], kind="marking"),
    ]
    y0 = BUTTON_TOP_Y
    for i in range(N_BUTTONS):
        internals.append(_button(f"button-{i + 1}", BUTTON_MM * 0.8, y0 - BUTTON_PITCH * i))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.4, "waist"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.4, WAIST_Y),
                               fc.P(hw * 0.4, front_length - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    """Back, cut 2 mirrored (lining/satin). Carries the cinch buckle."""
    hw = QUARTER_CHEST * 0.92
    # The shoulder and armscye MATCH the front's exactly (same neck point, same
    # shoulder point, same armhole) so the shoulder and side seams close; only the
    # hem/waist run narrower on the back, which is the vest's cut-away back.
    p_hem_cb = fc.P(0.0, WAIST_Y * 0.4)
    p_hem_side = fc.P(QUARTER_CHEST, WAIST_Y * 0.4)
    p_waist_side = fc.P(QUARTER_WAIST, WAIST_Y)
    p_armhole = fc.P(QUARTER_CHEST, front_length - QUARTER_CHEST * 0.42)
    p_shoulder_pt = fc.P(QUARTER_CHEST * 0.5, front_length - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, front_length)
    p_neck_cb = fc.P(0.0, front_length - HALF_NECK * 0.28)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.curve_through(
            p_armhole, p_shoulder_pt, bulge=0.22, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.4, "waist"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.35, WAIST_Y),
                               fc.P(hw * 0.35, front_length - 30.0)),
        internals=[
            fc.Internal("cinch buckle placement",
                        [fc.P(hw * 0.3, WAIST_Y + 10.0),
                         fc.P(hw * 0.7, WAIST_Y + 10.0)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (cut 2, mirrored)",
    )


def build_welt():
    """The welt-pocket welt, cut 4. Clamped against the front."""
    w = WELT_LEN
    h = max(18.0, BUTTON_MM * 1.2)
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "welt", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("top", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        internals=[
            fc.Internal("edge-stitch",
                        [fc.P(EDGESTITCH, EDGESTITCH), fc.P(w - EDGESTITCH, EDGESTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=4),
        label="Welt (cut 4)",
    )


def build():
    pattern = fc.PatternSet("waistcoat-6button")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "welt": everything or target_piece == "welt",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        pattern.add(build_front())
    if want["back"]:
        pattern.add(build_back())
    if want["welt"]:
        pattern.add(build_welt())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "wool worsted, 280 gsm (front) + lining (back)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 68% marker; the back is "
                 f"traditionally cut in lining/satin, the front in the suit cloth."},
        {"item": "sew-through button", "qty": N_BUTTONS, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm); SOLVED pitch "
                 f"{BUTTON_PITCH:.1f} mm, the bottom button above the point."},
        {"item": "back cinch buckle + strap", "qty": 1, "unit": "set",
         "note": "the back adjuster; a companion hard good, not the bridged one."},
        {"item": "fine edge-stitch thread + needle 80/12", "qty": 1, "unit": "spool",
         "note": f"{EDGESTITCH:.0f} mm edge-stitch on the front edge and welts."},
    ]
    pattern.metadata = {
        "fc400_rank": 313,
        "family": "tailoring",
        "tier": 3,
        "fabric_hint": "wool-worsted",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_length": round(front_length, 1),
            "point_drop": round(POINT_DROP, 1),
            "welt_length": round(WELT_LEN, 1),
        },
        "solved": {
            "button_count": N_BUTTONS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "button_run_mm": round(BUTTON_RUN, 2),
            "button_bottom_above_point": bool(BUTTON_BOTTOM_Y > WAIST_Y * 0.4),
            "point_drop_requested_mm": round(point_drop, 2),
            "point_drop_floored_mm": round(POINT_DROP, 2),
            "point_drop_was_floored": bool(abs(POINT_DROP - point_drop) > 0.01),
            "welt_requested_mm": round(_WELT_RAW, 2),
            "welt_clamped_mm": round(WELT_LEN, 2),
            "welt_was_clamped": bool(abs(WELT_LEN - _WELT_RAW) > 0.01),
            "waist_dart_clamped_mm": round(WAIST_DART, 2),
            "note": "the six buttons are pitched across the MEASURED run from the "
                    "top button to the last button ABOVE the point where the fronts "
                    "diverge, so the traditionally-undone bottom button sits on "
                    "cloth, not on the open point. The point drop is floored so it "
                    "cannot invert above the waist (a negative drop the kernel "
                    "CCW-normalizes into a valid-looking crossed hem), and the welts "
                    "are clamped against the front.",
        },
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne is fed from this "
                    "garment's button_ligne, which also sizes the buttonholes and "
                    "the six-button spacing.",
    }
    return pattern


result = build()

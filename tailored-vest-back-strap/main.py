"""
Cinch-Back Tailoring Vest — Fashion Cabinet Garment Cartridge
(FC-400 #320, tailoring, T3).

The cinch-back waistcoat: a tailored vest whose back is split at the centre and
drawn together by a strap running through a buckle, so the wearer nips the waist
to fit. The signature is the BACK STRAP AND BUCKLE, and the number that has to be
right is the strap's cut length against its adjustment range — a strap cut to the
nominal back width runs out of buckle before it can cinch, and one cut too long
leaves a tail flapping past the buckle.

Three things are solved by measurement rather than by formula:

  1. THE BACK STRAP IS CUT TO THE MEASURED BACK GAP PLUS THE BUCKLE'S TRAVEL. The
     two back halves stop short of the centre by a MEASURED gap; the strap spans
     that gap plus a symmetric adjustment range centred on the nominal setting,
     plus the wrap round the buckle bar. A strap cut to the gap alone cannot
     tighten; the travel is what lets the vest cinch and let out.

  2. THE FRONT BUTTON RUN IS PITCHED ACROSS THE MEASURED FRONT, ABOVE THE POINT.
     As on any waistcoat, the buttons run to a pointed hem and the bottom one is
     worn undone, so the run is measured from the top button to the last button
     ABOVE the divergence and the pitch recomputed.

  3. THE POINT DROP AND WELTS ARE CLAMPED. The point drop is floored so it cannot
     invert above the waist, and the welt lengths are clamped against the front,
     because an inverted piece is CCW-normalized by the kernel into a healthy-
     looking outline.

TAILORING CONVENTIONS: fine edge-stitch; a lining back; the buckle a Yantra4D
reference. The STRAP-BUCKLE SOLID is Yantra4D territory (`strap-buckle`; see
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
# front|back|strap|welt|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
front_length = float(PARAM(lambda: front_length, 560.0))
neck_width = float(PARAM(lambda: neck_width, 170.0))
shoulder_slope = float(PARAM(lambda: shoulder_slope, 45.0))
button_count = float(PARAM(lambda: button_count, 5.0))
button_ligne = float(PARAM(lambda: button_ligne, 24.0))
point_drop = float(PARAM(lambda: point_drop, 60.0))
back_gap = float(PARAM(lambda: back_gap, 120.0))          # gap the strap spans
strap_width = float(PARAM(lambda: strap_width, 34.0))     # buckle strap width
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
back_gap = max(60.0, min(back_gap, 240.0))
strap_width = max(22.0, min(strap_width, 55.0))
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

POINT_DROP = max(20.0, min(point_drop, front_length * 0.4))
WAIST_Y = POINT_DROP + hem_allowance + 30.0

BUTTON_TOP_Y = front_length - NECK_DROP_F - BUTTON_MM
BUTTON_BOTTOM_Y = WAIST_Y + BUTTON_MM
BUTTON_RUN = max(BUTTON_MM * 2.0, BUTTON_TOP_Y - BUTTON_BOTTOM_Y)
N_INTERVALS = max(1, N_BUTTONS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS

TOTAL_SUPPRESS = max(0.0, QUARTER_CHEST - QUARTER_WAIST)
WAIST_DART = max(0.0, min(TOTAL_SUPPRESS * 0.6, QUARTER_CHEST * 0.24))

_WELT_RAW = welt_length
WELT_LEN = max(50.0, min(_WELT_RAW, QUARTER_CHEST - 2.0 * seam_allowance))

# The back strap: spans the MEASURED gap plus the buckle's travel plus the wrap.
BUCKLE_TRAVEL = max(40.0, back_gap * 0.5)
STRAP_WRAP = strap_width * 2.0
STRAP_CUT = back_gap + BUCKLE_TRAVEL + STRAP_WRAP + 2.0 * seam_allowance


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    hw = QUARTER_CHEST
    p_point = fc.P(-POINT_DROP * 0.35, 0.0)
    p_hem_side = fc.P(hw, WAIST_Y * 0.4)
    p_waist_side = fc.P(QUARTER_WAIST, WAIST_Y)
    p_armhole = fc.P(hw, front_length - QUARTER_CHEST * 0.42)
    p_shoulder_pt = fc.P(hw * 0.5, front_length - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, front_length)
    p_neck_cf = fc.P(0.0, front_length - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_point, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.curve_through(p_armhole, p_shoulder_pt,
                                             bulge=0.22, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.30, side=1.0)]),
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
        fc.Internal("welt pocket",
                    [fc.P(hw * 0.22, WAIST_Y - 10.0),
                     fc.P(hw * 0.22 + WELT_LEN, WAIST_Y - 10.0)], kind="marking"),
    ]
    y0 = BUTTON_TOP_Y
    for i in range(N_BUTTONS):
        internals.append(_button(f"button-{i + 1}", BUTTON_MM * 0.8, y0 - BUTTON_PITCH * i))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.4, "waist"), fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.4, WAIST_Y), fc.P(hw * 0.4, front_length - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    """Back half, cut 2 mirrored. Stops short of CB by half the gap; the strap and
    buckle span it."""
    half_gap = back_gap / 2.0
    p_hem_cb = fc.P(half_gap, WAIST_Y * 0.4)
    p_hem_side = fc.P(QUARTER_CHEST, WAIST_Y * 0.4)
    p_waist_side = fc.P(QUARTER_WAIST, WAIST_Y)
    p_armhole = fc.P(QUARTER_CHEST, front_length - QUARTER_CHEST * 0.42)
    p_shoulder_pt = fc.P(QUARTER_CHEST * 0.5, front_length - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, front_length)
    p_neck_cb = fc.P(half_gap, front_length - HALF_NECK * 0.28)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.curve_through(p_armhole, p_shoulder_pt,
                                             bulge=0.22, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb_edge", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.4, "waist"),
                 fc.Notch("cb_edge", 0.5, "strap/buckle anchor")],
        grainline=fc.Grainline(fc.P(QUARTER_CHEST * 0.5, WAIST_Y),
                               fc.P(QUARTER_CHEST * 0.5, front_length - 30.0)),
        internals=[
            fc.Internal("strap anchor",
                        [fc.P(half_gap + 6.0, WAIST_Y), fc.P(half_gap + 6.0 + strap_width,
                                                            WAIST_Y)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back half (cut 2, mirrored)",
    )


def build_strap():
    """The cinch strap, cut 2. Spans the gap plus the buckle's travel plus wrap."""
    ln = STRAP_CUT
    w = strap_width * 2.0 + 2.0 * seam_allowance
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("buckle_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("anchor_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.0, "anchor end"),
                 fc.Notch("lower", 1.0, "buckle end")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            fc.Internal("buckle travel",
                        [fc.P(ln - seam_allowance - STRAP_WRAP - BUCKLE_TRAVEL, w / 2.0),
                         fc.P(ln - seam_allowance - STRAP_WRAP, w / 2.0)],
                        kind="marking"),
            fc.Internal("nominal setting",
                        [fc.P(ln - seam_allowance - STRAP_WRAP - BUCKLE_TRAVEL / 2.0, 0.0),
                         fc.P(ln - seam_allowance - STRAP_WRAP - BUCKLE_TRAVEL / 2.0, w)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Cinch strap (cut 2)",
    )


def build_welt():
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
        internals=[],
        cut=fc.CutSpec(quantity=4),
        label="Welt (cut 4)",
    )


def build():
    pattern = fc.PatternSet("tailored-vest-back-strap")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "strap": everything or target_piece == "strap",
        "welt": everything or target_piece == "welt",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        pattern.add(build_front())
    if want["back"]:
        pattern.add(build_back())
    if want["strap"]:
        pattern.add(build_strap())
    if want["welt"]:
        pattern.add(build_welt())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if want["strap"]:
        pattern.declare_seam(("strap", "lower"), ("strap", "upper"), tol=0.3)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "wool worsted, 280 gsm (front) + lining (back)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 68% marker."},
        {"item": "sew-through button", "qty": N_BUTTONS, "unit": "piece",
         "note": f"front closure at {button_ligne:.0f} ligne; SOLVED pitch "
                 f"{BUTTON_PITCH:.1f} mm. A companion hard good — the buckle is "
                 f"the bridged notion."},
        {"item": "strap buckle", "qty": 1, "unit": "piece",
         "note": f"Yantra4D strap-buckle (notion.hardware_ref) for a "
                 f"{strap_width:.0f} mm strap; {BUCKLE_TRAVEL:.0f} mm of cinch "
                 f"travel across a MEASURED {back_gap:.0f} mm back gap."},
        {"item": "fine edge-stitch thread + needle 80/12", "qty": 1, "unit": "spool",
         "note": f"{EDGESTITCH:.0f} mm edge-stitch on the front edge."},
    ]
    pattern.metadata = {
        "fc400_rank": 320,
        "family": "tailoring",
        "tier": 3,
        "fabric_hint": "wool-worsted",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_length": round(front_length, 1),
            "back_gap": round(back_gap, 1),
            "strap_cut_length": round(STRAP_CUT, 1),
        },
        "solved": {
            "button_count": N_BUTTONS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "back_gap_mm": round(back_gap, 2),
            "buckle_travel_mm": round(BUCKLE_TRAVEL, 2),
            "strap_cut_mm": round(STRAP_CUT, 2),
            "point_drop_floored_mm": round(POINT_DROP, 2),
            "point_drop_was_floored": bool(abs(POINT_DROP - point_drop) > 0.01),
            "welt_clamped_mm": round(WELT_LEN, 2),
            "welt_was_clamped": bool(abs(WELT_LEN - _WELT_RAW) > 0.01),
            "note": "the cinch strap is cut to the MEASURED back gap plus the "
                    "buckle's travel plus the wrap round the bar, so the vest can "
                    "cinch and let out — a strap cut to the gap alone cannot "
                    "tighten. The front buttons are pitched above the point, the "
                    "point drop is floored so it cannot invert, and the welts are "
                    "clamped against the front.",
        },
        "hardware": "strap buckle via Yantra4D (notion.hardware_ref -> strap-buckle); "
                    "the solid's webbing is fed from this garment's strap_width, "
                    "which also sizes the cinch strap the buckle grips. The front "
                    "buttons are a companion hard good, marked and counted.",
    }
    return pattern


result = build()

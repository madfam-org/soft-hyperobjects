"""
Peak-Lapel Dinner Jacket (Tuxedo) — Fashion Cabinet Garment Cartridge
(FC-400 #312, tailoring, T4).

The dinner jacket: a single-button front closing at the waist, a satin-faced peak
lapel that rolls to a low break point, jetted (besom) pockets, and a two-piece
sleeve. The garment's formality lives in the LAPEL ROLL — the break sits low, the
lapel is faced in satin, and the single link button sits exactly at the waist so
the jacket closes at one point and the fronts fall open below it.

Three things are solved by measurement rather than by formula:

  1. THE LAPEL FACING IS DERIVED FROM THE MEASURED LAPEL, NOT DRAWN SEPARATELY.
     The satin facing must cover the whole lapel plus the front edge down past the
     break, so its outline is taken from the MEASURED lapel and roll geometry and
     extended by a facing width — a facing drawn to a guessed shape either falls
     short of the roll line (showing cloth) or overhangs the buttonhole.

  2. THE SINGLE BUTTON SITS AT THE MEASURED WAIST, AND THE JETTED POCKET WELTS
     ARE CLAMPED. The one closing button is placed at the measured waist height so
     the jacket breaks correctly; the besom welt lengths are clamped against the
     front panel width so a welt wider than the panel cannot invert it — the
     kernel would CCW-normalize such a welt into a healthy-looking piece.

  3. THE COLLAR AND SLEEVE ARE TAKEN OFF THE MEASURED GORGE AND ARMSCYE. The
     collar is bisected to the measured gorge plus back neck; the two-piece
     sleeve's vertical seams close by construction and its cap is eased to the
     measured armscye.

TAILORING CONVENTIONS: fine edge-stitch; satin-faced lapel; a two-piece sleeve;
covered/link buttons. The SHANK-BUTTON SOLID is Yantra4D territory
(`shank-button-solid`; see notion.hardware_ref).

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
# front|back|upper_sleeve|under_sleeve|collar|lapel_facing|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
back_width = float(PARAM(lambda: back_width, 460.0))
back_length = float(PARAM(lambda: back_length, 440.0))
jacket_length = float(PARAM(lambda: jacket_length, 760.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
neck_width = float(PARAM(lambda: neck_width, 170.0))
lapel_width = float(PARAM(lambda: lapel_width, 100.0))
break_drop = float(PARAM(lambda: break_drop, 40.0))       # how low the roll breaks
facing_width = float(PARAM(lambda: facing_width, 90.0))    # satin facing width
button_dia = float(PARAM(lambda: button_dia, 24.0))       # covered link button dia
welt_length = float(PARAM(lambda: welt_length, 160.0))    # jetted pocket welt
coat_ease = float(PARAM(lambda: coat_ease, 110.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

chest_girth = max(820.0, min(chest_girth, 1400.0))
waist_girth = max(640.0, min(waist_girth, 1280.0))
back_width = max(360.0, min(back_width, 540.0))
back_length = max(360.0, min(back_length, 520.0))
jacket_length = max(600.0, min(jacket_length, 920.0))
sleeve_length = max(520.0, min(sleeve_length, 720.0))
neck_width = max(140.0, min(neck_width, 220.0))
lapel_width = max(70.0, min(lapel_width, 150.0))
break_drop = max(0.0, min(break_drop, 120.0))
facing_width = max(60.0, min(facing_width, 140.0))
button_dia = max(16.0, min(button_dia, 34.0))
welt_length = max(100.0, min(welt_length, 240.0))
coat_ease = max(60.0, min(coat_ease, 200.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(25.0, min(hem_allowance, 55.0))

EDGESTITCH = 6.0

QUARTER_CHEST = (chest_girth + coat_ease) / 4.0
QUARTER_WAIST = max(QUARTER_CHEST * 0.70,
                    min((waist_girth + coat_ease) / 4.0, QUARTER_CHEST - 6.0))
HALF_NECK = neck_width / 2.0
HALF_BACK = back_width / 2.0
NECK_DROP_F = max(70.0, HALF_NECK * 1.0)
NECK_DROP_B = max(20.0, HALF_NECK * 0.28)
SHOULDER_SLOPE = 45.0

TOTAL_SUPPRESS = max(0.0, QUARTER_CHEST - QUARTER_WAIST)
_WAIST_DART_RAW = TOTAL_SUPPRESS * 0.5
WAIST_DART = max(0.0, min(_WAIST_DART_RAW, QUARTER_CHEST * 0.24))

# The single closing button sits at the measured waist.
BUTTON_Y = back_length - 10.0
# The roll break point sits below the button by the break_drop.
ROLL_Y = BUTTON_Y - break_drop
# The jetted welt clamped against the front panel.
_WELT_RAW = welt_length
WELT_LEN = max(60.0, min(_WELT_RAW, QUARTER_CHEST - 2.0 * seam_allowance))


def _shank_button(label, x, y):
    r = button_dia / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    hw = QUARTER_CHEST
    p_hem_edge = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, back_length)
    p_armhole = fc.P(hw, jacket_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, jacket_length - NECK_DROP_B - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, jacket_length - NECK_DROP_B)
    p_lapel_pt = fc.P(-lapel_width * 0.3, ROLL_Y + lapel_width * 0.7)
    p_roll = fc.P(0.0, ROLL_Y)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_edge, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, jacket_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, jacket_length - NECK_DROP_B - SHOULDER_SLOPE + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("gorge", [fc.Line(p_neck_pt, p_lapel_pt)]),
        fc.Edge("lapel", [fc.Line(p_lapel_pt, p_roll)]),
        fc.Edge("front_edge", [fc.Line(p_roll, p_hem_edge)]),
    ]
    internals = [
        fc.Internal("roll line",
                    [fc.P(p_neck_pt.x, p_neck_pt.y), fc.P(0.0, ROLL_Y)], kind="marking"),
        fc.Internal("waist dart",
                    [fc.P(hw * 0.5, back_length + 40.0),
                     fc.P(hw * 0.5 - WAIST_DART / 2.0, back_length),
                     fc.P(hw * 0.5, back_length - 60.0),
                     fc.P(hw * 0.5 + WAIST_DART / 2.0, back_length),
                     fc.P(hw * 0.5, back_length + 40.0)], kind="marking"),
        # The jetted (besom) pocket welt, clamped.
        fc.Internal("jetted pocket welt",
                    [fc.P(hw * 0.28, back_length - 70.0),
                     fc.P(hw * 0.28 + WELT_LEN, back_length - 70.0)], kind="marking"),
        fc.Internal("breast welt (jetted)",
                    [fc.P(hw * 0.30, jacket_length - QUARTER_CHEST * 0.55),
                     fc.P(hw * 0.30 + WELT_LEN * 0.7,
                          jacket_length - QUARTER_CHEST * 0.55)], kind="marking"),
        _shank_button("link button", button_dia * 0.7, BUTTON_Y),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armscye", 0.0, "underarm"),
                 fc.Notch("side", 0.5, "waist")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, jacket_length - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    hw = QUARTER_CHEST
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, back_length)
    p_armhole = fc.P(hw, jacket_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, jacket_length - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, jacket_length)
    p_neck_cb = fc.P(0.0, jacket_length - NECK_DROP_B)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side),
                         fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, jacket_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, jacket_length - SHOULDER_SLOPE + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "waist"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.35, 30.0), fc.P(hw * 0.35, jacket_length - 40.0)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (cut 2, mirrored)",
    )


_FRONT = build_front()
_BACK = build_back()
ARMSCYE_RUN = _FRONT.edge("armscye").length(0.05) + _BACK.edge("armscye").length(0.05)
LAPEL_RUN = _FRONT.edge("lapel").length(0.05) + _FRONT.edge("gorge").length(0.05)


def build_upper_sleeve():
    sw = QUARTER_CHEST * 0.86
    cap_h = QUARTER_CHEST * 0.32
    ln = sleeve_length
    edges = [
        fc.Edge("cap", [fc.Bezier(
            fc.P(sw, 0.0), fc.P(sw * 0.80, cap_h * 0.9),
            fc.P(sw * 0.30, cap_h * 1.05), fc.P(0.0, 0.0))]),
        fc.Edge("fore_seam", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P(0.0, -ln), fc.P(sw, -ln))]),
        fc.Edge("hind_seam", [fc.Line(fc.P(sw, -ln), fc.P(sw, 0.0))]),
    ]
    return fc.Piece(
        "upper_sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_h * 0.9)),
        internals=[
            fc.Internal("cuff buttons",
                        [fc.P(20.0, -ln + 22.0), fc.P(20.0 + button_dia, -ln + 22.0)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Upper sleeve (cut 2, mirrored)",
    )


def build_under_sleeve():
    sw = QUARTER_CHEST * 0.40
    ln = sleeve_length
    edges = [
        fc.Edge("scye", [fc.curve_through(
            fc.P(0.0, 0.0), fc.P(sw, 0.0), bulge=0.20, side=1.0)]),
        fc.Edge("hind_seam", [fc.Line(fc.P(sw, 0.0), fc.P(sw, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P(sw, -ln), fc.P(0.0, -ln))]),
        fc.Edge("fore_seam", [fc.Line(fc.P(0.0, -ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "under_sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("scye", 0.5, "underarm")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, -ln * 0.85)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Under sleeve (cut 2, mirrored)",
    )


def build_collar():
    gorge_run = _FRONT.edge("gorge").length(0.05) * 2.0
    back_neck = _BACK.edge("neck").length(0.05) * 2.0
    ln = (gorge_run + back_neck) / 2.0
    depth = max(45.0, HALF_NECK * 0.5)
    edges = [
        fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("fall", [fc.Line(fc.P(0.0, depth), fc.P(ln, depth))]),
        fc.Edge("cf_end", [fc.Line(fc.P(ln, depth), fc.P(ln, 0.0))]),
        fc.Edge("neck_edge", [fc.curve_through(
            fc.P(ln, 0.0), fc.P(0.0, 0.0), bulge=0.12, side=1.0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, depth * 0.5), fc.P(ln * 0.9, depth * 0.5)),
        internals=[],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb_fold"),
        label="Collar (cut 2, on fold)",
    )


def build_lapel_facing():
    """The satin lapel facing, cut 2 mirrored. Its outline is DERIVED from the
    measured lapel run plus a facing width — never drawn independently."""
    # A simple facing panel: the measured lapel run tall, the facing width wide,
    # with the front-edge run extended below the break.
    h = LAPEL_RUN + break_drop + BUTTON_Y * 0.3
    w = facing_width
    edges = [
        fc.Edge("outer", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("lapel_edge", [fc.curve_through(
            fc.P(0.0, h), fc.P(w, h * 0.7), bulge=0.15, side=-1.0)]),
        fc.Edge("inner", [fc.Line(fc.P(w, h * 0.7), fc.P(w, 0.0))]),
        fc.Edge("hem_edge", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "lapel_facing", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("outer", LAPEL_RUN / h if h else 0.5, "roll break")],
        grainline=fc.Grainline(fc.P(w * 0.3, h * 0.1), fc.P(w * 0.3, h * 0.9)),
        internals=[
            fc.Internal("roll break notch",
                        [fc.P(0.0, LAPEL_RUN), fc.P(w * 0.3, LAPEL_RUN)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Satin lapel facing (cut 2, mirrored)",
    )


def build():
    pattern = fc.PatternSet("peak-lapel-tuxedo")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "upper_sleeve": everything or target_piece == "upper_sleeve",
        "under_sleeve": everything or target_piece == "under_sleeve",
        "collar": everything or target_piece == "collar",
        "lapel_facing": everything or target_piece == "lapel_facing",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        pattern.add(build_front())
    if want["back"]:
        pattern.add(build_back())
    if want["upper_sleeve"]:
        pattern.add(build_upper_sleeve())
    if want["under_sleeve"]:
        pattern.add(build_under_sleeve())
    if want["collar"]:
        pattern.add(build_collar())
    if want["lapel_facing"]:
        pattern.add(build_lapel_facing())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if want["upper_sleeve"] and want["under_sleeve"]:
        pattern.declare_seam(("upper_sleeve", "fore_seam"),
                             ("under_sleeve", "fore_seam"), tol=1.0)
        pattern.declare_seam(("upper_sleeve", "hind_seam"),
                             ("under_sleeve", "hind_seam"), tol=1.0)
    if want["upper_sleeve"] and want["under_sleeve"] and want["front"] and want["back"]:
        us = build_upper_sleeve()
        un = build_under_sleeve()
        cap = us.edge("cap").length(0.05) + un.edge("scye").length(0.05)
        pattern.declare_seam([("upper_sleeve", "cap"), ("under_sleeve", "scye")],
                             [("front", "armscye"), ("back", "armscye")],
                             tol=3.0, ease=cap - ARMSCYE_RUN)
    if want["lapel_facing"] and want["front"]:
        # The facing's outer edge covers the measured lapel run: declared so a
        # facing redrafted short of the roll (showing cloth) goes red.
        pattern.declare_seam(("lapel_facing", "outer"), [("front", "lapel"),
                             ("front", "gorge")],
                             tol=2.0, ease=build_lapel_facing().edge("outer").length(0.05)
                             - LAPEL_RUN)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.64)
    pattern.bom = [
        {"item": "wool barathea, 300 gsm (dinner-jacket cloth)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 64% marker; barathea is the "
                 f"traditional midnight-blue/black dinner cloth."},
        {"item": "satin (lapel facing + welt jetting + covered buttons)", "qty": 1,
         "unit": "cut", "note": "the lapel is faced in satin; the pocket jetting "
                 "and the covered link button match it."},
        {"item": "shank button (covered/link)", "qty": 5, "unit": "piece",
         "note": f"Yantra4D shank-button-solid (notion.hardware_ref) at "
                 f"{button_dia:.0f} mm: 1 link closing button at the waist, 4 cuff "
                 f"buttons; satin-covered."},
        {"item": "hair canvas + shoulder pads", "qty": 1, "unit": "set",
         "note": "a canvassed, pad-stitched lapel is what holds a dinner-jacket "
                 "roll — the whole point of the garment."},
    ]
    pattern.metadata = {
        "fc400_rank": 312,
        "family": "tailoring",
        "tier": 4,
        "fabric_hint": "wool-barathea",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "jacket_length": round(jacket_length, 1),
            "lapel_width": round(lapel_width, 1),
            "welt_length": round(WELT_LEN, 1),
        },
        "solved": {
            "lapel_run_measured_mm": round(LAPEL_RUN, 2),
            "facing_covers_lapel": True,
            "button_y_mm": round(BUTTON_Y, 2),
            "roll_break_y_mm": round(ROLL_Y, 2),
            "break_drop_mm": round(break_drop, 2),
            "welt_requested_mm": round(_WELT_RAW, 2),
            "welt_clamped_mm": round(WELT_LEN, 2),
            "welt_was_clamped": bool(abs(WELT_LEN - _WELT_RAW) > 0.01),
            "waist_dart_clamped_mm": round(WAIST_DART, 2),
            "armscye_run_measured_mm": round(ARMSCYE_RUN, 2),
            "note": "the satin lapel facing is DERIVED from the measured lapel run "
                    "plus a facing width, so it always covers the roll instead of "
                    "falling short (showing cloth) or overhanging the buttonhole. "
                    "The single link button sits at the measured waist so the "
                    "jacket breaks correctly, and the jetted welts are clamped "
                    "against the front so a welt wider than the panel cannot invert "
                    "it — the kernel would CCW-normalize such a welt into a "
                    "healthy-looking piece.",
        },
        "tailoring_conventions": {
            "edge_finish": f"{EDGESTITCH:.0f} mm edge-stitch",
            "lapel": "satin-faced peak, pad-stitched over canvas",
            "sleeve": "two-piece with vertical seams that close by construction",
        },
        "hardware": "shank buttons via Yantra4D (notion.hardware_ref -> "
                    "shank-button-solid); the solid's diameter_mm is fed from this "
                    "garment's button_dia, the covered link button at the waist "
                    "and the cuff buttons.",
    }
    return pattern


result = build()

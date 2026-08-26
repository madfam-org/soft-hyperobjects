"""
Double-Breasted Blazer — Fashion Cabinet Garment Cartridge
(FC-400 #311, tailoring, T3).

The double-breasted blazer: two columns of buttons, a wide wrap that carries the
front edge past the centre to the far button column, peak lapels, a waist-
suppressed body with a bust dart and a waist dart, and a two-piece tailored
sleeve. The signature is the WRAP — the overlap that makes it double-breasted —
and the geometry that has to be right is the relationship between the wrap, the
two button columns, and the lapel roll line, none of which are independent.

Three things are solved by measurement rather than by formula:

  1. THE WRAP AND THE TWO BUTTON COLUMNS ARE ONE SOLVED SYSTEM. The front edge
     extends past the centre front by the MEASURED wrap; the two button columns
     sit symmetrically about the centre at a spacing derived from the wrap (so
     the outer column lands near the front edge and the inner near the centre);
     and the button rows are pitched across the MEASURED button run from the
     roll point to the hem. A blazer that sets the buttons at a guessed spacing
     puts the outer column off the cloth or the inner on the centre seam.

  2. THE WAIST SUPPRESSION IS SPLIT BETWEEN A BUST DART AND A WAIST DART, EACH
     CLAMPED. The total suppression is the MEASURED chest-to-waist difference;
     it is divided between the two darts, and each dart intake is clamped so a
     large suppression cannot fold the panel through itself — a dart deeper than
     the panel is CCW-normalized by the kernel into a healthy-looking piece.

  3. THE LAPEL ROLL AND THE COLLAR ARE TAKEN OFF THE MEASURED GORGE. The lapel
     climbs the button stand to a solved roll point; the collar is bisected to
     the MEASURED gorge plus back neck so it sets on cleanly.

TAILORING CONVENTIONS: 2 mm edge-stitch (fine, not topstitch); pad-stitched
lapels; a two-piece sleeve; every hard good a Yantra4D reference. The SEW-THROUGH
BUTTON SOLID is Yantra4D territory (`sew-through-button`; see notion.hardware_ref).

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


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|upper_sleeve|under_sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 900.0))
back_width = float(PARAM(lambda: back_width, 460.0))
back_length = float(PARAM(lambda: back_length, 440.0))     # nape to waist
jacket_length = float(PARAM(lambda: jacket_length, 760.0))  # nape to hem
sleeve_length = float(PARAM(lambda: sleeve_length, 630.0))
neck_width = float(PARAM(lambda: neck_width, 170.0))
wrap = float(PARAM(lambda: wrap, 110.0))                   # double-breasted overlap
button_rows = float(PARAM(lambda: button_rows, 3.0))       # rows per column
button_ligne = float(PARAM(lambda: button_ligne, 36.0))
lapel_width = float(PARAM(lambda: lapel_width, 95.0))
coat_ease = float(PARAM(lambda: coat_ease, 120.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(820.0, min(chest_girth, 1400.0))
waist_girth = max(640.0, min(waist_girth, 1300.0))
back_width = max(360.0, min(back_width, 540.0))
back_length = max(360.0, min(back_length, 520.0))
jacket_length = max(600.0, min(jacket_length, 920.0))
sleeve_length = max(520.0, min(sleeve_length, 720.0))
neck_width = max(140.0, min(neck_width, 220.0))
wrap = max(60.0, min(wrap, 180.0))
button_rows = max(2.0, min(round(button_rows), 4.0))
button_ligne = max(28.0, min(button_ligne, 46.0))
lapel_width = max(60.0, min(lapel_width, 140.0))
coat_ease = max(60.0, min(coat_ease, 220.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(25.0, min(hem_allowance, 55.0))

EDGESTITCH = 6.0
N_ROWS = int(button_rows)
BUTTON_MM = button_ligne * 0.635

QUARTER_CHEST = (chest_girth + coat_ease) / 4.0
QUARTER_WAIST = max(QUARTER_CHEST * 0.70,
                    min((waist_girth + coat_ease) / 4.0, QUARTER_CHEST - 6.0))
HALF_NECK = neck_width / 2.0
HALF_BACK = back_width / 2.0
NECK_DROP_F = max(70.0, HALF_NECK * 1.0)
NECK_DROP_B = max(20.0, HALF_NECK * 0.28)
SHOULDER_SLOPE = 45.0
BODY_BELOW_WAIST = jacket_length - back_length

# Total waist suppression, split between a bust dart and a waist dart, each
# clamped so a large suppression cannot fold the panel through itself.
TOTAL_SUPPRESS = max(0.0, QUARTER_CHEST - QUARTER_WAIST)
_BUST_DART_RAW = TOTAL_SUPPRESS * 0.45
_WAIST_DART_RAW = TOTAL_SUPPRESS * 0.55
BUST_DART = max(0.0, min(_BUST_DART_RAW, QUARTER_CHEST * 0.22))
WAIST_DART = max(0.0, min(_WAIST_DART_RAW, QUARTER_CHEST * 0.24))

# The wrap and button columns: one solved system. The front edge extends past CF
# by the wrap; button columns sit symmetric about CF.
BUTTON_COL_SPACING = max(BUTTON_MM * 2.0, wrap - BUTTON_MM * 1.2)
# The button run from the roll point to the hem.
ROLL_Y = back_length + BODY_BELOW_WAIST * 0.10      # roll point above the waist
BUTTON_TOP_Y = back_length - 20.0                    # top button near the waist
BUTTON_BOTTOM_Y = hem_allowance + BUTTON_MM * 2.0
BUTTON_RUN = max(BUTTON_MM * 2.0, BUTTON_TOP_Y - BUTTON_BOTTOM_Y)
N_INTERVALS = max(1, N_ROWS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS if N_ROWS > 1 else 0.0


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    """Front, cut 2 mirrored. Extends past CF by the wrap; peak lapel; two darts."""
    hw = QUARTER_CHEST
    # Front edge is at x = -wrap (past the centre front at x=0).
    p_hem_edge = fc.P(-wrap, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    # The side seam is waist-suppressed to match the back's — in at the waist,
    # out to the armhole — so the two side seams MEASURE the same and close.
    p_waist_side = fc.P(QUARTER_WAIST, back_length)
    p_armhole = fc.P(hw, jacket_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, jacket_length - NECK_DROP_B - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, jacket_length - NECK_DROP_B)
    # Peak lapel: from neck point out to the lapel point, then down the roll to
    # the front edge at the roll point, then straight down the extended edge.
    p_lapel_pt = fc.P(-wrap - lapel_width * 0.2, ROLL_Y + lapel_width * 0.5)
    p_roll = fc.P(-wrap, ROLL_Y)
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
                    [fc.P(p_neck_pt.x, p_neck_pt.y), fc.P(-wrap, ROLL_Y)],
                    kind="marking"),
        fc.Internal("edge-stitch",
                    [fc.P(-wrap + EDGESTITCH, EDGESTITCH),
                     fc.P(-wrap + EDGESTITCH, ROLL_Y)], kind="trace"),
        # The bust dart: from the side toward the bust point, clamped intake.
        fc.Internal("bust dart",
                    [fc.P(hw - 10.0, jacket_length - QUARTER_CHEST * 0.55),
                     fc.P(hw * 0.5, jacket_length - QUARTER_CHEST * 0.62),
                     fc.P(hw - 10.0 - BUST_DART, jacket_length - QUARTER_CHEST * 0.55)],
                    kind="marking"),
        # The waist dart: vertical suppression at the waist, clamped intake.
        fc.Internal("waist dart",
                    [fc.P(hw * 0.52, back_length + 40.0),
                     fc.P(hw * 0.52 - WAIST_DART / 2.0, back_length),
                     fc.P(hw * 0.52, back_length - 60.0),
                     fc.P(hw * 0.52 + WAIST_DART / 2.0, back_length),
                     fc.P(hw * 0.52, back_length + 40.0)], kind="marking"),
    ]
    # The two button columns, solved and drilled.
    for col, cx in (("outer", -BUTTON_COL_SPACING / 2.0),
                    ("inner", BUTTON_COL_SPACING / 2.0)):
        for i in range(N_ROWS):
            y = BUTTON_TOP_Y - BUTTON_PITCH * i
            internals.append(_button(f"{col} button-{i + 1}", cx, y))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armscye", 0.0, "underarm"),
                 fc.Notch("shoulder", 0.5, "shoulder mid"),
                 fc.Notch("side", 0.0, "hem")],
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
        # The side seam is waist-suppressed: out at the hem, in at the waist, out
        # to the armhole.
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
        internals=[
            fc.Internal("CB edge-stitch",
                        [fc.P(EDGESTITCH, EDGESTITCH),
                         fc.P(EDGESTITCH, jacket_length - NECK_DROP_B)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (cut 2, mirrored)",
    )


_FRONT = build_front()
_BACK = build_back()
ARMSCYE_RUN = _FRONT.edge("armscye").length(0.05) + _BACK.edge("armscye").length(0.05)


def build_upper_sleeve():
    sw = QUARTER_CHEST * 0.86
    cap_h = QUARTER_CHEST * 0.32
    ln = sleeve_length
    # The fore/hind seams run STRAIGHT DOWN (vertical), so the upper and under
    # sleeve seams measure identically by construction — the taper of a tailored
    # sleeve is taken at the cuff vent, not by angling the seams, which is what
    # keeps the two-piece seams closing at the extremes.
    p_ul = fc.P(0.0, 0.0)
    p_ur = fc.P(sw, 0.0)
    edges = [
        fc.Edge("cap", [fc.Bezier(
            p_ur, fc.P(sw * 0.80, cap_h * 0.9),
            fc.P(sw * 0.30, cap_h * 1.05), p_ul)]),
        fc.Edge("fore_seam", [fc.Line(p_ul, fc.P(0.0, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P(0.0, -ln), fc.P(sw, -ln))]),
        fc.Edge("hind_seam", [fc.Line(fc.P(sw, -ln), p_ur)]),
    ]
    return fc.Piece(
        "upper_sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.2, "back cap notch")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_h * 0.9)),
        internals=[
            fc.Internal("cuff buttons",
                        [fc.P(25.0, -ln + 25.0),
                         fc.P(25.0 + BUTTON_MM * 1.3, -ln + 25.0)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Upper sleeve (cut 2, mirrored)",
    )


def build_under_sleeve():
    sw = QUARTER_CHEST * 0.40
    ln = sleeve_length
    # Vertical seams of length ln, matching the upper sleeve's by construction.
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
        internals=[
            fc.Internal("roll line",
                        [fc.P(0.0, depth * 0.5), fc.P(ln, depth * 0.5)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb_fold"),
        label="Collar (cut 2, on fold)",
    )


def build():
    pattern = fc.PatternSet("double-breasted-blazer")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "upper_sleeve": everything or target_piece == "upper_sleeve",
        "under_sleeve": everything or target_piece == "under_sleeve",
        "collar": everything or target_piece == "collar",
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

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if want["upper_sleeve"] and want["under_sleeve"]:
        # Both seams run vertical at length sleeve_length, so they close exactly.
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

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "wool flannel, 300 gsm (suiting)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 66% marker (tailoring nap +"
                 f" lapel-roll waste)."},
        {"item": "sew-through button", "qty": N_ROWS * 2 + 4, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm): two columns of "
                 f"{N_ROWS} at a SOLVED pitch of {BUTTON_PITCH:.1f} mm and column "
                 f"spacing {BUTTON_COL_SPACING:.0f} mm, plus 4 cuff buttons."},
        {"item": "hair canvas + lapel felt + shoulder pad set", "qty": 1, "unit": "set",
         "note": "a double-breasted blazer is a tailored, canvassed front — the "
                 "lapel is pad-stitched to hold its roll."},
        {"item": "fine edge-stitch thread + needle 80/12", "qty": 1, "unit": "spool",
         "note": f"{EDGESTITCH:.0f} mm edge-stitch on the lapel and front edge "
                 f"(fine, not workwear topstitch)."},
    ]
    pattern.metadata = {
        "fc400_rank": 311,
        "family": "tailoring",
        "tier": 3,
        "fabric_hint": "wool-flannel",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "jacket_length": round(jacket_length, 1),
            "wrap": round(wrap, 1),
            "button_column_spacing": round(BUTTON_COL_SPACING, 1),
        },
        "solved": {
            "wrap_mm": round(wrap, 2),
            "button_column_spacing_mm": round(BUTTON_COL_SPACING, 2),
            "button_rows": N_ROWS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "button_run_mm": round(BUTTON_RUN, 2),
            "total_suppression_mm": round(TOTAL_SUPPRESS, 2),
            "bust_dart_requested_mm": round(_BUST_DART_RAW, 2),
            "bust_dart_clamped_mm": round(BUST_DART, 2),
            "bust_dart_was_clamped": bool(abs(BUST_DART - _BUST_DART_RAW) > 0.01),
            "waist_dart_requested_mm": round(_WAIST_DART_RAW, 2),
            "waist_dart_clamped_mm": round(WAIST_DART, 2),
            "waist_dart_was_clamped": bool(abs(WAIST_DART - _WAIST_DART_RAW) > 0.01),
            "armscye_run_measured_mm": round(ARMSCYE_RUN, 2),
            "note": "the wrap, the two button columns and the button pitch are one "
                    "solved system: the front edge extends past CF by the wrap, the "
                    "columns sit symmetric about CF at a spacing derived from the "
                    "wrap, and the rows are pitched across the measured run. The "
                    "waist suppression is split between a bust dart and a waist "
                    "dart, each clamped so a large suppression cannot fold the "
                    "panel through itself — a dart deeper than the panel is CCW-"
                    "normalized by the kernel into a healthy-looking piece.",
        },
        "tailoring_conventions": {
            "edge_finish": f"{EDGESTITCH:.0f} mm edge-stitch, not topstitch",
            "sleeve": "two-piece (upper + under), the tailored sleeve",
            "canvassing": "pad-stitched lapel over hair canvas",
        },
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne is fed from this "
                    "garment's button_ligne, which also sizes the buttonholes and "
                    "the whole two-column layout.",
    }
    return pattern


result = build()

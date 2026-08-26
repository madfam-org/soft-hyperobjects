"""
Frock Coat — Fashion Cabinet Garment Cartridge (FC-400 #318, tailoring, T4).

The frock coat (levita, redingote): a waist-seamed knee-length coat, double-
breasted, with a bodice cut to the waist and a full skirt hung below it on its own
grain. The garment IS the waist seam — the whole reason a frock coat is drafted
this way rather than as a long jacket is that the skirt can then be cut on its own
straight grain and hang clean, flaring from the waist without the bodice's shaping
dragging it. So the number that has to be right is the reconciliation of the
bodice waist and the skirt top: they must MEASURE the same or the waist seam ripples.

Three things are solved by measurement rather than by formula:

  1. THE BODICE WAIST AND SKIRT TOP ARE RECONCILED TO ONE MEASURED WAIST. The
     bodice narrows to the MEASURED waist quarter and the skirt top is drafted to
     the same quarter, so the waist seam closes at delta zero — the declared seam
     catches any redraft that breaks it.

  2. THE SKIRT FLARE IS SOLVED, NOT DRAWN. The skirt hem width is derived from the
     waist plus a MEASURED flare added at the hem (not the waist), so the skirt
     falls straight from the waist and flares only below — a skirt flared from the
     waist itself pulls the waist seam open. The flare is floored so the hem can
     never come out narrower than the waist (an inverted skirt panel the kernel
     CCW-normalizes into a healthy-looking piece).

  3. THE DOUBLE-BREASTED BUTTON SYSTEM IS SOLVED. The wrap, the two button columns
     and the pitch are one system, as on any double-breasted front, solved off the
     measured wrap.

TAILORING CONVENTIONS: edge-stitch; a waist-seamed skirt on its own grain; a
two-piece sleeve. The SEW-THROUGH BUTTON SOLID is Yantra4D territory
(`sew-through-button`; see notion.hardware_ref).

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
# bodice_front|bodice_back|skirt_front|skirt_back|upper_sleeve|under_sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
back_width = float(PARAM(lambda: back_width, 460.0))
back_length = float(PARAM(lambda: back_length, 440.0))
skirt_length = float(PARAM(lambda: skirt_length, 380.0))    # waist to knee hem
sleeve_length = float(PARAM(lambda: sleeve_length, 630.0))
neck_width = float(PARAM(lambda: neck_width, 170.0))
wrap = float(PARAM(lambda: wrap, 110.0))
button_rows = float(PARAM(lambda: button_rows, 3.0))
button_ligne = float(PARAM(lambda: button_ligne, 36.0))
skirt_flare = float(PARAM(lambda: skirt_flare, 120.0))      # flare added at the hem
lapel_width = float(PARAM(lambda: lapel_width, 90.0))
coat_ease = float(PARAM(lambda: coat_ease, 120.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 45.0))

chest_girth = max(820.0, min(chest_girth, 1400.0))
waist_girth = max(640.0, min(waist_girth, 1300.0))
back_width = max(360.0, min(back_width, 540.0))
back_length = max(360.0, min(back_length, 520.0))
skirt_length = max(280.0, min(skirt_length, 560.0))
sleeve_length = max(520.0, min(sleeve_length, 720.0))
neck_width = max(140.0, min(neck_width, 220.0))
wrap = max(60.0, min(wrap, 180.0))
button_rows = max(2.0, min(round(button_rows), 4.0))
button_ligne = max(28.0, min(button_ligne, 46.0))
skirt_flare = max(0.0, min(skirt_flare, 320.0))
lapel_width = max(60.0, min(lapel_width, 140.0))
coat_ease = max(60.0, min(coat_ease, 220.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(28.0, min(hem_allowance, 65.0))

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
BODICE_LEN = back_length          # bodice height, nape to waist

# The skirt hem quarter: the waist quarter plus a MEASURED flare added at the hem,
# floored so the hem can never come out narrower than the waist.
SKIRT_HEM_QUARTER = QUARTER_WAIST + max(0.0, skirt_flare / 2.0)

# The double-breasted button system.
BUTTON_COL_SPACING = max(BUTTON_MM * 2.0, wrap - BUTTON_MM * 1.2)
ROLL_Y = BODICE_LEN + 30.0
BUTTON_TOP_Y = BODICE_LEN - 20.0
BUTTON_BOTTOM_Y = 20.0
BUTTON_RUN = max(BUTTON_MM * 2.0, BUTTON_TOP_Y - BUTTON_BOTTOM_Y)
BUTTON_PITCH = BUTTON_RUN / max(1, N_ROWS - 1) if N_ROWS > 1 else 0.0


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_bodice_front():
    """Bodice front to the waist, cut 2 mirrored. Extends past CF by the wrap."""
    hw = QUARTER_CHEST
    p_waist_edge = fc.P(-wrap, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, 0.0)
    p_armhole = fc.P(hw, BODICE_LEN - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, BODICE_LEN - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, BODICE_LEN)
    p_lapel_pt = fc.P(-wrap - lapel_width * 0.2, ROLL_Y - BODICE_LEN + lapel_width * 0.5
                      + BODICE_LEN - lapel_width)
    p_roll = fc.P(-wrap, min(BODICE_LEN - 10.0, ROLL_Y - 40.0))
    edges = [
        fc.Edge("waist", [fc.Line(p_waist_edge, p_waist_side)]),
        fc.Edge("side", [fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, BODICE_LEN - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, BODICE_LEN - SHOULDER_SLOPE + 20.0), p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("gorge", [fc.Line(p_neck_pt, p_lapel_pt)]),
        fc.Edge("lapel", [fc.Line(p_lapel_pt, p_roll)]),
        fc.Edge("front_edge", [fc.Line(p_roll, p_waist_edge)]),
    ]
    internals = [
        fc.Internal("roll line", [fc.P(p_neck_pt.x, p_neck_pt.y), fc.P(-wrap, p_roll.y)],
                    kind="marking"),
    ]
    for col, cx in (("outer", -BUTTON_COL_SPACING / 2.0),
                    ("inner", BUTTON_COL_SPACING / 2.0)):
        for i in range(N_ROWS):
            internals.append(_button(f"{col} button-{i + 1}", cx,
                                     BUTTON_TOP_Y - BUTTON_PITCH * i))
    return fc.Piece(
        "bodice_front", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("armscye", 0.0, "underarm"),
                 fc.Notch("waist", 1.0, "side seam / skirt match")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 20.0), fc.P(hw * 0.4, BODICE_LEN - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bodice front (cut 2, mirrored)",
    )


def build_bodice_back():
    hw = QUARTER_CHEST
    p_waist_cb = fc.P(0.0, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, 0.0)
    p_armhole = fc.P(hw, BODICE_LEN - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, BODICE_LEN - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, BODICE_LEN)
    p_neck_cb = fc.P(0.0, BODICE_LEN - NECK_DROP_B)
    edges = [
        fc.Edge("waist", [fc.Line(p_waist_cb, p_waist_side)]),
        fc.Edge("side", [fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, BODICE_LEN - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, BODICE_LEN - SHOULDER_SLOPE + 20.0), p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_waist_cb)]),
    ]
    return fc.Piece(
        "bodice_back", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("waist", 1.0, "side seam / skirt match"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.35, 20.0), fc.P(hw * 0.35, BODICE_LEN - 20.0)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bodice back (cut 2, mirrored)",
    )


def build_skirt_front():
    """Skirt front, cut 2 mirrored. Waist = the MEASURED bodice waist; flares to
    the hem on its own straight grain."""
    # The hem side point matches the back's (SKIRT_HEM_QUARTER) so the two side
    # seams MEASURE the same; the wrap is added ONLY as the front-edge extension
    # (the CF overlap runs at -wrap), not spread across the whole hem.
    p_hem_cf = fc.P(-wrap, 0.0)
    p_hem_side = fc.P(SKIRT_HEM_QUARTER, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, skirt_length)
    p_waist_edge = fc.P(-wrap, skirt_length)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_edge)]),
        fc.Edge("front_edge", [fc.Line(p_waist_edge, p_hem_cf)]),
    ]
    return fc.Piece(
        "skirt_front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "bodice waist match"),
                 fc.Notch("side", 1.0, "side seam")],
        grainline=fc.Grainline(fc.P(SKIRT_HEM_QUARTER * 0.4, 20.0),
                               fc.P(QUARTER_WAIST * 0.4, skirt_length - 20.0)),
        internals=[
            fc.Internal("edge-stitch",
                        [fc.P(-wrap + EDGESTITCH, skirt_length),
                         fc.P(-wrap + EDGESTITCH, EDGESTITCH)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Skirt front (cut 2, mirrored)",
    )


def build_skirt_back():
    """Skirt back, cut 2 mirrored. A centre-back vent pleat, same waist quarter."""
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(SKIRT_HEM_QUARTER, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, skirt_length)
    p_waist_cb = fc.P(0.0, skirt_length)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_cb)]),
        fc.Edge("cb", [fc.Line(p_waist_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "skirt_back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "bodice waist match"),
                 fc.Notch("side", 1.0, "side seam")],
        grainline=fc.Grainline(fc.P(SKIRT_HEM_QUARTER * 0.4, 20.0),
                               fc.P(QUARTER_WAIST * 0.4, skirt_length - 20.0)),
        internals=[
            fc.Internal("CB vent pleat", [fc.P(0.0, 0.0), fc.P(0.0, skirt_length * 0.5)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Skirt back (cut 2, mirrored)",
    )


_BF = build_bodice_front()
_BB = build_bodice_back()
ARMSCYE_RUN = _BF.edge("armscye").length(0.05) + _BB.edge("armscye").length(0.05)


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
        internals=[],
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
    gorge_run = _BF.edge("gorge").length(0.05) * 2.0
    back_neck = _BB.edge("neck").length(0.05) * 2.0
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


def build():
    pattern = fc.PatternSet("frock-coat")
    everything = target_piece == "set"
    want = {
        "bodice_front": everything or target_piece == "bodice_front",
        "bodice_back": everything or target_piece == "bodice_back",
        "skirt_front": everything or target_piece == "skirt_front",
        "skirt_back": everything or target_piece == "skirt_back",
        "upper_sleeve": everything or target_piece == "upper_sleeve",
        "under_sleeve": everything or target_piece == "under_sleeve",
        "collar": everything or target_piece == "collar",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["bodice_front"]:
        pattern.add(build_bodice_front())
    if want["bodice_back"]:
        pattern.add(build_bodice_back())
    if want["skirt_front"]:
        pattern.add(build_skirt_front())
    if want["skirt_back"]:
        pattern.add(build_skirt_back())
    if want["upper_sleeve"]:
        pattern.add(build_upper_sleeve())
    if want["under_sleeve"]:
        pattern.add(build_under_sleeve())
    if want["collar"]:
        pattern.add(build_collar())

    if want["bodice_front"] and want["bodice_back"]:
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.5)
        pattern.declare_seam(("bodice_front", "shoulder"), ("bodice_back", "shoulder"),
                             tol=1.0)
    if want["skirt_front"] and want["skirt_back"]:
        pattern.declare_seam(("skirt_front", "side"), ("skirt_back", "side"), tol=1.5)
    if want["bodice_front"] and want["skirt_front"]:
        # The waist seam: bodice waist to skirt waist, both to the SAME measured
        # quarter (plus the wrap on the front), so they close at delta zero.
        pattern.declare_seam(("bodice_front", "waist"), ("skirt_front", "waist"), tol=0.8)
    if want["bodice_back"] and want["skirt_back"]:
        pattern.declare_seam(("bodice_back", "waist"), ("skirt_back", "waist"), tol=0.8)
    if want["upper_sleeve"] and want["under_sleeve"]:
        pattern.declare_seam(("upper_sleeve", "fore_seam"),
                             ("under_sleeve", "fore_seam"), tol=1.0)
        pattern.declare_seam(("upper_sleeve", "hind_seam"),
                             ("under_sleeve", "hind_seam"), tol=1.0)
    if want["upper_sleeve"] and want["under_sleeve"] and want["bodice_front"] \
            and want["bodice_back"]:
        us = build_upper_sleeve()
        un = build_under_sleeve()
        cap = us.edge("cap").length(0.05) + un.edge("scye").length(0.05)
        pattern.declare_seam([("upper_sleeve", "cap"), ("under_sleeve", "scye")],
                             [("bodice_front", "armscye"), ("bodice_back", "armscye")],
                             tol=3.0, ease=cap - ARMSCYE_RUN)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.64)
    pattern.bom = [
        {"item": "wool melton, 500 gsm (coating)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 64% marker; a heavy melton gives "
                 f"the frock coat's structured skirt and clean edge."},
        {"item": "sew-through button", "qty": N_ROWS * 2 + 4, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm): two columns of "
                 f"{N_ROWS} at a SOLVED pitch of {BUTTON_PITCH:.1f} mm, plus back-"
                 f"waist and cuff buttons."},
        {"item": "hair canvas + shoulder pads", "qty": 1, "unit": "set",
         "note": "a fully canvassed bodice; the skirt hangs from the waist seam "
                 "unlined or half-lined."},
        {"item": "fine edge-stitch thread + needle 90/14", "qty": 1, "unit": "spool",
         "note": f"{EDGESTITCH:.0f} mm edge-stitch on the lapel, front edge and "
                 f"skirt front."},
    ]
    pattern.metadata = {
        "fc400_rank": 318,
        "family": "tailoring",
        "tier": 4,
        "fabric_hint": "wool-melton",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "bodice_length": round(BODICE_LEN, 1),
            "skirt_length": round(skirt_length, 1),
            "skirt_hem_quarter": round(SKIRT_HEM_QUARTER, 1),
            "wrap": round(wrap, 1),
        },
        "solved": {
            "waist_quarter_mm": round(QUARTER_WAIST, 2),
            "skirt_hem_quarter_mm": round(SKIRT_HEM_QUARTER, 2),
            "skirt_flare_mm": round(skirt_flare, 2),
            "skirt_hem_ge_waist": bool(SKIRT_HEM_QUARTER >= QUARTER_WAIST),
            "button_rows": N_ROWS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "button_column_spacing_mm": round(BUTTON_COL_SPACING, 2),
            "armscye_run_measured_mm": round(ARMSCYE_RUN, 2),
            "note": "the bodice waist and the skirt top are both drafted to the "
                    "same MEASURED waist quarter, so the waist seam — the whole "
                    "reason a frock coat is cut this way — closes at delta zero. "
                    "The skirt flare is added at the HEM, not the waist, so the "
                    "skirt falls straight from the waist and flares only below, and "
                    "the flare is floored so the hem can never come out narrower "
                    "than the waist (an inverted panel the kernel CCW-normalizes "
                    "into a healthy-looking piece).",
        },
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne is fed from this "
                    "garment's button_ligne, which also sizes the two-column layout.",
    }
    return pattern


result = build()

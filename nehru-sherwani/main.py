"""
Sherwani — Fashion Cabinet Heritage Cartridge (FC-500 #492, heritage_global; South Asia;
made-to-measure, tier 4).

The sherwani is the fitted long formal coat of South Asia — the men's ceremonial dress of
weddings and state occasions across India, Pakistan and Bangladesh, worn over a kurta and
churidar or a straight trouser. It is a TAILORED garment: fitted through the waist, buttoned
all the way up to a raised stand collar (the Nehru / bandhgala collar), with set-in sleeves and
a flared skirt below the waist. This is the made-to-measure tier of the FC-500 heritage lane,
and its draft is a fitted coat block, not a panel robe.

Three things the draft solves honestly:

  1. THE BODY IS FITTED AND THE WAIST IS SOLVED FROM THE MEASURES. The coat follows the figure:
     the waist is solved from the chest-waist-hip measurements and suppressed with a side take-in
     plus a vertical dart, and the skirt flares below the waist. It is drafted from body
     measurements, not a size chart.

  2. THE SLEEVE CAP IS CUT TO THE MEASURED ARMSCYE. A tailored set-in sleeve hangs only if the
     cap equals the armhole; the cap is solved to the MEASURED front + back armscye, and the
     declared seam proves it.

  3. THE STAND COLLAR IS CUT TO THE MEASURED NECKLINE. The bandhgala stand is cut to the
     MEASURED neck run, not a neck girth, so it closes cleanly at the throat.

Pieces:
  - front  : the fitted front (cut 2), full button front, waist dart, flared skirt.
  - back   : the fitted back (cut on fold), waist dart, flared skirt, centre vent.
  - sleeve : the two-part-feel long sleeve (cut 2), cap MEASURED to the armscye.
  - collar : the bandhgala stand collar, cut to the MEASURED neckline.

Hardware: full front buttons — Yantra4D shank-button-solid, LINKED (metal or covered shank
buttons, the sherwani signature).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
hip_girth = float(PARAM(lambda: hip_girth, 1020.0))
sherwani_length = float(PARAM(lambda: sherwani_length, 1140.0))  # nape to hem (knee/calf)
neck_girth = float(PARAM(lambda: neck_girth, 410.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
armhole_depth = float(PARAM(lambda: armhole_depth, 250.0))
nape_to_waist = float(PARAM(lambda: nape_to_waist, 440.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 220.0))
collar_height = float(PARAM(lambda: collar_height, 48.0))
skirt_flare = float(PARAM(lambda: skirt_flare, 120.0))       # extra hem width per side vs hip
chest_ease = float(PARAM(lambda: chest_ease, 90.0))
button_diameter = float(PARAM(lambda: button_diameter, 16.0))  # shank button diameter (mm)
button_count = int(PARAM(lambda: button_count, 6))
back_vent = float(PARAM(lambda: back_vent, 300.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(840.0, min(chest_girth, 1300.0))
waist_girth = max(680.0, min(waist_girth, 1200.0))
hip_girth = max(860.0, min(hip_girth, 1350.0))
sherwani_length = max(1000.0, min(sherwani_length, 1350.0))
neck_girth = max(360.0, min(neck_girth, 480.0))
shoulder_width = max(400.0, min(shoulder_width, 520.0))
sleeve_length = max(560.0, min(sleeve_length, 720.0))
armhole_depth = max(220.0, min(armhole_depth, 320.0))
nape_to_waist = max(400.0, min(nape_to_waist, 500.0))
wrist_girth = max(180.0, min(wrist_girth, 280.0))
collar_height = max(32.0, min(collar_height, 65.0))
skirt_flare = max(40.0, min(skirt_flare, 240.0))
chest_ease = max(50.0, min(chest_ease, 160.0))
button_diameter = max(11.0, min(button_diameter, 26.0))
button_count = max(4, min(button_count, 12))
back_vent = max(150.0, min(back_vent, 500.0))
seam_allowance = max(8.0, min(seam_allowance, 16.0))
hem_allowance = max(15.0, min(hem_allowance, 70.0))

# ── Fit solve ────────────────────────────────────────────────────────────────
CHEST_Q = (chest_girth + chest_ease) / 4.0
WAIST_Q = (waist_girth + chest_ease * 0.55) / 4.0
HIP_Q = (hip_girth + chest_ease * 0.7) / 4.0
WAIST_SUPP = max(CHEST_Q - WAIST_Q, 0.0)
SIDE_TAKE = WAIST_SUPP * 0.5
DART_TAKE = WAIST_SUPP - SIDE_TAKE
HALF_SHOULDER = shoulder_width / 2.0
NECK_HALF = min((neck_girth + 26.0) / 4.0, HALF_SHOULDER - 30.0)
FRONT_NECK_DROP = min(NECK_HALF * 0.65 + 10.0, 60.0)   # a stand collar sits high
BACK_NECK_DROP = 22.0
armhole_depth = min(armhole_depth, nape_to_waist - 40.0)
back_vent = min(back_vent, (sherwani_length - nape_to_waist) * 0.9)
SHOULDER_Y = sherwani_length
WAIST_Y = sherwani_length - nape_to_waist
UNDERARM_Y = sherwani_length - armhole_depth
HEM_Q = HIP_Q + skirt_flare               # the skirt flares below the hip


def _armscye(x_side, y_underarm, x_shoulder, y_shoulder, front):
    bias = 0.42 if front else 0.30
    run = x_side - x_shoulder
    rise = y_shoulder - y_underarm
    return fc.Bezier(
        fc.P(x_side, y_underarm),
        fc.P(x_side - run * 0.10, y_underarm + rise * 0.42),
        fc.P(x_shoulder + run * bias, y_shoulder - rise * 0.12),
        fc.P(x_shoulder, y_shoulder))


def _fitted_side(y_hem, y_waist, y_underarm, x_hem, x_waist, x_bust):
    """Side seam: flared at the hem, in at the waist, out to the underarm."""
    return [
        fc.Bezier(fc.P(x_hem, y_hem),
                  fc.P(x_hem - (x_hem - x_waist) * 0.3, y_hem + (y_waist - y_hem) * 0.5),
                  fc.P(x_waist, y_waist - (y_waist - y_hem) * 0.18),
                  fc.P(x_waist, y_waist)),
        fc.Bezier(fc.P(x_waist, y_waist),
                  fc.P(x_waist, y_waist + (y_underarm - y_waist) * 0.30),
                  fc.P(x_bust, y_underarm - (y_underarm - y_waist) * 0.35),
                  fc.P(x_bust, y_underarm)),
    ]


def build_front():
    x_hem = HEM_Q
    x_waist = WAIST_Q + SIDE_TAKE
    x_bust = CHEST_Q
    x_shoulder = HALF_SHOULDER
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_hem, 0.0)
    p_shoulder_tip = fc.P(x_shoulder, SHOULDER_Y)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y)
    p_neck_cf = fc.P(0.0, SHOULDER_Y - FRONT_NECK_DROP)
    side = _fitted_side(0.0, WAIST_Y, UNDERARM_Y, x_hem, x_waist, x_bust)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", side),
        fc.Edge("armhole", [_armscye(x_bust, UNDERARM_Y, x_shoulder, SHOULDER_Y, True)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.6, SHOULDER_Y - 4.0),
                                   fc.P(NECK_HALF * 0.28, p_neck_cf.y + 6.0),
                                   p_neck_cf)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("waist-dart",
                    [fc.P(x_bust * 0.5, WAIST_Y - 110.0),
                     fc.P(x_bust * 0.5 - DART_TAKE * 0.5, WAIST_Y),
                     fc.P(x_bust * 0.5, WAIST_Y + 130.0)], kind="dart"),
    ]
    span = (SHOULDER_Y - FRONT_NECK_DROP) - 40.0
    for i in range(button_count):
        t = (i + 0.5) / button_count
        y = 40.0 + span * t
        bx = 10.0 + button_diameter
        internals.append(fc.Internal(f"button-{i + 1}", [fc.P(10.0, y), fc.P(bx, y)],
                                     kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "waist"), fc.Notch("armhole", 0.5, "front notch")],
        grainline=fc.Grainline(fc.P(x_bust * 0.3, hem_allowance + 30.0),
                               fc.P(x_bust * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Fitted front (full button front, waist dart, flared skirt)",
    )


def build_back():
    x_hem = HEM_Q
    x_waist = WAIST_Q + SIDE_TAKE
    x_bust = CHEST_Q
    x_shoulder = HALF_SHOULDER
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_hem, 0.0)
    p_shoulder_tip = fc.P(x_shoulder, SHOULDER_Y)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y)
    p_neck_cb = fc.P(0.0, SHOULDER_Y - BACK_NECK_DROP)
    side = _fitted_side(0.0, WAIST_Y, UNDERARM_Y, x_hem, x_waist, x_bust)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", side),
        fc.Edge("armhole", [_armscye(x_bust, UNDERARM_Y, x_shoulder, SHOULDER_Y, False)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.55, SHOULDER_Y - 3.0),
                                   fc.P(NECK_HALF * 0.25, p_neck_cb.y + 3.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    internals = [
        fc.Internal("waist-dart",
                    [fc.P(x_bust * 0.55, WAIST_Y - 110.0),
                     fc.P(x_bust * 0.55 - DART_TAKE * 0.5, WAIST_Y),
                     fc.P(x_bust * 0.55, WAIST_Y + 130.0)], kind="dart"),
        fc.Internal("centre-vent", [fc.P(6.0, 30.0), fc.P(6.0, back_vent)], kind="marking"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "waist"), fc.Notch("cb", back_vent / SHOULDER_Y, "vent")],
        grainline=fc.Grainline(fc.P(x_bust * 0.3, hem_allowance + 30.0),
                               fc.P(x_bust * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Fitted back (waist dart, flared skirt, centre vent), cut on fold",
    )


# ── Measure armscyes + neckline ──────────────────────────────────────────────
_FRONT = build_front()
_BACK = build_back()
FRONT_SCYE = _FRONT.edge("armhole").length(0.2)
BACK_SCYE = _BACK.edge("armhole").length(0.2)
ARMSCYE = FRONT_SCYE + BACK_SCYE
CAP_EASE = 20.0            # a tailored cap takes real ease
CAP_TARGET = ARMSCYE + CAP_EASE
FRONT_NECK = _FRONT.edge("neck").length(0.2)
BACK_NECK = _BACK.edge("neck").length(0.2)
NECK_RUN = 2.0 * FRONT_NECK + 2.0 * BACK_NECK
NECK_NAIVE = neck_girth + 26.0


def _cap_curve(x_right, x_left, y_base, cap_height):
    span = x_right - x_left
    return fc.Bezier(
        fc.P(x_right, y_base),
        fc.P(x_right - span * 0.14, y_base + cap_height * 1.32),
        fc.P(x_left + span * 0.14, y_base + cap_height * 1.32),
        fc.P(x_left, y_base))


def build_sleeve():
    cuff_open = wrist_girth + 60.0
    cap_height = armhole_depth * 0.58
    y_cap = cap_height
    cap_span = CAP_TARGET * 0.72
    for _ in range(8):
        xr = cap_span / 2.0
        got = fc.Edge("probe", [_cap_curve(xr, -xr, 0.0, cap_height)]).length(0.2)
        if got <= 1e-6:
            break
        cap_span *= CAP_TARGET / got
    total_w = cap_span
    cuff_open = min(cuff_open, total_w * 0.9)
    p_bl = fc.P((total_w - cuff_open) / 2.0, -sleeve_length)
    p_br = fc.P((total_w + cuff_open) / 2.0, -sleeve_length)
    p_cap_r = fc.P(total_w, y_cap)
    p_cap_l = fc.P(0.0, y_cap)
    edges = [
        fc.Edge("cuff_edge", [fc.Line(p_bl, p_br)]),
        fc.Edge("under_r", [fc.Line(p_br, p_cap_r)]),
        fc.Edge("cap", [_cap_curve(total_w, 0.0, y_cap, cap_height)]),
        fc.Edge("under_l", [fc.Line(p_cap_l, p_bl)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff_edge": hem_allowance * 0.5},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(total_w / 2.0, y_cap),
                               fc.P(total_w / 2.0, -sleeve_length + 20.0)),
        internals=[fc.Internal("cap-notch",
                               [fc.P(total_w / 2.0, y_cap + cap_height * 0.9),
                                fc.P(total_w / 2.0, y_cap + cap_height * 0.9 - 12.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Long sleeve (cap measured to the armscye)",
    )


def build_collar():
    ln = NECK_RUN
    h = collar_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", FRONT_NECK / ln, "left shoulder"),
                 fc.Notch("neck_edge", (FRONT_NECK + BACK_NECK) / ln, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, collar_height + 2.0),
                                        fc.P(ln, collar_height + 2.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Bandhgala stand collar (cut to the measured neckline)",
    )


def build():
    pattern = fc.PatternSet("nehru-sherwani")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_FRONT)
    if everything or target_piece == "back":
        pattern.add(_BACK)
    sleeve = build_sleeve()
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    cap_measured = sleeve.edge("cap").length(0.2)
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=2.0, ease=CAP_EASE)
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    pattern.bom = [
        {"item": "brocade silk, wool-silk, or fine cotton (sherwani shell)", "qty": round(
            (sherwani_length + sleeve_length + hem_allowance) * 2.6 / 10.0) * 10,
         "unit": "mm_length", "note": "the tailored coat; usually fully lined and often "
                 "underlined/canvassed through the chest for a firm front."},
        {"item": "shank buttons (front)", "qty": button_count, "unit": "count",
         "note": f"{button_diameter:.0f} mm shank buttons up the full front; the Yantra4D "
                 f"shank-button-solid, linked. Metal or self-covered are traditional."},
        {"item": "collar & chest canvas", "qty": round(NECK_RUN + 600.0), "unit": "mm_length",
         "note": "the bandhgala stand and the coat front are interfaced/canvassed."},
        {"item": "lining", "qty": 1, "unit": "coat", "note": "the sherwani is fully lined."},
    ]
    pattern.metadata = {
        "fc500_rank": 492,
        "family": "heritage_global",
        "fabric_hint": "brocado-seda",
        "made_to_measure": True,
        "finished_mm": {
            "chest_girth": round(chest_girth, 1),
            "waist_girth": round(waist_girth, 1),
            "sherwani_length": round(sherwani_length, 1),
            "collar_height": round(collar_height, 1),
        },
        "solved": {
            "chest_quarter_mm": round(CHEST_Q, 2),
            "waist_quarter_mm": round(WAIST_Q, 2),
            "hip_quarter_mm": round(HIP_Q, 2),
            "hem_quarter_mm": round(HEM_Q, 2),
            "waist_suppression_mm": round(WAIST_SUPP, 2),
            "side_take_mm": round(SIDE_TAKE, 2),
            "dart_take_mm": round(DART_TAKE, 2),
            "armscye_total_mm": round(ARMSCYE, 3),
            "sleeve_cap_target_mm": round(CAP_TARGET, 3),
            "sleeve_cap_measured_mm": round(cap_measured, 3),
            "collar_run_mm": round(NECK_RUN, 3),
            "collar_vs_neck_estimate_mm": round(NECK_RUN - NECK_NAIVE, 3),
            "back_vent_mm": round(back_vent, 2),
            "note": "the sherwani is a TAILORED, made-to-measure coat: the waist is solved "
                    "from the chest-waist-hip measures and suppressed with a side take-in plus "
                    "a vertical dart, and the skirt flares below the hip. The set-in sleeve cap "
                    "is SOLVED to the measured armscye plus a real tailored ease. The bandhgala "
                    "stand collar is cut to the MEASURED neckline (both fronts + both backs), "
                    "off the naive estimate by collar_vs_neck_estimate_mm.",
        },
        "heritage": {
            "garment": "sherwani (bandhgala) — the South Asian men's formal coat",
            "worn": "over a kurta and churidar or straight trouser; men's ceremonial dress at "
                    "weddings and state occasions across India, Pakistan and Bangladesh",
            "construction": "fitted, canvassed coat with a full shank-button front, bandhgala "
                            "stand collar, set-in sleeves, flared skirt and a centre back vent",
            "excluded": "no zardozi or thread-embroidery motif is drawn — the surface work is "
                        "the karigar's (the embroiderer's), not a pattern generator's",
        },
        "hardware": "full front shank buttons: Yantra4D shank-button-solid, linked, driven by "
                    "the button diameter.",
    }
    return pattern


result = build()

"""
Kebaya lace blouse — Fashion Cabinet Heritage Cartridge (FC-500 #490, heritage_global;
Indonesia, Malaysia, and the wider Nusantara).

The kebaya is the fitted front-opening blouse of Indonesia, Malaysia, Brunei, Singapore and
the Peranakan world — worn over a kemben or camisole with a batik or songket sarong, and made
in sheer embroidered voile, lace, or fine cotton. It is a fitted garment: bust and waist
shaping give the close body, the front opens edge-to-edge (or with the small kutubaru insert
panel), and it is held not by a buttoned placket but by a set of hooks or the linked brooches
(kerongsang) that are its signature jewellery.

Two facts govern the draft:

  1. THE BODY IS FITTED, THROUGH THE BUST AND WAIST. A bust dart and a waist take-in give the
     kebaya its close fit; the waist is SOLVED from the bust-waist-hip girths, not guessed. The
     front opening runs straight down centre front and curves away below the waist (the
     rounded or pointed kebaya front).

  2. THE SLEEVE IS SET IN, TO THE MEASURED ARMSCYE. The long fitted sleeve's cap is solved to
     the MEASURED front + back armhole, so it hangs cleanly; the declared seam proves it.

Pieces:
  - front  : the fitted front (cut 2), bust dart, curved-away front opening.
  - back   : the fitted back (cut on fold), waist shaping.
  - sleeve : the long sleeve, cap MEASURED to the armscye, cut 2.

Hardware: front hooks — Yantra4D hook-and-eye, LINKED (kerongsang brooches traditional).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|set

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
waist_girth = float(PARAM(lambda: waist_girth, 740.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
kebaya_length = float(PARAM(lambda: kebaya_length, 620.0))   # nape to point
neck_girth = float(PARAM(lambda: neck_girth, 360.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 380.0))  # tip to tip
armhole_depth = float(PARAM(lambda: armhole_depth, 210.0))
bust_to_waist = float(PARAM(lambda: bust_to_waist, 300.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 560.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 200.0))
front_point = float(PARAM(lambda: front_point, 120.0))      # how far the front curves below waist
bust_ease = float(PARAM(lambda: bust_ease, 70.0))
closure_span = float(PARAM(lambda: closure_span, 20.0))
closure_count = int(PARAM(lambda: closure_count, 5))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(740.0, min(bust_girth, 1150.0))
waist_girth = max(560.0, min(waist_girth, 1020.0))
hip_girth = max(800.0, min(hip_girth, 1250.0))
kebaya_length = max(520.0, min(kebaya_length, 780.0))
neck_girth = max(300.0, min(neck_girth, 440.0))
shoulder_width = max(320.0, min(shoulder_width, 460.0))
armhole_depth = max(180.0, min(armhole_depth, 280.0))
bust_to_waist = max(260.0, min(bust_to_waist, 400.0))
sleeve_length = max(420.0, min(sleeve_length, 660.0))
wrist_girth = max(160.0, min(wrist_girth, 260.0))
front_point = max(40.0, min(front_point, 260.0))
bust_ease = max(30.0, min(bust_ease, 140.0))
closure_span = max(12.0, min(closure_span, 36.0))
closure_count = max(3, min(closure_count, 8))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 40.0))

# ── Fit solve ────────────────────────────────────────────────────────────────
BUST_Q = (bust_girth + bust_ease) / 4.0
WAIST_Q = (waist_girth + bust_ease * 0.5) / 4.0
HIP_Q = (hip_girth + bust_ease * 0.7) / 4.0
WAIST_SUPP = max(BUST_Q - WAIST_Q, 0.0)
SIDE_TAKE = WAIST_SUPP * 0.5
DART_TAKE = WAIST_SUPP - SIDE_TAKE
HALF_SHOULDER = shoulder_width / 2.0
NECK_HALF = (neck_girth + 24.0) / 4.0
NECK_HALF = min(NECK_HALF, HALF_SHOULDER - 30.0)
FRONT_NECK_DROP = min(NECK_HALF * 0.9 + 20.0, armhole_depth * 0.7)
BACK_NECK_DROP = 20.0
armhole_depth = min(armhole_depth, bust_to_waist - 30.0)
SHOULDER_Y = kebaya_length
WAIST_Y = kebaya_length - bust_to_waist
UNDERARM_Y = kebaya_length - armhole_depth
# The front hangs LOWER at centre front, forming the kebaya point. The side hem sits level
# with the back hem (y = 0), and the CF point drops BELOW it by front_point (negative y), so
# the front and back side seams are the same length and balance.
FRONT_POINT_Y = -front_point              # CF point drops below the level side hem


def _armscye(x_side, y_underarm, x_shoulder, y_shoulder, front):
    bias = 0.42 if front else 0.30
    run = x_side - x_shoulder
    rise = y_shoulder - y_underarm
    return fc.Bezier(
        fc.P(x_side, y_underarm),
        fc.P(x_side - run * 0.10, y_underarm + rise * 0.42),
        fc.P(x_shoulder + run * bias, y_shoulder - rise * 0.12),
        fc.P(x_shoulder, y_shoulder))


def _fitted_side(y_hem, y_waist, y_underarm, x_hip, x_waist, x_bust):
    return [
        fc.Bezier(fc.P(x_hip, y_hem),
                  fc.P(x_hip, y_hem + (y_waist - y_hem) * 0.45),
                  fc.P(x_waist, y_waist - (y_waist - y_hem) * 0.20),
                  fc.P(x_waist, y_waist)),
        fc.Bezier(fc.P(x_waist, y_waist),
                  fc.P(x_waist, y_waist + (y_underarm - y_waist) * 0.30),
                  fc.P(x_bust, y_underarm - (y_underarm - y_waist) * 0.35),
                  fc.P(x_bust, y_underarm)),
    ]


def build_front():
    """The fitted FRONT (cut 2): bust dart, curved-away front opening ending in a point at CF."""
    x_hip = HIP_Q
    x_waist = WAIST_Q + SIDE_TAKE
    x_bust = BUST_Q
    x_shoulder = HALF_SHOULDER
    # the CF point drops below the level side hem (y = 0).
    p_point_cf = fc.P(0.0, FRONT_POINT_Y)
    p_hem_side = fc.P(x_hip, 0.0)
    p_shoulder_tip = fc.P(x_shoulder, SHOULDER_Y)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y)
    p_neck_cf = fc.P(0.0, SHOULDER_Y - FRONT_NECK_DROP)
    side = _fitted_side(0.0, WAIST_Y, UNDERARM_Y, x_hip, x_waist, x_bust)
    edges = [
        # the curved-away front hem: from the CF point up and out to the level side hem.
        fc.Edge("front_hem", [fc.Bezier(p_point_cf,
                                        fc.P(x_hip * 0.4, FRONT_POINT_Y * 0.55),
                                        fc.P(x_hip * 0.75, FRONT_POINT_Y * 0.15),
                                        p_hem_side)]),
        fc.Edge("side", side),
        fc.Edge("armhole", [_armscye(x_bust, UNDERARM_Y, x_shoulder, SHOULDER_Y, True)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.6, SHOULDER_Y - 6.0),
                                   fc.P(NECK_HALF * 0.28, p_neck_cf.y + 10.0),
                                   p_neck_cf)]),
        # the centre-front opening edge, from the neck down to the point.
        fc.Edge("cf", [fc.Line(p_neck_cf, p_point_cf)]),
    ]
    internals = [
        fc.Internal("bust-dart",
                    [fc.P(x_bust - 20.0, WAIST_Y + 10.0),
                     fc.P(x_bust * 0.62, UNDERARM_Y - 30.0),
                     fc.P(x_bust - 20.0, WAIST_Y - 40.0)], kind="dart"),
    ]
    span = (SHOULDER_Y - FRONT_NECK_DROP) - WAIST_Y
    span = max(span, 60.0)
    for i in range(closure_count):
        t = (i + 0.5) / closure_count
        y = WAIST_Y + span * t
        internals.append(fc.Internal(f"hook-{i + 1}",
                                     [fc.P(6.0, y), fc.P(6.0 + closure_span, y)],
                                     kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"front_hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "waist"),
                 fc.Notch("armhole", 0.5, "front notch")],
        grainline=fc.Grainline(fc.P(x_bust * 0.3, 30.0),
                               fc.P(x_bust * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Fitted front (bust dart, curved-away opening)",
    )


def build_back():
    """The fitted BACK (cut on fold): waist shaping, straight hem."""
    x_hip = HIP_Q
    x_waist = WAIST_Q + SIDE_TAKE
    x_bust = BUST_Q
    x_shoulder = HALF_SHOULDER
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_hip, 0.0)
    p_shoulder_tip = fc.P(x_shoulder, SHOULDER_Y)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y)
    p_neck_cb = fc.P(0.0, SHOULDER_Y - BACK_NECK_DROP)
    side = _fitted_side(0.0, WAIST_Y, UNDERARM_Y, x_hip, x_waist, x_bust)
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
                    [fc.P(x_bust * 0.55, WAIST_Y - 90.0),
                     fc.P(x_bust * 0.55 - DART_TAKE * 0.5, WAIST_Y),
                     fc.P(x_bust * 0.55, WAIST_Y + 90.0)], kind="dart"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "waist")],
        grainline=fc.Grainline(fc.P(x_bust * 0.3, hem_allowance + 20.0),
                               fc.P(x_bust * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Fitted back (waist shaping), cut on fold",
    )


# ── Measure the armscyes for the sleeve cap ──────────────────────────────────
_FRONT = build_front()
_BACK = build_back()
FRONT_SCYE = _FRONT.edge("armhole").length(0.2)
BACK_SCYE = _BACK.edge("armhole").length(0.2)
ARMSCYE = FRONT_SCYE + BACK_SCYE
CAP_EASE = 14.0
CAP_TARGET = ARMSCYE + CAP_EASE


def _cap_curve(x_right, x_left, y_base, cap_height):
    span = x_right - x_left
    return fc.Bezier(
        fc.P(x_right, y_base),
        fc.P(x_right - span * 0.14, y_base + cap_height * 1.32),
        fc.P(x_left + span * 0.14, y_base + cap_height * 1.32),
        fc.P(x_left, y_base))


def build_sleeve():
    """The long fitted sleeve: cap solved to the MEASURED armscye, tapering to the wrist."""
    cuff_open = wrist_girth + 30.0
    cap_height = armhole_depth * 0.56
    y_cap = cap_height
    cap_span = CAP_TARGET * 0.72
    for _ in range(8):
        xr = cap_span / 2.0
        xl = -cap_span / 2.0
        got = fc.Edge("probe", [_cap_curve(xr, xl, 0.0, cap_height)]).length(0.2)
        if got <= 1e-6:
            break
        cap_span *= CAP_TARGET / got
    cap_span = max(cap_span, cuff_open * 1.02)
    total_w = cap_span
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
    internals = [
        fc.Internal("cap-notch", [fc.P(total_w / 2.0, y_cap + cap_height * 0.9),
                                  fc.P(total_w / 2.0, y_cap + cap_height * 0.9 - 12.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff_edge": hem_allowance * 0.5},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(total_w / 2.0, y_cap),
                               fc.P(total_w / 2.0, -sleeve_length + 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Long sleeve (cap measured to the armscye)",
    )


def build():
    pattern = fc.PatternSet("kebaya-lace-blouse")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_FRONT)
    if everything or target_piece == "back":
        pattern.add(_BACK)
    sleeve = build_sleeve()
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)

    cap_measured = sleeve.edge("cap").length(0.2)
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # THE seam that solves: the sleeve cap against the MEASURED armscye.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=2.0, ease=CAP_EASE)

    pattern.bom = [
        {"item": "embroidered voile, lace, or fine cotton", "qty": round(
            (kebaya_length + sleeve_length) * 1.8 / 10.0) * 10, "unit": "mm_length",
         "note": "sheer, worn over a kemben or camisole with a batik or songket sarong. "
                 "Lace and embroidery are the maker's; none is drafted."},
        {"item": "front hook-and-eye sets", "qty": closure_count, "unit": "count",
         "note": f"{closure_span:.0f} mm hook-and-eye up the centre front; the Yantra4D "
                 f"hook-and-eye solid, linked. Kerongsang brooches are the traditional "
                 f"alternative — those are jewellery, not drafted here."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 490,
        "family": "heritage_global",
        "fabric_hint": "encaje-elastico",
        "finished_mm": {
            "bust_girth": round(bust_girth, 1),
            "waist_girth": round(waist_girth, 1),
            "kebaya_length": round(kebaya_length, 1),
            "front_point": round(front_point, 1),
        },
        "solved": {
            "bust_quarter_mm": round(BUST_Q, 2),
            "waist_quarter_mm": round(WAIST_Q, 2),
            "waist_suppression_mm": round(WAIST_SUPP, 2),
            "side_take_mm": round(SIDE_TAKE, 2),
            "dart_take_mm": round(DART_TAKE, 2),
            "front_scye_mm": round(FRONT_SCYE, 3),
            "back_scye_mm": round(BACK_SCYE, 3),
            "armscye_total_mm": round(ARMSCYE, 3),
            "sleeve_cap_target_mm": round(CAP_TARGET, 3),
            "sleeve_cap_measured_mm": round(cap_measured, 3),
            "note": "the kebaya is FITTED: the waist is solved from the three girths and "
                    "suppressed with a side take-in plus a bust/waist dart. The long sleeve "
                    "cap is SOLVED to the MEASURED armscye (front + back) plus ease — the "
                    "cap width is iterated until the drawn cap curve hits the target, and the "
                    "declared seam proves it. The front opens straight and curves away to a "
                    "point below the waist; it is held by hooks or kerongsang, not a placket.",
        },
        "heritage": {
            "garment": "kebaya — the fitted front-opening blouse of the Nusantara",
            "worn": "over a kemben/camisole with a batik or songket sarong; across Indonesia, "
                    "Malaysia, Brunei, Singapore and the Peranakan world",
            "construction": "fitted body with bust/waist shaping, set-in sleeve, curved-away "
                            "front opening, hook or kerongsang closure",
            "excluded": "no lace pattern or embroidery motif is drawn — those are the maker's",
        },
        "hardware": "front hook-and-eye: Yantra4D hook-and-eye, linked, sized from the closure "
                    "span; kerongsang brooches are the traditional alternative.",
    }
    return pattern


result = build()

"""
Barong Tagalog — Fashion Cabinet Heritage Cartridge (FC-500 #486, heritage_global;
Philippines; piña / jusi).

The barong tagalog is the Philippine formal shirt: a sheer, untucked, straight-cut shirt of
piña (pineapple-leaf fibre) or jusi (banana/abacá-silk), worn open at the hem over a plain
undershirt (camisa de chino), with a worked embroidered chest panel (the **pechera**), a
front button placket, a band collar, long sleeves with cuffs, and side slits. It is the
national formal dress of Filipino men and the ancestor of the everyday polo barong.

Two facts the draft solves honestly:

  1. THE SLEEVE CAP IS CUT TO THE MEASURED ARMSCYE. A set-in sleeve only hangs cleanly if the
     sleeve-cap seam equals the armhole it sews into. So the front and back armholes are
     drafted and MEASURED, and the sleeve cap is drawn to that measured length (plus a little
     ease), not recomputed from a formula and hoped to agree. The declared seam proves it.

  2. THE BARONG IS SHEER AND UNTUCKED, SO THE FINISH IS THE GARMENT. The placket, the band
     collar and the pechera are the worked zones; the hem is straight and open at the sides
     (the side slits). The embroidered pechera is a MARKED field, not drawn decoration —
     what fills it is the embroiderer's (calado, sombrado, hand embroidery).

Pieces:
  - front  : shirt front (cut 2), with the button placket and the pechera field.
  - back   : shirt back (cut on fold), with a shallow yoke line marked.
  - sleeve : long sleeve, cap MEASURED to the armscye, cut 2.
  - cuff   : the sleeve cuff, cut to the wrist opening, cut 2.
  - collar : the band collar, cut to the MEASURED neckline.

Hardware: front-placket buttons — Yantra4D sew-through-button, LINKED, sized in lignes.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|cuff|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
shirt_length = float(PARAM(lambda: shirt_length, 760.0))   # nape to hem
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))  # full shoulder tip to tip
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))   # shoulder to wrist
armhole_depth = float(PARAM(lambda: armhole_depth, 250.0))   # shoulder to underarm
wrist_girth = float(PARAM(lambda: wrist_girth, 190.0))
cuff_height = float(PARAM(lambda: cuff_height, 65.0))
collar_height = float(PARAM(lambda: collar_height, 38.0))
pechera_width = float(PARAM(lambda: pechera_width, 300.0))   # embroidered chest field width
side_slit = float(PARAM(lambda: side_slit, 130.0))
ease = float(PARAM(lambda: ease, 140.0))
button_ligne = float(PARAM(lambda: button_ligne, 18.0))
button_count = int(PARAM(lambda: button_count, 6))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1300.0))
shirt_length = max(650.0, min(shirt_length, 900.0))
neck_girth = max(340.0, min(neck_girth, 480.0))
shoulder_width = max(380.0, min(shoulder_width, 540.0))
sleeve_length = max(500.0, min(sleeve_length, 720.0))
armhole_depth = max(210.0, min(armhole_depth, 310.0))
wrist_girth = max(160.0, min(wrist_girth, 240.0))
cuff_height = max(45.0, min(cuff_height, 90.0))
collar_height = max(28.0, min(collar_height, 52.0))
pechera_width = max(200.0, min(pechera_width, 420.0))
side_slit = max(40.0, min(side_slit, 240.0))
ease = max(80.0, min(ease, 240.0))
button_ligne = max(12.0, min(button_ligne, 30.0))
button_count = max(4, min(button_count, 9))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 40.0))

# ── Derived body geometry ────────────────────────────────────────────────────
CHEST_Q = (chest_girth + ease) / 4.0            # quarter chest with ease
HALF_SHOULDER = shoulder_width / 2.0
NECK_HALF = (neck_girth + 30.0) / 4.0           # neckline half-width at shoulder line
FRONT_NECK_DROP = NECK_HALF * 0.75 + 20.0
BACK_NECK_DROP = 24.0
# The pechera field cannot exceed twice the front chest quarter (it must fit on the two
# fronts across the placket), and its depth is a fraction of the shirt above the waist.
PECHERA_HALF = min(pechera_width / 2.0, CHEST_Q - 30.0)
PECHERA_DEPTH = min(shirt_length * 0.5, armhole_depth + 120.0)
# Side slit capped below the hem-to-underarm run.
side_slit = min(side_slit, (shirt_length - armhole_depth) * 0.7)


def _armscye(x_side, y_underarm, x_shoulder, y_shoulder, front):
    """The armhole from the underarm (side, lower) up to the shoulder tip (upper).
    Front scyes are scooped deeper than back; the flag biases the control points."""
    bias = 0.42 if front else 0.30
    run = x_side - x_shoulder
    rise = y_shoulder - y_underarm
    return fc.Bezier(
        fc.P(x_side, y_underarm),
        fc.P(x_side - run * 0.10, y_underarm + rise * 0.42),
        fc.P(x_shoulder + run * bias, y_shoulder - rise * 0.12),
        fc.P(x_shoulder, y_shoulder))


def build_front():
    """One shirt front (cut 2): straight body, set-in armscye, front placket edge, pechera
    field. x = 0 is centre front; x = CHEST_Q is the side."""
    top = shirt_length
    x_side = CHEST_Q
    x_shoulder = HALF_SHOULDER
    y_underarm = top - armhole_depth
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side, 0.0)
    p_underarm = fc.P(x_side, y_underarm)
    p_shoulder_tip = fc.P(x_shoulder, top)
    p_neck_shoulder = fc.P(NECK_HALF, top)
    p_neck_cf = fc.P(0.0, top - FRONT_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [_armscye(x_side, y_underarm, x_shoulder, top, True)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.6, top - 6.0),
                                   fc.P(NECK_HALF * 0.28, p_neck_cf.y + 10.0),
                                   p_neck_cf)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("placket", [fc.P(14.0, top - FRONT_NECK_DROP), fc.P(14.0, 30.0)],
                    kind="marking"),
        fc.Internal("pechera-field",
                    [fc.P(18.0, top - FRONT_NECK_DROP - 20.0),
                     fc.P(min(PECHERA_HALF, x_side - 10.0), top - FRONT_NECK_DROP - 20.0),
                     fc.P(min(PECHERA_HALF, x_side - 10.0),
                          top - FRONT_NECK_DROP - 20.0 - PECHERA_DEPTH),
                     fc.P(18.0, top - FRONT_NECK_DROP - 20.0 - PECHERA_DEPTH)],
                    kind="marking"),
        fc.Internal("slit-head", [fc.P(x_side, side_slit), fc.P(x_side - 24.0, side_slit)],
                    kind="marking"),
    ]
    span = (top - FRONT_NECK_DROP) - 60.0
    for i in range(button_count):
        t = (i + 0.5) / button_count
        y = 60.0 + span * t
        internals.append(fc.Internal(f"button-{i + 1}",
                                     [fc.P(14.0, y), fc.P(14.0 + button_ligne * 0.635, y)],
                                     kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", side_slit / max(y_underarm, 1.0), "slit head"),
                 fc.Notch("armhole", 0.5, "front notch (single)")],
        grainline=fc.Grainline(fc.P(x_side * 0.3, hem_allowance + 30.0),
                               fc.P(x_side * 0.3, y_underarm - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shirt front (placket + pechera)",
    )


def build_back():
    """The shirt back (cut on fold at CB): straight body, set-in armscye, shallow yoke line."""
    top = shirt_length
    x_side = CHEST_Q
    x_shoulder = HALF_SHOULDER
    y_underarm = top - armhole_depth
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side, 0.0)
    p_underarm = fc.P(x_side, y_underarm)
    p_shoulder_tip = fc.P(x_shoulder, top)
    p_neck_shoulder = fc.P(NECK_HALF, top)
    p_neck_cb = fc.P(0.0, top - BACK_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [_armscye(x_side, y_underarm, x_shoulder, top, False)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_tip, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.55, top - 3.0),
                                   fc.P(NECK_HALF * 0.25, p_neck_cb.y + 3.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    internals = [
        fc.Internal("yoke-line", [fc.P(0.0, top - 90.0), fc.P(x_side, top - 90.0)],
                    kind="marking"),
        fc.Internal("slit-head", [fc.P(x_side, side_slit), fc.P(x_side - 24.0, side_slit)],
                    kind="marking"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", side_slit / max(y_underarm, 1.0), "slit head")],
        grainline=fc.Grainline(fc.P(x_side * 0.3, hem_allowance + 30.0),
                               fc.P(x_side * 0.3, y_underarm - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Shirt back (cut on fold)",
    )


# ── Measure the armscyes for the sleeve cap ──────────────────────────────────
_FRONT = build_front()
_BACK = build_back()
FRONT_SCYE = _FRONT.edge("armhole").length(0.2)
BACK_SCYE = _BACK.edge("armhole").length(0.2)
ARMSCYE = FRONT_SCYE + BACK_SCYE                 # the whole armhole one sleeve sews into
SLEEVE_CAP_EASE = 12.0                           # a shirt takes little cap ease
CAP_TARGET = ARMSCYE + SLEEVE_CAP_EASE
FRONT_NECK = _FRONT.edge("neck").length(0.2)
BACK_NECK = _BACK.edge("neck").length(0.2)
NECK_RUN = 2.0 * FRONT_NECK + 2.0 * BACK_NECK    # both fronts + both back quarters


def _cap_curve(x_right, x_left, y_base, cap_height):
    """The sleeve-cap ogee AS DRAWN, from the right cap point down over to the left cap point.
    A symmetric S-curve rising `cap_height` above the base line. The single curve used both to
    solve the width and to draw the edge, so the measured length is exactly the target."""
    span = x_right - x_left
    return fc.Bezier(
        fc.P(x_right, y_base),
        fc.P(x_right - span * 0.14, y_base + cap_height * 1.32),
        fc.P(x_left + span * 0.14, y_base + cap_height * 1.32),
        fc.P(x_left, y_base))


def build_sleeve():
    """The long sleeve: a cap whose seam MEASURES to the armscye, tapering to the wrist.

    The cap height is set; the cap width is SOLVED by iterating until the drawn cap curve's
    length equals CAP_TARGET. The same curve function draws the edge, so measured == target."""
    cuff_open = wrist_girth + 40.0               # the sleeve base above the cuff (with pleat)
    cap_height = armhole_depth * 0.55
    y_cap = cap_height
    # Iterate the cap span so the DRAWN cap curve length hits CAP_TARGET. The curve is centred
    # on the sleeve; we vary its span and measure the real edge each pass.
    cap_span = CAP_TARGET * 0.72                  # first estimate
    for _ in range(8):
        xr = cap_span / 2.0
        xl = -cap_span / 2.0
        got = fc.Edge("probe", [_cap_curve(xr, xl, 0.0, cap_height)]).length(0.2)
        if got <= 1e-6:
            break
        cap_span *= CAP_TARGET / got
    cap_span = max(cap_span, cuff_open * 1.02)   # the cap must be at least as wide as the base
    total_w = cap_span
    x_left = 0.0
    x_right = total_w
    p_bl = fc.P((total_w - cuff_open) / 2.0, 0.0)
    p_br = fc.P((total_w + cuff_open) / 2.0, 0.0)
    p_cap_r = fc.P(x_right, y_cap)
    p_cap_l = fc.P(x_left, y_cap)
    edges = [
        fc.Edge("cuff_edge", [fc.Line(p_bl, p_br)]),
        fc.Edge("under_r", [fc.Line(p_br, p_cap_r)]),
        fc.Edge("cap", [_cap_curve(x_right, x_left, y_cap, cap_height)]),
        fc.Edge("under_l", [fc.Line(p_cap_l, p_bl)]),
    ]
    internals = [
        fc.Internal("cap-notch",
                    [fc.P(total_w / 2.0, y_cap + cap_height * 0.9),
                     fc.P(total_w / 2.0, y_cap + cap_height * 0.9 - 12.0)],
                    kind="marking"),
        fc.Internal("cuff-pleat", [fc.P(total_w * 0.62, 0.0), fc.P(total_w * 0.62, 30.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff_edge": 0.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("under_r", 0.5, "underarm")],
        grainline=fc.Grainline(fc.P(total_w / 2.0, y_cap + cap_height * 0.2),
                               fc.P(total_w / 2.0, 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Long sleeve (cap measured to the armscye)",
    )


def build_cuff():
    """The sleeve cuff: a band at the wrist girth plus overlap, cut to double cuff height."""
    ln = wrist_girth + 60.0
    h = cuff_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("wrist_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "cuff", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("wrist_edge", 0.5, "cuff centre")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, cuff_height + 2.0),
                                        fc.P(ln, cuff_height + 2.0)], kind="marking"),
                   fc.Internal("cuff-button", [fc.P(ln - button_ligne, h * 0.5),
                                               fc.P(ln - 8.0, h * 0.5)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Sleeve cuff",
    )


def build_collar():
    """The band collar, cut to the MEASURED neckline run."""
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
        notches=[fc.Notch("neck_edge", BACK_NECK / ln, "back quarter"),
                 fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, collar_height + 2.0),
                                        fc.P(ln, collar_height + 2.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Band collar (cut to the measured neckline)",
    )


def build():
    pattern = fc.PatternSet("barong-tagalog")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_FRONT)
    if everything or target_piece == "back":
        pattern.add(_BACK)
    sleeve = build_sleeve()
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    cap_measured = sleeve.edge("cap").length(0.2)
    if everything:
        # THE seam that had to solve: the sleeve cap against the MEASURED armscye (front +
        # back), with a little ease. Draft the cap from a formula instead and it puckers.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=2.0, ease=SLEEVE_CAP_EASE)
        # The side seam: front side to back side (both drawn to the same chest quarter).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        # The shoulder seam.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # The collar band against the whole measured neckline.
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    pattern.bom = [
        {"item": "piña, jusi, or piña-seda (sheer)", "qty": round(
            (shirt_length + hem_allowance) * 2.4 / 10.0) * 10, "unit": "mm_length",
         "note": "sheer pineapple-leaf or banana-silk cloth; the barong is worn untucked "
                 "over a plain camisa de chino."},
        {"item": "front-placket buttons", "qty": button_count, "unit": "count",
         "note": f"{button_ligne:.0f}-ligne buttons; the Yantra4D sew-through-button, linked. "
                 f"Mother-of-pearl or shell buttons are traditional."},
        {"item": "collar & cuff interlining", "qty": round(NECK_RUN + wrist_girth * 2),
         "unit": "mm_length", "note": "the band collar and cuffs are interfaced."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 486,
        "family": "heritage_global",
        "fabric_hint": "organza-pina",
        "finished_mm": {
            "chest_girth": round(chest_girth, 1),
            "shirt_length": round(shirt_length, 1),
            "sleeve_length": round(sleeve_length, 1),
            "collar_height": round(collar_height, 1),
        },
        "solved": {
            "chest_quarter_mm": round(CHEST_Q, 2),
            "front_scye_mm": round(FRONT_SCYE, 3),
            "back_scye_mm": round(BACK_SCYE, 3),
            "armscye_total_mm": round(ARMSCYE, 3),
            "sleeve_cap_target_mm": round(CAP_TARGET, 3),
            "sleeve_cap_measured_mm": round(cap_measured, 3),
            "sleeve_cap_ease_mm": round(SLEEVE_CAP_EASE, 3),
            "front_neck_quarter_mm": round(FRONT_NECK, 3),
            "back_neck_quarter_mm": round(BACK_NECK, 3),
            "collar_run_mm": round(NECK_RUN, 3),
            "pechera_half_mm": round(PECHERA_HALF, 2),
            "side_slit_mm": round(side_slit, 2),
            "note": "the set-in sleeve cap is SOLVED to the MEASURED armscye (front + back) "
                    "plus a little ease, not recomputed from a formula and hoped to agree — "
                    "the cap width is iterated until the cap curve length hits the target, "
                    "and the declared seam proves it. The band collar is cut to the MEASURED "
                    "neckline (both fronts + both back quarters). The pechera is a MARKED "
                    "embroidery field, not drawn decoration.",
        },
        "heritage": {
            "garment": "barong tagalog — Philippine formal shirt (national formal dress)",
            "fabric": "piña (pineapple-leaf fibre), jusi (banana/abacá-silk), or piña-seda; "
                      "sheer, worn untucked over a camisa de chino",
            "construction": "straight cut, set-in sleeves with cuffs, band collar, front "
                            "button placket, embroidered pechera chest panel, side slits",
            "excluded": "no specific embroidery pattern (calado, sombrado, hand embroidery) "
                        "is drawn — the pechera is a marked field the embroiderer fills",
        },
        "hardware": "front-placket buttons: Yantra4D sew-through-button, linked, sized in "
                    "lignes (mother-of-pearl traditional).",
    }
    return pattern


result = build()

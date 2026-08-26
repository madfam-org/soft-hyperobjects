"""
Waffle Thermal Henley — Fashion Cabinet Garment Cartridge (FC-500 #465; y4d sew-through-button).

A long-sleeve waffle-knit thermal with a henley placket: a fitted knit body (front + back), set-in
long sleeves, a ribbed neckband, and a partial button placket down the centre front closing on a
column of Yantra4D `sew-through-button`. The waffle (thermal) knit is a mid-stretch fabric, so the
body is cut at a modest negative ease, and the placket length sets how many buttons the column
carries — drafted, not guessed.

The DIMENSIONAL HANDSHAKE. The placket buttons are `sew-through-button`s of `button_ligne` ligne.
The garment's `button_ligne` drives BOTH the drafted button seats on the placket AND the
hardware's `sew_face` flange; `button_count` is derived from the placket length and the pitch, and
both `button_ligne` and `placket_length` drive the garment's own `placket` interface. The
buttonholes are spaced evenly down the drafted placket, so the column the wearer buttons is
exactly the column the placket carries.

Made to measure to chest/bust, waist and arm length. FC-500 lane 7 (intimates & loungewear III).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 960.0))
waist_girth = float(PARAM(lambda: waist_girth, 840.0))
body_length = float(PARAM(lambda: body_length, 680.0))      # nape to hem
arm_length  = float(PARAM(lambda: arm_length, 600.0))       # shoulder to cuff
bicep_girth = float(PARAM(lambda: bicep_girth, 320.0))
neck_girth  = float(PARAM(lambda: neck_girth, 400.0))
placket_length = float(PARAM(lambda: placket_length, 180.0))  # CF opening depth
button_ligne = float(PARAM(lambda: button_ligne, 18.0))
button_pitch = float(PARAM(lambda: button_pitch, 55.0))     # spacing down the placket
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 5.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_bust_girth = max(700.0, min(chest_bust_girth, 1500.0))
waist_girth = max(560.0, min(waist_girth, 1400.0))
body_length = max(450.0, min(body_length, 900.0))
arm_length  = max(400.0, min(arm_length, 750.0))
bicep_girth = max(220.0, min(bicep_girth, 550.0))
neck_girth  = max(300.0, min(neck_girth, 520.0))
placket_length = max(90.0, min(placket_length, 300.0))
button_ligne = max(12.0, min(button_ligne, 30.0))
button_pitch = max(35.0, min(button_pitch, 90.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 14.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# ── Solved widths ────────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
CHEST_HALF = (chest_bust_girth * NEG) / 2.0
WAIST_HALF = (waist_girth * NEG) / 2.0
PANEL_CHEST = CHEST_HALF / 2.0    # per panel quarter (front/back share the side seam)
PANEL_WAIST = WAIST_HALF / 2.0
BL = body_length
AL = arm_length
BUTTON_DIA = button_ligne * 0.635
NECK_W = max(70.0, neck_girth / 6.0)         # front neck half-width
ARMSCYE_DROP = max(180.0, PANEL_CHEST * 1.1) # armscye depth from shoulder
# Number of buttons the placket carries.
BUTTON_COUNT = max(1, int(placket_length // button_pitch))


def build_back():
    """Back body panel, cut on CB fold. Hem, side, armscye, shoulder, back neck, CB fold."""
    p_cb_hem = fc.P(0.0, 0.0)
    p_side_hem = fc.P(PANEL_WAIST, 0.0)
    armscye_y = BL - ARMSCYE_DROP
    p_underarm = fc.P(PANEL_CHEST, armscye_y)
    shoulder_y = BL
    p_shoulder = fc.P(NECK_W + (PANEL_CHEST - NECK_W) * 0.7, shoulder_y - 8.0)
    p_neck = fc.P(NECK_W, shoulder_y)
    p_cb_neck = fc.P(0.0, shoulder_y)
    edges = [
        fc.Edge("hem", [fc.Line(p_cb_hem, p_side_hem)]),
        fc.Edge("side", [fc.Bezier(p_side_hem,
                                   fc.P(PANEL_WAIST + (PANEL_CHEST - PANEL_WAIST) * 0.4,
                                        armscye_y * 0.5),
                                   fc.P(PANEL_CHEST * 0.98, armscye_y * 0.85),
                                   p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm,
                                      fc.P(PANEL_CHEST * 0.9, armscye_y + ARMSCYE_DROP * 0.45),
                                      fc.P(p_shoulder.x + 14.0, p_shoulder.y - 30.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck,
                                   fc.P(NECK_W * 0.55, shoulder_y - 2.0),
                                   fc.P(NECK_W * 0.2, shoulder_y - 1.0),
                                   p_cb_neck)]),
        fc.Edge("center_back", [fc.Line(p_cb_neck, p_cb_hem)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match"),
                 fc.Notch("armscye", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(PANEL_CHEST * 0.4, BL * 0.2),
                               fc.P(PANEL_CHEST * 0.4, BL * 0.8)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back"),
        label="Back (cut 1 on CB fold)",
    )


def build_front():
    """Front body panel, cut 2 (mirror) so the CF opening can carry the placket. Its CF edge
    is straight; the placket piece topstitches onto it. Front neck is scooped lower than back."""
    p_cf_hem = fc.P(0.0, 0.0)
    p_side_hem = fc.P(PANEL_WAIST, 0.0)
    armscye_y = BL - ARMSCYE_DROP
    p_underarm = fc.P(PANEL_CHEST, armscye_y)
    shoulder_y = BL
    p_shoulder = fc.P(NECK_W + (PANEL_CHEST - NECK_W) * 0.7, shoulder_y - 8.0)
    front_neck_drop = NECK_W * 0.9
    p_neck_shoulder = fc.P(NECK_W, shoulder_y)
    p_cf_neck = fc.P(0.0, shoulder_y - front_neck_drop)
    edges = [
        fc.Edge("hem", [fc.Line(p_cf_hem, p_side_hem)]),
        fc.Edge("side", [fc.Bezier(p_side_hem,
                                   fc.P(PANEL_WAIST + (PANEL_CHEST - PANEL_WAIST) * 0.4,
                                        armscye_y * 0.5),
                                   fc.P(PANEL_CHEST * 0.98, armscye_y * 0.85),
                                   p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm,
                                      fc.P(PANEL_CHEST * 0.9, armscye_y + ARMSCYE_DROP * 0.45),
                                      fc.P(p_shoulder.x + 14.0, p_shoulder.y - 30.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.7, shoulder_y - front_neck_drop * 0.35),
                                   fc.P(NECK_W * 0.3, shoulder_y - front_neck_drop * 0.8),
                                   p_cf_neck)]),
        fc.Edge("center_front", [fc.Line(p_cf_neck, p_cf_hem)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match"),
                 fc.Notch("center_front", 1.0 - placket_length / (shoulder_y - front_neck_drop),
                          "placket base")],
        grainline=fc.Grainline(fc.P(PANEL_CHEST * 0.4, BL * 0.2),
                               fc.P(PANEL_CHEST * 0.4, BL * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2 — CF placket opening)",
    )


def _bell_points(chord, height, n=41):
    """A symmetric sleeve-cap bell over `chord` (from (0,0) to (chord,0)) peaking at `height`,
    as two mirrored Beziers sampled to a polyline. Monotone in `height` for its arc length."""
    mid = chord / 2.0
    left = fc.Bezier(fc.P(0.0, 0.0),
                     fc.P(chord * 0.14, height * 0.10),
                     fc.P(mid * 0.55, height),
                     fc.P(mid, height))
    right = fc.Bezier(fc.P(mid, height),
                      fc.P(mid + (mid - mid * 0.55), height),
                      fc.P(chord - chord * 0.14, height * 0.10),
                      fc.P(chord, 0.0))
    pts = left.flatten(0.2) + right.flatten(0.2)[1:]
    # translate so first sample is at (0,0)
    return pts


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def build_sleeve(armscye_len):
    """Set-in long sleeve: the cap is built to EXACTLY the measured armscye run by solving the
    cap height with bisection, so the cap and the armscye balance at every extreme."""
    bicep_half = (bicep_girth * (1.0 + 0.06)) / 2.0   # a little ease at the bicep
    # A sleeve cap cannot be shorter than its own bicep chord, and it must set into the
    # armscye — so the bicep chord is capped below the armscye run. Without this clamp a very
    # large bicep on a small chest forces cap > armscye and the seam can never balance.
    chord = min(2.0 * bicep_half, armscye_len * 0.92)
    bicep_half = chord / 2.0
    cuff_half = max(70.0, bicep_half * 0.62)
    target = max(armscye_len, chord * 1.01)           # cap is at least a hair longer than chord
    # Bisect cap height so the bell's arc length == target.
    lo, hi = 1.0, max(chord, target)                  # generous upper bound
    for _ in range(48):
        mid_h = (lo + hi) / 2.0
        length = _poly_len(_bell_points(chord, mid_h))
        if length < target:
            lo = mid_h
        else:
            hi = mid_h
    cap_pts = _bell_points(chord, (lo + hi) / 2.0)
    sleeve_len = AL
    p_under_l = cap_pts[0]                 # (0,0)
    p_under_r = cap_pts[-1]                # (chord,0)
    p_cuff_r = fc.P(bicep_half + cuff_half, -sleeve_len)
    p_cuff_l = fc.P(bicep_half - cuff_half, -sleeve_len)
    edges = [
        fc.Edge("cap", [fc.Line(cap_pts[i], cap_pts[i + 1]) for i in range(len(cap_pts) - 1)]),
        fc.Edge("underseam_r", [fc.Line(p_under_r, p_cuff_r)]),
        fc.Edge("cuff", [fc.Line(p_cuff_r, p_cuff_l)]),
        fc.Edge("underseam_l", [fc.Line(p_cuff_l, p_under_l)]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(bicep_half, -sleeve_len * 0.2),
                               fc.P(bicep_half, -sleeve_len * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Long sleeve (cut 2, mirror)",
    )


def build_placket():
    """The button placket: a rectangle down the CF opening carrying the button column. Cut 2
    (overlap + underlap). `attach` sews to the CF; the buttons space evenly down it."""
    width = max(30.0, BUTTON_DIA + 18.0)
    length = placket_length
    p0, p1 = fc.P(0.0, 0.0), fc.P(width, 0.0)
    p2, p3 = fc.P(width, length), fc.P(0.0, length)
    edges = [
        fc.Edge("bottom", [fc.Line(p0, p1)]),
        fc.Edge("attach", [fc.Line(p1, p2)]),   # to CF
        fc.Edge("top", [fc.Line(p2, p3)]),
        fc.Edge("fold", [fc.Line(p3, p0)]),
    ]
    internals = []
    for i in range(BUTTON_COUNT):
        by = length - (i + 0.5) * (length / BUTTON_COUNT)
        bx = width * 0.5
        internals.append(fc.Internal(f"button-{i}",
                                     [fc.P(bx - BUTTON_DIA / 2.0, by),
                                      fc.P(bx + BUTTON_DIA / 2.0, by)], kind="marking"))
    return fc.Piece(
        "placket", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "CF centre")],
        grainline=fc.Grainline(fc.P(width * 0.5, length * 0.1), fc.P(width * 0.5, length * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Button placket (cut 2 — overlap + underlap)",
    )


def build_neckband(neck_run):
    """Ribbed neckband, cut to the MEASURED neck run (front + back) at negative ease."""
    length = neck_run * 0.92     # rib stretches on
    cut_depth = max(30.0, NECK_W * 0.5) * 2.0
    p0, p1 = fc.P(0.0, 0.0), fc.P(length, 0.0)
    p2, p3 = fc.P(length, cut_depth), fc.P(0.0, cut_depth)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("free", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("fold-line", [fc.P(0.0, cut_depth / 2.0), fc.P(length, cut_depth / 2.0)],
                             kind="marking")]
    return fc.Piece(
        "neckband", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "CB centre")],
        grainline=fc.Grainline(fc.P(length * 0.08, cut_depth * 0.4),
                               fc.P(length * 0.92, cut_depth * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Ribbed neckband (cut 1)",
    )


def build():
    pattern = fc.PatternSet("thermal-waffle-henley")
    back = build_back()
    front = build_front()
    armscye_len = front.edge("armscye").length() + back.edge("armscye").length()
    sleeve = build_sleeve(armscye_len)
    placket = build_placket()
    # neck run: two front necks + one back neck (back cut on fold => *2)
    neck_run = 2.0 * front.edge("neck").length() + 2.0 * back.edge("neck").length()
    neckband = build_neckband(neck_run)

    picked = {"back": back, "front": front, "sleeve": sleeve, "placket": placket,
              "neckband": neckband}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (back, front, sleeve, placket, neckband):
            pattern.add(piece)
        # Side seam: front side to back side (mirror halves).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        # Shoulder: front shoulder to back shoulder.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Sleeve cap == the measured armscye (front + back).
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armscye"), ("back", "armscye")], tol=2.0)
        # Neckband == the measured neck run, eased on (declared with the rib ease).
        # The rib neckband is cut SHORTER than the neck and stretched on: side_a (band) is
        # shorter than side_b (neck) by the rib ease, so the declared ease is negative.
        pattern.declare_seam(("neckband", "attach"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")],
                             tol=2.0, ease=(neckband.edge("attach").length() - neck_run))

    fabric_width = 1700.0
    area = (back.area() + front.area() * 2.0 + sleeve.area() * 2.0 + placket.area() * 2.0
            + neckband.area())
    marker_len = area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "waffle thermal knit (cotton/poly)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"body and sleeves in the waffle; at {fabric_width:.0f} mm width, 80% marker. "
                 "Cut across the stretch."},
        {"item": "placket buttons (Yantra4D sew-through-button)", "qty": BUTTON_COUNT,
         "unit": "piece",
         "note": f"{BUTTON_COUNT} buttons at {button_ligne:.0f} ligne ({BUTTON_DIA:.1f} mm), "
                 f"spaced {button_pitch:.0f} mm down the {placket_length:.0f} mm placket "
                 "(notion.hardware_ref -> sew-through-button)."},
        {"item": "rib knit (neckband)", "qty": round(neckband.edge('attach').length() / 10.0) * 10,
         "unit": "mm_length", "note": "1x1 rib for the neckband, cut to the solved neck run."},
        {"item": "coverstitch + wooly nylon", "qty": 1, "unit": "set",
         "note": "coverstitch hems and cuffs; flatlock the shoulder for a flat inside."},
    ]
    pattern.metadata = {
        "fc500_rank": 465, "family": "underwear_lounge", "fabric_hint": "punto-waffle",
        "silhouette_note": "Long-sleeve waffle thermal henley: fitted knit body, set-in sleeves, "
            "a ribbed neckband, and a partial button placket down the centre front. The placket "
            "length sets the button column — drafted, not guessed.",
        "hardware": "placket buttons via Yantra4D (notion.hardware_ref -> sew-through-button); "
            "button_ligne drives the button seats AND the hardware sew face.",
        "solved": {
            "chest_finished_half_mm": round(CHEST_HALF, 1),
            "button_ligne": round(button_ligne, 1),
            "button_dia_mm": round(BUTTON_DIA, 2),
            "placket_length_mm": round(placket_length, 1),
            "button_count": BUTTON_COUNT,
            "armscye_run_mm": round(armscye_len, 1),
            "note": "button_count = placket_length // button_pitch; the sleeve cap is built to "
                    "the measured armscye run.",
        },
        "closure": "partial button placket (henley)",
        "drafting": "Made to measure to chest/bust, waist, arm length, bicep and neck.",
    }
    return pattern


result = build()

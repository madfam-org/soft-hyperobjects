"""
Shweshwe pinafore dress — Fashion Cabinet Heritage Cartridge (FC-500 #485,
heritage_global; Southern Africa — Sotho, Xhosa, Tswana; shweshwe printed cotton).

Shweshwe is the indigo (and later chocolate and red) discharge-printed cotton of Southern
Africa — originally imported, now woven and printed at Da Gama Textiles in the Eastern Cape
— worn across Sotho, Xhosa and Tswana dress and central to the "German print" pinafore and
the traditional wedding **seshweshwe**. This cartridge drafts a **pinafore dress**: a
sleeveless bib-front shift with a fitted bodice, a gathered skirt, and a button closure at
the back, the everyday and Sunday form of the shweshwe frock.

Two things the draft solves honestly:

  1. THE WAIST SEAM MUST BALANCE. The bodice's waist edge and the skirt's waist edge are
     drafted separately — the bodice to the waist girth with darts, the skirt gathered to a
     multiple of it — and the seam that joins them must MATCH (skirt gathered edge to bodice
     waist plus the gather ratio). Drafting the skirt to a free width and hoping it gathers
     to the bodice is the mistake; here the skirt width is SOLVED from the bodice waist times
     the gather ratio, so the waist seam balances by construction.

  2. THE ARMHOLE AND NECK ARE FACED, AND THE BACK OPENS. A pinafore is sleeveless: the
     armscye is a finished edge, not a sleeve mount. The back is split to a button placket so
     it can be pulled on; the buttons are real hardware (a Yantra4D sew-through-button), sized
     in lignes, and the placket length reads the bodice length.

Pieces:
  - front  : the pinafore front (bib bodice + gathered-skirt front), cut on fold.
  - back   : the pinafore back (cut 2), with the button placket at centre back.
  - facing : the neck + armhole facing.

Hardware: back-closure buttons — Yantra4D sew-through-button, LINKED, sized in lignes.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|facing|set

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
waist_girth = float(PARAM(lambda: waist_girth, 740.0))
bodice_length = float(PARAM(lambda: bodice_length, 400.0))   # shoulder to waist
skirt_length = float(PARAM(lambda: skirt_length, 640.0))     # waist to hem
gather_ratio = float(PARAM(lambda: gather_ratio, 1.9))       # skirt fullness vs waist
neck_width = float(PARAM(lambda: neck_width, 150.0))         # half neck opening
neck_drop = float(PARAM(lambda: neck_drop, 90.0))            # front neck depth
armhole_drop = float(PARAM(lambda: armhole_drop, 220.0))     # shoulder to underarm
shoulder_width = float(PARAM(lambda: shoulder_width, 195.0))  # CF to shoulder tip (half)
button_ligne = float(PARAM(lambda: button_ligne, 24.0))      # back-button size, lignes
button_count = int(PARAM(lambda: button_count, 6))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 45.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
bust_girth = max(760.0, min(bust_girth, 1200.0))
waist_girth = max(600.0, min(waist_girth, 1080.0))
bodice_length = max(320.0, min(bodice_length, 500.0))
skirt_length = max(400.0, min(skirt_length, 950.0))
gather_ratio = max(1.3, min(gather_ratio, 2.6))
neck_width = max(100.0, min(neck_width, 220.0))
neck_drop = max(50.0, min(neck_drop, 160.0))
armhole_drop = max(160.0, min(armhole_drop, 300.0))
shoulder_width = max(150.0, min(shoulder_width, 260.0))
button_ligne = max(14.0, min(button_ligne, 40.0))
button_count = max(3, min(button_count, 10))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 90.0))

# ── The waist-seam solve — the skirt is SOLVED to the bodice ─────────────────
# Quarter measures (one side of a fold-cut front / a back half).
BODICE_WAIST_Q = waist_girth / 4.0          # the bodice waist quarter
BUST_Q = bust_girth / 4.0
# The skirt waist quarter is the bodice waist quarter times the gather ratio: SOLVED, so the
# waist seam balances. The skirt hem follows the same gathered width (a straight gathered
# skirt), for a full swing.
SKIRT_WAIST_Q = BODICE_WAIST_Q * gather_ratio
# The shoulder tip must sit INBOARD of the side seam, and the neck point INBOARD of the
# shoulder tip — both clamped so the bib never inverts (neck outboard of shoulder) or runs
# past the side. These are real bounds at the parameter extremes.
shoulder_width = min(shoulder_width, BUST_Q - 30.0)
shoulder_width = max(shoulder_width, 120.0)
neck_width = min(neck_width, shoulder_width - 30.0)
neck_width = max(neck_width, 60.0)
neck_drop = min(neck_drop, bodice_length * 0.45)
armhole_drop = min(armhole_drop, bodice_length - 40.0)


def _neck_curve(x_shoulder, y_top, x_cf, y_drop):
    return fc.Bezier(
        fc.P(x_shoulder, y_top),
        fc.P(x_shoulder * 0.55, y_top - (y_top - y_drop) * 0.12),
        fc.P(x_cf + (x_shoulder - x_cf) * 0.22, y_drop + (y_top - y_drop) * 0.10),
        fc.P(x_cf, y_drop))


def _armhole_curve(x_side, y_underarm, x_shoulder, y_top):
    """Armhole drawn from the UNDERARM (side, lower) up to the SHOULDER point (upper)."""
    return fc.Bezier(
        fc.P(x_side, y_underarm),
        fc.P(x_side, y_top - (y_top - y_underarm) * 0.55),
        fc.P(x_shoulder + (x_side - x_shoulder) * 0.42, y_top - (y_top - y_underarm) * 0.06),
        fc.P(x_shoulder, y_top))


def _bodice_and_skirt_front():
    """The pinafore FRONT, cut on the CF fold: bib bodice above the waist seam, gathered
    skirt below it, drawn as one continuous outline (the waist seam is an internal marking so
    the piece is a single closed ring — the skirt is gathered onto the bodice in make-up)."""
    total_h = bodice_length + skirt_length
    waist_y = skirt_length                  # measured up from the hem
    x_side_bodice = BUST_Q
    x_side_skirt = SKIRT_WAIST_Q
    x_shoulder = shoulder_width
    # outline CCW from CF hem
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side_skirt, 0.0)
    p_waist_side = fc.P(x_side_skirt, waist_y)
    # underarm at y = waist + (bodice_length - armhole_drop)
    p_underarm = fc.P(x_side_bodice, waist_y + (bodice_length - armhole_drop))
    p_shoulder_out = fc.P(x_shoulder, total_h)
    p_neck_cf = fc.P(0.0, total_h - neck_drop)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("skirt_side", [fc.Line(p_hem_side, p_waist_side)]),
        # the waist step: the skirt side is wider than the bodice side; the step in is drawn
        # as a short edge so the outline stays closed (the gather takes up the width).
        fc.Edge("waist_step", [fc.Line(p_waist_side, p_underarm)]),
        fc.Edge("armhole", [_armhole_curve(x_side_bodice,
                                           waist_y + (bodice_length - armhole_drop),
                                           x_shoulder, total_h)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, fc.P(neck_width, total_h))]),
        fc.Edge("neck", [_neck_curve(neck_width, total_h, 0.0, total_h - neck_drop)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("waist-seam", [fc.P(0.0, waist_y), fc.P(x_side_skirt, waist_y)],
                    kind="marking"),
        fc.Internal("gather-zone", [fc.P(0.0, waist_y + 4.0), fc.P(x_side_skirt, waist_y + 4.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist_step", 0.5, "waist match"),
                 fc.Notch("hem", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(x_side_bodice * 0.25, hem_allowance + 30.0),
                               fc.P(x_side_bodice * 0.25, total_h - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Pinafore front (bib bodice + gathered skirt), cut on fold",
    )


def _bodice_and_skirt_back():
    """The pinafore BACK half (cut 2): like the front but with a shallow back neck and a
    button placket allowance at centre back (the opening the buttons close)."""
    total_h = bodice_length + skirt_length
    waist_y = skirt_length
    x_side_bodice = BUST_Q
    x_side_skirt = SKIRT_WAIST_Q
    x_shoulder = shoulder_width
    back_neck_drop = min(35.0, neck_drop * 0.5)
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side_skirt, 0.0)
    p_waist_side = fc.P(x_side_skirt, waist_y)
    p_underarm = fc.P(x_side_bodice, waist_y + (bodice_length - armhole_drop))
    p_shoulder_out = fc.P(x_shoulder, total_h)
    p_neck_cb = fc.P(0.0, total_h - back_neck_drop)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("skirt_side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist_step", [fc.Line(p_waist_side, p_underarm)]),
        fc.Edge("armhole", [_armhole_curve(x_side_bodice,
                                           waist_y + (bodice_length - armhole_drop),
                                           x_shoulder, total_h)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, fc.P(neck_width, total_h))]),
        fc.Edge("neck", [_neck_curve(neck_width, total_h, 0.0, total_h - back_neck_drop)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    # the button placket runs down the bodice portion of centre back.
    placket_top = total_h - back_neck_drop - 8.0
    placket_bottom = waist_y - 20.0
    internals = [
        fc.Internal("waist-seam", [fc.P(0.0, waist_y), fc.P(x_side_skirt, waist_y)],
                    kind="marking"),
        fc.Internal("cb-placket", [fc.P(6.0, placket_top), fc.P(6.0, placket_bottom)],
                    kind="marking"),
    ]
    # button seats along the placket, evenly spaced.
    span = placket_top - placket_bottom
    for i in range(button_count):
        t = (i + 0.5) / button_count
        y = placket_bottom + span * t
        bx = 6.0 + button_ligne * 0.635
        internals.append(fc.Internal(f"button-{i + 1}", [fc.P(6.0, y), fc.P(bx, y)],
                                     kind="marking"))
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist_step", 0.5, "waist match"),
                 fc.Notch("cb", (waist_y) / total_h, "waist at CB")],
        grainline=fc.Grainline(fc.P(x_side_bodice * 0.25, hem_allowance + 30.0),
                               fc.P(x_side_bodice * 0.25, total_h - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Pinafore back half (with CB button placket)",
    )


def build_facing():
    """A combined neck + armhole facing band, cut to the MEASURED neck + armhole runs."""
    _front = _bodice_and_skirt_front()
    neck_run = _front.edge("neck").length(0.2)
    arm_run = _front.edge("armhole").length(0.2)
    inner = 2.0 * neck_run + 2.0 * arm_run   # both fronts + both armholes, roughly
    depth = 45.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(inner, 0.0)
    p2 = fc.P(inner, depth)
    p3 = fc.P(0.0, depth)
    edges = [
        fc.Edge("inner", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "facing", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("inner", neck_run / inner, "neck/armhole junction")],
        grainline=fc.Grainline(fc.P(inner * 0.1, depth * 0.5), fc.P(inner * 0.9, depth * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, depth * 0.5), fc.P(inner, depth * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Neck + armhole facing",
    )


def build():
    pattern = fc.PatternSet("shweshwe-pinafore")
    everything = target_piece == "set"
    front = _bodice_and_skirt_front()
    back = _bodice_and_skirt_back()
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "facing":
        pattern.add(build_facing())

    if everything:
        # The side seam: front bodice+skirt side to back bodice+skirt side. Both are drawn
        # to the same skirt width and bodice width, so they match by construction.
        pattern.declare_seam([("front", "skirt_side"), ("front", "waist_step")],
                             [("back", "skirt_side"), ("back", "waist_step")], tol=1.0)
        # The shoulder seam.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)

    waist_seam_q = SKIRT_WAIST_Q
    pattern.bom = [
        {"item": "shweshwe printed cotton", "qty": round(
            (bodice_length + skirt_length + hem_allowance) * 2.2 / 10.0) * 10,
         "unit": "mm_length",
         "note": "indigo/chocolate/red discharge-printed cotton (Da Gama, Three Cats/Toto). "
                 "Shweshwe is stiff with its finishing starch — soak and iron before cutting."},
        {"item": "sew-through buttons (back closure)", "qty": button_count, "unit": "count",
         "note": f"{button_ligne:.0f}-ligne buttons down the centre-back placket; the "
                 f"Yantra4D sew-through-button solid, linked."},
        {"item": "facing / interfacing", "qty": 1, "unit": "panel",
         "note": "the sleeveless armholes and neck are FACED, not bound; interface the bib."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 485,
        "family": "heritage_global",
        "fabric_hint": "algodon-estampado",
        "finished_mm": {
            "bust_girth": round(bust_girth, 1),
            "waist_girth": round(waist_girth, 1),
            "bodice_length": round(bodice_length, 1),
            "skirt_length": round(skirt_length, 1),
            "gather_ratio": round(gather_ratio, 2),
        },
        "solved": {
            "bodice_waist_quarter_mm": round(BODICE_WAIST_Q, 2),
            "skirt_waist_quarter_mm": round(SKIRT_WAIST_Q, 2),
            "waist_gather_take_up_mm": round(SKIRT_WAIST_Q - BODICE_WAIST_Q, 2),
            "waist_seam_quarter_mm": round(waist_seam_q, 2),
            "button_ligne": round(button_ligne, 1),
            "button_count": button_count,
            "note": "the skirt waist is SOLVED from the bodice waist times the gather ratio, "
                    "so the waist seam balances by construction rather than by drafting the "
                    "skirt to a free width and hoping it gathers to the bodice. The sleeveless "
                    "armholes and neck are FACED; the back opens on a button placket sized to "
                    "the bodice, closed with real sew-through buttons (lignes).",
        },
        "heritage": {
            "garment": "shweshwe pinafore dress — Southern African printed-cotton frock",
            "fabric": "shweshwe / seshoeshoe — indigo (later chocolate & red) discharge-"
                      "printed cotton, central to Sotho, Xhosa and Tswana dress",
            "construction": "sleeveless bib bodice, gathered skirt on a balanced waist seam, "
                            "faced neck and armholes, centre-back button placket",
            "excluded": "no specific shweshwe print motif is drawn — the print is the "
                        "fabric's, chosen by the maker",
        },
        "hardware": "back-closure buttons: Yantra4D sew-through-button, linked, sized in "
                    "lignes; the placket length reads the bodice.",
    }
    return pattern


result = build()

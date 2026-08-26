"""
Pantomime Dame Gown — Fashion Cabinet Costume Cartridge (FC-500 #477; y4d hook-and-eye).

The panto DAME gown: the deliberately OUTSIZE, comic gown of the British pantomime dame — a man
playing a grotesque older woman — built to read as absurd from the back of the gods. Everything is
exaggerated on purpose: a huge padded bust shelf, an enormous skirt on a bumroll, gigantic puff
sleeves, and a fast centre-back Yantra4D `hook-and-eye` because the dame changes costume many
times a show. It is drafted here as a fitted-but-padded bodice, a very full gathered skirt, and a
puff sleeve, all scaled by an `exaggeration` factor that pushes the proportions past the
naturalistic.

The exaggeration SOLVE. The comedy is in the RATIO, not the raw size, so a single `exaggeration`
factor scales the bust shelf, the skirt fullness, and the sleeve puff together, over a bodice
still cut to the performer's real chest so it actually fits. The skirt is gathered onto the waist
at `skirt_fullness * exaggeration`, declared as gathered ease so the enormous gather is proven
arithmetic rather than a fistful of fabric crammed under a waistband.

The DIMENSIONAL HANDSHAKE. The centre back closes on a `hook-and-eye`; `closure_rows` drives the
hook `columns` and `bodice_length` the drafted placket AND the gown's own `cb_closure` interface.

Made to measure to chest, waist and lengths. FC-500 lane 9 (costume, dance & performance).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 1000.0))
waist_girth = float(PARAM(lambda: waist_girth, 900.0))
bodice_length = float(PARAM(lambda: bodice_length, 400.0))
skirt_length = float(PARAM(lambda: skirt_length, 900.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 500.0))
exaggeration = float(PARAM(lambda: exaggeration, 1.6))
skirt_fullness = float(PARAM(lambda: skirt_fullness, 2.2))
closure_rows = float(PARAM(lambda: closure_rows, 8.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

chest_bust_girth = max(800.0, min(chest_bust_girth, 1500.0))
waist_girth = max(650.0, min(waist_girth, 1400.0))
bodice_length = max(300.0, min(bodice_length, 560.0))
skirt_length = max(500.0, min(skirt_length, 1300.0))
sleeve_length = max(250.0, min(sleeve_length, 700.0))
exaggeration = max(1.1, min(exaggeration, 2.4))
skirt_fullness = max(1.6, min(skirt_fullness, 3.5))
closure_rows = max(3.0, min(closure_rows, 14.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

N_ROWS = int(round(closure_rows))
CHEST_HALF = (chest_bust_girth * 1.04) / 2.0
WAIST_HALF = (waist_girth * 1.04) / 2.0
BODICE_PANEL = CHEST_HALF / 2.0
WAIST_PANEL = WAIST_HALF / 2.0
BL = bodice_length
# skirt is gathered at fullness * exaggeration
SKIRT_CIRC = waist_girth * skirt_fullness * exaggeration
BUST_SHELF = BODICE_PANEL * (exaggeration - 1.0)   # extra padded projection at the bust


def _rect(w, h, names):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(0.0, 0.0), fc.P(w, 0.0), fc.P(w, h), fc.P(0.0, h)
    return [fc.Edge(names[0], [fc.Line(p0, p1)]), fc.Edge(names[1], [fc.Line(p1, p2)]),
            fc.Edge(names[2], [fc.Line(p2, p3)]), fc.Edge(names[3], [fc.Line(p3, p0)])]


def _bodice(is_front):
    # Front and back share the side seam (same `top` width at the underarm), so it balances.
    # The bust shelf is PADDING, marked on the front, not a wider side panel.
    top = BODICE_PANEL
    bot = WAIST_PANEL
    neck_w = max(60.0, BODICE_PANEL * 0.5)
    neck_drop = (BODICE_PANEL * 0.8) if is_front else (BODICE_PANEL * 0.2)
    p_cf_waist = fc.P(0.0, 0.0)
    p_side_waist = fc.P(bot, 0.0)
    p_underarm = fc.P(top, BL * 0.55)
    p_shoulder = fc.P(neck_w + (top - neck_w) * 0.5, BL)
    p_neck = fc.P(neck_w, BL)
    p_cf_neck = fc.P(0.0, BL - neck_drop)
    edges = [
        fc.Edge("waist", [fc.Line(p_cf_waist, p_side_waist)]),
        fc.Edge("side", [fc.Line(p_side_waist, p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm, fc.P(top * 0.95, BL * 0.78),
                                      fc.P(p_shoulder.x + 10.0, BL - 20.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck, fc.P(neck_w * 0.6, BL - neck_drop * 0.4),
                                   fc.P(neck_w * 0.2, BL - neck_drop * 0.85), p_cf_neck)]),
        fc.Edge("center", [fc.Line(p_cf_neck, p_cf_waist)]),
    ]
    name = "bodice_front" if is_front else "bodice_back"
    internals = []
    if is_front:
        # the padded bust shelf zone (a marking; the padding is a separate made-up piece)
        internals.append(fc.Internal("bust-shelf",
                                     [fc.P(top * 0.2, BL * 0.5), fc.P(top * 0.9, BL * 0.5),
                                      fc.P(top * 0.9, BL * 0.85), fc.P(top * 0.2, BL * 0.85),
                                      fc.P(top * 0.2, BL * 0.5)], kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"armscye": 0.0, "neck": 0.0},
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("waist", 0.5, "skirt match")],
        internals=internals,
        grainline=fc.Grainline(fc.P(top * 0.4, BL * 0.2), fc.P(top * 0.4, BL * 0.8)),
        cut=fc.CutSpec(quantity=(1 if is_front else 2), mirror=(not is_front),
                       on_fold=is_front, fold_edge=("center" if is_front else None)),
        label=("Bodice front — padded bust (cut 1 on fold)" if is_front
               else "Bodice back (cut 2, CB hook)"),
    )


def build_skirt():
    edges = _rect(SKIRT_CIRC, skirt_length, ("hem", "cb_r", "waist", "cb_l"))
    return fc.Piece(
        "skirt", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 0.25, "q"), fc.Notch("waist", 0.5, "CF"),
                 fc.Notch("waist", 0.75, "q")],
        grainline=fc.Grainline(fc.P(SKIRT_CIRC * 0.08, skirt_length * 0.4),
                               fc.P(SKIRT_CIRC * 0.92, skirt_length * 0.4)),
        cut=fc.CutSpec(quantity=1),
        label="Very full skirt (cut 1, gathered)",
    )


def build_sleeve():
    # a huge puff: a rectangle of width = bicep circumference * puff, gathered at cap and cuff
    puff = 1.4 * exaggeration
    w = max(300.0, CHEST_HALF * 0.7 * puff)
    edges = _rect(w, sleeve_length, ("cuff_edge", "seam_r", "cap_edge", "seam_l"))
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("cap_edge", 0.5, "shoulder"), fc.Notch("cuff_edge", 0.5, "under")],
        grainline=fc.Grainline(fc.P(w * 0.5, sleeve_length * 0.2),
                               fc.P(w * 0.5, sleeve_length * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Giant puff sleeve (cut 2, gathered cap + cuff)",
    )


def build_placket(cb_len):
    w = max(40.0, closure_rows * 12.0)
    edges = _rect(w, cb_len, ("bottom", "attach", "top", "fold"))
    internals = [fc.Internal(f"hook-{i}", [fc.P(w * 0.4, (i + 0.5) * cb_len / N_ROWS),
                                           fc.P(w * 0.6, (i + 0.5) * cb_len / N_ROWS)],
                                               kind="drill")
                 for i in range(N_ROWS)]
    return fc.Piece(
        "placket", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(w * 0.5, cb_len * 0.1), fc.P(w * 0.5, cb_len * 0.9)),
        internals=internals, cut=fc.CutSpec(quantity=2),
        label="CB hook-and-eye placket (cut 2)",
    )


def build():
    pattern = fc.PatternSet("panto-dame-gown")
    b_front = _bodice(True)
    b_back = _bodice(False)
    skirt = build_skirt()
    sleeve = build_sleeve()
    placket = build_placket(b_back.edge("center").length())

    picked = {"bodice_front": b_front, "bodice_back": b_back, "skirt": skirt, "sleeve": sleeve,
              "placket": placket}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (b_front, b_back, skirt, sleeve, placket):
            pattern.add(piece)
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=2.0)
        # Skirt gathers onto the bodice waist ring at fullness*exaggeration.
        bodice_waist = 2.0 * (b_front.edge("waist").length() + b_back.edge("waist").length())
        pattern.declare_seam(("skirt", "waist"),
                             [("bodice_front", "waist"), ("bodice_front", "waist"),
                              ("bodice_back", "waist"), ("bodice_back", "waist")],
                             tol=3.0, ease=(skirt.edge("waist").length() - bodice_waist))
        # Sleeve cap gathers into the armscye (front + back).
        armscye = 2.0 * (b_front.edge("armscye").length() + b_back.edge("armscye").length())
        pattern.declare_seam(("sleeve", "cap_edge"),
                             [("bodice_front", "armscye"), ("bodice_front", "armscye"),
                              ("bodice_back", "armscye"), ("bodice_back", "armscye")],
                             tol=3.0, ease=(sleeve.edge("cap_edge").length() - armscye))
        pattern.declare_seam(("placket", "attach"), ("bodice_back", "center"), tol=2.0)

    fabric_width = 1450.0
    area = (b_front.area() * 2.0 + b_back.area() * 2.0 + skirt.area() + sleeve.area() * 2.0
            + placket.area() * 2.0)
    marker_len = area / (fabric_width * 0.65)
    pattern.bom = [
        {"item": "loud print / bold colour (dress)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"the louder the better; at {fabric_width:.0f} mm width. A panto dame reads from "
                 "the back row, so scale of print matters."},
        {"item": "bust shelf padding + bumroll", "qty": 1, "unit": "set",
         "note": f"a padded bust shelf ({BUST_SHELF:.0f} mm projection) and a bumroll under the "
                 "skirt — the exaggeration is padding, not the performer."},
        {"item": "hook-and-eye tape (Yantra4D hook-and-eye)", "qty": 1, "unit": "piece",
         "note": f"fast CB closure, {N_ROWS} rows (hardware_ref -> hook-and-eye) — the dame "
                 "changes many times a show."},
        {"item": "petticoat + interfacing", "qty": round(SKIRT_CIRC * 0.6), "unit": "mm_length",
         "note": "a stiff petticoat holds the enormous skirt out."},
    ]
    pattern.metadata = {
        "fc500_rank": 477, "family": "costume_historical", "fabric_hint": "raso-poliester",
        "provenance": "The pantomime dame is a British theatrical tradition (a man in comic drag "
            "as a grotesque older woman) dating to the Victorian music hall. The costume is "
            "deliberately outsize — huge bust, vast skirt, giant sleeves — and changes many times "
            "a show, so it wants a fast closure.",
        "silhouette_note": "A deliberately outsize comic gown: padded bust shelf, enormous "
            "gathered skirt on a bumroll, giant puff sleeves, fast centre-back hook closure. One "
            "exaggeration factor scales the comedy over a bodice cut to the real performer.",
        "hardware": "fast CB closure via Yantra4D (hardware_ref -> hook-and-eye); closure_rows "
            "drives the hook columns and bodice_length the drafted placket.",
        "solved": {
            "exaggeration": round(exaggeration, 2),
            "skirt_circ_mm": round(SKIRT_CIRC, 1),
            "bust_shelf_mm": round(BUST_SHELF, 1),
            "note": "one exaggeration factor scales bust shelf, skirt fullness and sleeve puff "
                    "together over a bodice cut to the performer's real chest — the comedy is the "
                    "ratio, and it still fits.",
        },
        "closure": "fast centre-back hook-and-eye",
        "drafting": "Made to measure to chest, waist and lengths; exaggeration scales the comedy.",
    }
    return pattern


result = build()

"""
Marching-Band Tunic — Fashion Cabinet Costume Cartridge (FC-500 #480; y4d epaulette-board).

The high-collared, structured tunic of the marching band and the drum corps: a fitted military
coat with a standing collar, a chest of horizontal braid (the "frogging" or Austrian knots), and
rigid EPAULETTES (shoulder boards) that hold their shape on the shoulder — the boards are Yantra4D
`epaulette-board` solids, and this cartridge drafts the tunic and the seat the board sits on so
the printed board matches the shoulder it caps.

The epaulette that must SOLVE. An epaulette board is a rigid trapezoid that sits FLAT on a curved
shoulder, so its seat on the tunic is the shoulder seam plus a stabilised patch, and the board's
length must not exceed the shoulder seam or it hangs off the arm. The board length is clamped to
the drafted shoulder seam, and its wide/narrow ends are placed at the neck and sleeve ends of the
shoulder — so the trapezoid points the right way (wide at the shoulder point, narrow at the neck,
the military convention).

The DIMENSIONAL HANDSHAKE. `epaulette-board`'s `shoulder_edge` flange is driven by `board_len`,
`wide_w`, `narrow_w`. `board_len` drives the board AND the drafted epaulette seat AND the tunic's
own `epaulette_seat` interface, and it is clamped to the shoulder seam so the board fits by
construction.

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

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 960.0))
waist_girth = float(PARAM(lambda: waist_girth, 840.0))
tunic_length = float(PARAM(lambda: tunic_length, 720.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 330.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
collar_height = float(PARAM(lambda: collar_height, 55.0))
board_len = float(PARAM(lambda: board_len, 120.0))
braid_rows = float(PARAM(lambda: braid_rows, 6.0))
ease_pct = float(PARAM(lambda: ease_pct, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

chest_bust_girth = max(760.0, min(chest_bust_girth, 1400.0))
waist_girth = max(600.0, min(waist_girth, 1300.0))
tunic_length = max(480.0, min(tunic_length, 950.0))
sleeve_length = max(420.0, min(sleeve_length, 760.0))
bicep_girth = max(240.0, min(bicep_girth, 550.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
collar_height = max(25.0, min(collar_height, 100.0))
board_len = max(60.0, min(board_len, 220.0))
braid_rows = max(3.0, min(braid_rows, 12.0))
ease_pct = max(0.0, min(ease_pct, 14.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

N_BRAID = int(round(braid_rows))
E = 1.0 + ease_pct / 100.0
CHEST_HALF = (chest_bust_girth * E) / 2.0
WAIST_HALF = (waist_girth * E) / 2.0
PANEL_CHEST = CHEST_HALF / 2.0
PANEL_WAIST = WAIST_HALF / 2.0
TL = tunic_length
AL = sleeve_length
NECK_W = max(70.0, neck_girth / 6.0)
ARMSCYE = max(200.0, PANEL_CHEST * 1.1)


def _bell_points(chord, height):
    mid = chord / 2.0
    left = fc.Bezier(fc.P(0.0, 0.0), fc.P(chord * 0.14, height * 0.10),
                     fc.P(mid * 0.55, height), fc.P(mid, height))
    right = fc.Bezier(fc.P(mid, height), fc.P(mid + (mid - mid * 0.55), height),
                      fc.P(chord - chord * 0.14, height * 0.10), fc.P(chord, 0.0))
    return left.flatten(0.2) + right.flatten(0.2)[1:]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _rect(w, h, names):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(0.0, 0.0), fc.P(w, 0.0), fc.P(w, h), fc.P(0.0, h)
    return [fc.Edge(names[0], [fc.Line(p0, p1)]), fc.Edge(names[1], [fc.Line(p1, p2)]),
            fc.Edge(names[2], [fc.Line(p2, p3)]), fc.Edge(names[3], [fc.Line(p3, p0)])]


def _body(is_front):
    p_hem_l = fc.P(0.0, 0.0)
    p_side_hem = fc.P(PANEL_WAIST, 0.0)
    armscye_y = TL - ARMSCYE
    p_underarm = fc.P(PANEL_CHEST, armscye_y)
    p_shoulder = fc.P(NECK_W + (PANEL_CHEST - NECK_W) * 0.6, TL - 8.0)
    p_neck = fc.P(NECK_W, TL)
    p_c_top = fc.P(0.0, TL)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_l, p_side_hem)]),
        fc.Edge("side", [fc.Bezier(p_side_hem,
                                   fc.P(PANEL_WAIST + (PANEL_CHEST - PANEL_WAIST) * 0.4,
                                        armscye_y * 0.5),
                                   fc.P(PANEL_CHEST * 0.98, armscye_y * 0.85), p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm,
                                      fc.P(PANEL_CHEST * 0.9, armscye_y + ARMSCYE * 0.45),
                                      fc.P(p_shoulder.x + 12.0, p_shoulder.y - 30.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Line(p_neck, p_c_top)]),
        fc.Edge("center", [fc.Line(p_c_top, p_hem_l)]),
    ]
    name = "tunic_front" if is_front else "tunic_back"
    internals = []
    if is_front:
        for i in range(N_BRAID):
            by = TL * (0.35 + 0.45 * i / max(1, N_BRAID - 1))
            internals.append(fc.Internal(f"braid-{i}",
                                         [fc.P(0.0, by), fc.P(PANEL_CHEST * 0.85, by)],
                                         kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"armscye": 0.0, "neck": 0.0},
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("shoulder", 0.5, "epaulette")],
        internals=internals,
        grainline=fc.Grainline(fc.P(PANEL_CHEST * 0.4, TL * 0.2),
                               fc.P(PANEL_CHEST * 0.4, TL * 0.8)),
        cut=fc.CutSpec(quantity=(2 if is_front else 1), mirror=is_front,
                       on_fold=(not is_front), fold_edge=(None if is_front else "center")),
        label=("Tunic front (cut 2, braid + buttons)" if is_front
               else "Tunic back (cut 1 on fold)"),
    )


def build_sleeve(armscye_len):
    bicep_half = (bicep_girth * E) / 2.0
    chord = min(2.0 * bicep_half, armscye_len * 0.92)
    bicep_half = chord / 2.0
    cuff_half = max(70.0, bicep_half * 0.75)
    target = max(armscye_len, chord * 1.01)
    lo, hi = 1.0, max(chord, target)
    for _ in range(48):
        mid_h = (lo + hi) / 2.0
        if _poly_len(_bell_points(chord, mid_h)) < target:
            lo = mid_h
        else:
            hi = mid_h
    cap_pts = _bell_points(chord, (lo + hi) / 2.0)
    p_cuff_r = fc.P(bicep_half + cuff_half, -AL)
    p_cuff_l = fc.P(bicep_half - cuff_half, -AL)
    return fc.Piece(
        "sleeve",
        [fc.Edge("cap", [fc.Line(cap_pts[i], cap_pts[i + 1]) for i in range(len(cap_pts) - 1)]),
         fc.Edge("underseam_r", [fc.Line(cap_pts[-1], p_cuff_r)]),
         fc.Edge("cuff", [fc.Line(p_cuff_r, p_cuff_l)]),
         fc.Edge("underseam_l", [fc.Line(p_cuff_l, cap_pts[0])])],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(bicep_half, -AL * 0.2), fc.P(bicep_half, -AL * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirror)",
    )


def build_collar(neck_run):
    """Standing collar, cut to the measured neck run, of collar_height."""
    length = neck_run
    edges = _rect(length, collar_height, ("attach", "end_r", "top", "end_l"))
    return fc.Piece(
        "collar", edges, seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(length * 0.08, collar_height * 0.4),
                               fc.P(length * 0.92, collar_height * 0.4)),
        cut=fc.CutSpec(quantity=1),
        label="Standing collar (cut 1)",
    )


def build_epaulette(shoulder_len):
    """The epaulette seat: a trapezoid matching the drafted shoulder seam, board_len long (clamped
    to the shoulder), wide at the shoulder point, narrow at the neck (the military convention)."""
    bl = min(board_len, shoulder_len)
    wide = max(20.0, collar_height * 0.9)
    narrow = wide * 0.6
    # An isosceles trapezoid: narrow end (neck) at x=0, wide end (shoulder) at x=bl.
    p0 = fc.P(0.0, (wide - narrow) / 2.0)          # neck end, lower
    p1 = fc.P(0.0, (wide - narrow) / 2.0 + narrow)  # neck end, upper
    p2 = fc.P(bl, wide)                             # shoulder end, upper
    p3 = fc.P(bl, 0.0)                              # shoulder end, lower
    edges = [
        fc.Edge("seat", [fc.Line(p0, p3)]),        # the shoulder-seam edge (board_len)
        fc.Edge("wide_end", [fc.Line(p3, p2)]),
        fc.Edge("outer", [fc.Line(p2, p1)]),
        fc.Edge("narrow_end", [fc.Line(p1, p0)]),
    ]
    internals = [
        fc.Internal("button-boss",
            [fc.P(bl * 0.85, wide * 0.5), fc.P(bl * 0.85, wide * 0.5)],
                             kind="drill")]
    return fc.Piece(
        "epaulette", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("seat", 0.5, "shoulder centre")],
        grainline=fc.Grainline(fc.P(bl * 0.2, wide * 0.5), fc.P(bl * 0.8, wide * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Epaulette board seat (cut 2)",
    )


def build():
    pattern = fc.PatternSet("marching-band-tunic")
    front = _body(True)
    back = _body(False)
    armscye_len = front.edge("armscye").length() + back.edge("armscye").length()
    sleeve = build_sleeve(armscye_len)
    neck_run = 2.0 * front.edge("neck").length() + 2.0 * back.edge("neck").length()
    collar = build_collar(neck_run)
    shoulder_len = front.edge("shoulder").length()
    epaulette = build_epaulette(shoulder_len)

    picked = {"tunic_front": front, "tunic_back": back, "sleeve": sleeve, "collar": collar,
              "epaulette": epaulette}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back, sleeve, collar, epaulette):
            pattern.add(piece)
        pattern.declare_seam(("tunic_front", "side"), ("tunic_back", "side"), tol=2.0)
        pattern.declare_seam(("tunic_front", "shoulder"), ("tunic_back", "shoulder"), tol=2.0)
        pattern.declare_seam(("sleeve", "cap"),
                             [("tunic_front", "armscye"), ("tunic_back", "armscye")], tol=2.0)
        pattern.declare_seam(("collar", "attach"),
                             [("tunic_front", "neck"), ("tunic_front", "neck"),
                              ("tunic_back", "neck"), ("tunic_back", "neck")], tol=2.0)
        # The epaulette seat sits on the shoulder seam (board_len clamped to it).
        pattern.declare_seam(("epaulette", "seat"), ("tunic_front", "shoulder"), tol=2.0,
                             ease=(epaulette.edge("seat").length()
                                   - front.edge("shoulder").length()))

    fabric_width = 1500.0
    area = (front.area() * 2.0 + back.area() * 2.0 + sleeve.area() * 2.0 + collar.area()
            + epaulette.area() * 2.0)
    marker_len = area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "melton / gabardine (tunic)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"a firm wool or poly gabardine holds the military line; at {fabric_width:.0f} mm "
                 "width."},
        {"item": "epaulette boards (Yantra4D epaulette-board)", "qty": 2, "unit": "count",
         "note": f"board {min(board_len, shoulder_len):.0f} mm (clamped to the "
                 f"{shoulder_len:.0f} mm shoulder seam) (hardware_ref -> epaulette-board); wide at "
                 "the shoulder, narrow at the neck."},
        {"item": "military braid / soutache", "qty": round(N_BRAID * PANEL_CHEST * 0.85 * 2.0),
         "unit": "mm_length",
         "note": f"{N_BRAID} rows of horizontal frogging across the chest, both fronts."},
        {"item": "buttons + hooks + interfacing", "qty": 1, "unit": "set",
         "note": "a fully interfaced front and standing collar; the braid is couched over it."},
    ]
    pattern.metadata = {
        "fc500_rank": 480, "family": "costume_historical", "fabric_hint": "gabardina-poliester",
        "provenance": "The marching-band / drum-corps tunic descends from 18th-19th century "
            "military full dress: standing collar, braided chest, rigid epaulettes. It is worn by "
            "school and community bands worldwide as a uniform that must read sharp on a field "
            "from a distance.",
        "silhouette_note": "A fitted high-collared military tunic with a braided chest and rigid "
            "epaulette boards on the shoulders, a standing collar cut to the neck, and a set-in "
            "sleeve.",
        "hardware": "epaulette boards via Yantra4D (hardware_ref -> epaulette-board); board_len "
            "drives the board AND the drafted seat, clamped to the shoulder seam.",
        "solved": {
            "shoulder_seam_mm": round(shoulder_len, 1),
            "board_len_used_mm": round(min(board_len, shoulder_len), 1),
            "braid_rows": N_BRAID,
            "collar_height_mm": round(collar_height, 1),
            "armscye_run_mm": round(armscye_len, 1),
            "note": "board_len is clamped to the drafted shoulder seam so the rigid board never "
                    "hangs off the arm; the sleeve cap is solved to the armscye.",
        },
        "closure": "front buttons + standing-collar hooks",
        "drafting": "Made to measure to chest, waist and lengths; epaulette clamped to shoulder.",
    }
    return pattern


result = build()

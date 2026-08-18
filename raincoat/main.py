"""
Raincoat — FC-100 rank #61. Fashion Cabinet Garment Cartridge.

A hooded WATERPROOF shell coat ("impermeable"): the zip-hoodie / track-jacket
zip-front architecture (rank #14 / #51) lengthened to a knee-length coat and
cut ROOMY over layers, dressed with every raincoat detail as verified geometry.

  - The front is cut as TWO mirrored halves whose center edge is the SEPARATING
    zipper seam (15 mm tape allowance, top/bottom stop notches, 7 mm stitch line
    per the zipper-notion convention). The zipper is a Yantra4D solid.
  - A STORM FLAP (placket) covers the zip: a distinct panel whose `attach` edge
    is bisection-solved to the measured front center edge, so it sews onto the CF
    with delta ≈ 0 (declared). Snap crosses mark the closure (snaps are a Yantra4D
    ref, never drafted). Under-flap over the teeth is what keeps rain off the zip.
  - The HOOD is TWO panels whose neck edge is SOLVED by bisection to the half neck
    opening (hoodie-pullover method): hood.neck ↔ (front.neck + back.neck),
    delta ≈ 0. A brim wire channel + a face drawcord are marked/BOM.
  - The set-in SLEEVE cap is solved by bisection to the measured armhole pair PLUS
    a declared ease; underarm ventilation eyelets are marked (grommets = BOM).
  - The signature waterproof property is CONSTRUCTION, not a new outline: the BOM
    carries SEAM-SEALING TAPE at ~the total sewn seam length, and a note that the
    heat-taped seams over the needle holes are what actually make it waterproof.
  - A back storm-cape / yoke vent is a marked ventilation line (teaching-grade),
    with big flap pockets marked on the fronts. All markings are traces.

Reference idioms borrowed:
  - zip-hoodie / track-jacket (#14 / #51): halved-at-CF separating-zip front
    (tape allowance, stop notches, stitch line, derived zipper length), set-in
    sleeve cap solved to the armhole pair with declared ease.
  - hoodie-pullover (#5): the TWO-PANEL HOOD whose neck edge is bisection-solved
    to the half neck opening (attach-a-piece-to-a-measured-curve).
  - trench-coat (#60): the long shell-coat silhouette, the storm flap caught /
    attached over the front, and flap-pocket + back-cape ventilation markings.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front | back | sleeve | hood | storm_flap | set

chest_girth    = float(PARAM(lambda: chest_girth, 1020.0))
body_length    = float(PARAM(lambda: body_length, 1040.0))   # nape to knee-length hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 620.0))  # cap apex to wrist
shell_ease     = float(PARAM(lambda: shell_ease, 240.0))     # roomy layering ease
hood_height    = float(PARAM(lambda: hood_height, 380.0))    # generous rain hood
hood_depth     = float(PARAM(lambda: hood_depth, 280.0))
storm_flap_w   = float(PARAM(lambda: storm_flap_w, 70.0))    # finished storm-flap width
cap_ease       = float(PARAM(lambda: cap_ease, 25.0))        # eased set-in cap
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))  # taped-seam allowance
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))   # coat hem

# ── Clamps (mirror the manifest sliders) ─────────────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1800.0))
body_length = max(820.0, min(body_length, 1300.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(460.0, min(sleeve_length, 780.0))
shell_ease = max(140.0, min(shell_ease, 420.0))
hood_height = max(300.0, min(hood_height, 460.0))
hood_depth = max(220.0, min(hood_depth, 340.0))
storm_flap_w = max(45.0, min(storm_flap_w, 100.0))
cap_ease = max(0.0, min(cap_ease, 45.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(25.0, min(hem_allowance, 65.0))

# ── Roomy shell-coat block (sweatshirt frame, lengthened + widened) ──────────
CHEST_E = chest_girth + shell_ease
W = CHEST_E / 4.0                              # quarter body width (CF/CB at x=0)
L = body_length
AH = CHEST_E / 8.0 + 130.0                     # coat-deep armhole (HPS to underarm)
AH = max(200.0, min(AH, L - 300.0))
NW = max(66.0, neck_girth / 5.0 + 8.0)         # wider neck: the hood needs room
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 34.0)           # coat shoulder sits a touch lower
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 92.0
BACK_NECK_DROP = 22.0
YOKE_Y = max(UNDERARM.y + 40.0, HPS_Y - 250.0)  # back storm-cape ventilation line
ZIP_SA = 15.0          # tape allowance on the front center edge (zipper seam)
ZIP_STITCH = 7.0       # stitch line offset from the seam line (zipper-notion)
ZIP_STOP_INSET = 12.0  # stop notches sit this far inside the seam ends


def _armhole_edge():
    span = SH_END.y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - span * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + span * 0.30), UNDERARM)],
    )


def _body_edges(neck_drop):
    """Half-body outline shared by front and back; center edge at x = 0."""
    neck_top_y = HPS_Y - neck_drop
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(neck_drop, 24.0) * 0.45), fc.P(NW, HPS_Y))],
    )
    return [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]


def _flap_pocket_marks():
    """Big flap hip-pocket: a flap outline + its attach line (welt is future work)."""
    cx = min(W * 0.55, W - 90.0)
    attach = max(150.0, min(L * 0.34, UNDERARM.y - 120.0))
    fw, fh = 210.0, 70.0
    flap = [fc.P(cx - fw / 2.0, attach), fc.P(cx + fw / 2.0, attach),
            fc.P(cx + fw / 2.0, attach - fh), fc.P(cx - fw / 2.0, attach - fh),
            fc.P(cx - fw / 2.0, attach)]
    line = [fc.P(cx - fw / 2.0 - 8.0, attach + 14.0),
            fc.P(cx + fw / 2.0 + 8.0, attach + 14.0)]
    return [
        fc.Internal("hip flap pocket", flap, kind="trace"),
        fc.Internal("flap attach line", line, kind="trace"),
    ]


def build_front():
    """Half front, cut 2 mirrored (never on fold): the center edge is the zip seam.

    The center edge carries a 15 mm tape allowance for the SEPARATING zipper, a
    7 mm stitch line and top/bottom stop notches. The storm flap (a separate
    piece) covers this edge in wear. Big flap hip pockets are marked."""
    zlen = HPS_Y - FRONT_NECK_DROP                 # straight zipper-seam length (CF)
    t_stop = ZIP_STOP_INSET / zlen
    internals = [
        fc.Internal(
            "zipper stitch line",
            [fc.P(ZIP_STITCH, ZIP_STOP_INSET), fc.P(ZIP_STITCH, zlen - ZIP_STOP_INSET)],
            kind="trace",
        ),
        fc.Internal(
            "storm-flap placement (over CF, right front laps left)",
            [fc.P(storm_flap_w, ZIP_STOP_INSET), fc.P(storm_flap_w, zlen - ZIP_STOP_INSET)],
            kind="trace",
        ),
    ]
    internals += _flap_pocket_marks()
    return fc.Piece(
        "front",
        _body_edges(FRONT_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": ZIP_SA},
        notches=[
            fc.Notch("side", 0.5), fc.Notch("armhole", 0.5),
            fc.Notch("center", 1.0 - t_stop, "zipper top stop"),
            fc.Notch("center", t_stop, "zipper bottom stop"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.62, 90.0), fc.P(W * 0.62, L - 150.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (zip half)",
    )


def build_back():
    """Back, cut 1 on fold. A back storm-cape / yoke line is a ventilation
    marking (a real cape panel is future work); the knee-length hem finishes with
    a generous coat allowance."""
    top = fc.P(W - 20.0, YOKE_Y + 6.0)
    return fc.Piece(
        "back",
        _body_edges(BACK_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 90.0), fc.P(W * 0.62, L - 150.0)),
        internals=[
            fc.Internal("back storm-cape / vent yoke line (ventilation)",
                        [fc.P(0.0, YOKE_Y), top], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12), fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch), fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
    """Set-in sleeve; the cap is solved by bisection to the measured armhole pair
    PLUS the declared ease (a set-in cap eases into the armhole). Underarm
    ventilation eyelets are marked (grommets are BOM, never drafted)."""
    ch = max(60.0, AH * 0.30)
    sl = max(120.0, sleeve_length - ch)
    goal = cap_target + cap_ease
    lo, hi = 20.0, goal / 2.0 + ch + 80.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < goal:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - goal) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(105.0, hb * 0.66)
    vent_y = sl * 0.16
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl + ch * 0.5)),
        internals=[
            fc.Internal("underarm ventilation eyelet 1",
                        [fc.P(-chw * 0.5, vent_y), fc.P(-chw * 0.5, vent_y)], kind="drill"),
            fc.Internal("underarm ventilation eyelet 2",
                        [fc.P(chw * 0.5, vent_y), fc.P(chw * 0.5, vent_y)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (set-in, eased)",
    )


def _hood_neck_edge(back_x):
    """Hood bottom (neck seam): front-bottom corner to a scaled back-bottom point."""
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(back_x, 35.0), fc.P(back_x * 0.60, -22.0),
                   fc.P(back_x * 0.28, -18.0), fc.P(0.0, 0.0))],
    )


def build_hood(half_opening):
    """Two-panel hood; the neck edge is solved by bisection to the half neck
    opening (hoodie-pullover method). A brim-wire channel runs the face edge and
    a face drawcord threads the front (wire + cord + stops are BOM)."""
    lo, hi = half_opening * 0.35, half_opening * 1.1
    for _ in range(48):
        bx = (lo + hi) / 2.0
        if _hood_neck_edge(bx).length(0.05) < half_opening:
            lo = bx
        else:
            hi = bx
    bx = (lo + hi) / 2.0
    if abs(_hood_neck_edge(bx).length(0.05) - half_opening) > 1.0:
        raise ValueError("hood neck-edge solver did not converge")
    face_x = -20.0                                     # slight forward rain overhang
    top = fc.P(face_x + 30.0, hood_height)
    edges = [
        _hood_neck_edge(bx),                           # back-bottom → front-bottom
        fc.Edge("face", [fc.Line(fc.P(0.0, 0.0), fc.P(face_x, hood_height * 0.55)),
                         fc.Line(fc.P(face_x, hood_height * 0.55), top)]),
        fc.Edge(
            "crown",
            [fc.Bezier(top, fc.P(top.x + hood_depth * 0.55, hood_height + 8.0),
                       fc.P(bx + (hood_depth - bx) * 0.9, hood_height * 0.72),
                       fc.P(hood_depth, hood_height * 0.45)),
             fc.Bezier(fc.P(hood_depth, hood_height * 0.45),
                       fc.P(hood_depth - 4.0, hood_height * 0.22),
                       fc.P(bx + 14.0, 60.0), fc.P(bx, 35.0))],
        ),
    ]
    return fc.Piece(
        "hood",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match"),
                 fc.Notch("face", 0.5, "brim wire / drawcord")],
        grainline=fc.Grainline(fc.P(hood_depth * 0.45, 80.0),
                               fc.P(hood_depth * 0.45, hood_height * 0.8)),
        internals=[
            fc.Internal("face brim-wire channel + drawcord",
                        [fc.P(2.0, hood_height * 0.10), fc.P(face_x + 2.0, hood_height * 0.55),
                         fc.P(face_x + 30.0, hood_height - 6.0)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood (side panel)",
    )


def build_storm_flap(center_len):
    """The STORM FLAP over the zip: a placket panel whose `attach` edge is solved
    by bisection to the measured front center edge so it sews onto the CF with
    delta ≈ 0 (declared). It laps over the closed zipper to keep rain off the
    teeth; snap crosses mark the closure (snaps are a Yantra4D ref). Cut 1
    (covers the CF once). The free edges include the seam allowance."""
    # attach edge is a straight vertical line of exactly the front center length.
    a0 = fc.P(0.0, 0.0)
    a1 = fc.P(0.0, center_len)
    ow = storm_flap_w + seam_allowance             # outer (free) width past CF
    internals = [
        fc.Internal("storm-flap fold / CF cover line",
                    [fc.P(storm_flap_w, 6.0), fc.P(storm_flap_w, center_len - 6.0)],
                    kind="trace"),
    ]
    # snap crosses down the flap (hardware = Yantra4D snap-notion; not drafted)
    n_snaps = max(3, int(center_len // 180.0))
    for i in range(n_snaps):
        sy = center_len * (i + 0.5) / n_snaps
        sx = storm_flap_w * 0.5
        internals += [
            fc.Internal(f"snap {i + 1}-h", [fc.P(sx - 5.0, sy), fc.P(sx + 5.0, sy)], kind="drill"),
            fc.Internal(f"snap {i + 1}-v", [fc.P(sx, sy - 5.0), fc.P(sx, sy + 5.0)], kind="drill"),
        ]
    return fc.Piece(
        "storm_flap",
        [
            fc.Edge("attach", [fc.Line(a0, a1)]),          # sews onto the CF zip edge
            fc.Edge("top", [fc.Line(a1, fc.P(ow, center_len))]),
            fc.Edge("outer", [fc.Line(fc.P(ow, center_len), fc.P(ow, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ow, 0.0), a0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": seam_allowance, "outer": seam_allowance, "bottom": seam_allowance},
        notches=[fc.Notch("attach", 1.0 - ZIP_STOP_INSET / center_len, "zipper top stop"),
                 fc.Notch("attach", ZIP_STOP_INSET / center_len, "zipper bottom stop")],
        grainline=fc.Grainline(fc.P(ow * 0.5, center_len * 0.2),
                               fc.P(ow * 0.5, center_len * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Storm Flap (placket over CF zip)",
    )


def build():
    pattern = fc.PatternSet("raincoat")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    # HALF opening = one front-half neck + one back-half neck. One hood panel
    # covers one side of the head; its neck edge is solved to exactly this length.
    half_opening = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    center_len = front.edge("center").length(0.05)

    names = ("front", "back", "sleeve", "hood", "storm_flap")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    sleeve = build_sleeve(cap_target) if wanted["sleeve"] else None
    hood = build_hood(half_opening) if wanted["hood"] else None
    storm_flap = build_storm_flap(center_len) if wanted["storm_flap"] else None

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(sleeve)
    if wanted["hood"]:
        pattern.add(hood)
    if wanted["storm_flap"]:
        pattern.add(storm_flap)

    # ── Declared seams (every sewn relationship; delta ≈ 0) ──────────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        # Front is cut 2 (never on fold): each physical sleeve meets ONE front
        # armhole + ONE back armhole — the drafted pair. The cap carries ease.
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")],
                             tol=2.0, ease=cap_ease)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
    if wanted["hood"] and wanted["front"] and wanted["back"]:
        # One hood panel's neck edge = the half opening (one front + one back neck).
        pattern.declare_seam([("hood", "neck")],
                             [("front", "neck"), ("back", "neck")], tol=2.0)
    if wanted["storm_flap"] and wanted["front"]:
        # The storm flap's attach edge sews onto ONE front center (the zip edge).
        pattern.declare_seam(("storm_flap", "attach"), ("front", "center"), tol=1.5)

    # ── Seam-sealing tape: ~the TOTAL sewn seam length (the waterproofing) ────
    # Every needle-perforated seam is heat-taped on the inside; the tape length
    # is the sum of the physical sewn seams (each seam once, counting both cut-2
    # fronts and the folded back). This is what actually waterproofs the coat.
    front_side = front.edge("side").length()
    front_shoulder = front.edge("shoulder").length()
    front_arm = front.edge("armhole").length()
    back_arm = back.edge("armhole").length()
    hood_neck = hood.edge("neck").length() if hood else half_opening
    sleeve_underarm = sleeve.edge("underarm_front").length() if sleeve else 0.0
    # 2 side seams + 2 shoulder seams + 2 armhole rings + 2 underarm seams
    # + hood↔neck ring (2 panels) + CF zip seam + storm-flap attach.
    tape_len = (
        2.0 * front_side                       # both side seams
        + 2.0 * front_shoulder                 # both shoulder seams
        + 2.0 * (front_arm + back_arm)         # both set-in armhole rings
        + 2.0 * sleeve_underarm                # both sleeve underarm seams
        + 2.0 * hood_neck                      # hood neck ring (2 panels to neckline)
        + center_len                           # CF zipper tape seam
        + center_len                           # storm-flap attach seam
    )
    tape_len_mm = int(round(tape_len / 10.0) * 10)

    # Separating zipper: full CF opening + a little into the neck; order to 10 mm.
    zip_total = center_len + 20.0
    zipper_len = int(round(zip_total / 10.0) * 10)

    # ── Shell fabric marker (nylon-ripstop-shell) ────────────────────────────
    fabric_width = 1450.0                              # ripstop shell card width
    total_area = 0.0
    for p in pattern.pieces:
        mult = p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        total_area += p.area() * mult
    # If a single piece was requested, still give a representative full-garment
    # marker by summing the always-present body pieces.
    if target_piece != "set":
        total_area = (front.area() * 2.0 + back.area() * 2.0
                      + (sleeve.area() * 2.0 if sleeve else 0.0)
                      + (hood.area() * 2.0 if hood else 0.0)
                      + (storm_flap.area() if storm_flap else 0.0))
    marker_len = total_area / (fabric_width * 0.60)    # crisp shell nests moderately
    marker_len_mm = round(marker_len / 10.0) * 10

    n_snaps = max(3, int(center_len // 180.0))
    pattern.bom = [
        {"item": "nylon-ripstop-shell",
         "qty": marker_len_mm, "unit": "mm_length",
         "note": f"waterproof shell at {fabric_width:.0f} mm width, ~60% marker "
                 "efficiency; a DWR finish or a PU/PTFE laminate grade takes this "
                 "ripstop from water-resistant to waterproof. Cut true (no stretch "
                 "compensation); pin inside the allowance with a fine microtex "
                 "needle so the holes stay small"},
        {"item": "seam-sealing tape (heat-activated)",
         "qty": tape_len_mm, "unit": "mm_length",
         "note": f"~{tape_len_mm} mm = the total sewn seam length. HEAT-TAPING every "
                 "needle-perforated seam on the inside is WHAT MAKES THE COAT "
                 "WATERPROOF — the fabric may be laminated, but every stitch is a "
                 "hole until the tape seals it. Taped seams are the raincoat's "
                 "defining construction property (see docs/README.md)"},
        {"item": "separating zipper (water-resistant)",
         "qty": zipper_len, "unit": "mm_length",
         "note": f"order this SEPARATING (open-end) zipper, ~{zipper_len} mm = the CF "
                 "opening; run it under the STORM FLAP so rain sheds off the teeth. "
                 "A water-resistant / laminated zipper tape is preferred. Slider / "
                 "pull / teeth HARDWARE is a Yantra4D cartridge reference "
                 "(zipper-notion), never drafted here"},
        {"item": "storm-flap snaps", "qty": n_snaps, "unit": "pcs",
         "note": f"{n_snaps} snap fasteners down the storm flap to hold it closed "
                 "over the zip; snap HARDWARE is a Yantra4D cartridge reference "
                 "(snap-notion), never drafted here"},
        {"item": "hood face drawcord", "qty": round(half_opening * 2.2 + 200.0),
         "unit": "mm_length",
         "note": "elastic/round drawcord threaded through the hood face channel to "
                 "cinch the hood against wind-driven rain"},
        {"item": "cord stops / cord locks", "qty": 2, "unit": "pcs",
         "note": "2 spring cord locks on the hood drawcord (and optional hem cord); "
                 "HARDWARE is a Yantra4D cartridge reference (cord-stop notion), "
                 "never drafted here"},
        {"item": "hood brim wire", "qty": round(half_opening * 1.1),
         "unit": "mm_length",
         "note": "a bendable brim wire in the hood face channel holds a rain visor "
                 "shape (optional; omit for a soft hood)"},
        {"item": "underarm ventilation eyelets / grommets", "qty": 4, "unit": "pcs",
         "note": "4 metal eyelets (2 per underarm) for pit ventilation; grommet "
                 "HARDWARE is a Yantra4D cartridge reference (eyelet notion)"},
        {"item": "polyester thread + fine microtex needle 70/10", "qty": 1, "unit": "set",
         "note": "sew with a fine microtex needle so the needle holes stay small for "
                 "the seam tape to bridge; do NOT skip the taping step"},
    ]

    pattern.metadata = {
        "fc100_rank": 61,
        "fabric_hint": "nylon-ripstop-shell",
        "silhouette": "hooded knee-length waterproof shell coat",
        "waterproofing_note": "the raincoat's defining property is CONSTRUCTION, not a "
                              "special outline: every needle-perforated seam is "
                              "HEAT-TAPED on the inside (BOM seam-sealing tape ~ total "
                              "seam length). The laminated/DWR shell resists water; the "
                              "taped seams over the stitch holes are what make it "
                              "actually waterproof",
        "closure_note": "full-length CENTER-FRONT separating zipper under a STORM FLAP; "
                        "the front is cut 2 (never on fold) with a 15 mm tape allowance, "
                        "7 mm stitch line and top/bottom stop notches on the center edge",
        "storm_flap": {"finished_width_mm": round(storm_flap_w, 1),
                       "attach": "front center (CF) seam (declared, delta ~ 0)",
                       "closure": "snap fasteners (Yantra4D)",
                       "note": "laps over the closed zipper to keep rain off the teeth"},
        "hood": {"panels": 2, "solved_to": "half neck opening (bisection)",
                 "height_mm": round(hood_height, 1), "depth_mm": round(hood_depth, 1),
                 "features": "brim-wire channel + face drawcord (BOM)"},
        "ventilation": "back storm-cape / vent-yoke line + 2 underarm eyelets per sleeve "
                       "(marked; grommets are BOM)",
        "seam_tape_length_mm": tape_len_mm,
        "zipper_length_mm": zipper_len,
        "neck_half_opening_mm": round(half_opening, 1),
        "hood_neck_solved_mm": round(hood_neck, 1),
        "armhole_pair_mm": round(cap_target, 1),
        "cap_ease_mm": cap_ease,
        "cap_target_mm": round(cap_target + cap_ease, 1),
        "center_edge_mm": round(center_len, 1),
        "seam_allowance_mm": seam_allowance,
        "hem_allowance_mm": hem_allowance,
        "drafting": "roomy sweatshirt/zip block halved at CF for the separating zipper, "
                    "lengthened to a knee-length coat and widened for layering; set-in "
                    "cap solved to the armhole pair + declared ease; two-panel hood "
                    "solved to the half neck opening; storm-flap placket solved to the "
                    "front center edge; waterproofing carried as seam-sealing tape "
                    "(~ total seam length) + taped-seam note, not a new outline",
    }
    return pattern


result = build()

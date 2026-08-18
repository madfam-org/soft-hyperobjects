"""
Parka — FC-100 rank #59. Fashion Cabinet Garment Cartridge.

A long, roomy, insulated hooded technical coat (thigh/knee length). The
zip-hoodie architecture (rank #14) grown into a coat: the front is cut as TWO
mirrored halves whose center edge is a full separating zipper seam (15 mm tape
allowance, top/bottom stop notches, 7 mm stitch line per the zipper-notion
convention); the back is cut on fold; the set-in sleeve cap is SOLVED by
bisection against the measured armhole pair plus a small declared ease; and the
two-panel HOOD's neck edge is SOLVED by bisection to the measured half neck
opening (the hoodie method), declared against front.neck + back.neck so the
delta is ~0.

Two parka-signature pieces sit on top of that block, each verified:
  - a STORM FLAP: a placket strip that snaps over the zipper. Its `attach`
    edge is a straight line of exactly the front center (zipper) length, so it
    sews into the CF seam with delta ~0 (declared) — the trench gun-flap
    method applied to the center front. Snap positions are marked; snap
    hardware is a Yantra4D notion reference.
  - a BELLOWS PATCH POCKET: a real chamfered patch pocket (cut 2) with a 3D
    bellows-gusset fold trace and a flap marking — a big cargo hip pocket, an
    appliqué that is not sewn into a length-balanced seam (patch-pocket idiom).

Roomy-coat finishes, all honest markings + BOM (blazer-pocket rule):
  - a DRAWCORD WAIST and a DRAWCORD HEM: internal channel traces on the front
    and back with cord-exit eyelet marks; cord + cord stops are BOM (stops are
    a Yantra4D notion), waist/hem elastic-or-cord length is exact-mm.
  - RIB inner CUFFS at the sleeve hem: derived rib bands (sleeve opening x
    cuff_ratio), negative-eased storm cuffs inside the shell sleeve.
  - full INSULATED LINING: shell quilted/bagged to a lining over synthetic
    fill — BOM lines for lining + fill (by garment area) + a fur-trim note for
    the hood edge.

Geometry stays a normal long jacket; the parka-ness is the storm flap, the
hood, the bellows pocket, the drawcord channels, the rib cuffs, and the BOM —
exactly like the blazer's pockets are markings on a normal jacket block.

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
# front|back|sleeve|hood|storm_flap|pocket|cuff|set

chest_girth    = float(PARAM(lambda: chest_girth, 1060.0))
body_length    = float(PARAM(lambda: body_length, 820.0))    # HPS region to coat hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 640.0))
parka_ease     = float(PARAM(lambda: parka_ease, 260.0))     # roomy layering ease
hood_height    = float(PARAM(lambda: hood_height, 380.0))
hood_depth     = float(PARAM(lambda: hood_depth, 280.0))
cap_ease       = float(PARAM(lambda: cap_ease, 20.0))        # eased set-in cap
storm_flap_w   = float(PARAM(lambda: storm_flap_w, 70.0))    # finished storm-flap width
cuff_ratio     = float(PARAM(lambda: cuff_ratio, 0.80))      # inner rib cuff/opening
cuff_height    = float(PARAM(lambda: cuff_height, 70.0))
waist_ratio    = float(PARAM(lambda: waist_ratio, 0.70))     # drawcord waist height ↑ hem
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps (match the manifest slider bounds) ────────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1600.0))
body_length = max(680.0, min(body_length, 1050.0))
neck_girth = max(320.0, min(neck_girth, 540.0))
sleeve_length = max(500.0, min(sleeve_length, 780.0))
parka_ease = max(160.0, min(parka_ease, 420.0))
hood_height = max(300.0, min(hood_height, 460.0))
hood_depth = max(220.0, min(hood_depth, 360.0))
cap_ease = max(0.0, min(cap_ease, 40.0))
storm_flap_w = max(45.0, min(storm_flap_w, 100.0))
cuff_ratio = max(0.60, min(cuff_ratio, 0.95))
cuff_height = max(40.0, min(cuff_height, 110.0))
waist_ratio = max(0.55, min(waist_ratio, 0.85))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(20.0, min(hem_allowance, 55.0))

# ── Parka block (roomy coat off the zip-hoodie/bomber body frame) ────────────
W = (chest_girth + parka_ease) / 4.0            # quarter body width
L = body_length
AH = (chest_girth + parka_ease) / 8.0 + 120.0   # coat-deep armhole (auto)
AH = max(200.0, min(AH, L - 120.0))
NW = max(66.0, neck_girth / 5.0 + 8.0)          # wider neck: the hood needs room
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 34.0)            # coat shoulder sits a touch lower
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 95.0
BACK_NECK_DROP = 22.0
ZIP_SA = 15.0          # tape allowance on the front center edge (zipper seam)
ZIP_STITCH = 7.0       # stitch line offset from the seam line (zipper-notion)
ZIP_STOP_INSET = 12.0  # stop notches sit this far inside the seam ends
WAIST_Y = min(L * waist_ratio, UNDERARM.y - 30.0)   # drawcord waist below chest
WAIST_Y = max(WAIST_Y, L * 0.40)
HEM_CHANNEL_Y = max(45.0, hem_allowance + 12.0)     # drawcord hem channel height


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


def _drawcord_channels(is_front):
    """Waist + hem drawcord channel traces (two parallel lines each = the casing)
    plus cord-exit eyelet marks. On the front they stop short of the zipper /
    storm-flap edge (x = 40) so the cord exits through eyelets, not the zip."""
    x_in = 40.0 if is_front else 0.0
    casing = 22.0                                   # channel casing height
    marks = [
        fc.Internal("waist drawcord channel",
                    [fc.P(x_in, WAIST_Y), fc.P(W, WAIST_Y)], kind="trace"),
        fc.Internal("waist drawcord channel (lower)",
                    [fc.P(x_in, WAIST_Y - casing), fc.P(W, WAIST_Y - casing)],
                    kind="trace"),
        fc.Internal("hem drawcord channel",
                    [fc.P(x_in, HEM_CHANNEL_Y), fc.P(W, HEM_CHANNEL_Y)], kind="trace"),
        fc.Internal("hem drawcord channel (upper)",
                    [fc.P(x_in, HEM_CHANNEL_Y + casing), fc.P(W, HEM_CHANNEL_Y + casing)],
                    kind="trace"),
    ]
    if is_front:
        # cord-exit eyelets near the front edge at waist and hem
        for label, y in (("waist eyelet", WAIST_Y - casing / 2.0),
                         ("hem eyelet", HEM_CHANNEL_Y + casing / 2.0)):
            marks.append(fc.Internal(label,
                         [fc.P(x_in + 6.0, y), fc.P(x_in + 6.0, y - 1.0)], kind="drill"))
    return marks


def build_front():
    """Half front, cut 2 mirrored (never on fold): the center edge is the zip
    seam. Carries the drawcord waist + hem channels and the pocket placement."""
    zlen = HPS_Y - FRONT_NECK_DROP                 # straight zipper-seam length
    t_stop = ZIP_STOP_INSET / zlen
    stitch = fc.Internal(
        "zipper stitch line",
        [fc.P(ZIP_STITCH, ZIP_STOP_INSET), fc.P(ZIP_STITCH, zlen - ZIP_STOP_INSET)],
        kind="trace",
    )
    # bellows-pocket placement box (the pocket piece is drafted separately)
    pk_cx = min(W * 0.55, W - 130.0)
    pk_cy = max(HEM_CHANNEL_Y + 90.0, WAIST_Y - 190.0)
    pk_w, pk_h = 200.0, 220.0
    placement = fc.Internal(
        "pocket placement",
        [fc.P(pk_cx - pk_w / 2.0, pk_cy + pk_h / 2.0),
         fc.P(pk_cx + pk_w / 2.0, pk_cy + pk_h / 2.0),
         fc.P(pk_cx + pk_w / 2.0, pk_cy - pk_h / 2.0),
         fc.P(pk_cx - pk_w / 2.0, pk_cy - pk_h / 2.0),
         fc.P(pk_cx - pk_w / 2.0, pk_cy + pk_h / 2.0)],
        kind="marking",
    )
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
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 120.0)),
        internals=[stitch, placement] + _drawcord_channels(is_front=True),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (zip half)",
    )


def build_back():
    return fc.Piece(
        "back",
        _body_edges(BACK_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 120.0)),
        internals=_drawcord_channels(is_front=False),
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
    """Long set-in coat sleeve; the cap is solved by bisection to the armhole
    pair PLUS the declared cap ease. A rib storm cuff finishes the wrist."""
    ch = max(60.0, AH * 0.30)
    sl = max(140.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(100.0, hb * 0.62)
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match"), fc.Notch("hem", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.5)),
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
    opening. The face edge carries a drawcord channel + fur-trim note; the trim
    itself is a BOM line."""
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
    face_x = -20.0                                     # slight forward overhang
    top = fc.P(face_x + 30.0, hood_height)
    face = fc.Edge("face", [fc.Line(fc.P(0.0, 0.0), fc.P(face_x, hood_height * 0.55)),
                            fc.Line(fc.P(face_x, hood_height * 0.55), top)])
    edges = [
        _hood_neck_edge(bx),                           # back-bottom → front-bottom
        face,
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
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(hood_depth * 0.45, 80.0),
                               fc.P(hood_depth * 0.45, hood_height * 0.8)),
        internals=[fc.Internal(
            "face drawcord channel (fur-trim edge)",
            [fc.P(-6.0, hood_height * 0.10), fc.P(face_x - 6.0, hood_height * 0.55),
             fc.P(top.x - 6.0, hood_height - 6.0)], kind="trace")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood (side panel)",
    )


def build_storm_flap(zip_len):
    """The parka STORM FLAP: a placket strip that snaps over the separating
    zipper on the inside of the left front. Its `attach` edge is a straight line
    of exactly the front center (zipper) length, so it sews into the CF seam
    with delta ~0 (declared) — the trench gun-flap method at the center front.
    Snap positions are marked; snap hardware is a Yantra4D notion reference.
    Cut 1 (left front only)."""
    w = storm_flap_w + seam_allowance              # attach sa on the CF side only
    a0 = fc.P(0.0, 0.0)
    a1 = fc.P(0.0, zip_len)                         # attach edge, length = zip seam
    snaps = []
    n = max(3, int(zip_len // 150.0))
    for i in range(n):
        y = zip_len * (i + 0.5) / n
        snaps.append(fc.Internal(f"snap-{i + 1}",
                     [fc.P(w * 0.55, y - 4.5), fc.P(w * 0.55, y + 4.5)], kind="drill"))
        snaps.append(fc.Internal(f"snap-{i + 1}-x",
                     [fc.P(w * 0.55 - 4.5, y), fc.P(w * 0.55 + 4.5, y)], kind="drill"))
    return fc.Piece(
        "storm_flap",
        [
            fc.Edge("attach", [fc.Line(a0, a1)]),      # sewn into the CF zip seam
            fc.Edge("top", [fc.Line(a1, fc.P(w, zip_len))]),
            fc.Edge("free_edge", [fc.Line(fc.P(w, zip_len), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), a0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"attach": ZIP_SA},                 # matches the front center tape
        notches=[fc.Notch("attach", 0.5, "CF match")],
        grainline=fc.Grainline(fc.P(w * 0.5, zip_len * 0.15),
                               fc.P(w * 0.5, zip_len * 0.85)),
        internals=snaps,
        cut=fc.CutSpec(quantity=1),
        label="Storm Flap (zip placket, left front)",
    )


def build_pocket():
    """Big BELLOWS cargo hip pocket — a real chamfered patch pocket (cut 2),
    with a 3D bellows-gusset fold trace around the sides/bottom and a flap
    marking above the opening. An appliqué: it is topstitched to the front, not
    sewn into a length-balanced seam (patch-pocket idiom), so no seam declare."""
    w, h, c = 200.0, 210.0, 34.0                       # width, height, chamfer
    gusset = 26.0                                       # bellows depth (fold-back)
    inset = gusset + 8.0
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),           # opening
        fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, c))]),
        fc.Edge("chamfer_r", [fc.Line(fc.P(w, c), fc.P(w - c, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w - c, 0.0), fc.P(c, 0.0))]),
        fc.Edge("chamfer_l", [fc.Line(fc.P(c, 0.0), fc.P(0.0, c))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, c), fc.P(0.0, h))]),
    ]
    bellows = fc.Internal(
        "bellows fold line",
        [fc.P(inset, h), fc.P(inset, inset), fc.P(w - inset, inset), fc.P(w - inset, h)],
        kind="trace",
    )
    flap = fc.Internal(
        "flap (cut + fold above opening)",
        [fc.P(-6.0, h + 8.0), fc.P(w + 6.0, h + 8.0), fc.P(w + 6.0, h + 78.0),
         fc.P(-6.0, h + 78.0), fc.P(-6.0, h + 8.0)],
        kind="marking",
    )
    return fc.Piece(
        "pocket",
        edges,
        seam_allowance=seam_allowance,
        allowances={"top": 25.0},                      # folded facing on the opening
        notches=[fc.Notch("top", 0.5, "center match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.15), fc.P(w / 2.0, h * 0.85)),
        internals=[bellows, flap],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bellows Cargo Pocket",
    )


def _rib(name, finished_len, finished_height, qty, label):
    """Derived rib band (bomber idiom): folded to 2 x height, no solve check."""
    band_h = 2.0 * finished_height
    length = finished_len + 2.0 * seam_allowance
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("parka")
    front = build_front()
    back = build_back()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    cap_target = front_ah + back_ah + cap_ease
    half_opening = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    zip_len = front.edge("center").length(0.05)
    everything = target_piece == "set"

    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    sleeve = None
    if everything or target_piece in ("sleeve", "cuff"):
        sleeve = build_sleeve(cap_target)              # cuff needs the measured opening
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "hood":
        pattern.add(build_hood(half_opening))
    if everything or target_piece == "storm_flap":
        pattern.add(build_storm_flap(zip_len))
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())
    if everything or target_piece == "cuff":
        cuff_circ = sleeve.edge("hem").length()
        pattern.add(_rib("cuff", cuff_circ * cuff_ratio, cuff_height, 2,
                         "Storm Cuff (rib)"))

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Front is cut 2 (not on fold), so each PHYSICAL sleeve meets exactly
        # ONE front armhole + ONE back armhole — the drafted pair — with the
        # declared cap ease.
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")],
                             ease=cap_ease, tol=2.5)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
        # One hood panel covers one side of the head: its neck edge equals the
        # half opening (one front half's neck + the folded back's neck).
        pattern.declare_seam([("hood", "neck")],
                             [("front", "neck"), ("back", "neck")], tol=2.0)
        # Storm flap is caught in the center-front (zipper) seam of the left front.
        pattern.declare_seam(("storm_flap", "attach"), ("front", "center"), tol=1.5)

    # Full separating zipper to order: the front opening runs the center edge
    # plus the hem drawcord-channel casing below the bottom stop.
    zip_total = zip_len + HEM_CHANNEL_Y
    # Fabric consumption estimate (shell) for the BOM marker.
    fabric_width = 1450.0                               # nylon-ripstop-shell card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    ) if pattern.pieces else 0.0
    marker_len = total_area / (fabric_width * 0.60) if total_area else 0.0
    shell_qty = round(marker_len / 10.0) * 10
    waist_cord = round((2.0 * (front.edge("hem").length() + back.edge("hem").length())
                        * 0.85 + 300.0) / 10.0) * 10   # waist wrap + tails
    hem_cord = round((2.0 * (front.edge("hem").length() + back.edge("hem").length())
                      + 300.0) / 10.0) * 10            # hem wrap + tails

    pattern.bom = [
        {"item": "nylon-ripstop-shell", "qty": shell_qty, "unit": "mm_length",
         "note": f"outer shell at {fabric_width:.0f} mm width, ~60% marker efficiency; "
                 f"slippery hand — pin inside the allowance, fine microtex needle"},
        {"item": "insulated lining (taffeta/ripstop bagged to fill)", "qty": shell_qty,
         "unit": "mm_length",
         "note": "full body + sleeve + hood lining; lining pieces are "
                 "noted-not-drafted in v0 (cut from the shell fronts/back/sleeves/"
                 "hood). The shell is bagged to the lining over the fill."},
        {"item": "synthetic insulation fill (60–100 g/m^2)", "qty":
         round(total_area / 1_000_000.0 * 1.15, 2), "unit": "m2",
         "note": "garment area + 15% for quilting take-up; a real down parka uses "
                 "baffled down instead — synthetic keeps loft when wet (shell note)"},
        {"item": "separating zipper (closed-bottom, coil)", "qty": 1, "unit": "pcs",
         "note": f"~{int(round(zip_total / 10.0) * 10)} mm full separating zipper; "
                 f"slider/pull hardware is a Yantra4D cartridge via the "
                 f"zipper-notion reference, never re-implemented here"},
        {"item": "snap fasteners (storm-flap placket)", "qty": max(3, int(zip_len // 150.0)),
         "unit": "pcs",
         "note": "cover snaps over the zipper on the storm flap; snap hardware is a "
                 "Yantra4D cartridge reference, never re-implemented here"},
        {"item": "drawcord (waist)", "qty": waist_cord, "unit": "mm_length",
         "note": "elastic-or-cord waist drawcord through the waist channel; exits at "
                 "the two front eyelets"},
        {"item": "drawcord (hem)", "qty": hem_cord, "unit": "mm_length",
         "note": "hem drawcord through the hem channel; exits at the two front hem "
                 "eyelets to cinch the coat hem"},
        {"item": "cord stops / toggles", "qty": 4, "unit": "pcs",
         "note": "2 waist + 2 hem spring cord-locks; cord-stop hardware is a Yantra4D "
                 "cartridge reference, never re-implemented here"},
        {"item": "hood drawcord + 2 cord stops", "qty": 1, "unit": "set",
         "note": "cord through the hood face channel to close the hood; stops are a "
                 "Yantra4D cartridge reference"},
        {"item": "detachable fur-trim ruff (hood face edge)", "qty": 1, "unit": "pcs",
         "note": "faux-fur ruff snapped to the hood face edge; a parka signature — "
                 "optional, and a purchased trim, not drafted here"},
        {"item": "polyester thread + microtex 80/12 needle", "qty": 1, "unit": "set",
         "note": "topstitch the bellows pockets, storm flap and channels; press "
                 "seams low, tape/seal if a waterproof build is wanted"},
    ]
    pattern.metadata = {
        "fc100_rank": 59,
        "fabric_hint": "nylon-ripstop-shell",
        "silhouette": "long hooded insulated parka (thigh/knee length)",
        "shell_note": "lightweight ripstop nylon shell (95 gsm); bagged to an "
                      "insulated lining over synthetic fill (a real down parka uses "
                      "baffled down — synthetic keeps loft when wet)",
        "lining": "full insulated lining noted-not-drafted in v0 (BOM lines); cut "
                  "from the shell fronts/back/sleeves/hood",
        "storm_flap": {"attach": "center-front (zipper) seam of the left front (declared)",
                       "finished_width_mm": round(storm_flap_w, 1),
                       "snaps": max(3, int(zip_len // 150.0)),
                       "note": "snaps over the zipper; snap hardware is Yantra4D"},
        "hood": {"panels": 2, "solved": "neck edge bisected to the half neck opening",
                 "height_mm": round(hood_height, 1), "depth_mm": round(hood_depth, 1),
                 "face": "drawcord channel + detachable fur ruff (BOM)"},
        "bellows_pocket": {"cut": "cut 2 mirror", "gusset": "3D bellows fold trace",
                           "flap": "cut-and-fold flap above the opening",
                           "attach": "topstitched appliqué (not a length-balanced seam)"},
        "drawcord": {"waist_y_mm": round(WAIST_Y, 1),
                     "hem_channel_y_mm": round(HEM_CHANNEL_Y, 1),
                     "waist_cord_mm": waist_cord, "hem_cord_mm": hem_cord,
                     "note": "elastic-or-cord through casing channels; front eyelets"},
        "cuff": {"type": "rib storm cuff inside the shell sleeve",
                 "ratio": cuff_ratio, "height_mm": round(cuff_height, 1)},
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_ease_mm": cap_ease,
        "cap_target_mm": round(cap_target, 1),
        "half_neck_opening_mm": round(half_opening, 1),
        "zipper_seam_mm": round(zip_len, 1),
        "zipper_length_mm": int(round(zip_total / 10.0) * 10),
        "seam_allowance_mm": seam_allowance,
        "hem_allowance_mm": hem_allowance,
        "drafting": "zip-hoodie block grown to a long roomy coat: front halved at "
                    "CF for a full separating zipper; set-in cap solved to the "
                    "armholes + declared ease; two-panel hood solved to the half "
                    "neck opening; storm flap caught in the CF seam (gun-flap "
                    "method); bellows cargo pockets as topstitched appliqués; "
                    "drawcord waist + hem channels; rib storm cuffs; full "
                    "insulated lining and fill in the BOM",
        "teaching_grade": "geometry is a normal long jacket; the parka-ness lives "
                          "in the storm flap, hood, bellows pockets, drawcord "
                          "channels, rib cuffs and BOM (blazer-pocket rule). "
                          "Insulation/fill/lining/fur/cord/snaps are purchased "
                          "components; zipper/snap/cord-stop hardware is Yantra4D.",
    }
    return pattern


result = build()

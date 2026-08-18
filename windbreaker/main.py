"""
Windbreaker — FC-100 rank #62. Fashion Cabinet Garment Cartridge.

A lightweight, UNLINED hooded shell jacket — the simplest Wave-J technical
piece (no insulation, no quilting). It reuses the zip-hoodie / track-jacket
halved-at-CF full-zip front (front cut as TWO mirrored halves whose center
edge is the separating-zipper seam: 15 mm tape allowance, top/bottom stop
notches, 7 mm stitch line) and the hoodie-pullover TWO-PANEL HOOD whose neck
edge is SOLVED by bisection to the HALF neck opening (delta ≈ 0). The set-in
sleeve cap is likewise SOLVED against the measured armhole pair with a small
ease.

The SIGNATURE FINISH is elastic/drawcord, done as SELF-FABRIC CASINGS on the
shell edges (no separate rib bands — a windbreaker is unlined shell):
  - body hem  → a deep hem casing (fold-line marked) with a DRAWCORD threaded
                through and two cord stops at the two CF exits (exact-mm BOM).
  - sleeve hem→ a deep cuff casing (fold-line marked) with ELASTIC threaded and
                joined to a recovered circumference (exact-mm BOM).
  - hood face → a drawcord channel (marked) with a drawcord + two cord stops.
The hood packs away into the collar area (stowaway note). All zipper, cord-stop
and drawcord HARDWARE is a Yantra4D cartridge reference in the BOM (never
drafted here). The shell is DWR-treated ripstop nylon — wind- and
water-resistant; a fine microtex needle keeps the needle holes small.

Idioms borrowed:
  - zip-hoodie / track-jacket: halved-at-CF separating-zip front (tape
    allowance, stop notches, stitch line), set-in cap solved to the armhole
    pair, derived zipper length, the notion.hardware_ref block.
  - hoodie-pullover: the two-panel hood solved by bisection to the half neck
    opening (attach-piece-to-measured-curve).

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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front | back | sleeve | hood | set

chest_girth   = float(PARAM(lambda: chest_girth, 1040.0))
body_length   = float(PARAM(lambda: body_length, 680.0))    # nape to finished hem
neck_girth    = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 610.0))  # to finished cuff
shell_ease    = float(PARAM(lambda: shell_ease, 200.0))     # relaxed shell, positive
hood_height   = float(PARAM(lambda: hood_height, 360.0))
hood_depth    = float(PARAM(lambda: hood_depth, 270.0))
hem_casing    = float(PARAM(lambda: hem_casing, 32.0))      # body-hem drawcord casing depth
cuff_casing   = float(PARAM(lambda: cuff_casing, 30.0))     # sleeve-hem elastic casing depth
cuff_ratio    = float(PARAM(lambda: cuff_ratio, 0.72))      # elastic / sleeve-hem opening
face_channel  = float(PARAM(lambda: face_channel, 24.0))    # hood-face drawcord channel depth
pockets       = bool(PARAM(lambda: pockets, True))          # hand + chest pockets (markings)
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest sliders) ─────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 950.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(200.0, min(sleeve_length, 800.0))
shell_ease = max(100.0, min(shell_ease, 450.0))
hood_height = max(280.0, min(hood_height, 450.0))
hood_depth = max(200.0, min(hood_depth, 340.0))
hem_casing = max(18.0, min(hem_casing, 55.0))
cuff_casing = max(18.0, min(cuff_casing, 50.0))
cuff_ratio = max(0.55, min(cuff_ratio, 0.95))
face_channel = max(16.0, min(face_channel, 40.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# ── Derived draft dimensions ─────────────────────────────────────────────────
# Positive ease → relaxed unlined shell (worn over layers). Crisp ripstop cuts
# true (fabric card cut_scale = 1.0), so no stretch compensation is applied.
CHEST_E = chest_girth + shell_ease
W = CHEST_E / 4.0                      # quarter body width (fold at CB / CF at x=0)
L = body_length
AH = CHEST_E / 8.0 + 108.0             # armhole depth (HPS line to underarm)
AH = max(185.0, min(AH, L - 100.0))
NW = max(66.0, neck_girth / 5.0 + 8.0)  # wider neck: the hood needs room
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 28.0)
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 88.0
BACK_NECK_DROP = 20.0
ZIP_SA = 15.0          # tape allowance on the front center edge (zipper seam)
ZIP_STITCH = 7.0       # stitch line offset from the seam line (zipper-notion)
ZIP_STOP_INSET = 12.0  # stop notches sit this far inside the seam ends


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _body_edges(neck_drop):
    """Half-body outline shared by front and back; center edge at x = 0.

    The `hem` runs the finished hemline; the deep hem casing that carries the
    drawcord is added as a per-edge cut allowance + a marked fold line, not as
    extra outline (a windbreaker hem is a self-casing turned back to the inside).
    """
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


def _hem_casing_marks():
    """Body-hem drawcord casing: an interior fold line the hem turns back on."""
    return fc.Internal(
        "hem drawcord casing fold",
        [fc.P(0.0, hem_casing), fc.P(W, hem_casing)],
        kind="trace",
    )


def _hand_pocket_marks():
    """Slanted hand-warmer pocket opening + bag box on each front half."""
    cx = min(W * 0.55, W - 78.0)
    cy = max(120.0, min(L * 0.30, UNDERARM.y - 110.0))
    half = 78.0                                     # half the opening length
    along = fc.P(0.30, 0.95)                        # near-vertical, top toward CF
    perp = fc.P(0.95, -0.30)                        # bag depth direction
    p_top = fc.P(cx - along.x * half, cy + along.y * half)   # upper (CF side)
    p_bot = fc.P(cx + along.x * half, cy - along.y * half)   # lower (side-seam side)
    opening = fc.Internal("hand pocket opening", [p_top, p_bot], kind="trace")
    e1 = p_top + along * 12.0
    e2 = p_bot - along * 12.0
    corners = [e1 + perp * 22.0, e2 + perp * 22.0, e2 - perp * 22.0, e1 - perp * 22.0]
    box = fc.Internal("hand pocket bag", corners + corners[:1])
    return [opening, box]


def _chest_pocket_marks():
    """A small horizontal chest zip-pocket opening (right front)."""
    cx = W * 0.42
    cy = min(L * 0.62, UNDERARM.y - 20.0)
    half = 55.0
    p_a = fc.P(cx - half, cy)
    p_b = fc.P(cx + half, cy)
    opening = fc.Internal("chest zip pocket opening", [p_a, p_b], kind="trace")
    corners = [fc.P(cx - half - 8.0, cy + 16.0), fc.P(cx + half + 8.0, cy + 16.0),
               fc.P(cx + half + 8.0, cy - 108.0), fc.P(cx - half - 8.0, cy - 108.0)]
    box = fc.Internal("chest pocket bag", corners + corners[:1])
    return [opening, box]


def build_front():
    """Half front, cut 2 mirrored (never on fold): the center edge is the zip seam."""
    zlen = HPS_Y - FRONT_NECK_DROP                 # straight zipper-seam length (CF)
    t_stop = ZIP_STOP_INSET / zlen
    stitch = fc.Internal(
        "zipper stitch line",
        [fc.P(ZIP_STITCH, ZIP_STOP_INSET), fc.P(ZIP_STITCH, zlen - ZIP_STOP_INSET)],
        kind="trace",
    )
    internals = [stitch, _hem_casing_marks()]
    if pockets:
        internals += _hand_pocket_marks()
        internals += _chest_pocket_marks()
    return fc.Piece(
        "front",
        _body_edges(FRONT_NECK_DROP),
        seam_allowance=seam_allowance,
        # Deep hem casing carries the drawcord; the CF edge carries zip tape.
        allowances={"hem": hem_casing, "center": ZIP_SA},
        notches=[
            fc.Notch("side", 0.5), fc.Notch("armhole", 0.5),
            fc.Notch("hem", 0.5, "hem casing / drawcord"),
            fc.Notch("center", 1.0 - t_stop, "zipper top stop"),
            fc.Notch("center", t_stop, "zipper bottom stop"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (zip half)",
    )


def build_back():
    return fc.Piece(
        "back",
        _body_edges(BACK_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": hem_casing},
        notches=[
            fc.Notch("side", 0.5), fc.Notch("armhole", 0.5),
            fc.Notch("hem", 0.5, "hem casing / drawcord"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        internals=[_hem_casing_marks()],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


SLEEVE_EASE = 10.0     # set-in cap ease over the armhole (declared on the seam)


def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12), fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch), fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
    """Set-in sleeve; the cap is solved by bisection to the measured armhole pair.

    A small ease (`SLEEVE_EASE`) is intentionally carried on the cap over the
    armhole (a set-in cap is eased in). It is declared on the seam so the
    balance check accounts for it (delta ≈ 0 against target + ease). The sleeve
    hem gets a deep elastic-casing allowance + a marked fold line (the cuff is a
    self-casing, not a separate rib).
    """
    ch = max(52.0, AH * 0.30)
    sl = max(100.0, sleeve_length - ch)
    goal = cap_target + SLEEVE_EASE
    lo, hi = 20.0, goal / 2.0 + ch + 60.0
    for _ in range(56):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < goal:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - goal) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(95.0, hb * 0.64)
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": cuff_casing},
        notches=[
            fc.Notch("cap", 0.5, "shoulder match"),
            fc.Notch("hem", 0.5, "cuff elastic casing"),
        ],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.5)),
        internals=[fc.Internal("cuff elastic casing fold",
                               [fc.P(-chw, cuff_casing), fc.P(chw, cuff_casing)],
                               kind="trace")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (set-in)",
    )


def _hood_neck_edge(back_x):
    """Hood bottom (neck seam): front-bottom corner to a scaled back-bottom point."""
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(back_x, 35.0), fc.P(back_x * 0.60, -22.0),
                   fc.P(back_x * 0.28, -18.0), fc.P(0.0, 0.0))],
    )


def build_hood(half_opening):
    """Two-panel hood; the neck edge is solved to the half neck opening.

    A drawcord runs the face edge in a marked channel; the packable hood stows
    into the collar area at the neckline (see metadata stowaway_note).
    """
    lo, hi = half_opening * 0.35, half_opening * 1.1
    for _ in range(56):
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
    # Face edge: front-bottom (0,0) up to the crown-front (two straight runs).
    face_mid = fc.P(face_x, hood_height * 0.55)
    edges = [
        _hood_neck_edge(bx),                           # back-bottom → front-bottom
        fc.Edge("face", [fc.Line(fc.P(0.0, 0.0), face_mid),
                         fc.Line(face_mid, top)]),
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
    # Drawcord channel: parallel to the face edge, offset inward by face_channel.
    chan_a = fc.P(0.0 + face_channel, 0.0 + face_channel * 0.2)
    chan_b = fc.P(face_mid.x + face_channel, face_mid.y)
    chan_c = fc.P(top.x + face_channel, top.y - face_channel * 0.2)
    channel = fc.Internal("hood face drawcord channel",
                          [chan_a, chan_b, chan_c], kind="trace")
    return fc.Piece(
        "hood",
        edges,
        seam_allowance=seam_allowance,
        allowances={"face": face_channel},             # face casing carries the drawcord
        notches=[
            fc.Notch("neck", 0.5, "shoulder match"),
            fc.Notch("face", 0.08, "drawcord exit"),
            fc.Notch("face", 0.92, "drawcord exit"),
        ],
        grainline=fc.Grainline(fc.P(hood_depth * 0.45, 80.0),
                               fc.P(hood_depth * 0.45, hood_height * 0.8)),
        internals=[channel],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood (side panel)",
    )


def build():
    pattern = fc.PatternSet("windbreaker")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    # HALF opening = one front-half neck + one back-half neck. One hood panel
    # covers one side of the head, so its neck edge is solved to exactly this.
    half_opening = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    neck_opening = 2.0 * half_opening                  # two fronts + folded back

    everything = target_piece == "set"

    sleeve = build_sleeve(cap_target)
    hood = build_hood(half_opening)

    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "hood":
        pattern.add(hood)

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Front is cut 2 (not on fold), so each PHYSICAL sleeve meets exactly ONE
        # front armhole + ONE back armhole — the drafted pair. Cap carries ease.
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")],
                             tol=2.0, ease=SLEEVE_EASE)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
        # One hood panel's neck edge = the half opening (one front-half neck +
        # one back-half neck); the two panels + cut-2 front make the full ring.
        pattern.declare_seam([("hood", "neck")],
                             [("front", "neck"), ("back", "neck")], tol=2.0)

    # ── Notion / finish accounting (exact-mm factory spec numbers) ────────────
    # Separating zipper: runs the full CF opening (finished, hem casing to neck)
    # plus a little to clear the hem casing. Order to the nearest 10 mm.
    zip_total = front.edge("center").length() + hem_casing
    zipper_len = int(round(zip_total / 10.0) * 10)

    # Body-hem drawcord: total finished hem circumference + tails for the two CF
    # exits + adjustment. Hem circ = 2 x (front hem + back hem).
    hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
    hem_drawcord_len = int(round((hem_circ + 300.0) / 10.0) * 10)  # + ~300 mm tails

    # Cuff elastic: cut per cuff to a recovered circumference (elastic pulls the
    # sleeve hem in). qty is the finished elastic length per cuff (exact mm).
    sleeve_hem = sleeve.edge("hem").length()
    cuff_elastic_each = int(round(sleeve_hem * cuff_ratio))

    # Hood-face drawcord: face edge length + tails for the two exits.
    face_len = hood.edge("face").length()
    hood_drawcord_len = int(round((face_len + 250.0) / 10.0) * 10)

    fabric_width = 1450.0                                # ripstop card width
    body_area = (front.area() * 2.0) + back.area() * 2.0  # front cut 2; back on fold
    trims_area = sleeve.area() * 2.0 + hood.area() * 2.0
    # Crisp woven shell, no nap, nests reasonably tight.
    marker_len = (body_area + trims_area) / (fabric_width * 0.68)

    pattern.bom = [
        {"item": "nylon-ripstop-shell",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"unlined DWR ripstop shell at {fabric_width:.0f} mm width, ~68% "
                 "marker efficiency; wind/water-resistant. Cuts true (no stretch "
                 "compensation); sew with a fine microtex needle so the needle holes "
                 "stay small, and topstitch the self-casings closed"},
        {"item": "separating zipper", "qty": zipper_len, "unit": "mm_length",
         "note": f"order this SEPARATING (open-end) zipper, ~{zipper_len} mm = CF "
                 f"opening + {hem_casing:.0f} mm to clear the hem casing; the front is "
                 "cut 2 with a 15 mm tape allowance, 7 mm stitch line and top/bottom "
                 "stop notches. Slider/pull/teeth HARDWARE is a Yantra4D cartridge "
                 "reference (zipper-notion), not drafted here"},
        {"item": "hem drawcord", "qty": hem_drawcord_len, "unit": "mm_length",
         "note": f"~{hem_drawcord_len} mm elastic drawcord = hem circumference "
                 f"{hem_circ:.0f} mm + ~300 mm tails; threaded through the "
                 f"{hem_casing:.0f} mm self-casing at the body hem (fold line marked), "
                 "exiting at the two CF hem corners"},
        {"item": "hood drawcord", "qty": hood_drawcord_len, "unit": "mm_length",
         "note": f"~{hood_drawcord_len} mm drawcord = hood face {face_len:.0f} mm + "
                 f"~250 mm tails; threaded through the {face_channel:.0f} mm face "
                 "channel of both hood panels, exiting at the two marked drawcord notches"},
        {"item": f"cuff elastic {cuff_casing:.0f} mm casing", "qty": 2, "unit": "pieces",
         "note": f"2 cuff elastics cut {cuff_elastic_each} mm each (sleeve hem "
                 f"{sleeve_hem:.0f} mm x {cuff_ratio:.2f}); joined into a ring and "
                 f"threaded through the {cuff_casing:.0f} mm self-casing at each sleeve "
                 "hem (fold line marked)"},
        {"item": "cord stops", "qty": 4, "unit": "pieces",
         "note": "4 spring cord stops (2 at the hem drawcord exits, 2 at the hood "
                 "drawcord exits) + cord-end tips; HARDWARE is a Yantra4D cartridge "
                 "reference (drawcord-stop / cord-lock), not drafted here"},
        {"item": "polyester thread + bar-tacks", "qty": 1, "unit": "set",
         "note": "all-purpose polyester; bar-tack the pocket mouths and cord-exit "
                 "eyelets; flat-fell or bind the interior seams on an unlined shell to "
                 "keep them from fraying"},
    ]
    if pockets:
        pattern.bom.append(
            {"item": "pocket zips", "qty": 3, "unit": "pieces",
             "note": "1 chest zip (~140 mm) + 2 hand-pocket zips (~160 mm) at the marked "
                     "openings; closed-end. HARDWARE is a Yantra4D cartridge reference "
                     "(zipper-notion), not drafted here"})

    pattern.metadata = {
        "fc100_rank": 62,
        "fabric_hint": "nylon-ripstop-shell",
        "garment_note": "lightweight UNLINED hooded shell jacket — the simplest Wave-J "
                        "technical piece: no insulation, no quilting, relaxed fit over "
                        "layers (shell_ease added to the chest girth)",
        "closure_note": "full-length CENTER-FRONT separating zipper; the front is cut 2 "
                        "(never on fold) with a 15 mm tape allowance, 7 mm stitch line "
                        "and top/bottom stop notches on the center edge",
        "hood_note": "two-panel packable hood; the neck edge is bisection-solved to the "
                     "HALF neck opening (delta approx 0), and a drawcord runs a marked "
                     "channel along the face edge",
        "stowaway_note": "the soft unlined hood rolls and stows into the neckline/collar "
                         "area; add a small zip or snap pocket at the CB neck to hold it "
                         "(marked at assembly, not a separate drafted piece)",
        "finish_note": "SIGNATURE elastic/drawcord finish done as self-fabric casings on "
                       "the shell edges (no rib bands): a drawcord hem casing, elastic "
                       "cuff casings, and a hood-face drawcord channel — all exact-mm in "
                       "the BOM; cord stops via Yantra4D (drawcord-stop cartridge)",
        "weather_note": "DWR-treated wind- and water-resistant ripstop; this is NOT a "
                        "seam-sealed raincoat — the seams are not taped",
        "neck_opening_mm": round(neck_opening, 1),
        "half_opening_solved_mm": round(half_opening, 1),
        "armhole_pair_mm": round(cap_target, 1),
        "sleeve_cap_ease_mm": SLEEVE_EASE,
        "zipper_length_mm": zipper_len,
        "hem_circumference_mm": round(hem_circ, 1),
        "hem_drawcord_length_mm": hem_drawcord_len,
        "hood_drawcord_length_mm": hood_drawcord_len,
        "cuff_elastic_each_mm": cuff_elastic_each,
        "hem_casing_mm": hem_casing,
        "cuff_casing_mm": cuff_casing,
        "face_channel_mm": face_channel,
        "pockets": pockets,
        "drafting": "zip-hoodie / track-jacket block halved at CF for the separating "
                    "zipper; set-in cap solved to the armhole pair (with ease); "
                    "hoodie-pullover two-panel hood solved to the half neck opening; "
                    "teaching-grade — the elastic/drawcord finishes are self-casings "
                    "(allowance + marked fold line + exact-mm BOM), not separate pieces",
    }
    return pattern


result = build()

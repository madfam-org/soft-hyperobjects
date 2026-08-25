"""
Epaulette dress tunic — FC-300 rank #295. Fashion Cabinet Garment Cartridge.

The ceremonial dress tunic: the high-collared, straight-fronted uniform coat
worn by bands, honour guards, cadet corps, ushers and doormen. Its defining
feature is not the collar or the front — it is the SHOULDER BOARD. A rigid
epaulette board sits on each shoulder, carrying rank or unit insignia, and the
tunic is drafted AROUND it: a shoulder tab whose length, wide end and narrow
end are the board's own dimensions, a retaining button at the neck end, and a
seam position that puts the board's outer edge exactly on the shoulder point.

That is what makes this the FC-300 consumer for the Yantra4D `epaulette-board`
solid. `printed-epaulette` (the notion) already bridged the board as a finding;
this cartridge is the first GARMENT that mounts it, and the mapping is
dimensional rather than nominal: `shoulder_len` sizes both the tab drafted here
and the board printed there, so the two cannot drift apart.

Three things solve:

  - THE BOARD SEAT: the tab is drafted to the board's footprint plus turn-under
    on three sides. Its wide end sits at the armhole (where the board is widest)
    and its narrow end at the neck (where the retaining button goes). The seat's
    length is SOLVED against the measured shoulder seam, so a board longer than
    the shoulder is clamped rather than emitted hanging off the garment.
  - THE STAND COLLAR: a high mandarin stand, its neck edge bisected to the
    measured front plus back necklines. A dress tunic's collar is the piece that
    holds the posture; it is solved, not assumed.
  - THE FRONT: a straight closed front with a button ladder whose COUNT is
    derived from the closure run over the pitch. A derived count is exactly the
    value that goes to zero at parameter extremes, so it is clamped.

Hardware: the shoulder boards bridge to Yantra4D `epaulette-board`; the front
buttons and the two board-retaining buttons are drilled marks driven by the same
`board_button_dia` that drives the board's own button boss.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
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
# front|back|sleeve|collar|epaulette_tab|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
tunic_length = float(PARAM(lambda: tunic_length, 760.0))   # nape to hem
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
tunic_ease = float(PARAM(lambda: tunic_ease, 110.0))
collar_height = float(PARAM(lambda: collar_height, 45.0))  # mandarin stand
shoulder_len = float(PARAM(lambda: shoulder_len, 140.0))   # THE board length
board_wide_w = float(PARAM(lambda: board_wide_w, 60.0))    # board width at the armhole
board_narrow_w = float(PARAM(lambda: board_narrow_w, 40.0))  # board width at the neck
board_button_dia = float(PARAM(lambda: board_button_dia, 14.0))  # retaining button
front_buttons_run = float(PARAM(lambda: front_buttons_run, 560.0))
button_pitch = float(PARAM(lambda: button_pitch, 90.0))
cap_ease = float(PARAM(lambda: cap_ease, 22.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps (match the manifest slider bounds exactly) ────────────────────────
chest_girth = max(760.0, min(chest_girth, 1500.0))
tunic_length = max(560.0, min(tunic_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(420.0, min(sleeve_length, 760.0))
tunic_ease = max(70.0, min(tunic_ease, 220.0))
collar_height = max(25.0, min(collar_height, 80.0))
shoulder_len = max(60.0, min(shoulder_len, 260.0))
board_wide_w = max(20.0, min(board_wide_w, 120.0))
board_narrow_w = max(15.0, min(board_narrow_w, 120.0))
board_button_dia = max(8.0, min(board_button_dia, 24.0))
front_buttons_run = max(150.0, min(front_buttons_run, 900.0))
button_pitch = max(45.0, min(button_pitch, 200.0))
cap_ease = max(0.0, min(cap_ease, 40.0))
seam_allowance = max(8.0, min(seam_allowance, 20.0))
hem_allowance = max(25.0, min(hem_allowance, 60.0))

# ── The uniform block ────────────────────────────────────────────────────────
W = (chest_girth + tunic_ease) / 4.0           # quarter body width
L = tunic_length
NW = max(58.0, neck_girth / 5.0 - 4.0)         # half neck width; a tunic neck is close
AH = (chest_girth + tunic_ease) / 8.0 + 105.0
AH = max(175.0, min(AH, L - 230.0))            # chest line well above the hem
HPS_Y = L + 20.0
SHOULDER_DROP = 34.0
BACK_NECK_DROP = 20.0
FRONT_NECK_DROP = 34.0                         # a stand collar sits close at the front
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y
BUTTON_STAND = 20.0

# ── The board seat: SOLVED against the measured shoulder, then clamped ───────
# The shoulder seam runs from the neck point (NW, HPS_Y) to the shoulder end.
# The board must lie ALONG it, so its length cannot exceed that seam. This is a
# DERIVED bound: at extremes (a wide board on a narrow body, or a maximum
# shoulder_len against a minimum chest) the leftover room goes to zero or
# NEGATIVE — and a negative tab length does not fail, it inverts the tab, which
# the kernel's CCW normalization then launders into a valid-LOOKING outline.
_shoulder_span = ((SH_END.x - NW) ** 2 + (SH_END.y - HPS_Y) ** 2) ** 0.5
BOARD_ROOM = max(50.0, _shoulder_span - 10.0)  # leave the seam ends clear
BOARD_LEN = max(50.0, min(shoulder_len, BOARD_ROOM))
BOARD_CLAMPED = shoulder_len > BOARD_ROOM

# The board tapers from its wide end (armhole) to its narrow end (neck). A
# narrow end WIDER than the wide end is not a board, it is a wedge pointing the
# wrong way — so the narrow end is capped at the wide end rather than silently
# producing an inverted taper.
BOARD_WIDE = board_wide_w
BOARD_NARROW = min(board_narrow_w, BOARD_WIDE)
TAPER_CLAMPED = board_narrow_w > BOARD_WIDE

# ── The front button ladder: a DERIVED count, therefore clamped ──────────────
_run_room = max(120.0, HPS_Y - FRONT_NECK_DROP - 60.0)
BUTTON_RUN = max(120.0, min(front_buttons_run, _run_room))
RUN_CLAMPED = front_buttons_run > _run_room
BUTTON_COUNT = int(max(2.0, min(BUTTON_RUN / button_pitch, 14.0)))


def _cross(label, x, y, half=5.0):
    """Drill cross-mark as two internals (the commons' buttonhole convention)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


def _solve_flat(edge_fn, target, what):
    """Bisect a monotonic flat-length -> measured-curve-length edge builder."""
    lo, hi = target * 0.55, target * 1.15
    for _ in range(52):
        mid = (lo + hi) / 2.0
        if edge_fn(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(edge_fn(flat).length(0.05) - target) > 1.0:
        raise ValueError(f"{what} solver did not converge on {target:.1f} mm")
    return flat


def _board_seat_marks(prefix):
    """The board's footprint, drawn ON the shoulder of the panel that carries it.

    This is what makes the tunic a CONSUMER of the epaulette-board rather than a
    garment that merely mentions one: the marked seat is the board's own
    outline, positioned so its WIDE end sits at the shoulder point (where the
    board is widest and the shoulder is broadest) and its NARROW end at the neck
    point, with the retaining-button drill exactly at the narrow end.
    """
    # Unit vector along the shoulder seam, neck point → shoulder end.
    dx, dy = SH_END.x - NW, SH_END.y - HPS_Y
    ln = max(1.0, (dx * dx + dy * dy) ** 0.5)
    ux, uy = dx / ln, dy / ln
    px, py = -uy, ux                            # perpendicular, into the body
    # Start the board a little in from the neck point so the tab root is caught
    # in the collar seam, and run it BOARD_LEN toward the shoulder end.
    inset = 6.0
    ax, ay = NW + ux * inset, HPS_Y + uy * inset
    bx, by = ax + ux * BOARD_LEN, ay + uy * BOARD_LEN
    hn, hw = BOARD_NARROW / 2.0, BOARD_WIDE / 2.0
    outline = [
        fc.P(ax + px * hn, ay + py * hn),
        fc.P(bx + px * hw, by + py * hw),
        fc.P(bx - px * hw, by - py * hw),
        fc.P(ax - px * hn, ay - py * hn),
        fc.P(ax + px * hn, ay + py * hn),
    ]
    marks = [fc.Internal(f"{prefix} board seat", outline, kind="marking")]
    marks += _cross(f"{prefix} board button", ax, ay, half=board_button_dia / 2.0)
    return marks


def build_front():
    """Front (cut 2, mirrored): a straight closed uniform front with a button
    stand, a shallow neckline for the stand collar, and the front half of the
    board seat marked on the shoulder."""
    neck_top = HPS_Y - FRONT_NECK_DROP
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, neck_top)],
                    kind="marking"),
    ]
    internals += _board_seat_marks("front")
    for i in range(BUTTON_COUNT):
        y = neck_top - (i + 0.5) * (BUTTON_RUN / BUTTON_COUNT)
        internals += _cross(f"buttonhole-{i + 1}", 0.0, y)
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front",
                    [fc.Line(fc.P(-BUTTON_STAND, 0.0),
                             fc.P(-BUTTON_STAND, neck_top))]),
            fc.Edge("neck", [fc.Bezier(
                fc.P(-BUTTON_STAND, neck_top), fc.P(NW * 0.5, neck_top),
                fc.P(NW, neck_top + FRONT_NECK_DROP * 0.4), fc.P(NW, HPS_Y))]),
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            fc.Edge("armhole", [fc.Bezier(
                SH_END, fc.P(SH_END.x - 20.0, SH_END.y - AH * 0.40),
                fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)]),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-BUTTON_STAND, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center_front": seam_allowance * 2.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder match"),
                 fc.Notch("armhole", 0.5, "front armhole"),
                 fc.Notch("side", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.55, 70.0), fc.P(W * 0.55, CHEST_Y - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Back (cut 1 on the centre-back fold), with the back half of the board seat
    marked on the shoulder so front and back tab positions agree."""
    nape = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
    internals = _board_seat_marks("back")
    internals.append(fc.Internal(
        "back vent", [fc.P(0.0, 0.0), fc.P(0.0, min(220.0, L * 0.3))],
        kind="marking"))
    return fc.Piece(
        "back",
        [
            fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), nape)]),
            fc.Edge("neck", [fc.Bezier(
                nape, fc.P(NW * 0.55, nape.y),
                fc.P(NW, nape.y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))]),
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            fc.Edge("armhole", [fc.Bezier(
                SH_END, fc.P(SH_END.x - 16.0, SH_END.y - AH * 0.38),
                fc.P(W - 4.0, UNDERARM.y + AH * 0.28), UNDERARM)]),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.5, "shoulder match"),
                 fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("side", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.5, 70.0), fc.P(W * 0.5, CHEST_Y - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back",
                       mirror=True),
        label="Back (on fold)",
    )


def build_epaulette_tab():
    """THE PIECE THAT CONSUMES THE BOARD (cut 2, mirrored).

    The fabric tab that covers the rigid Yantra4D `epaulette-board` and is sewn
    into the shoulder seam at its wide end and buttoned at its narrow end. It is
    drafted to the board's footprint plus turn-under on three sides, tapering
    from BOARD_WIDE at the armhole to BOARD_NARROW at the neck.

    The dimensions here and the printed board's are the SAME parameters
    (`shoulder_len`, `board_wide_w`, `board_narrow_w`, `board_button_dia` via
    notion.hardware_ref.params_map), so the sleeve of cloth and the board inside
    it cannot drift apart.
    """
    turn = seam_allowance                       # turn-under on the three free sides
    ln = BOARD_LEN + turn                       # extra at the seam end
    hw = BOARD_WIDE / 2.0 + turn
    hn = BOARD_NARROW / 2.0 + turn
    # Frame: x = 0 at the neck (narrow) end, x = ln at the armhole (wide) end.
    # The board's OWN outline inside the turn-under: this is the line the rigid
    # board must land on, so the maker can see the cloth's grip on it.
    internals = [
        fc.Internal("board outline", [
            fc.P(turn, BOARD_NARROW / 2.0),
            fc.P(turn + BOARD_LEN, BOARD_WIDE / 2.0),
            fc.P(turn + BOARD_LEN, -BOARD_WIDE / 2.0),
            fc.P(turn, -BOARD_NARROW / 2.0),
            fc.P(turn, BOARD_NARROW / 2.0),
        ], kind="marking"),
        fc.Internal("fold line", [fc.P(0.0, 0.0), fc.P(ln, 0.0)], kind="marking"),
    ]
    internals += _cross("board button", turn + board_button_dia,
                        0.0, half=board_button_dia / 2.0)
    return fc.Piece(
        "epaulette_tab",
        [
            fc.Edge("neck_end", [fc.Line(fc.P(0.0, -hn), fc.P(0.0, hn))]),
            fc.Edge("upper", [fc.Line(fc.P(0.0, hn), fc.P(ln, hw))]),
            fc.Edge("shoulder_seam", [fc.Line(fc.P(ln, hw), fc.P(ln, -hw))]),
            fc.Edge("lower", [fc.Line(fc.P(ln, -hw), fc.P(0.0, -hn))]),
        ],
        seam_allowance=0.0,                     # turn-under already in the outline
        notches=[fc.Notch("shoulder_seam", 0.5, "shoulder seam match")],
        grainline=fc.Grainline(fc.P(ln * 0.2, 0.0), fc.P(ln * 0.8, 0.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Epaulette tab (over the board)",
    )


def _collar_neck(flat):
    return fc.Edge("neck", [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, 10.0),
                                             bulge=0.06, side=-1.0)])


def build_collar(neck_target):
    """The mandarin stand, half on the CB fold. Its neck edge is bisected to the
    measured front plus back necklines — on a dress tunic the collar is the
    piece that holds the posture, so it is solved rather than assumed."""
    flat = _solve_flat(_collar_neck, neck_target, "stand-collar neck")
    d = collar_height
    return fc.Piece(
        "collar",
        [
            _collar_neck(flat),
            fc.Edge("front_edge", [fc.Line(fc.P(flat, 10.0), fc.P(flat, 10.0 + d))]),
            fc.Edge("top", [fc.curve_through(fc.P(flat, 10.0 + d), fc.P(0.0, d),
                                             bulge=0.03, side=1.0)]),
            fc.Edge("cb", [fc.Line(fc.P(0.0, d), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder seam match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, d / 2.0), fc.P(flat * 0.8, d / 2.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Stand collar (half, on fold)",
    )


def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.66, sl + ch * 0.12),
                  fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                  fc.P(-hb * 0.66, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(arm_target):
    """A one-piece set-in sleeve with a cuff-button drill. Its cap is bisected to
    the measured front + back armholes plus the declared cap ease."""
    cap_target = arm_target + cap_ease
    ch = max(66.0, AH * 0.31)
    sl = max(200.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    for _ in range(52):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(95.0, min(hb * 0.60, hb - 10.0))
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.curve_through(
                fc.P(chw, 0.0), fc.P(hb, sl), bulge=0.03, side=-1.0)]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.curve_through(
                fc.P(-hb, sl), fc.P(-chw, 0.0), bulge=0.03, side=-1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", (arm_target * 0.55 + cap_ease / 2.0) / cap_target,
                          "cap back match"),
                 fc.Notch("hem", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.8)),
        internals=_cross("cuff button", chw - 30.0, 30.0,
                         half=board_button_dia / 2.0),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build():
    pattern = fc.PatternSet("epaulette-dress-tunic")
    front = build_front()
    back = build_back()
    arm_target = (front.edge("armhole").length(0.05)
                  + back.edge("armhole").length(0.05))
    neck_target = (front.edge("neck").length(0.05)
                   + back.edge("neck").length(0.05))

    names = ("front", "back", "sleeve", "collar", "epaulette_tab")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(arm_target))
    if wanted["collar"]:
        pattern.add(build_collar(neck_target))
    if wanted["epaulette_tab"]:
        pattern.add(build_epaulette_tab())

    # ── Declared seams ───────────────────────────────────────────────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")],
                             ease=cap_ease, tol=2.5)
    if wanted["sleeve"]:
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front", "neck"), ("back", "neck")], tol=1.5)
    # THE BOARD SEAM: the tab's wide end is caught in the shoulder seam. The
    # shoulder is longer than the tab is wide (the tab sits on it, it does not
    # replace it), so that surplus is declared as honest ease rather than hidden
    # behind a loosened tolerance.
    if wanted["epaulette_tab"] and wanted["front"]:
        sh = front.edge("shoulder").length(0.05)
        tab = pattern.piece("epaulette_tab").edge("shoulder_seam").length(0.05)
        pattern.declare_seam(("front", "shoulder"),
                             ("epaulette_tab", "shoulder_seam"),
                             tol=1.0, ease=sh - tab)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1500.0                       # lana-peinada-traje card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "lana-peinada-traje", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"worsted at {fabric_width:.0f} mm width, 60% marker. A dress "
                 "tunic is pressed hard and often; pre-shrink by steaming"},
        {"item": "epaulette board", "qty": 2, "unit": "pcs",
         "note": f"Yantra4D epaulette-board, {BOARD_LEN:.0f} mm long, "
                 f"{BOARD_WIDE:.0f} mm at the armhole tapering to "
                 f"{BOARD_NARROW:.0f} mm at the neck (see "
                 "notion.hardware_ref). The tab is drafted to this footprint "
                 "plus turn-under, so board and sleeve cannot drift apart"},
        {"item": f"retaining button {board_button_dia:.0f} mm", "qty": 2,
         "unit": "pcs",
         "note": "one per shoulder, at the board's narrow end; the same "
                 "diameter drives the board's own button boss"},
        {"item": "front buttons", "qty": BUTTON_COUNT, "unit": "pcs",
         "note": "the count is DERIVED from the closure run over the pitch and "
                 "clamped to 2-14"},
        {"item": "fusible interfacing (fronts, collar stand, tabs)", "qty": 1,
         "unit": "set",
         "note": "the stand collar and the epaulette tabs both need a firm hand "
                 "or the board reads through the cloth as a ripple"},
        {"item": "thread + buttonhole twist", "qty": 1, "unit": "set",
         "note": "uniform buttonholes are worked to a visible standard"},
    ]
    pattern.metadata = {
        "fc300_rank": 295,
        "family": "workwear_uniforms",
        "fabric_hint": "lana-peinada-traje",
        "signature": "the SHOULDER BOARD: the tunic is drafted around a rigid "
                     "Yantra4D epaulette-board, with a tab sized to the board's "
                     "own footprint, a seat marked on both shoulders and a "
                     "retaining button at the narrow end",
        "consumes": "yantra4d/epaulette-board — this is the first GARMENT in "
                    "the commons that mounts the board; `printed-epaulette` "
                    "bridged it as a notion, this one wears it",
        "finished_mm": {"length": round(tunic_length, 1),
                        "chest_drafted": round(chest_girth + tunic_ease, 1),
                        "collar_stand": round(collar_height, 1)},
        "solved": {
            "shoulder_span_mm": round(_shoulder_span, 2),
            "board_room_mm": round(BOARD_ROOM, 2),
            "board_len_mm": round(BOARD_LEN, 2),
            "board_wide_mm": round(BOARD_WIDE, 2),
            "board_narrow_mm": round(BOARD_NARROW, 2),
            "neck_target_mm": round(neck_target, 2),
            "armhole_target_mm": round(arm_target, 2),
            "button_run_mm": round(BUTTON_RUN, 2),
            "button_count": BUTTON_COUNT,
            "board_clamped": BOARD_CLAMPED,
            "taper_clamped": TAPER_CLAMPED,
            "button_run_clamped": RUN_CLAMPED,
            "note": "the board's length is bounded by the MEASURED shoulder "
                    "seam, its narrow end by its wide end, and the button count "
                    "by the closure run — all three are DERIVED, and a derived "
                    "dimension that goes negative does not fail, it inverts the "
                    "piece into geometry the kernel's CCW normalization "
                    "launders into a valid-LOOKING outline",
        },
        "hardware": "shoulder boards via Yantra4D (notion.hardware_ref -> "
                    "epaulette-board); shoulder_len, board_wide_w and "
                    "board_narrow_w size the printed board AND the fabric tab "
                    "drafted here, and board_button_dia drives both the board's "
                    "button boss and the drilled retaining mark",
        "scope": "no insignia, rank marks, braid or piping are drafted — those "
                 "are organisation-specific and a default would be an invention",
    }
    return pattern


result = build()

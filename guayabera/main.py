"""
Guayabera — FC-100 rank #96. Fashion Cabinet Garment Cartridge.

The guayabera is a Latin American / Mexican men's dress shirt — a formal-casual
garment of real cultural significance, worn UNTUCKED over a straight hem with
side vents. This cartridge encodes its four defining features honestly and
respectfully:

  - BUTTON PLACKET + TURNDOWN COLLAR: a drop-shoulder woven shirt block with the
    front center edge extended `button_stand` past CF as a folded button
    placket (seven buttonhole cross-marks on the CF line), and a proper
    two-piece turndown collar — a STAND solved by bisection to the measured
    neckline (collar-band method) and a FALL solved to the stand's own measured
    top edge (the chained multi-solve inherited from the dress shirt, rank #4).
    Worn buttoned to the throat like a shirt.

  - ALFORZAS (the signature, the heart of the garment): the vertical rows of
    fine PINTUCKS that decorate a guayabera. Modelled as fc.Internal(kind=
    "trace") vertical lines driven by a `pintuck_rows` parameter — TWO columns
    of `pintuck_rows` fine tucks on EACH front (flanking the pockets), THREE
    columns down the back, and a matching column on each pocket. This is the
    decoration that makes a guayabera a guayabera.

  - FOUR PATCH POCKETS (the signature): the classic guayabera carries four
    pockets — two chest + two lower/hip — each with its own alforza column and
    a button. Drafted here as TWO real patch-pocket pieces: a chest pocket
    (cut 2) and a larger hip pocket (cut 2), four pockets in all. Their
    placements are traced on the front, and their pintuck columns align with
    the front alforzas.

  - SIDE VENTS worn untucked: a straight hem, a slightly LONGER back (`back_drop`
    below the front hem), and side vents (`vent_height`) topped by a small
    button TAB — the classic guayabera side slit. The tab is a real cut piece.

Simplifications (docs/README.md, teaching-grade): the full back armhole is kept
equal to the front armhole on this drop-shoulder block (real tailored guayaberas
split a smaller back armhole across a yoke); the alforzas and side vents are
drafted as placement traces/markings, not as consumed tuck fabric (real tucks
eat width — see the note); the longer back is a straight hem step at the side
seam. The collar is a standard turndown; some guayaberas use a camp collar.

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
# front|back|sleeve|stand|fall|chest_pocket|hip_pocket|vent_tab|set
sleeve = str(PARAM(lambda: sleeve, "long"))            # long | short

chest_girth    = float(PARAM(lambda: chest_girth, 1080.0))
body_length    = float(PARAM(lambda: body_length, 760.0))    # nape to front hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 620.0))  # shoulder to wrist/hem
woven_ease     = float(PARAM(lambda: woven_ease, 180.0))     # total; relaxed fit
button_stand   = float(PARAM(lambda: button_stand, 32.0))    # front edge past CF
pintuck_rows   = int(PARAM(lambda: pintuck_rows, 5))         # tucks per alforza column
back_drop      = float(PARAM(lambda: back_drop, 40.0))       # back hem below front
vent_height    = float(PARAM(lambda: vent_height, 120.0))    # side-vent slit height
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(500.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(100.0, min(sleeve_length, 720.0))
woven_ease = max(80.0, min(woven_ease, 400.0))
button_stand = max(20.0, min(button_stand, 50.0))
pintuck_rows = max(2, min(pintuck_rows, 7))
back_drop = max(0.0, min(back_drop, 90.0))
vent_height = max(40.0, min(vent_height, 220.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 50.0))

# ── Drop-shoulder woven shirt block (woven-tops family, shirt neckline) ──────
W = (chest_girth + woven_ease) / 4.0           # quarter body width
L = body_length
AH = (chest_girth + woven_ease) / 8.0 + 95.0   # drop-shoulder armhole depth
AH = max(160.0, min(AH, L - 120.0))
NW = max(60.0, neck_girth / 5.0)               # half neck width at HPS
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 20.0
FRONT_NECK_DROP = max(70.0, neck_girth / 5.0 + 10.0)   # buttons to the throat
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
CB_NECK_Y = HPS_Y - BACK_NECK_DROP
OVERLAP = 15.0                                 # collar stand end past CF (button line)
STAND_H, STAND_RISE = 30.0, 12.0               # collar stand geometry (dress-shirt)
FALL_H, FALL_RISE, FALL_POINT = 58.0, 10.0, 42.0   # collar fall geometry
BUTTONS = 7                                    # front buttons (classic count)

# Alforza pintuck geometry ---------------------------------------------------
TUCK_GAP = 7.0                                 # spacing between tucks in a column
FRONT_COLS = 2                                 # alforza columns per front panel
BACK_COLS = 3                                  # alforza columns down the back

# Pocket geometry (real cut pieces) ------------------------------------------
CHEST_W, CHEST_H = 120.0, 130.0
HIP_W, HIP_H = 165.0, 175.0
POCKET_BTN_INSET = 20.0                        # button drop from pocket top

SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)


# ── Shared block edges ───────────────────────────────────────────────────────
def _armhole_edge():
    """Shared front/back armhole (drop-shoulder shirts keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _front_neck_edge():
    """Front neck: OVERLAP straight run past CF (the button line where the
    collar stand ends), then the scoop up to HPS.

    Including the straight run makes the per-half seam check
    stand.neck == front.neck + back.neck close exactly: the front is cut 2 (its
    neck appears once per garment half), the on-fold back contributes its half.
    """
    cf = fc.P(0.0, CF_NECK_Y)
    scoop = fc.Bezier(cf, fc.P(NW * 0.55, CF_NECK_Y),
                      fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))
    return fc.Edge("neck", [fc.Line(fc.P(-OVERLAP, CF_NECK_Y), cf), scoop])


# ── Alforza pintuck columns (fc.Internal traces) ─────────────────────────────
def _alforza_column(label, cx, y_top, y_bottom, rows):
    """One alforza = a column of `rows` fine vertical pintuck traces `TUCK_GAP`
    apart, centred on cx. Each tuck is a two-point vertical trace line."""
    marks = []
    span = (rows - 1) * TUCK_GAP
    x0 = cx - span / 2.0
    for i in range(rows):
        x = x0 + i * TUCK_GAP
        marks.append(fc.Internal(
            f"{label} tuck {i + 1}",
            [fc.P(x, y_top), fc.P(x, y_bottom)],
            kind="trace",
        ))
    return marks


def _buttonhole_marks():
    """Seven cross-marks on the CF line (x = 0), evenly spaced down the placket."""
    top = CF_NECK_Y - 55.0
    bottom = max(150.0, top - 520.0)
    arm = 4.0
    marks = []
    for i in range(BUTTONS):
        y = top - (top - bottom) * i / (BUTTONS - 1.0)
        marks.append(fc.Internal(
            f"buttonhole {i + 1}",
            [fc.P(-arm, y), fc.P(arm, y), fc.P(0.0, y),
             fc.P(0.0, y - arm), fc.P(0.0, y + arm)],
            kind="drill",
        ))
    return marks


def _front_pocket_traces():
    """Placement traces for this front's chest + hip patch pockets.

    Pockets sit on the outer half of the front (wearer's side once mirrored),
    OUTBOARD of the inner alforza column so the two decorations read as the
    classic guayabera stack: alforzas flank the pocket, pocket carries its own
    tuck column. Returns (traces, chest_cx, hip_cx) so the alforza columns can
    be placed relative to the pockets.
    """
    chest_top = min(UNDERARM.y + 55.0, CF_NECK_Y - 30.0)
    chest_bottom = chest_top - CHEST_H
    hip_top = max(chest_bottom - 90.0, 55.0 + HIP_H)
    hip_bottom = hip_top - HIP_H
    # Centre the pockets on the outer half of the panel.
    chest_cx = W * 0.60
    chest_left = chest_cx - CHEST_W / 2.0
    chest_right = chest_cx + CHEST_W / 2.0
    hip_cx = W * 0.58
    hip_left = hip_cx - HIP_W / 2.0
    hip_right = hip_cx + HIP_W / 2.0
    traces = [
        fc.Internal("chest pocket placement",
                    [fc.P(chest_left, chest_top), fc.P(chest_right, chest_top),
                     fc.P(chest_right, chest_bottom), fc.P(chest_left, chest_bottom),
                     fc.P(chest_left, chest_top)], kind="trace"),
        fc.Internal("hip pocket placement",
                    [fc.P(hip_left, hip_top), fc.P(hip_right, hip_top),
                     fc.P(hip_right, hip_bottom), fc.P(hip_left, hip_bottom),
                     fc.P(hip_left, hip_top)], kind="trace"),
    ]
    return traces, chest_cx, hip_cx, chest_top, chest_bottom, hip_top, hip_bottom


def _vent_mark(side_x):
    """Side-vent slit marking on the side seam, above the front hem."""
    return fc.Internal(
        "side vent",
        [fc.P(side_x, 0.0), fc.P(side_x, vent_height),
         fc.P(side_x - 8.0, vent_height)],
        kind="marking",
    )


# ── Front ────────────────────────────────────────────────────────────────────
def build_front():
    """Front, cut 2 mirrored: center edge extended button_stand past CF, with
    two alforza columns flanking the pocket stack and the pocket placements."""
    neck = _front_neck_edge()
    cf_t = max(0.02, min(0.5, OVERLAP / neck.length(0.05)))
    (pocket_traces, chest_cx, hip_cx,
     chest_top, chest_bottom, hip_top, hip_bottom) = _front_pocket_traces()

    # Alforza columns: the guayabera front carries two vertical tuck columns
    # per side. Place one INBOARD of the pocket stack (toward CF) and one
    # OUTBOARD (toward the side seam), flanking the pockets top-to-hem.
    alf_top = CF_NECK_Y - 40.0
    alf_bottom = 60.0
    inner_cx = min(chest_cx, hip_cx) - max(CHEST_W, HIP_W) / 2.0 - 22.0
    inner_cx = max(inner_cx, button_stand + 30.0)
    outer_cx = max(chest_cx + CHEST_W / 2.0, hip_cx + HIP_W / 2.0) + 22.0
    outer_cx = min(outer_cx, W - 25.0)
    alforzas = (
        _alforza_column("alforza inner", inner_cx, alf_top, alf_bottom, pintuck_rows)
        + _alforza_column("alforza outer", outer_cx, alf_top, alf_bottom, pintuck_rows)
    )

    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, CF_NECK_Y)],
                    kind="marking"),
        *_buttonhole_marks(),
        *alforzas,
        *pocket_traces,
        _vent_mark(W),
    ]
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-button_stand, 0.0),
                                       fc.P(-button_stand, CF_NECK_Y))]),
            fc.Edge("stand_top", [fc.Line(fc.P(-button_stand, CF_NECK_Y),
                                          fc.P(-OVERLAP, CF_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-button_stand, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole"),
                 fc.Notch("neck", cf_t, "CF / collar end")],
        grainline=fc.Grainline(fc.P(W * 0.60, 80.0), fc.P(W * 0.60, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


# ── Back ─────────────────────────────────────────────────────────────────────
def build_back():
    """Back, cut 1 on fold at CB. Straight boxy body, a longer back hem that
    dips to `back_drop` below the front hemline at CB (the guayabera's slightly
    longer back / shirt-tail step), a side vent mark, and THREE alforza columns
    evenly spaced across the half-back.

    The side edge still ends at (W, 0), exactly matching the front side seam so
    the seam check closes at delta 0; only the HEM edge shapes down toward CB,
    holding level near the vent so the vent tops align, then dropping to
    (0, -back_drop) at the fold.
    """
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, CB_NECK_Y), fc.P(NW * 0.55, CB_NECK_Y),
                   fc.P(NW, CB_NECK_Y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    # Shaped longer-back hem: level at the side seam (so front/back vents meet),
    # curving down to -back_drop at the CB fold. A single gentle Bézier.
    hem = fc.Edge(
        "hem",
        [fc.Bezier(fc.P(W, 0.0), fc.P(W * 0.62, 0.0),
                   fc.P(W * 0.34, -back_drop), fc.P(0.0, -back_drop))],
    )
    # Three alforza columns across the half-back, centred and evenly spread.
    alf_top = CB_NECK_Y - 60.0
    alf_bottom = 70.0
    back_cols = []
    for i in range(BACK_COLS):
        # spread columns over the central 60% of the half-back
        frac = 0.20 + 0.60 * (i / (BACK_COLS - 1.0))
        cx = W * frac
        back_cols += _alforza_column(f"back alforza {i + 1}", cx,
                                     alf_top, alf_bottom, pintuck_rows)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, -back_drop), fc.P(0.0, CB_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            hem,
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(W * 0.60, 80.0), fc.P(W * 0.60, L - 120.0)),
        internals=[_vent_mark(W), *back_cols],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


# ── Sleeve (short or long select) ────────────────────────────────────────────
def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    """Set-flat sleeve; cap solved by bisection to the front + back armholes at
    zero ease. `sleeve` select drives short (turn-up hem) vs long (deep hem)."""
    is_short = sleeve == "short"
    length = 230.0 if is_short else sleeve_length
    ch = max(45.0, AH * 0.33)                       # shallow relaxed cap
    sl = max(55.0, length - ch)                     # underarm-to-hem length
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(48):                             # cap length grows with hb
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs {cap_target:.1f}"
        )
    chw = max(80.0, hb * (0.82 if is_short else 0.74))   # opening half-width
    fold = fc.Internal("turn-up cuff fold",
                       [fc.P(-chw, hem_allowance + 18.0),
                        fc.P(chw, hem_allowance + 18.0)], kind="marking")
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
        grainline=fc.Grainline(fc.P(0.0, 25.0), fc.P(0.0, sl + ch * 0.6)),
        internals=[fold] if is_short else [],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (short)" if is_short else "Sleeve (long)",
    )


# ── Collar stand + fall (chained bisection solve, from the dress shirt) ───────
def _stand_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, STAND_RISE),
                          bulge=0.05, side=-1.0)],
    )


def _solve_flat(edge_fn, target, what):
    """Bisect a monotonic flat-length → measured-curve-length edge builder."""
    lo, hi = target * 0.7, target * 1.05
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if edge_fn(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(edge_fn(flat).length(0.05) - target) > 1.0:
        raise ValueError(f"{what} solver did not converge on {target:.1f} mm")
    return flat


def build_stand(half_neck):
    """Collar stand, half on fold at CB (collar-band method): neck edge solved
    by bisection to the half neckline + button overlap."""
    target = half_neck + OVERLAP
    flat = _solve_flat(_stand_neck, target, "collar-stand neck")
    neck = _stand_neck(flat)
    top_start = fc.P(0.0, STAND_H)
    top_end = fc.P(flat, STAND_RISE + STAND_H)
    t_cf = half_neck / target                       # CF button line along the neck
    return fc.Piece(
        "stand",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, STAND_RISE), top_end)]),
            fc.Edge("top",
                    [fc.curve_through(top_end, top_start, bulge=0.05, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match"),
                 fc.Notch("neck", t_cf, "CF / button line")],
        grainline=fc.Grainline(fc.P(flat * 0.2, STAND_H * 0.5),
                               fc.P(flat * 0.75, STAND_H * 0.5 + STAND_RISE * 0.7)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Collar Stand (half, on fold)",
    )


def _fall_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, FALL_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_fall(stand_top_len):
    """Collar fall, half on fold: neck edge solved to the stand's measured TOP
    edge — the second solve, chained off the first. Pointed front."""
    flat = _solve_flat(_fall_neck, stand_top_len, "collar-fall neck")
    neck = _fall_neck(flat)
    point = fc.P(flat + FALL_POINT, FALL_RISE + FALL_H)
    return fc.Piece(
        "fall",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, FALL_RISE), point)]),
            fc.Edge("top",
                    [fc.curve_through(point, fc.P(0.0, FALL_H),
                                      bulge=0.03, side=1.0)]),
            fc.Edge("cb", [fc.Line(fc.P(0.0, FALL_H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "stand match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, FALL_H * 0.55),
                               fc.P(flat * 0.7, FALL_H * 0.55)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Collar Fall (half, on fold)",
    )


# ── Patch pockets (real cut pieces; cut 2 each → four pockets) ───────────────
def _patch_pocket(name, w, h, label, quantity):
    """A guayabera patch pocket: rectangle with a shallow angled bottom point,
    its own alforza column of `pintuck_rows` tucks, and a button mark. The top
    edge is the opening (folds to a facing); the button sits below the top."""
    flap = 20.0                                     # angled bottom-point drop
    tuck_top = h - 26.0
    tuck_bottom = flap + 18.0
    internals = [
        fc.Internal("fold line (top facing)",
                    [fc.P(0.0, h - hem_allowance - 12.0),
                     fc.P(w, h - hem_allowance - 12.0)], kind="marking"),
        *_alforza_column(f"{name} alforza", w / 2.0, tuck_top, tuck_bottom,
                         pintuck_rows),
        fc.Internal("pocket button",
                    [fc.P(w / 2.0 - 4.0, h - POCKET_BTN_INSET),
                     fc.P(w / 2.0 + 4.0, h - POCKET_BTN_INSET),
                     fc.P(w / 2.0, h - POCKET_BTN_INSET - 4.0),
                     fc.P(w / 2.0, h - POCKET_BTN_INSET + 4.0)], kind="drill"),
    ]
    return fc.Piece(
        name,
        [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, flap))]),
            fc.Edge("point_r", [fc.Line(fc.P(w, flap), fc.P(w / 2.0, 0.0))]),
            fc.Edge("point_l", [fc.Line(fc.P(w / 2.0, 0.0), fc.P(0.0, flap))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, flap), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance},             # top hem folds inside
        grainline=fc.Grainline(fc.P(w * 0.5, 25.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def build_chest_pocket():
    return _patch_pocket("chest_pocket", CHEST_W, CHEST_H,
                         "Chest Pocket (cut 2)", 2)


def build_hip_pocket():
    return _patch_pocket("hip_pocket", HIP_W, HIP_H,
                         "Hip Pocket (cut 2)", 2)


# ── Side-vent button tab (real small cut piece) ──────────────────────────────
def build_vent_tab():
    """Small rectangular button tab that closes the top of each side vent — the
    classic guayabera side-slit detail. Cut 2 (one per side); has a buttonhole
    at the free end and an attach trace at the fixed end."""
    tw, th = 30.0, 70.0
    return fc.Piece(
        "vent_tab",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(tw, 0.0))]),
            fc.Edge("right", [fc.Line(fc.P(tw, 0.0), fc.P(tw, th))]),
            fc.Edge("top", [fc.Line(fc.P(tw, th), fc.P(0.0, th))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, th), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(tw * 0.5, 12.0), fc.P(tw * 0.5, th - 12.0)),
        internals=[
            fc.Internal("tab buttonhole",
                        [fc.P(tw / 2.0 - 4.0, th - 14.0),
                         fc.P(tw / 2.0 + 4.0, th - 14.0),
                         fc.P(tw / 2.0, th - 18.0),
                         fc.P(tw / 2.0, th - 10.0)], kind="drill"),
            fc.Internal("attach line (to back vent)",
                        [fc.P(0.0, 14.0), fc.P(tw, 14.0)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Vent Tab (cut 2)",
    )


# ── Assembly ─────────────────────────────────────────────────────────────────
def build():
    pattern = fc.PatternSet("guayabera")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    half_neck = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    stand = build_stand(half_neck)
    stand_top_len = stand.edge("top").length(0.05)

    names = ("front", "back", "sleeve", "stand", "fall",
             "chest_pocket", "hip_pocket", "vent_tab")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    if wanted["stand"]:
        pattern.add(stand)
    if wanted["fall"]:
        pattern.add(build_fall(stand_top_len))
    if wanted["chest_pocket"]:
        pattern.add(build_chest_pocket())
    if wanted["hip_pocket"]:
        pattern.add(build_hip_pocket())
    if wanted["vent_tab"]:
        pattern.add(build_vent_tab())

    # ── Seams (all delta ≈ 0) ────────────────────────────────────────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
    if wanted["stand"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("stand", "neck")],
                             [("front", "neck"), ("back", "neck")],
                             tol=2.0, ease=OVERLAP)
    if wanted["fall"] and wanted["stand"]:
        pattern.declare_seam([("fall", "neck")], [("stand", "top")], tol=2.0)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1450.0                            # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.60)  # allow for alforza take-up
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"crisp cotton poplin at {fabric_width:.0f} mm width, 60% marker "
                 "efficiency; add ~5-8% for the alforza (pintuck) take-up, which "
                 "consumes real width per tuck; manta-cruda is the linen-look "
                 "alternative"},
        {"item": "fusible interfacing (collar stand + fall + button placket)",
         "qty": 1, "unit": "set",
         "note": "shirt-weight; stand and fall cut doubled on fold, placket fused "
                 "full length"},
        {"item": "shirt buttons Ø 11.5 mm", "qty": BUTTONS + 4 + 2 + 1,
         "unit": "pieces",
         "note": f"{BUTTONS} front + 4 pockets + 2 side-vent tabs + 1 collar stand; "
                 "hard goods federate to the Yantra4D button family (shank-button "
                 "cartridge), never re-implemented here"},
        {"item": "polyester/cotton thread + universal needle", "qty": 1,
         "unit": "set",
         "note": "sharp 80/12 for poplin; a twin needle or pintuck foot forms the "
                 "alforzas (the fine parallel tucks) evenly"},
    ]

    # ── Metadata (all solved dims + respectful heritage note) ────────────────
    pattern.metadata = {
        "fc100_rank": 96,
        "fabric_hint": "popelina-algodon",
        "heritage": (
            "The guayabera is a Latin American / Mexican men's dress shirt of "
            "real cultural significance — a formal-casual garment worn untucked "
            "on hot days across Mexico, Cuba, and the Caribbean, and to many "
            "formal occasions. Its identity lives in three details this cartridge "
            "keeps faithfully: the ALFORZAS (fine vertical pintuck columns), the "
            "FOUR patch pockets, and the vented, untucked hem. Drafted here with "
            "respect for that lineage."
        ),
        "silhouette": "worn untucked; straight hem with side vents; longer back",
        "alforzas": {
            "front_columns_per_panel": FRONT_COLS,
            "back_columns": BACK_COLS,
            "tucks_per_column": pintuck_rows,
            "tuck_gap_mm": TUCK_GAP,
            "note": "modelled as fc.Internal trace lines; real tucks also consume "
                    "fabric width (see BOM)",
        },
        "pockets": {
            "count": 4,
            "chest_mm": [CHEST_W, CHEST_H],
            "hip_mm": [HIP_W, HIP_H],
            "note": "two chest + two hip, each cut piece carries its own alforza "
                    "column and a button",
        },
        "side_vent_mm": vent_height,
        "back_drop_mm": back_drop,
        "collar": "two-piece turndown (stand + fall), chained bisection solve",
        "half_neckline_mm": round(half_neck, 1),
        "stand_neck_target_mm": round(half_neck + OVERLAP, 1),
        "stand_top_mm": round(stand_top_len, 1),
        "neck_opening_full_mm": round(2.0 * half_neck, 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "cap_target_mm": round(cap_target, 1),
        "overlap_mm": OVERLAP,
        "button_stand_mm": button_stand,
        "buttons_front": BUTTONS,
        "sleeve": sleeve,
        "drafting": "drop-shoulder woven shirt block; full back armhole kept "
                    "equal to the front on this block; two-piece turndown collar "
                    "solved by chained bisection (stand to neckline, fall to the "
                    "stand's top edge); set-flat sleeve cap solved by bisection; "
                    "alforzas and side vents drafted as traces/markings "
                    "(teaching-grade)",
    }
    return pattern


result = build()

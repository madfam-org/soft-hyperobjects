"""
Camp-collar shirt — FC-100 rank #77. Fashion Cabinet Garment Cartridge.

The relaxed open-collar resort shirt ("camisa de cuello camp", also Cuban /
convertible collar). Family sibling of the casual button-down (rank #20): the
same drop-shoulder woven block and one-piece-per-half collar solve, but the
collar is FLAT and OPEN instead of a standing band. Four things this cartridge
encodes:

  - CAMP COLLAR (the signature): a ONE-PIECE flat collar, half cut on fold at
    CB, whose neck edge is solved by bisection to the measured neckline
    (front.neck + back.neck per garment half) exactly like the collar-band
    enabler — but the body lies WIDE and FLAT, folding open over the shoulders.
    Its front edge breaks outward to a collar point; the gap between the two
    mirrored fronts over the open placket is the camp "V" notch at CF. Neck
    seam solved at ease 0, delta ≈ 0.
  - BUTTON PLACKET: the front's center edge is extended `button_stand` past CF
    as a folded-edge placket; six buttonhole cross-marks sit on the CF line.
    The camp convention leaves the TOP button open, so the top mark is a
    reference only (see docs/README.md).
  - SHORT SLEEVE: a set-flat sleeve whose cap is solved by bisection to the
    front + back armholes at zero ease; short by default with a turn-up-friendly
    plain hem (long-sleeve preset reuses the same solve).
  - Relaxed boxy body: straight hem with marked side vents above the hem, chest
    patch-pocket placement traced as an internal.

Simplifications (docs/README.md): the collar is drafted as a single flat piece
(real camp collars are sometimes drafted with a tiny separate under-stand at
CB); the side vent and pocket are markings, not cut detail; straight hem v0.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|collar|pocket|set

chest_girth    = float(PARAM(lambda: chest_girth, 1060.0))
body_length    = float(PARAM(lambda: body_length, 720.0))    # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 230.0))  # shoulder to hem (short)
woven_ease     = float(PARAM(lambda: woven_ease, 200.0))     # total; relaxed boxy fit
button_stand   = float(PARAM(lambda: button_stand, 30.0))    # front edge past CF
collar_width   = float(PARAM(lambda: collar_width, 85.0))    # camp collar depth (flat)
collar_point   = float(PARAM(lambda: collar_point, 55.0))    # front collar-point reach
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(400.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(100.0, min(sleeve_length, 660.0))
woven_ease = max(80.0, min(woven_ease, 420.0))
button_stand = max(20.0, min(button_stand, 40.0))
collar_width = max(55.0, min(collar_width, 120.0))
collar_point = max(30.0, min(collar_point, 90.0))

# ── Drop-shoulder shirt block (woven-tops family, camp neckline) ─────────────
W = (chest_girth + woven_ease) / 4.0           # quarter body width
L = body_length
AH = (chest_girth + woven_ease) / 8.0 + 95.0   # drop-shoulder armhole depth
AH = max(160.0, min(AH, L - 120.0))
NW = max(60.0, neck_girth / 5.0)               # half neck width at HPS
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 20.0
# Camp collars sit on a slightly deeper, more open front scoop than a dress
# neckline — the collar rolls open here rather than buttoning to the throat.
FRONT_NECK_DROP = max(78.0, neck_girth / 5.0 + 20.0)
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
CB_NECK_Y = HPS_Y - BACK_NECK_DROP
OVERLAP = 15.0                                 # collar end past CF (button line)
COLLAR_NECK_RISE = 12.0                        # flat collar neck-edge curl
VENT_HEIGHT = 110.0                            # side-vent slit above the hem
BUTTONHOLES = 6
POCKET_W, POCKET_H = 120.0, 130.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)


def _armhole_edge():
    """Shared front/back armhole (drop-shoulder shirts keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _front_neck_edge():
    """Front neck: OVERLAP straight run past CF (the placket button line, where
    the camp collar ends), then the open scoop up to HPS.

    Including the straight run makes the per-half seam check
    collar.neck == front.neck + back.neck close exactly, just like the casual
    button-down: the front is cut 2 (its neck appears once per garment half),
    the on-fold back and collar each contribute their half.
    """
    cf = fc.P(0.0, CF_NECK_Y)
    scoop = fc.Bezier(cf, fc.P(NW * 0.55, CF_NECK_Y),
                      fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.42), fc.P(NW, HPS_Y))
    return fc.Edge("neck", [fc.Line(fc.P(-OVERLAP, CF_NECK_Y), cf), scoop])


def _buttonhole_marks():
    """Six cross-marks on the CF line (x = 0), evenly spaced.

    Camp style leaves the top button open; the top mark documents it as a
    reference point (the collar rolls open above it).
    """
    top = CF_NECK_Y - 30.0
    bottom = max(110.0, top - 500.0)
    arm = 4.0
    marks = []
    for i in range(BUTTONHOLES):
        y = top - (top - bottom) * i / (BUTTONHOLES - 1.0)
        marks.append(fc.Internal(
            f"buttonhole {i + 1}",
            [fc.P(-arm, y), fc.P(arm, y), fc.P(0.0, y),
             fc.P(0.0, y - arm), fc.P(0.0, y + arm)],
            kind="drill",
        ))
    return marks


def _pocket_trace():
    """Chest patch-pocket placement (wearer's left once mirrored)."""
    top = max(180.0, min(UNDERARM.y + 60.0, CF_NECK_Y - 30.0))
    bottom = max(top - POCKET_H, 40.0)
    left = W * 0.30
    right = min(left + POCKET_W, W * 0.92)
    return fc.Internal(
        "pocket placement",
        [fc.P(left, top), fc.P(right, top), fc.P(right, bottom),
         fc.P(left, bottom), fc.P(left, top)],
        kind="trace",
    )


def _vent_mark():
    """Side-vent slit marking on the side seam, above the hem."""
    return fc.Internal(
        "side vent",
        [fc.P(W, 0.0), fc.P(W, VENT_HEIGHT), fc.P(W - 8.0, VENT_HEIGHT)],
        kind="marking",
    )


def build_front():
    """Front, cut 2 mirrored: center edge extended button_stand past CF."""
    neck = _front_neck_edge()
    cf_t = max(0.02, min(0.5, OVERLAP / neck.length(0.05)))
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
        internals=[_pocket_trace(), _vent_mark(), *_buttonhole_marks()],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Back, cut 1 on fold at CB, straight boxy body with a side-vent mark."""
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, CB_NECK_Y), fc.P(NW * 0.55, CB_NECK_Y),
                   fc.P(NW, CB_NECK_Y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, CB_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(W * 0.60, 80.0), fc.P(W * 0.60, L - 120.0)),
        internals=[_vent_mark()],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    """Short sleeve; cap solved by bisection to the front + back armholes, ease 0."""
    ch = max(45.0, AH * 0.33)                      # shallow relaxed cap
    sl = max(55.0, sleeve_length - ch)             # underarm-to-hem length
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(48):                            # cap length grows with hb
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
    chw = max(75.0, hb * 0.80)                     # relaxed short-sleeve opening
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
        internals=[fc.Internal("turn-up cuff fold",
                               [fc.P(-chw, hem_allowance + 18.0),
                                fc.P(chw, hem_allowance + 18.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def _collar_neck_edge(flat):
    """Flat camp-collar neck edge: shallow curve solved to the half neckline."""
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_NECK_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(half_target):
    """One-piece FLAT camp collar, half on fold at CB.

    Neck edge bisected to half_target = one front.neck (incl. overlap) + half
    back.neck. Unlike a standing band, the body is wide and flat: it extends
    `collar_width` outward from the neck and breaks to a forward collar point,
    the notch that opens the camp "V" at CF over the placket.
    """
    lo, hi = half_target * 0.7, half_target * 1.05
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if _collar_neck_edge(mid).length(0.05) < half_target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(_collar_neck_edge(flat).length(0.05) - half_target) > 1.0:
        raise ValueError("camp collar neck-edge solver did not converge")
    # Neck edge runs CB (0,0) → front-neck end (flat, COLLAR_NECK_RISE). The
    # collar body rises in +y. Front point reaches forward (+x) and out (+y),
    # forming the open notch; the outer style edge sweeps back to the CB top.
    neck_end = fc.P(flat, COLLAR_NECK_RISE)
    point = fc.P(flat + collar_point, COLLAR_NECK_RISE + collar_width * 0.62)
    top_start = fc.P(0.0, collar_width)
    piece = fc.Piece(
        "collar",
        [
            _collar_neck_edge(flat),
            fc.Edge("front_edge", [fc.Line(neck_end, point)]),
            fc.Edge("outer",
                    [fc.curve_through(point, top_start, bulge=0.06, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(flat * 0.18, collar_width * 0.45),
                               fc.P(flat * 0.72, collar_width * 0.45 + 6.0)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Camp Collar (half, on fold)",
    )
    return piece, flat


def build_pocket():
    """Chest patch pocket as a real cut piece (mitred-flap-free camp pocket)."""
    flap = 22.0                                    # angled bottom point drop
    return fc.Piece(
        "pocket",
        [
            fc.Edge("top", [fc.Line(fc.P(0.0, POCKET_H), fc.P(POCKET_W, POCKET_H))]),
            fc.Edge("side_r", [fc.Line(fc.P(POCKET_W, POCKET_H),
                                       fc.P(POCKET_W, flap))]),
            fc.Edge("point_r", [fc.Line(fc.P(POCKET_W, flap),
                                        fc.P(POCKET_W / 2.0, 0.0))]),
            fc.Edge("point_l", [fc.Line(fc.P(POCKET_W / 2.0, 0.0),
                                        fc.P(0.0, flap))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, flap), fc.P(0.0, POCKET_H))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance},         # top hem folds to the inside
        grainline=fc.Grainline(fc.P(POCKET_W * 0.5, 25.0),
                               fc.P(POCKET_W * 0.5, POCKET_H - 20.0)),
        internals=[fc.Internal("fold line (top facing)",
                               [fc.P(0.0, POCKET_H - hem_allowance - 12.0),
                                fc.P(POCKET_W, POCKET_H - hem_allowance - 12.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Chest Pocket",
    )


def build():
    pattern = fc.PatternSet("camp-collar-shirt")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    half_neck = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "collar": target_piece in ("collar", "set"),
        "pocket": target_piece in ("pocket", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    collar_flat = None
    if wanted["collar"]:
        collar, collar_flat = build_collar(half_neck)
        pattern.add(collar)
    if wanted["pocket"]:
        pattern.add(build_pocket())
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
        )
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("collar", "neck")],
            [("front", "neck"), ("back", "neck")],
            tol=2.0,
        )
    fabric_width = 1450.0                           # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.65)
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 65% marker efficiency; "
                 "manta-cruda is the linen-look alternative"},
        {"item": "fusible interfacing (camp collar + button stands)", "qty": 1,
         "unit": "set",
         "note": "collar cut doubled on fold (upper + under); stands fused full length"},
        {"item": "shirt buttons Ø 12-15 mm", "qty": BUTTONHOLES, "unit": "pieces",
         "note": "6 front (camp style leaves the top open); hard goods federate to "
                 "the Yantra4D button family, never re-implemented here"},
        {"item": "polyester thread + universal needle", "qty": 1, "unit": "set",
         "note": "sharp 80/12 for poplin (or 90/14 for the heavier muslin option)"},
    ]
    pattern.metadata = {
        "fc100_rank": 77,
        "fabric_hint": "popelina-algodon",
        "collar_style": "camp / Cuban / convertible (one-piece flat open collar)",
        "collar_half_target_mm": round(half_neck, 1),
        "collar_flat_mm": None if collar_flat is None else round(collar_flat, 1),
        "collar_width_mm": collar_width,
        "collar_point_mm": collar_point,
        "neck_opening_full_mm": round(2.0 * half_neck, 1),
        "front_neck_drop_mm": round(FRONT_NECK_DROP, 1),
        "overlap_mm": OVERLAP,
        "button_stand_mm": button_stand,
        "buttonholes": BUTTONHOLES,
        "top_button": "open (camp convention)",
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "side_vent_mm": VENT_HEIGHT,
        "drafting": "drop-shoulder woven shirt; ONE-PIECE flat camp collar solved "
                    "by bisection to the measured neckline (ease 0) with a forward "
                    "collar point forming the open CF V-notch; short set-flat sleeve "
                    "cap also solved by bisection; teaching-grade single-piece collar",
    }
    return pattern


result = build()

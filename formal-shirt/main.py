"""
Formal shirt (tuxedo / evening dress shirt) — FC-100 rank #70.
Fashion Cabinet Garment Cartridge.

A dress shirt refined for black-tie: the full woven multi-solve chain of the
dress shirt (rank #4) — button-stand fronts, back ending at the yoke seam, a
yoke carrying the back neck + shoulders, a placket sleeve, a collar STAND solved
to the measured neckline (collar-band method) and a collar FALL solved to the
stand's measured top edge (the chained second solve) — PLUS three evening
refinements:

  • a stiff BIB panel (cut 2, marcella / piqué): a distinct front-overlay piece
    whose neck and shoulder edges are copied verbatim from the front, so it is
    caught in the collar seam and the shoulder seam with delta ≡ 0; its face
    carries pintuck TRACE lines (pleated-bib option) and its sides/bottom are
    edge-stitched onto the front (an overlay, not a sewn seam);
  • a `collar_style` select — turndown (classic pointed fall) | wing (a short
    stand-collar band whose tiny turned-back wings are trace marks). Both solve
    their neck edge to the SAME stand-top length, so the fall↔stand seam
    balances in either style;
  • a `cuff_style` select — barrel (single 1-button cuff) | french (double cuff,
    cut at 2× depth, folded back and closed with a cufflink). Cuff length is
    wrist × ratio + placket in both.

Closure is a covered/fly button placket by default; the front stand also carries
seven marks that read as buttonholes OR stud holes (evening studs). Buttons,
studs, and cufflinks are Yantra4D hardware cartridges referenced in the BOM,
never re-implemented here.

Simplifications (docs/README.md): the full back armhole is drafted on the back
piece (real shirts split it across back + yoke); straight hem v0; slit sleeve
placket; the bib is a flat overlay panel (no separate boxed pleat construction —
the pleats are trace lines the maker folds).

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
# front|back|yoke|sleeve|cuff|stand|fall|bib|set

chest_girth    = float(PARAM(lambda: chest_girth, 1020.0))
body_length    = float(PARAM(lambda: body_length, 780.0))    # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 640.0))  # cap apex to wrist
woven_ease     = float(PARAM(lambda: woven_ease, 130.0))     # total ease (trimmer)
button_stand   = float(PARAM(lambda: button_stand, 30.0))    # extension past CF
yoke_drop      = float(PARAM(lambda: yoke_drop, 100.0))      # HPS to yoke seam
wrist_opening  = float(PARAM(lambda: wrist_opening, 240.0))  # finished-ish girth
bib_width      = float(PARAM(lambda: bib_width, 300.0))      # full bib width at chest
bib_height     = float(PARAM(lambda: bib_height, 320.0))     # CF-neck down to bib bottom
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# collar_style: "turndown" | "wing"  ;  cuff_style: "barrel" | "french"
collar_style = str(PARAM(lambda: collar_style, "wing")).lower()
if collar_style not in ("turndown", "wing"):
    collar_style = "wing"
cuff_style = str(PARAM(lambda: cuff_style, "french")).lower()
if cuff_style not in ("barrel", "french"):
    cuff_style = "french"

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(500.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(400.0, min(sleeve_length, 750.0))
woven_ease = max(60.0, min(woven_ease, 320.0))
button_stand = max(20.0, min(button_stand, 50.0))
yoke_drop = max(60.0, min(yoke_drop, 160.0))
wrist_opening = max(180.0, min(wrist_opening, 320.0))
bib_width = max(200.0, min(bib_width, 460.0))
bib_height = max(200.0, min(bib_height, 460.0))

# ── Woven shirt block (drop-shoulder constants, yoke split) ──────────────────
W = (chest_girth + woven_ease) / 4.0          # quarter body width
L = body_length
AH = (chest_girth + woven_ease) / 8.0 + 95.0  # armhole depth (auto)
AH = max(AH, yoke_drop + 60.0)                # keep the armhole below the yoke
AH = max(160.0, min(AH, L - 120.0))
NW = max(60.0, neck_girth / 5.0)              # half neck width at HPS
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 25.0                         # HPS to CB nape (on the yoke)
FRONT_NECK_DROP = NW + 5.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
YOKE_Y = HPS_Y - yoke_drop                    # yoke seam height on the body
FNY = HPS_Y - FRONT_NECK_DROP                 # CF neck point height
BS = button_stand
OVERLAP = 15.0                                # collar-stand button extension
STAND_H, STAND_RISE = 32.0, 12.0
FALL_H, FALL_RISE, FALL_POINT = 60.0, 10.0, 45.0   # turndown fall
WING_H, WING_RISE, WING_TAB = 26.0, 8.0, 26.0      # wing collar (short band + tabs)
CUFF_OVERLAP = 25.0
SLEEVE_FULLNESS = 1.15                        # pleated into the cuff
PLACKET_LEN = 130.0
BUTTONS = 7                                   # front stud/button marks
# Cuff geometry: finished band depth, doubled for french (folds back).
CUFF_BAND = 70.0
CUFF_DEPTH = CUFF_BAND * (2.0 if cuff_style == "french" else 1.0)
CUFF_H = 2.0 * CUFF_DEPTH                     # cut doubled in height, folded at mid
CUFF_RATIO = 0.9                              # wrist × ratio for cuff length


def _cross(label, x, y, half=4.0):
    """Drill cross-mark as two internals (zipper-notion convention)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


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


def _front_neck_segment():
    """The CF→HPS neck bezier, shared verbatim by front and bib (delta ≡ 0)."""
    return fc.Bezier(fc.P(0.0, FNY), fc.P(NW * 0.55, FNY),
                     fc.P(NW, FNY + (HPS_Y - FNY) * 0.45), fc.P(NW, HPS_Y))


def _front_armhole():
    fah = SH_END.y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - fah * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + fah * 0.30), UNDERARM)],
    )


def _back_armhole():
    """FULL back armhole on the back piece, from the yoke-seam end down."""
    top = fc.P(W - 5.0, YOKE_Y)
    bah = YOKE_Y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(top, fc.P(W - 14.0, YOKE_Y - bah * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + bah * 0.30), UNDERARM)],
    )


def build_front():
    """Cut 2 mirror; the center edge extends `button_stand` past CF (x=0).

    The seven cross-marks on the CF read as buttonholes (covered placket) OR
    stud holes (evening studs) — closure hardware is a BOM reference. A trace
    box marks the covered/fly placket fold and the bib overlay outline."""
    bh_top = FNY - 70.0
    bh_bottom = 150.0
    step = (bh_top - bh_bottom) / (BUTTONS - 1)
    internals = [fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, FNY)],
                             kind="marking")]
    # Covered / fly placket: a fold-back trace box either side of the CF marks.
    fly_w = 22.0
    internals.append(fc.Internal(
        "covered placket fold",
        [fc.P(fly_w, bh_bottom - 20.0), fc.P(fly_w, bh_top + 20.0),
         fc.P(-fly_w, bh_top + 20.0), fc.P(-fly_w, bh_bottom - 20.0)],
        kind="trace"))
    for i in range(BUTTONS):
        internals += _cross(f"stud-{i + 1}", 0.0, bh_top - i * step)
    # Bib overlay outline on the front face (the bib piece is stitched here).
    hb = min(bib_width / 2.0, W - 20.0)
    bib_bottom_y = FNY - bib_height
    internals.append(fc.Internal(
        "bib overlay outline",
        [fc.P(0.0, bib_bottom_y), fc.P(hb, bib_bottom_y + 10.0),
         fc.P(hb, FNY - 30.0)],
        kind="trace"))
    # The neckline is split into two named edges (casual-button-down idiom):
    #   stand_top = the horizontal button-stand top (−BS → CF), caught in the
    #               collar seam but NOT shared by the bib overlay;
    #   neck      = the pure CF→HPS neckline bezier, which the bib copies verbatim
    #               so the bib-attach seam is delta ≡ 0.
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, 0.0), fc.P(-BS, FNY))]),
            fc.Edge("stand_top", [fc.Line(fc.P(-BS, FNY), fc.P(0.0, FNY))]),
            fc.Edge("neck", [_front_neck_segment()]),
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _front_armhole(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-BS, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.6, 80.0), fc.P(W * 0.6, L - 140.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_bib():
    """Stiff evening BIB, cut 2 mirror (marcella / piqué), overlaying the upper
    front chest. Its NECK and SHOULDER edges are the SAME geometry as the front's
    (so it is caught in the collar seam and the shoulder seam, delta ≡ 0). Its CF
    edge and shaped lower/side edges are edge-stitched onto the front — an
    overlay, not a sewn seam. Pintuck TRACE lines give the pleated-bib option."""
    hb = min(bib_width / 2.0, W - 20.0)
    bib_bottom_y = FNY - bib_height
    sh_end = SH_END
    # Closed CCW chain, starting at the CF-bottom corner and running:
    #   cf (up) → neck (CF→HPS) → shoulder (HPS→shoulder end) →
    #   side (shoulder end → outer bottom corner) → bottom (corner → CF-bottom).
    # neck and shoulder are the SAME geometry as the front's edges (length is
    # direction-independent) so the bib attach seams are delta ≡ 0.
    cf = fc.Edge("cf", [fc.Line(fc.P(0.0, bib_bottom_y), fc.P(0.0, FNY))])
    neck = fc.Edge("neck", [_front_neck_segment()])              # (0,FNY)→(NW,HPS_Y)
    shoulder = fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), sh_end)])
    side = fc.Edge(
        "side",
        [fc.Bezier(sh_end, fc.P(hb + 12.0, sh_end.y - (sh_end.y - bib_bottom_y) * 0.30),
                   fc.P(hb + 4.0, bib_bottom_y + (sh_end.y - bib_bottom_y) * 0.28),
                   fc.P(hb, bib_bottom_y))],
    )
    # Classic U / horseshoe lower edge from the outer corner in to the CF.
    bottom = fc.Edge(
        "bottom",
        [fc.Bezier(fc.P(hb, bib_bottom_y), fc.P(hb * 0.55, bib_bottom_y - 30.0),
                   fc.P(hb * 0.35, bib_bottom_y - 30.0), fc.P(0.0, bib_bottom_y))],
    )
    # Pintuck pleat traces: vertical folds evenly across the bib half-width.
    n_pleats = 4
    pleats = []
    for i in range(1, n_pleats + 1):
        px = hb * i / (n_pleats + 1)
        pleats.append(fc.Internal(
            f"bib pintuck {i}",
            [fc.P(px, bib_bottom_y + 12.0), fc.P(px, FNY - 24.0)],
            kind="trace"))
    return fc.Piece(
        "bib",
        [cf, neck, shoulder, side, bottom],
        seam_allowance=seam_allowance,
        allowances={"cf": 0.0, "bottom": hem_allowance},
        notches=[fc.Notch("neck", 0.5, "HPS match"),
                 fc.Notch("shoulder", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(hb * 0.45, bib_bottom_y + 24.0),
                               fc.P(hb * 0.45, FNY - 30.0)),
        internals=pleats,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bib (marcella / piqué)",
    )


def build_back():
    """Cut 1 on fold; the top edge ends at the yoke seam (back neck = yoke)."""
    origin = fc.P(0.0, 0.0)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(origin, fc.P(0.0, YOKE_Y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, YOKE_Y), fc.P(W - 5.0, YOKE_Y))]),
            _back_armhole(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("top", 0.5, "yoke match")],
        grainline=fc.Grainline(fc.P(W * 0.62, 80.0), fc.P(W * 0.62, YOKE_Y - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_yoke():
    """Cut 1 on fold, DOUBLED in construction. Own frame: bottom edge at y=0.

    Carries the back neck curve and the shoulder edges. Its side edge is
    straight and clear of the armhole — the full back armhole lives on the
    back piece (v0 simplification, see docs/README.md).
    """
    cb_h = yoke_drop - BACK_NECK_DROP            # CB height above the yoke seam
    hps = fc.P(NW, yoke_drop)
    sh_end = fc.P(W - 5.0, yoke_drop - SHOULDER_DROP)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, cb_h), fc.P(NW * 0.55, cb_h),
                   fc.P(NW, cb_h + BACK_NECK_DROP * 0.45), hps)],
    )
    return fc.Piece(
        "yoke",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, cb_h))]),
            neck,
            fc.Edge("shoulder", [fc.Line(hps, sh_end)]),
            fc.Edge("side", [fc.Line(sh_end, fc.P(W - 5.0, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(W - 5.0, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(W * 0.5, 12.0), fc.P(W * 0.5, cb_h * 0.75)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Yoke (doubled)",
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, back side first."""
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                  fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                  fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(front_ah, back_ah):
    """Long sleeve; cap solved by bisection to front + back armholes (ease 0)."""
    cap_target = front_ah + back_ah
    ch = max(70.0, AH * 0.33)
    sl = max(220.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(100.0, min(wrist_opening * SLEEVE_FULLNESS / 2.0, hb - 10.0))
    px = chw * 0.55                              # placket slit, back of the wrist
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},      # wrist is cuffed, not hemmed
        notches=[fc.Notch("cap", back_ah / cap_target, "shoulder match"),
                 fc.Notch("hem", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.8)),
        internals=[
            fc.Internal("sleeve placket slit",
                        [fc.P(px, 0.0), fc.P(px, PLACKET_LEN)], kind="marking"),
            fc.Internal("placket stop",
                        [fc.P(px - 4.0, PLACKET_LEN), fc.P(px + 4.0, PLACKET_LEN)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_cuff():
    """Cuff, cut doubled in height and folded at mid. Length = wrist × ratio +
    placket overlap + 2×sa. A french cuff (cuff_style) is cut at 2× band depth
    so it folds back on itself and closes with a cufflink through both marks; a
    barrel cuff is a single band with a button + buttonhole."""
    length = wrist_opening * CUFF_RATIO + CUFF_OVERLAP + 2.0 * seam_allowance
    internals = [fc.Internal("fold line",
                             [fc.P(0.0, CUFF_H / 2.0), fc.P(length, CUFF_H / 2.0)],
                             kind="marking")]
    if cuff_style == "french":
        # Cufflink holes: BOTH ends marked (the cuff folds back, link pierces all
        # four layers). Cufflink hardware is a Yantra4D reference in the BOM.
        internals += _cross("cufflink hole a", seam_allowance + 12.0, CUFF_H * 0.25)
        internals += _cross("cufflink hole b", length - seam_allowance - 12.0,
                            CUFF_H * 0.25)
        # Turn-back fold trace at quarter/three-quarter height (double cuff).
        internals.append(fc.Internal(
            "turn-back fold", [fc.P(0.0, CUFF_H * 0.25), fc.P(length, CUFF_H * 0.25)],
            kind="trace"))
        label = "Cuff (french / double)"
    else:
        internals += _cross("cuff buttonhole", seam_allowance + 12.0, CUFF_H * 0.25)
        internals += _cross("cuff button", length - seam_allowance - 12.0,
                            CUFF_H * 0.25)
        label = "Cuff (barrel)"
    return fc.Piece(
        "cuff",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, CUFF_H))]),
            fc.Edge("top", [fc.Line(fc.P(length, CUFF_H), fc.P(0.0, CUFF_H))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, CUFF_H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                      # length already includes 2×sa
        grainline=fc.Grainline(fc.P(length * 0.2, CUFF_H / 2.0 + 14.0),
                               fc.P(length * 0.8, CUFF_H / 2.0 + 14.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label=label,
    )


def _stand_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, STAND_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_stand(half_neck):
    """Collar stand, half on fold at CB — the collar-band method verbatim:
    neck edge solved to the half neckline + button overlap."""
    target = half_neck + OVERLAP
    flat = _solve_flat(_stand_neck, target, "collar-stand neck")
    neck = _stand_neck(flat)
    top_start = fc.P(0.0, STAND_H)
    top_end = fc.P(flat, STAND_RISE + STAND_H)
    t_cf = half_neck / target                    # CF button/stud line along the neck
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
                 fc.Notch("neck", t_cf, "CF / stud line")],
        grainline=fc.Grainline(fc.P(flat * 0.2, STAND_H * 0.5),
                               fc.P(flat * 0.75, STAND_H * 0.5 + STAND_RISE * 0.7)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Collar Stand (half, on fold)",
    )


def _fall_neck(flat, rise):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, rise),
                          bulge=0.05, side=-1.0)],
    )


def build_fall(stand_top_len):
    """Collar fall / wing, half on fold: neck edge solved to the stand's measured
    TOP edge — the second solve, chained off the first. `collar_style` sets the
    silhouette above that shared neck edge:

      turndown → a tall pointed turndown collar (classic dress-shirt fall);
      wing     → a short upright band whose small turned-back WING tabs are trace
                 marks (the formal wing collar).

    Both solve their neck to `stand_top_len`, so fall.neck ↔ stand.top is delta
    ≡ 0 in either style."""
    if collar_style == "wing":
        h, rise, point = WING_H, WING_RISE, WING_TAB
    else:
        h, rise, point = FALL_H, FALL_RISE, FALL_POINT
    flat = _solve_flat(lambda f: _fall_neck(f, rise), stand_top_len,
                       "collar-fall neck")
    neck = _fall_neck(flat, rise)
    internals = []
    if collar_style == "wing":
        # The wing tabs: short turned-back triangles at the CF, drawn as traces.
        internals.append(fc.Internal(
            "wing tab",
            [fc.P(flat, rise), fc.P(flat + point, rise + h * 0.5),
             fc.P(flat, rise + h)],
            kind="trace"))
        front = fc.Edge("front_edge", [fc.Line(fc.P(flat, rise), fc.P(flat, rise + h))])
        top = fc.Edge("top",
                      [fc.curve_through(fc.P(flat, rise + h), fc.P(0.0, h),
                                        bulge=0.02, side=1.0)])
    else:
        point_p = fc.P(flat + point, rise + h)
        front = fc.Edge("front_edge", [fc.Line(fc.P(flat, rise), point_p)])
        top = fc.Edge("top",
                      [fc.curve_through(point_p, fc.P(0.0, h),
                                        bulge=0.03, side=1.0)])
    return fc.Piece(
        "fall",
        [
            neck,
            front,
            top,
            fc.Edge("cb", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "stand match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, h * 0.55),
                               fc.P(flat * 0.7, h * 0.55)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label=("Wing Collar (half, on fold)" if collar_style == "wing"
               else "Collar Fall (half, on fold)"),
    )


def build():
    pattern = fc.PatternSet("formal-shirt")
    front = build_front()
    bib = build_bib()
    back = build_back()
    yoke = build_yoke()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    # Half neckline the stand sews to = front stand-top + front neckline + yoke.
    half_neck = (front.edge("stand_top").length(0.05)
                 + front.edge("neck").length(0.05)
                 + yoke.edge("neck").length(0.05))
    stand = build_stand(half_neck)
    stand_top_len = stand.edge("top").length(0.05)
    wanted = {
        name: target_piece in (name, "set")
        for name in ("front", "bib", "back", "yoke", "sleeve", "cuff",
                     "stand", "fall")
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["bib"]:
        pattern.add(bib)
    if wanted["back"]:
        pattern.add(back)
    if wanted["yoke"]:
        pattern.add(yoke)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(front_ah, back_ah))
    if wanted["cuff"]:
        pattern.add(build_cuff())
    if wanted["stand"]:
        pattern.add(stand)
    if wanted["fall"]:
        pattern.add(build_fall(stand_top_len))
    # ── Seams (every one balances by construction; deltas ≈ 0) ───────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    if wanted["front"] and wanted["yoke"]:
        pattern.declare_seam(("front", "shoulder"), ("yoke", "shoulder"), tol=1.5)
    if wanted["yoke"] and wanted["back"]:
        pattern.declare_seam(("yoke", "bottom"), ("back", "top"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
    if wanted["cuff"] and wanted["sleeve"]:
        # Cuff bottom ↔ pleated sleeve hem: the sleeve hem is eased/pleated in,
        # so the cuff band is shorter by (hem − cuff length). Declared with the
        # measured ease so the check is real, not loosened.
        sleeve = pattern.piece("sleeve")
        cuff = pattern.piece("cuff")
        hem_len = sleeve.edge("hem").length(0.05)
        cuff_len = cuff.edge("bottom").length(0.05)
        pattern.declare_seam(("sleeve", "hem"), ("cuff", "bottom"),
                             tol=1.5, ease=round(hem_len - cuff_len, 2))
    if wanted["stand"] and wanted["front"] and wanted["yoke"]:
        pattern.declare_seam(
            [("stand", "neck")],
            [("front", "stand_top"), ("front", "neck"), ("yoke", "neck")],
            tol=2.0, ease=OVERLAP)
    if wanted["fall"] and wanted["stand"]:
        pattern.declare_seam([("fall", "neck")], [("stand", "top")], tol=2.0)
    # BIB attach: the bib is caught in the collar seam (its neck == front neck)
    # and the shoulder seam (its shoulder == front shoulder). Both delta ≡ 0
    # because the bib copies the front's geometry verbatim.
    if wanted["bib"] and wanted["front"]:
        pattern.declare_seam(("bib", "neck"), ("front", "neck"), tol=1.0)
        pattern.declare_seam(("bib", "shoulder"), ("front", "shoulder"), tol=1.0)

    fabric_width = 1450.0                        # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.65)
    stud_note = ("7 front + collar stand; evening STUDS or buttons — hardware "
                 "is a Yantra4D cartridge (shirt-stud / shank-button), never "
                 "re-implemented here")
    bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"cotton poplin body at {fabric_width:.0f} mm width, "
                 f"65% marker efficiency"},
        {"item": "marcella / piqué bib panel", "qty": 1, "unit": "set",
         "note": "stiffer piqué face for the two bib pieces (evening option); "
                 "poplin is the plain-front fallback"},
        {"item": "fusible interfacing (stand, fall/wing, cuffs, front stands, "
                 "bib)", "qty": 1, "unit": "set",
         "note": "shirt-weight; heavier under the bib for a crisp plastron"},
        {"item": "shirt studs or buttons 11.5 mm", "qty": BUTTONS + 1,
         "unit": "pcs", "note": stud_note},
    ]
    if cuff_style == "french":
        bom.append({"item": "cufflinks", "qty": 1, "unit": "pair",
                    "note": "french/double cuff closure; cufflink is a Yantra4D "
                            "cartridge reference, never re-implemented here"})
    else:
        bom.append({"item": "cuff buttons 11.5 mm", "qty": 2, "unit": "pcs",
                    "note": "barrel-cuff closure; Yantra4D shank-button ref"})
    bom.append({"item": "polyester thread + universal needle", "qty": 1,
                "unit": "set", "note": "sharp 80/12 for poplin and piqué"})
    pattern.bom = bom
    pattern.metadata = {
        "fc100_rank": 70,
        "fabric_hint": "popelina-algodon",
        "collar_style": collar_style,
        "cuff_style": cuff_style,
        "half_neckline_mm": round(half_neck, 1),
        "stand_neck_mm": round(half_neck + OVERLAP, 1),
        "stand_top_mm": round(stand_top_len, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_target_mm": round(front_ah + back_ah, 1),
        "bib_width_mm": round(min(bib_width, 2.0 * (W - 20.0)), 1),
        "bib_height_mm": round(bib_height, 1),
        "cuff_length_mm": round(wrist_opening * CUFF_RATIO + CUFF_OVERLAP
                                + 2.0 * seam_allowance, 1),
        "cuff_cut_depth_mm": round(CUFF_DEPTH, 1),
        "studs": {"count": BUTTONS, "line": "CF (x=0)",
                  "closure": "covered/fly placket or evening studs",
                  "stand_extension_mm": BS},
        "drafting": "tuxedo dress shirt on the woven yoke-split block; bib is a "
                    "cut-2 overlay whose neck+shoulder copy the front (attach "
                    "delta 0); cap, stand neck, and fall/wing neck solved by "
                    "bisection — fall chained to the stand's measured top edge; "
                    "cuff band eased into the pleated sleeve hem",
    }
    return pattern


result = build()

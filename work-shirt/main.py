"""
Work shirt — FC-100 rank #90. Fashion Cabinet Garment Cartridge.

The classic two-pocket utility / uniform work shirt ("camisa de trabajo"),
cut here in chambray-weight denim: a slightly relaxed woven shirt with a wide
topstitched CF button placket, a proper two-piece turndown collar (stand +
fall, both solved), a back yoke with a CB box pleat, a barrel cuff with a
sleeve placket, and — the signature — TWO chest FLAP pockets drafted as real
cut pieces (a patch-pocket body plus a button-through flap each).

Pieces (nine): a ONE-PIECE front cut 2 mirrored whose center edge extends
`placket_width` past CF (seven buttonhole cross-marks on the CF line, the wide
topstitched placket box marked, and both chest flap-pocket placements + flap
attach lines traced); a BACK cut 1 on fold at CB whose top edge ends at the
yoke seam, with the CB box pleat marked as two internal fold lines and the full
back armhole below the yoke; a YOKE cut 1 on fold (doubled in construction)
carrying the back neck and both shoulders (dress-shirt yoke method); a set-in
SLEEVE cut 2 whose cap is solved by bisection to the front + back armholes plus
a little cap ease, with a sleeve-placket slit marked and a straight hem into
the cuff; a barrel CUFF cut 2 (doubled and folded); a collar STAND cut 2 on
fold whose neck edge is solved to the half neckline + button overlap
(collar-band method); a collar FALL cut 2 on fold whose neck edge is solved to
the stand's measured top edge — the second solve chained off the first; a real
CHEST_POCKET body cut 2 (a chamfered-corner patch with a topstitch attach
guide); and a real POCKET_FLAP cut 2 (a button-through flap with an angled
lower edge and a flap buttonhole). The pockets and flaps are topstitched
appliqué: each is its own closed piece with its placement traced on the front;
only the flap-to-pocket opening is a declared balance seam, never the appliqué
edges themselves.

Simplifications (docs/README.md): the full back armhole is drafted on the back
piece (real shirts split it across back + yoke); the sleeve placket and the
box pleat are markings; the collar fall and the pocket bag are single-layer in
v0; a straight hem. Teaching-grade — verified geometry, not a factory pattern.

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
# front|back|yoke|sleeve|cuff|stand|fall|chest_pocket|pocket_flap|set

chest_girth    = float(PARAM(lambda: chest_girth, 1060.0))
body_length    = float(PARAM(lambda: body_length, 760.0))    # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 410.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 620.0))  # cap apex to wrist
woven_ease     = float(PARAM(lambda: woven_ease, 200.0))     # relaxed utility fit
placket_width  = float(PARAM(lambda: placket_width, 38.0))   # wide CF work placket
yoke_drop      = float(PARAM(lambda: yoke_drop, 110.0))      # HPS to yoke seam
wrist_opening  = float(PARAM(lambda: wrist_opening, 250.0))
pocket_width   = float(PARAM(lambda: pocket_width, 130.0))   # chest flap pocket
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1800.0))
body_length = max(500.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(400.0, min(sleeve_length, 760.0))
woven_ease = max(100.0, min(woven_ease, 400.0))
placket_width = max(28.0, min(placket_width, 55.0))
yoke_drop = max(70.0, min(yoke_drop, 170.0))
wrist_opening = max(200.0, min(wrist_opening, 320.0))
pocket_width = max(105.0, min(pocket_width, 175.0))

# ── Utility woven shirt block (drop-shoulder-ish, yoke split) ────────────────
W = (chest_girth + woven_ease) / 4.0            # quarter body width
L = body_length
NW = max(60.0, neck_girth / 5.0)                # half neck width at HPS
AH = (chest_girth + woven_ease) / 8.0 + 100.0   # armhole depth (auto)
AH = max(AH, yoke_drop + 60.0)                  # keep the armhole below the yoke
AH = max(170.0, min(AH, L - 120.0))
HPS_Y = L + 20.0
SHOULDER_DROP = 34.0
BACK_NECK_DROP = 24.0                            # HPS to CB nape (on the yoke)
FRONT_NECK_DROP = max(70.0, NW + 6.0)
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
YOKE_Y = HPS_Y - yoke_drop                       # yoke seam height on the body
PW = placket_width                               # CF placket extension past CF
OVERLAP = 15.0                                   # collar end past CF (button line)
STAND_H, STAND_RISE = 32.0, 12.0
FALL_H, FALL_RISE, FALL_POINT = 58.0, 10.0, 44.0
CAP_EASE = 14.0                                  # set-in sleeve cap ease
CUFF_H = 2.0 * 60.0                              # cut doubled, folded at mid
CUFF_OVERLAP = 25.0
BUTTONS = 7                                      # CF placket buttons
PLACKET_TOPSTITCH = 6.0                          # inset of the placket box lines
PLEAT_LINES_X = (16.0, 46.0)                     # CB box-pleat folds, 30 mm apart
PLEAT_LEN = 130.0
SLEEVE_PLACKET_LEN = 130.0
# Chest flap pocket geometry (both breast pockets; wearer's chest once mirrored)
POCKET_H = pocket_width + 20.0                   # slightly tall utility pocket
POCKET_CHAMFER = 24.0                            # 45° clipped bottom corners
POCKET_HEM = 26.0                                # opening hem facing
TOPSTITCH_INSET = 9.0
FLAP_H, FLAP_CLIP = 62.0, 20.0                   # flap depth, angled lower corner


def _cross(label, x, y, half=4.0):
    """Drill cross-mark as two internals (denim-jacket / zipper-notion idiom)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


def _solve_flat(edge_fn, target, what):
    """Bisect a monotonic flat-length → measured-curve-length edge builder."""
    lo, hi = target * 0.65, target * 1.05
    for _ in range(56):
        mid = (lo + hi) / 2.0
        if edge_fn(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(edge_fn(flat).length(0.05) - target) > 1.0:
        raise ValueError(f"{what} solver did not converge on {target:.1f} mm")
    return flat


def _front_armhole():
    """Front armhole: HPS shoulder end down to the underarm."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 15.0, SH_END.y - AH * 0.34),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _back_armhole():
    """Full back armhole on the back piece, from the yoke-seam corner down."""
    top = fc.P(W - 5.0, YOKE_Y)
    bah = YOKE_Y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(top, fc.P(W - 13.0, YOKE_Y - bah * 0.34),
                   fc.P(W - 6.0, UNDERARM.y + bah * 0.30), UNDERARM)],
    )


def _pocket_placement(label, cx, cy, w, h):
    """A chest flap-pocket body placement rectangle (internal trace)."""
    return fc.Internal(
        label,
        [fc.P(cx - w / 2.0, cy), fc.P(cx + w / 2.0, cy),
         fc.P(cx + w / 2.0, cy - h), fc.P(cx - w / 2.0, cy - h),
         fc.P(cx - w / 2.0, cy)],
        kind="trace",
    )


def _placements():
    """Two chest flap-pocket placements: pocket body box, the flap attach line
    above it, and a flap buttonhole cross. Mirrored across x = W/2 so both the
    wearer's-left and wearer's-right breast pockets are drawn on the front.

    Drawn clear of the button placket and the armhole so each topstitch box
    lands on flat cloth."""
    cy = min(UNDERARM.y - 20.0, CF_NECK_Y - 45.0)
    cy = max(cy, POCKET_H + 120.0)
    left_cx = W * 0.36
    right_cx = W - left_cx                       # mirror partner about CF? no —
    # both pockets sit on the ONE-PIECE front which is cut twice mirrored; we
    # draw both breast placements symmetric about the quarter-width centre so
    # the trace reads on either cut. Keep them inside [PW+curve, W].
    right_cx = min(max(right_cx, left_cx + pocket_width + 20.0), W - pocket_width * 0.55)
    out = []
    for tag, cx in (("wearer-left", left_cx), ("wearer-right", right_cx)):
        out.append(_pocket_placement(f"chest pocket placement ({tag})",
                                     cx, cy, pocket_width, POCKET_H))
        # flap attach line sits FLAP_H above the pocket top (flap folds down)
        attach_y = cy + FLAP_H
        out.append(fc.Internal(
            f"flap attach line ({tag})",
            [fc.P(cx - pocket_width / 2.0, attach_y),
             fc.P(cx + pocket_width / 2.0, attach_y)],
            kind="marking",
        ))
        out += _cross(f"flap button ({tag})", cx, cy - POCKET_H * 0.28)
    return out


def build_front():
    """Front, cut 2 mirrored: center edge extended placket_width past CF, the
    wide topstitched placket box, seven buttonhole crosses, and both chest
    flap-pocket placements. Full front armhole."""
    neck = fc.Edge(
        "neck",
        [fc.Line(fc.P(-OVERLAP, CF_NECK_Y), fc.P(0.0, CF_NECK_Y)),
         fc.Bezier(fc.P(0.0, CF_NECK_Y), fc.P(NW * 0.55, CF_NECK_Y),
                   fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    cf_t = max(0.02, min(0.5, OVERLAP / neck.length(0.05)))
    # ── internals: CF line, placket box, buttonholes, pocket placements ──
    marks = [fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, CF_NECK_Y)],
                         kind="marking")]
    # wide topstitched front placket box (both fold/topstitch lines)
    for x in (-PW + PLACKET_TOPSTITCH, -PLACKET_TOPSTITCH):
        marks.append(fc.Internal(
            "placket topstitch", [fc.P(x, 0.0), fc.P(x, CF_NECK_Y)],
            kind="marking"))
    bh_top = CF_NECK_Y - 60.0
    bh_bottom = max(140.0, bh_top - 500.0)
    step = (bh_top - bh_bottom) / (BUTTONS - 1)
    for i in range(BUTTONS):
        marks += _cross(f"buttonhole-{i + 1}", 0.0, bh_top - i * step)
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(-PW, 0.0), fc.P(-PW, CF_NECK_Y))]),
            fc.Edge("stand_top",
                    [fc.Line(fc.P(-PW, CF_NECK_Y), fc.P(-OVERLAP, CF_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _front_armhole(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(-PW, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole"),
                 fc.Notch("neck", cf_t, "CF / collar end"),
                 fc.Notch("hem", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(W * 0.66, 80.0), fc.P(W * 0.66, L - 120.0)),
        internals=[*_placements(), *marks],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Back, cut 1 on fold at CB: top edge ends at the yoke seam, CB box pleat
    marked as two fold lines, full back armhole below the yoke."""
    origin = fc.P(0.0, 0.0)
    pleats = [
        fc.Internal(f"box pleat fold ({tag})",
                    [fc.P(x, YOKE_Y), fc.P(x, YOKE_Y - PLEAT_LEN)])
        for tag, x in zip(("inner", "outer"), PLEAT_LINES_X, strict=True)
    ]
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
                 fc.Notch("top", 0.5, "yoke match"),
                 fc.Notch("hem", 0.5, "front match")],
        grainline=fc.Grainline(fc.P(W * 0.6, 60.0), fc.P(W * 0.6, YOKE_Y - 60.0)),
        internals=pleats,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_yoke():
    """Yoke, cut 1 on fold, DOUBLED in construction. Own frame: bottom at y=0.

    Carries the back neck curve and both shoulder edges (dress-shirt yoke
    method). Its side edge is straight and clear of the armhole — the full
    back armhole lives on the back piece (v0 simplification)."""
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
    """Set-in sleeve; cap solved by bisection to front + back armholes plus a
    small cap ease. A sleeve placket is marked; the wrist is closed by the
    cuff, not hemmed."""
    cap_target = front_ah + back_ah + CAP_EASE
    ch = max(80.0, AH * 0.32)
    sl = max(230.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    for _ in range(56):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs {cap_target:.1f}"
        )
    chw = max(110.0, min(wrist_opening / 2.0 + 45.0, hb - 12.0))
    px = chw * 0.55                              # wrist placket, back of the sleeve
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
        notches=[fc.Notch("cap", back_ah / (front_ah + back_ah), "shoulder match"),
                 fc.Notch("hem", 0.5, "cuff match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl * 0.8)),
        internals=[
            fc.Internal("sleeve placket slit",
                        [fc.P(px, 0.0), fc.P(px, SLEEVE_PLACKET_LEN)],
                        kind="marking"),
            fc.Internal("placket stop",
                        [fc.P(px - 4.0, SLEEVE_PLACKET_LEN),
                         fc.P(px + 4.0, SLEEVE_PLACKET_LEN)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_cuff():
    """Barrel cuff, cut doubled in height and folded at mid; button + hole."""
    length = wrist_opening + CUFF_OVERLAP + 2.0 * seam_allowance
    internals = [fc.Internal("fold line",
                             [fc.P(0.0, CUFF_H / 2.0), fc.P(length, CUFF_H / 2.0)],
                             kind="marking")]
    internals += _cross("cuff buttonhole", seam_allowance + 14.0, CUFF_H * 0.25)
    internals += _cross("cuff button", length - seam_allowance - 14.0,
                        CUFF_H * 0.25)
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
        label="Cuff",
    )


def _stand_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, STAND_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_stand(half_neck):
    """Collar stand, half on fold at CB — collar-band method: neck edge solved
    to the half neckline + button overlap."""
    target = half_neck + OVERLAP
    flat = _solve_flat(_stand_neck, target, "collar-stand neck")
    neck = _stand_neck(flat)
    top_start = fc.P(0.0, STAND_H)
    top_end = fc.P(flat, STAND_RISE + STAND_H)
    t_cf = half_neck / target                    # CF button line along the neck
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
    edge — the second solve, chained off the first. Gently pointed front."""
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


def build_chest_pocket():
    """A real chest patch-pocket body, cut 2 (both breasts): a hexagon with 45°
    chamfered bottom corners, the top edge is the opening (hem-facing
    allowance), and a topstitch guide traces the attach path inside the sides
    and bottom (patch-pocket enabler method). Appliquéd to the front, not sewn
    as a balance seam."""
    w, h = pocket_width, POCKET_H
    c = min(POCKET_CHAMFER, min(w, h) / 3.0 - 0.5)
    inset = TOPSTITCH_INSET
    return fc.Piece(
        "chest_pocket",
        [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, c))]),
            fc.Edge("chamfer_r", [fc.Line(fc.P(w, c), fc.P(w - c, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w - c, 0.0), fc.P(c, 0.0))]),
            fc.Edge("chamfer_l", [fc.Line(fc.P(c, 0.0), fc.P(0.0, c))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, c), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": POCKET_HEM},
        notches=[fc.Notch("top", 0.5, "center match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.15), fc.P(w / 2.0, h * 0.85)),
        internals=[fc.Internal(
            "topstitch guide",
            [fc.P(w - inset, h), fc.P(w - inset, inset),
             fc.P(inset, inset), fc.P(inset, h)],
        )],
        cut=fc.CutSpec(quantity=2),
        label="Chest Pocket Body",
    )


def build_pocket_flap():
    """A real button-through pocket flap, cut 2. `pocket_width` wide (matches
    the pocket opening), FLAP_H deep, with angled lower corners and a central
    flap buttonhole. The top edge (`attach`) is sewn to the front above the
    pocket; the flap folds down over the pocket opening — declared as a balance
    seam to the pocket's top edge so the flap matches the mouth width."""
    w, h, c = pocket_width, FLAP_H, FLAP_CLIP
    return fc.Piece(
        "pocket_flap",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, c))]),
            fc.Edge("corner_r", [fc.Line(fc.P(w, c), fc.P(w - c, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w - c, 0.0), fc.P(c, 0.0))]),
            fc.Edge("corner_l", [fc.Line(fc.P(c, 0.0), fc.P(0.0, c))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, c), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "pocket match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.2), fc.P(w / 2.0, h * 0.8)),
        internals=_cross("flap buttonhole", w / 2.0, h * 0.32),
        cut=fc.CutSpec(quantity=2),
        label="Pocket Flap",
    )


def build():
    pattern = fc.PatternSet("work-shirt")
    front = build_front()
    back = build_back()
    yoke = build_yoke()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    half_neck = (front.edge("neck").length(0.05)
                 + yoke.edge("neck").length(0.05))
    stand = build_stand(half_neck)
    stand_top_len = stand.edge("top").length(0.05)
    names = ("front", "back", "yoke", "sleeve", "cuff", "stand", "fall",
             "chest_pocket", "pocket_flap")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
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
    if wanted["chest_pocket"]:
        pattern.add(build_chest_pocket())
    if wanted["pocket_flap"]:
        pattern.add(build_pocket_flap())

    # ── Declared seams (all balance to delta ≈ 0) ────────────────────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    if wanted["front"] and wanted["yoke"]:
        pattern.declare_seam(("front", "shoulder"), ("yoke", "shoulder"), tol=1.5)
    if wanted["yoke"] and wanted["back"]:
        pattern.declare_seam(("yoke", "bottom"), ("back", "top"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")],
                             tol=2.0, ease=CAP_EASE)
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
    if wanted["stand"] and wanted["front"] and wanted["yoke"]:
        pattern.declare_seam([("stand", "neck")],
                             [("front", "neck"), ("yoke", "neck")],
                             tol=2.0, ease=OVERLAP)
    if wanted["fall"] and wanted["stand"]:
        pattern.declare_seam([("fall", "neck")], [("stand", "top")], tol=2.0)
    # Flap opening matches the pocket mouth width (appliqué balance): the flap
    # is cut the same width as the pocket top so it covers the opening exactly.
    if wanted["pocket_flap"] and wanted["chest_pocket"]:
        pattern.declare_seam(("pocket_flap", "attach"),
                             ("chest_pocket", "top"), tol=1.0)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1500.0                        # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "mezclilla-denim", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 62% marker efficiency; "
                 "chambray-weight denim work shirt with two chest flap pockets"},
        {"item": "fusible interfacing (collar stand + fall, cuffs, CF placket)",
         "qty": 1, "unit": "set",
         "note": "shirt-weight fusible; stand and fall cut doubled on fold, the "
                 "CF placket fused full length under the buttonholes"},
        {"item": "shirt buttons 11.5 mm", "qty": BUTTONS + 4, "unit": "pcs",
         "note": f"{BUTTONS} CF placket + 2 cuffs + 2 pocket-flap; hardware is a "
                 "Yantra4D cartridge (shank-button guide), never re-implemented "
                 "here"},
        {"item": "heavy topstitch thread (contrast) + jeans needle 100/16",
         "qty": 1, "unit": "set",
         "note": "workwear topstitch: fell the load-bearing side, armhole, and "
                 "yoke seams; double-topstitch the placket, yoke, collar, cuffs, "
                 "and every pocket + flap edge (3 mm gauge)"},
        {"item": "all-purpose polyester thread + universal needle 90/14",
         "qty": 1, "unit": "set", "note": "construction seams and buttonholes"},
    ]
    pattern.metadata = {
        "fc100_rank": 90,
        "fabric_hint": "mezclilla-denim",
        "half_neckline_mm": round(half_neck, 1),
        "stand_neck_target_mm": round(half_neck + OVERLAP, 1),
        "stand_top_mm": round(stand_top_len, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_target_mm": round(front_ah + back_ah + CAP_EASE, 1),
        "cap_ease_mm": CAP_EASE,
        "yoke_seam_y_mm": round(YOKE_Y, 1),
        "quarter_width_mm": round(W, 1),
        "buttons": {"count_cf": BUTTONS, "line": "CF (x=0)",
                    "placket_extension_mm": PW,
                    "flap_buttons": 2, "cuff_buttons": 2},
        "box_pleat": {"fold_lines_x": list(PLEAT_LINES_X), "length_mm": PLEAT_LEN,
                      "location": "CB, marked (teaching-grade)"},
        "collar": {"type": "two-piece turndown (stand + fall)",
                   "stand_height_mm": STAND_H, "fall_height_mm": FALL_H,
                   "solve": "stand neck → half neckline + overlap; fall neck → "
                            "stand top edge (chained)"},
        "flap_pockets": {
            "count": 2, "layout": "two chest / breast",
            "pocket_mm": [round(pocket_width, 1), round(POCKET_H, 1)],
            "flap_mm": [round(pocket_width, 1), round(FLAP_H, 1)],
            "chamfer_mm": POCKET_CHAMFER, "hem_facing_mm": POCKET_HEM,
            "attach": "topstitched appliqué — pocket body + flap are their own "
                      "closed pieces, placements traced on the front; only the "
                      "flap-to-pocket opening is a declared balance seam",
        },
        "topstitch": "heavy contrast, 3 mm gauge: CF placket, back yoke, collar, "
                     "cuffs, pocket + flap edges, and felled structural seams",
        "drafting": "slightly relaxed woven utility work shirt: one-piece "
                    "button-placket front, back ending at the yoke seam with a "
                    "marked CB box pleat, a doubled yoke carrying the back neck "
                    "and shoulders, a two-piece turndown collar (stand solved to "
                    "the half neckline + overlap, fall chained to the stand's "
                    "top edge), a set-in sleeve solved to the summed armholes + "
                    "14 mm cap ease and closed by a barrel cuff, and two real "
                    "chest flap pockets appliquéd to marked placements — "
                    "teaching-grade: full back armhole on the back piece, "
                    "sleeve placket and box pleat marked, single-layer fall and "
                    "pocket bag in v0",
    }
    return pattern


result = build()

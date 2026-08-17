"""
Denim jacket — FC-100 rank #28. Fashion Cabinet Garment Cartridge.

Trucker-style denim jacket ("chamarra de mezclilla") on the dress-shirt
architecture, cropped and boxy. Front AND back split at the chest line: front
yokes (cut 2) over button-stand front bodies carrying six buttonhole
cross-marks and chest flap-pocket markings; back yoke and back body each cut
on fold. The armholes are drafted fully on the BODY pieces, starting at the
yoke-seam corner and clear of the yokes (dress-shirt back-armhole precedent),
and the long sleeve cap is solved by bisection to their measured sum. A
one-piece band collar is solved to the measured half neckline + 15 mm button
overlap (collar-band method), rectangular buttoned cuffs close the sleeves,
and a two-half hem waistband — crossover tab + plain, the dress-trousers
method — is verified against the body hems with the tab declared as seam ease.

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
# front_yoke|front_body|back_yoke|back_body|sleeve|cuff|collar|band_tab|
# band_plain|set

chest_girth    = float(PARAM(lambda: chest_girth, 1020.0))
body_length    = float(PARAM(lambda: body_length, 620.0))    # nape to band hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 610.0))  # cap apex to wrist
woven_ease     = float(PARAM(lambda: woven_ease, 200.0))     # boxy trucker ease
chest_line     = float(PARAM(lambda: chest_line, 150.0))     # HPS to yoke seams
button_stand   = float(PARAM(lambda: button_stand, 35.0))    # extension past CF
collar_height  = float(PARAM(lambda: collar_height, 70.0))
wrist_opening  = float(PARAM(lambda: wrist_opening, 230.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
body_length = max(450.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(400.0, min(sleeve_length, 750.0))
woven_ease = max(100.0, min(woven_ease, 400.0))
chest_line = max(120.0, min(chest_line, 220.0))
button_stand = max(20.0, min(button_stand, 50.0))
collar_height = max(40.0, min(collar_height, 90.0))
wrist_opening = max(180.0, min(wrist_opening, 300.0))

# ── Boxy trucker block (dress-shirt constants, chest-line split) ─────────────
W = (chest_girth + woven_ease) / 4.0           # quarter body width
L = body_length
NW = max(60.0, neck_girth / 5.0)               # half neck width at HPS
chest_line = max(chest_line, NW + 25.0)        # keep the front neck on the yoke
AH = (chest_girth + woven_ease) / 8.0 + 140.0  # jacket-deep armhole (auto)
AH = max(AH, chest_line + 70.0)                # armhole fully below the yokes
AH = max(200.0, min(AH, L - 140.0))
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 25.0                          # HPS to CB nape (on the yoke)
FRONT_NECK_DROP = NW + 5.0
FNY = HPS_Y - FRONT_NECK_DROP                  # CF neck point height
CHEST_Y = HPS_Y - chest_line                   # yoke seam height, front + back
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
BS = button_stand
BAND_FIN = 45.0                                # finished waistband height
HEM_Y = BAND_FIN                               # bodies end at the band seam
OVERLAP = 15.0                                 # collar button extension
COLLAR_RISE = 16.0
TAB = 50.0                                     # waistband crossover-tab extra
CUFF_H = 2.0 * 55.0                            # cut doubled, folded at mid
CUFF_OVERLAP = 25.0
SLEEVE_FULLNESS = 1.15                         # pleated into the cuff
SLIT_LEN = 110.0
BUTTONS = 6


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


def _armhole(scoop):
    """Body armhole: yoke-seam corner down to the underarm (fully on the body,
    below the yoke seam — the dress-shirt back-armhole precedent)."""
    top = fc.P(W - 5.0, CHEST_Y)
    span = CHEST_Y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(top, fc.P(W - 5.0 - scoop, CHEST_Y - span * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + span * 0.30), UNDERARM)],
    )


def _front_marks():
    """CF line + six buttonhole crosses, split between the front yoke and the
    front body at the chest seam by each mark's own height."""
    yoke_marks = [fc.Internal("CF line (yoke)",
                              [fc.P(0.0, CHEST_Y), fc.P(0.0, FNY)],
                              kind="marking")]
    body_marks = [fc.Internal("CF line",
                              [fc.P(0.0, HEM_Y), fc.P(0.0, CHEST_Y)],
                              kind="marking")]
    bh_top = FNY - 70.0
    bh_bottom = HEM_Y + 55.0
    step = (bh_top - bh_bottom) / (BUTTONS - 1)
    for i in range(BUTTONS):
        y = bh_top - i * step
        dest = yoke_marks if y > CHEST_Y else body_marks
        dest += _cross(f"buttonhole-{i + 1}", 0.0, y)
    return yoke_marks, body_marks


def _flap_pocket():
    """Chest flap-pocket markings: flap + pocket rectangles and the attach
    line. Markings only in v0 — welt/flap construction is future work."""
    cx = W * 0.45
    attach = CHEST_Y - 35.0
    fw, fh = 125.0, 55.0
    pw, ph = 115.0, 115.0
    flap = [fc.P(cx - fw / 2.0, attach), fc.P(cx + fw / 2.0, attach),
            fc.P(cx + fw / 2.0, attach - fh), fc.P(cx - fw / 2.0, attach - fh),
            fc.P(cx - fw / 2.0, attach)]
    p_top = attach - fh + 10.0
    pocket = [fc.P(cx - pw / 2.0, p_top), fc.P(cx + pw / 2.0, p_top),
              fc.P(cx + pw / 2.0, p_top - ph), fc.P(cx - pw / 2.0, p_top - ph),
              fc.P(cx - pw / 2.0, p_top)]
    line = [fc.P(cx - fw / 2.0 - 6.0, attach), fc.P(cx + fw / 2.0 + 6.0, attach)]
    return [
        fc.Internal("chest flap", flap),
        fc.Internal("chest pocket", pocket),
        fc.Internal("flap attach line", line),
    ]


def build_front_yoke(marks):
    """Cut 2 mirror; carries the front neck, shoulder, and the button stand's
    top run. Straight side edge, clear of the armhole."""
    neck = fc.Edge(
        "neck",
        [fc.Line(fc.P(-BS, FNY), fc.P(0.0, FNY)),
         fc.Bezier(fc.P(0.0, FNY), fc.P(NW * 0.55, FNY),
                   fc.P(NW, FNY + (HPS_Y - FNY) * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "front_yoke",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, CHEST_Y), fc.P(-BS, FNY))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            fc.Edge("side", [fc.Line(SH_END, fc.P(W - 5.0, CHEST_Y))]),
            fc.Edge("bottom",
                    [fc.Line(fc.P(W - 5.0, CHEST_Y), fc.P(-BS, CHEST_Y))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "body match")],
        grainline=fc.Grainline(fc.P(W * 0.45, CHEST_Y + 20.0),
                               fc.P(W * 0.45, CHEST_Y + chest_line * 0.7)),
        internals=marks,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Yoke",
    )


def build_front_body(marks):
    """Cut 2 mirror; button stand continues to the band seam. Carries the full
    front armhole and the chest flap-pocket markings."""
    return fc.Piece(
        "front_body",
        [
            fc.Edge("center", [fc.Line(fc.P(-BS, HEM_Y), fc.P(-BS, CHEST_Y))]),
            fc.Edge("top", [fc.Line(fc.P(-BS, CHEST_Y), fc.P(W - 5.0, CHEST_Y))]),
            _armhole(12.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, HEM_Y))]),
            fc.Edge("hem", [fc.Line(fc.P(W, HEM_Y), fc.P(-BS, HEM_Y))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole"),
                 fc.Notch("top", 0.5, "yoke match"),
                 fc.Notch("hem", 0.5, "band match")],
        grainline=fc.Grainline(fc.P(W * 0.72, HEM_Y + 45.0),
                               fc.P(W * 0.72, CHEST_Y - 60.0)),
        internals=marks + _flap_pocket(),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Body",
    )


def build_back_yoke():
    """Cut 1 on fold; carries the back neck and both shoulders. Straight side
    edge, clear of the armhole (dress-shirt yoke precedent)."""
    nape = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(nape, fc.P(NW * 0.55, nape.y),
                   fc.P(NW, nape.y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "back_yoke",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, CHEST_Y), nape)]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            fc.Edge("side", [fc.Line(SH_END, fc.P(W - 5.0, CHEST_Y))]),
            fc.Edge("bottom",
                    [fc.Line(fc.P(W - 5.0, CHEST_Y), fc.P(0.0, CHEST_Y))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "body match")],
        grainline=fc.Grainline(fc.P(W * 0.45, CHEST_Y + 15.0),
                               fc.P(W * 0.45, CHEST_Y + chest_line * 0.7)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back Yoke",
    )


def build_back_body():
    """Cut 1 on fold; carries the full back armhole below the yoke seam."""
    return fc.Piece(
        "back_body",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, HEM_Y), fc.P(0.0, CHEST_Y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, CHEST_Y), fc.P(W - 5.0, CHEST_Y))]),
            _armhole(8.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, HEM_Y))]),
            fc.Edge("hem", [fc.Line(fc.P(W, HEM_Y), fc.P(0.0, HEM_Y))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("top", 0.5, "yoke match"),
                 fc.Notch("hem", 0.5, "band match")],
        grainline=fc.Grainline(fc.P(W * 0.6, HEM_Y + 45.0),
                               fc.P(W * 0.6, CHEST_Y - 60.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back Body",
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
    ch = max(70.0, AH * 0.30)
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
    px = chw * 0.55                              # cuff slit, back of the wrist
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
            fc.Internal("cuff slit", [fc.P(px, 0.0), fc.P(px, SLIT_LEN)],
                        kind="marking"),
            fc.Internal("slit stop",
                        [fc.P(px - 4.0, SLIT_LEN), fc.P(px + 4.0, SLIT_LEN)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_cuff():
    """Rectangular buttoned cuff, cut doubled in height and folded at mid."""
    length = wrist_opening * 0.9 + CUFF_OVERLAP + 2.0 * seam_allowance
    internals = [fc.Internal("fold line",
                             [fc.P(0.0, CUFF_H / 2.0), fc.P(length, CUFF_H / 2.0)],
                             kind="marking")]
    internals += _cross("cuff buttonhole", seam_allowance + 12.0, CUFF_H * 0.25)
    internals += _cross("cuff button", length - seam_allowance - 12.0,
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


def _collar_neck(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(half_neck):
    """One-piece band collar, half on fold at CB — the collar-band method
    verbatim: neck edge solved to the half neckline + button overlap."""
    target = half_neck + OVERLAP
    flat = _solve_flat(_collar_neck, target, "collar neck")
    neck = _collar_neck(flat)
    top_start = fc.P(0.0, collar_height)
    top_end = fc.P(flat, COLLAR_RISE + collar_height)
    t_cf = half_neck / target                    # CF button line along the neck
    return fc.Piece(
        "collar",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_RISE), top_end)]),
            fc.Edge("top",
                    [fc.curve_through(top_end, top_start, bulge=0.04, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match"),
                 fc.Notch("neck", t_cf, "CF / button line")],
        grainline=fc.Grainline(fc.P(flat * 0.2, collar_height * 0.5),
                               fc.P(flat * 0.75,
                                    collar_height * 0.5 + COLLAR_RISE * 0.7)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Collar (half, on fold)",
    )


def _band_half(name, length, label, extras):
    """One folded waistband half: a rectangle with a center fold line."""
    band_h = 2.0 * (BAND_FIN + seam_allowance)
    cy = band_h / 2.0
    fold = fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)])
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                      # ends already include the sa
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        internals=[fold] + extras,
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def build_bands(hems):
    """Two hem-waistband halves (dress-trousers method): each half covers one
    front hem + the half back hem; the tab half extends +50 into a crossover
    tab with a button cross-mark, declared as seam ease."""
    band_h = 2.0 * (BAND_FIN + seam_allowance)
    tab_len = hems + TAB + 2.0 * seam_allowance
    plain_len = hems + 2.0 * seam_allowance
    tab_line = fc.Internal(
        "tab line", [fc.P(tab_len - TAB, 0.0), fc.P(tab_len - TAB, band_h)])
    tab_extras = [tab_line] + _cross("tab button", tab_len - TAB / 2.0,
                                    band_h * 0.25)
    tab = _band_half("band_tab", tab_len, "Waistband Half (tab)", tab_extras)
    plain = _band_half("band_plain", plain_len, "Waistband Half (plain)", [])
    return tab, plain


def build():
    pattern = fc.PatternSet("denim-jacket")
    yoke_marks, body_marks = _front_marks()
    front_yoke = build_front_yoke(yoke_marks)
    front_body = build_front_body(body_marks)
    back_yoke = build_back_yoke()
    back_body = build_back_body()
    front_ah = front_body.edge("armhole").length(0.05)
    back_ah = back_body.edge("armhole").length(0.05)
    half_neck = (front_yoke.edge("neck").length(0.05)
                 + back_yoke.edge("neck").length(0.05))
    hems = (front_body.edge("hem").length(0.05)
            + back_body.edge("hem").length(0.05))
    names = ("front_yoke", "front_body", "back_yoke", "back_body", "sleeve",
             "cuff", "collar", "band_tab", "band_plain")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front_yoke"]:
        pattern.add(front_yoke)
    if wanted["front_body"]:
        pattern.add(front_body)
    if wanted["back_yoke"]:
        pattern.add(back_yoke)
    if wanted["back_body"]:
        pattern.add(back_body)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(front_ah, back_ah))
    if wanted["cuff"]:
        pattern.add(build_cuff())
    if wanted["collar"]:
        pattern.add(build_collar(half_neck))
    if wanted["band_tab"] or wanted["band_plain"]:
        tab, plain = build_bands(hems)
        if wanted["band_tab"]:
            pattern.add(tab)
        if wanted["band_plain"]:
            pattern.add(plain)
    if wanted["front_body"] and wanted["back_body"]:
        pattern.declare_seam(("front_body", "side"), ("back_body", "side"),
                             tol=1.5)
    if wanted["front_yoke"] and wanted["back_yoke"]:
        pattern.declare_seam(("front_yoke", "shoulder"),
                             ("back_yoke", "shoulder"), tol=1.5)
    if wanted["front_yoke"] and wanted["front_body"]:
        pattern.declare_seam(("front_yoke", "bottom"), ("front_body", "top"),
                             tol=1.5)
    if wanted["back_yoke"] and wanted["back_body"]:
        pattern.declare_seam(("back_yoke", "bottom"), ("back_body", "top"),
                             tol=1.5)
    if wanted["sleeve"] and wanted["front_body"] and wanted["back_body"]:
        pattern.declare_seam([("sleeve", "cap")],
                             [("front_body", "armhole"),
                              ("back_body", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
    if wanted["collar"] and wanted["front_yoke"] and wanted["back_yoke"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front_yoke", "neck"), ("back_yoke", "neck")],
                             tol=2.0, ease=OVERLAP)
    if wanted["band_tab"] and wanted["front_body"] and wanted["back_body"]:
        pattern.declare_seam([("band_tab", "bottom")],
                             [("front_body", "hem"), ("back_body", "hem")],
                             tol=2.5, ease=TAB + 2.0 * seam_allowance)
    if wanted["band_plain"] and wanted["front_body"] and wanted["back_body"]:
        pattern.declare_seam([("band_plain", "bottom")],
                             [("front_body", "hem"), ("back_body", "hem")],
                             tol=2.5, ease=2.0 * seam_allowance)
    fabric_width = 1500.0                        # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "mezclilla-denim", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 60% marker efficiency"},
        {"item": "jean tack buttons 17 mm", "qty": 9, "unit": "pcs",
         "note": "6 front + 2 cuffs + 1 band tab; hardware is a Yantra4D "
                 "cartridge (shank-button guide), never re-implemented here"},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "set", "note": "double-needle where available"},
    ]
    pattern.metadata = {
        "fc100_rank": 28,
        "fabric_hint": "mezclilla-denim",
        "half_neckline_mm": round(half_neck, 1),
        "collar_neck_mm": round(half_neck + OVERLAP, 1),
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "cap_target_mm": round(front_ah + back_ah, 1),
        "hem_half_mm": round(hems, 1),
        "band_tab_mm": round(hems + TAB + 2.0 * seam_allowance, 1),
        "band_plain_mm": round(hems + 2.0 * seam_allowance, 1),
        "buttonholes": {"count": BUTTONS, "line": "CF (x=0)",
                        "stand_extension_mm": BS},
        "topstitch": "double-needle heavy contrast (gold), 3 mm gauge: yoke "
                     "seams, button stand, flap and pocket edges, band, cuffs",
        "drafting": "trucker jacket on the dress-shirt architecture: front and "
                    "back split at the chest line into yokes + bodies; armholes "
                    "drafted fully on the body pieces below the yoke seams; "
                    "band collar solved to the half neckline + overlap; cap "
                    "solved to the summed armholes; two-half hem band, tab as "
                    "declared ease",
    }
    return pattern


result = build()

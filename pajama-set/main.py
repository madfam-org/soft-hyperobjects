"""
Pajama Set — FC-100 rank #41. Fashion Cabinet Garment Cartridge.

The commons' first TWO-GARMENT cartridge: one object drafts a complete sleep
set ("pijama (conjunto)"). `target_piece` selects the garment — "top",
"pants", or "set" (both; the default and the fallback) — and the manifest
exposes the same three as modes. Piece names are namespaced per garment
(top_front vs pant_front) so the full set coexists in one PatternSet, and
seam checks are declared only among the pieces actually rendered.

TOP — the casual-button-down drop-shoulder block at lounge ease: front cut 2
with the center edge extended `button_stand` (28 mm) past CF (four buttonhole
cross-marks on the CF line, chest patch-pocket trace), plain back cut 1 on
fold (no pleat — the sleep ease carries the fullness), a LONG sleeve (580 mm)
whose cap is solved by bisection to the front + back armholes at zero ease,
and the notched collar SIMPLIFIED to the solved one-piece band collar
inherited from casual-button-down: half on fold at CB, neck edge bisected to
one front neck (15 mm overlap past CF included) + half back neck.

PANTS — the sweatpants side-seamed block relaxed to the same lounge ease:
separate front/back legs cut 2 each, deeper back fork with the front inseam
bowed outward by a solved amount to match, equal side seams by construction,
straight open hems, and an elastic + drawstring casing waistband with two
drawstring-exit crosses straddling center front (band-end seam sits at CB).

The BOM totals BOTH garments (one marker) regardless of the rendered mode.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # top|pants|set

chest_girth    = float(PARAM(lambda: chest_girth, 1000.0))
hip_girth      = float(PARAM(lambda: hip_girth, 1000.0))
top_length     = float(PARAM(lambda: top_length, 720.0))    # nape to hem
inseam_length  = float(PARAM(lambda: inseam_length, 720.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 580.0)) # cap apex to hem
lounge_ease    = float(PARAM(lambda: lounge_ease, 180.0))   # total; both garments
front_rise     = float(PARAM(lambda: front_rise, 275.0))
back_rise      = float(PARAM(lambda: back_rise, 315.0))
hem_width      = float(PARAM(lambda: hem_width, 135.0))     # pant front half-hem
collar_height  = float(PARAM(lambda: collar_height, 60.0))
button_stand   = float(PARAM(lambda: button_stand, 28.0))   # front edge past CF
elastic_width  = float(PARAM(lambda: elastic_width, 30.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
hip_girth = max(650.0, min(hip_girth, 1800.0))
top_length = max(400.0, min(top_length, 1000.0))
inseam_length = max(300.0, min(inseam_length, 950.0))
sleeve_length = max(100.0, min(sleeve_length, 660.0))
lounge_ease = max(80.0, min(lounge_ease, 400.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
hem_width = max(90.0, min(hem_width, 260.0))
collar_height = max(40.0, min(collar_height, 90.0))
button_stand = max(20.0, min(button_stand, 40.0))
elastic_width = max(20.0, min(elastic_width, 60.0))

MODE = target_piece if target_piece in ("top", "pants", "set") else "set"

# ── Top block (casual-button-down geometry, lounge ease, derived neck) ───────
NECK = max(300.0, min(250.0 + chest_girth * 0.15, 520.0))  # derived neck girth
W = (chest_girth + lounge_ease) / 4.0          # quarter body width
L = top_length
AH = (chest_girth + lounge_ease) / 8.0 + 95.0  # drop-shoulder armhole depth
AH = max(160.0, min(AH, L - 120.0))
NW = max(60.0, NECK / 5.0)                     # half neck width at HPS
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0
BACK_NECK_DROP = 20.0
FRONT_NECK_DROP = max(65.0, NECK / 5.0 + 8.0)
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
CB_NECK_Y = HPS_Y - BACK_NECK_DROP
OVERLAP = 15.0                                 # collar end past CF (button line)
COLLAR_RISE = 14.0                             # band front-edge curl
COLLAR_POINT = 8.0                             # gentle forward lean of the band end
BUTTONHOLES = 4
POCKET_W, POCKET_H = 110.0, 120.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)

# ── Pant block (sweatpants geometry at lounge ease) ──────────────────────────
HIP_E = hip_girth + lounge_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0


def _armhole_edge():
    """Shared front/back armhole (drop-shoulder blocks keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _front_neck_edge():
    """Front neck: 15 mm overlap line past CF, then the scoop up to HPS.

    The straight run from (-OVERLAP, CF_NECK_Y) to CF is where the band collar
    ends (button line); including it in the neck edge makes the per-half seam
    check collar.neck == top_front.neck + top_back.neck close exactly.
    """
    cf = fc.P(0.0, CF_NECK_Y)
    scoop = fc.Bezier(cf, fc.P(NW * 0.55, CF_NECK_Y),
                      fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))
    return fc.Edge("neck", [fc.Line(fc.P(-OVERLAP, CF_NECK_Y), cf), scoop])


def _buttonhole_marks():
    """Four cross-marks on the CF line (x = 0), evenly spaced."""
    top = CF_NECK_Y - 60.0
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
    top = max(180.0, min(UNDERARM.y + 70.0, CF_NECK_Y - 40.0))
    bottom = max(top - POCKET_H, 40.0)
    left = W * 0.30
    right = min(left + POCKET_W, W * 0.92)
    return fc.Internal(
        "pocket placement",
        [fc.P(left, top), fc.P(right, top), fc.P(right, bottom),
         fc.P(left, bottom), fc.P(left, top)],
        kind="trace",
    )


def build_top_front():
    """Top front, cut 2 mirrored: center edge extended button_stand past CF."""
    neck = _front_neck_edge()
    cf_t = max(0.02, min(0.5, OVERLAP / neck.length(0.05)))
    return fc.Piece(
        "top_front",
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
        internals=[_pocket_trace(), *_buttonhole_marks()],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Top Front",
    )


def build_top_back():
    """Top back, cut 1 on fold at CB — plain; the lounge ease is the fullness."""
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, CB_NECK_Y), fc.P(NW * 0.55, CB_NECK_Y),
                   fc.P(NW, CB_NECK_Y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "top_back",
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
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Top Back",
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_top_sleeve(cap_target):
    """Long sleeve: cap solved by bisection to the front + back armholes."""
    ch = max(45.0, AH * 0.33)                      # shallow relaxed cap
    sl = max(60.0, sleeve_length - ch)             # underarm-to-hem length
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
    chw = max(70.0, hb * 0.72)                     # plain-hem opening half-width
    return fc.Piece(
        "top_sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Top Sleeve (long)",
    )


def _collar_neck_edge(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(half_target):
    """One-piece band collar, half on fold at CB, neck edge bisected to
    half_target = top_front.neck (one side, incl. overlap) + top_back.neck."""
    lo, hi = half_target * 0.7, half_target * 1.05
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if _collar_neck_edge(mid).length(0.05) < half_target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(_collar_neck_edge(flat).length(0.05) - half_target) > 1.0:
        raise ValueError("collar neck-edge solver did not converge")
    point = fc.P(flat + COLLAR_POINT, COLLAR_RISE + collar_height)
    top_start = fc.P(0.0, collar_height)
    piece = fc.Piece(
        "collar",
        [
            _collar_neck_edge(flat),
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_RISE), point)]),
            fc.Edge("top", [fc.curve_through(point, top_start, bulge=0.04, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(flat * 0.20, collar_height * 0.55),
                               fc.P(flat * 0.75, collar_height * 0.55 + 7.0)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Band Collar (half, on fold)",
    )
    return piece, flat


def build_pant_legs():
    """Front/back legs; front inseam bowed by a solved amount to the back."""
    f_tip = fc.P(FW + FORK_F, CROTCH_Y)
    b_tip = fc.P(BW + FORK_B, CROTCH_Y)

    def f_inseam(bulge):
        return fc.Edge("inseam", [fc.curve_through(f_tip, fc.P(FHW, 0.0),
                                                   bulge=bulge, side=-1.0)])

    b_inseam = fc.Edge("inseam", [fc.Line(b_tip, fc.P(BHW, 0.0))])
    back_len = b_inseam.length(0.05)
    lo, hi = 0.0, 0.35
    for _ in range(44):
        mid = (lo + hi) / 2.0
        if f_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(f_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge")

    def make(name, width, tip, inseam_edge, hem_w, cb_y, label):
        waist_in = width * 0.92
        edges = [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
            fc.Edge(
                "crotch",
                [fc.Bezier(fc.P(waist_in, cb_y),
                           fc.P(width - 4.0, cb_y - front_rise * 0.45),
                           fc.P(width + (tip.x - width) * 0.35, CROTCH_Y + 55.0), tip)],
            ),
            inseam_edge,
            fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))]),
        ]
        return fc.Piece(
            name,
            edges,
            seam_allowance=seam_allowance,
            allowances={"hem": hem_allowance},
            notches=[fc.Notch("inseam", 0.5), fc.Notch("side", 0.5)],
            grainline=fc.Grainline(fc.P(width * 0.45, inseam_length * 0.12),
                                   fc.P(width * 0.45, inseam_length * 0.92)),
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("pant_front", FW, f_tip, f_inseam(bulge), FHW, WAIST_Y,
                 "Pant Front Leg")
    back = make("pant_back", BW, b_tip, b_inseam, BHW,
                WAIST_Y + (back_rise - front_rise), "Pant Back Leg")
    return front, back, bulge


def _exit_cross(tag, cx, cy, half=4.0):
    """One drawstring-exit cross (two drill strokes) centred at (cx, cy)."""
    return [
        fc.Internal(f"drawstring-exit-{tag}-h",
                    [fc.P(cx - half, cy), fc.P(cx + half, cy)], kind="drill"),
        fc.Internal(f"drawstring-exit-{tag}-v",
                    [fc.P(cx, cy - half), fc.P(cx, cy + half)], kind="drill"),
    ]


def build_pant_waistband(front, back):
    """Elastic + drawstring casing cut to the measured waist; exits at CF.

    The strip seams into a loop at its ends (seam worn at CB), so the middle
    of the length is CF: the two exit crosses straddle it 40 mm apart.
    """
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    band_h = 2.0 * (elastic_width + seam_allowance)
    length = circ + 2.0 * seam_allowance
    cy = band_h / 2.0
    exits = [
        *_exit_cross("a", length / 2.0 - 20.0, cy),
        *_exit_cross("b", length / 2.0 + 20.0, cy),
    ]
    return fc.Piece(
        "pant_waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        internals=[fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)]),
                   *exits],
        cut=fc.CutSpec(quantity=1),
        label="Pant Waistband Casing (elastic + drawstring)",
    )


def build():
    pattern = fc.PatternSet("pajama-set")
    want_top = MODE in ("top", "set")
    want_pants = MODE in ("pants", "set")

    # Both garments are always drafted (the BOM totals both); only the wanted
    # ones are added to the pattern, and seams follow the added pieces.
    top_front = build_top_front()
    top_back = build_top_back()
    cap_target = (top_front.edge("armhole").length(0.05)
                  + top_back.edge("armhole").length(0.05))
    half_neck = (top_front.edge("neck").length(0.05)
                 + top_back.edge("neck").length(0.05))
    top_sleeve = build_top_sleeve(cap_target)
    collar, collar_flat = build_collar(half_neck)
    pant_front, pant_back, inseam_bulge = build_pant_legs()
    pant_waistband = build_pant_waistband(pant_front, pant_back)

    if want_top:
        for piece in (top_front, top_back, top_sleeve, collar):
            pattern.add(piece)
        pattern.declare_seam(("top_front", "side"), ("top_back", "side"), tol=1.5)
        pattern.declare_seam(("top_front", "shoulder"), ("top_back", "shoulder"),
                             tol=1.5)
        pattern.declare_seam(
            [("top_sleeve", "cap")],
            [("top_front", "armhole"), ("top_back", "armhole")],
            tol=2.0,
        )
        pattern.declare_seam(
            ("top_sleeve", "underarm_front"), ("top_sleeve", "underarm_back"), tol=1.0
        )
        pattern.declare_seam(
            [("collar", "neck")],
            [("top_front", "neck"), ("top_back", "neck")],
            tol=2.0,
        )
    if want_pants:
        for piece in (pant_front, pant_back, pant_waistband):
            pattern.add(piece)
        pattern.declare_seam(("pant_front", "side"), ("pant_back", "side"), tol=1.5)
        pattern.declare_seam(("pant_front", "inseam"), ("pant_back", "inseam"),
                             tol=1.5)

    fabric_width = 1450.0                          # popelina-algodon card width
    both = (top_front, top_back, top_sleeve, collar,
            pant_front, pant_back, pant_waistband)
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0) for p in both
    )
    marker_len = total_area / (fabric_width * 0.65)
    waist_circ = 2.0 * (pant_front.edge("waist").length()
                        + pant_back.edge("waist").length())
    elastic_len = round(waist_circ * 0.85 / 10.0) * 10
    cord_len = round((waist_circ + 500.0) / 10.0) * 10
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"BOTH garments at {fabric_width:.0f} mm width, 65% marker efficiency"},
        {"item": f"woven elastic {elastic_width:.0f} mm", "qty": elastic_len,
         "unit": "mm_length",
         "note": "pant casing; cut ~15% under the garment waist, join flat"},
        {"item": "drawstring cord (flat, 6-8 mm)", "qty": cord_len,
         "unit": "mm_length",
         "note": "threads the same casing; exits at the two CF crosses; knot the ends"},
        {"item": "shirt buttons Ø 10-12 mm", "qty": BUTTONHOLES + 1, "unit": "pieces",
         "note": "4 front + 1 spare; hard goods federate to Yantra4D (button family)"},
        {"item": "fusible interfacing (collar band + button stands)", "qty": 1,
         "unit": "set",
         "note": "band cut doubled on fold; stands fused full length"},
        {"item": "polyester thread + universal needle", "qty": 1, "unit": "set",
         "note": "sharp 80/12 for poplin; french-seam or overlock the lounge seams"},
    ]
    pattern.metadata = {
        "fc100_rank": 41,
        "fabric_hint": "popelina-algodon",
        "set_note": "two garments, one cartridge; BOM totals both",
        "mode": MODE,
        "derived_neck_girth_mm": round(NECK, 1),
        "collar_half_target_mm": round(half_neck, 1),
        "collar_flat_mm": round(collar_flat, 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "sleeve_cap_target_mm": round(cap_target, 1),
        "inseam_bulge": round(inseam_bulge, 4),
        "pant_waist_circ_mm": round(waist_circ, 1),
        "marker_length_mm": round(marker_len, 1),
        "buttonholes": BUTTONHOLES,
        "button_stand_mm": button_stand,
        "drafting": "two-garment set: casual-button-down top block (solved band "
                    "collar + long solved cap, no pleat) over the sweatpants pant "
                    "block (solved inseam bow, elastic + drawstring casing)",
    }
    return pattern


result = build()

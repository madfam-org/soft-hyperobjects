"""
Track Jacket — FC-100 rank #51. Fashion Cabinet Garment Cartridge.

The classic zip-up athletic jacket: the zip-hoodie / bomber architecture
(rank #14 / #29) — front cut as TWO mirrored halves whose center edge is the
zipper seam (15 mm tape allowance, top/bottom stop notches, 7 mm stitch line),
a set-in sleeve whose cap is SOLVED by bisection against the measured armhole
pair, and cuff + split hem bands DERIVED from the measured openings — but the
hood/rib-collar is replaced with a SOLVED STAND COLLAR (funnel / mock-neck).
The collar is the differentiator: a curved band cut on fold at CB whose NECK
EDGE is bisection-solved (collar-band method) to the HALF neck opening so the
collar↔neckline seam balances with delta ≈ 0, and whose center-front edges
carry the SAME zipper tape allowance — the separating zipper runs up through
the collar. Fit is RELAXED: a small POSITIVE ease is added to the chest girth;
this is NOT a compression cut, so the power-stretch card's negative cut_scale
is deliberately NOT applied (the interlock only lends comfort give). Optional
front zip pockets are marked as welt/zip openings. The separating zipper and
the pocket zips are Yantra4D solids, federated through the zipper-notion
cartridge (never drafted here).

Idioms borrowed:
  - zip-hoodie / bomber-jacket: halved-at-CF zip front (tape allowance, stop
    notches, stitch line), set-in sleeve cap solved to the armhole pair, split
    hem band + cuffs derived from measured openings, derived zipper length.
  - collar-band: a stand collar whose neck edge is bisection-solved to the
    measured opening (here HALF the opening, since the collar is cut on fold).
  - track-pants: RELAXED technical fit (positive ease, no compression scale)
    and exact-mm notion accounting in the BOM.

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
# front | back | sleeve | collar | cuff | hem_band | set

chest_girth   = float(PARAM(lambda: chest_girth, 1020.0))
body_length   = float(PARAM(lambda: body_length, 660.0))   # nape to hem-band seam
neck_girth    = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))  # to cuff seam
relaxed_ease  = float(PARAM(lambda: relaxed_ease, 170.0))   # POSITIVE ease at the chest
collar_height = float(PARAM(lambda: collar_height, 70.0))   # funnel / mock-neck stand
collar_rise   = float(PARAM(lambda: collar_rise, 12.0))     # CF curl of the stand
cuff_ratio    = float(PARAM(lambda: cuff_ratio, 0.80))      # cuff / sleeve-hem opening
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.88))   # hem band / hem circumference
cuff_height   = float(PARAM(lambda: cuff_height, 60.0))
hemband_height = float(PARAM(lambda: hemband_height, 60.0))
pockets        = bool(PARAM(lambda: pockets, True))          # front zip pockets (markings)
seam_allowance = float(PARAM(lambda: seam_allowance, 9.0))

# ── Clamps (mirror the manifest sliders) ─────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(200.0, min(sleeve_length, 780.0))
relaxed_ease = max(80.0, min(relaxed_ease, 400.0))
collar_height = max(35.0, min(collar_height, 130.0))
collar_rise = max(0.0, min(collar_rise, 30.0))
cuff_ratio = max(0.60, min(cuff_ratio, 0.95))
hemband_ratio = max(0.70, min(hemband_ratio, 1.0))
cuff_height = max(30.0, min(cuff_height, 100.0))
hemband_height = max(30.0, min(hemband_height, 100.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# ── Derived draft dimensions ─────────────────────────────────────────────────
# POSITIVE ease → relaxed fit. The power-stretch interlock lends comfort give;
# this is NOT a compression cut, so the fabric card's cut_scale < 1.0 (negative
# ease) is deliberately NOT applied here (see metadata fit_note).
CHEST_E = chest_girth + relaxed_ease
W = CHEST_E / 4.0                      # quarter body width (fold at CB / CF at x=0)
L = body_length
AH = CHEST_E / 8.0 + 105.0             # armhole depth (HPS line to underarm)
AH = max(180.0, min(AH, L - 100.0))
NW = max(60.0, neck_girth / 5.0 + 4.0)  # neck half-width at the shoulder
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 30.0)
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 80.0
BACK_NECK_DROP = 20.0
ZIP_SA = 15.0          # tape allowance on the front / collar center edge (zip seam)
ZIP_STITCH = 7.0       # stitch line offset from the seam line (zipper-notion)
ZIP_STOP_INSET = 10.0  # stop notches sit this far inside the seam ends


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
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


def _pocket_marks():
    """Front zip-pocket marking: a near-vertical welt opening + surround box.

    A slightly slanted hand-warmer opening on each front half — upper end toward
    center front, lower end toward the side seam (the hand enters downward and
    outward). The zip is a separating pocket zip; hardware via zipper-notion.
    """
    cx = min(W * 0.52, W - 70.0)
    cy = max(120.0, min(L * 0.34, UNDERARM.y - 90.0))
    half = 70.0                                     # half the opening length
    along = fc.P(0.28, 0.96)                        # near-vertical, top toward CF
    perp = fc.P(0.96, -0.28)                        # box depth direction
    p_top = fc.P(cx - along.x * half, cy + along.y * half)   # upper (CF side)
    p_bot = fc.P(cx + along.x * half, cy - along.y * half)   # lower (side-seam side)
    opening = fc.Internal("front zip pocket opening", [p_top, p_bot], kind="trace")
    e1 = p_top + along * 10.0
    e2 = p_bot - along * 10.0
    corners = [e1 + perp * 18.0, e2 + perp * 18.0, e2 - perp * 18.0, e1 - perp * 18.0]
    box = fc.Internal("front zip pocket box", corners + corners[:1])
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
    internals = [stitch]
    if pockets:
        internals += _pocket_marks()
    return fc.Piece(
        "front",
        _body_edges(FRONT_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance, "center": ZIP_SA},
        notches=[
            fc.Notch("side", 0.5), fc.Notch("armhole", 0.5),
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
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


SLEEVE_EASE = 12.0     # set-in cap ease over the armhole (declared on the seam)


def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12), fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch), fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
    """Set-in sleeve; the cap is solved by bisection to the measured armhole pair.

    A small ease (`SLEEVE_EASE`) is intentionally carried on the cap over the
    armhole — a set-in cap is eased into the armhole. It is declared on the seam
    so the balance check accounts for it (delta ≈ 0 against target + ease).
    """
    ch = max(50.0, AH * 0.30)
    sl = max(100.0, sleeve_length - ch)
    goal = cap_target + SLEEVE_EASE
    lo, hi = 20.0, goal / 2.0 + ch + 60.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < goal:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - goal) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(90.0, hb * 0.62)
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
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (set-in)",
    )


def _collar_neck(flat_len):
    """Collar neck (inner) edge on the +x half: solved to the half opening.

    A gentle curve from CB fold (x=0) out to the CF corner. The stand rises a
    little at CF (`collar_rise`) so the funnel wraps to the throat. side=-1 bows
    the curve toward the neck, matching the body's neckline sweep.
    """
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat_len, collar_rise),
                          bulge=0.06, side=-1.0)],
    )


def build_collar(half_opening):
    """Stand / funnel collar, cut on fold at CB; neck edge SOLVED to half opening.

    The collar-band method: bisect the flat run of the neck edge until its arc
    length equals the HALF neck opening (one front-half neck + one back-half
    neck). The CF edge is the zipper edge — it carries the SAME 15 mm tape
    allowance as the front center, because the separating zipper runs up through
    the collar. Cut on fold at CB means the drafted half doubles into the full
    stand; the declared seam balances one collar-half against one front + one
    back neck (delta ≈ 0).
    """
    lo, hi = half_opening * 0.70, half_opening * 1.08
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if _collar_neck(mid).length(0.05) < half_opening:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(_collar_neck(flat).length(0.05) - half_opening) > 1.0:
        raise ValueError("collar neck-edge solver did not converge")
    neck = _collar_neck(flat)
    cf_bottom = fc.P(flat, collar_rise)
    cf_top = fc.P(flat, collar_rise + collar_height)
    cb_top = fc.P(0.0, collar_height)
    piece = fc.Piece(
        "collar",
        [
            neck,                                              # CB fold → CF (inner)
            fc.Edge("front_edge", [fc.Line(cf_bottom, cf_top)]),   # CF zip edge
            fc.Edge("top", [fc.curve_through(cf_top, cb_top, bulge=0.04, side=1.0)]),
            fc.Edge("cb", [fc.Line(cb_top, fc.P(0.0, 0.0))]),      # center-back fold
        ],
        seam_allowance=seam_allowance,
        allowances={"front_edge": ZIP_SA},   # zipper runs up through the collar
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(flat * 0.25, collar_height * 0.5),
                               fc.P(flat * 0.75, collar_height * 0.5 + collar_rise * 0.5)),
        internals=[fc.Internal("collar fold / roll line",
                               [fc.P(0.0, collar_height * 0.5),
                                fc.P(flat, collar_rise + collar_height * 0.5)])],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Stand Collar (funnel, on fold)",
    )
    return piece, flat


def _band(name, finished_len, finished_height, qty, label, notches=None):
    """Rectangular fold-over band (cuff or split hem band), elastic/rib-recovered."""
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
        notches=list(notches or []),
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("track-jacket")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    # HALF opening = one front-half neck + one back-half neck. The collar is cut
    # on fold, so its drafted (half) neck edge is solved to exactly this length.
    half_opening = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    # Full neck opening = TWO front halves (cut 2) + the folded back's two halves.
    neck_opening = 2.0 * half_opening

    everything = target_piece == "set"

    # Bands + collar are built up-front so declared seams can read exact edge
    # lengths. Bands carry their own join allowance (2 x sa) and are drafted
    # SMALLER than their opening (rib/elastic recovers), so the seam balances
    # via an exact measured `ease`, not a fudged tolerance.
    sleeve = build_sleeve(cap_target)
    collar, collar_flat = build_collar(half_opening)
    cuff = _band("cuff", sleeve.edge("hem").length() * cuff_ratio, cuff_height, 2,
                 "Cuff (rib/elastic)")
    hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
    # The hem band is SPLIT for the zipper: cut flat, ends open at center front;
    # the center notch (= center back when worn) marks the gap.
    cbz = fc.Notch("bottom", 0.5, "center back; zipper gap at the ends")
    hem_band = _band("hem_band", hem_circ * hemband_ratio, hemband_height, 1,
                     "Hem Band (split rib/elastic)", notches=[cbz])

    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "collar":
        pattern.add(collar)
    if everything or target_piece == "cuff":
        pattern.add(cuff)
    if everything or target_piece == "hem_band":
        pattern.add(hem_band)

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
        # One collar-half (on fold) sews to one front-half neck + one back-half
        # neck; the folded/doubled collar and the cut-2 front make the full ring.
        pattern.declare_seam([("collar", "neck")],
                             [("front", "neck"), ("back", "neck")], tol=1.5)
        # One cuff (a ring) closes one sleeve hem. ease is negative: the cuff is
        # smaller than the sleeve opening (rib recovers).
        cuff_ease = cuff.edge("bottom").length() - sleeve.edge("hem").length()
        pattern.declare_seam(("cuff", "bottom"), ("sleeve", "hem"),
                             tol=1.5, ease=cuff_ease)
        # The split hem band sews onto the whole hem = 2 x (front hem + back hem).
        # ease is negative (band drafted under the hem circumference).
        hemband_ease = hem_band.edge("bottom").length() - hem_circ
        pattern.declare_seam(
            ("hem_band", "bottom"),
            [("front", "hem"), ("front", "hem"), ("back", "hem"), ("back", "hem")],
            tol=1.5, ease=hemband_ease,
        )

    # ── Notion accounting (exact-mm factory spec numbers) ────────────────────
    # Separating zipper: runs the full CF opening + the split hem band's height +
    # up through the collar's CF edge. Order to the nearest 10 mm.
    zip_total = front.edge("center").length() + hemband_height + collar_height
    zipper_len = int(round(zip_total / 10.0) * 10)
    cuff_len_each = round(sleeve.edge("hem").length() * cuff_ratio)
    hemband_len = round(hem_circ * hemband_ratio)
    pocket_zip_len = 140  # ~140 mm closed-end pocket zips

    fabric_width = 1550.0                                 # power-stretch card width
    body_area = (front.area() * 2.0) + back.area() * 2.0  # front cut 2; back on fold
    trims_area = sleeve.area() * 2.0 + collar.area() * 2.0 + cuff.area() * 2.0 \
        + hem_band.area()
    marker_len = (body_area + trims_area) / (fabric_width * 0.62)   # knits nest tight

    bom = [
        {"item": "poliester-elastano-compresion",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"relaxed track jacket at {fabric_width:.0f} mm width, ~62% marker "
                 "efficiency; greatest stretch weft (around the body). Small POSITIVE "
                 "ease — RELAXED fit, NOT a compression cut, so the card's cut_scale "
                 "(negative ease) is deliberately NOT applied"},
        {"item": "separating zipper", "qty": zipper_len, "unit": "mm_length",
         "note": f"order this SEPARATING (open-end) zipper, ~{zipper_len} mm = CF "
                 f"opening + {hemband_height:.0f} mm hem band + {collar_height:.0f} mm "
                 "collar; the zip runs up through the stand collar. Slider/pull/teeth "
                 "HARDWARE is a Yantra4D cartridge reference (zipper-notion), not "
                 "drafted here"},
        {"item": f"cuff rib/elastic {cuff_height:.0f} mm", "qty": round(2.0 * cuff_height),
         "unit": "mm_length",
         "note": f"2 cuffs cut {cuff_len_each} mm each (sleeve hem "
                 f"{sleeve.edge('hem').length():.0f} mm x {cuff_ratio:.2f}); self-rib "
                 "or knit tube folded to 2 x cuff_height"},
        {"item": f"hem band rib/elastic {hemband_height:.0f} mm",
         "qty": round(2.0 * hemband_height), "unit": "mm_length",
         "note": f"1 split band cut {hemband_len} mm (hem circumference "
                 f"{hem_circ:.0f} mm x {hemband_ratio:.2f}); ends open at CF for the "
                 "zipper, center-back notch marks the gap"},
        {"item": "stretch/wooly thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11; flatlock or 3-thread overlock + coverstitch the "
                 "band and cuff joins to avoid chafe (per the fabric card)"},
    ]
    if pockets:
        bom.append({"item": "pocket zips", "qty": 2, "unit": "pieces",
                    "note": f"two ~{pocket_zip_len} mm closed-end pocket zips (one per "
                            "front); HARDWARE is a Yantra4D cartridge reference "
                            "(zipper-notion), not drafted here — set at the two marked "
                            "front zip-pocket openings"})
    pattern.bom = bom

    pattern.metadata = {
        "fc100_rank": 51,
        "fabric_hint": "poliester-elastano-compresion",
        "fit_note": "RELAXED zip-up jacket with small positive ease (relaxed_ease "
                    "added to the chest girth) — NOT a compression cut; the technical "
                    "power-stretch interlock only lends comfort stretch, so the fabric "
                    "card's negative cut_scale is deliberately not applied",
        "collar_note": "SOLVED stand collar (funnel / mock-neck): the neck edge is "
                       "bisection-solved (collar-band method) to the HALF neck opening; "
                       "cut on fold at CB, its CF edge carries the 15 mm zipper tape "
                       "allowance because the separating zipper runs up through it",
        "closure_note": "full-length CENTER-FRONT separating zipper; the front is cut "
                        "2 (never on fold) with a 15 mm tape allowance, 7 mm stitch "
                        "line and top/bottom stop notches on the center edge",
        "neck_opening_mm": round(neck_opening, 1),
        "collar_half_solved_mm": round(collar_flat, 1),
        "collar_height_mm": collar_height,
        "armhole_pair_mm": round(cap_target, 1),
        "sleeve_cap_ease_mm": SLEEVE_EASE,
        "zipper_length_mm": zipper_len,
        "cuff_length_each_mm": cuff_len_each,
        "hemband_length_mm": hemband_len,
        "pockets": pockets,
        "drafting": "zip-hoodie / bomber block halved at CF for the separating zipper; "
                    "set-in cap solved to the armhole pair (with ease); split hem band "
                    "+ cuffs derived from measured openings; hood/rib-collar replaced "
                    "with a collar-band-solved funnel stand collar the zip runs through",
    }
    return pattern


result = build()

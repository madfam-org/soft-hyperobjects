"""
School Polo — FC-100 rank #95. Fashion Cabinet Garment Cartridge.

A children's uniform polo: the polo-shirt block scaled to child proportions
(smaller girths, shorter body/sleeve — the kids-tee scale) with a neat,
uniform-appropriate fit. It keeps the two signatures of a polo:

  1. A short CF button PLACKET (2–3 buttons) — two placement lines plus evenly
     spaced buttonhole crosses on the folded front, faced by a separate backing
     strip. The CF-side line rides the fold; the slash opens on centre.
  2. A folded RIB COLLAR band, solved to the measured neck opening by a
     rib-stretch ratio (negative ease — the band is knit shorter than the
     opening and stretches on, exactly like a real 1×1 rib collar). A
     halves-on-both-sides seam check enforces the fit at render time.

Plus the classic school-polo cut: short set-in sleeves finished with rib
bands, side VENTS at the hem (the side seam sews only from the underarm down to
the vent top; below that front and back are independent finished edges), and a
slightly dropped back hem — the "tennis tail" — for tuck-in coverage.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `chest_girth`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr —
    they are not in the sandbox's allowed builtins.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

# Child defaults (~age 7–8 uniform): smaller girths, shorter body & sleeve.
chest_girth    = float(PARAM(lambda: chest_girth, 700.0))     # full chest
body_length    = float(PARAM(lambda: body_length, 460.0))     # nape to front hem
neck_girth     = float(PARAM(lambda: neck_girth, 300.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 150.0))   # cap apex to hem
knit_ease      = float(PARAM(lambda: knit_ease, 60.0))        # total (neat fit)
placket_length = float(PARAM(lambda: placket_length, 110.0))  # CF neck point down
placket_width  = float(PARAM(lambda: placket_width, 28.0))
collar_height  = float(PARAM(lambda: collar_height, 55.0))    # finished rib collar height
collar_ratio   = float(PARAM(lambda: collar_ratio, 0.88))     # rib length / neck opening
button_count   = int(PARAM(lambda: button_count, 2))          # 2 or 3 buttons
back_tail_drop = float(PARAM(lambda: back_tail_drop, 20.0))   # tennis-tail extra length
vent_height    = float(PARAM(lambda: vent_height, 40.0))      # side vent opening height
cuff_height    = float(PARAM(lambda: cuff_height, 22.0))      # finished sleeve rib band
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (mirror the manifest slider min/max exactly) ──────────────────────
chest_girth = max(500.0, min(chest_girth, 1000.0))
body_length = max(320.0, min(body_length, 620.0))
neck_girth = max(240.0, min(neck_girth, 400.0))
sleeve_length = max(70.0, min(sleeve_length, 320.0))
knit_ease = max(-40.0, min(knit_ease, 200.0))
placket_length = max(60.0, min(placket_length, 180.0))
placket_width = max(18.0, min(placket_width, 40.0))
collar_height = max(35.0, min(collar_height, 80.0))
collar_ratio = max(0.75, min(collar_ratio, 1.0))
button_count = max(2, min(button_count, 3))
back_tail_drop = max(0.0, min(back_tail_drop, 60.0))
vent_height = max(0.0, min(vent_height, 90.0))
cuff_height = max(0.0, min(cuff_height, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))
hem_allowance = max(0.0, min(hem_allowance, 40.0))

# ── Derived block geometry (child block, drop-shoulder knit) ─────────────────
W = (chest_girth + knit_ease) / 4.0          # quarter body width (fold at CF/CB)
L = body_length                              # front nape-to-hem
AH = (chest_girth + knit_ease) / 8.0 + 60.0  # child armhole depth
AH = max(110.0, min(AH, L - 80.0))
NW = max(45.0, neck_girth / 5.0)             # half neck width on the fold
HPS_Y = L + 15.0                             # high point shoulder above nape line
SHOULDER_DROP = 24.0                         # child shoulder slope
FRONT_NECK_DROP = 62.0
BACK_NECK_DROP = 16.0                        # HPS to CB nape
SH_END = fc.P(W - 4.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
# The sewn side seam runs from the underarm down to the vent top; below it the
# front & back hems are independent finished edges (the vent + tennis tail).
# Vent height is measured up from the FRONT hem (y=0); keep the vent top a safe
# margin below the underarm and always above the front hem (min 8 mm of vent so
# the front `vent` edge is never degenerate).
VENT_TOP_Y = min(max(vent_height, 8.0), UNDERARM.y - 20.0)
CAP_EASE = 0.0                               # knit cap sewn flat, no cap ease


def _armhole_edge():
    """Shared front/back armhole curve (drop-shoulder knits keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 11.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _buttonhole_cross(cx, cy, i, half=4.0):
    """A '+' drill mark drawn as one polyline (return strokes retrace the bars)."""
    pts = [fc.P(cx - half, cy), fc.P(cx + half, cy), fc.P(cx, cy),
           fc.P(cx, cy + half), fc.P(cx, cy - half)]
    return fc.Internal(f"buttonhole {i}", pts, kind="drill")


def _placket_internals(cf_neck_y):
    """Placket box on the folded front: two vertical edges + N buttonhole marks.

    The CF-side line rides the fold (the slash opens on centre); the second line
    sits placket_width away. Buttonholes are evenly spaced down the box: the top
    one sits ~1/(N+1) below the neck, so N=2 → thirds, N=3 → quarters.
    """
    y_top, y_bot = cf_neck_y, cf_neck_y - placket_length
    marks = [
        fc.Internal("placket edge (CF)", [fc.P(0.0, y_top), fc.P(0.0, y_bot)]),
        fc.Internal("placket edge", [fc.P(placket_width, y_top), fc.P(placket_width, y_bot)]),
    ]
    for i in range(1, button_count + 1):
        cy = cf_neck_y - placket_length * i / (button_count + 1)
        marks.append(_buttonhole_cross(placket_width / 2.0, cy, i))
    return marks


def _body_piece(name, neck_edge, neck_top_y, hem_y, label, internals=None):
    """A body half. The side splits into a sewn `side` (underarm→vent top) and a
    finished `vent` (vent top→hem); `hem_y` lets the back drop for the tennis
    tail. CF/CB is the fold at x=0; hem runs along y=hem_y back to the fold."""
    origin = fc.P(0.0, hem_y)
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck_edge,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, VENT_TOP_Y))]),
        fc.Edge("vent", [fc.Line(fc.P(W, VENT_TOP_Y), fc.P(W, hem_y))]),
        fc.Edge("hem", [fc.Line(fc.P(W, hem_y), origin)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, f"{name} armhole")],
        grainline=fc.Grainline(fc.P(W * 0.58, hem_y + 40.0), fc.P(W * 0.58, HPS_Y - 60.0)),
        internals=internals or [],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    cf_neck_y = HPS_Y - FRONT_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, cf_neck_y), fc.P(NW * 0.55, cf_neck_y),
                   fc.P(NW, cf_neck_y + FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    return _body_piece("front", neck, cf_neck_y, 0.0, "Front",
                       internals=_placket_internals(cf_neck_y))


def build_back():
    cb_neck_y = HPS_Y - BACK_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, cb_neck_y), fc.P(NW, HPS_Y), bulge=0.12, side=-1.0)],
    )
    # Tennis tail: the back hem drops below the front hem line (y < 0).
    return _body_piece("back", neck, cb_neck_y, -back_tail_drop, "Back")


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    ch = max(35.0, AH * 0.33)                       # shallow knit cap
    sl = max(45.0, sleeve_length - ch)              # underarm-to-hem length
    lo, hi = 15.0, cap_target / 2.0 + ch + 50.0
    hb = hi
    for _ in range(48):                             # bisect: cap length grows with hb
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs target {cap_target:.1f}"
        )
    chw = max(45.0, min(hb * 0.9, hb))              # half hem width (rib band attaches)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
        fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
        _cap_curve(hb, sl, ch),
        fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
    ]
    return fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},         # rib band finishes the hem
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 25.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_collar(opening):
    """Folded RIB COLLAR band, solved to the neck opening by a rib-stretch ratio.

    The band is a rectangle folded lengthwise when sewn (like a rib neckband but
    taller). Its stitched neck edge is knit shorter than the opening — negative
    ease — so it stretches on: neck length = opening × collar_ratio. The seam
    check records that negative ease so delta ≈ 0. `2 × collar_height` tall,
    plus a small stand rise so the folded band reads as a stand collar."""
    neck_len = opening * collar_ratio + 2.0 * seam_allowance
    band_h = 2.0 * collar_height
    return fc.Piece(
        "collar",
        [
            fc.Edge("neck", [fc.Line(fc.P(0.0, 0.0), fc.P(neck_len, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(neck_len, 0.0), fc.P(neck_len, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(neck_len, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.25, "CB fold"), fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(neck_len * 0.2, band_h / 2.0),
                               fc.P(neck_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(neck_len, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Collar (rib band)",
    )


def build_placket_backing():
    """Facing strip behind the placket slash: (length + 25) tall, 2× width wide."""
    w = 2.0 * placket_width
    h = placket_length + 25.0
    return fc.Piece(
        "placket_backing",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("side_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("side_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                         # strip already includes finishing
        grainline=fc.Grainline(fc.P(w * 0.3, h * 0.12), fc.P(w * 0.3, h * 0.88)),
        internals=[fc.Internal(
            "CF slash line",
            [fc.P(w / 2.0, h), fc.P(w / 2.0, h - placket_length)],
        )],
        cut=fc.CutSpec(quantity=1),
        label="Placket Backing (interfaced)",
    )


def build_cuff(sleeve_hem_len):
    """Ribbed sleeve band derived from the sleeve hem (folded lengthwise)."""
    length = sleeve_hem_len * collar_ratio + 2.0 * seam_allowance
    band_h = 2.0 * cuff_height
    return fc.Piece(
        "cuff",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                         # band length already includes joins
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=2),
        label="Sleeve Band (rib)",
    )


def build():
    pattern = fc.PatternSet("school-polo")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    opening = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    sleeve = build_sleeve(cap_target)
    collar = build_collar(opening)
    want_cuff = cuff_height > 0.0
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "collar": target_piece in ("collar", "set"),
        "placket_backing": target_piece in ("placket_backing", "set"),
        "cuff": target_piece in ("cuff", "set") and want_cuff,
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
        wanted["cuff"] = wanted["cuff"] and want_cuff
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(sleeve)
    if wanted["collar"]:
        pattern.add(collar)
    if wanted["placket_backing"]:
        pattern.add(build_placket_backing())
    if wanted["cuff"]:
        pattern.add(build_cuff(sleeve.edge("hem").length()))

    # ── Seams (every sewn relationship declared; deltas ≈ 0) ──────────────────
    if wanted["front"] and wanted["back"]:
        # Side seam runs only from the underarm to the vent top (vents + tail
        # are independent finished edges below). Front & back sides are equal.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0, ease=CAP_EASE,
        )
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        # Rib collar band stitched to the full neck opening. The band is knit
        # shorter (negative ease) and stretches on: record that ease so the
        # length check balances instead of loosening tolerance.
        collar_neck = collar.edge("neck").length(0.05)
        pattern.declare_seam(
            [("collar", "neck")],
            [("front", "neck"), ("back", "neck")],
            tol=1.5, ease=collar_neck - opening,
        )
    if wanted["cuff"] and wanted["sleeve"]:
        # Rib sleeve band stitched to the sleeve hem, negative-eased likewise.
        cuff = pattern.piece("cuff")
        sleeve_hem = sleeve.edge("hem").length(0.05)
        pattern.declare_seam(
            [("cuff", "bottom")],
            [("sleeve", "hem")],
            tol=1.5, ease=cuff.edge("bottom").length(0.05) - sleeve_hem,
        )

    # ── BOM ───────────────────────────────────────────────────────────────────
    fabric_width = 1600.0                       # jersey-algodon card width
    rib_pieces = ("collar", "cuff")             # knitted trims, not from the marker
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces if p.name not in rib_pieces
    )
    marker_len = total_area / (fabric_width * 0.70)   # knits nest tightly
    pattern.bom = [
        {"item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"cotton pique/jersey at {fabric_width:.0f} mm width, 70% marker efficiency; "
                 f"cut with weft stretch around the body"},
        {"item": "1x1 rib for collar + sleeve bands", "qty": 1 + (2 if want_cuff else 0),
         "unit": "strip",
         "note": "self-fabric rib knit; one folded collar band"
                 + (" + two sleeve bands" if want_cuff else "") + "; see piece dimensions"},
        {"item": "fusible knit interfacing", "qty": 1, "unit": "strip",
         "note": f"placket backing {2 * placket_width:.0f} x {placket_length + 25:.0f} mm; "
                 f"stabilises the buttonhole slash"},
        {"item": "11 mm flat 2-hole buttons", "qty": button_count, "unit": "pieces",
         "note": f"placket closure; hardware is a Yantra4D cartridge reference "
                 f"(shank-button / flat-button), not modelled here; "
                 f"{button_count} buttonhole crosses marked on the front"},
        {"item": "stretch thread + ballpoint needle", "qty": 1, "unit": "set",
         "note": "polyester woolly / stretch thread, ballpoint 70/10 for jersey"},
    ]

    # ── Metadata ────────────────────────────────────────────────────────────────
    collar_neck_solved = collar.edge("neck").length(0.05)
    pattern.metadata = {
        "fc100_rank": 95,
        "fabric_hint": "jersey-algodon",
        "family": "kids_baby",
        "proportion": "child block (~age 7-8 uniform default); girths & lengths "
                      "scaled to the kids-tee range",
        "neck_opening_mm": round(opening, 1),
        "collar_rib_ratio": round(collar_ratio, 3),
        "collar_neck_solved_mm": round(collar_neck_solved, 1),
        "collar_negative_ease_mm": round(collar_neck_solved - opening, 1),
        "collar_finished_height_mm": round(collar_height, 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "sleeve_cap_solved_mm": round(sleeve.edge("cap").length(0.05), 1),
        "placket_box_mm": [round(placket_length, 1), round(placket_width, 1)],
        "buttons": button_count,
        "back_tail_drop_mm": round(back_tail_drop, 1),
        "side_vent_height_mm": round(vent_height, 1),
        "sleeve_band": "rib" if want_cuff else "hemmed",
        "uniform_note": "uniform-appropriate neat fit; rib collar + short placket "
                        "are the two tier-2 constructions a school polo teaches",
        "drafting": "teaching-grade child knit block; polo placket marked + faced, "
                    "rib collar & sleeve bands solved by rib-stretch ratio (negative "
                    "ease), sleeve cap solved by bisection to the armholes, side vents "
                    "+ tennis tail as independent finished edges",
    }
    return pattern


result = build()

"""
Polo Shirt — FC-100 rank #3. Fashion Cabinet Garment Cartridge.

The t-shirt knit block grown into tier 2: front on fold with a marked button
PLACKET (two placement lines + three buttonhole crosses) backed by a separate
facing strip, a flat pointed COLLAR whose neck edge is SOLVED by bisection to
half the measured neck opening, and a short sleeve whose cap is SOLVED to the
front + back armholes and finished with a derived rib cuff band.

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

chest_girth    = float(PARAM(lambda: chest_girth, 1000.0))
body_length    = float(PARAM(lambda: body_length, 700.0))     # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 390.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 210.0))   # cap apex to hem
knit_ease      = float(PARAM(lambda: knit_ease, 80.0))        # total
placket_length = float(PARAM(lambda: placket_length, 150.0))  # CF neck point down
placket_width  = float(PARAM(lambda: placket_width, 32.0))
collar_height  = float(PARAM(lambda: collar_height, 75.0))    # flat collar height
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(600.0, min(chest_girth, 1800.0))
body_length = max(400.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(80.0, min(sleeve_length, 700.0))
knit_ease = max(-80.0, min(knit_ease, 300.0))
placket_length = max(60.0, min(placket_length, 260.0))
placket_width = max(20.0, min(placket_width, 50.0))
collar_height = max(40.0, min(collar_height, 110.0))

W = (chest_girth + knit_ease) / 4.0          # quarter body width (fold at CF/CB)
L = body_length
AH = (chest_girth + knit_ease) / 8.0 + 95.0
AH = max(160.0, min(AH, L - 120.0))
NW = max(60.0, neck_girth / 5.0)             # half neck width on the fold
HPS_Y = L + 20.0                             # high point shoulder above nape line
SHOULDER_DROP = 35.0
FRONT_NECK_DROP = 85.0
BACK_NECK_DROP = 20.0                        # HPS to CB nape
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
COLLAR_RISE = 10.0                           # slight front-edge curl of the flat collar
COLLAR_POINT = 20.0                          # pointed front: edge angles outward this much
CUFF_RATIO = 0.85                            # rib cuff length / sleeve hem length
CUFF_HEIGHT = 25.0                           # finished cuff height


def _armhole_edge():
    """Shared front/back armhole curve (drop-shoulder knits keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _buttonhole_cross(cx, cy, i, half=5.0):
    """A '+' drill mark drawn as one polyline (return strokes retrace the bars)."""
    pts = [fc.P(cx - half, cy), fc.P(cx + half, cy), fc.P(cx, cy),
           fc.P(cx, cy + half), fc.P(cx, cy - half)]
    return fc.Internal(f"buttonhole {i}", pts, kind="drill")


def _placket_internals(cf_neck_y):
    """Placket box on the folded front: two vertical edges + 3 buttonhole marks.

    The CF-side line rides the fold (the slash opens on center); the second
    line sits placket_width away. Buttonholes are evenly spaced on the box
    centerline at 1/4, 2/4, 3/4 of the placket length.
    """
    y_top, y_bot = cf_neck_y, cf_neck_y - placket_length
    marks = [
        fc.Internal("placket edge (CF)", [fc.P(0.0, y_top), fc.P(0.0, y_bot)]),
        fc.Internal("placket edge", [fc.P(placket_width, y_top), fc.P(placket_width, y_bot)]),
    ]
    for i in (1, 2, 3):
        cy = cf_neck_y - placket_length * i / 4.0
        marks.append(_buttonhole_cross(placket_width / 2.0, cy, i))
    return marks


def _body_piece(name, neck_edge, neck_top_y, label, internals=None):
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck_edge,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, f"{name} armhole")],
        grainline=fc.Grainline(fc.P(W * 0.62, 80.0), fc.P(W * 0.62, L - 120.0)),
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
    return _body_piece("front", neck, cf_neck_y, "Front",
                       internals=_placket_internals(cf_neck_y))


def build_back():
    cb_neck_y = HPS_Y - BACK_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, cb_neck_y), fc.P(NW, HPS_Y), bulge=0.12, side=-1.0)],
    )
    return _body_piece("back", neck, cb_neck_y, "Back")


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    ch = max(45.0, AH * 0.33)                       # shallow knit cap
    sl = max(60.0, sleeve_length - ch)              # underarm-to-hem length
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
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
    chw = max(60.0, min(hb * 0.85, hb))             # half hem width (cuff attaches)
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
        allowances={"hem": seam_allowance},         # rib cuff band finishes the hem
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def _collar_neck_edge(flat_len):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat_len, COLLAR_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(half_target):
    """Flat pointed collar (half, on fold at CB); neck edge solved to the half
    neck opening with zero overlap — the placket carries the closure."""
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
    neck = _collar_neck_edge(flat)
    top_start = fc.P(0.0, collar_height)
    top_end = fc.P(flat + COLLAR_POINT, COLLAR_RISE + collar_height)  # pointed front
    return fc.Piece(
        "collar",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_RISE), top_end)]),
            fc.Edge("top", [fc.curve_through(top_end, top_start, bulge=0.04, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, collar_height * 0.5),
                               fc.P(flat * 0.75, collar_height * 0.5)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Flat Collar (half, on fold)",
    )


def build_placket_backing():
    """Facing strip behind the placket slash: (length + 30) tall, 2× width wide."""
    w = 2.0 * placket_width
    h = placket_length + 30.0
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
        label="Placket Backing",
    )


def build_cuff(sleeve_hem_len):
    """Ribbed cuff band derived from the sleeve hem (folded lengthwise when sewn)."""
    length = sleeve_hem_len * CUFF_RATIO + 2.0 * seam_allowance
    band_h = 2.0 * CUFF_HEIGHT
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
        label="Cuff (rib)",
    )


def build():
    pattern = fc.PatternSet("polo-shirt")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    half_opening = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    sleeve = build_sleeve(cap_target)
    collar = build_collar(half_opening)
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "collar": target_piece in ("collar", "set"),
        "placket_backing": target_piece in ("placket_backing", "set"),
        "cuff": target_piece in ("cuff", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
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
        # The half collar on fold sews to the folded front + back neck halves:
        # its solved neck edge must equal the half opening (halves on both sides).
        pattern.declare_seam(
            [("collar", "neck")],
            [("front", "neck"), ("back", "neck")],
            tol=2.0,
        )
    fabric_width = 1600.0                       # jersey-algodon card width
    rib_pieces = ("collar", "cuff")             # knitted trims, not cut from the marker
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces if p.name not in rib_pieces
    )
    marker_len = total_area / (fabric_width * 0.70)   # knits nest tightly
    pattern.bom = [
        {"item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker efficiency"},
        {"item": "1x1 rib for collar + cuffs", "qty": 3, "unit": "strip",
         "note": "one collar pair + two cuffs; see piece dimensions"},
        {"item": "12 mm flat buttons", "qty": 3, "unit": "pieces",
         "note": "placket closure; buttonhole crosses marked on the front"},
        {"item": "polyester thread + stretch needle", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11"},
    ]
    pattern.metadata = {
        "fc100_rank": 3,
        "fabric_hint": "jersey-algodon",
        "neck_opening_mm": round(2.0 * half_opening, 1),
        "collar_half_target_mm": round(half_opening, 1),
        "collar_neck_solved_mm": round(collar.edge("neck").length(0.05), 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "sleeve_cap_solved_mm": round(sleeve.edge("cap").length(0.05), 1),
        "placket_box_mm": [round(placket_length, 1), round(placket_width, 1)],
        "buttonholes": 3,
        "drafting": "tee knit block + solved flat collar + marked placket + derived rib cuff",
    }
    return pattern


result = build()

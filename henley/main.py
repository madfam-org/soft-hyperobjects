"""
Henley — FC-100 rank #73. Fashion Cabinet Garment Cartridge.

The collarless placket shirt: rank #1's drop-shoulder knit block carrying the
polo's marked button placket (three buttonhole crosses, backed by a separate
facing strip), a LONG tapered sleeve whose cap is SOLVED to the front + back
armholes, and the crew tee's derived rib neckband. No collar — the band IS the
finish: it runs the FULL neck opening, riding across the placket top, so the
top button closes band against band.

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

chest_girth    = float(PARAM(lambda: chest_girth, 980.0))
body_length    = float(PARAM(lambda: body_length, 730.0))     # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 590.0))   # cap apex to wrist
knit_ease      = float(PARAM(lambda: knit_ease, 60.0))        # total
placket_length = float(PARAM(lambda: placket_length, 180.0))  # CF neck point down
placket_width  = float(PARAM(lambda: placket_width, 30.0))
neckband_ratio = float(PARAM(lambda: neckband_ratio, 0.85))   # rib length / opening
neckband_width = float(PARAM(lambda: neckband_width, 18.0))   # finished band height
wrist_opening  = float(PARAM(lambda: wrist_opening, 190.0))   # flat width at hem
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(600.0, min(chest_girth, 1800.0))
body_length = max(400.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(300.0, min(sleeve_length, 780.0))
knit_ease = max(-80.0, min(knit_ease, 300.0))
placket_length = max(60.0, min(placket_length, 260.0))
placket_width = max(20.0, min(placket_width, 50.0))
neckband_ratio = max(0.70, min(neckband_ratio, 1.0))
neckband_width = max(10.0, min(neckband_width, 40.0))
wrist_opening = max(140.0, min(wrist_opening, 400.0))

W = (chest_girth + knit_ease) / 4.0          # quarter body width (fold at CF/CB)
L = body_length
AH = max(160.0, min((chest_girth + knit_ease) / 8.0 + 95.0, L - 120.0))
NW = max(60.0, neck_girth / 5.0)             # half neck width on the fold
HPS_Y = L + 20.0                             # high point shoulder above nape line
SHOULDER_DROP = 35.0
FRONT_NECK_DROP = 85.0
BACK_NECK_DROP = 20.0                        # HPS to CB nape
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)


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
    """Placket box on the folded front: the placket sits ON the fold like the
    polo's — the CF-side line rides the fold (the slash opens on center), the
    second line sits placket_width away, and a bottom bar closes the box (the
    fold edge makes a notch there ambiguous, so the bottom is marked with an
    internal instead). Three buttonhole crosses space evenly down the box
    centerline at 1/4, 2/4, 3/4 of the placket length.
    """
    y_top, y_bot = cf_neck_y, cf_neck_y - placket_length
    marks = [
        fc.Internal("placket edge (CF)", [fc.P(0.0, y_top), fc.P(0.0, y_bot)]),
        fc.Internal("placket edge", [fc.P(placket_width, y_top), fc.P(placket_width, y_bot)]),
        fc.Internal("placket bottom", [fc.P(0.0, y_bot), fc.P(placket_width, y_bot)]),
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
    """Long tapered sleeve; cap length bisected to the front + back armholes."""
    ch = max(45.0, AH * 0.33)                       # shallow knit cap
    sl = max(200.0, sleeve_length - ch)             # underarm-to-wrist length
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
    chw = max(70.0, min(wrist_opening / 2.0, hb))   # half wrist width (taper)
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
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (long, tapered)",
    )


def build_neckband(front, back):
    """Rib neckband derived from the measured opening, like the crew tee's.

    The band runs the FULL neckline — including across the placket top; the
    henley has no collar, so the band edge is the finish and the top button
    closes band against band.
    """
    half_opening = front.edge("neck").length() + back.edge("neck").length()
    band_len = 2.0 * half_opening * neckband_ratio + 2.0 * seam_allowance
    band_h = 2.0 * neckband_width                   # folded lengthwise when sewn
    return fc.Piece(
        "neckband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                         # band length already includes joins
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(band_len, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Neckband (rib, full opening)",
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


def build():
    pattern = fc.PatternSet("henley")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    half_opening = front.edge("neck").length() + back.edge("neck").length()
    sleeve = build_sleeve(cap_target)
    neckband = build_neckband(front, back)
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "neckband": target_piece in ("neckband", "set"),
        "placket_backing": target_piece in ("placket_backing", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(sleeve)
    if wanted["neckband"]:
        pattern.add(neckband)
    if wanted["placket_backing"]:
        pattern.add(build_placket_backing())
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
    fabric_width = 1600.0                       # jersey-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces if p.name != "neckband"
    )
    marker_len = total_area / (fabric_width * 0.70)   # knits nest tightly
    pattern.bom = [
        {"item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker efficiency"},
        {"item": "1x1 rib for neckband", "qty": 1, "unit": "strip",
         "note": "full neck opening x ratio + joins; band crosses the placket top"},
        {"item": "12 mm flat buttons", "qty": 3, "unit": "pieces",
         "note": "placket closure; buttonhole crosses marked on the front"},
        {"item": "polyester thread + stretch needle", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11"},
    ]
    pattern.metadata = {
        "fc100_rank": 73,
        "fabric_hint": "jersey-algodon",
        "neck_opening_mm": round(2.0 * half_opening, 1),
        "neckband_len_mm": round(neckband.edge("bottom").length(), 1),
        "neckband_spans_placket_top": True,
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "sleeve_cap_solved_mm": round(sleeve.edge("cap").length(0.05), 1),
        "wrist_flat_mm": round(sleeve.edge("hem").length(), 1),
        "placket_box_mm": [round(placket_length, 1), round(placket_width, 1)],
        "buttonholes": 3,
        "drafting": "rank #1 block + polo placket + full-opening rib band + long solved sleeve",
    }
    return pattern


result = build()

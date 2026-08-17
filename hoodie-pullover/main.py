"""
Pullover Hoodie — FC-100 rank #5. Fashion Cabinet Garment Cartridge.

The sweatshirt architecture plus two new pieces: a TWO-PANEL HOOD whose neck
edge is solved (by scaling its back depth) to match the measured half neck
opening exactly, and a kangaroo pocket cut on fold. Cuffs and hem band stay
derived ribs; the neckline is finished by the hood itself.

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

chest_girth   = float(PARAM(lambda: chest_girth, 1000.0))
body_length   = float(PARAM(lambda: body_length, 670.0))
neck_girth    = float(PARAM(lambda: neck_girth, 390.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 570.0))
fleece_ease   = float(PARAM(lambda: fleece_ease, 160.0))
hood_height   = float(PARAM(lambda: hood_height, 350.0))
hood_depth    = float(PARAM(lambda: hood_depth, 260.0))
cuff_ratio    = float(PARAM(lambda: cuff_ratio, 0.78))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.85))
cuff_height    = float(PARAM(lambda: cuff_height, 60.0))
hemband_height = float(PARAM(lambda: hemband_height, 60.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 950.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(200.0, min(sleeve_length, 780.0))
fleece_ease = max(60.0, min(fleece_ease, 400.0))
hood_height = max(280.0, min(hood_height, 450.0))
hood_depth = max(200.0, min(hood_depth, 340.0))

W = (chest_girth + fleece_ease) / 4.0
L = body_length
AH = (chest_girth + fleece_ease) / 8.0 + 105.0
AH = max(180.0, min(AH, L - 100.0))
NW = max(64.0, neck_girth / 5.0 + 6.0)         # wider neck: the hood needs room
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 30.0)
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 90.0
BACK_NECK_DROP = 20.0


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _body_piece(name, neck_drop, label):
    neck_top_y = HPS_Y - neck_drop
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(neck_drop, 24.0) * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12), fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch), fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
    ch = max(50.0, AH * 0.30)
    sl = max(100.0, sleeve_length - ch)
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
        label="Sleeve",
    )


def _hood_neck_edge(back_x):
    """Hood bottom (neck seam): front-bottom corner to a scaled back-bottom point."""
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(back_x, 35.0), fc.P(back_x * 0.60, -22.0),
                   fc.P(back_x * 0.28, -18.0), fc.P(0.0, 0.0))],
    )


def build_hood(half_opening):
    """Two-panel hood; the neck edge is solved to the half neck opening."""
    lo, hi = half_opening * 0.35, half_opening * 1.1
    for _ in range(48):
        bx = (lo + hi) / 2.0
        if _hood_neck_edge(bx).length(0.05) < half_opening:
            lo = bx
        else:
            hi = bx
    bx = (lo + hi) / 2.0
    if abs(_hood_neck_edge(bx).length(0.05) - half_opening) > 1.0:
        raise ValueError("hood neck-edge solver did not converge")
    face_x = -18.0                                     # slight forward overhang
    top = fc.P(face_x + 30.0, hood_height)
    edges = [
        _hood_neck_edge(bx),                           # back-bottom → front-bottom
        fc.Edge("face", [fc.Line(fc.P(0.0, 0.0), fc.P(face_x, hood_height * 0.55)),
                         fc.Line(fc.P(face_x, hood_height * 0.55), top)]),
        fc.Edge(
            "crown",
            [fc.Bezier(top, fc.P(top.x + hood_depth * 0.55, hood_height + 8.0),
                       fc.P(bx + (hood_depth - bx) * 0.9, hood_height * 0.72),
                       fc.P(hood_depth, hood_height * 0.45)),
             fc.Bezier(fc.P(hood_depth, hood_height * 0.45),
                       fc.P(hood_depth - 4.0, hood_height * 0.22),
                       fc.P(bx + 14.0, 60.0), fc.P(bx, 35.0))],
        ),
    ]
    return fc.Piece(
        "hood",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(hood_depth * 0.45, 80.0),
                               fc.P(hood_depth * 0.45, hood_height * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood (side panel)",
    )


def build_pocket():
    w, h, mouth = W * 0.62, 190.0, 60.0                # half-width on fold
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w - mouth, h))]),
        fc.Edge("mouth", [fc.Line(fc.P(w - mouth, h), fc.P(w, h - mouth))]),
        fc.Edge("side", [fc.Line(fc.P(w, h - mouth), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "pocket",
        edges,
        seam_allowance=seam_allowance,
        allowances={"mouth": 18.0},                    # folded facing on the hand opening
        grainline=fc.Grainline(fc.P(w * 0.5, 30.0), fc.P(w * 0.5, h - 40.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Kangaroo Pocket",
    )


def _rib(name, finished_len, finished_height, qty, label):
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
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("hoodie-pullover")
    front = _body_piece("front", FRONT_NECK_DROP, "Front")
    back = _body_piece("back", BACK_NECK_DROP, "Back")
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    half_opening = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve(cap_target))
    if everything or target_piece == "hood":
        pattern.add(build_hood(half_opening))
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())
    if everything or target_piece == "ribs":
        hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
        cuff_circ = pattern.piece("sleeve").edge("hem").length() if everything else 0.0
        if cuff_circ:
            pattern.add(_rib("cuff", cuff_circ * cuff_ratio, cuff_height, 2, "Cuff (rib)"))
        pattern.add(_rib("hem_band", hem_circ * hemband_ratio, hemband_height, 1,
                         "Hem Band (rib)"))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
        # One hood panel covers one side of the head: its neck edge must equal
        # the half opening (front neck + back neck of the folded halves).
        pattern.declare_seam([("hood", "neck")],
                             [("front", "neck"), ("back", "neck")], tol=2.0)
    pattern.metadata = {
        "fc100_rank": 5,
        "fabric_hint": "felpa-algodon",
        "drafting": "sweatshirt block + solved two-panel hood + kangaroo pocket",
    }
    return pattern


result = build()

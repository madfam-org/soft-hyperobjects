"""
Long-sleeve Tee — FC-100 rank #13. Fashion Cabinet Garment Cartridge.

Rank #1's drop-shoulder knit block with a long, tapered, cap-solved sleeve
and the same derived rib neckband. Self-contained per the commons contract
(cartridges never import each other).

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


target_piece = str(PARAM(lambda: target_piece, "set"))

chest_girth    = float(PARAM(lambda: chest_girth, 980.0))
body_length    = float(PARAM(lambda: body_length, 720.0))
neck_girth     = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 590.0))
knit_ease      = float(PARAM(lambda: knit_ease, 60.0))
wrist_opening  = float(PARAM(lambda: wrist_opening, 190.0))  # flat width at hem
neckband_ratio = float(PARAM(lambda: neckband_ratio, 0.85))
neckband_width = float(PARAM(lambda: neckband_width, 20.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

chest_girth = max(600.0, min(chest_girth, 1800.0))
body_length = max(400.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(300.0, min(sleeve_length, 780.0))
knit_ease = max(-80.0, min(knit_ease, 300.0))
wrist_opening = max(140.0, min(wrist_opening, 400.0))
neckband_ratio = max(0.70, min(neckband_ratio, 1.0))

W = (chest_girth + knit_ease) / 4.0
L = body_length
AH = max(160.0, min((chest_girth + knit_ease) / 8.0 + 95.0, L - 120.0))
NW = max(60.0, neck_girth / 5.0)
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 35.0)
UNDERARM = fc.P(W, SH_END.y - AH)


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
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
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 80.0), fc.P(W * 0.62, L - 120.0)),
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
    ch = max(45.0, AH * 0.33)
    sl = max(200.0, sleeve_length - ch)
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
    chw = max(70.0, min(wrist_opening / 2.0, hb))
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
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (long, tapered)",
    )


def build_neckband(front, back):
    half_opening = front.edge("neck").length() + back.edge("neck").length()
    band_len = 2.0 * half_opening * neckband_ratio + 2.0 * seam_allowance
    band_h = 2.0 * neckband_width
    return fc.Piece(
        "neckband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(band_len, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Neckband (rib)",
    )


def build():
    pattern = fc.PatternSet("long-sleeve-tee")
    front = _body_piece("front", 85.0, "Front")
    back = _body_piece("back", 20.0, "Back")
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve(cap_target))
    if everything or target_piece == "neckband":
        pattern.add(build_neckband(front, back))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
    pattern.metadata = {
        "fc100_rank": 13,
        "fabric_hint": "jersey-algodon",
        "drafting": "rank #1 block, long tapered cap-solved sleeve",
    }
    return pattern


result = build()

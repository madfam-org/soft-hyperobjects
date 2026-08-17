"""
T-shirt (crew neck) — FC-100 rank #1. Fashion Cabinet Garment Cartridge.

The most-produced garment on earth, as a parametric knit block: front and
back cut on fold, a sleeve whose cap length is SOLVED numerically to match
the front + back armholes (multi-edge seam check), and a neckband derived
from the measured neck opening times a rib-stretch ratio. Relaxed
drop-shoulder draft, jersey-appropriate 7 mm allowances.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|neckband|set

chest_girth    = float(PARAM(lambda: chest_girth, 980.0))
body_length    = float(PARAM(lambda: body_length, 720.0))   # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 220.0))  # cap apex to hem
knit_ease      = float(PARAM(lambda: knit_ease, 60.0))       # total, can be small
armhole_depth  = float(PARAM(lambda: armhole_depth, 0.0))    # 0 = auto
sleeve_opening = float(PARAM(lambda: sleeve_opening, 0.0))   # full width flat; 0 = auto
neckband_ratio = float(PARAM(lambda: neckband_ratio, 0.85))  # rib length / opening
neckband_width = float(PARAM(lambda: neckband_width, 20.0))  # finished band height
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(600.0, min(chest_girth, 1800.0))
body_length = max(400.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(80.0, min(sleeve_length, 700.0))
knit_ease = max(-80.0, min(knit_ease, 300.0))
neckband_ratio = max(0.70, min(neckband_ratio, 1.0))
neckband_width = max(10.0, min(neckband_width, 40.0))

W = (chest_girth + knit_ease) / 4.0          # quarter body width (fold at CF/CB)
L = body_length
AH = armhole_depth if armhole_depth > 0 else (chest_girth + knit_ease) / 8.0 + 95.0
AH = max(160.0, min(AH, L - 120.0))
NW = max(60.0, neck_girth / 5.0)             # half neck width on the fold
HPS_Y = L + 20.0                             # high point shoulder above nape line
SHOULDER_DROP = 35.0
FRONT_NECK_DROP = 85.0
BACK_NECK_DROP = 20.0                        # HPS to CB nape
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)


def _armhole_edge():
    """Shared front/back armhole curve (drop-shoulder tees keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _body_piece(name, neck_edge, neck_top_y, label):
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
    return _body_piece("front", neck, cf_neck_y, "Front")


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
    chw = (sleeve_opening / 2.0) if sleeve_opening > 0 else hb * 0.85
    chw = max(60.0, min(chw, hb))
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
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_neckband(front_piece, back_piece):
    half_opening = front_piece.edge("neck").length() + back_piece.edge("neck").length()
    band_len = 2.0 * half_opening * neckband_ratio + 2.0 * seam_allowance
    band_h = 2.0 * neckband_width                   # folded lengthwise when sewn
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "neckband",
        edges,
        seam_allowance=0.0,                         # band length already includes joins
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal(
            "fold line",
            [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)],
        )],
        cut=fc.CutSpec(quantity=1),
        label="Neckband (rib)",
    )


def build():
    pattern = fc.PatternSet("t-shirt-crew")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "neckband": target_piece in ("neckband", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    if wanted["neckband"]:
        pattern.add(build_neckband(front, back))
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
    half_opening = front.edge("neck").length() + back.edge("neck").length()
    pattern.metadata = {
        "fc100_rank": 1,
        "neck_opening_mm": round(2.0 * half_opening, 1),
        "neckband_ratio": neckband_ratio,
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "min_head_stretch_pct": round(
            (560.0 / max(2.0 * half_opening * neckband_ratio, 1.0) - 1.0) * 100.0, 1
        ),
        "fabric_hint": "jersey-algodon",
        "drafting": "relaxed drop-shoulder knit block; cap solved to armhole length",
    }
    return pattern


result = build()

"""
Robe — FC-100 rank #42. Fashion Cabinet Garment Cartridge.

Shawl-front lounge robe: back on fold; two wrap fronts whose center edge is a
straight diagonal from the hem-side center front up to the shoulder-neck
point (open wrap, no closures); a wide sleeve with the cap solved to the
front+back armholes (rank #6 numeric method, cap ease 0); self belt with
loops; patch pockets. The index's shawl collar is simplified in v0 to the
plain hemmed wrap edge — see docs/README.md.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|belt|pocket|set

chest_girth   = float(PARAM(lambda: chest_girth, 1040.0))
robe_length   = float(PARAM(lambda: robe_length, 1100.0))   # nape to finished hem
neck_girth    = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 540.0))  # apex to hemmed opening
lounge_ease   = float(PARAM(lambda: lounge_ease, 240.0))    # generous total wrap ease
belt_width    = float(PARAM(lambda: belt_width, 80.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
robe_length = max(700.0, min(robe_length, 1500.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(250.0, min(sleeve_length, 760.0))
lounge_ease = max(120.0, min(lounge_ease, 500.0))
belt_width = max(50.0, min(belt_width, 120.0))

# ── Drop-shoulder robe block (rank #6 geometry constants, lengthened) ────────
W = (chest_girth + lounge_ease) / 4.0
L = robe_length
AH = (chest_girth + lounge_ease) / 8.0 + 105.0
AH = max(180.0, min(AH, L - 100.0))
NW = max(62.0, neck_girth / 5.0 + 2.0)
HPS_Y = L + 20.0
SHOULDER_DROP = 30.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
BACK_NECK_DROP = 20.0
WRAP_X = 120.0                                     # wrap-edge x at the hem
WAIST_Y = max(150.0, UNDERARM.y - 220.0)           # belt line height
BELT_T = (UNDERARM.y - WAIST_Y) / UNDERARM.y       # belt notch fraction down the side
POCKET_W, POCKET_H = 170.0, 190.0


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def build_back():
    neck_top_y = HPS_Y - BACK_NECK_DROP
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(BACK_NECK_DROP, 24.0) * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "back",
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
        notches=[fc.Notch("side", BELT_T, "belt loop"), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    """Half-back outline, but the center edge is the straight wrap diagonal.

    The wrap runs from (WRAP_X, 0) at the hem up to the shoulder-neck point
    (NW, HPS_Y) — it replaces both the center edge and the front neck curve.
    """
    px = max(WRAP_X + 8.0, (W + WRAP_X) / 2.0 - POCKET_W / 2.0)
    py = max(200.0, WAIST_Y - 340.0)
    return fc.Piece(
        "front",
        [
            fc.Edge("wrap", [fc.Line(fc.P(WRAP_X, 0.0), fc.P(NW, HPS_Y))]),
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(WRAP_X, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "wrap": hem_allowance},
        notches=[fc.Notch("side", BELT_T, "belt loop"), fc.Notch("armhole", 0.5),
                 fc.Notch("wrap", WAIST_Y / HPS_Y, "belt line")],
        grainline=fc.Grainline(fc.P(W * 0.72, 70.0), fc.P(W * 0.72, L - 110.0)),
        internals=[fc.Internal(
            "pocket placement",
            [fc.P(px, py), fc.P(px + POCKET_W, py), fc.P(px + POCKET_W, py + POCKET_H),
             fc.P(px, py + POCKET_H), fc.P(px, py)],
        )],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
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
    chw = max(120.0, hb * 0.8)                     # wide open wrist, no cuff
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
        label="Sleeve",
    )


def _strip(name, length, width, qty, label, notches=None):
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
            fc.Edge("top", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=notches or [],
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0), fc.P(length * 0.8, width / 2.0)),
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build_pocket():
    return fc.Piece(
        "pocket",
        [
            fc.Edge("side_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, POCKET_H))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, POCKET_H), fc.P(POCKET_W, POCKET_H))]),
            fc.Edge("side_b", [fc.Line(fc.P(POCKET_W, POCKET_H), fc.P(POCKET_W, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(POCKET_W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance},
        notches=[fc.Notch("top", 0.5, "center match")],
        grainline=fc.Grainline(fc.P(POCKET_W / 2.0, 25.0), fc.P(POCKET_W / 2.0, POCKET_H - 25.0)),
        cut=fc.CutSpec(quantity=2),
        label="Patch Pocket",
    )


def build():
    pattern = fc.PatternSet("robe")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve(cap_target))
    if all_pieces or target_piece == "belt":
        belt_len = chest_girth * 2.2               # waist proxy: chest girth
        pattern.add(_strip("belt", belt_len, belt_width, 1, "Belt",
                           notches=[fc.Notch("top", 0.5, "center back")]))
        pattern.add(_strip("belt_loop", 60.0, 20.0, 2, "Belt Loop"))
    if all_pieces or target_piece == "pocket":
        pattern.add(build_pocket())
    if all_pieces:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
    pattern.metadata = {
        "fc100_rank": 42,
        "fabric_hint": "felpa-algodon",
        "wrap": {"hem_x_mm": WRAP_X, "belt_line_y_mm": round(WAIST_Y, 1)},
        "drafting": "drop-shoulder robe block; straight wrap diagonal replaces the front "
                    "neck; cap solved to armholes (ease 0); shawl collar simplified to "
                    "the wrap edge in v0",
    }
    return pattern


result = build()

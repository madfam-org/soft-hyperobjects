"""
Tunic — FC-100 rank #78. Fashion Cabinet Garment Cartridge.

Flowing woven tunic with an INTEGRATED kimono/dolman sleeve: front and back
are cut on fold, the shoulder line extends from the high point of shoulder
out to a wide short sleeve end, and the underarm curves down and in to the
side seam — no separate sleeve piece, no cap solver. The side seam is sewn
only from the underarm to the slit top (notched on each side edge); below it
the seam opens as a side slit. The round neckline is finished with a derived
bias binding strip (measured opening x 0.95 + 2 seam allowances).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|binding|set

bust_girth     = float(PARAM(lambda: bust_girth, 950.0))
body_length    = float(PARAM(lambda: body_length, 820.0))    # HPS line to hem
neck_girth     = float(PARAM(lambda: neck_girth, 390.0))
sleeve_reach   = float(PARAM(lambda: sleeve_reach, 320.0))   # HPS to sleeve end
sleeve_opening = float(PARAM(lambda: sleeve_opening, 400.0))  # vertical opening
flare_mm       = float(PARAM(lambda: flare_mm, 60.0))        # hem beyond bust line
slit_height    = float(PARAM(lambda: slit_height, 180.0))    # slit top above hem
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(600.0, min(bust_girth, 1700.0))
body_length = max(500.0, min(body_length, 1200.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
sleeve_reach = max(150.0, min(sleeve_reach, 600.0))
sleeve_opening = max(150.0, min(sleeve_opening, 650.0))
flare_mm = max(0.0, min(flare_mm, 250.0))
slit_height = max(0.0, min(slit_height, 500.0))

EASE = 180.0    # total flowing ease over the bust girth (woven, loose fit)
UA_DROP = 70.0  # underarm curve depth below the sleeve-end bottom
SLOPE = 0.15    # gentle dolman shoulder drop per mm of horizontal reach
BIND_W = 15.0   # finished neck-binding width; the strip is cut doubled

W = (bust_girth + EASE) / 4.0                    # quarter width at bust line
L = body_length                                  # hem at y=0, HPS line at y=L
NW = max(60.0, neck_girth / 5.0 - 6.0)           # half neck width
HPS = fc.P(NW, L)
DX = sleeve_reach / (1.0 + SLOPE * SLOPE) ** 0.5  # horizontal run of the reach
SLV_X = NW + DX
SLV_TOP = fc.P(SLV_X, L - SLOPE * DX)
sleeve_opening = min(sleeve_opening, max(150.0, SLV_TOP.y - UA_DROP - 120.0))
SLV_BOT = fc.P(SLV_X, SLV_TOP.y - sleeve_opening)
SIDE_TOP = fc.P(W, SLV_BOT.y - UA_DROP)
HEM_SIDE = fc.P(W + flare_mm, 0.0)
slit_height = max(0.0, min(slit_height, SIDE_TOP.y - 60.0))
T_SLIT = 1.0 - slit_height / SIDE_TOP.y          # arc fraction of slit top
FRONT_NECK_DROP = 90.0
BACK_NECK_DROP = 25.0


def _top_edges():
    """Integrated sleeve run — identical for front and back (kimono cut)."""
    underarm = fc.Edge(
        "underarm",
        [fc.Bezier(SLV_BOT, fc.P(SLV_X, SLV_BOT.y - UA_DROP * 0.6),
                   fc.P(W, SIDE_TOP.y + UA_DROP * 0.6), SIDE_TOP)],
    )
    return [
        fc.Edge("shoulder_sleeve", [fc.Line(HPS, SLV_TOP)]),
        fc.Edge("sleeve_end", [fc.Line(SLV_TOP, SLV_BOT)]),
        underarm,
    ]


def _body_piece(name, neck_drop, label):
    neck_top_y = L - neck_drop
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + neck_drop * 0.45), HPS)],
    )
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck,
        *_top_edges(),
        fc.Edge("side", [fc.Line(SIDE_TOP, HEM_SIDE)]),
        fc.Edge("hem", [fc.Line(HEM_SIDE, origin)]),
    ]
    notches = []
    if slit_height > 0.0:
        notches.append(fc.Notch("side", T_SLIT, "slit top"))
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "sleeve_end": hem_allowance, "neck": 0.0},
        notches=notches,
        grainline=fc.Grainline(fc.P(W * 0.55, 80.0), fc.P(W * 0.55, L - 160.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _binding(name, finished_len, label):
    band_h = 2.0 * BIND_W
    length = finished_len + 2.0 * seam_allowance
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def build():
    pattern = fc.PatternSet("tunic")
    front = _body_piece("front", FRONT_NECK_DROP, "Front")
    back = _body_piece("back", BACK_NECK_DROP, "Back")
    want_body = target_piece in ("front", "back", "set")
    want_bind = target_piece in ("binding", "set")
    if not (want_body or want_bind):
        want_body = want_bind = True
    if target_piece in ("front", "set"):
        pattern.add(front)
    if target_piece in ("back", "set"):
        pattern.add(back)
    if want_bind:
        neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
        pattern.add(_binding("neck_binding", neck_opening * 0.95, "Neck Binding (bias)"))
    if target_piece == "set":
        pattern.declare_seam(("front", "shoulder_sleeve"), ("back", "shoulder_sleeve"), tol=1.5)
        pattern.declare_seam(("front", "underarm"), ("back", "underarm"), tol=1.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 78,
        "fabric_hint": "popelina-algodon",
        "ease_total_mm": EASE,
        "slit_height_mm": slit_height,
        "drafting": "kimono-sleeve tunic; side sewn underarm to slit top; bound neck",
    }
    return pattern


result = build()

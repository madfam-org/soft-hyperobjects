"""
Nightgown — FC-100 rank #43. Fashion Cabinet Garment Cartridge.

The camisole lengthened into a gown: front and back cut on fold with a gentle
A-flare from the bust to a below-knee hem. Same strap-point construction as
the camisole — bound top edges (zero allowance, one binding strip derived from
the measured openings times a stretch ratio) and two separate strap strips
sewn into 8 mm spaghetti. New to the gown: side slits (the side seam is sewn
from the underarm down to the slit-top notches, placed at the same computed
arc fraction on front and back) and an optional empire "gather zone" marking
line under the bust for elastic or shirring.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|straps|binding|set

bust_girth     = float(PARAM(lambda: bust_girth, 900.0))
gown_length    = float(PARAM(lambda: gown_length, 1150.0))  # strap point to hem
front_drop     = float(PARAM(lambda: front_drop, 105.0))    # CF below strap point
back_drop      = float(PARAM(lambda: back_drop, 45.0))      # CB below strap point
strap_length   = float(PARAM(lambda: strap_length, 400.0))  # cut length per strap
flare_mm       = float(PARAM(lambda: flare_mm, 120.0))      # gentle A-flare per quarter
slit_height    = float(PARAM(lambda: slit_height, 200.0))   # side slit above the hem
knit_ease      = float(PARAM(lambda: knit_ease, 20.0))      # total ease, may go negative
binding_ratio  = float(PARAM(lambda: binding_ratio, 0.92))
binding_width  = float(PARAM(lambda: binding_width, 10.0))  # finished binding height
empire_gather  = bool(PARAM(lambda: empire_gather, True))   # mark under-bust gather zone
bodice_line    = float(PARAM(lambda: bodice_line, 260.0))   # gather zone below strap point
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(600.0, min(bust_girth, 1600.0))
gown_length = max(700.0, min(gown_length, 1500.0))
front_drop = max(40.0, min(front_drop, 200.0))
back_drop = max(10.0, min(back_drop, 120.0))
strap_length = max(250.0, min(strap_length, 600.0))
flare_mm = max(0.0, min(flare_mm, 250.0))
slit_height = max(0.0, min(slit_height, gown_length / 4.0))  # manifest constraint, enforced
knit_ease = max(-80.0, min(knit_ease, 150.0))
binding_ratio = max(0.75, min(binding_ratio, 1.0))
binding_width = max(6.0, min(binding_width, 20.0))
bodice_line = max(150.0, min(bodice_line, 450.0))

W = (bust_girth + knit_ease) / 4.0                  # half-piece width at bust
TOP_Y = gown_length                                 # hem sits at y = 0
AH = (bust_girth + knit_ease) / 16.0 + 75.0         # shallow camisole armhole
AH = max(90.0, min(AH, TOP_Y - 150.0))
STRAP_PT = fc.P(max(40.0, W * 0.5), TOP_Y)          # strap attachment point
UNDERARM = fc.P(W, TOP_Y - AH)                      # side seam top
HEM_W = W + flare_mm                                # gentle A-flare sweep
STRAP_CUT_W = 24.0                                  # folds into 8 mm spaghetti
SIDE_TOP_Y = UNDERARM.y                             # side edge spans this down to y = 0
SLIT_Y = min(slit_height, SIDE_TOP_Y - 20.0)        # slit top, kept below the underarm
SLIT_T = (SIDE_TOP_Y - SLIT_Y) / SIDE_TOP_Y         # arc fraction along the side edge


def _armhole_edge():
    """Shallow scoop from the strap point to the underarm, identical front/back."""
    return fc.Edge("armhole", [fc.curve_through(STRAP_PT, UNDERARM, bulge=0.16, side=-1.0)])


def _gather_zone():
    """Horizontal empire marking under the bust, center fold to the side seam."""
    drop_y = max(bodice_line, AH + 20.0, front_drop + 30.0)
    y = TOP_Y - drop_y
    side_x = W + flare_mm * (SIDE_TOP_Y - y) / SIDE_TOP_Y
    return fc.Internal("gather zone", [fc.P(0.0, y), fc.P(side_x, y)])


def _body_piece(name, drop, bulge, label, internals=None):
    """Fold-cut gown panel; the top edge is bound, so it carries no allowance."""
    top_start = fc.P(0.0, TOP_Y - drop)
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, top_start)]),
        fc.Edge("top", [fc.curve_through(top_start, STRAP_PT, bulge=bulge, side=-1.0)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(HEM_W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(HEM_W, 0.0), origin)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "top": 0.0},  # bound top edge
        notches=[fc.Notch("top", 1.0, "strap"), fc.Notch("side", SLIT_T, "slit top")],
        grainline=fc.Grainline(fc.P(W * 0.5, 80.0), fc.P(W * 0.5, UNDERARM.y - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _strip(name, length, height, label, quantity):
    """A straight-grain strip cut net (allowances already folded into `length`)."""
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, height))]),
        fc.Edge("top", [fc.Line(fc.P(length, height), fc.P(0.0, height))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, height), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, height / 2.0),
                               fc.P(length * 0.8, height / 2.0)),
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def build():
    pattern = fc.PatternSet("nightgown")
    front_marks = [_gather_zone()] if empire_gather else None
    front = _body_piece("front", front_drop, 0.06, "Front", internals=front_marks)
    back = _body_piece("back", back_drop, 0.03, "Back")
    known = target_piece in ("front", "back", "straps", "binding", "set")
    add_front = not known or target_piece in ("front", "set")
    add_back = not known or target_piece in ("back", "set")
    add_straps = not known or target_piece in ("straps", "set")
    add_binding = not known or target_piece in ("binding", "set")
    if add_front:
        pattern.add(front)
    if add_back:
        pattern.add(back)
    if add_straps:
        pattern.add(_strip("strap", strap_length, STRAP_CUT_W, "Strap (8 mm spaghetti)", 2))
    if add_binding:
        # Fold-cut halves → the garment openings are twice the drafted edges.
        top_opening = 2.0 * (front.edge("top").length() + back.edge("top").length())
        binding_len = top_opening * binding_ratio + 2.0 * seam_allowance
        pattern.add(_strip("top_binding", binding_len, 2.0 * binding_width, "Top Binding", 1))
    if add_front and add_back:
        # Shared construction: identical side edges, sewn from the underarm down
        # to the slit-top notches (same arc fraction t on front and back).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 43,
        "fabric_hint": "jersey-algodon",
        "slit_notch_t": round(SLIT_T, 4),
        "note": "camisole lengthened into a gown; slits open below the side notches",
    }
    return pattern


result = build()

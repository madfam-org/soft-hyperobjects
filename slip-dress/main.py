"""
Slip dress — FC-100 rank #46. Fashion Cabinet Garment Cartridge.

The nightgown refined into outerwear: a woven bias-cut slip that skims instead
of hanging. Front and back keep the camisole family's strap-point construction
(bound top edges with a derived binding strip, separate spaghetti-strap strips)
but the drafting shifts: the grainline is drawn at a true 45 degrees for bias
cutting, the front neck is a cowl-ish gentle inward sag, the back top edge is
nearly straight so the fold mirror leaves a small V dip at CB, and the side
seam is a two-bezier shaped curve (blouse's trick) through a gentle waist
suppression computed from the bust/waist difference. French seams throughout
(12 mm allowance, sewn 6 + 6); no slits, no gather zone.

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
waist_girth    = float(PARAM(lambda: waist_girth, 720.0))
dress_length   = float(PARAM(lambda: dress_length, 1150.0))  # strap point to hem
front_drop     = float(PARAM(lambda: front_drop, 115.0))     # CF below strap point
back_drop      = float(PARAM(lambda: back_drop, 55.0))       # CB below strap point
strap_length   = float(PARAM(lambda: strap_length, 420.0))   # cut length per strap
flare_mm       = float(PARAM(lambda: flare_mm, 70.0))        # skimming flare per quarter
binding_ratio  = float(PARAM(lambda: binding_ratio, 0.95))   # woven bias barely stretches
binding_width  = float(PARAM(lambda: binding_width, 10.0))   # finished binding height
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))  # French seam: sewn 6 + 6
hem_allowance  = float(PARAM(lambda: hem_allowance, 15.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(600.0, min(bust_girth, 1600.0))
waist_girth = max(500.0, min(waist_girth, 1500.0))
dress_length = max(700.0, min(dress_length, 1500.0))
front_drop = max(60.0, min(front_drop, 200.0))
back_drop = max(20.0, min(back_drop, 120.0))
strap_length = max(250.0, min(strap_length, 600.0))
flare_mm = max(0.0, min(flare_mm, 200.0))
binding_ratio = max(0.85, min(binding_ratio, 1.0))
binding_width = max(6.0, min(binding_width, 20.0))

BIAS_EASE = 60.0                                    # fixed skim ease: 45° grain gives
W = (bust_girth + BIAS_EASE) / 4.0                  # mechanical stretch, so keep it low
TOP_Y = dress_length                                # hem sits at y = 0
AH = (bust_girth + BIAS_EASE) / 16.0 + 75.0         # shallow camisole-family armhole
AH = max(90.0, min(AH, TOP_Y - 150.0))
STRAP_PT = fc.P(max(40.0, W * 0.5), TOP_Y)          # strap attachment point
UNDERARM = fc.P(W, TOP_Y - AH)                      # side seam top
SIDE_TOP_Y = UNDERARM.y
HEM_W = W + flare_mm                                # less sweep than the gown
STRAP_CUT_W = 18.0                                  # folds into 6 mm spaghetti
WAIST_SUPPRESS = max(0.0, min(25.0, (bust_girth - waist_girth) / 8.0))  # skims, not fits
WAIST_Y = max(120.0, min(TOP_Y - 385.0, SIDE_TOP_Y - 80.0))             # waist level
WAIST_PT = fc.P(W - WAIST_SUPPRESS, WAIST_Y)


def _armhole_edge():
    """Shallow scoop from the strap point to the underarm, identical front/back."""
    return fc.Edge("armhole", [fc.curve_through(STRAP_PT, UNDERARM, bulge=0.16, side=-1.0)])


def _side_edge():
    """Shaped side seam, identical on front and back (blouse's shared-geometry
    trick, so the declared seam passes by construction): one bezier eases from
    the underarm into the gentle waist suppression, a second sweeps out to the
    flared hem, meeting it square. Both are vertical at the waist point, so the
    curve stays tangent-continuous and the dress skims instead of gripping."""
    drop = SIDE_TOP_Y - WAIST_Y
    rise = WAIST_Y
    return fc.Edge(
        "side",
        [fc.Bezier(UNDERARM, fc.P(W, SIDE_TOP_Y - drop * 0.45),
                   fc.P(W - WAIST_SUPPRESS, WAIST_Y + drop * 0.30), WAIST_PT),
         fc.Bezier(WAIST_PT, fc.P(W - WAIST_SUPPRESS, WAIST_Y - rise * 0.25),
                   fc.P(HEM_W, rise * 0.30), fc.P(HEM_W, 0.0))],
    )


_SIDE_PROBE = _side_edge()
_UPPER_LEN = _SIDE_PROBE.segments[0].length()
WAIST_T = _UPPER_LEN / (_UPPER_LEN + _SIDE_PROBE.segments[1].length())  # waist notch t

# True-bias grainline: equal run and rise = an exact 45° diagonal on both panels.
GRAIN_RISE = W * 0.30
GRAIN_A = fc.P(W * 0.25, TOP_Y * 0.35)
GRAIN_B = fc.P(W * 0.55, TOP_Y * 0.35 + GRAIN_RISE)


def _front_neck():
    """Cowl-ish front: a gentle inward sag toward CF instead of a straight edge."""
    cf = fc.P(0.0, TOP_Y - front_drop)
    return fc.Edge("top", [fc.curve_through(cf, STRAP_PT, bulge=0.12, side=-1.0)])


def _back_neck():
    """Nearly straight back edge; the fold mirror leaves a small V dip at CB."""
    cb = fc.P(0.0, TOP_Y - back_drop)
    return fc.Edge("top", [fc.curve_through(cb, STRAP_PT, bulge=0.02, side=-1.0)])


def _body_piece(name, neck_edge, drop, label):
    """Fold-drafted panel; the top edge is bound, so it carries no allowance."""
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, TOP_Y - drop))]),
        neck_edge,
        _armhole_edge(),
        _side_edge(),
        fc.Edge("hem", [fc.Line(fc.P(HEM_W, 0.0), origin)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "top": 0.0},  # bound top edge
        notches=[fc.Notch("top", 1.0, "strap"), fc.Notch("side", WAIST_T, "waist")],
        grainline=fc.Grainline(GRAIN_A, GRAIN_B),       # true 45° bias
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _strip(name, length, height, label, quantity):
    """A straight strip cut net (allowances already folded into `length`)."""
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
    pattern = fc.PatternSet("slip-dress")
    front = _body_piece("front", _front_neck(), front_drop, "Front")
    back = _body_piece("back", _back_neck(), back_drop, "Back")
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
        pattern.add(_strip("strap", strap_length, STRAP_CUT_W, "Strap (6 mm spaghetti)", 2))
    top_opening = 2.0 * (front.edge("top").length() + back.edge("top").length())
    binding_len = top_opening * binding_ratio + 2.0 * seam_allowance
    if add_binding:
        # Fold-drafted halves → the garment openings are twice the drawn edges.
        pattern.add(_strip("top_binding", binding_len, 2.0 * binding_width, "Top Binding", 1))
    if add_front and add_back:
        # Shared shaped side edge, French-seamed; identical geometry both sides.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 46,
        "fabric_hint": "popelina-algodon",
        "bias_cut": True,
        "bias_note": "cut single layer on true bias; French seams",
        "waist_notch_t": round(WAIST_T, 4),
        "waist_suppress_mm": round(WAIST_SUPPRESS, 1),
        "top_opening_mm": round(top_opening, 1),
        "binding_length_mm": round(binding_len, 1),
        "note": "nightgown refined into outerwear: 45° grain, cowl-ish front, shaped side",
    }
    return pattern


result = build()

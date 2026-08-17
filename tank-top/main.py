"""
Tank Top — FC-100 rank #8. Fashion Cabinet Garment Cartridge.

Sleeveless knit tank: front and back cut on fold with a deeper armhole scoop
and narrow straps, plus neck and armhole BINDING strips derived from the
measured openings times a rib ratio — the construction rule encoded, not a
fixed number.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|bindings|set

chest_girth   = float(PARAM(lambda: chest_girth, 940.0))
body_length   = float(PARAM(lambda: body_length, 680.0))   # nape line to hem
neck_girth    = float(PARAM(lambda: neck_girth, 380.0))
knit_ease     = float(PARAM(lambda: knit_ease, 30.0))
strap_width   = float(PARAM(lambda: strap_width, 38.0))
binding_ratio = float(PARAM(lambda: binding_ratio, 0.90))
binding_width = float(PARAM(lambda: binding_width, 12.0))  # finished binding height
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(600.0, min(chest_girth, 1700.0))
body_length = max(380.0, min(body_length, 950.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
knit_ease = max(-100.0, min(knit_ease, 250.0))
strap_width = max(20.0, min(strap_width, 80.0))
binding_ratio = max(0.75, min(binding_ratio, 1.0))

W = (chest_girth + knit_ease) / 4.0
L = body_length
AH = (chest_girth + knit_ease) / 8.0 + 110.0        # deeper scoop than a tee
AH = max(180.0, min(AH, L - 100.0))
NW = max(55.0, neck_girth / 5.0 - 8.0)              # narrower neck for straps
HPS_Y = L + 20.0
STRAP_END = fc.P(NW + strap_width, HPS_Y - 12.0)
UNDERARM = fc.P(W, HPS_Y - AH)
FRONT_NECK_DROP = 100.0
BACK_NECK_DROP = 30.0


def _armhole_edge():
    """Deep tank scoop, identical front/back."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(STRAP_END, fc.P(STRAP_END.x + 6.0, STRAP_END.y - AH * 0.45),
                   fc.P(W - AH * 0.28, UNDERARM.y + 14.0), UNDERARM)],
    )


def _body_piece(name, neck_drop, label):
    neck_top_y = HPS_Y - neck_drop
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + neck_drop * 0.45), fc.P(NW, HPS_Y))],
    )
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), STRAP_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "neck": 0.0, "armhole": 0.0},  # bound edges
        notches=[fc.Notch("side", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.6, 70.0), fc.P(W * 0.6, L - 130.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _binding(name, finished_len, label):
    band_h = 2.0 * binding_width
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
    pattern = fc.PatternSet("tank-top")
    front = _body_piece("front", FRONT_NECK_DROP, "Front")
    back = _body_piece("back", BACK_NECK_DROP, "Back")
    want_body = target_piece in ("front", "back", "set")
    want_bind = target_piece in ("bindings", "set")
    if not (want_body or want_bind):
        want_body = want_bind = True
    if target_piece in ("front", "set"):
        pattern.add(front)
    if target_piece in ("back", "set"):
        pattern.add(back)
    if want_bind:
        neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
        armhole_opening = front.edge("armhole").length() + back.edge("armhole").length()
        pattern.add(_binding("neck_binding", neck_opening * binding_ratio,
                             "Neck Binding (rib)"))
        armhole_binding = _binding("armhole_binding", armhole_opening * binding_ratio,
                                   "Armhole Binding (rib)")
        armhole_binding.cut = fc.CutSpec(quantity=2)
        pattern.add(armhole_binding)
    if target_piece == "set":
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 8,
        "fabric_hint": "jersey-algodon",
        "binding_ratio": binding_ratio,
        "drafting": "deep-scoop knit tank; neck/armhole edges bound, not hemmed",
    }
    return pattern


result = build()

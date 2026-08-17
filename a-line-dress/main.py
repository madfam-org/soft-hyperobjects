"""
A-Line Dress — FC-100 rank #22 (Vestido línea A).

First dress of the family: a waist-seamless sleeveless shift-to-flare. Front
cut on fold from a scooped neck through a fitted bust region, then an A-line
flare to a hem `flare_mm` wider than the bust quarter; back cut 2 with a CB
seam carrying an invisible-zipper notch, a shallow neck, and one fisheye
waist dart per panel. Darts stay internal (teaching-grade, not rotated into
the outline). Front and back share one shoulder, armhole, side, and hem
construction, so the declared seams match exactly, and the neck/armhole
FACING strips are derived from the measured openings — the construction rule
encoded, not a fixed number.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|facings|set

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
waist_girth = float(PARAM(lambda: waist_girth, 740.0))
dress_length = float(PARAM(lambda: dress_length, 950.0))   # nape line to hem
flare_mm = float(PARAM(lambda: flare_mm, 110.0))
strap_width = float(PARAM(lambda: strap_width, 42.0))
front_drop = float(PARAM(lambda: front_drop, 95.0))
zipper_length = float(PARAM(lambda: zipper_length, 400.0))
bust_dart_intake = float(PARAM(lambda: bust_dart_intake, 28.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

bust_girth = max(600.0, min(bust_girth, 1700.0))
waist_girth = max(450.0, min(waist_girth, 1500.0))
dress_length = max(700.0, min(dress_length, 1400.0))
flare_mm = max(40.0, min(flare_mm, 400.0))
strap_width = max(24.0, min(strap_width, 80.0))
front_drop = max(60.0, min(front_drop, 160.0))
bust_dart_intake = max(0.0, min(bust_dart_intake, 50.0))
zipper_length = max(250.0, min(zipper_length, dress_length * 0.5))

BUST_EASE = 80.0        # woven shift ease, folded into every width below
NECK_W = 62.0           # half neck width at the high point of shoulder
BACK_NECK_DROP = 30.0   # shallow back scoop
BACK_WAIST = 400.0      # nape-to-waist; locates the back fisheye darts
BUST_DROP = 60.0        # fitted vertical run below the underarm
DART_LEN = 110.0        # side-bust dart, leg line to apex
FISHEYE_INTAKE = 14.0
FISHEYE_LEN = 240.0
FACING_DEPTH = 30.0     # finished facing depth; strips are 2x this tall

W = (bust_girth + BUST_EASE) / 4.0                  # bust quarter
HPS_Y = dress_length + 20.0                         # nape line at y = dress_length
AH = (bust_girth + BUST_EASE) / 8.0 + 90.0          # armhole scoop depth
AH = max(170.0, min(AH, 280.0))
STRAP_END = fc.P(NECK_W + strap_width, HPS_Y - 12.0)
UNDERARM = fc.P(W, HPS_Y - AH)
BUST_PT = fc.P(W, UNDERARM.y - BUST_DROP)
HEM_OUT = fc.P(W + flare_mm, 0.0)                   # hem half-width = W + flare
WAIST_Y = dress_length - BACK_WAIST


def _neck_edge(drop):
    """Scoop from the center top to the HPS point — tank-style curve."""
    top_y = HPS_Y - drop
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, top_y), fc.P(NECK_W * 0.55, top_y),
                   fc.P(NECK_W, top_y + drop * 0.45), fc.P(NECK_W, HPS_Y))],
    )


def _armhole_edge():
    """Tank-style scoop, identical front/back — the facings depend on it."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(STRAP_END, fc.P(STRAP_END.x + 6.0, STRAP_END.y - AH * 0.45),
                   fc.P(W - AH * 0.28, UNDERARM.y + 14.0), UNDERARM)],
    )


def _shoulder_edge():
    return fc.Edge("shoulder", [fc.Line(fc.P(NECK_W, HPS_Y), STRAP_END)])


def _side_edge():
    """Fitted run underarm -> bust line, then a gentle flare to the hem.

    One construction for BOTH pieces, so front.side matches back.side
    exactly. The flare Bezier leaves the bust point straight down (G1 with
    the fitted run) and arrives at the hem along the flare direction.
    """
    flare_dir = (HEM_OUT - BUST_PT).normalized()
    c0 = fc.P(W, BUST_PT.y * 0.72)
    c1 = HEM_OUT - flare_dir * (BUST_PT.y * 0.35)
    return fc.Edge("side", [fc.Line(UNDERARM, BUST_PT), fc.Bezier(BUST_PT, c0, c1, HEM_OUT)])


def _hem_edge():
    return fc.Edge("hem", [fc.Line(HEM_OUT, fc.P(0.0, 0.0))])


def _grainline():
    return fc.Grainline(fc.P(W * 0.62, 90.0), fc.P(W * 0.62, UNDERARM.y - 60.0))


def _front():
    top_y = HPS_Y - front_drop
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
        _neck_edge(front_drop),
        _shoulder_edge(),
        _armhole_edge(),
        _side_edge(),
        _hem_edge(),
    ]
    # Side-bust dart, internal only. Legs sit on the fitted vertical run at
    # the side seam; the fold-mirror cut yields one dart per physical side.
    y_d = BUST_PT.y + BUST_DROP / 2.0
    half = bust_dart_intake / 2.0
    dart = fc.Internal(
        "side bust dart",
        [fc.P(W, y_d + half), fc.P(W - DART_LEN, y_d), fc.P(W, y_d - half)],
        kind="dart",
    )
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "side match")],
        grainline=_grainline(),
        internals=[dart] if bust_dart_intake > 0.5 else [],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Dress Front",
    )


def _back():
    cb_len = HPS_Y - BACK_NECK_DROP
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, cb_len))]),
        _neck_edge(BACK_NECK_DROP),
        _shoulder_edge(),
        _armhole_edge(),
        _side_edge(),
        _hem_edge(),
    ]
    # One fisheye (lens) waist dart per panel — the mirrored cut-2 pair gives
    # the classic two back neck-to-waist darts. Widest at the waist line and
    # kept below the bust line on short drafts.
    cx = max(60.0, min(waist_girth / 8.0, W - 40.0))
    top = min(WAIST_Y + FISHEYE_LEN / 2.0, BUST_PT.y - 15.0)
    bot = top - FISHEYE_LEN
    mid = (top + bot) / 2.0
    half = FISHEYE_INTAKE / 2.0
    fisheye = fc.Internal(
        "back fisheye dart",
        [fc.P(cx, top), fc.P(cx - half, mid), fc.P(cx, bot),
         fc.P(cx + half, mid), fc.P(cx, top)],
        kind="dart",
    )
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": 20.0},  # CB seam carries the zipper
        notches=[
            fc.Notch("side", 0.5, "side match"),
            # Invisible zipper spans zipper_length from the neck DOWN; the
            # notch marks the stop. `center` is authored hem->neck, so the
            # stop sits at authored fraction 1 - zipper_length / cb_len.
            fc.Notch("center", 1.0 - zipper_length / cb_len, "zipper stop"),
        ],
        grainline=_grainline(),
        internals=[fisheye],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Dress Back",
    )


def _facing(name, opening_len, quantity, label):
    """Straight facing strip: measured opening + 2 sa ends, 2x depth tall."""
    length = opening_len + 2.0 * seam_allowance
    h = 2.0 * FACING_DEPTH
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, h))]),
        fc.Edge("top", [fc.Line(fc.P(length, h), fc.P(0.0, h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, h / 2.0), fc.P(length * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def build():
    pattern = fc.PatternSet("a-line-dress")
    front = _front()
    back = _back()
    want_body = target_piece in ("front", "back", "set")
    want_face = target_piece in ("facings", "set")
    if not (want_body or want_face):
        want_body = want_face = True
    if want_body and target_piece in ("front", "set"):
        pattern.add(front)
    if want_body and target_piece in ("back", "set"):
        pattern.add(back)
    if want_face:
        # Physical neck opening: the front is cut on fold, so its drafted
        # half-neck sews in twice; the back is cut 2, so its drafted neck
        # edge also appears twice (once per panel). Facing length =
        #   2*front.neck + 2*back.neck + 2*sa  (ends meet the CB zipper).
        neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
        # Each armhole is one front scoop + one back scoop; cut 2 (one per
        # armhole), each facing = (front.armhole + back.armhole) + 2*sa.
        armhole_opening = front.edge("armhole").length() + back.edge("armhole").length()
        pattern.add(_facing("neck_facing", neck_opening, 1, "Neck Facing"))
        pattern.add(_facing("armhole_facing", armhole_opening, 2, "Armhole Facing"))
    if target_piece == "set":
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 22,
        "fabric_hint": "popelina-algodon",
        "drafting": "waist-seamless shift-to-flare; internal darts (side bust + back "
                    "fisheye); CB invisible zipper; facings derived from measured openings",
    }
    return pattern


result = build()

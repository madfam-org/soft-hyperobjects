"""
Shift Dress — FC-100 rank #23 (Vestido recto).

The a-line-dress draft straightened into the classic loose shift: minimal hem
flare over a straight-ish side seam, generous shift ease, and SET-IN SHORT
SLEEVES in place of the sleeveless facing-only finish. Front cut on fold with
internal side-bust darts; back cut 2 with a CB seam carrying an
invisible-zipper notch and one internal fisheye waist dart per panel. Front
and back share one shoulder, armhole, side, and hem construction, so the
declared seams match exactly; the sleeve-cap length is SOLVED numerically
(bisection) to the measured front + back armholes at zero ease, and the neck
facing strip is derived from the measured opening — the construction rule
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


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|facing|set

bust_girth = float(PARAM(lambda: bust_girth, 940.0))
dress_length = float(PARAM(lambda: dress_length, 920.0))    # nape line to hem
neck_girth = float(PARAM(lambda: neck_girth, 385.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 200.0))  # cap apex to sleeve hem
shift_ease = float(PARAM(lambda: shift_ease, 120.0))        # total; the loose shift room
flare_mm = float(PARAM(lambda: flare_mm, 25.0))             # minimal — shift, not A-line
front_drop = float(PARAM(lambda: front_drop, 90.0))
zipper_length = float(PARAM(lambda: zipper_length, 380.0))
bust_dart_intake = float(PARAM(lambda: bust_dart_intake, 26.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

bust_girth = max(600.0, min(bust_girth, 1700.0))
dress_length = max(700.0, min(dress_length, 1400.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(80.0, min(sleeve_length, 350.0))
shift_ease = max(60.0, min(shift_ease, 300.0))
flare_mm = max(0.0, min(flare_mm, 120.0))
front_drop = max(60.0, min(front_drop, 160.0))
bust_dart_intake = max(0.0, min(bust_dart_intake, 50.0))
zipper_length = max(250.0, min(zipper_length, dress_length * 0.5))

BACK_NECK_DROP = 25.0   # shallow back scoop
SHOULDER_DROP = 30.0    # HPS down to the shoulder point
BACK_WAIST = 400.0      # nape-to-waist; locates the back fisheye darts
BUST_DROP = 55.0        # vertical side run below the underarm; carries the dart legs
DART_LEN = 105.0        # side-bust dart, leg line to apex
FISHEYE_INTAKE = 12.0   # light back shaping — the shift stays loose
FISHEYE_LEN = 220.0
FACING_DEPTH = 30.0     # finished facing depth; the strip is 2x this tall
CB_ALLOWANCE = 20.0     # CB seam allowance carrying the invisible zipper

W = (bust_girth + shift_ease) / 4.0                 # bust quarter
HPS_Y = dress_length + 20.0                         # nape line at y = dress_length
NECK_W = max(55.0, min(neck_girth / 5.0, 110.0))    # half neck width at HPS
AH = (bust_girth + shift_ease) / 8.0 + 85.0         # armhole depth below the shoulder pt
AH = max(170.0, min(AH, 260.0))
SH_X = max(NECK_W + 20.0, min(NECK_W + 118.0, W - 30.0))
SH_END = fc.P(SH_X, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, SH_END.y - AH)
BUST_PT = fc.P(W, UNDERARM.y - BUST_DROP)
HEM_OUT = fc.P(W + flare_mm, 0.0)                   # hem half-width = W + minimal flare
WAIST_Y = dress_length - BACK_WAIST


def _neck_edge(drop):
    """Scoop from the center top to the HPS point — jewel-style curve."""
    top_y = HPS_Y - drop
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, top_y), fc.P(NECK_W * 0.55, top_y),
                   fc.P(NECK_W, top_y + drop * 0.45), fc.P(NECK_W, HPS_Y))],
    )


def _shoulder_edge():
    return fc.Edge("shoulder", [fc.Line(fc.P(NECK_W, HPS_Y), SH_END)])


def _armhole_edge():
    """Set-in scoop shared by front and back — the solved sleeve cap depends on it."""
    c0 = fc.P(SH_X + 6.0, SH_END.y - AH * 0.45)
    c1 = fc.P(SH_X + (W - SH_X) * 0.35, UNDERARM.y + 14.0)
    return fc.Edge("armhole", [fc.Bezier(SH_END, c0, c1, UNDERARM)])


def _side_edge():
    """Straight-ish shift side: a short vertical run under the arm (carrying
    the front dart legs), then one straight line to the barely-flared hem.
    One construction for BOTH pieces, so front.side matches back.side exactly.
    """
    return fc.Edge("side", [fc.Line(UNDERARM, BUST_PT), fc.Line(BUST_PT, HEM_OUT)])


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
    # Side-bust dart, internal only. Legs sit on the vertical run at the side
    # seam; the fold-mirror cut yields one dart per physical side.
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
    # the classic two back darts. Widest at the waist, kept below the bust line.
    cx = max(60.0, min(W * 0.45, W - 40.0))
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
        allowances={"hem": hem_allowance, "center": CB_ALLOWANCE},  # CB carries the zipper
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


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def _sleeve(cap_target):
    """Short sleeve; the cap half-width is bisected until the cap length
    matches the measured front + back armholes (zero ease — a loose poplin
    shift sews the cap flat, no easing-in required)."""
    ch = max(50.0, AH * 0.38)                       # cap height
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
    chw = max(60.0, min(hb * 0.82, hb))             # gently tapered hem opening
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
        fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
        _cap_curve(hb, sl, ch),
        fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 25.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def _neck_facing(front, back):
    """Straight neck facing strip: measured opening + 2 sa ends, 2x depth tall.

    Physical opening: the front is cut on fold, so its drafted half-neck sews
    in twice; the back is cut 2, so its drafted neck edge also appears twice
    (once per panel). The strip ends meet at the CB invisible zipper.
    """
    opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
    length = opening + 2.0 * seam_allowance
    h = 2.0 * FACING_DEPTH
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, h))]),
        fc.Edge("top", [fc.Line(fc.P(length, h), fc.P(0.0, h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "neck_facing", edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, h / 2.0), fc.P(length * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Neck Facing",
    )


def build():
    pattern = fc.PatternSet("shift-dress")
    front = _front()
    back = _back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "facing": target_piece in ("facing", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(_sleeve(cap_target))
    if wanted["facing"]:
        pattern.add(_neck_facing(front, back))
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
        )
    if wanted["sleeve"]:
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
    pattern.metadata = {
        "fc100_rank": 23,
        "fabric_hint": "popelina-algodon",
        "neck_opening_mm": round(neck_opening, 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "facing_length_mm": round(neck_opening + 2.0 * seam_allowance, 1),
        "drafting": "straight shift from the a-line draft: minimal flare, internal darts "
                    "(side bust + back fisheye), CB invisible zipper, short-sleeve cap "
                    "solved to the armholes, neck facing derived from the measured opening",
    }
    return pattern


result = build()

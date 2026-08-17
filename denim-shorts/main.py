"""
Denim Shorts — FC-100 rank #19. Fashion Cabinet Garment Cartridge.

Jeans-style shorts on the athletic-shorts block: straight hems, a grown-on
fly extension on the upper front crotch (rejoining the crotch curve with
tangent continuity), a fly J-topstitch trace, quarter-circle scoop-pocket
openings with rivet drill crosses, a marked back yoke line (uncut in v0)
and pentagon patch-pocket placement, a straight cut-1 waistband with a
40 mm button-stand overlap, and belt loops. The back hem width is solved
analytically so the straight inseams match exactly (athletic-shorts method).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))

hip_girth      = float(PARAM(lambda: hip_girth, 1000.0))
waist_girth    = float(PARAM(lambda: waist_girth, 880.0))
inseam_length  = float(PARAM(lambda: inseam_length, 130.0))
front_rise     = float(PARAM(lambda: front_rise, 255.0))
back_rise      = float(PARAM(lambda: back_rise, 290.0))
denim_ease     = float(PARAM(lambda: denim_ease, 80.0))
hem_width      = float(PARAM(lambda: hem_width, 250.0))    # front half-hem, flat
fly_width      = float(PARAM(lambda: fly_width, 36.0))
fly_depth      = float(PARAM(lambda: fly_depth, 180.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))  # turned twice

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(550.0, min(waist_girth, 1600.0))
inseam_length = max(70.0, min(inseam_length, 350.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 80.0))
denim_ease = max(40.0, min(denim_ease, 300.0))
hem_width = max(160.0, min(hem_width, 340.0))
fly_width = max(24.0, min(fly_width, 50.0))
fly_depth = max(120.0, min(fly_depth, front_rise - 70.0))

HIP_E = hip_girth + denim_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0, HIP_E / 12.0
WAIST_F = 0.80 + 0.12 * max(0.6, min(waist_girth / hip_girth, 1.1))
OVERLAP = 40.0     # waistband button-stand overlap
POCKET_R = 120.0   # scoop-pocket opening radius


def _scoop_pocket():
    """Quarter-circle pocket-opening trace from waist down to the side seam."""
    pts = []
    for i in range(9):
        ang = math.radians(90.0 * i / 8.0)
        pts.append(fc.P(POCKET_R * math.cos(ang), WAIST_Y - POCKET_R * math.sin(ang)))
    return fc.Internal("front pocket opening", pts)


def _rivets():
    """Two rivet drill crosses just inside the scoop-pocket opening ends."""
    marks = []
    for tag, cx, cy in (("a", POCKET_R - 12.0, WAIST_Y - 16.0),
                        ("b", 16.0, WAIST_Y - (POCKET_R - 12.0))):
        marks.append(fc.Internal(f"rivet-{tag}-h", [fc.P(cx - 4.0, cy), fc.P(cx + 4.0, cy)],
                                 kind="drill"))
        marks.append(fc.Internal(f"rivet-{tag}-v", [fc.P(cx, cy - 4.0), fc.P(cx, cy + 4.0)],
                                 kind="drill"))
    return marks


def _fly_j(cf_at):
    """Fly J-topstitch trace: parallel to the CF, quarter-hook back onto it."""
    off = fly_width - 6.0
    y_elbow = WAIST_Y - fly_depth + off + 6.0
    c = cf_at(y_elbow)
    pts = [fc.P(cf_at(WAIST_Y - 2.0).x - off, WAIST_Y - 2.0), fc.P(c.x - off, y_elbow)]
    for i in range(1, 9):
        ang = math.radians(180.0 + 90.0 * i / 8.0)
        pts.append(fc.P(c.x + off * math.cos(ang), y_elbow + off * math.sin(ang)))
    y_end = y_elbow - off - 2.0
    pts.append(fc.P(cf_at(y_end).x - 1.0, y_end))
    return fc.Internal("fly J topstitch", pts, kind="trace")


def _front(tip_x):
    """Front leg with a grown-on fly extension on the upper crotch."""
    waist_in = FW * WAIST_F
    a = fc.P(waist_in, WAIST_Y)                       # CF at the waist
    cs = fc.P(FW - 4.0, WAIST_Y - fly_depth - 20.0)   # fork-curve start on the CF
    dn = (cs - a).normalized()

    def cf_at(y):
        return a.lerp(cs, (WAIST_Y - y) / (WAIST_Y - cs.y))

    e_top = fc.P(waist_in + fly_width, WAIST_Y)
    e_low = cf_at(WAIST_Y - fly_depth + 50.0) + fc.P(fly_width, 0.0)
    rejoin = fc.Bezier(e_low, e_low + dn * 35.0, cs - dn * 30.0, cs)
    fork = fc.Bezier(cs, cs + dn * 40.0,
                     fc.P(FW + (tip_x - FW) * 0.35, CROTCH_Y + 35.0),
                     fc.P(tip_x, CROTCH_Y))
    edges = [
        fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), e_top)]),
        fc.Edge("crotch", [fc.Line(e_top, e_low), rejoin, fork]),
        fc.Edge("inseam", [fc.Line(fc.P(tip_x, CROTCH_Y), fc.P(hem_width, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(hem_width, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(FW * 0.45, WAIST_Y * 0.15),
                               fc.P(FW * 0.45, WAIST_Y * 0.8)),
        internals=[_scoop_pocket(), _fly_j(cf_at)] + _rivets(),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def _back(tip_x, hem_w):
    """Back leg with yoke-line and pentagon patch-pocket markings."""
    waist_in = BW * WAIST_F
    cb_y = WAIST_Y + (back_rise - front_rise)
    yoke = fc.Internal("back yoke line",
                       [fc.P(0.0, WAIST_Y - 70.0), fc.P(waist_in, cb_y - 110.0)])
    cx, top = BW * 0.5, WAIST_Y - 140.0
    pocket = fc.Internal("back pocket placement", [
        fc.P(cx - 70.0, top), fc.P(cx + 70.0, top), fc.P(cx + 70.0, top - 90.0),
        fc.P(cx, top - 125.0), fc.P(cx - 70.0, top - 90.0), fc.P(cx - 70.0, top),
    ])
    edges = [
        fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
        fc.Edge(
            "crotch",
            [fc.Bezier(fc.P(waist_in, cb_y), fc.P(BW - 4.0, cb_y - front_rise * 0.45),
                       fc.P(BW + (tip_x - BW) * 0.35, CROTCH_Y + 40.0),
                       fc.P(tip_x, CROTCH_Y))],
        ),
        fc.Edge("inseam", [fc.Line(fc.P(tip_x, CROTCH_Y), fc.P(hem_w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(BW * 0.45, WAIST_Y * 0.15),
                               fc.P(BW * 0.45, WAIST_Y * 0.8)),
        internals=[yoke, pocket],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back",
    )


def build_legs():
    f_tip_x = FW + FORK_F
    b_tip_x = BW + FORK_B
    front_len = math.hypot(f_tip_x - hem_width, CROTCH_Y)
    run = math.sqrt(max(front_len**2 - CROTCH_Y**2, 25.0))
    bhw = b_tip_x - run                              # back hem solved analytically
    if bhw < 100.0:
        raise ValueError("solved back hem width degenerate; widen hem_width")
    return _front(f_tip_x), _back(b_tip_x, bhw)


def build_waistband(front, back):
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    length = circ + OVERLAP + 2.0 * seam_allowance
    band_h = 2.0 * (42.0 + seam_allowance)
    return fc.Piece(
        "waistband",
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
        cut=fc.CutSpec(quantity=1),
        label="Waistband",
    )


def build_beltloop():
    w, h = 12.0, 55.0
    return fc.Piece(
        "beltloop",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("long_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("long_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.15), fc.P(w / 2.0, h * 0.85)),
        cut=fc.CutSpec(quantity=5),
        label="Belt Loop",
    )


def build():
    pattern = fc.PatternSet("denim-shorts")
    front, back = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "waistband":
        pattern.add(build_waistband(front, back))
    if everything or target_piece == "beltloop":
        pattern.add(build_beltloop())
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        pattern.declare_seam(
            [("waistband", "bottom")],
            [("front", "waist"), ("front", "waist"), ("back", "waist"), ("back", "waist")],
            tol=2.5,
            ease=OVERLAP + 2.0 * seam_allowance,
        )
    pattern.metadata = {
        "fc100_rank": 19,
        "fabric_hint": "mezclilla-denim",
        "drafting": "jeans shorts on the athletic-shorts block; back hem solved to match inseams",
        "topstitch": "double-needle, heavy contrast thread; fly J, yoke line, pockets and hems",
    }
    return pattern


result = build()

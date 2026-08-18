"""
Jeans (5-pocket) — FC-100 rank #2. Fashion Cabinet Garment Cartridge.

The canonical five-pocket jean on the side-seamed trouser block (same frame as
chinos): a front leg (cut 2 mirror) with a grown-on fly extension on the upper
crotch that rejoins the fork curve with tangent continuity, a fly J-topstitch
trace, a fly-stop notch, and a curved coin-pocket ("scoop") placement marking;
a back leg (cut 2 mirror) whose TOP edge is the YOKE SEAM — the defining
five-pocket feature — a straight seam from side to centre-back where the shaped
back yoke attaches; a shaped back YOKE (cut 2 mirror) whose lower edge is built
from the same two endpoints as the back leg's yoke seam so the two match by
construction (delta ≈ 0); a back patch pocket (cut 2) with a topstitched upper
edge trace; a two-piece waistband (left/right halves) whose bottom edge carries
the closure overlap as declared seam ease; a fly facing/shield (cut 1); and
five belt-loop strips. A `fly_type` select switches the CF closure note between
a zipper and a button fly.

Honest, teaching-grade: the coin pocket is a placement marking (not a cut bag),
the pocket bags/facings beyond the fly shield are omitted, and the topstitch is
represented as guide traces. Hardware (tack button, copper rivets, zipper)
federates to Yantra4D cartridges via the BOM notes — never modelled here.

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
fly_type = str(PARAM(lambda: fly_type, "zip"))
if fly_type not in ("zip", "button"):
    fly_type = "zip"

hip_girth      = float(PARAM(lambda: hip_girth, 1000.0))
waist_girth    = float(PARAM(lambda: waist_girth, 860.0))
inseam_length  = float(PARAM(lambda: inseam_length, 780.0))
front_rise     = float(PARAM(lambda: front_rise, 255.0))
back_rise      = float(PARAM(lambda: back_rise, 300.0))
denim_ease     = float(PARAM(lambda: denim_ease, 90.0))
hem_width      = float(PARAM(lambda: hem_width, 100.0))    # front half-hem, flat
yoke_depth     = float(PARAM(lambda: yoke_depth, 90.0))    # yoke height at side seam
fly_width      = float(PARAM(lambda: fly_width, 36.0))
fly_depth      = float(PARAM(lambda: fly_depth, 190.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(500.0, min(waist_girth, 1600.0))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
denim_ease = max(40.0, min(denim_ease, 300.0))
hem_width = max(80.0, min(hem_width, 260.0))
yoke_depth = max(50.0, min(yoke_depth, 130.0))
fly_width = max(20.0, min(fly_width, 60.0))
fly_depth = max(80.0, min(fly_depth, front_rise - 30.0))

HIP_E = hip_girth + denim_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
HIP_LINE_Y = CROTCH_Y + front_rise * 0.4
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0
# Waist intake fraction: how far in from the hip line the waist point sits.
WAIST_F = 0.80 + 0.12 * max(0.6, min(waist_girth / hip_girth, 1.1))

OVERLAP = 40.0            # waistband button-stand overlap (declared as seam ease)
BAND_H = 40.0            # finished waistband height (folded)
LOOP_W, LOOP_H = 12.0, 55.0
POCKET_W, POCKET_TOP, POCKET_H = 130.0, 130.0, 150.0   # back patch pocket
COIN_R = 70.0            # coin/scoop pocket opening radius on the front


def _coin_pocket():
    """Curved coin-pocket ('scoop') opening: quarter arc from waist to side."""
    pts = []
    for i in range(9):
        ang = math.radians(90.0 * i / 8.0)
        pts.append(fc.P(COIN_R * math.cos(ang), WAIST_Y - COIN_R * math.sin(ang)))
    return fc.Internal("coin pocket opening", pts)


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


def _crease(hem_half, top_y, label):
    """Pressed jean centre line, leg center from hem to just below the hip."""
    x = hem_half / 2.0
    return fc.Internal(label, [fc.P(x, 0.0), fc.P(x, top_y)])


def build_front():
    """Front leg with a grown-on fly extension on the upper crotch."""
    waist_in = FW * WAIST_F
    tip_x = FW + FORK_F
    a = fc.P(waist_in, WAIST_Y)                        # CF at the waist
    cs = fc.P(FW - 4.0, WAIST_Y - fly_depth - 20.0)    # fork-curve start on the CF
    dn = (cs - a).normalized()

    def cf_at(y):
        return a.lerp(cs, (WAIST_Y - y) / (WAIST_Y - cs.y))

    e_top = fc.P(waist_in + fly_width, WAIST_Y)
    e_low = cf_at(WAIST_Y - fly_depth + 50.0) + fc.P(fly_width, 0.0)
    rejoin = fc.Bezier(e_low, e_low + dn * 35.0, cs - dn * 30.0, cs)
    fork = fc.Bezier(cs, cs + dn * 40.0,
                     fc.P(FW + (tip_x - FW) * 0.35, CROTCH_Y + 35.0),
                     fc.P(tip_x, CROTCH_Y))
    crotch = fc.Edge("crotch", [fc.Line(e_top, e_low), rejoin, fork])
    fly_frac = fly_depth / crotch.length(0.05)

    edges = [
        fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), e_top)]),
        crotch,
        fc.Edge("inseam", [fc.Line(fc.P(tip_x, CROTCH_Y), fc.P(FHW, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(FHW, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("crotch", fly_frac, "fly stop"),
                 fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(FW * 0.45, WAIST_Y * 0.12),
                               fc.P(FW * 0.45, WAIST_Y * 0.92)),
        internals=[_coin_pocket(), _fly_j(cf_at),
                   _crease(FHW, HIP_LINE_Y, "front crease")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Leg",
    )


def _yoke_seam_points():
    """The two endpoints of the back yoke seam, shared by leg top and yoke.

    Side end sits `yoke_depth` below the waist on the side seam (x=0). CB end
    sits `yoke_depth` below the CB waist point, measured down the CB rise line.
    Returns (side_pt, cb_pt, waist_in, cb_y).
    """
    waist_in = BW * WAIST_F
    cb_y = WAIST_Y + (back_rise - front_rise)
    side_pt = fc.P(0.0, WAIST_Y - yoke_depth)
    # CB waist point is (waist_in, cb_y); step down the waist→CB direction is
    # nearly vertical, so drop the yoke depth straight down at the CB x.
    cb_pt = fc.P(waist_in, cb_y - yoke_depth)
    return side_pt, cb_pt, waist_in, cb_y


def _solved_back_hem(tip_x):
    """Back hem half-width solved so the straight back inseam matches the front.

    Front inseam is a straight run from (FW+FORK_F, CROTCH_Y) to (FHW, 0); its
    length fixes the target. The back inseam is a straight run from (tip_x,
    CROTCH_Y) to (bhw, 0); solve bhw = tip_x - sqrt(front_len² - CROTCH_Y²).
    """
    f_tip_x = FW + FORK_F
    front_len = math.hypot(f_tip_x - FHW, CROTCH_Y)
    run = math.sqrt(max(front_len**2 - CROTCH_Y**2, 25.0))
    bhw = tip_x - run
    if bhw < 60.0:
        raise ValueError("solved back hem width degenerate; widen hem_width")
    return bhw


def build_back():
    """Back leg: TOP edge is the yoke seam (side→CB); yoke attaches above it."""
    side_pt, cb_pt, waist_in, cb_y = _yoke_seam_points()
    tip_x = BW + FORK_B
    bhw = _solved_back_hem(tip_x)

    cx, top = BW * 0.5, side_pt.y - 30.0
    pocket_mark = fc.Internal("back pocket placement", [
        fc.P(cx - POCKET_W / 2.0, top - POCKET_H),
        fc.P(cx + POCKET_W / 2.0, top - POCKET_H),
        fc.P(cx + POCKET_W / 2.0, top),
        fc.P(cx, top + 18.0),
        fc.P(cx - POCKET_W / 2.0, top),
        fc.P(cx - POCKET_W / 2.0, top - POCKET_H),
    ])

    edges = [
        fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), side_pt)]),
        fc.Edge("yoke_seam", [fc.Line(side_pt, cb_pt)]),
        fc.Edge(
            "crotch",
            [fc.Bezier(cb_pt, fc.P(BW - 4.0, cb_y - front_rise * 0.55),
                       fc.P(BW + (tip_x - BW) * 0.35, CROTCH_Y + 45.0),
                       fc.P(tip_x, CROTCH_Y))],
        ),
        fc.Edge("inseam", [fc.Line(fc.P(tip_x, CROTCH_Y), fc.P(bhw, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(bhw, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5),
                 fc.Notch("yoke_seam", 0.5, "yoke centre")],
        grainline=fc.Grainline(fc.P(BW * 0.45, CROTCH_Y * 0.15),
                               fc.P(BW * 0.45, side_pt.y * 0.9)),
        internals=[pocket_mark, _crease(bhw, HIP_LINE_Y, "back crease")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Leg",
    )


def build_yoke():
    """Shaped back yoke: lower edge shares the leg's yoke-seam endpoints.

    The lower edge runs cb→side using exactly the leg yoke_seam endpoints, so
    the two match by construction. The upper (waist) edge is drawn parallel at
    `yoke_depth` above; a slight CB scoop suppresses the waist as a real jean
    yoke does. Waist-edge length is what the waistband is checked against.
    """
    side_pt, cb_pt, waist_in, cb_y = _yoke_seam_points()
    # Upper edge: raise both ends by yoke_depth (back to the true waist line),
    # then bring the CB in by a small suppression so the yoke wedges shut.
    cb_up = fc.P(cb_pt.x - 12.0, cb_y)
    side_up = fc.P(side_pt.x, WAIST_Y)
    edges = [
        # lower edge: cb → side (identical endpoints to leg yoke_seam, reversed)
        fc.Edge("lower", [fc.Line(cb_pt, side_pt)]),
        fc.Edge("side", [fc.Line(side_pt, side_up)]),
        fc.Edge("waist", [fc.Line(side_up, cb_up)]),
        fc.Edge("cb", [fc.Line(cb_up, cb_pt)]),
    ]
    return fc.Piece(
        "yoke", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("lower", 0.5, "yoke centre"), fc.Notch("waist", 0.5)],
        grainline=fc.Grainline(fc.P(side_up.x + (cb_up.x - side_up.x) * 0.5, side_pt.y + 8.0),
                               fc.P(side_up.x + (cb_up.x - side_up.x) * 0.5, WAIST_Y - 8.0)),
        internals=[fc.Internal("yoke topstitch",
                               [cb_pt.lerp(side_pt, 0.04), side_pt.lerp(cb_pt, 0.04)],
                               kind="trace")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Yoke",
    )


def build_back_pocket():
    """Back patch pocket: pentagon (cut 2), upper edge carries a topstitch trace."""
    w, h, point = POCKET_W, POCKET_H, 26.0
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, point))]),
        fc.Edge("point_r", [fc.Line(fc.P(w, point), fc.P(w / 2.0, 0.0))]),
        fc.Edge("point_l", [fc.Line(fc.P(w / 2.0, 0.0), fc.P(0.0, point))]),
        fc.Edge("left", [fc.Line(fc.P(0.0, point), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "back_pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"top": 30.0},
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.2), fc.P(w / 2.0, h * 0.85)),
        internals=[fc.Internal("pocket hem topstitch",
                               [fc.P(6.0, h - 16.0), fc.P(w - 6.0, h - 16.0)],
                               kind="trace")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Patch Pocket",
    )


def build_fly_shield():
    """Fly facing / shield (cut 1): a rounded rectangle behind the fly."""
    w = fly_width + 22.0
    h = fly_depth
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("outer",
                [fc.Bezier(fc.P(w, h), fc.P(w + 10.0, h * 0.6),
                           fc.P(w + 10.0, h * 0.4), fc.P(w, 24.0)),
                 fc.Line(fc.P(w, 24.0), fc.P(w - 24.0, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w - 24.0, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "fly_shield", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.85)),
        cut=fc.CutSpec(quantity=1),
        label="Fly Shield",
    )


def build_waistband(front, yoke):
    """Straight waistband half: full waist circumference plus overlap+closures.

    Cut 2 mirror halves; each half spans one body side, but the declared seam
    checks the band bottom against the whole waist (2 fronts + 2 yokes), so the
    band length is the full circumference (denim-shorts convention).
    """
    waists = 2.0 * (front.edge("waist").length() + yoke.edge("waist").length())
    length = waists + OVERLAP + 2.0 * seam_allowance
    band_h = 2.0 * (BAND_H + seam_allowance)
    cy = band_h / 2.0
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        internals=[fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)])],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Waistband (half)",
    )


def build_belt_loop():
    """Belt-loop strip, cut five."""
    return fc.Piece(
        "belt_loop",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(LOOP_W, 0.0))]),
            fc.Edge("side_b", [fc.Line(fc.P(LOOP_W, 0.0), fc.P(LOOP_W, LOOP_H))]),
            fc.Edge("top", [fc.Line(fc.P(LOOP_W, LOOP_H), fc.P(0.0, LOOP_H))]),
            fc.Edge("side_a", [fc.Line(fc.P(0.0, LOOP_H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(LOOP_W / 2.0, LOOP_H * 0.15),
                               fc.P(LOOP_W / 2.0, LOOP_H * 0.85)),
        cut=fc.CutSpec(quantity=5),
        label="Belt Loop",
    )


def build():
    pattern = fc.PatternSet("jeans-5-pocket")
    front = build_front()
    back = build_back()
    yoke = build_yoke()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "yoke":
        pattern.add(yoke)
    if everything or target_piece == "back_pocket":
        pattern.add(build_back_pocket())
    if everything or target_piece == "fly_shield":
        pattern.add(build_fly_shield())
    if everything or target_piece == "waistband":
        pattern.add(build_waistband(front, yoke))
    if everything or target_piece == "belt_loop":
        pattern.add(build_belt_loop())

    if everything:
        # Side seam: the full-height front side ↔ the back assembly side, which
        # the yoke splits into back-leg side + yoke side (both sum to the front).
        pattern.declare_seam(
            [("front", "side")],
            [("back", "side"), ("yoke", "side")],
            tol=1.5,
        )
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        # THE signature seam: yoke lower edge ↔ back leg upper (yoke) edge.
        pattern.declare_seam(("yoke", "lower"), ("back", "yoke_seam"), tol=1.0)
        # Waistband bottom ↔ (front + yoke) waists ×2, eased by the overlap.
        pattern.declare_seam(
            [("waistband", "bottom")],
            [("front", "waist"), ("front", "waist"),
             ("yoke", "waist"), ("yoke", "waist")],
            tol=2.5,
            ease=OVERLAP + 2.0 * seam_allowance,
        )

    band_length = (2.0 * (front.edge("waist").length() + yoke.edge("waist").length())
                   + OVERLAP + 2.0 * seam_allowance)
    fly_note = ("YKK-style jeans zipper (Yantra4D hardware cartridge ref); "
                "modelled as the fly J-topstitch trace + fly-stop notch only"
                if fly_type == "zip" else
                "button fly: 4-5 tack buttons up the CF (Yantra4D hardware "
                "cartridge refs); fly J-topstitch trace marks the topstitch")

    pattern.bom = [
        {"item": "denim (mezclilla)", "qty": round((WAIST_Y + hem_allowance + 120.0) / 1000.0, 2),
         "unit": "m", "note": "~1.5 m usable width; two legs + yoke + waistband + pockets"},
        {"item": "pocketing (bag lining)", "qty": 0.3, "unit": "m",
         "note": "coin + front slant pocket bags (teaching-grade: bags not drafted here)"},
        {"item": "jeans tack button", "qty": 1, "unit": "pc",
         "note": "Yantra4D hardware cartridge ref (no-sew shank button); never modelled here"},
        {"item": "copper rivets", "qty": 6, "unit": "pc",
         "note": "Yantra4D hardware cartridge ref; front pocket corners + coin pocket"},
        {"item": "closure", "qty": 1, "unit": "set", "note": fly_note},
        {"item": "topstitch thread (heavy)", "qty": 1, "unit": "spool",
         "note": "double-needle contrast; fly J, yoke seam, out-seam, hems, pocket edges"},
        {"item": "bar-tack thread", "qty": 1, "unit": "spool",
         "note": "belt-loop ends + pocket-mouth reinforcement"},
    ]

    pattern.metadata = {
        "fc100_rank": 2,
        "fabric_hint": "mezclilla-denim",
        "fly_type": fly_type,
        "yoke_depth_mm": round(yoke_depth, 1),
        "yoke_seam_len_mm": round(back.edge("yoke_seam").length(), 1),
        "waistband_length_mm": round(band_length, 1),
        "drafting": ("five-pocket jean on the side-seamed trouser block; back "
                     "yoke lower edge matched to the back-leg top by shared "
                     "endpoints; grown-on fly with tangent-continuous rejoin"),
        "teaching_grade": ("coin pocket + back pocket + slant pockets are "
                           "placement markings, pocket bags omitted; topstitch "
                           "shown as guide traces; hardware federates to Yantra4D"),
        "topstitch": "double-needle heavy contrast thread throughout",
    }
    return pattern


result = build()

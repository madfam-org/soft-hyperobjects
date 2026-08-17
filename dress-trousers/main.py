"""
Dress trousers — FC-100 rank #36. Fashion Cabinet Garment Cartridge.

The chinos block refined for tailoring: front/back legs (cut 2 each) with the
front inseam bowed by a solved amount to match the deeper back fork, a
grown-on fly extension with a fly J-topstitch guide and fly-stop notch, a
pleated front (main pleat on the crease line, two fold lines pleat_depth
apart meeting the waist with a depth rung, plus a secondary pleat toward the
side), straight side-entry pocket marks on the side seams, full-length
pressed creases carrying the grainline, two back waist darts plus a
double-besom pocket marking, a sharper hem taper, and a two-half waistband
whose tab half extends into a +60 crossover tab with a button cross-mark,
verified against the leg waists with the tab declared as seam ease.

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

hip_girth     = float(PARAM(lambda: hip_girth, 1020.0))
waist_girth   = float(PARAM(lambda: waist_girth, 880.0))
inseam_length = float(PARAM(lambda: inseam_length, 780.0))
front_rise    = float(PARAM(lambda: front_rise, 280.0))
back_rise     = float(PARAM(lambda: back_rise, 320.0))
woven_ease    = float(PARAM(lambda: woven_ease, 90.0))
hem_width     = float(PARAM(lambda: hem_width, 95.0))      # front half-hem, flat
pleat_depth   = float(PARAM(lambda: pleat_depth, 25.0))
fly_width     = float(PARAM(lambda: fly_width, 38.0))
fly_depth     = float(PARAM(lambda: fly_depth, 200.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))  # blind-hem depth

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(500.0, min(waist_girth, hip_girth))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
woven_ease = max(40.0, min(woven_ease, 400.0))
hem_width = max(80.0, min(hem_width, 260.0))
pleat_depth = max(10.0, min(pleat_depth, 45.0))
fly_width = max(20.0, min(fly_width, 60.0))
fly_depth = max(80.0, min(fly_depth, front_rise - 30.0))

HIP_E = hip_girth + woven_ease
WAIST_E = waist_girth + 40.0                 # waist wearing ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
HIP_LINE_Y = CROTCH_Y + front_rise * 0.4
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0       # sharper dress taper via default 95

DART_INTAKE, DART_LEN = 12.0, 90.0
TAB = 60.0                                   # waistband crossover-tab extension
BAND_H = 40.0                                # finished waistband height (folded)
SEC_PLEAT_OFF, SEC_PLEAT_W = 40.0, 15.0      # secondary pleat: to the side, width
POCKET_DROP, POCKET_OPEN = 45.0, 150.0       # side-entry pocket: below waist, span
BESOM_W, BESOM_GAP = 130.0, 12.0             # double-besom welts: length, spacing


def _fly_j(fw_in):
    """Fly J-topstitch guide: vertical run inside CF hooking toward the fly stop."""
    jx = fw_in - fly_width
    cy = WAIST_Y - fly_depth + fly_width + 10.0
    pts = [fc.P(jx, WAIST_Y), fc.P(jx, cy)]
    for step in range(1, 7):
        a = math.radians(180.0 + 15.0 * step)
        pts.append(fc.P(fw_in + fly_width * math.cos(a), cy + fly_width * math.sin(a)))
    return fc.Internal("fly J topstitch", pts, kind="trace")


def _side_pocket():
    """Straight side-entry pocket mark: the opening span drawn on the side seam."""
    top = WAIST_Y - POCKET_DROP
    return fc.Internal(
        "side pocket opening",
        [fc.P(0.0, top), fc.P(0.0, top - POCKET_OPEN)],
    )


def _pleat(fold_x, width, label):
    """Pleat marking: two fold lines meeting the waist, bridged by a depth rung."""
    return fc.Internal(
        label,
        [fc.P(fold_x, WAIST_Y), fc.P(fold_x, HIP_LINE_Y),
         fc.P(fold_x + width, HIP_LINE_Y), fc.P(fold_x + width, WAIST_Y)],
    )


def _crease(hem_half, top_y, label):
    """Pressed crease: vertical at hem center, hem to the waist (full length)."""
    x = hem_half / 2.0
    return fc.Internal(label, [fc.P(x, 0.0), fc.P(x, top_y)])


def _back_dart(bw_run, rise_delta, frac, label):
    """Back waist dart as an internal: legs on the waist line, apex below."""
    slope = rise_delta / bw_run
    cx = bw_run * frac
    half = DART_INTAKE / 2.0
    return fc.Internal(
        label,
        [fc.P(cx - half, WAIST_Y + (cx - half) * slope),
         fc.P(cx, WAIST_Y + cx * slope - DART_LEN),
         fc.P(cx + half, WAIST_Y + (cx + half) * slope)],
        kind="dart",
    )


def _besom_pocket():
    """Double-besom marking: two parallel welt lines 130 apart-by-12, closed."""
    cx = BW * 0.5
    top = WAIST_Y - 90.0
    corners = [
        fc.P(cx - BESOM_W / 2.0, top),
        fc.P(cx + BESOM_W / 2.0, top),
        fc.P(cx + BESOM_W / 2.0, top - BESOM_GAP),
        fc.P(cx - BESOM_W / 2.0, top - BESOM_GAP),
    ]
    return fc.Internal("double besom pocket", corners + corners[:1])


def build_legs():
    fw_in = max(FW * 0.55, min(WAIST_E / 4.0, FW * 0.95))
    bw_run = max(BW * 0.55, min(WAIST_E / 4.0 + 2.0 * DART_INTAKE, BW * 0.95))
    rise_delta = back_rise - front_rise
    cb_y = WAIST_Y + rise_delta
    f_tip = fc.P(FW + FORK_F, CROTCH_Y)
    b_tip = fc.P(BW + FORK_B, CROTCH_Y)

    def f_inseam(bulge):
        return fc.Edge(
            "inseam",
            [fc.curve_through(f_tip, fc.P(FHW, 0.0), bulge=bulge, side=-1.0)],
        )

    b_inseam = fc.Edge(
        "inseam",
        [fc.curve_through(b_tip, fc.P(BHW, 0.0), bulge=0.0, side=-1.0)],
    )
    back_len = b_inseam.length(0.05)
    lo, hi = 0.0, 0.35
    for _ in range(44):
        mid = (lo + hi) / 2.0
        if f_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(f_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge")

    # Front crotch: line down the grown-on fly extension, then a bezier that
    # rejoins the fork curve smoothly (tangent-continuous at the fly stop).
    fx = fw_in + fly_width
    fly_knee = fc.P(fx, WAIST_Y - fly_depth)
    fork_drop = (WAIST_Y - fly_depth) - CROTCH_Y
    front_crotch = fc.Edge(
        "crotch",
        [
            fc.Line(fc.P(fx, WAIST_Y), fly_knee),
            fc.Bezier(
                fly_knee,
                fc.P(fx, fly_knee.y - fork_drop * 0.5),
                fc.P(fx + (f_tip.x - fx) * 0.4, CROTCH_Y + fork_drop * 0.38),
                f_tip,
            ),
        ],
    )
    fly_frac = fly_depth / front_crotch.length(0.05)

    crease_x = FHW / 2.0
    sec_x = max(6.0, crease_x - SEC_PLEAT_OFF)
    pocket_top_t = (WAIST_Y - POCKET_DROP) / WAIST_Y
    pocket_bot_t = (WAIST_Y - POCKET_DROP - POCKET_OPEN) / WAIST_Y

    front = fc.Piece(
        "front",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(fx, WAIST_Y))]),
            front_crotch,
            f_inseam(bulge),
            fc.Edge("hem", [fc.Line(fc.P(FHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[
            fc.Notch("crotch", fly_frac, "fly stop"),
            fc.Notch("side", 0.5),
            fc.Notch("inseam", 0.5),
            fc.Notch("side", pocket_top_t, "pocket"),
            fc.Notch("side", pocket_bot_t, "pocket"),
        ],
        grainline=fc.Grainline(fc.P(crease_x, inseam_length * 0.12),
                               fc.P(crease_x, inseam_length * 0.92)),
        internals=[
            _fly_j(fw_in),
            _side_pocket(),
            _pleat(crease_x, pleat_depth, "main pleat"),
            _pleat(sec_x, SEC_PLEAT_W, "secondary pleat"),
            _crease(FHW, WAIST_Y, "front crease"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Leg",
    )

    back_crotch = fc.Edge(
        "crotch",
        [fc.Bezier(fc.P(bw_run, cb_y), fc.P(BW - 4.0, cb_y - front_rise * 0.45),
                   fc.P(BW + (b_tip.x - BW) * 0.35, CROTCH_Y + 55.0), b_tip)],
    )
    b_slope = rise_delta / bw_run
    b_crease_x = BHW / 2.0
    back = fc.Piece(
        "back",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(bw_run, cb_y))]),
            back_crotch,
            b_inseam,
            fc.Edge("hem", [fc.Line(fc.P(BHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(b_crease_x, inseam_length * 0.12),
                               fc.P(b_crease_x, inseam_length * 0.92)),
        internals=[_back_dart(bw_run, rise_delta, 0.35, "back dart 1"),
                   _back_dart(bw_run, rise_delta, 0.62, "back dart 2"),
                   _besom_pocket(),
                   _crease(BHW, WAIST_Y + b_crease_x * b_slope, "back crease")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Leg",
    )
    return front, back


def _button_cross(x, y, arm=4.0):
    """Button cross-mark: one drill polyline drawing a small + at (x, y)."""
    return fc.Internal(
        "tab button",
        [fc.P(x - arm, y), fc.P(x + arm, y), fc.P(x, y),
         fc.P(x, y - arm), fc.P(x, y + arm)],
        kind="drill",
    )


def _band_half(name, length, label, extras):
    """One folded waistband half: a rectangle with a center fold line."""
    band_h = 2.0 * (BAND_H + seam_allowance)
    cy = band_h / 2.0
    fold = fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)])
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        internals=[fold] + extras,
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def build_waistbands(front, back):
    """Two waistband halves: one extended +60 into the crossover tab, one plain."""
    waists = front.edge("waist").length() + back.edge("waist").length()
    band_h = 2.0 * (BAND_H + seam_allowance)
    tab_len = waists + TAB + 2.0 * seam_allowance
    plain_len = waists + 2.0 * seam_allowance
    tab_line = fc.Internal(
        "tab line",
        [fc.P(tab_len - TAB, 0.0), fc.P(tab_len - TAB, band_h)],
    )
    tab_half = _band_half(
        "waistband_tab", tab_len, "Waistband Half (tab)",
        [tab_line, _button_cross(tab_len - TAB / 2.0, band_h * 0.25)],
    )
    plain_half = _band_half("waistband_plain", plain_len, "Waistband Half (plain)", [])
    return tab_half, plain_half


def build():
    pattern = fc.PatternSet("dress-trousers")
    front, back = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece in ("waistband_tab", "waistband_plain"):
        tab_half, plain_half = build_waistbands(front, back)
        if everything or target_piece == "waistband_tab":
            pattern.add(tab_half)
        if everything or target_piece == "waistband_plain":
            pattern.add(plain_half)
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        pattern.declare_seam(
            [("waistband_tab", "bottom")],
            [("front", "waist"), ("back", "waist")],
            tol=2.5,
            ease=TAB + 2.0 * seam_allowance,
        )
        pattern.declare_seam(
            [("waistband_plain", "bottom")],
            [("front", "waist"), ("back", "waist")],
            tol=2.5,
            ease=2.0 * seam_allowance,
        )
    pattern.metadata = {
        "fc100_rank": 36,
        "fabric_hint": "popelina-algodon",
        "note": "suiting-wool card pending; popelina as stand-in",
    }
    return pattern


result = build()

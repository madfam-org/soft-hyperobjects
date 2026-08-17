"""
Cargo pants — FC-100 rank #37. Fashion Cabinet Garment Cartridge.

The chinos block relaxed for utility wear: front/back legs (cut 2 each) with
extra hip ease and a wide straight hem, the front inseam bowed by a solved
amount to match the deeper back fork, a grown-on fly extension with a fly
J-topstitch guide and fly-stop notch, diagonal slash pockets with pocket-mouth
notches on both side seams, two back waist darts plus a back patch-pocket
placement — and the bellows cargo pocket drafted as real pieces: a hexagonal
main-face-plus-fold-wings outline (one closed 8-edge outline with bellows fold
lines as internals), an angled-corner flap, and a mid-thigh placement
rectangle marked on each front leg. The waistband is the dress-trousers
two-half split (crossover tab + plain), each half verified with its own eased
check; six belt-loop strips.

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
inseam_length = float(PARAM(lambda: inseam_length, 760.0))
front_rise    = float(PARAM(lambda: front_rise, 275.0))
back_rise     = float(PARAM(lambda: back_rise, 315.0))
cargo_ease    = float(PARAM(lambda: cargo_ease, 160.0))
hem_width     = float(PARAM(lambda: hem_width, 130.0))     # front half-hem, flat
pocket_width  = float(PARAM(lambda: pocket_width, 180.0))
pocket_height = float(PARAM(lambda: pocket_height, 200.0))
bellows       = float(PARAM(lambda: bellows, 30.0))
fly_width     = float(PARAM(lambda: fly_width, 38.0))
fly_depth     = float(PARAM(lambda: fly_depth, 200.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 35.0))

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(500.0, min(waist_girth, hip_girth))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
cargo_ease = max(40.0, min(cargo_ease, 400.0))
hem_width = max(80.0, min(hem_width, 260.0))
pocket_width = max(120.0, min(pocket_width, 260.0))
pocket_height = max(140.0, min(pocket_height, 280.0))
bellows = max(10.0, min(bellows, pocket_width / 3.0))
fly_width = max(20.0, min(fly_width, 60.0))
fly_depth = max(80.0, min(fly_depth, front_rise - 30.0))

HIP_E = hip_girth + cargo_ease
WAIST_E = waist_girth + 40.0                 # waist wearing ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
HIP_LINE_Y = CROTCH_Y + front_rise * 0.4
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0

DART_INTAKE, DART_LEN = 12.0, 90.0
TAB = 60.0                                   # waistband crossover-tab extension
BAND_H = 40.0                                # finished waistband height (folded)
LOOP_W, LOOP_H = 12.0, 55.0
BPKT_W, BPKT_H = 130.0, 140.0                # back patch-pocket marking
SLASH_DROP = 140.0                           # slash mouth: below waist on the side seam
THIGH_DROP = 120.0                           # cargo placement top: below the crotch line
FLAP_H, FLAP_CLIP = 70.0, 25.0               # flap depth, angled-corner clip


def _fly_j(fw_in):
    """Fly J-topstitch guide: vertical run inside CF hooking toward the fly stop."""
    jx = fw_in - fly_width
    cy = WAIST_Y - fly_depth + fly_width + 10.0
    pts = [fc.P(jx, WAIST_Y), fc.P(jx, cy)]
    for step in range(1, 7):
        a = math.radians(180.0 + 15.0 * step)
        pts.append(fc.P(fw_in + fly_width * math.cos(a), cy + fly_width * math.sin(a)))
    return fc.Internal("fly J topstitch", pts, kind="trace")


def _slash_pocket():
    """Slash-pocket opening: diagonal from the waist to the side seam."""
    return fc.Internal(
        "slash pocket opening",
        [fc.P(55.0, WAIST_Y), fc.P(0.0, WAIST_Y - SLASH_DROP)],
    )


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


def _back_pocket():
    """Back patch-pocket placement rectangle, set below the darts."""
    cx = BW * 0.5
    top = WAIST_Y - 90.0
    corners = [
        fc.P(cx - BPKT_W / 2.0, top - BPKT_H),
        fc.P(cx + BPKT_W / 2.0, top - BPKT_H),
        fc.P(cx + BPKT_W / 2.0, top),
        fc.P(cx - BPKT_W / 2.0, top),
    ]
    return fc.Internal("back pocket placement", corners + corners[:1])


def _cargo_placement():
    """Cargo-pocket placement: the main-face rectangle at mid-thigh."""
    cx = max(pocket_width / 2.0 + 10.0, FHW / 2.0)
    top = max(CROTCH_Y - THIGH_DROP, pocket_height + 30.0)
    corners = [
        fc.P(cx - pocket_width / 2.0, top - pocket_height),
        fc.P(cx + pocket_width / 2.0, top - pocket_height),
        fc.P(cx + pocket_width / 2.0, top),
        fc.P(cx - pocket_width / 2.0, top),
    ]
    return fc.Internal("cargo pocket placement", corners + corners[:1])


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
    pocket_t = (WAIST_Y - SLASH_DROP) / WAIST_Y

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
            fc.Notch("side", pocket_t, "pocket mouth"),
        ],
        grainline=fc.Grainline(fc.P(FW * 0.45, inseam_length * 0.12),
                               fc.P(FW * 0.45, inseam_length * 0.92)),
        internals=[_fly_j(fw_in), _slash_pocket(), _cargo_placement()],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Leg",
    )

    back_crotch = fc.Edge(
        "crotch",
        [fc.Bezier(fc.P(bw_run, cb_y), fc.P(BW - 4.0, cb_y - front_rise * 0.45),
                   fc.P(BW + (b_tip.x - BW) * 0.35, CROTCH_Y + 55.0), b_tip)],
    )
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
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5),
                 fc.Notch("side", pocket_t, "pocket mouth")],
        grainline=fc.Grainline(fc.P(BW * 0.45, inseam_length * 0.12),
                               fc.P(BW * 0.45, inseam_length * 0.92)),
        internals=[_back_dart(bw_run, rise_delta, 0.35, "back dart 1"),
                   _back_dart(bw_run, rise_delta, 0.62, "back dart 2"),
                   _back_pocket()],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Leg",
    )
    return front, back


def build_cargo_pocket():
    """Bellows pocket cut flat: main face + fold wings as one 8-edge outline.

    The wings taper away over the bottom corners so the bellows folds flat;
    the two vertical fold lines are internals at the face/wing boundaries.
    """
    w = 2.0 * bellows + pocket_width
    h = pocket_height
    xa, xb = bellows, bellows + pocket_width
    return fc.Piece(
        "cargo_pocket",
        [
            fc.Edge("bottom", [fc.Line(fc.P(xa, 0.0), fc.P(xb, 0.0))]),
            fc.Edge("corner_b", [fc.Line(fc.P(xb, 0.0), fc.P(w, bellows))]),
            fc.Edge("side_b", [fc.Line(fc.P(w, bellows), fc.P(w, h))]),
            fc.Edge("wing_top_b", [fc.Line(fc.P(w, h), fc.P(xb, h))]),
            fc.Edge("mouth", [fc.Line(fc.P(xb, h), fc.P(xa, h))]),
            fc.Edge("wing_top_a", [fc.Line(fc.P(xa, h), fc.P(0.0, h))]),
            fc.Edge("side_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, bellows))]),
            fc.Edge("corner_a", [fc.Line(fc.P(0.0, bellows), fc.P(xa, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": hem_allowance, "wing_top_a": hem_allowance,
                    "wing_top_b": hem_allowance},
        notches=[fc.Notch("mouth", 0.5, "flap match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.12), fc.P(w / 2.0, h * 0.88)),
        internals=[fc.Internal("bellows fold a", [fc.P(xa, 0.0), fc.P(xa, h)]),
                   fc.Internal("bellows fold b", [fc.P(xb, 0.0), fc.P(xb, h)])],
        cut=fc.CutSpec(quantity=2),
        label="Cargo Bellows Pocket",
    )


def build_flap():
    """Cargo flap: pocket_width wide, 70 deep, angled lower corners."""
    w, h, c = pocket_width, FLAP_H, FLAP_CLIP
    return fc.Piece(
        "flap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(c, 0.0), fc.P(w - c, 0.0))]),
            fc.Edge("corner_b", [fc.Line(fc.P(w - c, 0.0), fc.P(w, c))]),
            fc.Edge("side_b", [fc.Line(fc.P(w, c), fc.P(w, h))]),
            fc.Edge("attach", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("side_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, c))]),
            fc.Edge("corner_a", [fc.Line(fc.P(0.0, c), fc.P(c, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "pocket match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.2), fc.P(w / 2.0, h * 0.8)),
        cut=fc.CutSpec(quantity=2),
        label="Pocket Flap",
    )


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


def build_belt_loop():
    """Belt-loop strip, cut six."""
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
        cut=fc.CutSpec(quantity=6),
        label="Belt Loop",
    )


def build():
    pattern = fc.PatternSet("cargo-pants")
    front, back = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "cargo_pocket":
        pattern.add(build_cargo_pocket())
    if everything or target_piece == "flap":
        pattern.add(build_flap())
    if everything or target_piece in ("waistband_tab", "waistband_plain"):
        tab_half, plain_half = build_waistbands(front, back)
        if everything or target_piece == "waistband_tab":
            pattern.add(tab_half)
        if everything or target_piece == "waistband_plain":
            pattern.add(plain_half)
    if everything or target_piece == "belt_loop":
        pattern.add(build_belt_loop())
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
        pattern.declare_seam(("flap", "attach"), ("cargo_pocket", "mouth"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 37,
        "fabric_hint": "mezclilla-denim",
        "drafting": "chinos block relaxed; bellows cargo pockets as pieces; solved inseam bow",
    }
    return pattern


result = build()

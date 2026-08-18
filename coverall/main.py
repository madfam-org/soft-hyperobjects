"""
Coverall — FC-100 rank #84 (Coverall / Overol industrial). Fashion Cabinet Cartridge.

The classic mechanic's one-piece work coverall: a shirt-like woven BODICE
(sleeved, collared, front cut 2 with a full CENTER-FRONT SEPARATING ZIPPER from
the collar to the waist) joined to a straight-leg TROUSER at a declared WAIST
SEAM — the jumpsuit top-to-bottom join. Bodice hem half-widths and leg waist
half-widths are driven by the SAME waist formulas ((waist + ease)/4 -/+ a
quarter shift), so the eight-reference waist seam (each physical cut listed
once) closes with delta ~ 0 by construction.

The signature is the ACTION BACK: a bi-swing pleat over each shoulder blade
whose intake is folded at the shoulder seam. The back is cut on fold at CB; its
shoulder edge is drafted LONGER than the front shoulder by the pleat intake, and
the shoulder seam is declared with that intake as EASE — a real, verified
bi-swing that still balances. The pleat fold lines are traced on the back.

Three real PATCH POCKETS (chest bib pocket, hip pocket, thigh tool pocket) use
the patch-pocket hexagon idiom (45 deg bottom chamfers, hem-facing on the
opening, a topstitch attach guide). The collar is a one-piece band SOLVED to the
measured neckline (collar-band method); its CF edges carry the zipper tape
allowance because the separating zipper runs up through the collar. Long sleeves
finish in a buttoned cuff whose length is solved to the sleeve-hem opening.

Hardware — the separating CF zipper and the pocket/cuff snaps — federates to
Yantra4D (zipper-notion, snap family); nothing hard is re-implemented here.

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


_KNOWN = ("bodice_front", "bodice_back", "sleeve", "cuff", "collar",
          "leg_front", "leg_back", "chest_pocket", "hip_pocket", "thigh_pocket",
          "set")
target_piece = str(PARAM(lambda: target_piece, "set"))

# ── Parameters (millimetres; girths are full-body) ───────────────────────────
chest_girth    = float(PARAM(lambda: chest_girth, 1080.0))
waist_girth    = float(PARAM(lambda: waist_girth, 940.0))
hip_girth      = float(PARAM(lambda: hip_girth, 1060.0))
neck_girth     = float(PARAM(lambda: neck_girth, 420.0))
bodice_length  = float(PARAM(lambda: bodice_length, 430.0))   # nape to waist seam
sleeve_length  = float(PARAM(lambda: sleeve_length, 610.0))   # shoulder to cuff line
inseam_length  = float(PARAM(lambda: inseam_length, 740.0))
front_rise     = float(PARAM(lambda: front_rise, 280.0))
back_rise      = float(PARAM(lambda: back_rise, 320.0))
coverall_ease  = float(PARAM(lambda: coverall_ease, 220.0))   # total woven work ease
hem_width      = float(PARAM(lambda: hem_width, 125.0))       # leg half-hem, flat
action_pleat   = float(PARAM(lambda: action_pleat, 45.0))     # bi-swing intake per blade
collar_height  = float(PARAM(lambda: collar_height, 70.0))
cuff_height    = float(PARAM(lambda: cuff_height, 70.0))
zipper_length  = float(PARAM(lambda: zipper_length, 700.0))   # collar top down along CF
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 35.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
waist_girth = max(550.0, min(waist_girth, 1650.0))
hip_girth = max(700.0, min(hip_girth, 1800.0))
neck_girth = max(320.0, min(neck_girth, 560.0))
bodice_length = max(320.0, min(bodice_length, 620.0))
sleeve_length = max(200.0, min(sleeve_length, 720.0))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(200.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
coverall_ease = max(120.0, min(coverall_ease, 400.0))
hem_width = max(95.0, min(hem_width, 260.0))
action_pleat = max(0.0, min(action_pleat, 80.0))
collar_height = max(40.0, min(collar_height, 95.0))
cuff_height = max(45.0, min(cuff_height, 100.0))
zipper_length = max(400.0, min(zipper_length, 1000.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

# ── Constants ────────────────────────────────────────────────────────────────
QS = 12.0               # quarter shift: front quarters narrower, back wider
ZIP_SA = 15.0           # tape allowance on the CF / collar center edge (zip seam)
ZIP_STITCH = 8.0        # stitch line offset from the zip seam (zipper-notion)
SHOULDER_DROP = 30.0    # work-shirt shoulder slope
BACK_NECK_DROP = 22.0
COLLAR_RISE = 12.0      # band CF curl
COLLAR_POINT = 8.0      # gentle forward lean of the collar end
PLEAT_LEN = 220.0       # action-back pleat fold-line length below the shoulder
BACK_HEM_EXTRA = 12.0   # back leg hem slightly wider, like the block

# ── Shared waist formulas — THE waist seam is driven from here, both sides ──
CHEST_E = chest_girth + coverall_ease
WAIST_E = waist_girth + coverall_ease
HIP_E = hip_girth + coverall_ease
WAIST_F, WAIST_B = WAIST_E / 4.0 - QS, WAIST_E / 4.0 + QS

# ── Bodice frame: waist seam at y = 0, HPS at y = bodice_length + 20 ─────────
L = bodice_length
HPS_Y = L + 20.0
NW = max(64.0, neck_girth / 5.0)                 # half neck width at HPS
FRONT_NECK_DROP = max(70.0, neck_girth / 5.0 + 10.0)
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP
CB_NECK_Y = HPS_Y - BACK_NECK_DROP
AH = CHEST_E / 8.0 + 100.0                        # roomy work armhole depth
AH = max(170.0, min(AH, L - 90.0))
CHEST_F, CHEST_B = CHEST_E / 4.0 - QS, CHEST_E / 4.0 + QS
UNDERARM_Y = HPS_Y - SHOULDER_DROP - AH
# Shoulder tip x: the front tip sits at SH_TIP_X; the back tip extends past it by
# the action-pleat intake (the extra length is folded at the shoulder seam).
SH_TIP_X = CHEST_F - 6.0
SH_END = fc.P(SH_TIP_X, HPS_Y - SHOULDER_DROP)

# ── Trouser frame: hem at y = 0, front waist line at y = inseam + front_rise ──
CROTCH_Y = inseam_length
P_WAIST_Y = inseam_length + front_rise
RISE_DIFF = back_rise - front_rise
PFW, PBW = HIP_E / 4.0 - QS, HIP_E / 4.0 + QS
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + BACK_HEM_EXTRA
# The straight waist edge from the side (x=0) up to the CB rises RISE_DIFF on the
# back; solve its inner x so the slanted back-waist edge is EXACTLY the shared
# back waist quarter (front is horizontal, so its x is the quarter directly).
PANT_WAIST_XF = WAIST_F
PANT_WAIST_XB = math.sqrt(max(1.0, WAIST_B * WAIST_B - RISE_DIFF * RISE_DIFF))


# ── Bodice edges ─────────────────────────────────────────────────────────────
def _front_neck_edge():
    """Front neck scoop from the CF zip point up to the HPS."""
    cf = fc.P(0.0, CF_NECK_Y)
    return fc.Edge(
        "neck",
        [fc.Bezier(cf, fc.P(NW * 0.55, CF_NECK_Y),
                   fc.P(NW, HPS_Y - FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )


def _back_neck_edge():
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, CB_NECK_Y), fc.P(NW * 0.55, CB_NECK_Y),
                   fc.P(NW, CB_NECK_Y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )


def _armhole_edge(chest_w):
    """Roomy work armhole; front/back differ only by the quarter shift."""
    underarm = fc.P(chest_w, UNDERARM_Y)
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(chest_w - 14.0, SH_END.y - AH * 0.34),
                   fc.P(chest_w - 6.0, UNDERARM_Y + AH * 0.30), underarm)],
    )


def _side_edge(chest_w, waist_w):
    """Straight taper underarm -> waist seam. Front and back share the same
    vertical run and horizontal intake (chest_w - waist_w == (CHEST_E-WAIST_E)/4
    on both), so the declared bodice side seam matches by construction."""
    return fc.Edge("side", [fc.Line(fc.P(chest_w, UNDERARM_Y), fc.P(waist_w, 0.0))])


def _zip_stitch_line(top_y):
    """Topstitch guide 8 mm in from the CF zip seam (zipper-notion practice)."""
    return fc.Internal(
        "zipper stitch line",
        [fc.P(ZIP_STITCH, 0.0), fc.P(ZIP_STITCH, top_y)],
        kind="trace",
    )


def _bib_pocket_trace():
    """Chest bib patch-pocket placement (wearer's left once mirrored)."""
    top = min(UNDERARM_Y + 40.0, CF_NECK_Y - 30.0)
    bottom = max(top - 150.0, 60.0)
    left = CHEST_F * 0.34
    right = min(left + 130.0, CHEST_F * 0.94)
    return fc.Internal(
        "chest pocket placement",
        [fc.P(left, top), fc.P(right, top), fc.P(right, bottom),
         fc.P(left, bottom), fc.P(left, top)],
        kind="trace",
    )


def _bodice_front():
    """Front, cut 2 mirrored: the straight CF edge is the separating-zip seam."""
    neck = _front_neck_edge()
    return fc.Piece(
        "bodice_front",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, CF_NECK_Y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(CHEST_F),
            _side_edge(CHEST_F, WAIST_F),
            fc.Edge("hem", [fc.Line(fc.P(WAIST_F, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"center": ZIP_SA},  # CF carries the separating zipper tape
        notches=[
            fc.Notch("hem", 0.5, "waist quarter"),
            fc.Notch("side", 0.5, "side match"),
            fc.Notch("center", 0.0, "zipper bottom stop"),
            # Zip runs collar-top down; on the bodice CF the tape covers the whole
            # center edge — the top stop sits at the neck point (fraction 1.0).
            fc.Notch("center", min(1.0, zipper_length / (CF_NECK_Y + collar_height)),
                     "zipper (continues into collar)"),
        ],
        grainline=fc.Grainline(fc.P(CHEST_F * 0.55, 60.0),
                               fc.P(CHEST_F * 0.55, UNDERARM_Y - 40.0)),
        internals=[_zip_stitch_line(CF_NECK_Y), _bib_pocket_trace()],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bodice Front",
    )


def _action_pleat_traces():
    """Bi-swing pleat fold lines: an inverted pleat centered over the shoulder
    blade, drawn from just under the shoulder seam straight down."""
    cx = SH_TIP_X * 0.58                            # over the shoulder blade
    top = HPS_Y - SHOULDER_DROP - 8.0
    half = action_pleat / 2.0
    return [
        fc.Internal("action pleat fold (outer)",
                    [fc.P(cx - half, top), fc.P(cx - half, top - PLEAT_LEN)],
                    kind="trace"),
        fc.Internal("action pleat fold (center)",
                    [fc.P(cx, top), fc.P(cx, top - PLEAT_LEN)],
                    kind="trace"),
        fc.Internal("action pleat fold (inner)",
                    [fc.P(cx + half, top), fc.P(cx + half, top - PLEAT_LEN)],
                    kind="trace"),
    ]


def _bodice_back():
    """Back, cut 1 on fold at CB. The action-back bi-swing pleat is drafted into
    the SHOULDER edge as extra length (`action_pleat`); the shoulder seam is
    declared with that intake as ease, so the pleat is a real verified feature.
    """
    # Shoulder runs HPS -> shoulder tip; add the pleat intake at the tip so the
    # back shoulder is longer than the front by exactly `action_pleat`.
    sh_tip_back = fc.P(SH_TIP_X + action_pleat, HPS_Y - SHOULDER_DROP)
    return fc.Piece(
        "bodice_back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, CB_NECK_Y))]),
            _back_neck_edge(),
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), sh_tip_back)]),
            # Armhole starts at the pleated shoulder tip; keep the same underarm.
            fc.Edge(
                "armhole",
                [fc.Bezier(sh_tip_back,
                           fc.P(CHEST_B - 14.0, sh_tip_back.y - AH * 0.34),
                           fc.P(CHEST_B - 6.0, UNDERARM_Y + AH * 0.30),
                           fc.P(CHEST_B, UNDERARM_Y))],
            ),
            _side_edge(CHEST_B, WAIST_B),
            fc.Edge("hem", [fc.Line(fc.P(WAIST_B, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[
            fc.Notch("hem", 0.5, "waist quarter"),
            fc.Notch("side", 0.5, "side match"),
        ],
        grainline=fc.Grainline(fc.P(CHEST_B * 0.55, 60.0),
                               fc.P(CHEST_B * 0.55, UNDERARM_Y - 40.0)),
        internals=_action_pleat_traces(),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Bodice Back (action pleat)",
    )


# ── Sleeve + cuff ────────────────────────────────────────────────────────────
def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R->L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    """Cap solved by bisection to the front + back armholes, zero ease. Long
    work sleeve tapering to a plackettless cuffed opening."""
    ch = max(55.0, AH * 0.34)                       # cap height
    sl = max(80.0, sleeve_length - ch - cuff_height)  # cap seam down to cuff line
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    hb = hi
    for _ in range(52):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs {cap_target:.1f}"
        )
    chw = max(95.0, hb * 0.66)                       # cuff-line opening half-width
    piece = fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("cap", 0.5, "shoulder match"),
                 fc.Notch("hem", 0.5, "cuff pleat")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )
    return piece, 2.0 * chw


def build_cuff(cuff_opening):
    """Buttoned cuff band; length = sleeve-hem opening + wearing/overlap ease.
    Drafted flat (net), folds double at `cuff_height`. Snaps federate to
    Yantra4D."""
    overlap = 30.0
    length = cuff_opening + overlap + 2.0 * seam_allowance
    band_h = 2.0 * (cuff_height + seam_allowance)
    cy = band_h / 2.0
    return fc.Piece(
        "cuff",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        internals=[fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)])],
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cuff",
    ), overlap


# ── Collar (one-piece band, solved to the neckline; CF is the zip edge) ──────
def _collar_neck_edge(flat):
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(half_target):
    """Band collar, half on fold at CB; neck edge bisected to
    half_target = front.neck + back.neck (per half). The CF (front_edge) carries
    the SAME zipper tape allowance — the separating zipper runs up through it."""
    lo, hi = half_target * 0.7, half_target * 1.05
    for _ in range(52):
        mid = (lo + hi) / 2.0
        if _collar_neck_edge(mid).length(0.05) < half_target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(_collar_neck_edge(flat).length(0.05) - half_target) > 1.0:
        raise ValueError("collar neck-edge solver did not converge")
    point = fc.P(flat + COLLAR_POINT, COLLAR_RISE + collar_height)
    top_start = fc.P(0.0, collar_height)
    piece = fc.Piece(
        "collar",
        [
            _collar_neck_edge(flat),
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_RISE), point)]),
            fc.Edge("top", [fc.curve_through(point, top_start, bulge=0.04, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"front_edge": ZIP_SA},  # zipper runs up through the collar
        notches=[fc.Notch("neck", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(flat * 0.20, collar_height * 0.55),
                               fc.P(flat * 0.75, collar_height * 0.55 + 7.0)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Band Collar (half, on fold)",
    )
    return piece, flat


# ── Trouser (jumpsuit/chinos lineage, woven ease, fitted waist seam) ────────
def _leg_edges(width, fork, hem_w, waist_x, cb_y, rise):
    tip = fc.P(width + fork, CROTCH_Y)
    waist = fc.Edge("waist", [fc.Line(fc.P(0.0, P_WAIST_Y), fc.P(waist_x, cb_y))])
    crotch = fc.Edge(
        "crotch",
        [fc.Bezier(fc.P(waist_x, cb_y), fc.P(width - 4.0, cb_y - rise * 0.45),
                   fc.P(width + (tip.x - width) * 0.35, CROTCH_Y + 55.0), tip)],
    )

    def inseam(bulge):
        return fc.Edge(
            "inseam",
            [fc.curve_through(tip, fc.P(hem_w, 0.0), bulge=bulge, side=-1.0)],
        )

    return waist, crotch, inseam


def _thigh_pocket_trace():
    """Tool/thigh patch-pocket placement on the front leg (wearer's left)."""
    top = min(P_WAIST_Y - 260.0, CROTCH_Y + front_rise * 0.55)
    bottom = max(top - 170.0, 120.0)
    left = PFW * 0.30
    right = min(left + 150.0, PFW * 0.95)
    return fc.Internal(
        "thigh pocket placement",
        [fc.P(left, top), fc.P(right, top), fc.P(right, bottom),
         fc.P(left, bottom), fc.P(left, top)],
        kind="trace",
    )


def build_legs():
    f_waist, f_crotch, f_inseam = _leg_edges(
        PFW, FORK_F, FHW, PANT_WAIST_XF, P_WAIST_Y, front_rise)
    b_waist, b_crotch, b_inseam = _leg_edges(
        PBW, FORK_B, BHW, PANT_WAIST_XB, P_WAIST_Y + RISE_DIFF, back_rise)
    # Solve the front-inseam bow so it matches the deeper back (bisection).
    back_len = b_inseam(0.0).length(0.05)
    lo, hi = 0.0, 0.35
    for _ in range(46):
        mid = (lo + hi) / 2.0
        if f_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(f_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge")

    def make(name, waist, crotch, inseam_edge, hem_w, width, label, internals):
        edges = [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, P_WAIST_Y))]),
            waist,
            crotch,
            inseam_edge,
            fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))]),
        ]
        return fc.Piece(
            name, edges,
            seam_allowance=seam_allowance,
            allowances={"hem": hem_allowance},  # plain open hem
            notches=[fc.Notch("waist", 0.5, "waist quarter"),
                     fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
            grainline=fc.Grainline(fc.P(width * 0.45, inseam_length * 0.12),
                                   fc.P(width * 0.45, inseam_length * 0.92)),
            internals=internals,
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("leg_front", f_waist, f_crotch, f_inseam(bulge), FHW, PFW,
                 "Leg Front", [_thigh_pocket_trace()])
    back = make("leg_back", b_waist, b_crotch, b_inseam(0.0), BHW, PBW,
                "Leg Back", [])
    return front, back


# ── Patch pockets (real hexagon pieces; the patch-pocket enabler idiom) ──────
def _patch_pocket(name, w, h, chamfer, quantity, label):
    """Rectangular patch pocket, 45 deg bottom chamfers; TOP is the opening and
    carries a hem-facing allowance; a topstitch guide traces the attach path."""
    c = max(5.0, min(chamfer, min(w, h) / 3.0 - 0.5))
    inset = 8.0
    return fc.Piece(
        name,
        [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, c))]),
            fc.Edge("chamfer_r", [fc.Line(fc.P(w, c), fc.P(w - c, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w - c, 0.0), fc.P(c, 0.0))]),
            fc.Edge("chamfer_l", [fc.Line(fc.P(c, 0.0), fc.P(0.0, c))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, c), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": 25.0},  # opening hem facing
        notches=[fc.Notch("top", 0.5, "center match")],
        grainline=fc.Grainline(fc.P(w / 2.0, h * 0.15), fc.P(w / 2.0, h * 0.85)),
        internals=[fc.Internal(
            "topstitch guide",
            [fc.P(w - inset, h), fc.P(w - inset, inset),
             fc.P(inset, inset), fc.P(inset, h)])],
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def build():
    pattern = fc.PatternSet("coverall")
    b_front = _bodice_front()
    b_back = _bodice_back()
    leg_front, leg_back = build_legs()
    cap_target = (b_front.edge("armhole").length(0.05)
                  + b_back.edge("armhole").length(0.05))
    half_neck = (b_front.edge("neck").length(0.05)
                 + b_back.edge("neck").length(0.05))

    known = target_piece in _KNOWN
    want = {
        "bodice_front": not known or target_piece in ("bodice_front", "set"),
        "bodice_back": not known or target_piece in ("bodice_back", "set"),
        "sleeve": not known or target_piece in ("sleeve", "set"),
        "cuff": not known or target_piece in ("cuff", "set"),
        "collar": not known or target_piece in ("collar", "set"),
        "leg_front": not known or target_piece in ("leg_front", "set"),
        "leg_back": not known or target_piece in ("leg_back", "set"),
        "chest_pocket": not known or target_piece in ("chest_pocket", "set"),
        "hip_pocket": not known or target_piece in ("hip_pocket", "set"),
        "thigh_pocket": not known or target_piece in ("thigh_pocket", "set"),
    }

    sleeve_opening = None
    cuff_overlap = 30.0
    collar_flat = None
    if want["bodice_front"]:
        pattern.add(b_front)
    if want["bodice_back"]:
        pattern.add(b_back)
    if want["sleeve"]:
        sleeve, sleeve_opening = build_sleeve(cap_target)
        pattern.add(sleeve)
    if want["cuff"]:
        if sleeve_opening is None:
            _s, sleeve_opening = build_sleeve(cap_target)
        cuff, cuff_overlap = build_cuff(sleeve_opening)
        pattern.add(cuff)
    if want["collar"]:
        collar, collar_flat = build_collar(half_neck)
        pattern.add(collar)
    if want["leg_front"]:
        pattern.add(leg_front)
    if want["leg_back"]:
        pattern.add(leg_back)
    if want["chest_pocket"]:
        pattern.add(_patch_pocket("chest_pocket", 130.0, 150.0, 25.0, 2,
                                  "Chest Bib Pocket"))
    if want["hip_pocket"]:
        pattern.add(_patch_pocket("hip_pocket", 150.0, 165.0, 30.0, 2,
                                  "Hip Pocket"))
    if want["thigh_pocket"]:
        pattern.add(_patch_pocket("thigh_pocket", 150.0, 175.0, 20.0, 1,
                                  "Thigh Tool Pocket"))

    # ── Seams (all delta ~ 0) ────────────────────────────────────────────────
    if want["bodice_front"] and want["bodice_back"]:
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"),
                             tol=1.5)
        # Action back: the back shoulder is drafted LONGER than the front by the
        # pleat intake, folded into a bi-swing pleat at the shoulder seam. The
        # longer side (back) is side_a; the ease is the measured extra length —
        # both sides count twice (front cut 2, back on fold, two shoulders each).
        front_sh = b_front.edge("shoulder").length(0.05)
        back_sh = b_back.edge("shoulder").length(0.05)
        pleat_ease = 2.0 * (back_sh - front_sh)
        pattern.declare_seam(
            [("bodice_back", "shoulder"), ("bodice_back", "shoulder")],
            [("bodice_front", "shoulder"), ("bodice_front", "shoulder")],
            tol=1.5, ease=pleat_ease,
        )
    if want["sleeve"] and want["bodice_front"] and want["bodice_back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("bodice_front", "armhole"), ("bodice_back", "armhole")],
            tol=2.0,
        )
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
    if want["sleeve"] and want["cuff"]:
        # Two cuffs (cut 2) each sew to one sleeve hem; the cuff bottom carries
        # the closure overlap as declared ease.
        pattern.declare_seam(
            [("cuff", "bottom")],
            [("sleeve", "hem")],
            tol=2.0, ease=cuff_overlap + 2.0 * seam_allowance,
        )
    if want["collar"] and want["bodice_front"] and want["bodice_back"]:
        pattern.declare_seam(
            [("collar", "neck")],
            [("bodice_front", "neck"), ("bodice_back", "neck")],
            tol=2.0,
        )
    if want["leg_front"] and want["leg_back"]:
        pattern.declare_seam(("leg_front", "side"), ("leg_back", "side"), tol=1.5)
        pattern.declare_seam(("leg_front", "inseam"), ("leg_back", "inseam"),
                             tol=1.5)
    if (want["bodice_front"] and want["bodice_back"]
            and want["leg_front"] and want["leg_back"]):
        # THE WAIST SEAM (the jumpsuit top-to-bottom join). Each reference
        # appears once per physical cut: the cut-2 fronts and the on-fold back
        # (sewing in twice) on the bodice side; the cut-2 legs on the trouser
        # side. Both sides are driven by WAIST_F/WAIST_B, so delta ~ 0.
        pattern.declare_seam(
            [("bodice_front", "hem"), ("bodice_front", "hem"),
             ("bodice_back", "hem"), ("bodice_back", "hem")],
            [("leg_front", "waist"), ("leg_front", "waist"),
             ("leg_back", "waist"), ("leg_back", "waist")],
            tol=3.0,
        )

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1500.0                            # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.62)  # denim, one-piece nesting
    pattern.bom = [
        {"item": "mezclilla-denim", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"heavy 12 oz denim at {fabric_width:.0f} mm width, 62% marker "
                 "efficiency; a one-piece coverall nests poorly — cut single ply"},
        {"item": "separating zipper (CF, collar to waist)",
         "qty": round(zipper_length), "unit": "mm",
         "note": "brass/molded separating zip; runs collar-top down through the "
                 "whole center front; HARD GOOD — federates to Yantra4D "
                 "(zipper-notion, subtype separating), not drafted here"},
        {"item": "snap fasteners Ø 15 mm", "qty": 8, "unit": "pieces",
         "note": "2 cuffs + 3 patch-pocket flaps + spares; HARD GOODS federate "
                 "to Yantra4D (snap family), not drafted here"},
        {"item": "heavy topstitch thread (Tex 40) + bar-tack thread", "qty": 1,
         "unit": "set",
         "note": "fell/topstitch the load-bearing seams; bar-tack pocket mouths "
                 "and the action-pleat ends per the denim card"},
        {"item": "jeans needle 100/16 + universal thread", "qty": 1, "unit": "set",
         "note": "heavy denim construction"},
    ]

    pattern.metadata = {
        "fc100_rank": 84,
        "fabric_hint": "mezclilla-denim",
        "one_piece": "shirt bodice + trouser joined at a declared waist seam "
                     "(jumpsuit method); the CF separating zipper runs collar to waist",
        "action_back": {
            "kind": "bi-swing shoulder pleat",
            "intake_per_blade_mm": round(action_pleat, 1),
            "declared_as": "ease on the shoulder seam (2 x intake); pleat folds "
                           "traced on the back",
        },
        "patch_pockets": ["chest_pocket (cut 2)", "hip_pocket (cut 2)",
                          "thigh_pocket (cut 1)"],
        "waist_seam_mm": round(2.0 * (WAIST_F + WAIST_B), 1),
        "bodice_waist_front_mm": round(WAIST_F, 1),
        "bodice_waist_back_mm": round(WAIST_B, 1),
        "leg_waist_front_mm": round(PANT_WAIST_XF, 1),
        "leg_waist_back_slanted_mm": round(
            math.hypot(PANT_WAIST_XB, RISE_DIFF), 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "collar_half_target_mm": round(half_neck, 1),
        "collar_flat_mm": None if collar_flat is None else round(collar_flat, 1),
        "neck_opening_full_mm": round(2.0 * half_neck, 1),
        "zipper_length_mm": round(zipper_length, 1),
        "drafting": "teaching-grade one-piece work coverall: shirt bodice (CF "
                    "separating zip, solved band collar, bi-swing action back) "
                    "joined to a side-seamed straight-leg trouser at a shared-"
                    "formula waist seam; sleeve cap, collar neck, and front "
                    "inseam bow all solved by bisection to delta ~ 0",
    }
    return pattern


result = build()

"""
Chelsea boot upper — FC-400 rank #360, Lane 6 (footwear). Fashion Cabinet Cartridge.

The Chelsea boot: an ankle boot with NO laces — a vamp over the foot, two quarters up the
ankle, and an ELASTIC SIDE GUSSET on each side that lets the boot pull on and grip. A pull
tab at the back heel helps it on. The elastic gusset's tension is delegated to a Yantra4D
side-release-buckle used here as the printed gusset tension-and-latch element (co-create:
the wearable buckle exists in the yantra4d 500 catalog; this is its first FC boot use).

FOOT SIZING NOTE (honest, checked): ISO 8559 declares NO foot landmark codes. This
cartridge drafts from PLAIN sized parameters (foot_length, foot_girth, ankle_girth is
canonical but the plain foot params drive the shape). No landmark code is invented.

Pieces:
  - vamp    : toe + instep cover (cut 1).
  - quarter : ankle wrap (cut 2, mirrored), with a gusset opening cut on the side.
  - gusset  : the elastic side panel (cut 2), fitting the quarter's gusset opening.
  - tab     : the back pull tab (cut 1).

Solving and clamps. Lasting arcs are PROPORTIONATE BOWS over each piece's chord (never a
share of the whole sole, which slivers at extremes). The gusset opening length on the
quarter is drafted to the gusset panel length so the declared seam balances. Boot height
is floored.

Hardware: Yantra4D side-release-buckle (co-create; the gusset tension element).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # vamp|quarter|gusset|tab|set

foot_length = float(PARAM(lambda: foot_length, 260.0))
foot_girth = float(PARAM(lambda: foot_girth, 245.0))
boot_height = float(PARAM(lambda: boot_height, 150.0))   # sole to top of the ankle
vamp_depth = float(PARAM(lambda: vamp_depth, 120.0))
gusset_width = float(PARAM(lambda: gusset_width, 45.0))  # elastic panel width
gusset_height = float(PARAM(lambda: gusset_height, 100.0))
webbing_w = float(PARAM(lambda: webbing_w, 25.0))        # buckle webbing width
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

foot_length = max(150.0, min(foot_length, 340.0))
foot_girth = max(150.0, min(foot_girth, 330.0))
boot_height = max(90.0, min(boot_height, 320.0))
vamp_depth = max(60.0, min(vamp_depth, 200.0))
gusset_width = max(20.0, min(gusset_width, 110.0))
gusset_height = max(50.0, min(gusset_height, 260.0))
webbing_w = max(15.0, min(webbing_w, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

SOLE_K = 1.08
VAMP_SHARE = max(0.30, min(vamp_depth / foot_length + 0.12, 0.58))
VAMP_HALF = max(20.0, foot_girth / 2.0 / 2.0 + 8.0)
QUARTER_HALF = max(18.0, foot_girth / 2.0 / 2.0 * 0.95)
_vamp_bow = 1.10 + 0.55 * VAMP_SHARE
_quarter_bow = 1.10 + 0.35 * (1.0 - VAMP_SHARE)
VAMP_LAST = 2.0 * VAMP_HALF * _vamp_bow
QUARTER_LAST = 2.0 * QUARTER_HALF * _quarter_bow
BOOT_H = max(80.0, boot_height)
# Gusset height clamped below the boot height so the opening fits inside the quarter.
GH = max(40.0, min(gusset_height, BOOT_H - 20.0))
GW = max(20.0, gusset_width)


def _arc(name, p0, p1, target, side):
    def mk(bulge):
        return fc.Edge(name, [fc.curve_through(p0, p1, bulge=bulge, side=side)])
    chord = ((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2) ** 0.5
    if target <= chord:
        raise ValueError(f"{name}: target {target:.1f} < chord {chord:.1f}")
    lo, hi = 0.0, 3.0
    if mk(hi).length(0.05) < target:
        raise ValueError(f"{name}: target unreachable")
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if mk(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    return mk((lo + hi) / 2.0)


def build_vamp():
    h = vamp_depth
    p_ll = fc.P(-VAMP_HALF, 0.0)
    p_lr = fc.P(VAMP_HALF, 0.0)
    p_tr = fc.P(VAMP_HALF * 0.80, h)
    p_tl = fc.P(-VAMP_HALF * 0.80, h)
    return fc.Piece(
        "vamp",
        [
            _arc("lasting", p_ll, p_lr, VAMP_LAST, side=1.0),
            fc.Edge("throat_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("throat", [fc.curve_through(p_tr, p_tl, bulge=0.10, side=1.0)]),
            fc.Edge("throat_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"throat": 10.0},
        notches=[fc.Notch("lasting", 0.5, "centre toe"), fc.Notch("throat", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe + instep)",
    )


def _gusset_opening_len(throat_len):
    """The gusset opening length on the quarter — GH clamped below the throat length so it
    fits inside the throat edge. Computed once so the quarter and the gusset panel agree."""
    dx = QUARTER_HALF * 0.12
    dy = max(1.0, (throat_len ** 2 - dx ** 2)) ** 0.5
    return max(30.0, min(GH, dy - 15.0))


def build_quarter(throat_len):
    """The ankle wrap (cut 2 mirrored). A gusset opening (a straight edge of length gh_eff)
    is cut into the front-side so the elastic gusset fits in. Its throat edge is drafted to
    the vamp's throat side length."""
    hw = QUARTER_HALF
    lasting = QUARTER_LAST
    # base corners
    p_bl = fc.P(-hw, 0.0)
    p_br = fc.P(hw, 0.0)
    # throat side: from the throat-side lower up to a top; length == throat_len EXACTLY
    # (never capped — the declared seam must balance). The effective boot height is the
    # LARGER of the requested boot_height and the throat top, so the shaft always contains
    # the throat and the back edge never dips below it.
    dx = hw * 0.12
    dy2 = throat_len ** 2 - dx ** 2
    if dy2 <= 1.0:
        raise ValueError("quarter: throat shorter than its run")
    dy = dy2 ** 0.5
    eff_boot_h = max(BOOT_H, dy)
    p_throat_top = fc.P(hw - dx, dy)
    # gusset opening: a vertical slit of length gh_eff on the throat side, from the top
    # down. gh_eff is clamped below the throat length so the opening fits inside it.
    gh_eff = _gusset_opening_len(throat_len)
    p_gusset_bot = fc.P(hw - dx, dy - gh_eff)
    p_top_back = fc.P(-hw + dx, eff_boot_h)
    return fc.Piece(
        "quarter",
        [
            _arc("lasting", p_bl, p_br, lasting, side=1.0),
            # throat side up to the gusset top
            fc.Edge("throat", [fc.Line(p_br, p_throat_top)]),
            # gusset opening down
            fc.Edge("gusset_edge", [fc.Line(p_throat_top, p_gusset_bot)]),
            # inner front edge from gusset bottom up to the back top (the ankle opening front)
            fc.Edge("topline", [fc.Line(p_gusset_bot, p_top_back)]),
            # back seam down to the base
            fc.Edge("back_seam", [fc.Line(p_top_back, p_bl)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 8.0},
        notches=[fc.Notch("lasting", 0.5, "side"), fc.Notch("gusset_edge", 0.5, "gusset")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, BOOT_H - 8.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Quarter (ankle wrap, gusset opening)",
    )


def build_gusset(opening_len):
    """The elastic side panel (cut 2). A rectangle GW × opening_len that fills the quarter's
    gusset opening; its attach edge matches the quarter's gusset_edge length exactly."""
    gh = opening_len
    return fc.Piece(
        "gusset",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, gh))]),   # to the quarter opening
            fc.Edge("top", [fc.Line(fc.P(0.0, gh), fc.P(GW, gh))]),
            fc.Edge("free", [fc.Line(fc.P(GW, gh), fc.P(GW, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(GW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "gusset centre")],
        grainline=fc.Grainline(fc.P(GW * 0.5, gh * 0.2), fc.P(GW * 0.5, gh * 0.8)),
        internals=[fc.Internal("elastic grain",
                               [fc.P(GW * 0.5, gh * 0.1), fc.P(GW * 0.5, gh * 0.9)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Elastic side gusset",
    )


def build_tab():
    w, h = max(30.0, webbing_w + 20.0), 70.0
    return fc.Piece(
        "tab",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w * 0.8, h))]),
            fc.Edge("top", [fc.curve_through(fc.P(w * 0.8, h), fc.P(w * 0.2, h),
                                             bulge=0.2, side=1.0)]),
            fc.Edge("side_l", [fc.Line(fc.P(w * 0.2, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(w * 0.5, 5.0), fc.P(w * 0.5, h - 5.0)),
        cut=fc.CutSpec(quantity=1),
        label="Back pull tab",
    )


def build():
    pattern = fc.PatternSet("chelsea-boot-upper")
    everything = target_piece == "set"
    vamp = build_vamp()
    throat_len = vamp.edge("throat_r").length(0.05)
    quarter = build_quarter(throat_len)
    gusset = build_gusset(_gusset_opening_len(throat_len))
    tab = build_tab()
    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "quarter":
        pattern.add(quarter)
    if everything or target_piece == "gusset":
        pattern.add(gusset)
    if everything or target_piece == "tab":
        pattern.add(tab)

    names = {p.name for p in pattern.pieces}
    if {"vamp", "quarter"} <= names:
        pattern.declare_seam(("vamp", "throat_r"), ("quarter", "throat"), tol=1.5)
        pattern.declare_seam(("vamp", "throat_l"), ("quarter", "throat"), tol=1.5)
    if {"quarter", "gusset"} <= names:
        pattern.declare_seam(("quarter", "gusset_edge"), ("gusset", "attach"), tol=1.0)
    if "quarter" in names:
        pattern.declare_seam(("quarter", "back_seam"), ("quarter", "back_seam"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "suede / calf leather (upper)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ area proxy at 1400 mm, 55% marker. Per PAIR, double this."},
        {"item": "elastic gusset webbing", "qty": 2, "unit": "pcs",
         "note": "the stretch side panels that let the Chelsea pull on."},
        {"item": "side-release buckle / tension element", "qty": 2, "unit": "count",
         "note": "Yantra4D side-release-buckle (see notion.hardware_ref, co-create) — the "
                 "printed gusset tension-and-latch element; first FC boot use."},
        {"item": "leather sole + welt, waxed thread", "qty": 1, "unit": "pair",
         "note": "lasting-edge stitch-down; a curved needle for the back seam."},
    ]
    pattern.metadata = {
        "fc400_rank": 360, "family": "footwear_soft", "lane": 6,
        "fabric_hint": "leather-suede",
        "silhouette_note": "A lace-free ankle boot: a vamp, two ankle quarters, an elastic "
            "side gusset each side, and a back pull tab.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — ISO 8559 "
            "declares no foot landmark codes, so none is claimed and none is invented.",
        "solved": {
            "vamp_lasting_mm": round(VAMP_LAST, 1),
            "quarter_lasting_mm": round(QUARTER_LAST, 1),
            "throat_seam_mm": round(throat_len, 1),
            "gusset_opening_mm": round(_gusset_opening_len(throat_len), 1),
            "boot_height_mm": round(BOOT_H, 1),
            "note": "lasting arcs are proportionate bows over each chord (never sliver at "
                    "extremes); the gusset height is clamped below the boot height so the "
                    "opening fits inside the quarter",
        },
        "hardware": "Yantra4D side-release-buckle (co-create; the elastic gusset tension "
                    "element — first FC boot use)",
    }
    return pattern


result = build()

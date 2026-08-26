"""
Hand-sewn moccasin upper — FC-400 rank #362, Lane 6 (footwear). Fashion Cabinet Cartridge.

The true moccasin (plug construction): a single WRAPAROUND piece that comes up from under
the foot and wraps the sides and heel, gathered at the toe, and a raised PLUG (the apron)
that fills the U-shaped throat at the front and is whip-stitched to the gathered wrap. There
is no separate sole — the wraparound IS the bottom — which is what makes it a moccasin.

FOOT SIZING NOTE (honest, checked): ISO 8559 declares NO foot landmark codes. This
cartridge drafts from PLAIN sized parameters (foot_length, foot_girth). No landmark code is
invented.

Pieces:
  - wrap  : the wraparound bottom-and-sides (cut 1). A long piece; its inner U-edge is the
            throat the plug sews into, its outer edge is the top opening.
  - plug  : the raised apron (cut 1). Its perimeter (three sides) sews to the wrap's U-edge.

Solving and clamps. The wrap's throat U-edge length is SOLVED and the plug is drafted so its
three sewn sides sum to that exact length, so the declared seam balances. Every derived
width is FLOORED; the plug width is clamped below the wrap width so the throat never
inverts.

Hardware: none — a hand-sewn moccasin is whip-stitched, no hardware.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # wrap|plug|set

foot_length = float(PARAM(lambda: foot_length, 255.0))
foot_girth = float(PARAM(lambda: foot_girth, 240.0))
plug_length = float(PARAM(lambda: plug_length, 110.0))   # how far back the apron reaches
plug_width = float(PARAM(lambda: plug_width, 60.0))      # apron width
side_height = float(PARAM(lambda: side_height, 55.0))    # how high the wrap comes up the sides
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

foot_length = max(150.0, min(foot_length, 330.0))
foot_girth = max(150.0, min(foot_girth, 320.0))
plug_length = max(50.0, min(plug_length, 200.0))
plug_width = max(30.0, min(plug_width, 140.0))
side_height = max(30.0, min(side_height, 130.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# The wrap is drafted flat as a long shape: length ~ foot_length + toe gather, width ~ the
# foot girth flattened plus the side rise on each edge.
WRAP_LEN = max(180.0, foot_length * 1.05)
HALF_W = max(50.0, foot_girth / 2.0 / 2.0 + side_height * 0.6)
# The plug (apron) sits in the front third; its width is clamped below the wrap's half so
# the throat never inverts.
PLUG_W = max(24.0, min(plug_width, HALF_W - 12.0))
PLUG_L = max(40.0, min(plug_length, WRAP_LEN * 0.6))


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


def build_plug():
    """The apron plug. A rounded rectangle whose three sewn sides (two sides + the front
    curve) sum to a known length; the back edge is the plug's own top opening (not sewn to
    the wrap)."""
    w, ln = PLUG_W, PLUG_L
    bl = fc.P(-w / 2.0, 0.0)                              # back-left (top opening side)
    br = fc.P(w / 2.0, 0.0)
    fr = fc.P(w / 2.0 * 0.7, ln)                          # front narrows
    fl = fc.P(-w / 2.0 * 0.7, ln)
    return fc.Piece(
        "plug",
        [
            fc.Edge("back", [fc.Line(bl, br)]),            # the plug's own opening edge
            fc.Edge("sew_r", [fc.Line(br, fr)]),
            fc.Edge("front", [fc.curve_through(fr, fl, bulge=0.22, side=1.0)]),
            fc.Edge("sew_l", [fc.Line(fl, bl)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front", 0.5, "centre toe"), fc.Notch("back", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, ln - 8.0)),
        cut=fc.CutSpec(quantity=1),
        label="Plug (apron)",
    )


def build_wrap(plug_sewn_len):
    """The wraparound bottom-and-sides. Frame: x=0 centre line, y=0 heel, y=WRAP_LEN toe.
    Its inner U-throat (the sew edge the plug fills) has total sewn length == plug_sewn_len.
    Drafted as a long piece with a U notch at the front for the plug."""
    hw = HALF_W
    heel_l = fc.P(-hw, 0.0)
    heel_r = fc.P(hw, 0.0)
    # Toe region: the wrap narrows and the U-throat opens. The throat opening starts at
    # y = WRAP_LEN - PLUG_L and runs to the toe.
    throat_y = WRAP_LEN - PLUG_L
    # The U-throat is a symmetric V of two equal sew edges whose combined length is
    # plug_sewn_len; each edge runs from the throat opening (at x = ±throat_hw) to the toe
    # point (0, toe_y). The throat opening half-width `throat_hw` is CLAMPED below the
    # half-target so the V can ALWAYS reach the target length (a wide opening on a short
    # sewn perimeter would otherwise be unreachable). toe_y is then solved.
    half_target = max(20.0, plug_sewn_len / 2.0)
    throat_hw = min(hw * 0.85, half_target - 10.0)
    dy2 = half_target ** 2 - throat_hw ** 2
    toe_y = throat_y + max(8.0, dy2 ** 0.5)
    side_r_top = fc.P(throat_hw, throat_y)
    side_l_top = fc.P(-throat_hw, throat_y)
    toe = fc.P(0.0, toe_y)
    return fc.Piece(
        "wrap",
        [
            fc.Edge("heel", [fc.Line(heel_l, heel_r)]),        # heel gather / seam
            fc.Edge("side_r", [fc.Line(heel_r, side_r_top)]),   # right top opening
            fc.Edge("sew_r", [fc.Line(side_r_top, toe)]),       # U-throat right (to plug)
            fc.Edge("sew_l", [fc.Line(toe, side_l_top)]),       # U-throat left (to plug)
            fc.Edge("side_l", [fc.Line(side_l_top, heel_l)]),   # left top opening
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sew_r", 0.5, "throat"), fc.Notch("heel", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, 15.0), fc.P(0.0, throat_y - 15.0)),
        internals=[fc.Internal("foot centre", [fc.P(0.0, 0.0), fc.P(0.0, throat_y)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Wraparound (bottom + sides)",
    )


def build():
    pattern = fc.PatternSet("moccasin-upper")
    everything = target_piece == "set"
    plug = build_plug()
    # the plug's two side sew edges + front curve are the sewn perimeter.
    plug_sewn = (plug.edge("sew_r").length(0.05) + plug.edge("front").length(0.05)
                 + plug.edge("sew_l").length(0.05))
    wrap = build_wrap(plug_sewn)
    if everything or target_piece == "plug":
        pattern.add(plug)
    if everything or target_piece == "wrap":
        pattern.add(wrap)

    if everything or target_piece == "set":
        # the plug's three sewn sides fill the wrap's U-throat (two sew edges).
        pattern.declare_seam(
            [("plug", "sew_r"), ("plug", "front"), ("plug", "sew_l")],
            [("wrap", "sew_r"), ("wrap", "sew_l")], tol=3.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "deerskin / soft moccasin leather",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ area proxy at 1400 mm, 55% marker. A soft, pliable leather gathers at "
                 "the toe. Per PAIR, double this."},
        {"item": "waxed sinew / hand-sewing thread", "qty": 1, "unit": "spool",
         "note": "the plug is whip-stitched to the gathered throat by hand."},
        {"item": "optional soft insole", "qty": 1, "unit": "pair",
         "note": "the wrap is the sole; a thin insole adds comfort."},
    ]
    pattern.metadata = {
        "fc400_rank": 362, "family": "footwear_soft", "lane": 6,
        "fabric_hint": "leather-deerskin",
        "silhouette_note": "A true plug-construction moccasin: a wraparound that is the "
            "bottom and sides, gathered at the toe, with a raised apron plug whip-stitched "
            "into the U-throat. No separate sole.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — ISO 8559 "
            "declares no foot landmark codes, so none is claimed and none is invented.",
        "solved": {
            "wrap_length_mm": round(WRAP_LEN, 1),
            "plug_sewn_perimeter_mm": round(plug_sewn, 1),
            "half_width_mm": round(HALF_W, 1),
            "plug_width_mm": round(PLUG_W, 1),
            "note": "the plug's three sewn sides sum to the wrap's U-throat length exactly; "
                    "the plug width is clamped below the wrap half so the throat never "
                    "inverts",
        },
        "hardware": "none — a hand-sewn moccasin is whip-stitched, no hardware",
    }
    return pattern


result = build()

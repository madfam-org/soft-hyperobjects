"""
Wireless Bra (soft bralette) — FC-100 rank #11. Fashion Cabinet Garment Cartridge.

A wire-free bra that shapes with SEAMS + STRETCH, never boning. Support comes
first from the UNDERBAND: a gripping band whose finished length is the underbust
girth times a negative-ease ratio — the band tensions around the ribcage and
carries the load. The bust is shaped by a curved vertical CUP SEAM joining an
inner and an outer cup half: two curved edges sewn together cone the flat cloth
into projection the way a dart would, so no wire is needed. Back wings wrap to a
center-back HOOK-AND-EYE closure (hardware, referenced not modelled), and two
adjustable STRAPS run from cup to back over sliders and rings.

Every mated edge is built to a shared target length so all structural seams
balance by construction (delta ≈ 0). Neckline, armhole and the band's lower edge
are elastic-finished (allowance 0, marked elastic zones) and the BOM emits
exact-mm elastic cut lengths from the measured openings — the numbers factories
keep on private spec sheets.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # a piece name, or "set"

underbust_girth   = float(PARAM(lambda: underbust_girth, 760.0))   # ribcage under the bust
bust_girth        = float(PARAM(lambda: bust_girth, 940.0))        # full bust girth
cup_depth         = float(PARAM(lambda: cup_depth, 150.0))         # apex projection / cup height
band_height       = float(PARAM(lambda: band_height, 42.0))        # finished underband height
strap_length      = float(PARAM(lambda: strap_length, 340.0))     # cup-over-shoulder-to-back span
strap_width       = float(PARAM(lambda: strap_width, 16.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 18.0))  # band grip (bras run high)
cup_frac          = float(PARAM(lambda: cup_frac, 0.56))           # cup share of each band half
band_elastic_ratio = float(PARAM(lambda: band_elastic_ratio, 0.92))  # band elastic / opening
edge_elastic_ratio = float(PARAM(lambda: edge_elastic_ratio, 0.85))  # neck/arm elastic / opening
seam_allowance    = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth = max(640.0, min(bust_girth, 1500.0))
cup_depth = max(90.0, min(cup_depth, 260.0))
band_height = max(25.0, min(band_height, 90.0))
strap_length = max(220.0, min(strap_length, 460.0))
strap_width = max(8.0, min(strap_width, 40.0))
negative_ease_pct = max(10.0, min(negative_ease_pct, 25.0))
cup_frac = max(0.45, min(cup_frac, 0.70))
band_elastic_ratio = max(0.80, min(band_elastic_ratio, 1.0))
edge_elastic_ratio = max(0.75, min(edge_elastic_ratio, 1.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# ── Derived support geometry (the load path) ─────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_FINISHED = underbust_girth * NEG        # gripping band, full ring (opens at CB hook)
BAND_HALF = BAND_FINISHED / 2.0              # one band piece: CF -> CB (cut 2, mirror)
CUP_SPAN = BAND_HALF * cup_frac              # band top length under one cup
BACK_SPAN = BAND_HALF - CUP_SPAN             # band top length across one back wing
BH = band_height
# Bust surplus over the band drives how deep/wide the cup must be.
BUST_SURPLUS = max(20.0, (bust_girth * NEG - underbust_girth * NEG) / 2.0)  # per side
CD = cup_depth
ELASTIC_ZONE = 8.0                           # marked elastic application width (mm)


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic edge, ELASTIC_ZONE mm inside.

    Pieces are authored CCW, so the inward normal at tangent t is (-t.y, t.x).
    The [t0, t1] window keeps the trace off the corners.
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


# ── The shaped cup seam (shared curve = matched by construction) ─────────────
# A single curved profile, used as the mating seam on BOTH cup halves. Because
# the identical curve is reused, cup_inner.cup_seam and cup_outer.cup_seam are
# equal in length to the micron: delta = 0. Its bow (BUST_SURPLUS) is what cones
# the flat cloth into bust projection without a wire.
CUP_HALF_BOTTOM = CUP_SPAN / 2.0             # each cup half sits on half the band-cup span
SEAM_BOW = BUST_SURPLUS * 0.5                # lateral bow of the vertical cup seam


def _cup_seam_curve(x0):
    """Vertical shaped seam from bottom (x0, 0) up to the apex neighbourhood.

    Bows outward by SEAM_BOW at mid-height, then returns — this is the wire-free
    shaping. Returned as a single Bezier so both cup halves reuse it verbatim.
    """
    return fc.Bezier(
        fc.P(x0, 0.0),
        fc.P(x0 + SEAM_BOW, CD * 0.42),
        fc.P(x0 + SEAM_BOW * 0.85, CD * 0.82),
        fc.P(x0, CD),
    )


def build_cup_inner():
    """Inner cup half: center-front edge, bottom (to band), shaped cup seam, top neckline."""
    x_seam = CUP_HALF_BOTTOM
    center = fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, CD * 0.96))])
    # Neckline sweeps from CF top out to the top of the cup seam (elastic-finished).
    neckline = fc.Edge(
        "neckline",
        [fc.Bezier(fc.P(0.0, CD * 0.96), fc.P(x_seam * 0.5, CD * 1.02),
                   fc.P(x_seam * 0.9, CD * 0.99), fc.P(x_seam, CD))],
    )
    cup_seam = fc.Edge("cup_seam", [_cup_seam_curve(x_seam).reversed()])
    bottom = fc.Edge("bottom", [fc.Line(fc.P(x_seam, 0.0), fc.P(0.0, 0.0))])
    return fc.Piece(
        "cup_inner",
        [center, neckline, cup_seam, bottom],
        seam_allowance=seam_allowance,
        allowances={"neckline": 0.0},  # elastic-finished neckline
        notches=[fc.Notch("bottom", 0.5, "band match"),
                 fc.Notch("cup_seam", 0.5, "cup seam match")],
        grainline=fc.Grainline(fc.P(x_seam * 0.35, CD * 0.2),
                               fc.P(x_seam * 0.35, CD * 0.75)),
        internals=[_elastic_zone(neckline, "neckline elastic zone", 0.08, 0.92)],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — inner half (cut 2 pairs)",
    )


def build_cup_outer():
    """Outer cup half: shaped cup seam, bottom (to band), armhole side, strap tab, top.

    The strap tab is a short horizontal edge (length = strap_width) at the top-
    outer corner; the armhole side drops from there to the band. Bottom length is
    CUP_HALF_BOTTOM so inner.bottom + outer.bottom = CUP_SPAN = band.top_cup.
    """
    x_seam = CUP_HALF_BOTTOM
    tab_x = x_seam - strap_width              # tab spans [tab_x, x_seam] at the top
    cup_seam = fc.Edge("cup_seam", [_cup_seam_curve(0.0)])
    top = fc.Edge(
        "top",
        [fc.Bezier(fc.P(0.0, CD), fc.P(x_seam * 0.5, CD * 1.0),
                   fc.P(x_seam * 0.75, CD * 0.98), fc.P(tab_x, CD * 0.9))],
    )
    # Short strap tab at the top-outer corner: the strap sews to this edge.
    strap_tab = fc.Edge("strap_tab",
                        [fc.Line(fc.P(tab_x, CD * 0.9), fc.P(x_seam, CD * 0.9))])
    # Armhole/side edge bows out then drops to the band corner (elastic-finished).
    side = fc.Edge(
        "side",
        [fc.Bezier(fc.P(x_seam, CD * 0.9), fc.P(x_seam + CD * 0.16, CD * 0.52),
                   fc.P(x_seam + CD * 0.10, CD * 0.18), fc.P(x_seam, 0.0))],
    )
    bottom = fc.Edge("bottom", [fc.Line(fc.P(x_seam, 0.0), fc.P(0.0, 0.0))])
    return fc.Piece(
        "cup_outer",
        [cup_seam, top, strap_tab, side, bottom],
        seam_allowance=seam_allowance,
        allowances={"side": 0.0},  # elastic-finished armhole edge
        notches=[fc.Notch("bottom", 0.5, "band match"),
                 fc.Notch("cup_seam", 0.5, "cup seam match")],
        grainline=fc.Grainline(fc.P(x_seam * 0.55, CD * 0.2),
                               fc.P(x_seam * 0.55, CD * 0.7)),
        internals=[_elastic_zone(side, "armhole elastic zone", 0.08, 0.92)],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — outer half (cut 2 pairs)",
    )


def build_underband():
    """Gripping band, cut 2 mirror (CF seam -> CB hook). Top has two matched spans.

    top_cup (length CUP_SPAN) sews to the two cup bottoms; top_back (length
    BACK_SPAN) sews to the back wing bottom. The lower edge is elastic-finished.
    """
    # Chain CCW: cf (up) -> top_cup (right) -> top_back (right) -> cb (down) -> lower (left)
    cf = fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))])
    top_cup = fc.Edge("top_cup", [fc.Line(fc.P(0.0, BH), fc.P(CUP_SPAN, BH))])
    top_back = fc.Edge("top_back",
                       [fc.Line(fc.P(CUP_SPAN, BH), fc.P(CUP_SPAN + BACK_SPAN, BH))])
    cb = fc.Edge("center_back",
                 [fc.Line(fc.P(BAND_HALF, BH), fc.P(BAND_HALF, 0.0))])
    lower = fc.Edge("lower", [fc.Line(fc.P(BAND_HALF, 0.0), fc.P(0.0, 0.0))])
    return fc.Piece(
        "underband",
        [cf, top_cup, top_back, cb, lower],
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0},  # elastic-finished band edge
        notches=[fc.Notch("top_cup", 0.5, "cup center match"),
                 fc.Notch("center_back", 0.5, "hook closure position")],
        grainline=fc.Grainline(fc.P(BAND_HALF * 0.5, BH * 0.25),
                               fc.P(BAND_HALF * 0.5, BH * 0.75)),
        internals=[_elastic_zone(lower, "underband elastic zone", 0.04, 0.96)],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Underband (cut 2 pairs, CB hook)",
    )


def build_back(side_len):
    """Back wing: cup side seam, top (elastic wing edge), strap tab, CB hook, bottom.

    `side_len` is the measured cup_outer.side length; the wing's straight side is
    built to exactly that so the side seam balances (delta ≈ 0). Bottom length is
    BACK_SPAN so back.bottom = band.top_back by construction.
    """
    wing_h = side_len                        # straight side == curved cup side length
    x_end = BACK_SPAN
    side = fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, wing_h))])
    strap_tab = fc.Edge("strap_tab",
                        [fc.Line(fc.P(0.0, wing_h), fc.P(strap_width, wing_h))])
    # Top wing edge tapers down toward the back CB (elastic-finished).
    top = fc.Edge(
        "top",
        [fc.Bezier(fc.P(strap_width, wing_h), fc.P(x_end * 0.4, wing_h * 0.68),
                   fc.P(x_end * 0.82, BH + 12.0), fc.P(x_end, BH))],
    )
    cb = fc.Edge("center_back", [fc.Line(fc.P(x_end, BH), fc.P(x_end, 0.0))])
    bottom = fc.Edge("bottom", [fc.Line(fc.P(x_end, 0.0), fc.P(0.0, 0.0))])
    return fc.Piece(
        "back",
        [side, strap_tab, top, cb, bottom],
        seam_allowance=seam_allowance,
        allowances={"top": 0.0},  # elastic-finished wing edge
        notches=[fc.Notch("bottom", 0.5, "band match"),
                 fc.Notch("center_back", 0.5, "hook closure position")],
        grainline=fc.Grainline(fc.P(x_end * 0.5, BH * 0.4), fc.P(x_end * 0.5, wing_h * 0.7)),
        internals=[_elastic_zone(top, "back wing elastic zone", 0.06, 0.94)],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back wing (cut 2 pairs, CB hook)",
    )


def build_strap():
    """Adjustable strap: a narrow rectangle, cut 2. Length is the shoulder span;
    final adjustment is by slider + ring hardware, so both ends are declared as
    hardware spans, not sewn to a fixed edge."""
    length = strap_length
    w = strap_width
    edges = [
        fc.Edge("end_cup", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("outer", [fc.Line(fc.P(0.0, w), fc.P(length, w))]),
        fc.Edge("end_back", [fc.Line(fc.P(length, w), fc.P(length, 0.0))]),
        fc.Edge("inner", [fc.Line(fc.P(length, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap",
        edges,
        seam_allowance=0.0,  # folded/turned strap, or plush elastic cut to width
        notches=[fc.Notch("outer", 0.5, "slider position (adjustable)")],
        grainline=fc.Grainline(fc.P(length * 0.2, w / 2.0), fc.P(length * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Strap (cut 2, adjustable)",
    )


def build():
    pattern = fc.PatternSet("bra-wireless")
    cup_inner = build_cup_inner()
    cup_outer = build_cup_outer()
    underband = build_underband()
    # Back wing side is built to the measured cup side length so the side seam
    # balances by construction across every parameter combination.
    back = build_back(cup_outer.edge("side").length())
    strap = build_strap()
    picked = {
        "cup_inner": cup_inner,
        "cup_outer": cup_outer,
        "underband": underband,
        "back": back,
        "strap": strap,
    }
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # "set"
        for piece in (cup_inner, cup_outer, underband, back, strap):
            pattern.add(piece)
        # Cup seam: the two halves cone the cloth into a wire-free bust shape.
        pattern.declare_seam(("cup_inner", "cup_seam"), ("cup_outer", "cup_seam"),
                             tol=1.0)
        # Cup bottoms sew to the band's front span (inner.bottom + outer.bottom).
        pattern.declare_seam([("cup_inner", "bottom"), ("cup_outer", "bottom")],
                             ("underband", "top_cup"), tol=1.0)
        # Back wing bottom sews to the band's back span.
        pattern.declare_seam(("back", "bottom"), ("underband", "top_back"), tol=1.0)
        # Side seam: cup outer side edge to back side edge (both elastic-finished,
        # joined at the underarm).
        pattern.declare_seam(("cup_outer", "side"), ("back", "side"), tol=1.5)
        # Strap ends to cup + back tabs (widths matched; adjustment is hardware).
        pattern.declare_seam(("strap", "end_cup"), ("cup_outer", "strap_tab"), tol=1.0)
        pattern.declare_seam(("strap", "end_back"), ("back", "strap_tab"), tol=1.0)

    # ── Elastic + hardware accounting (the honest, factory-grade detail) ─────
    band_opening = 2.0 * underband.edge("lower").length()  # full ring, both band halves
    band_elastic = round(band_opening * band_elastic_ratio)
    neck_opening = 2.0 * cup_inner.edge("neckline").length()   # two cups
    neck_elastic = round(neck_opening * edge_elastic_ratio)
    arm_opening = 2.0 * (cup_outer.edge("side").length() + back.edge("top").length())
    arm_elastic = round(arm_opening * edge_elastic_ratio)
    strap_span = round(2.0 * strap.edge("outer").length())     # two straps

    fabric_width = 1600.0  # jersey-algodon card width
    # cut quantities: cups 2 pairs = 4 each, band 2, back 2, straps 2 (fabric or elastic)
    area = (
        cup_inner.area() * 4.0
        + cup_outer.area() * 4.0
        + underband.area() * 2.0
        + back.area() * 2.0
    )
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"cups + band + back at {fabric_width:.0f} mm width, 55% marker "
                 "efficiency; greatest stretch horizontal. Power-mesh lining "
                 "optional under the cups for extra wire-free support (add a "
                 "second cut of cup_inner + cup_outer in mesh)."},
        {"item": "band elastic (plush-back) 30 mm", "qty": band_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm ring x {band_elastic_ratio:.2f}; "
                 "the primary support — join in a ring at the CF, quarter-mark, "
                 "zigzag into the marked underband zone; CB ends finish at the hook."},
        {"item": "neckline/armhole elastic (picot) 8 mm", "qty": neck_elastic + arm_elastic,
         "unit": "mm_length",
         "note": f"neckline {neck_elastic} mm ({neck_opening:.0f} mm x "
                 f"{edge_elastic_ratio:.2f}) + armholes {arm_elastic} mm "
                 f"({arm_opening:.0f} mm x {edge_elastic_ratio:.2f}); apply into the "
                 "marked neckline/armhole zones."},
        {"item": "strap elastic 16 mm", "qty": strap_span, "unit": "mm_length",
         "note": f"two straps x {round(strap.edge('outer').length())} mm; trim to fit "
                 "after fitting — length is set by the slider."},
        {"item": "strap sliders + rings (set of 2 sliders, 2 rings)", "qty": 2,
         "unit": "set",
         "note": "adjustable strap hardware — Yantra4D cartridge reference "
                 "(notion.hardware_ref: yantra4d/strap-slider-ring); not modelled here."},
        {"item": "hook-and-eye bra back (3x2)", "qty": 1, "unit": "piece",
         "note": "center-back closure at the marked CB notch — Yantra4D cartridge "
                 "reference (notion.hardware_ref: yantra4d/hook-and-eye-3x2); "
                 "hardware, not modelled. A pullover (no-hook) variant omits this."},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; zigzag or 3-thread overlock every seam."},
    ]
    pattern.metadata = {
        "fc100_rank": 11,
        "fabric_hint": "jersey-algodon",
        "stretch_note": "cut with greatest stretch horizontal; add power-mesh cup "
                        "lining for firmer wire-free support",
        "support_note": "wire-free: support comes from the negative-ease underband "
                        "and the curved cup seam coning the cloth — NOT from boning",
        "negative_ease_pct": negative_ease_pct,
        "band_finished_mm": round(BAND_FINISHED, 1),
        "band_opening_mm": round(band_opening, 1),
        "band_elastic_mm": band_elastic,
        "cup_span_each_mm": round(CUP_SPAN, 1),
        "back_span_each_mm": round(BACK_SPAN, 1),
        "neck_opening_mm": round(neck_opening, 1),
        "neck_elastic_mm": neck_elastic,
        "arm_opening_mm": round(arm_opening, 1),
        "arm_elastic_mm": arm_elastic,
        "closure": "center-back hook-and-eye (3x2); pullover variant available",
        "drafting": "teaching-grade wireless bralette: curved cup seam for shape, "
                    "gripping underband for support, all structural seams matched by "
                    "construction; elastic cut lengths derived exactly from measured "
                    "openings. Made to measure to underbust + bust girths.",
    }
    return pattern


result = build()

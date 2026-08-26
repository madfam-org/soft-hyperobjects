"""
Balconette Underwire Bra — Fashion Cabinet Garment Cartridge (FC-500 #460; y4d bra-underwire).

A balconette (balcony) bra: a wired cup whose horizontal seam is set LOW and STRAIGHT so the cup
reads as a shelf that lifts from below, with WIDE-SET straps that drop nearly vertically from the
outer cup edge. It is not the same object as the commons' three-piece `underwire-bra` (a full/demi
cup with a diagonal seam and near-centred straps) — the balconette's defining geometry is the low
horizontal cup seam and the wide strap set, and this cartridge draws both as explicit parameters
(`cup_seam_drop`, `strap_set_frac`).

Like every wired bra in the commons it consumes the Yantra4D `bra-underwire` through a SOLVED wire
channel: the cradle's `wire_line` edge is the underwire's own arc, so the sewn channel is exactly
as long as the printed wire.

The DIMENSIONAL HANDSHAKE. `bra-underwire` is parameterised by `cup_width` (the wire chord) and
`sweep_deg` (the arc angle). Both drive the garment's own `wire_line` interface AND the hardware's
`cradle_seam` flange, so:

    cup_width  ->  wire chord AND cradle wire-line chord            (one number)
    sweep_deg  ->  wire arc angle AND cradle curve arc angle
        =>  arc length L = R θ, R = cup_width / (2 sin θ/2)

`_wire_arc_points` builds the cradle wire line as that exact arc; the two cup lower sections'
mouths sum to the same run, so wire, channel and cup mouth are one dimension, checked by
declare_seam.

Made to measure to underbust and bust girths. FC-500 lane 7 (intimates & loungewear III).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

underbust_girth = float(PARAM(lambda: underbust_girth, 760.0))
bust_girth      = float(PARAM(lambda: bust_girth, 940.0))
cup_width       = float(PARAM(lambda: cup_width, 130.0))    # wire chord tip-to-tip
sweep_deg       = float(PARAM(lambda: sweep_deg, 200.0))    # wire arc angle
cup_seam_drop   = float(PARAM(lambda: cup_seam_drop, 0.36)) # low horizontal seam (balconette)
strap_set_frac  = float(PARAM(lambda: strap_set_frac, 0.86))# strap position along cup top (wide)
cradle_height   = float(PARAM(lambda: cradle_height, 24.0))
band_height     = float(PARAM(lambda: band_height, 32.0))
strap_width     = float(PARAM(lambda: strap_width, 16.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 15.0))
seam_allowance  = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth      = max(640.0, min(bust_girth, 1500.0))
cup_width       = max(90.0, min(cup_width, 200.0))
sweep_deg       = max(150.0, min(sweep_deg, 250.0))
cup_seam_drop   = max(0.24, min(cup_seam_drop, 0.50))
strap_set_frac  = max(0.70, min(strap_set_frac, 0.95))
cradle_height   = max(14.0, min(cradle_height, 60.0))
band_height     = max(20.0, min(band_height, 80.0))
strap_width     = max(8.0, min(strap_width, 30.0))
negative_ease_pct = max(8.0, min(negative_ease_pct, 24.0))
seam_allowance  = max(0.0, min(seam_allowance, 12.0))

# ── Support geometry ─────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_FINISHED = underbust_girth * NEG
BAND_HALF = BAND_FINISHED / 2.0
BH = band_height
CH = cradle_height
SURPLUS = max(24.0, (bust_girth - underbust_girth) / 2.0)
APEX = SURPLUS * 0.60
# Balconette: cup rises low; total cup height is modest, seam sits low.
CUP_H = max(50.0, APEX + 34.0)
LOWER_H = max(24.0, CUP_H * cup_seam_drop)     # the low horizontal seam height
UPPER_H = max(20.0, CUP_H - LOWER_H)

# ── The solved wire line ─────────────────────────────────────────────────────
THETA = math.radians(sweep_deg)
WIRE_R = cup_width / (2.0 * math.sin(THETA / 2.0))
WIRE_RUN = WIRE_R * THETA
WIRE_RISE = WIRE_R * (1.0 - math.cos(THETA / 2.0))


def _wire_arc_points(x0, y0, samples=81):
    cx = x0 + cup_width / 2.0
    cy = y0 - WIRE_RISE + WIRE_R
    a0 = -math.pi / 2.0 - THETA / 2.0
    pts = []
    for i in range(samples):
        a = a0 + THETA * i / (samples - 1)
        pts.append(fc.P(cx + WIRE_R * math.cos(a), cy + WIRE_R * math.sin(a)))
    return pts


def _arc_split(frac):
    pts = _wire_arc_points(0.0, 0.0, samples=81)
    n = len(pts)
    k = max(1, min(n - 2, int(round(frac * (n - 1)))))
    return pts[: k + 1], pts[k:]


APEX_FRAC = 0.47


def build_cup_lower_inner():
    """Lower inner cup section: CF edge, low horizontal seam, apex seam, mouth arc."""
    first, _ = _arc_split(APEX_FRAC)
    cf_pt = first[0]
    apex_pt = first[-1]
    rev = list(reversed(first))                # mouth apex -> CF
    cf_top = fc.P(cf_pt.x, cf_pt.y + LOWER_H * 0.42)
    apex_top = fc.P(apex_pt.x, apex_pt.y + LOWER_H)
    edges = [
        fc.Edge("center_front", [fc.Line(cf_pt, cf_top)]),
        fc.Edge("upper_seam", [fc.Bezier(cf_top,
                                         fc.P(cf_top.x + (apex_pt.x - cf_top.x) * 0.45,
                                              cf_top.y + LOWER_H * 0.30),
                                         fc.P(cf_top.x + (apex_pt.x - cf_top.x) * 0.82,
                                              apex_top.y - LOWER_H * 0.06),
                                         apex_top)]),
        fc.Edge("apex_seam", [fc.Line(apex_top, apex_pt)]),
        fc.Edge("mouth", [fc.Line(rev[i], rev[i + 1]) for i in range(len(rev) - 1)]),
    ]
    return fc.Piece(
        "cup_lower_inner", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("mouth", 0.5, "cradle match"),
                 fc.Notch("apex_seam", 0.5, "apex match")],
        grainline=fc.Grainline(fc.P(apex_pt.x * 0.5, apex_pt.y + LOWER_H * 0.25),
                               fc.P(apex_pt.x * 0.5, apex_pt.y + LOWER_H * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — lower inner (cut 2 pairs)",
    )


def build_cup_lower_outer():
    """Lower outer cup section: apex seam, low horizontal seam, side rise, mouth arc."""
    _, second = _arc_split(APEX_FRAC)
    apex_pt = second[0]
    tip_pt = second[-1]
    rev = list(reversed(second))               # mouth outer tip -> apex
    apex_top = fc.P(apex_pt.x, apex_pt.y + LOWER_H)
    side_top = fc.P(tip_pt.x, tip_pt.y + LOWER_H * 0.55)
    edges = [
        fc.Edge("apex_seam", [fc.Line(apex_pt, apex_top)]),
        fc.Edge("upper_seam", [fc.Bezier(apex_top,
                                         fc.P(apex_top.x + (side_top.x - apex_top.x) * 0.32,
                                              apex_top.y - LOWER_H * 0.04),
                                         fc.P(apex_top.x + (side_top.x - apex_top.x) * 0.74,
                                              side_top.y + LOWER_H * 0.14),
                                         side_top)]),
        fc.Edge("side", [fc.Line(side_top, tip_pt)]),
        fc.Edge("mouth", [fc.Line(rev[i], rev[i + 1]) for i in range(len(rev) - 1)]),
    ]
    return fc.Piece(
        "cup_lower_outer", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("mouth", 0.5, "cradle match"),
                 fc.Notch("apex_seam", 0.5, "apex match")],
        grainline=fc.Grainline(fc.P((apex_pt.x + tip_pt.x) * 0.5, apex_pt.y + LOWER_H * 0.25),
                               fc.P((apex_pt.x + tip_pt.x) * 0.5, apex_pt.y + LOWER_H * 0.68)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — lower outer (cut 2 pairs)",
    )


def build_cup_upper(lower_inner, lower_outer):
    """The balconette upper band: a shallow STRAIGHT-ish top over the low seam, with the
    strap tab set WIDE (strap_set_frac along the top). Its lower edge is built to the
    measured combined upper_seam run of the lower sections."""
    run = (lower_inner.edge("upper_seam").length()
           + lower_outer.edge("upper_seam").length())
    # A shallow circular arc of length `run`.
    bow = 0.10
    phi = 1.0
    for _ in range(48):
        s_over_run = (1.0 - math.cos(phi / 2.0)) / phi
        phi *= (bow / s_over_run) ** 0.5 if s_over_run > 1e-9 else 1.0
        phi = max(0.05, min(phi, math.pi))
    r = run / phi
    n = 33
    pts = []
    for i in range(n):
        a = -math.pi / 2.0 - phi / 2.0 + phi * i / (n - 1)
        pts.append(fc.P(r * math.cos(a), r * math.sin(a) + r))
    dx, dy = pts[0].x, pts[0].y
    pts = [fc.P(p.x - dx, p.y - dy) for p in pts]
    left, right = pts[0], pts[-1]
    span = right.x - left.x
    # The outer `side` edge rises the full UPPER_H to the strap tab (like the commons
    # underwire cup), so it sums with the lower-outer side into the wing side seam. The
    # balconette WIDTH comes from where the strap tab sits and how far the neckline is cut
    # in: strap_set_frac places the tab's inner point wide (near the outer edge), and the
    # neckline sweeps low and shallow from there to the centre.
    top_r = fc.P(right.x - strap_width, right.y + UPPER_H)   # strap tab outer
    tab_r = fc.P(right.x, right.y + UPPER_H)                 # strap tab inner corner at side top
    top_l = fc.P(left.x, left.y + UPPER_H * 0.44)
    strap_in = fc.P(left.x + span * strap_set_frac, top_r.y - UPPER_H * 0.04)
    edges = [
        fc.Edge("cup_seam", [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]),
        fc.Edge("side", [fc.Line(right, tab_r)]),
        fc.Edge("strap_tab", [fc.Line(tab_r, top_r)]),
        fc.Edge("neckline", [fc.Bezier(top_r,
                                       fc.P(strap_in.x, strap_in.y),
                                       fc.P(top_l.x + span * 0.18, top_l.y + UPPER_H * 0.16),
                                       top_l)]),
        fc.Edge("center_front", [fc.Line(top_l, left)]),
    ]
    piece = fc.Piece(
        "cup_upper", edges, seam_allowance=seam_allowance,
        allowances={"neckline": 0.0},
        notches=[fc.Notch("cup_seam", APEX_FRAC, "apex match")],
        grainline=fc.Grainline(fc.P(right.x * 0.45, UPPER_H * 0.15),
                               fc.P(right.x * 0.45, UPPER_H * 0.70)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — balconette upper band (cut 2 pairs)",
    )
    return piece


def build_cradle():
    arc = _wire_arc_points(0.0, CH, samples=81)
    left, right = arc[0], arc[-1]
    bottom = fc.Edge("bottom", [fc.Line(fc.P(right.x, 0.0), fc.P(left.x, 0.0))])
    cf = fc.Edge("center_front", [fc.Line(fc.P(left.x, 0.0), left)])
    wire_line = fc.Edge("wire_line",
                        [fc.Line(arc[i], arc[i + 1]) for i in range(len(arc) - 1)])
    side = fc.Edge("side", [fc.Line(right, fc.P(right.x, 0.0))])
    channel = fc.Internal("wire channel (stitch line)",
                          [fc.P(p.x, p.y - 5.0) for p in arc[::4]], kind="marking")
    return fc.Piece(
        "cradle", [bottom, cf, wire_line, side], seam_allowance=seam_allowance,
        notches=[fc.Notch("wire_line", APEX_FRAC, "apex position"),
                 fc.Notch("bottom", 0.5, "band match")],
        grainline=fc.Grainline(fc.P(cup_width * 0.5, 4.0), fc.P(cup_width * 0.5, CH * 0.9)),
        internals=[channel], cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cradle — wire channel frame (cut 2 pairs)",
    )


def _rect(x0, y0, w, h, names):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(x0, y0), fc.P(x0 + w, y0), fc.P(x0 + w, y0 + h), fc.P(x0, y0 + h)
    return [fc.Edge(names[0], [fc.Line(p0, p1)]), fc.Edge(names[1], [fc.Line(p1, p2)]),
            fc.Edge(names[2], [fc.Line(p2, p3)]), fc.Edge(names[3], [fc.Line(p3, p0)])]


def build_band(cradle_bottom_len):
    front = cradle_bottom_len
    back = max(40.0, BAND_HALF - front)
    total = front + back
    edges = _rect(0.0, 0.0, total, BH, ("lower", "center_back", "top", "center_front"))
    piece = fc.Piece(
        "band", edges, seam_allowance=seam_allowance,
        allowances={"lower": 0.0},
        notches=[fc.Notch("top", front / total, "cradle edge"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P(total * 0.5, BH * 0.25), fc.P(total * 0.5, BH * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Underband (cut 2 pairs, CB hook)",
    )
    return piece


def build_back(side_len, back_span):
    # wing side is built to EXACTLY the cup's measured side run so the side seam balances;
    # side_len is always > 0 (two positive rises), no clamp that would break the seam.
    wing_h = side_len
    x_end = max(back_span, 60.0)
    side = fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, wing_h))])
    strap_tab = fc.Edge("strap_tab", [fc.Line(fc.P(0.0, wing_h), fc.P(strap_width, wing_h))])
    top = fc.Edge("top", [fc.Bezier(fc.P(strap_width, wing_h),
                                    fc.P(x_end * 0.42, wing_h * 0.68),
                                    fc.P(x_end * 0.84, BH + 8.0),
                                    fc.P(x_end, BH))])
    cb = fc.Edge("center_back", [fc.Line(fc.P(x_end, BH), fc.P(x_end, 0.0))])
    bottom = fc.Edge("bottom", [fc.Line(fc.P(x_end, 0.0), fc.P(0.0, 0.0))])
    piece = fc.Piece(
        "back", [side, strap_tab, top, cb, bottom], seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("bottom", 0.5, "band match"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P(x_end * 0.5, BH * 0.4), fc.P(x_end * 0.5, wing_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back wing (cut 2 pairs, CB hook)",
    )
    return piece


def build():
    pattern = fc.PatternSet("balconette-underwire-bra")
    lower_inner = build_cup_lower_inner()
    lower_outer = build_cup_lower_outer()
    upper = build_cup_upper(lower_inner, lower_outer)
    cradle = build_cradle()
    band = build_band(cradle.edge("bottom").length())
    back_span = max(40.0, BAND_HALF - cradle.edge("bottom").length())
    back = build_back(lower_outer.edge("side").length() + upper.edge("side").length(), back_span)

    picked = {"cup_lower_inner": lower_inner, "cup_lower_outer": lower_outer,
              "cup_upper": upper, "cradle": cradle, "band": band, "back": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (lower_inner, lower_outer, upper, cradle, band, back):
            pattern.add(piece)
        pattern.declare_seam(("cup_lower_inner", "apex_seam"),
                             ("cup_lower_outer", "apex_seam"), tol=1.0)
        # THE HANDSHAKE SEAM: both cup mouths = cradle wire line = solved arc = printed wire.
        pattern.declare_seam([("cup_lower_inner", "mouth"), ("cup_lower_outer", "mouth")],
                             ("cradle", "wire_line"), tol=1.0)
        # The low horizontal balconette cup seam.
        pattern.declare_seam(("cup_upper", "cup_seam"),
                             [("cup_lower_inner", "upper_seam"),
                              ("cup_lower_outer", "upper_seam")], tol=1.0)
        # Cradle front + back wing seat on the band's whole top edge.
        pattern.declare_seam([("cradle", "bottom"), ("back", "bottom")],
                             ("band", "top"), tol=1.5)
        # Side seam: cup outer rise + upper side joins the wing side.
        pattern.declare_seam([("cup_lower_outer", "side"), ("cup_upper", "side")],
                             ("back", "side"), tol=1.5)

    band_opening = 2.0 * band.edge("lower").length()
    neck_opening = 2.0 * upper.edge("neckline").length()
    arm_opening = 2.0 * back.edge("top").length()
    channel_run = 2.0 * cradle.edge("wire_line").length()

    fabric_width = 1500.0
    area = (lower_inner.area() * 4.0 + lower_outer.area() * 4.0 + upper.area() * 4.0
            + cradle.area() * 2.0 + band.area() * 2.0 + back.area() * 2.0)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "stable bra tricot / duoplex", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"cups + cradle + band + wings at {fabric_width:.0f} mm width, 55% marker. "
                 "The balconette upper band is cut on the stable grain so the low seam holds "
                 "its straight line."},
        {"item": "underwire (Yantra4D bra-underwire)", "qty": 2, "unit": "piece",
         "note": f"one pair; chord (cup_width) {cup_width:.0f} mm, sweep {sweep_deg:.0f}°, "
                 f"solved arc run {WIRE_RUN:.1f} mm each. The wire is the Yantra4D solid "
                 "(notion.hardware_ref -> bra-underwire); this cartridge draws the channel."},
        {"item": "wire channel tape 12 mm", "qty": round(channel_run * 1.06),
         "unit": "mm_length",
         "note": f"two channels x {WIRE_RUN:.1f} mm solved run + 6% turn-under; close both "
                 "ends so the wire tips cannot work through."},
        {"item": "band elastic (plush-back) 12 mm", "qty": round(band_opening * 0.92),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm opening x 0.92 — cut short, stretched on."},
        {"item": "neckline + armhole elastic (picot) 8 mm",
         "qty": round((neck_opening + arm_opening) * 0.85), "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} mm + wing top {arm_opening:.0f} mm at 0.85."},
        {"item": "strap elastic + sliders/rings", "qty": 2, "unit": "set",
         "note": "wide-set adjustable straps — the ring/slider hardware is Yantra4D "
                 "bra-ring-slider, not modelled here."},
        {"item": "hook-and-eye bra back (3x2)", "qty": 1, "unit": "piece",
         "note": "centre-back closure at the marked CB notch — Yantra4D hook-and-eye."},
        {"item": "polyester thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "the low horizontal seam is topstitched flat so it does not print through."},
    ]
    pattern.metadata = {
        "fc500_rank": 460, "family": "underwear_lounge", "fabric_hint": "encaje-elastico",
        "silhouette_note": "Balconette: a wired cup with a LOW STRAIGHT horizontal seam that "
            "lifts from below, and WIDE-SET straps that drop near-vertically from the outer "
            "cup edge. cup_seam_drop places the seam low; strap_set_frac sets the straps wide.",
        "hardware": "underwire via Yantra4D (notion.hardware_ref -> bra-underwire); cup_width "
            "drives both wire chord and cradle wire-line chord, sweep_deg both arc angles.",
        "solver": {
            "wire_chord_mm": round(cup_width, 1),
            "wire_sweep_deg": round(sweep_deg, 1),
            "wire_radius_mm": round(WIRE_R, 2),
            "wire_run_mm": round(WIRE_RUN, 2),
            "cradle_wire_line_mm": round(cradle.edge("wire_line").length(), 2),
            "cup_mouth_total_mm": round(lower_inner.edge("mouth").length()
                                        + lower_outer.edge("mouth").length(), 2),
            "note": "wire_run == cradle_wire_line == cup_mouth_total.",
        },
        "solved": {
            "band_finished_mm": round(BAND_FINISHED, 1),
            "bust_surplus_mm": round(SURPLUS, 1),
            "cup_height_mm": round(CUP_H, 1),
            "low_seam_height_mm": round(LOWER_H, 1),
            "strap_set_frac": round(strap_set_frac, 3),
            "band_opening_mm": round(band_opening, 1),
        },
        "closure": "centre-back hook-and-eye (3x2)",
        "drafting": "Made to measure to underbust and bust; wire solved to cup_width + sweep_deg.",
    }
    return pattern


result = build()

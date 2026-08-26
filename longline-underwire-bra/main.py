"""
Longline underwire bra — Fashion Cabinet Garment Cartridge (FC-400 #381; y4d bra-underwire).

The lane anchor and a deepening of the FC-300 underwire-bra (#219): the SAME three-piece
wired cup and the SAME dimensional handshake with the printed `bra-underwire`, extended
DOWN into a longline band that reaches to the waist. A longline bra is not a bra with a
wider band bolted on — the long band is a structural member that takes support off the
shoulders and holds the ribcage, and its own negative ease and vertical boning channels
are what make it work. This cartridge draws all of it honestly.

THE CUP AND THE WIRE HANDSHAKE (inherited, unchanged in principle). A moulded-looking cup
out of stable cloth needs two cones at right angles: a vertical apex seam between two lower
sections and a horizontal seam under an upper section. The cradle's upper edge is the WIRE
LINE, SOLVED to the underwire's own arc — `cup_width` sets the wire's chord AND the
channel's chord, `sweep_deg` sets both arc angles, so the drafted channel run and the
printed wire agree by construction (arc length L = R·θ, R = chord / (2 sin(θ/2))). The
manifest's `params_map` sends `cup_width` and `sweep_deg` to `bra-underwire`, and both
also drive the garment's own wire_line interface — a coupled handshake, not a name that
happens to resolve.

WHAT MAKES IT LONGLINE (the new depth). Below the cradle the band runs to the natural
waist, cut at the underbust girth's negative ease at the top and easing to the waist girth
below. It carries VERTICAL BONING CHANNELS at the side and centre front — the boning is a
`bra-underwire`-family stiffener the wearer supplies as tape or spiral steel; this
cartridge draws the channels, spaced from the band width, and reports their count and run.
The long band is what lets a longline bra support a larger cup without the straps digging,
because the ribcage grip carries the load a short band cannot.

Made to measure to underbust, bust and waist girths. FC-400 lane 9 (structured intimates).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

underbust_girth = float(PARAM(lambda: underbust_girth, 760.0))
bust_girth = float(PARAM(lambda: bust_girth, 940.0))
waist_girth = float(PARAM(lambda: waist_girth, 700.0))
cup_width = float(PARAM(lambda: cup_width, 130.0))     # wire chord, tip to tip
sweep_deg = float(PARAM(lambda: sweep_deg, 210.0))     # wire arc angle
cradle_height = float(PARAM(lambda: cradle_height, 26.0))
longline_drop = float(PARAM(lambda: longline_drop, 150.0))   # cradle base -> waist
strap_width = float(PARAM(lambda: strap_width, 16.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 14.0))
upper_cup_frac = float(PARAM(lambda: upper_cup_frac, 0.44))
bone_count = float(PARAM(lambda: bone_count, 3.0))     # boning channels per half band
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth = max(640.0, min(bust_girth, 1500.0))
waist_girth = max(500.0, min(waist_girth, 1300.0))
cup_width = max(90.0, min(cup_width, 200.0))
sweep_deg = max(150.0, min(sweep_deg, 260.0))
cradle_height = max(14.0, min(cradle_height, 60.0))
longline_drop = max(60.0, min(longline_drop, 280.0))
strap_width = max(8.0, min(strap_width, 30.0))
negative_ease_pct = max(8.0, min(negative_ease_pct, 24.0))
upper_cup_frac = max(0.30, min(upper_cup_frac, 0.60))
bone_count = max(1.0, min(round(bone_count), 6.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# ── Support geometry ─────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_TOP_FIN = underbust_girth * NEG
BAND_BOT_FIN = waist_girth * NEG
BAND_TOP_HALF = BAND_TOP_FIN / 2.0
BAND_BOT_HALF = BAND_BOT_FIN / 2.0
CH = cradle_height
SURPLUS = max(24.0, (bust_girth - underbust_girth) / 2.0)
APEX = SURPLUS * 0.62
ELASTIC_ZONE = 8.0

# ── THE SOLVER: the wire line ────────────────────────────────────────────────
THETA = math.radians(sweep_deg)
WIRE_R = cup_width / (2.0 * math.sin(THETA / 2.0))
WIRE_RUN = WIRE_R * THETA
WIRE_RISE = WIRE_R * (1.0 - math.cos(THETA / 2.0))


def _wire_arc_points(x0, y0, samples=41):
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


def _elastic_zone(edge, label, t0, t1, samples=13):
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


APEX_FRAC = 0.46
LOWER_H = APEX * (1.0 - upper_cup_frac) + APEX * 0.55
UPPER_H = APEX * upper_cup_frac + 10.0


def _apex_seam(x_at_mouth, y_at_mouth, height):
    return fc.Bezier(
        fc.P(x_at_mouth, y_at_mouth),
        fc.P(x_at_mouth + SURPLUS * 0.10, y_at_mouth + height * 0.40),
        fc.P(x_at_mouth + SURPLUS * 0.06, y_at_mouth + height * 0.78),
        fc.P(x_at_mouth, y_at_mouth + height),
    )


def build_cup_lower_inner():
    first, _ = _arc_split(APEX_FRAC)
    cf_pt = first[0]
    apex_pt = first[-1]
    top_of_seam = fc.P(apex_pt.x, apex_pt.y + LOWER_H)
    cf_top = fc.P(cf_pt.x, cf_pt.y + LOWER_H * 0.30)
    rev = list(reversed(first))
    edges = [
        fc.Edge("center_front", [fc.Line(cf_pt, cf_top)]),
        fc.Edge("upper_seam", [fc.Bezier(cf_top,
                                         fc.P(cf_top.x + (apex_pt.x - cf_top.x) * 0.45,
                                              cf_top.y + LOWER_H * 0.42),
                                         fc.P(cf_top.x + (apex_pt.x - cf_top.x) * 0.80,
                                              top_of_seam.y - LOWER_H * 0.10),
                                         top_of_seam)]),
        fc.Edge("apex_seam", [_apex_seam(apex_pt.x, apex_pt.y, LOWER_H).reversed()]),
        fc.Edge("mouth", [fc.Line(rev[i], rev[i + 1]) for i in range(len(rev) - 1)]),
    ]
    return fc.Piece(
        "cup_lower_inner", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("mouth", 0.5, "cradle match"),
                 fc.Notch("apex_seam", 0.5, "apex seam match")],
        grainline=fc.Grainline(fc.P(apex_pt.x * 0.5, apex_pt.y + LOWER_H * 0.25),
                               fc.P(apex_pt.x * 0.5, apex_pt.y + LOWER_H * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — lower inner section (cut 2 pairs)")


def build_cup_lower_outer():
    _, second = _arc_split(APEX_FRAC)
    apex_pt = second[0]
    tip_pt = second[-1]
    rev = list(reversed(second))
    top_of_seam = fc.P(apex_pt.x, apex_pt.y + LOWER_H)
    side_top = fc.P(tip_pt.x, tip_pt.y + LOWER_H * 0.42)
    edges = [
        fc.Edge("apex_seam", [_apex_seam(apex_pt.x, apex_pt.y, LOWER_H)]),
        fc.Edge("upper_seam", [fc.Bezier(top_of_seam,
                                         fc.P(top_of_seam.x + (side_top.x - top_of_seam.x) * 0.30,
                                              top_of_seam.y - LOWER_H * 0.06),
                                         fc.P(top_of_seam.x + (side_top.x - top_of_seam.x) * 0.72,
                                              side_top.y + LOWER_H * 0.18),
                                         side_top)]),
        fc.Edge("side", [fc.Line(side_top, tip_pt)]),
        fc.Edge("mouth", [fc.Line(rev[i], rev[i + 1]) for i in range(len(rev) - 1)]),
    ]
    return fc.Piece(
        "cup_lower_outer", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("mouth", 0.5, "cradle match"),
                 fc.Notch("apex_seam", 0.5, "apex seam match")],
        grainline=fc.Grainline(fc.P((apex_pt.x + tip_pt.x) * 0.5, apex_pt.y + LOWER_H * 0.25),
                               fc.P((apex_pt.x + tip_pt.x) * 0.5, apex_pt.y + LOWER_H * 0.70)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — lower outer section (cut 2 pairs)")


def build_cup_upper(lower_inner, lower_outer):
    run = (lower_inner.edge("upper_seam").length()
           + lower_outer.edge("upper_seam").length())
    bow_frac = 0.16
    phi = 1.0
    for _ in range(48):
        s_over_run = (1.0 - math.cos(phi / 2.0)) / phi
        phi *= (bow_frac / s_over_run) ** 0.5 if s_over_run > 1e-9 else 1.0
        phi = max(0.05, min(phi, math.pi))
    r = run / phi
    pts = []
    n = 33
    for i in range(n):
        a = -math.pi / 2.0 - phi / 2.0 + phi * i / (n - 1)
        pts.append(fc.P(r * math.cos(a), r * math.sin(a) + r))
    dx, dy = pts[0].x, pts[0].y
    pts = [fc.P(p.x - dx, p.y - dy) for p in pts]
    left, right = pts[0], pts[-1]
    top_l = fc.P(left.x, left.y + UPPER_H * 0.55)
    top_r = fc.P(right.x - strap_width, right.y + UPPER_H)
    tab_r = fc.P(right.x, right.y + UPPER_H)
    edges = [
        fc.Edge("cup_seam", [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]),
        fc.Edge("side", [fc.Line(right, tab_r)]),
        fc.Edge("strap_tab", [fc.Line(tab_r, top_r)]),
        fc.Edge("neckline", [fc.Bezier(top_r,
                                       fc.P(top_r.x * 0.62, top_r.y - UPPER_H * 0.18),
                                       fc.P(top_r.x * 0.26, top_l.y + UPPER_H * 0.14),
                                       top_l)]),
        fc.Edge("center_front", [fc.Line(top_l, left)]),
    ]
    piece = fc.Piece(
        "cup_upper", edges, seam_allowance=seam_allowance,
        allowances={"neckline": 0.0},
        notches=[fc.Notch("cup_seam", APEX_FRAC, "apex seam match")],
        grainline=fc.Grainline(fc.P(right.x * 0.45, UPPER_H * 0.15),
                               fc.P(right.x * 0.45, UPPER_H * 0.72)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — upper section (cut 2 pairs)")
    piece.internals = [_elastic_zone(piece.edge("neckline"), "neckline elastic zone", 0.08, 0.92)]
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
        label="Cradle — wire channel frame (cut 2 pairs)")


def build_longline_band(cradle_bottom_len):
    """The longline band, cut 2 mirror (CF -> CB hook), reaching to the waist.

    Its TOP edge is built to the measured cradle bottom (front span) plus a back wing span
    at the underbust ring; its LOWER edge is the waist ring, cut narrower (the band tapers
    to the waist). Vertical boning channels are marked at the side and centre-front, spaced
    from the band width. This long band is the longline structure — it holds the ribcage
    and takes support off the shoulders.
    """
    front = cradle_bottom_len
    back = max(40.0, BAND_TOP_HALF - front)
    top_w = front + back                          # underbust-ring half at the top
    # lower waist ring half, tapered in from the top by the waist:underbust ratio
    bot_w = top_w * (BAND_BOT_HALF / max(BAND_TOP_HALF, 1.0))
    dx = (top_w - bot_w) / 2.0                     # taper inset per side
    depth = CH * 0.0 + longline_drop               # band depth = longline drop
    # CCW: CF (up the front) -> top (CF->CB) -> CB (down) -> lower (CB->CF, tapered)
    cf = fc.Edge("center_front", [fc.Line(fc.P(dx, 0.0), fc.P(0.0, depth))])
    top = fc.Edge("top", [fc.Line(fc.P(0.0, depth), fc.P(top_w, depth))])
    cb = fc.Edge("center_back", [fc.Line(fc.P(top_w, depth), fc.P(top_w - dx, 0.0))])
    lower = fc.Edge("lower", [fc.Line(fc.P(top_w - dx, 0.0), fc.P(dx, 0.0))])
    # boning channels: evenly spaced verticals across the band half
    n = int(bone_count)
    channels = []
    for i in range(n):
        frac = (i + 1) / (n + 1)
        x = dx + (top_w - 2 * dx) * frac
        channels.append(fc.Internal(f"boning channel {i + 1}",
                                    [fc.P(x, depth * 0.06), fc.P(x, depth * 0.94)],
                                    kind="marking"))
    piece = fc.Piece(
        "longline_band", [cf, top, cb, lower], seam_allowance=seam_allowance,
        allowances={"lower": 0.0},                # elastic-finished waist edge
        notches=[fc.Notch("top", 0.5, "cradle/back junction"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P(top_w * 0.5, depth * 0.15),
                               fc.P(top_w * 0.5, depth * 0.85)),
        internals=channels, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Longline band to the waist (cut 2 pairs, CB hook)")
    piece.internals = channels + [_elastic_zone(piece.edge("lower"),
                                                 "waist elastic zone", 0.04, 0.96)]
    return piece


def build_back(side_len, back_span):
    """Back wing: side seam (built to the cup's measured side rise), strap tab, CB hook.

    On a longline the wing is joined to the top of the longline band; its bottom sews to
    the band's top back span.
    """
    wing_h = side_len
    x_end = back_span
    side = fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, wing_h))])
    strap_tab = fc.Edge("strap_tab", [fc.Line(fc.P(0.0, wing_h), fc.P(strap_width, wing_h))])
    # The wing top sweeps down to a short vertical centre-back edge that carries the
    # top of the long hook column (the band carries the rest of it below).
    cb_h = wing_h * 0.35
    top = fc.Edge("top", [fc.Bezier(fc.P(strap_width, wing_h),
                                    fc.P(x_end * 0.42, wing_h * 0.70),
                                    fc.P(x_end * 0.84, cb_h + 10.0),
                                    fc.P(x_end, cb_h))])
    cb = fc.Edge("center_back", [fc.Line(fc.P(x_end, cb_h), fc.P(x_end, 0.0))])
    bottom = fc.Edge("bottom", [fc.Line(fc.P(x_end, 0.0), fc.P(0.0, 0.0))])
    piece = fc.Piece(
        "back", [side, strap_tab, top, cb, bottom], seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("bottom", 0.5, "band match"),
                 fc.Notch("center_back", 0.5, "hook column top")],
        grainline=fc.Grainline(fc.P(x_end * 0.5, wing_h * 0.2), fc.P(x_end * 0.5, wing_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back wing (cut 2 pairs, joins longline band)")
    piece.internals = [_elastic_zone(piece.edge("top"), "wing elastic zone", 0.06, 0.94)]
    return piece


def build():
    pattern = fc.PatternSet("longline-underwire-bra")
    lower_inner = build_cup_lower_inner()
    lower_outer = build_cup_lower_outer()
    upper = build_cup_upper(lower_inner, lower_outer)
    cradle = build_cradle()
    band = build_longline_band(cradle.edge("bottom").length())
    back_span = max(40.0, BAND_TOP_HALF - cradle.edge("bottom").length())
    back = build_back(lower_outer.edge("side").length() + upper.edge("side").length(),
                      back_span)

    picked = {"cup_lower_inner": lower_inner, "cup_lower_outer": lower_outer,
              "cup_upper": upper, "cradle": cradle, "longline_band": band, "back": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (lower_inner, lower_outer, upper, cradle, band, back):
            pattern.add(piece)
        pattern.declare_seam(("cup_lower_inner", "apex_seam"),
                             ("cup_lower_outer", "apex_seam"), tol=1.0)
        # THE HANDSHAKE SEAM: both cup mouths together = the cradle's wire line = the
        # solved arc run = the printed underwire's arc length.
        pattern.declare_seam([("cup_lower_inner", "mouth"), ("cup_lower_outer", "mouth")],
                             ("cradle", "wire_line"), tol=1.0)
        pattern.declare_seam(("cup_upper", "cup_seam"),
                             [("cup_lower_inner", "upper_seam"),
                              ("cup_lower_outer", "upper_seam")], tol=1.0)
        # Cradle + back wing onto the longline band's top edge.
        pattern.declare_seam([("cradle", "bottom"), ("back", "bottom")],
                             ("longline_band", "top"), tol=1.5)
        # Side seam: the cup's outer rise + upper side joins the wing side.
        pattern.declare_seam([("cup_lower_outer", "side"), ("cup_upper", "side")],
                             ("back", "side"), tol=1.5)

    band_opening = 2.0 * band.edge("lower").length()
    neck_opening = 2.0 * upper.edge("neckline").length()
    channel_run = 2.0 * cradle.edge("wire_line").length()
    total_bones = int(bone_count) * 2
    fabric_width = 1500.0
    area = (lower_inner.area() * 4.0 + lower_outer.area() * 4.0 + upper.area() * 4.0
            + cradle.area() * 2.0 + band.area() * 2.0 + back.area() * 2.0)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "stable bra tricot / duoplex", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"cups + cradle + longline band + wings at {fabric_width:.0f} mm width, "
                 "55% marker. Cups are cut on the STABLE grain — a wired cup shapes by "
                 "seam, not by stretch."},
        {"item": "underwire (Yantra4D bra-underwire)", "qty": 2, "unit": "piece",
         "note": f"one pair; chord (cup_width) {cup_width:.0f} mm, sweep {sweep_deg:.0f}°, "
                 f"solved arc run {WIRE_RUN:.1f} mm each. The hardware is the Yantra4D solid "
                 "(notion.hardware_ref -> bra-underwire), never modelled here; this cartridge "
                 "draws the channel it lives in, solved to that same run."},
        {"item": "wire channel tape 12 mm", "qty": round(channel_run * 1.06),
         "unit": "mm_length",
         "note": f"two channels x {WIRE_RUN:.1f} mm solved run + 6% turn-under."},
        {"item": "boning (spiral steel or synthetic) 7 mm + channel tape", "qty": total_bones,
         "unit": "piece",
         "note": f"{total_bones} vertical bones ({int(bone_count)} per side) in the longline "
                 "band at the marked channels — the longline structure that holds the "
                 "ribcage and takes support off the shoulders."},
        {"item": "band elastic (plush-back) 12 mm (waist)", "qty": round(band_opening * 0.9),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm waist opening x 0.9."},
        {"item": "neckline elastic (picot) 8 mm", "qty": round(neck_opening * 0.85),
         "unit": "mm_length", "note": f"neckline {neck_opening:.0f} mm at 0.85."},
        {"item": "strap elastic + sliders/rings", "qty": 2, "unit": "set",
         "note": "adjustable straps — the ring/slider hardware is a Yantra4D cartridge "
                 "(bra-ring-slider), not modelled here."},
        {"item": "hook-and-eye bra back (long, 4x3+)", "qty": 1, "unit": "piece",
         "note": "a longline needs a long hook-and-eye column at the marked CB notch — "
                 "Yantra4D hook-and-eye."},
    ]
    pattern.metadata = {
        "fc400_rank": 381, "family": "underwear_lounge", "fabric_hint": "power-mesh",
        "silhouette_note": "A three-piece wired cup on a LONGLINE band that reaches to the "
            "waist, boned vertically. The long band holds the ribcage and takes support off "
            "the shoulders — the depth a plain underwire band cannot give.",
        "hardware": "underwire via Yantra4D (notion.hardware_ref -> bra-underwire); "
            "cup_width drives BOTH the wire chord and the cradle's wire-line chord, sweep_deg "
            "drives both arc angles — the dimensional handshake, inherited from #219.",
        "solver": {
            "wire_chord_mm": round(cup_width, 1),
            "wire_sweep_deg": round(sweep_deg, 1),
            "wire_radius_mm": round(WIRE_R, 2),
            "wire_run_mm": round(WIRE_RUN, 2),
            "cradle_wire_line_mm": round(cradle.edge("wire_line").length(), 2),
            "cup_mouth_total_mm": round(lower_inner.edge("mouth").length()
                                        + lower_outer.edge("mouth").length(), 2),
            "note": "wire_run == cradle_wire_line == cup_mouth_total: the wire, the channel "
                    "and the cup mouth are one solved dimension.",
        },
        "longline": {
            "band_top_finished_mm": round(BAND_TOP_FIN, 1),
            "band_waist_finished_mm": round(BAND_BOT_FIN, 1),
            "longline_drop_mm": round(longline_drop, 1),
            "boning_channels": total_bones,
            "note": "The long band is cut at the underbust ring's negative ease at the top "
                    "and tapers to the waist ring below, boned vertically so it holds the "
                    "ribcage.",
        },
        "closure": "long centre-back hook-and-eye column",
        "drafting": "Made to measure to underbust, bust and waist girths; the wire is chosen "
            "by cup_width + sweep_deg and the cradle is solved to it, and the band runs to "
            "the waist.",
    }
    return pattern


result = build()

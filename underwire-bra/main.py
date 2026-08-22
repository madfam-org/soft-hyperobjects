"""
Underwire Bra — Fashion Cabinet Garment Cartridge (FC-300 #219; y4d bra-underwire).

The lane's anchor garment, and the first FC object to consume `bra-underwire` — the
Wave-T solid that sat on the shelf without a fashion consumer. A real underwire bra is
four structures, and this cartridge draws all four honestly:

  1. A THREE-PIECE CUP. Two lower cup sections (inner + outer) and one upper section.
     The vertical seam between the lower sections cones the cloth into apex projection;
     the horizontal seam under the upper section adds the second cone. Two cones at
     right angles is what makes a moulded-looking cup out of flat, stable cloth — the
     classic Danish/"three-part" cup. Cup volume is MADE TO MEASURE: the bust-minus-
     underbust surplus sets the apex projection and the cup's plan width.
  2. A CRADLE (the frame the cups sit in). Its upper edge is the WIRE LINE: a curved
     run that carries the wire channel. This edge is **SOLVED** to the underwire's own
     arc, not merely drawn near it — see `_solve_wire_line` below.
  3. A BAND that grips at negative ease and carries the load off the shoulders.
  4. A back wing closing at a center-back hook-and-eye.

The DIMENSIONAL HANDSHAKE (the point of the lane). `bra-underwire` is parameterised by
`cup_width` (the wire's chord — the straight span between its two tips) and `sweep_deg`
(how far around the cup the wire travels). Fashion Cabinet does not model the wire; it
models the CHANNEL the wire lives in, and that channel must be exactly as long as the
wire. So the flow runs:

    cup_width  ->  the wire's chord AND the cradle's wire-line chord   (one number)
    sweep_deg  ->  the wire's arc angle AND the cradle curve's arc angle
        =>  arc length = R * theta, with R = chord / (2 sin(theta/2))

`_solve_wire_line` builds the cradle's `wire_line` edge as that exact circular arc,
sampled as a polyline, so the drafted channel run and the printed wire agree to the
tenth of a millimetre. The manifest's `params_map` sends `cup_width` and `sweep_deg`
to the hardware, and both also drive the garment's own `wire_line` interface — which is
what makes this a coupled handshake rather than a name that happens to resolve.

The cup's lower edges are then built to the SAME solved run, so cup-to-cradle balances
by construction: the wire, the channel and the cup mouth are one dimension.

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
bust_girth      = float(PARAM(lambda: bust_girth, 940.0))
cup_width       = float(PARAM(lambda: cup_width, 130.0))   # wire chord, tip to tip
sweep_deg       = float(PARAM(lambda: sweep_deg, 210.0))   # wire arc angle
band_height     = float(PARAM(lambda: band_height, 34.0))
cradle_height   = float(PARAM(lambda: cradle_height, 26.0))  # band top -> wire line
strap_width     = float(PARAM(lambda: strap_width, 16.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 16.0))
upper_cup_frac  = float(PARAM(lambda: upper_cup_frac, 0.44))  # upper section share
seam_allowance  = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth      = max(640.0, min(bust_girth, 1500.0))
cup_width       = max(90.0, min(cup_width, 200.0))
sweep_deg       = max(150.0, min(sweep_deg, 260.0))
band_height     = max(20.0, min(band_height, 80.0))
cradle_height   = max(14.0, min(cradle_height, 60.0))
strap_width     = max(8.0, min(strap_width, 30.0))
negative_ease_pct = max(8.0, min(negative_ease_pct, 24.0))
upper_cup_frac  = max(0.30, min(upper_cup_frac, 0.60))
seam_allowance  = max(0.0, min(seam_allowance, 12.0))

# ── Support geometry ─────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_FINISHED = underbust_girth * NEG
BAND_HALF = BAND_FINISHED / 2.0
BH = band_height
CH = cradle_height
# Bust surplus over the ribcage, per side — the volume the cup must contain.
SURPLUS = max(24.0, (bust_girth - underbust_girth) / 2.0)
APEX = SURPLUS * 0.62          # apex projection height above the wire line
ELASTIC_ZONE = 8.0


# ── THE SOLVER: the wire line ────────────────────────────────────────────────
# The underwire is a circular arc of chord `cup_width` swept through `sweep_deg`.
# For a chord c subtending angle θ on a circle of radius R:  c = 2 R sin(θ/2),
# so R = c / (2 sin(θ/2)) and the arc's true run is L = R θ (θ in radians).
# The cradle's wire-line edge is built as THAT arc, so the sewn channel is exactly
# as long as the wire that will be threaded through it.
THETA = math.radians(sweep_deg)
WIRE_R = cup_width / (2.0 * math.sin(THETA / 2.0))
WIRE_RUN = WIRE_R * THETA                       # channel run = wire arc length (mm)
WIRE_RISE = WIRE_R * (1.0 - math.cos(THETA / 2.0))  # arc depth below the chord


def _wire_arc_points(x0, y0, samples=41, flip=False):
    """Sample the solved wire arc as a polyline from one tip to the other.

    The chord runs along x from (x0, y0) to (x0 + cup_width, y0); the arc bulges
    DOWN by WIRE_RISE (the wire cradles under the breast). `flip=True` returns the
    same arc traversed the other way, for pieces authored in the opposite rotation.
    """
    cx = x0 + cup_width / 2.0
    cy = y0 - WIRE_RISE + WIRE_R          # circle centre sits above the chord
    # Tip angles measured from the centre; the arc spans THETA symmetric about -90deg.
    a0 = -math.pi / 2.0 - THETA / 2.0
    pts = []
    for i in range(samples):
        a = a0 + THETA * i / (samples - 1)
        pts.append(fc.P(cx + WIRE_R * math.cos(a), cy + WIRE_R * math.sin(a)))
    if flip:
        pts.reverse()
    return pts


def _arc_edge(name, x0, y0, flip=False):
    """The solved wire arc as an Edge of chained Lines (a polyline of the true arc)."""
    pts = _wire_arc_points(x0, y0, flip=flip)
    return fc.Edge(name, [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)])


def _arc_split(frac):
    """Split the solved arc into two runs at arc-length fraction `frac`.

    Returns (points_first, points_second) sharing the split point, so the two lower
    cup sections' mouths sum EXACTLY to WIRE_RUN — the cup mouth and the channel are
    one dimension, checked by declare_seam.
    """
    pts = _wire_arc_points(0.0, 0.0, samples=81)
    n = len(pts)
    k = max(1, min(n - 2, int(round(frac * (n - 1)))))
    return pts[: k + 1], pts[k:]


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic edge, ELASTIC_ZONE mm inside.

    Pieces are authored CCW, so the inward normal at tangent t is (-t.y, t.x).
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


# ── The three-piece cup ──────────────────────────────────────────────────────
# Lower cup: the solved arc is the mouth (sews into the cradle's wire line), split
# at the apex position into an inner and an outer section. Each section rises to the
# apex, and the two share the vertical apex seam (identical curve = delta 0).
APEX_FRAC = 0.46                     # apex sits slightly inboard of the arc's middle
LOWER_H = APEX * (1.0 - upper_cup_frac) + APEX * 0.55  # lower section height at apex
UPPER_H = APEX * upper_cup_frac + 10.0


def _apex_seam(x_at_mouth, y_at_mouth, height):
    """The vertical apex seam profile, shared verbatim by both lower sections.

    A single Bezier from the mouth point up to the apex; reusing the identical curve
    on both sections makes their seam lengths equal to the micron.
    """
    return fc.Bezier(
        fc.P(x_at_mouth, y_at_mouth),
        fc.P(x_at_mouth + SURPLUS * 0.10, y_at_mouth + height * 0.40),
        fc.P(x_at_mouth + SURPLUS * 0.06, y_at_mouth + height * 0.78),
        fc.P(x_at_mouth, y_at_mouth + height),
    )


def build_cup_lower_inner():
    """Lower cup, inner section: center-front edge, mouth (solved arc), apex seam."""
    first, _ = _arc_split(APEX_FRAC)
    cf_pt = first[0]                      # the arc's centre-front tip
    apex_pt = first[-1]                   # the apex end of this section's mouth
    top_of_seam = fc.P(apex_pt.x, apex_pt.y + LOWER_H)
    cf_top = fc.P(cf_pt.x, cf_pt.y + LOWER_H * 0.30)
    # mouth is traversed apex -> CF tip (the reverse of the sampled arc)
    rev = list(reversed(first))
    edges = [
        # CCW: up the CF, across the top to the apex, down the apex seam, along the mouth.
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
        "cup_lower_inner",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("mouth", 0.5, "cradle match"),
                 fc.Notch("apex_seam", 0.5, "apex seam match")],
        grainline=fc.Grainline(fc.P(apex_pt.x * 0.5, apex_pt.y + LOWER_H * 0.25),
                               fc.P(apex_pt.x * 0.5, apex_pt.y + LOWER_H * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — lower inner section (cut 2 pairs)",
    )


def build_cup_lower_outer():
    """Lower cup, outer section: apex seam, mouth (solved arc), side rise."""
    _, second = _arc_split(APEX_FRAC)
    apex_pt = second[0]
    tip_pt = second[-1]
    rev = list(reversed(second))           # outer tip -> apex
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
        # mouth runs outer tip -> apex, closing the ring back at the apex seam start
        fc.Edge("mouth", [fc.Line(rev[i], rev[i + 1]) for i in range(len(rev) - 1)]),
    ]
    return fc.Piece(
        "cup_lower_outer",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("mouth", 0.5, "cradle match"),
                 fc.Notch("apex_seam", 0.5, "apex seam match")],
        grainline=fc.Grainline(fc.P((apex_pt.x + tip_pt.x) * 0.5, apex_pt.y + LOWER_H * 0.25),
                               fc.P((apex_pt.x + tip_pt.x) * 0.5, apex_pt.y + LOWER_H * 0.70)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — lower outer section (cut 2 pairs)",
    )


def build_cup_upper(lower_inner, lower_outer):
    """Upper cup section: its lower edge is built to the MEASURED combined upper_seam
    run of the two lower sections, so the horizontal cup seam balances exactly.

    The neckline above is elastic-finished; the outer corner carries the strap tab.
    """
    run = (lower_inner.edge("upper_seam").length()
           + lower_outer.edge("upper_seam").length())
    # A shallow arc of the same run: solve the radius of a circular arc of known
    # length and a chosen bow so the drafted lower edge matches `run` to the tenth mm.
    bow_frac = 0.16
    # For a circular arc, run = R*phi and sagitta s = R(1-cos(phi/2)); pick phi from
    # the desired sagitta/run ratio by fixed-point iteration (fast, monotone).
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
    # normalise so the left tip sits at the origin
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
        "cup_upper",
        edges,
        seam_allowance=seam_allowance,
        allowances={"neckline": 0.0},   # elastic-finished
        notches=[fc.Notch("cup_seam", APEX_FRAC, "apex seam match")],
        grainline=fc.Grainline(fc.P(right.x * 0.45, UPPER_H * 0.15),
                               fc.P(right.x * 0.45, UPPER_H * 0.72)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — upper section (cut 2 pairs)",
    )
    piece.internals = [_elastic_zone(piece.edge("neckline"), "neckline elastic zone",
                                     0.08, 0.92)]
    return piece


def build_cradle():
    """The cradle: the frame the cup sits in, carrying the WIRE CHANNEL.

    `wire_line` IS the solved underwire arc — same chord (cup_width), same sweep
    (sweep_deg), therefore the same run. The channel topstitched along it is exactly
    long enough for the printed wire, and the cup mouth sews into it.
    """
    # The whole solved arc, lifted to the cradle's top edge height.
    arc = _wire_arc_points(0.0, CH, samples=81)
    left, right = arc[0], arc[-1]
    # CCW: bottom (right->left), CF side (up), wire line (left->right), side (down)
    bottom = fc.Edge("bottom", [fc.Line(fc.P(right.x, 0.0), fc.P(left.x, 0.0))])
    cf = fc.Edge("center_front", [fc.Line(fc.P(left.x, 0.0), left)])
    wire_line = fc.Edge("wire_line",
                        [fc.Line(arc[i], arc[i + 1]) for i in range(len(arc) - 1)])
    side = fc.Edge("side", [fc.Line(right, fc.P(right.x, 0.0))])
    channel = fc.Internal(
        "wire channel (stitch line)",
        [fc.P(p.x, p.y - 5.0) for p in arc[::4]],
        kind="marking",
    )
    return fc.Piece(
        "cradle",
        [bottom, cf, wire_line, side],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("wire_line", APEX_FRAC, "apex position"),
                 fc.Notch("bottom", 0.5, "band match")],
        grainline=fc.Grainline(fc.P(cup_width * 0.5, 4.0), fc.P(cup_width * 0.5, CH * 0.9)),
        internals=[channel],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cradle — wire channel frame (cut 2 pairs)",
    )


def build_band(cradle_bottom_len):
    """Underband, cut 2 mirror (CF -> CB hook).

    `top_cradle` is built to the measured cradle bottom so the cradle sits on the band
    with a balanced seam; `top_back` carries the back wing.
    """
    front = cradle_bottom_len
    back = max(40.0, BAND_HALF - front)
    cf = fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))])
    top_cradle = fc.Edge("top_cradle", [fc.Line(fc.P(0.0, BH), fc.P(front, BH))])
    top_back = fc.Edge("top_back", [fc.Line(fc.P(front, BH), fc.P(front + back, BH))])
    cb = fc.Edge("center_back", [fc.Line(fc.P(front + back, BH), fc.P(front + back, 0.0))])
    lower = fc.Edge("lower", [fc.Line(fc.P(front + back, 0.0), fc.P(0.0, 0.0))])
    piece = fc.Piece(
        "band",
        [cf, top_cradle, top_back, cb, lower],
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0},   # elastic-finished
        notches=[fc.Notch("top_cradle", 0.5, "cradle centre"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P((front + back) * 0.5, BH * 0.25),
                               fc.P((front + back) * 0.5, BH * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Underband (cut 2 pairs, CB hook)",
    )
    piece.internals = [_elastic_zone(piece.edge("lower"), "band elastic zone", 0.04, 0.96)]
    return piece


def build_back(side_len, back_span):
    """Back wing: side seam (built to the cup's measured side rise), strap tab, CB hook."""
    wing_h = side_len
    x_end = back_span
    side = fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, wing_h))])
    strap_tab = fc.Edge("strap_tab", [fc.Line(fc.P(0.0, wing_h), fc.P(strap_width, wing_h))])
    top = fc.Edge("top", [fc.Bezier(fc.P(strap_width, wing_h),
                                    fc.P(x_end * 0.42, wing_h * 0.70),
                                    fc.P(x_end * 0.84, BH + 10.0),
                                    fc.P(x_end, BH))])
    cb = fc.Edge("center_back", [fc.Line(fc.P(x_end, BH), fc.P(x_end, 0.0))])
    bottom = fc.Edge("bottom", [fc.Line(fc.P(x_end, 0.0), fc.P(0.0, 0.0))])
    piece = fc.Piece(
        "back",
        [side, strap_tab, top, cb, bottom],
        seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("bottom", 0.5, "band match"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P(x_end * 0.5, BH * 0.4), fc.P(x_end * 0.5, wing_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back wing (cut 2 pairs, CB hook)",
    )
    piece.internals = [_elastic_zone(piece.edge("top"), "wing elastic zone", 0.06, 0.94)]
    return piece


def build():
    pattern = fc.PatternSet("underwire-bra")
    lower_inner = build_cup_lower_inner()
    lower_outer = build_cup_lower_outer()
    upper = build_cup_upper(lower_inner, lower_outer)
    cradle = build_cradle()
    band = build_band(cradle.edge("bottom").length())
    back_span = max(40.0, BAND_HALF - cradle.edge("bottom").length())
    back = build_back(lower_outer.edge("side").length() + upper.edge("side").length(),
                      back_span)

    picked = {"cup_lower_inner": lower_inner, "cup_lower_outer": lower_outer,
              "cup_upper": upper, "cradle": cradle, "band": band, "back": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (lower_inner, lower_outer, upper, cradle, band, back):
            pattern.add(piece)
        # The apex seam: the two lower sections cone the cloth into projection.
        pattern.declare_seam(("cup_lower_inner", "apex_seam"),
                             ("cup_lower_outer", "apex_seam"), tol=1.0)
        # THE HANDSHAKE SEAM: both cup mouths together = the cradle's wire line =
        # the solved arc run = the printed underwire's arc length.
        pattern.declare_seam([("cup_lower_inner", "mouth"), ("cup_lower_outer", "mouth")],
                             ("cradle", "wire_line"), tol=1.0)
        # The horizontal cup seam: upper section onto both lower sections' tops.
        pattern.declare_seam(("cup_upper", "cup_seam"),
                             [("cup_lower_inner", "upper_seam"),
                              ("cup_lower_outer", "upper_seam")], tol=1.0)
        # Cradle onto the band's front span.
        pattern.declare_seam(("cradle", "bottom"), ("band", "top_cradle"), tol=1.0)
        # Back wing onto the band's back span.
        pattern.declare_seam(("back", "bottom"), ("band", "top_back"), tol=1.0)
        # Side seam: the cup's outer rise + upper side joins the wing side.
        pattern.declare_seam([("cup_lower_outer", "side"), ("cup_upper", "side")],
                             ("back", "side"), tol=1.5)

    # ── Elastic + hardware accounting ────────────────────────────────────────
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
         "note": f"cups + cradle + band + wings at {fabric_width:.0f} mm width, 55% "
                 "marker. Cups are cut on the STABLE (non-stretch) grain — an "
                 "underwire cup shapes by seam, not by stretch."},
        {"item": "underwire (Yantra4D bra-underwire)", "qty": 2, "unit": "piece",
         "note": f"one pair; chord (cup_width) {cup_width:.0f} mm, sweep "
                 f"{sweep_deg:.0f}°, solved arc run {WIRE_RUN:.1f} mm each. The "
                 "hardware is the Yantra4D solid (notion.hardware_ref -> "
                 "bra-underwire), never modelled here; this cartridge draws the "
                 "channel it lives in, solved to that same run."},
        {"item": "wire channel tape 12 mm", "qty": round(channel_run * 1.06),
         "unit": "mm_length",
         "note": f"two channels x {WIRE_RUN:.1f} mm solved run + 6% turn-under; "
                 "topstitch along the cradle's marked channel line, close both ends "
                 "so the wire tips cannot work through."},
        {"item": "band elastic (plush-back) 12 mm", "qty": round(band_opening * 0.92),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm opening x 0.92 — the band carries "
                 "the load, so it is cut short and stretched on."},
        {"item": "neckline + armhole elastic (picot) 8 mm",
         "qty": round((neck_opening + arm_opening) * 0.85), "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} mm + wing top {arm_opening:.0f} mm at "
                 "0.85; apply into the marked zones."},
        {"item": "strap elastic + sliders/rings", "qty": 2, "unit": "set",
         "note": "adjustable straps — the ring/slider hardware is a Yantra4D "
                 "cartridge (bra-ring-slider), not modelled here."},
        {"item": "hook-and-eye bra back (3x2)", "qty": 1, "unit": "piece",
         "note": "centre-back closure at the marked CB notch — Yantra4D hook-and-eye."},
        {"item": "polyester thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "fine needle; the cup seams are topstitched flat so they do not "
                 "print through."},
    ]
    pattern.metadata = {
        "fc300_rank": 219, "family": "underwear_lounge", "fabric_hint": "tricot-nylon",
        "silhouette_note": "Three-piece cup (two lower sections + one upper) in a "
            "wired cradle on a negative-ease band. Two cones at right angles — the "
            "vertical apex seam and the horizontal cup seam — build projection out of "
            "stable cloth, which is what an underwire bra does that a bralette cannot.",
        "hardware": "underwire via Yantra4D (notion.hardware_ref -> bra-underwire); "
            "cup_width drives BOTH the wire chord and the cradle's wire-line chord, "
            "sweep_deg drives both arc angles — the dimensional handshake.",
        "solver": {
            "wire_chord_mm": round(cup_width, 1),
            "wire_sweep_deg": round(sweep_deg, 1),
            "wire_radius_mm": round(WIRE_R, 2),
            "wire_run_mm": round(WIRE_RUN, 2),
            "wire_rise_mm": round(WIRE_RISE, 2),
            "cradle_wire_line_mm": round(cradle.edge("wire_line").length(), 2),
            "cup_mouth_total_mm": round(lower_inner.edge("mouth").length()
                                        + lower_outer.edge("mouth").length(), 2),
            "note": "wire_run == cradle_wire_line == cup_mouth_total: the wire, the "
                    "channel and the cup mouth are one solved dimension.",
        },
        "solved": {
            "band_finished_mm": round(BAND_FINISHED, 1),
            "bust_surplus_mm": round(SURPLUS, 1),
            "apex_projection_mm": round(APEX, 1),
            "band_opening_mm": round(band_opening, 1),
        },
        "closure": "centre-back hook-and-eye (3x2)",
        "drafting": "Made to measure to underbust and bust girths; the wire is chosen "
            "by cup_width + sweep_deg and the cradle is solved to it.",
    }
    return pattern


result = build()

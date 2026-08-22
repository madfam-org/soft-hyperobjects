"""
Balconette Bra — Fashion Cabinet Garment Cartridge (FC-300 #220; y4d bra-underwire).

The horizontal-seam cousin of the underwire bra. Where a three-piece cup cones the
cloth twice (a vertical apex seam plus a horizontal one), a BALCONETTE cones it ONCE,
along a single horizontal seam that runs straight across the cup at roughly apex
height. That one choice is the whole garment:

  - The cup is wide and shallow, cut off square at the top rather than curving up to
    the shoulder, so the neckline runs almost horizontally across the bust — the
    "balcony" the style is named for. Straps sit wide, near the outer cup corner.
  - Because there is no vertical seam through the apex, the horizontal seam carries
    ALL the shaping. It is drafted with a deliberate LENGTH SURPLUS on the lower
    section: the lower cup's top edge is longer than the upper cup's bottom edge, and
    that surplus is eased in during sewing. Easing a longer curve into a shorter one
    is exactly how flat cloth is forced into a cone — the seam's declared `ease`
    records it honestly instead of hiding it in a "sew and hope" instruction.
  - The wire runs shallower (a smaller sweep) than a full cup, which is what lets the
    top edge sit low and horizontal.

Same DIMENSIONAL HANDSHAKE as `underwire-bra`, and the same solver: `bra-underwire` is
parameterised by `cup_width` (the wire's chord) and `sweep_deg` (its arc angle), and
the cradle's `wire_line` edge is built as exactly that circular arc, so the sewn
channel is precisely as long as the wire threaded through it:

    R = cup_width / (2 sin(theta/2))      arc run L = R * theta

Both mapped parameters also drive the garment's own `wire_line` interface, so the
handshake is dimensional, not merely nominal.

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
cup_width       = float(PARAM(lambda: cup_width, 140.0))   # wire chord, tip to tip
sweep_deg       = float(PARAM(lambda: sweep_deg, 180.0))   # shallower than a full cup
band_height     = float(PARAM(lambda: band_height, 32.0))
cradle_height   = float(PARAM(lambda: cradle_height, 24.0))
strap_width     = float(PARAM(lambda: strap_width, 14.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 16.0))
cup_rise        = float(PARAM(lambda: cup_rise, 62.0))     # wire line -> top of cup
seam_ease_pct   = float(PARAM(lambda: seam_ease_pct, 7.0))  # eased into the cup seam
seam_allowance  = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth      = max(640.0, min(bust_girth, 1500.0))
cup_width       = max(90.0, min(cup_width, 210.0))
sweep_deg       = max(140.0, min(sweep_deg, 230.0))
band_height     = max(20.0, min(band_height, 80.0))
cradle_height   = max(14.0, min(cradle_height, 60.0))
strap_width     = max(8.0, min(strap_width, 30.0))
negative_ease_pct = max(8.0, min(negative_ease_pct, 24.0))
cup_rise        = max(35.0, min(cup_rise, 120.0))
seam_ease_pct   = max(0.0, min(seam_ease_pct, 14.0))
seam_allowance  = max(0.0, min(seam_allowance, 12.0))

# ── Support geometry ─────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_FINISHED = underbust_girth * NEG
BAND_HALF = BAND_FINISHED / 2.0
BH = band_height
CH = cradle_height
SURPLUS = max(24.0, (bust_girth - underbust_girth) / 2.0)
ELASTIC_ZONE = 8.0
# The horizontal seam sits at this height above the wire line — apex height.
SEAM_H = cup_rise * 0.52


# ── THE SOLVER: the wire line (shared with underwire-bra) ────────────────────
THETA = math.radians(sweep_deg)
WIRE_R = cup_width / (2.0 * math.sin(THETA / 2.0))
WIRE_RUN = WIRE_R * THETA
WIRE_RISE = WIRE_R * (1.0 - math.cos(THETA / 2.0))


def _wire_arc_points(x0, y0, samples=81):
    """Sample the solved wire arc from tip to tip; the arc bulges DOWN by WIRE_RISE."""
    cx = x0 + cup_width / 2.0
    cy = y0 - WIRE_RISE + WIRE_R
    a0 = -math.pi / 2.0 - THETA / 2.0
    return [fc.P(cx + WIRE_R * math.cos(a0 + THETA * i / (samples - 1)),
                 cy + WIRE_R * math.sin(a0 + THETA * i / (samples - 1)))
            for i in range(samples)]


def _poly_edge(name, pts):
    """Chain a sampled polyline into an Edge of Lines."""
    return fc.Edge(name, [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)])


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic edge, ELASTIC_ZONE mm inside (CCW normal)."""
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


def _arc_of_run(run, bow_frac, samples=41):
    """A circular arc polyline of a GIVEN run and a given sagitta/run ratio.

    Solves phi from (1 - cos(phi/2))/phi = bow_frac by fixed-point iteration, then
    R = run / phi. Used to draft an edge to a measured mating length exactly.
    """
    phi = 1.0
    for _ in range(60):
        s_over = (1.0 - math.cos(phi / 2.0)) / phi
        if s_over <= 1e-9:
            break
        phi *= (bow_frac / s_over) ** 0.5
        phi = max(0.05, min(phi, math.pi * 0.98))
    r = run / phi
    pts = [fc.P(r * math.cos(-math.pi / 2.0 - phi / 2.0 + phi * i / (samples - 1)),
                r * math.sin(-math.pi / 2.0 - phi / 2.0 + phi * i / (samples - 1)) + r)
           for i in range(samples)]
    dx, dy = pts[0].x, pts[0].y
    return [fc.P(p.x - dx, p.y - dy) for p in pts]


# ── Pieces ───────────────────────────────────────────────────────────────────
def build_cup_lower():
    """Lower cup: the solved wire arc is the mouth; a bowed top edge carries the ease.

    The top edge is drafted LONGER than the upper cup's bottom edge by seam_ease_pct;
    that surplus is eased in at the machine and is what cones the cloth. It is declared
    on the seam as `ease`, so the verifier checks the intended surplus rather than
    silently tolerating a mismatch.
    """
    arc = _wire_arc_points(0.0, 0.0)
    left, right = arc[0], arc[-1]
    # The seam line: a shallow bow whose run is the eased (longer) length.
    plain_run = cup_width * 1.02
    eased_run = plain_run * (1.0 + seam_ease_pct / 100.0)
    top_pts = _arc_of_run(eased_run, 0.10)
    # place the top edge at SEAM_H above the chord, spanning the cup
    span = top_pts[-1].x - top_pts[0].x
    x_off = left.x + (cup_width - span) / 2.0
    top_pts = [fc.P(p.x + x_off, p.y + SEAM_H) for p in top_pts]
    edges = [
        # CCW: mouth (left tip -> right tip), up the outer side, top (right -> left), CF down
        _poly_edge("mouth", arc),
        fc.Edge("side", [fc.Line(right, top_pts[-1])]),
        _poly_edge("cup_seam", list(reversed(top_pts))),
        fc.Edge("center_front", [fc.Line(top_pts[0], left)]),
    ]
    return fc.Piece(
        "cup_lower",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("mouth", 0.5, "cradle apex match"),
                 fc.Notch("cup_seam", 0.5, "apex — ease evenly either side")],
        grainline=fc.Grainline(fc.P(left.x + cup_width * 0.5, -WIRE_RISE * 0.4),
                               fc.P(left.x + cup_width * 0.5, SEAM_H * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — lower section (cut 2 pairs, ease into seam)",
    )


def build_cup_upper(lower):
    """Upper cup ('the balcony'): its bottom edge is built to the lower cup's seam run
    MINUS the ease, and its top edge runs nearly horizontally — the balconette line."""
    eased = lower.edge("cup_seam").length()
    plain = eased / (1.0 + seam_ease_pct / 100.0)
    bottom = _arc_of_run(plain, 0.10)
    left, right = bottom[0], bottom[-1]
    rise = cup_rise - SEAM_H
    # The top edge is close to horizontal (that is the balconette signature): it lifts
    # only slightly toward the outer corner where the strap lands.
    top_l = fc.P(left.x, left.y + rise * 0.86)
    tab_in = fc.P(right.x - strap_width, right.y + rise)
    tab_out = fc.P(right.x, right.y + rise)
    edges = [
        _poly_edge("cup_seam", bottom),
        fc.Edge("side", [fc.Line(right, tab_out)]),
        fc.Edge("strap_tab", [fc.Line(tab_out, tab_in)]),
        fc.Edge("neckline", [fc.Bezier(tab_in,
                                       fc.P(left.x + (tab_in.x - left.x) * 0.60,
                                            tab_in.y - rise * 0.06),
                                       fc.P(left.x + (tab_in.x - left.x) * 0.24,
                                            top_l.y + rise * 0.05),
                                       top_l)]),
        fc.Edge("center_front", [fc.Line(top_l, left)]),
    ]
    piece = fc.Piece(
        "cup_upper",
        edges,
        seam_allowance=seam_allowance,
        allowances={"neckline": 0.0},
        notches=[fc.Notch("cup_seam", 0.5, "apex match")],
        grainline=fc.Grainline(fc.P(right.x * 0.5, rise * 0.15),
                               fc.P(right.x * 0.5, rise * 0.80)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — upper section / balcony (cut 2 pairs)",
    )
    piece.internals = [_elastic_zone(piece.edge("neckline"), "neckline elastic zone",
                                     0.08, 0.92)]
    return piece


def build_cradle():
    """The cradle: `wire_line` IS the solved underwire arc — same chord, same sweep."""
    arc = _wire_arc_points(0.0, CH)
    left, right = arc[0], arc[-1]
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(right.x, 0.0), fc.P(left.x, 0.0))]),
        fc.Edge("center_front", [fc.Line(fc.P(left.x, 0.0), left)]),
        _poly_edge("wire_line", arc),
        fc.Edge("side", [fc.Line(right, fc.P(right.x, 0.0))]),
    ]
    channel = fc.Internal("wire channel (stitch line)",
                          [fc.P(p.x, p.y - 5.0) for p in arc[::4]], kind="marking")
    return fc.Piece(
        "cradle",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("wire_line", 0.5, "apex position"),
                 fc.Notch("bottom", 0.5, "band match")],
        grainline=fc.Grainline(fc.P(cup_width * 0.5, 4.0), fc.P(cup_width * 0.5, CH * 0.9)),
        internals=[channel],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cradle — wire channel frame (cut 2 pairs)",
    )


def build_band(front_span):
    """Underband, cut 2 mirror (CF -> CB hook), front span built to the cradle bottom."""
    back = max(40.0, BAND_HALF - front_span)
    edges = [
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))]),
        fc.Edge("top_cradle", [fc.Line(fc.P(0.0, BH), fc.P(front_span, BH))]),
        fc.Edge("top_back", [fc.Line(fc.P(front_span, BH), fc.P(front_span + back, BH))]),
        fc.Edge("center_back", [fc.Line(fc.P(front_span + back, BH),
                                        fc.P(front_span + back, 0.0))]),
        fc.Edge("lower", [fc.Line(fc.P(front_span + back, 0.0), fc.P(0.0, 0.0))]),
    ]
    piece = fc.Piece(
        "band",
        edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0},
        notches=[fc.Notch("top_cradle", 0.5, "cradle centre"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P((front_span + back) * 0.5, BH * 0.25),
                               fc.P((front_span + back) * 0.5, BH * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Underband (cut 2 pairs, CB hook)",
    )
    piece.internals = [_elastic_zone(piece.edge("lower"), "band elastic zone", 0.04, 0.96)]
    return piece


def build_back(side_len, back_span):
    """Back wing: side built to the measured cup side rise; CB hook closure."""
    wing_h = side_len
    x_end = back_span
    edges = [
        fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, wing_h))]),
        fc.Edge("strap_tab", [fc.Line(fc.P(0.0, wing_h), fc.P(strap_width, wing_h))]),
        fc.Edge("top", [fc.Bezier(fc.P(strap_width, wing_h),
                                  fc.P(x_end * 0.40, wing_h * 0.72),
                                  fc.P(x_end * 0.84, BH + 9.0),
                                  fc.P(x_end, BH))]),
        fc.Edge("center_back", [fc.Line(fc.P(x_end, BH), fc.P(x_end, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(x_end, 0.0), fc.P(0.0, 0.0))]),
    ]
    piece = fc.Piece(
        "back",
        edges,
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
    pattern = fc.PatternSet("balconette-bra")
    lower = build_cup_lower()
    upper = build_cup_upper(lower)
    cradle = build_cradle()
    front_span = cradle.edge("bottom").length()
    band = build_band(front_span)
    back_span = max(40.0, BAND_HALF - front_span)
    back = build_back(lower.edge("side").length() + upper.edge("side").length(), back_span)

    picked = {"cup_lower": lower, "cup_upper": upper, "cradle": cradle,
              "band": band, "back": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (lower, upper, cradle, band, back):
            pattern.add(piece)
        # THE HANDSHAKE SEAM: the cup mouth is the cradle's wire line is the wire arc.
        pattern.declare_seam(("cup_lower", "mouth"), ("cradle", "wire_line"), tol=1.0)
        # The single horizontal cup seam, with the shaping ease declared explicitly:
        # the lower section is longer by exactly the eased surplus.
        ease_mm = lower.edge("cup_seam").length() - upper.edge("cup_seam").length()
        pattern.declare_seam(("cup_lower", "cup_seam"), ("cup_upper", "cup_seam"),
                             tol=1.0, ease=ease_mm)
        pattern.declare_seam(("cradle", "bottom"), ("band", "top_cradle"), tol=1.0)
        pattern.declare_seam(("back", "bottom"), ("band", "top_back"), tol=1.0)
        pattern.declare_seam([("cup_lower", "side"), ("cup_upper", "side")],
                             ("back", "side"), tol=1.5)

    band_opening = 2.0 * band.edge("lower").length()
    neck_opening = 2.0 * upper.edge("neckline").length()
    arm_opening = 2.0 * back.edge("top").length()
    channel_run = 2.0 * cradle.edge("wire_line").length()
    ease_total = lower.edge("cup_seam").length() - upper.edge("cup_seam").length()

    fabric_width = 1500.0
    area = (lower.area() * 4.0 + upper.area() * 4.0 + cradle.area() * 2.0
            + band.area() * 2.0 + back.area() * 2.0)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "stable bra tricot / duoplex", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"cups + cradle + band + wings at {fabric_width:.0f} mm width, 55% "
                 "marker. Cut the cups on the stable grain — a balconette shapes by "
                 "the eased horizontal seam, not by stretch."},
        {"item": "underwire (Yantra4D bra-underwire)", "qty": 2, "unit": "piece",
         "note": f"one pair; chord {cup_width:.0f} mm, sweep {sweep_deg:.0f}°, solved "
                 f"arc run {WIRE_RUN:.1f} mm each. Hardware is the Yantra4D solid "
                 "(notion.hardware_ref -> bra-underwire), never modelled here; the "
                 "cradle channel is solved to that same run. A balconette runs a "
                 "SHALLOWER sweep than a full cup — that is what lets the top edge "
                 "sit low and horizontal."},
        {"item": "wire channel tape 12 mm", "qty": round(channel_run * 1.06),
         "unit": "mm_length",
         "note": f"two channels x {WIRE_RUN:.1f} mm + 6% turn-under; close both ends."},
        {"item": "band elastic (plush-back) 12 mm", "qty": round(band_opening * 0.92),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm opening x 0.92."},
        {"item": "neckline + armhole elastic (picot) 8 mm",
         "qty": round((neck_opening + arm_opening) * 0.85), "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} mm + wing top {arm_opening:.0f} mm at 0.85."},
        {"item": "strap elastic + sliders/rings", "qty": 2, "unit": "set",
         "note": "straps sit WIDE on a balconette — near the outer cup corner. Ring "
                 "and slider hardware is the Yantra4D bra-ring-slider cartridge."},
        {"item": "hook-and-eye bra back (2x2)", "qty": 1, "unit": "piece",
         "note": "centre-back closure at the marked CB notch — Yantra4D hook-and-eye."},
        {"item": "polyester thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": f"ease {ease_total:.1f} mm into the cup seam per cup, spread evenly "
                 "either side of the apex notch; press over a ham."},
    ]
    pattern.metadata = {
        "fc300_rank": 220, "family": "underwear_lounge", "fabric_hint": "tricot-nylon",
        "silhouette_note": "A balconette: ONE horizontal cup seam carrying all the "
            "shaping, a low near-horizontal top edge, wide-set straps, and a shallow "
            "wire sweep. The lower cup is cut longer than the upper and the surplus is "
            "eased in — the declared seam ease records the shaping honestly.",
        "hardware": "underwire via Yantra4D (notion.hardware_ref -> bra-underwire); "
            "cup_width drives both the wire chord and the channel chord, sweep_deg "
            "both arc angles — the dimensional handshake, shared with underwire-bra.",
        "solver": {
            "wire_chord_mm": round(cup_width, 1),
            "wire_sweep_deg": round(sweep_deg, 1),
            "wire_radius_mm": round(WIRE_R, 2),
            "wire_run_mm": round(WIRE_RUN, 2),
            "cradle_wire_line_mm": round(cradle.edge("wire_line").length(), 2),
            "cup_mouth_mm": round(lower.edge("mouth").length(), 2),
            "note": "wire_run == cradle_wire_line == cup_mouth: one solved dimension.",
        },
        "solved": {
            "band_finished_mm": round(BAND_FINISHED, 1),
            "bust_surplus_mm": round(SURPLUS, 1),
            "cup_seam_ease_mm": round(ease_total, 2),
            "seam_ease_pct": seam_ease_pct,
            "band_opening_mm": round(band_opening, 1),
        },
        "closure": "centre-back hook-and-eye (2x2)",
        "drafting": "Made to measure to underbust and bust girths; the wire is chosen "
            "by cup_width + sweep_deg and the cradle is solved to it.",
    }
    return pattern


result = build()

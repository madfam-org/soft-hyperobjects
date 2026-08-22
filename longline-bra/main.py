"""
Longline Bra — Fashion Cabinet Garment Cartridge (FC-300 #221; y4d boning-stay).

A bra that keeps going. Where an ordinary bra stops at the underband, a longline
continues down over the ribs to a deep midriff panel, and that extra length changes
what holds the garment up: the load stops hanging off a narrow elastic band and starts
being carried by a broad, lightly boned panel gripping the whole lower ribcage. That is
why longlines are the bridge between lingerie and foundationwear — and why they need
BONING to stop the panel rolling and collapsing on itself.

Structure:
  - A two-piece cup (lower + upper) over a wired cradle — the same solved wire geometry
    the rest of this lane uses, so the bra half is honest.
  - A MIDRIFF PANEL, front and side, whose vertical seams carry BONING CHANNELS. The
    panel's depth is `midriff_depth`, measured from the wire line down to the hem.
  - A back wing closing at a multi-row centre-back hook-and-eye (a longline needs more
    rows: there is more length to hold shut).

The DIMENSIONAL HANDSHAKE (this lane's `boning-stay` consumer). The Yantra4D solid
`boning-stay` is a stay PLUS the channel it lives in, parameterised by `stay_length`
and `stay_width`. A bone that is too long punches through the hem; too short and the
panel folds above it. So the channel length is not a guess — it is derived:

    channel_len = midriff_depth - 2 * bone_clearance

and `stay_length` is mapped to exactly that expression. Because `midriff_depth` also
drives the garment's own `midriff_seam` and `boning_channels` interfaces, the same
dimension reaches the printed stay and the drafted channel: a coupled handshake, which
is what `hardware_dimensional_rules` checks for. The drafted channel internals are
drawn at that literal solved length, so what is marked on the cloth is what is printed.

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
waist_girth     = float(PARAM(lambda: waist_girth, 700.0))
cup_width       = float(PARAM(lambda: cup_width, 135.0))
sweep_deg       = float(PARAM(lambda: sweep_deg, 200.0))
midriff_depth   = float(PARAM(lambda: midriff_depth, 130.0))  # wire line -> hem
bone_clearance  = float(PARAM(lambda: bone_clearance, 8.0))   # bone tip inset per end
cup_rise        = float(PARAM(lambda: cup_rise, 78.0))
strap_width     = float(PARAM(lambda: strap_width, 15.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 12.0))
seam_allowance  = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth      = max(640.0, min(bust_girth, 1500.0))
waist_girth     = max(500.0, min(waist_girth, 1400.0))
cup_width       = max(90.0, min(cup_width, 200.0))
sweep_deg       = max(150.0, min(sweep_deg, 250.0))
midriff_depth   = max(70.0, min(midriff_depth, 260.0))
bone_clearance  = max(3.0, min(bone_clearance, 20.0))
cup_rise        = max(45.0, min(cup_rise, 150.0))
strap_width     = max(8.0, min(strap_width, 30.0))
negative_ease_pct = max(6.0, min(negative_ease_pct, 22.0))
seam_allowance  = max(0.0, min(seam_allowance, 15.0))

# ── Support geometry ─────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
RIB_HALF = underbust_girth * NEG / 2.0        # half the gripping ribcage ring
WAIST_HALF = waist_girth * NEG / 2.0          # half the hem ring (the panel's bottom)
MD = midriff_depth
SURPLUS = max(24.0, (bust_girth - underbust_girth) / 2.0)
ELASTIC_ZONE = 8.0

# ── THE BONING SOLVER ────────────────────────────────────────────────────────
# The stay must live inside the panel with a clearance at each end so its tips cannot
# work through the hem or the wire line. This is the number the hardware receives.
CHANNEL_LEN = max(20.0, MD - 2.0 * bone_clearance)

# ── The wire solver (shared across the lane) ─────────────────────────────────
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
    return fc.Edge(name, [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)])


def _arc_of_run(run, bow_frac, samples=41):
    """A circular arc polyline of a GIVEN run and sagitta/run ratio (see balconette)."""
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


def _elastic_zone(edge, label, t0, t1, samples=13):
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


def _bone_channel(label, x, y_bottom):
    """A boning channel internal drawn at the SOLVED stay length.

    Marked from `y_bottom` upward for exactly CHANNEL_LEN mm — the same number the
    manifest maps to the hardware's `stay_length`. What is chalked is what is printed.
    """
    return fc.Internal(label, [fc.P(x, y_bottom), fc.P(x, y_bottom + CHANNEL_LEN)],
                       kind="marking")


# ── Pieces ───────────────────────────────────────────────────────────────────
def build_cup_lower():
    """Lower cup: the solved wire arc is the mouth; a bowed top edge takes the upper."""
    arc = _wire_arc_points(0.0, 0.0)
    left, right = arc[0], arc[-1]
    seam_h = cup_rise * 0.48
    top_pts = _arc_of_run(cup_width * 1.06, 0.10)
    span = top_pts[-1].x - top_pts[0].x
    x_off = left.x + (cup_width - span) / 2.0
    top_pts = [fc.P(p.x + x_off, p.y + seam_h) for p in top_pts]
    edges = [
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
                 fc.Notch("cup_seam", 0.5, "apex match")],
        grainline=fc.Grainline(fc.P(left.x + cup_width * 0.5, -WIRE_RISE * 0.4),
                               fc.P(left.x + cup_width * 0.5, seam_h * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cup — lower section (cut 2 pairs)",
    )


def build_cup_upper(lower):
    """Upper cup, built to the lower cup's measured seam run."""
    run = lower.edge("cup_seam").length()
    bottom = _arc_of_run(run, 0.10)
    left, right = bottom[0], bottom[-1]
    rise = cup_rise - cup_rise * 0.48
    top_l = fc.P(left.x, left.y + rise * 0.70)
    tab_in = fc.P(right.x - strap_width, right.y + rise)
    tab_out = fc.P(right.x, right.y + rise)
    edges = [
        _poly_edge("cup_seam", bottom),
        fc.Edge("side", [fc.Line(right, tab_out)]),
        fc.Edge("strap_tab", [fc.Line(tab_out, tab_in)]),
        fc.Edge("neckline", [fc.Bezier(tab_in,
                                       fc.P(left.x + (tab_in.x - left.x) * 0.58,
                                            tab_in.y - rise * 0.12),
                                       fc.P(left.x + (tab_in.x - left.x) * 0.22,
                                            top_l.y + rise * 0.10),
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
        label="Cup — upper section (cut 2 pairs)",
    )
    piece.internals = [_elastic_zone(piece.edge("neckline"), "neckline elastic zone",
                                     0.08, 0.92)]
    return piece


def build_cradle():
    """The cradle: `wire_line` IS the solved underwire arc; sits on the midriff panel."""
    ch = 20.0
    arc = _wire_arc_points(0.0, ch)
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
                 fc.Notch("bottom", 0.5, "midriff match")],
        grainline=fc.Grainline(fc.P(cup_width * 0.5, 3.0), fc.P(cup_width * 0.5, ch * 0.9)),
        internals=[channel],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cradle — wire channel frame (cut 2 pairs)",
    )


def build_midriff_front(top_run):
    """Front midriff panel: the boned heart of a longline.

    Top edge is built to the measured cradle bottom (they sew together); the panel
    tapers slightly to the waist and carries boning channels at both vertical seams,
    each drawn at the SOLVED CHANNEL_LEN.
    """
    top_w = top_run
    # The hem is nipped toward the waist proportionally.
    bot_w = top_w * max(0.72, min(1.0, WAIST_HALF / max(RIB_HALF, 1.0)))
    dx = (top_w - bot_w) / 2.0
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(dx + bot_w, 0.0), fc.P(dx, 0.0))]),
        fc.Edge("seam_cf", [fc.Line(fc.P(dx, 0.0), fc.P(0.0, MD))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, MD), fc.P(top_w, MD))]),
        fc.Edge("seam_side", [fc.Line(fc.P(top_w, MD), fc.P(dx + bot_w, 0.0))]),
    ]
    internals = [
        _bone_channel("bone channel — CF seam", dx * 0.5 + 5.0, bone_clearance),
        _bone_channel("bone channel — side seam", dx + bot_w - 5.0, bone_clearance),
    ]
    piece = fc.Piece(
        "midriff_front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 12.0},
        notches=[fc.Notch("top", 0.5, "cradle centre"),
                 fc.Notch("seam_side", 0.5, "side panel match")],
        grainline=fc.Grainline(fc.P(top_w * 0.5, 10.0), fc.P(top_w * 0.5, MD - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Midriff panel — front (cut 2 pairs, boned)",
    )
    return piece


def build_midriff_side(seam_len, span):
    """Side midriff panel: its CF-side seam is built to the measured front side seam,
    so the panel ring balances; it too carries a boning channel."""
    # Build a quadrilateral whose left seam length equals `seam_len` exactly.
    top_w = span
    bot_w = span * max(0.74, min(1.0, WAIST_HALF / max(RIB_HALF, 1.0)))
    dx = top_w - bot_w
    # Solve the panel height so the slanted left seam measures exactly seam_len.
    h = math.sqrt(max(1.0, seam_len * seam_len - dx * dx))
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(dx + bot_w, 0.0), fc.P(dx, 0.0))]),
        fc.Edge("seam_front", [fc.Line(fc.P(dx, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(top_w, h))]),
        fc.Edge("seam_back", [fc.Line(fc.P(top_w, h), fc.P(dx + bot_w, 0.0))]),
    ]
    internals = [_bone_channel("bone channel — side seam", dx + bot_w - 5.0,
                               bone_clearance)]
    return fc.Piece(
        "midriff_side",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 12.0},
        notches=[fc.Notch("seam_front", 0.5, "front panel match"),
                 fc.Notch("seam_back", 0.5, "back wing match")],
        grainline=fc.Grainline(fc.P(top_w * 0.5, 10.0), fc.P(top_w * 0.5, h - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Midriff panel — side (cut 2 pairs, boned)",
    )


def build_back(seam_len, span, cup_side_len):
    """Back wing: full-depth on a longline, closing at a multi-row CB hook.

    Its front seam is built to the measured midriff side-back seam; the wing rises to
    a strap tab at the shoulder line and carries a CB boning channel either side of
    the hook tape (which is what stops a deep closure from folding).
    """
    h = math.sqrt(max(1.0, seam_len * seam_len - (span * 0.10) ** 2))
    top_h = h + cup_side_len
    edges = [
        fc.Edge("seam_front", [fc.Line(fc.P(span * 0.10, 0.0), fc.P(0.0, h))]),
        fc.Edge("side", [fc.Line(fc.P(0.0, h), fc.P(0.0, top_h))]),
        fc.Edge("strap_tab", [fc.Line(fc.P(0.0, top_h), fc.P(strap_width, top_h))]),
        fc.Edge("top", [fc.Bezier(fc.P(strap_width, top_h),
                                  fc.P(span * 0.42, top_h * 0.76),
                                  fc.P(span * 0.86, h * 0.62),
                                  fc.P(span, h * 0.52))]),
        fc.Edge("center_back", [fc.Line(fc.P(span, h * 0.52), fc.P(span, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(span, 0.0), fc.P(span * 0.10, 0.0))]),
    ]
    internals = [_bone_channel("bone channel — centre back", span - 6.0, bone_clearance)]
    piece = fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"top": 0.0, "hem": 12.0},
        notches=[fc.Notch("center_back", 0.5, "hook tape position"),
                 fc.Notch("seam_front", 0.5, "midriff side match")],
        grainline=fc.Grainline(fc.P(span * 0.5, 10.0), fc.P(span * 0.5, h * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back wing (cut 2 pairs, boned CB, hook closure)",
    )
    piece.internals = piece.internals + [
        _elastic_zone(piece.edge("top"), "wing elastic zone", 0.08, 0.92)]
    return piece


def build():
    pattern = fc.PatternSet("longline-bra")
    lower = build_cup_lower()
    upper = build_cup_upper(lower)
    cradle = build_cradle()
    front_run = cradle.edge("bottom").length()
    midriff_front = build_midriff_front(front_run)
    # The side panel's front seam is built to the front panel's measured side seam.
    side_seam_len = midriff_front.edge("seam_side").length()
    side_span = max(50.0, (RIB_HALF - front_run) * 0.55)
    midriff_side = build_midriff_side(side_seam_len, side_span)
    back_span = max(50.0, RIB_HALF - front_run - side_span)
    back = build_back(midriff_side.edge("seam_back").length(), back_span,
                      lower.edge("side").length() + upper.edge("side").length())

    picked = {"cup_lower": lower, "cup_upper": upper, "cradle": cradle,
              "midriff_front": midriff_front, "midriff_side": midriff_side, "back": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (lower, upper, cradle, midriff_front, midriff_side, back):
            pattern.add(piece)
        # The wire handshake (shared with the rest of the lane).
        pattern.declare_seam(("cup_lower", "mouth"), ("cradle", "wire_line"), tol=1.0)
        pattern.declare_seam(("cup_lower", "cup_seam"), ("cup_upper", "cup_seam"), tol=1.0)
        # The cradle sits on the midriff panel — this is what makes it a LONGLINE.
        pattern.declare_seam(("cradle", "bottom"), ("midriff_front", "top"), tol=1.0)
        # The boned panel ring: front -> side -> back wing.
        pattern.declare_seam(("midriff_front", "seam_side"),
                             ("midriff_side", "seam_front"), tol=1.0)
        pattern.declare_seam(("midriff_side", "seam_back"), ("back", "seam_front"), tol=1.0)
        # Side seam: the cup's outer rise joins the wing's upper side.
        pattern.declare_seam([("cup_lower", "side"), ("cup_upper", "side")],
                             ("back", "side"), tol=1.5)

    hem_ring = 2.0 * (midriff_front.edge("hem").length()
                      + midriff_side.edge("hem").length()
                      + back.edge("hem").length())
    neck_opening = 2.0 * upper.edge("neckline").length()
    channel_run = 2.0 * cradle.edge("wire_line").length()
    # Bone count: 2 in the front panel, 1 per side panel, 1 per back wing (x2 sides).
    bone_count = 2 * 2 + 2 * 1 + 2 * 1

    fabric_width = 1400.0
    area = (lower.area() * 4.0 + upper.area() * 4.0 + cradle.area() * 2.0
            + midriff_front.area() * 2.0 + midriff_side.area() * 2.0 + back.area() * 2.0)
    marker_len = area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "powernet + stable tricot (self + lining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"cups + cradle + midriff + wings at {fabric_width:.0f} mm width, 60% "
                 "marker. The midriff is cut in firm powernet, fully lined — a longline "
                 "carries its load on the panel, not on a narrow band."},
        {"item": "boning stays (Yantra4D boning-stay)", "qty": bone_count, "unit": "piece",
         "note": f"stay_length {CHANNEL_LEN:.1f} mm = midriff_depth {MD:.0f} mm minus "
                 f"2 x {bone_clearance:.0f} mm clearance, so the tips cannot work "
                 "through the hem or the wire line. The stay and its channel are the "
                 "Yantra4D solid (notion.hardware_ref -> boning-stay), never modelled "
                 "here; the drafted channels are marked at that exact length."},
        {"item": "underwire (Yantra4D bra-underwire)", "qty": 2, "unit": "piece",
         "note": f"one pair; chord {cup_width:.0f} mm, sweep {sweep_deg:.0f}°, solved "
                 f"run {WIRE_RUN:.1f} mm each. Referenced, not modelled."},
        {"item": "wire channel tape 12 mm", "qty": round(channel_run * 1.06),
         "unit": "mm_length", "note": f"two channels x {WIRE_RUN:.1f} mm + turn-under."},
        {"item": "hem + neckline elastic 10 mm",
         "qty": round(hem_ring * 0.94 + neck_opening * 0.85), "unit": "mm_length",
         "note": f"hem ring {hem_ring:.0f} mm x 0.94 (a longline hem grips lightly, it "
                 f"does not carry) + neckline {neck_opening:.0f} mm x 0.85."},
        {"item": "hook-and-eye tape (4 rows)", "qty": 1, "unit": "piece",
         "note": "a longline needs more rows than a bra — more length to hold shut. "
                 "Yantra4D hook-and-eye; boned either side of the tape."},
        {"item": "strap elastic + sliders/rings", "qty": 2, "unit": "set",
         "note": "Yantra4D bra-ring-slider; not modelled here."},
        {"item": "polyester thread + topstitch thread", "qty": 1, "unit": "set",
         "note": "bone channels are topstitched both sides before the panels join."},
    ]
    pattern.metadata = {
        "fc300_rank": 221, "family": "underwear_lounge", "fabric_hint": "powernet",
        "silhouette_note": "A bra continued down over the ribs into a boned midriff "
            "panel. The load is carried by the broad gripping panel rather than a "
            "narrow band, which is what a longline is for; the bones stop that panel "
            "rolling and collapsing.",
        "hardware": "boning via Yantra4D (notion.hardware_ref -> boning-stay); "
            "stay_length is derived as midriff_depth - 2*bone_clearance, and "
            "midriff_depth also drives the garment's midriff and channel interfaces — "
            "the dimensional handshake. Underwire + hook tape referenced separately.",
        "solver": {
            "midriff_depth_mm": round(MD, 1),
            "bone_clearance_mm": round(bone_clearance, 1),
            "channel_len_mm": round(CHANNEL_LEN, 2),
            "bone_count": bone_count,
            "wire_run_mm": round(WIRE_RUN, 2),
            "cradle_wire_line_mm": round(cradle.edge("wire_line").length(), 2),
            "note": "channel_len == stay_length: what is chalked is what is printed.",
        },
        "solved": {
            "rib_half_mm": round(RIB_HALF, 1),
            "waist_half_mm": round(WAIST_HALF, 1),
            "hem_ring_mm": round(hem_ring, 1),
            "bust_surplus_mm": round(SURPLUS, 1),
        },
        "closure": "centre-back hook-and-eye tape (4 rows), boned either side",
        "drafting": "Made to measure to underbust, bust and waist girths.",
    }
    return pattern


result = build()

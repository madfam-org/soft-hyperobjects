"""
Nursing Bra — Fashion Cabinet Garment Cartridge (FC-300 #225; y4d bra-ring-slider).

A bra whose cup OPENS. The whole design problem is that one requirement: the cup must
drop away for feeding and come back to a supportive position afterwards, one-handed,
repeatedly, without the band losing its grip in between. That constraint drives every
decision here:

  1. THE CUP IS SPLIT HORIZONTALLY into a drop cup (the part that falls) and a fixed
     sling (the part that stays). The sling is not decorative — it is what still holds
     the breast when the cup is open, and it is why a nursing bra is not just a bra
     with a clip on it.
  2. THE STRAP IS THE HINGE. The drop cup hangs from the strap, and the strap detaches
     at a RING at the cup apex via a SLIDER clip. Cup and strap are therefore joined by
     hardware, not by a seam — which is exactly the point/slot case: the ring and slider
     grip the strap through a loop, with no sewn flange to match an edge against.
  3. THE BAND IS UNTOUCHED BY THE OPENING. Dropping the cup must not slacken the band,
     so the band and cradle run continuously under both cup sections and the drop
     happens entirely above the wire line.

The DIMENSIONAL HANDSHAKE. `bra-ring-slider` is parameterised by `strap_w` (the strap
that threads it), `wire_d` (the ring's wire gauge) and `slider_h`. The garment's
`strap_w` drives the drafted strap piece's cut width AND the drafted strap tabs on both
the sling and the drop cup — it is the `strap_ring` interface — and the same number
sizes the hardware's loop. A strap wider than the ring will not thread; narrower and the
clip slips under load, which on a nursing bra means it opens when it should not.

`sling_hold_pct` records the honest number nobody prints: how much of the cup's support
the fixed sling still provides with the drop cup open.

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

underbust_girth = float(PARAM(lambda: underbust_girth, 800.0))
bust_girth   = float(PARAM(lambda: bust_girth, 1010.0))   # nursing bust runs fuller
cup_width    = float(PARAM(lambda: cup_width, 145.0))
sweep_deg    = float(PARAM(lambda: sweep_deg, 200.0))
cup_rise     = float(PARAM(lambda: cup_rise, 95.0))
sling_frac   = float(PARAM(lambda: sling_frac, 0.42))     # sling share of the cup rise
strap_w      = float(PARAM(lambda: strap_w, 19.0))        # wide: nursing bras carry more
band_height  = float(PARAM(lambda: band_height, 40.0))
cradle_height = float(PARAM(lambda: cradle_height, 26.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 12.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(600.0, min(underbust_girth, 1300.0))
bust_girth   = max(700.0, min(bust_girth, 1600.0))
cup_width    = max(100.0, min(cup_width, 220.0))
sweep_deg    = max(150.0, min(sweep_deg, 250.0))
cup_rise     = max(55.0, min(cup_rise, 180.0))
sling_frac   = max(0.25, min(sling_frac, 0.60))
strap_w      = max(10.0, min(strap_w, 32.0))
band_height  = max(25.0, min(band_height, 90.0))
cradle_height = max(14.0, min(cradle_height, 60.0))
negative_ease_pct = max(6.0, min(negative_ease_pct, 20.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# ── Support geometry ─────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_FINISHED = underbust_girth * NEG
BAND_HALF = BAND_FINISHED / 2.0
BH = band_height
CH = cradle_height
SURPLUS = max(30.0, (bust_girth - underbust_girth) / 2.0)
ELASTIC_ZONE = 8.0

# The split: the sling occupies the lower `sling_frac` of the cup rise, the drop cup
# the rest. The sling is the part that keeps holding when the cup is open.
SLING_H = cup_rise * sling_frac
DROP_H = cup_rise - SLING_H
# The honest support number: with the drop cup open, the sling still spans this share
# of the cup's height, which is roughly the share of the support it keeps.
SLING_HOLD_PCT = 100.0 * SLING_H / max(cup_rise, 1.0)

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
    """A circular arc polyline of a GIVEN run and sagitta/run ratio."""
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


# ── Pieces ───────────────────────────────────────────────────────────────────
def build_sling():
    """The FIXED sling: the lower cup section that stays put when the cup drops.

    Its mouth is the solved wire arc (it sews into the cradle like any lower cup), and
    its top edge is where the drop cup overlaps. The outer corner carries a strap tab —
    the sling is anchored to the strap too, which is what stops it collapsing when the
    drop cup is released.
    """
    arc = _wire_arc_points(0.0, 0.0)
    left, right = arc[0], arc[-1]
    top_pts = _arc_of_run(cup_width * 1.04, 0.09)
    span = top_pts[-1].x - top_pts[0].x
    x_off = left.x + (cup_width - span) / 2.0
    top_pts = [fc.P(p.x + x_off, p.y + SLING_H) for p in top_pts]
    tab_top = fc.P(top_pts[-1].x, top_pts[-1].y + strap_w)
    edges = [
        _poly_edge("mouth", arc),
        fc.Edge("side", [fc.Line(right, top_pts[-1])]),
        fc.Edge("strap_tab", [fc.Line(top_pts[-1], tab_top)]),
        fc.Edge("upper", [fc.Bezier(tab_top,
                                    fc.P(top_pts[-1].x * 0.66, top_pts[-1].y + strap_w * 0.5),
                                    fc.P(top_pts[0].x + span * 0.28, top_pts[0].y + 4.0),
                                    top_pts[0])]),
        fc.Edge("center_front", [fc.Line(top_pts[0], left)]),
    ]
    piece = fc.Piece(
        "sling",
        edges,
        seam_allowance=seam_allowance,
        allowances={"upper": 0.0},   # elastic-finished free edge
        notches=[fc.Notch("mouth", 0.5, "cradle apex match"),
                 fc.Notch("strap_tab", 0.5, "sling strap anchor")],
        grainline=fc.Grainline(fc.P(left.x + cup_width * 0.5, -WIRE_RISE * 0.35),
                               fc.P(left.x + cup_width * 0.5, SLING_H * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sling — fixed lower cup (cut 2 pairs, holds when open)",
    )
    piece.internals = [_elastic_zone(piece.edge("upper"), "sling edge elastic zone",
                                     0.10, 0.90)]
    return piece


def build_drop_cup():
    """The DROP CUP: hangs from the strap through a ring, falls away for feeding.

    Its lower edge overlaps the sling (it is NOT sewn to it — that is the whole point),
    so it is declared as a free finished edge. The apex corner carries the ring tab: a
    short edge, `strap_w` wide, that the ring loop grips. Cup and strap are joined by
    HARDWARE, not by a seam.
    """
    run = cup_width * 1.06
    bottom = _arc_of_run(run, 0.09)
    left, right = bottom[0], bottom[-1]
    ring_in = fc.P(right.x - strap_w, right.y + DROP_H)
    ring_out = fc.P(right.x, right.y + DROP_H)
    top_l = fc.P(left.x, left.y + DROP_H * 0.62)
    edges = [
        _poly_edge("lower", bottom),
        fc.Edge("side", [fc.Line(right, ring_out)]),
        fc.Edge("ring_tab", [fc.Line(ring_out, ring_in)]),
        fc.Edge("neckline", [fc.Bezier(ring_in,
                                       fc.P(left.x + (ring_in.x - left.x) * 0.58,
                                            ring_in.y - DROP_H * 0.14),
                                       fc.P(left.x + (ring_in.x - left.x) * 0.22,
                                            top_l.y + DROP_H * 0.10),
                                       top_l)]),
        fc.Edge("center_front", [fc.Line(top_l, left)]),
    ]
    piece = fc.Piece(
        "drop_cup",
        edges,
        seam_allowance=seam_allowance,
        # BOTH the lower edge and the neckline are FREE finished edges: the drop cup is
        # not sewn to the sling, it overlaps it and falls away.
        allowances={"lower": 0.0, "neckline": 0.0},
        notches=[fc.Notch("ring_tab", 0.5, "ring position — clip here"),
                 fc.Notch("lower", 0.5, "overlap the sling to this notch")],
        grainline=fc.Grainline(fc.P(right.x * 0.5, DROP_H * 0.12),
                               fc.P(right.x * 0.5, DROP_H * 0.78)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Drop cup (cut 2 pairs, hangs from the ring)",
    )
    piece.internals = [
        _elastic_zone(piece.edge("lower"), "drop-cup lower elastic zone", 0.08, 0.92),
        _elastic_zone(piece.edge("neckline"), "neckline elastic zone", 0.08, 0.92),
    ]
    return piece


def build_cradle():
    """The cradle: `wire_line` IS the solved underwire arc. Continuous under both cup
    sections — dropping the cup must never slacken the band."""
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
    """Underband, cut 2 mirror (CF -> CB hook). Wide and firm: a nursing band is worn
    for months and must not be the part that gives up."""
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
        fc.Edge("strap_tab", [fc.Line(fc.P(0.0, wing_h), fc.P(strap_w, wing_h))]),
        fc.Edge("top", [fc.Bezier(fc.P(strap_w, wing_h),
                                  fc.P(x_end * 0.40, wing_h * 0.72),
                                  fc.P(x_end * 0.84, BH + 10.0),
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


def build_strap():
    """The nursing strap: wide, and cut to `strap_w` — the SAME number the ring and
    slider receive. Both ends are hardware spans (ring at the cup, slider at the back),
    so neither is a sewn seam."""
    length = cup_rise + 260.0
    edges = [
        fc.Edge("end_ring", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, strap_w))]),
        fc.Edge("strap_edge", [fc.Line(fc.P(0.0, strap_w), fc.P(length, strap_w))]),
        fc.Edge("end_slider", [fc.Line(fc.P(length, strap_w), fc.P(length, 0.0))]),
        fc.Edge("strap_edge_b", [fc.Line(fc.P(length, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap",
        edges,
        seam_allowance=0.0,
        notches=[fc.Notch("strap_edge", 0.55, "slider position (adjustable)"),
                 fc.Notch("end_ring", 0.5, "ring — the drop-cup hinge")],
        grainline=fc.Grainline(fc.P(length * 0.2, strap_w / 2.0),
                               fc.P(length * 0.8, strap_w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Strap (cut 2, ring at the cup end)",
    )


def build():
    pattern = fc.PatternSet("nursing-bra")
    sling = build_sling()
    drop = build_drop_cup()
    cradle = build_cradle()
    front_span = cradle.edge("bottom").length()
    band = build_band(front_span)
    back_span = max(40.0, BAND_HALF - front_span)
    back = build_back(sling.edge("side").length() + drop.edge("side").length(), back_span)
    strap = build_strap()

    picked = {"sling": sling, "drop_cup": drop, "cradle": cradle, "band": band,
              "back": back, "strap": strap}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (sling, drop, cradle, band, back, strap):
            pattern.add(piece)
        # The wire handshake: the sling's mouth is the cradle's wire line.
        pattern.declare_seam(("sling", "mouth"), ("cradle", "wire_line"), tol=1.0)
        pattern.declare_seam(("cradle", "bottom"), ("band", "top_cradle"), tol=1.0)
        pattern.declare_seam(("back", "bottom"), ("band", "top_back"), tol=1.0)
        # Side seam: sling + drop-cup sides join the wing side.
        pattern.declare_seam([("sling", "side"), ("drop_cup", "side")],
                             ("back", "side"), tol=1.5)
        # The strap's two ends are hardware spans; both must be the SAME width as the
        # tabs they clip to, which is `strap_w` everywhere.
        pattern.declare_seam(("strap", "end_ring"), ("drop_cup", "ring_tab"), tol=0.5)
        pattern.declare_seam(("strap", "end_slider"), ("back", "strap_tab"), tol=0.5)
        # The sling is anchored to the strap too — it must not collapse when the cup opens.
        pattern.declare_seam(("sling", "strap_tab"), ("strap", "end_ring"), tol=0.5)
        # NOTE: drop_cup.lower is deliberately NOT seamed to sling.upper. The cup drops;
        # sewing those edges together would defeat the entire garment.

    band_opening = 2.0 * band.edge("lower").length()
    neck_opening = 2.0 * drop.edge("neckline").length()
    drop_edge = 2.0 * drop.edge("lower").length()
    sling_edge = 2.0 * sling.edge("upper").length()
    arm_opening = 2.0 * back.edge("top").length()
    channel_run = 2.0 * cradle.edge("wire_line").length()

    fabric_width = 1500.0
    area = (sling.area() * 4.0 + drop.area() * 4.0 + cradle.area() * 2.0
            + band.area() * 2.0 + back.area() * 2.0)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "soft stretch tricot + cotton cup lining",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"cups + cradle + band + wings at {fabric_width:.0f} mm width, 55% "
                 "marker. Line the sling and drop cup in COTTON, not synthetic — this "
                 "garment is worn against skin for months at a stretch."},
        {"item": "nursing rings + sliders (Yantra4D bra-ring-slider)", "qty": 2,
         "unit": "set",
         "note": f"one ring + slider per strap, sized to strap_w {strap_w:.0f} mm. The "
                 "ring at the cup end IS the drop-cup hinge: the cup hangs from it and "
                 "unclips one-handed. Hardware is the Yantra4D solid "
                 "(notion.hardware_ref -> bra-ring-slider), never modelled here; the "
                 "strap and both tabs are cut to exactly the width its loop expects."},
        {"item": "underwire (Yantra4D bra-underwire)", "qty": 2, "unit": "piece",
         "note": f"chord {cup_width:.0f} mm, sweep {sweep_deg:.0f}°, solved run "
                 f"{WIRE_RUN:.1f} mm. Referenced, not modelled. Flexible or wire-free "
                 "variants: omit and rely on the cradle seam alone."},
        {"item": "wire channel tape 12 mm", "qty": round(channel_run * 1.06),
         "unit": "mm_length", "note": f"two channels x {WIRE_RUN:.1f} mm + turn-under."},
        {"item": f"strap elastic {strap_w:.0f} mm",
         "qty": round(2.0 * strap.edge("strap_edge").length() * 1.2), "unit": "mm_length",
         "note": "two straps + fold-backs at ring and slider. Cut to the SAME width as "
                 "the ring loop, or the clip slips under load — on a nursing bra that "
                 "means it opens when it should not."},
        {"item": "band elastic (plush-back) 15 mm", "qty": round(band_opening * 0.94),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm x 0.94. Wider and softer than a "
                 "regular bra's — worn for months, over a changing ribcage."},
        {"item": "edge elastic (soft picot) 8 mm",
         "qty": round((neck_opening + drop_edge + sling_edge + arm_opening) * 0.88),
         "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} + drop-cup lower {drop_edge:.0f} + sling "
                 f"upper {sling_edge:.0f} + wing top {arm_opening:.0f} mm at 0.88. The "
                 "drop-cup lower edge and the sling upper edge are BOTH finished free "
                 "edges — they overlap, they are never sewn together."},
        {"item": "hook-and-eye bra back (4x3)", "qty": 1, "unit": "piece",
         "note": "extra rows: a nursing ribcage changes size over months, and the band "
                 "must keep gripping across that range. Yantra4D hook-and-eye."},
        {"item": "polyester stretch thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "bar-tack the ring tabs hard — they take the whole cup's load, "
                 "repeatedly, one-handed."},
    ]
    pattern.metadata = {
        "fc300_rank": 225, "family": "underwear_lounge", "fabric_hint": "tricot-nylon",
        "silhouette_note": "A drop-cup nursing bra: a FIXED SLING that keeps holding "
            "when the cup is open, a drop cup hanging from a ring at the strap, and a "
            "band and cradle that run continuously underneath so opening the cup never "
            "slackens the support.",
        "hardware": "rings and sliders via Yantra4D (notion.hardware_ref -> "
            "bra-ring-slider), point/slot: the ring loop grips the strap, there is no "
            "sewn flange. strap_w drives the strap, both strap tabs and the ring loop — "
            "one number. Underwire + hook tape referenced separately.",
        "opening": {
            "sling_hold_pct": round(SLING_HOLD_PCT, 1),
            "sling_height_mm": round(SLING_H, 1),
            "drop_height_mm": round(DROP_H, 1),
            "note": "with the drop cup released the sling still spans this share of the "
                    "cup height — the support number a nursing bra label never prints. "
                    "Raise sling_frac for more hold when open, lower it for more access.",
        },
        "solver": {
            "strap_w_mm": round(strap_w, 1),
            "wire_run_mm": round(WIRE_RUN, 2),
            "cradle_wire_line_mm": round(cradle.edge("wire_line").length(), 2),
            "sling_mouth_mm": round(sling.edge("mouth").length(), 2),
            "note": "strap_w is the strap's cut width, both tab widths AND the ring "
                    "loop width — one number reaching every joint.",
        },
        "solved": {
            "band_finished_mm": round(BAND_FINISHED, 1),
            "band_opening_mm": round(band_opening, 1),
            "bust_surplus_mm": round(SURPLUS, 1),
        },
        "closure": "centre-back hook-and-eye (4 cols x 3 rows) + drop-cup rings",
        "drafting": "Made to measure to underbust and bust girths; the cup splits "
            "horizontally into a fixed sling and a drop cup.",
    }
    return pattern


result = build()

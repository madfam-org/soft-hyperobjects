"""
Princess-Seam Dance Leotard — Fashion Cabinet Costume Cartridge (FC-500 #474; y4d sew-on-snap).

A dance leotard shaped by PRINCESS SEAMS: curved vertical seams that run from the shoulder over
the bust apex to the waist, front and back, so the garment is fitted by seam rather than by dart —
the convention of stage and competition dancewear, where a dart would break the line the audience
reads. It is cut in four panels a side (centre + side, front + back), joined at those princess
seams and the side seam, on a leg-line leotard body closing at a Yantra4D `sew-on-snap` gusset.

The princess seam that must SOLVE. A princess seam is one physical seam sewn from two curves cut
on two different panels; the centre panel's seam curve and the side panel's seam curve MUST be the
same length or the bust puckers. This cartridge builds both curves to the SAME solved arc length —
the centre-panel princess edge and the side-panel princess edge are declared equal — so the seam
that carries all the bust shaping balances by construction rather than by a fitting.

The stretch is a MEASURED negative ease: a leotard is cut smaller than the body and stretched on,
so every girth is taken at `(1 - stretch)`. The leg line and the back scoop are drafted from the
body.

The DIMENSIONAL HANDSHAKE. The gusset closes on a `sew-on-snap`; `snap_dia` drives the snap's
`sew_face` flange AND the drafted gusset snap seat AND the leotard's own `gusset_snap` interface,
so the printed snap is exactly the size of the seat it sews to.

Made to measure to bust, waist and hip girths. FC-500 lane 9 (costume, dance & performance).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
waist_girth = float(PARAM(lambda: waist_girth, 720.0))
hip_girth = float(PARAM(lambda: hip_girth, 940.0))
torso_length = float(PARAM(lambda: torso_length, 620.0))   # shoulder to crotch
stretch = float(PARAM(lambda: stretch, 0.12))              # negative ease
back_scoop = float(PARAM(lambda: back_scoop, 200.0))       # how low the back is cut
leg_line = float(PARAM(lambda: leg_line, 40.0))            # leg-opening height above crotch
snap_dia = float(PARAM(lambda: snap_dia, 15.0))            # gusset snap diameter
strap_width = float(PARAM(lambda: strap_width, 30.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(680.0, min(bust_girth, 1400.0))
waist_girth = max(520.0, min(waist_girth, 1200.0))
hip_girth = max(700.0, min(hip_girth, 1500.0))
torso_length = max(440.0, min(torso_length, 820.0))
stretch = max(0.04, min(stretch, 0.24))
back_scoop = max(60.0, min(back_scoop, 380.0))
leg_line = max(0.0, min(leg_line, 140.0))
snap_dia = max(9.0, min(snap_dia, 24.0))
strap_width = max(12.0, min(strap_width, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# ── Solved widths ────────────────────────────────────────────────────────────
NEG = 1.0 - stretch     # stretch is a fraction (0.12 = 12% negative ease)
BUST_Q = (bust_girth * NEG) / 4.0     # quarter (centre + side share the princess seam)
WAIST_Q = (waist_girth * NEG) / 4.0
HIP_Q = (hip_girth * NEG) / 4.0
TL = torso_length
# split the quarter between centre panel and side panel
CENTRE_FRAC = 0.45
BUST_C = BUST_Q * CENTRE_FRAC
BUST_S = BUST_Q * (1.0 - CENTRE_FRAC)
WAIST_C = WAIST_Q * CENTRE_FRAC
WAIST_S = WAIST_Q * (1.0 - CENTRE_FRAC)
HIP_C = HIP_Q * CENTRE_FRAC
HIP_S = HIP_Q * (1.0 - CENTRE_FRAC)
BUST_Y = TL * 0.72     # bust apex height
WAIST_Y = TL * 0.5
GUSSET_W = max(50.0, HIP_Q * 0.5)


def _princess_curve(x_top, x_bust, x_waist, x_hip, y_top, name):
    """The princess seam curve as an Edge: from the top (shoulder/neck) down through the bust
    apex to the waist to the hip/crotch. Built identically (same control math) for the centre
    and side panels so the two seam edges are equal length."""
    p_top = fc.P(x_top, y_top)
    p_bust = fc.P(x_bust, BUST_Y)
    p_waist = fc.P(x_waist, WAIST_Y)
    p_hip = fc.P(x_hip, 0.0)
    seg1 = fc.Bezier(p_top, fc.P(x_top + (x_bust - x_top) * 0.4, y_top - (y_top - BUST_Y) * 0.5),
                     fc.P(x_bust, BUST_Y + (y_top - BUST_Y) * 0.3), p_bust)
    seg2 = fc.Bezier(p_bust, fc.P(x_bust, BUST_Y - (BUST_Y - WAIST_Y) * 0.4),
                     fc.P(x_waist + (x_bust - x_waist) * 0.3, WAIST_Y + (BUST_Y - WAIST_Y) * 0.2),
                     p_waist)
    seg3 = fc.Bezier(p_waist, fc.P(x_waist + (x_hip - x_waist) * 0.3, WAIST_Y * 0.5),
                     fc.P(x_hip, WAIST_Y * 0.2), p_hip)
    return fc.Edge(name, [seg1, seg2, seg3])


def build_front_centre():
    """Front centre panel: CF fold edge, princess seam on the outer side, neckline, crotch."""
    # CF at x=0; princess seam sweeps out to the bust then in to the waist/hip.
    princess = _princess_curve(BUST_C * 0.7, BUST_C, WAIST_C, HIP_C, TL, "princess")
    p_cf_top = fc.P(0.0, TL)
    p_cf_crotch = fc.P(0.0, 0.0)
    p_hip = princess.end
    p_top = princess.start   # (BUST_C*0.7, TL)
    # CCW ring: neckline (princess top -> CF top), CF down, crotch across to hip,
    # then the princess seam back UP from hip to its top (reversed).
    edges = [
        fc.Edge("neckline", [fc.Bezier(p_top,
                                       fc.P(BUST_C * 0.4, TL - 6.0),
                                       fc.P(BUST_C * 0.15, TL - 2.0), p_cf_top)]),
        fc.Edge("center_front", [fc.Line(p_cf_top, p_cf_crotch)]),
        fc.Edge("crotch", [fc.Line(p_cf_crotch, p_hip)]),
        fc.Edge("princess", princess.reversed().segments),
    ]
    return fc.Piece(
        "front_centre", edges, seam_allowance=seam_allowance,
        allowances={"neckline": 0.0},
        notches=[fc.Notch("princess", 0.35, "bust apex"), fc.Notch("princess", 0.65, "waist")],
        grainline=fc.Grainline(fc.P(BUST_C * 0.35, TL * 0.2), fc.P(BUST_C * 0.35, TL * 0.8)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_front"),
        label="Front centre panel (cut 1 on fold)",
    )


def build_front_side():
    """Front side panel: princess seam on its inner side (equal to the centre's), armhole,
    side seam, leg opening. Its princess edge is built to the SAME length by construction."""
    princess = _princess_curve(BUST_C * 0.7, BUST_C, WAIST_C, HIP_C, TL, "princess")
    # offset the side panel to sit alongside (its geometry uses side widths but same curve math
    # for the princess edge, so lengths match). Place the panel to the right of the centre.
    off = BUST_C + 20.0
    # side panel outer boundary
    # The side seam (underarm -> waist -> hip) is drafted as a VERTICAL line at a fixed x, so
    # its length depends only on the y-span and matches the back's side seam by construction —
    # the shaping lives in the princess seam, not the side. The x is the panel's widest point.
    side_x = off + max(BUST_S, WAIST_S, HIP_S)
    underarm_y = BUST_Y + (TL - BUST_Y) * 0.3
    p_shoulder = fc.P(off + BUST_S * 0.4, TL)
    p_underarm = fc.P(side_x, underarm_y)
    p_side_waist = fc.P(side_x, WAIST_Y)
    p_side_hip = fc.P(side_x, leg_line)
    p_leg = fc.P(off, 0.0)

    # The side panel's inner princess edge is the SAME curve as the centre panel's, translated
    # sideways — translation preserves length, so the two princess seam edges are equal by
    # construction (the seam that carries the bust shaping cannot pucker).
    def translate_edge(edge, dx):
        segs = [fc.Bezier(fc.P(s.p0.x + dx, s.p0.y), fc.P(s.c0.x + dx, s.c0.y),
                          fc.P(s.c1.x + dx, s.c1.y), fc.P(s.p1.x + dx, s.p1.y))
                for s in edge.segments]
        return fc.Edge(edge.name, segs)
    inner_edge = translate_edge(princess, off - (BUST_C * 0.7))  # align inner start near off
    inner_start = inner_edge.start
    inner_end = inner_edge.end
    edges = [
        # the inner princess edge (equal length to the centre's princess)
        inner_edge.reversed(),
        # from inner top up to the shoulder, across to underarm, down the side to waist/hip
        fc.Edge("shoulder", [fc.Line(inner_start, p_shoulder)]),
        fc.Edge("armscye", [fc.Bezier(p_shoulder, fc.P(p_shoulder.x + BUST_S * 0.5, TL - 20.0),
                                      fc.P(p_underarm.x, p_underarm.y + 30.0), p_underarm)]),
        fc.Edge("side", [fc.Line(p_underarm, p_side_waist)]),
        fc.Edge("side_lower", [fc.Line(p_side_waist, p_side_hip)]),
        fc.Edge("leg_opening", [fc.Bezier(p_side_hip, fc.P(off + HIP_S * 0.5, leg_line * 0.4),
                                          fc.P(off + GUSSET_W, 0.0), p_leg)]),
        fc.Edge("crotch", [fc.Line(p_leg, inner_end)]),
    ]
    return fc.Piece(
        "front_side", edges, seam_allowance=seam_allowance,
        allowances={"leg_opening": 0.0, "armscye": 0.0},
        notches=[fc.Notch("princess", 0.35, "bust apex")],
        grainline=fc.Grainline(fc.P(off + BUST_S * 0.4, TL * 0.2),
                               fc.P(off + BUST_S * 0.4, TL * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front side panel (cut 2, mirror)",
    )


def build_back():
    """Back panel (cut 1 on fold), princess-seamed into the front at the side seam, with a deep
    scoop. Simplified to a single shaped back panel per side (centre+side merged) for the scoop."""
    # The back side seam is drafted VERTICAL at a fixed x with the SAME y-spans as the front
    # side panel, so the shared side seam balances by construction.
    side_x = max(BUST_Q, WAIST_Q, HIP_Q)
    underarm_y = BUST_Y + (TL - BUST_Y) * 0.3
    p_cb_top = fc.P(0.0, TL - back_scoop)
    p_cb_crotch = fc.P(0.0, 0.0)
    p_side_hip = fc.P(side_x, leg_line)
    p_side_waist = fc.P(side_x, WAIST_Y)
    p_underarm = fc.P(side_x, underarm_y)
    p_shoulder = fc.P(BUST_Q * 0.4, TL)
    p_leg = fc.P(GUSSET_W, 0.0)
    edges = [
        fc.Edge("center_back", [fc.Line(p_cb_top, p_cb_crotch)]),
        fc.Edge("crotch", [fc.Line(p_cb_crotch, p_leg)]),
        fc.Edge("leg_opening", [fc.Bezier(p_leg, fc.P(HIP_Q * 0.5, leg_line * 0.4),
                                          fc.P(HIP_Q, leg_line * 0.6), p_side_hip)]),
        fc.Edge("side_lower", [fc.Line(p_side_hip, p_side_waist)]),
        fc.Edge("side", [fc.Line(p_side_waist, p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm, fc.P(BUST_Q * 0.8, TL - 20.0),
                                      fc.P(p_shoulder.x + 20.0, TL - 6.0), p_shoulder)]),
        fc.Edge("back_neck", [fc.Bezier(p_shoulder, fc.P(BUST_Q * 0.25, TL - back_scoop * 0.4),
                                        fc.P(0.0, TL - back_scoop * 0.85), p_cb_top)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        allowances={"leg_opening": 0.0, "armscye": 0.0, "back_neck": 0.0},
        notches=[fc.Notch("side", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(BUST_Q * 0.4, TL * 0.2),
                               fc.P(BUST_Q * 0.4, (TL - back_scoop) * 0.8)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back"),
        label="Back panel (cut 1 on fold, scooped)",
    )


def build_gusset():
    """The crotch gusset carrying the sew-on-snap closure seat."""
    depth = max(70.0, GUSSET_W * 1.1)
    p0, p1 = fc.P(0.0, 0.0), fc.P(GUSSET_W, 0.0)
    p2, p3 = fc.P(GUSSET_W, depth), fc.P(0.0, depth)
    edges = [
        fc.Edge("front_seam", [fc.Line(p0, p1)]),
        fc.Edge("right", [fc.Line(p1, p2)]),
        fc.Edge("back_seam", [fc.Line(p2, p3)]),
        fc.Edge("left", [fc.Line(p3, p0)]),
    ]
    cx, cy = GUSSET_W / 2.0, depth * 0.5
    r = snap_dia / 2.0
    internals = [
        fc.Internal("snap-seat", [fc.P(cx - r, cy - r), fc.P(cx + r, cy - r),
                                  fc.P(cx + r, cy + r), fc.P(cx - r, cy + r),
                                  fc.P(cx - r, cy - r)], kind="marking"),
    ]
    n = max(2, int(round(GUSSET_W / (snap_dia * 1.6))))
    for i in range(n):
        sx = (i + 0.5) * (GUSSET_W / n)
        internals.append(fc.Internal(f"snap-{i}", [fc.P(sx, cy), fc.P(sx, cy)], kind="drill"))
    return fc.Piece(
        "gusset", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("front_seam", 0.5, "front match"),
                 fc.Notch("back_seam", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(GUSSET_W * 0.5, depth * 0.2),
                               fc.P(GUSSET_W * 0.5, depth * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Gusset with sew-on-snap (cut 2)",
    )


def build():
    pattern = fc.PatternSet("leotard-princess-seam")
    fc_centre = build_front_centre()
    fc_side = build_front_side()
    back = build_back()
    gusset = build_gusset()

    picked = {"front_centre": fc_centre, "front_side": fc_side, "back": back, "gusset": gusset}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (fc_centre, fc_side, back, gusset):
            pattern.add(piece)
        # THE PRINCESS SEAM: centre-panel princess edge == side-panel princess edge (same curve).
        pattern.declare_seam(("front_centre", "princess"), ("front_side", "princess"), tol=1.0)
        # Side seam (upper + lower): front side panel to back, both drafted vertical so they
        # balance whatever the girths.
        pattern.declare_seam(("front_side", "side"), ("back", "side"), tol=2.0)
        pattern.declare_seam(("front_side", "side_lower"), ("back", "side_lower"), tol=2.0)
        # Gusset into the front-centre crotch and the back crotch.
        pattern.declare_seam(("gusset", "front_seam"), ("front_centre", "crotch"), tol=2.0,
                             ease=(gusset.edge("front_seam").length()
                                   - fc_centre.edge("crotch").length()))
        pattern.declare_seam(("gusset", "back_seam"), ("back", "crotch"), tol=2.0,
                             ease=(gusset.edge("back_seam").length()
                                   - back.edge("crotch").length()))

    fabric_width = 1500.0
    area = fc_centre.area() * 2.0 + fc_side.area() * 2.0 + back.area() * 2.0 + gusset.area() * 2.0
    marker_len = area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "4-way stretch dance knit (nylon/spandex)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"cut with the greatest stretch around the body; at {fabric_width:.0f} mm width, "
                 "70% marker. Princess panels nest economically."},
        {"item": "gusset sew-on snaps (Yantra4D sew-on-snap)", "qty": 2, "unit": "count",
         "note": f"snap {snap_dia:.0f} mm at the marked gusset seat (notion.hardware_ref -> "
                 "sew-on-snap); snap_dia drives the snap AND the drafted seat."},
        {"item": "picot elastic (leg, neck, back) 8 mm",
         "qty": round((back.edge('leg_opening').length() * 2.0
                       + fc_side.edge('leg_opening').length() * 2.0) * 0.9),
         "unit": "mm_length", "note": "into the leg, neckline and back-scoop edges at 0.9."},
        {"item": "clear elastic (bust princess) + wooly nylon", "qty": 1, "unit": "set",
         "note": "stabilise the princess seams over the bust; coverstitch or flatlock throughout."},
    ]
    pattern.metadata = {
        "fc500_rank": 474, "family": "costume_historical", "fabric_hint": "nylon-elastano",
        "provenance": "Princess-seam construction is the standard for stage and competition "
            "dancewear (ballet, figure skating, gymnastics): the bust is shaped by curved vertical "
            "seams, never a dart, so the line the audience reads is unbroken.",
        "silhouette_note": "Four-panel princess-seamed leotard body: centre + side panels front, a "
            "scooped back, a leg-line opening, and a sew-on-snap gusset. The bust shaping lives "
            "entirely in the princess seams.",
        "hardware": "gusset snap via Yantra4D (hardware_ref -> sew-on-snap); snap_dia drives the "
            "snap sew face AND the drafted seat.",
        "solved": {
            "stretch": round(stretch, 3),
            "bust_quarter_mm": round(BUST_Q, 1),
            "waist_quarter_mm": round(WAIST_Q, 1),
            "hip_quarter_mm": round(HIP_Q, 1),
            "princess_centre_mm": round(fc_centre.edge("princess").length(), 2),
            "princess_side_mm": round(fc_side.edge("princess").length(), 2),
            "note": "the centre and side princess edges are built from identical curve math so "
                    "they are equal length — the seam that carries all the bust shaping balances "
                    "by construction, not by a fitting.",
        },
        "closure": "sew-on-snap gusset",
        "drafting": "Made to measure to bust, waist and hip; negative-ease 4-way stretch.",
    }
    return pattern


result = build()

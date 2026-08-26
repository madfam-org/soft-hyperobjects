"""
Structured one-piece swimsuit — Fashion Cabinet Cartridge (FC-400 #389; y4d bra-ring-slider).

A STRUCTURED one-piece maillot in swim-lycra: a full-torso swimsuit with a built-in shelf
bra and ADJUSTABLE ring-and-slider straps, as distinct from the FC-100 pull-on maillot (#54,
no hardware). The structure is the point of this rank: a swimsuit that actually supports needs
an inner shelf bra and straps a wearer can tighten to their own shoulder height, and both are
drawn here.

Three real decisions:

  1. THE STRAPS ADJUST — THAT IS THE STRUCTURE. A pull-on maillot's straps are a fixed loop;
     this one's run from the back, through a RING at the front bust line, over the shoulder,
     and back through a SLIDER, so the wearer sets the height and the shelf bra sits where
     their bust is. `strap_w` drives BOTH the drafted strap's cut width AND the ring/slider
     channel — the dimensional handshake for this lane. Adjustable straps are what let one
     drafted suit fit a range of torso lengths.

  2. THE SHELF BRA IS A REAL INNER LAYER. A separate lined front shelf, gathered to the
     underbust line and finished with elastic, gives support the outer layer alone cannot.
     Its underbust ring is solved from the underbust girth at negative ease.

  3. THE LEG IS A HIGH-CUT OPENING ON A GUSSET. Front and back join at the side seams and at
     a lined gusset; the leg openings are high-cut curves finished with elastic, and there is
     no inseam. The whole suit is negative-ease so the lycra grips.

Pieces: front, back, shelf (inner bra), gusset, strap. Made to measure to bust, underbust,
waist, hip girths and the shoulder-to-crotch length.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
underbust_girth = float(PARAM(lambda: underbust_girth, 780.0))
waist_girth = float(PARAM(lambda: waist_girth, 740.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
shoulder_to_crotch = float(PARAM(lambda: shoulder_to_crotch, 680.0))
shelf_rise = float(PARAM(lambda: shelf_rise, 150.0))       # underbust to shelf top
leg_height = float(PARAM(lambda: leg_height, 120.0))       # how high the leg is cut
strap_w = float(PARAM(lambda: strap_w, 22.0))
neck_scoop = float(PARAM(lambda: neck_scoop, 110.0))
gusset_w = float(PARAM(lambda: gusset_w, 80.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 10.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1400.0))
underbust_girth = max(600.0, min(underbust_girth, 1250.0))
waist_girth = max(560.0, min(waist_girth, 1300.0))
hip_girth = max(700.0, min(hip_girth, 1600.0))
shoulder_to_crotch = max(520.0, min(shoulder_to_crotch, 920.0))
shelf_rise = max(60.0, min(shelf_rise, 300.0))
leg_height = max(40.0, min(leg_height, 260.0))
strap_w = max(12.0, min(strap_w, 45.0))
neck_scoop = max(40.0, min(neck_scoop, 240.0))
gusset_w = max(40.0, min(gusset_w, 150.0))
negative_ease_pct = max(4.0, min(negative_ease_pct, 20.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

TORSO_H = shoulder_to_crotch
neck_scoop = min(neck_scoop, TORSO_H * 0.4)
leg_height = min(leg_height, TORSO_H * 0.4)
shelf_rise = min(shelf_rise, TORSO_H * 0.55)

# ── The negative-ease solver ─────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BUST_FIN = bust_girth * NEG
UNDERBUST_FIN = underbust_girth * NEG
HIP_FIN = hip_girth * NEG
WIDEST = max(BUST_FIN, HIP_FIN)
PANEL_W = WIDEST / 2.0
SHELF_UNDERBUST = UNDERBUST_FIN / 2.0    # shelf underbust ring half
HIP_Y = TORSO_H * 0.28
STRAP_EDGE_LEN = TORSO_H * 0.6 + 200.0   # strap edge length (set precisely in build())


def _torso(name, neck, label):
    """Front or back torso panel: shoulder line to the crotch flat, straps as separate
    ring-slider pieces (so no strap is cut in one here — the top edges are the neckline and
    the back edge). CCW around: left leg opening -> left side -> left shoulder point ->
    neckline -> right shoulder point -> right side -> right leg opening -> crotch flat.
    """
    w = PANEL_W
    cx = w / 2.0
    top = TORSO_H
    g = gusset_w / 2.0
    sh_in = min(w * 0.30, w * 0.42)
    # The armhole/side-seam top is a FIXED height on both panels (independent of the neck
    # scoop) so front and back side seams are congruent. The neck scoop only lifts the
    # neckline between the shoulder points; the shoulder points stay at ARM_TOP.
    ARM_TOP = top - TORSO_H * 0.14
    crotch_l = fc.P(cx - g, 0.0)
    crotch_r = fc.P(cx + g, 0.0)
    side_bot_l = fc.P(0.0, leg_height)
    side_bot_r = fc.P(w, leg_height)
    edges = [
        fc.Edge("leg_opening_l", [fc.Bezier(crotch_l,
                                            fc.P((cx - g) * 0.5, leg_height * 0.25),
                                            fc.P(w * 0.05, leg_height * 0.7),
                                            side_bot_l)]),
        fc.Edge("side_seam_l", [fc.Line(side_bot_l, fc.P(0.0, ARM_TOP))]),
        fc.Edge("shoulder_l", [fc.Bezier(fc.P(0.0, ARM_TOP),
                                         fc.P(w * 0.08, ARM_TOP + (top - ARM_TOP) * 0.6),
                                         fc.P(sh_in * 0.7, top - 6.0),
                                         fc.P(sh_in, top))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(sh_in, top),
                                       fc.P(cx - w * 0.05, top - neck),
                                       fc.P(cx + w * 0.05, top - neck),
                                       fc.P(w - sh_in, top))]),
        fc.Edge("shoulder_r", [fc.Bezier(fc.P(w - sh_in, top),
                                         fc.P(w - sh_in * 0.7, top - 6.0),
                                         fc.P(w - w * 0.08, ARM_TOP + (top - ARM_TOP) * 0.6),
                                         fc.P(w, ARM_TOP))]),
        fc.Edge("side_seam_r", [fc.Line(fc.P(w, ARM_TOP), side_bot_r)]),
        fc.Edge("leg_opening_r", [fc.Bezier(side_bot_r,
                                            fc.P(w - w * 0.05, leg_height * 0.7),
                                            fc.P(cx + g + (w - cx - g) * 0.5, leg_height * 0.25),
                                            crotch_r)]),
        fc.Edge("crotch", [fc.Line(crotch_r, crotch_l)]),
    ]
    internals = [fc.Internal("underbust line",
                             [fc.P(0.0, TORSO_H * 0.6), fc.P(w, TORSO_H * 0.6)],
                             kind="marking")]
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"neckline": 0.0, "leg_opening_l": 0.0, "leg_opening_r": 0.0},
        notches=[fc.Notch("crotch", 0.5, "centre crotch"),
                 fc.Notch("side_seam_r", 0.5, "underbust line")],
        grainline=fc.Grainline(fc.P(cx, HIP_Y), fc.P(cx, top - 30.0)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False), label=label)


def build_front():
    return _torso("front", neck_scoop, "Front panel (cut 1)")


def build_back():
    return _torso("back", neck_scoop * 0.5, "Back panel (cut 1, higher back)")


def build_shelf():
    """Inner shelf bra (cut 1): a lined front shelf gathered to the underbust line, with a
    ring seat at each bust point for the strap. Its lower edge is the underbust ring (per
    half x2), finished with elastic; its top edge carries the two ring seats.
    """
    w = SHELF_UNDERBUST * 2.0        # full front underbust run
    cx = w / 2.0
    h = shelf_rise
    edges = [
        fc.Edge("underbust", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h * 0.5))]),
        fc.Edge("top", [fc.Bezier(fc.P(w, h * 0.5),
                                  fc.P(w * 0.72, h),
                                  fc.P(w * 0.28, h),
                                  fc.P(0.0, h * 0.5))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, h * 0.5), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("ring seat left", [fc.P(cx - w * 0.22, h * 0.8),
                                       fc.P(cx - w * 0.22 + strap_w, h * 0.8)], kind="marking"),
        fc.Internal("ring seat right", [fc.P(cx + w * 0.22 - strap_w, h * 0.8),
                                        fc.P(cx + w * 0.22, h * 0.8)], kind="marking"),
    ]
    return fc.Piece(
        "shelf", edges, seam_allowance=seam_allowance,
        allowances={"underbust": 0.0, "top": 0.0},
        notches=[fc.Notch("underbust", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(cx, h * 0.1), fc.P(cx, h * 0.6)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False),
        label="Inner shelf bra (cut 1, lined, ring seats)")


def build_gusset():
    w, ln = gusset_w, gusset_w * 1.5
    edges = [
        fc.Edge("front_end", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_a", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
        fc.Edge("back_end", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
        fc.Edge("side_b", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "gusset", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("front_end", 0.5, "centre-front match"),
                 fc.Notch("back_end", 0.5, "centre-back match")],
        grainline=fc.Grainline(fc.P(w * 0.5, ln * 0.15), fc.P(w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Gusset (cut 2 — self + swim lining)")


def build_strap():
    length = TORSO_H * 0.6 + 200.0
    edges = [
        fc.Edge("end_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, strap_w))]),
        fc.Edge("strap_edge", [fc.Line(fc.P(0.0, strap_w), fc.P(length, strap_w))]),
        fc.Edge("end_ring", [fc.Line(fc.P(length, strap_w), fc.P(length, 0.0))]),
        fc.Edge("strap_edge_b", [fc.Line(fc.P(length, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap", edges, seam_allowance=0.0,
        notches=[fc.Notch("strap_edge", 0.5, "slider position (adjustable)"),
                 fc.Notch("end_ring", 0.5, "ring at shelf bust line")],
        grainline=fc.Grainline(fc.P(length * 0.2, strap_w / 2.0),
                               fc.P(length * 0.8, strap_w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Adjustable strap (cut 2, ring at the shelf)")


def build():
    pattern = fc.PatternSet("swimsuit-one-piece")
    every = target_piece == "set"
    front = build_front()
    back = build_back()

    if not every:
        picked = {"front": front, "back": back, "shelf": build_shelf(),
                  "gusset": build_gusset(), "strap": build_strap()}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    shelf = build_shelf()
    gusset = build_gusset()
    strap = build_strap()
    global STRAP_EDGE_LEN
    STRAP_EDGE_LEN = strap.edge("strap_edge").length()
    for piece in (front, back, shelf, gusset, strap):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_seam_l"), ("back", "side_seam_l"), tol=1.0)
    pattern.declare_seam(("front", "side_seam_r"), ("back", "side_seam_r"), tol=1.0)
    pattern.declare_seam(("gusset", "front_end"), ("front", "crotch"), tol=1.0)
    pattern.declare_seam(("gusset", "back_end"), ("back", "crotch"), tol=1.0)
    # The strap threads through the ring, so its two ends match.
    pattern.declare_seam(("strap", "end_back"), ("strap", "end_ring"), tol=0.5)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    neck_opening = front.edge("neckline").length() + back.edge("neckline").length()
    leg_opening = 2.0 * (front.edge("leg_opening_r").length()
                         + back.edge("leg_opening_r").length())
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "swim lycra (chlorine-resistant, 4-way)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"front + back + shelf + gusset at {fabric_width:.0f} mm width, 60% marker. "
                 "Negative-ease throughout so the lycra grips the whole body."},
        {"item": "swim rings + sliders (Yantra4D bra-ring-slider)", "qty": 2, "unit": "set",
         "note": f"one ring + slider per strap; strap channel strap_w {strap_w:.0f} mm. The "
                 "ring/slider is the Yantra4D solid (notion.hardware_ref -> bra-ring-slider), "
                 "never modelled here. Adjustable straps ARE the structure of this rank."},
        {"item": f"strap elastic {strap_w:.0f} mm (swim)",
         "qty": round(2 * STRAP_EDGE_LEN * 1.2),
         "unit": "mm_length",
         "note": "cut to the ring channel width; swim elastic resists chlorine."},
        {"item": "leg + neckline elastic (swim, clear or rubber) 8 mm",
         "qty": round((neck_opening + leg_opening) * 0.92), "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} + legs {leg_opening:.0f} mm at 0.92; "
                 "high-cut legs finished so they lie flat."},
        {"item": "swim gusset lining", "qty": 1, "unit": "piece",
         "note": "the gusset self-piece encloses a swim lining, the hygienic standard."},
        {"item": "polyester thread + ballpoint + flatlock", "qty": 1, "unit": "set",
         "note": "flatlock the seams so they do not chafe under water."},
    ]
    pattern.metadata = {
        "fc400_rank": 389, "family": "active_swim", "fabric_hint": "swim-lycra",
        "silhouette_note": "A STRUCTURED one-piece maillot: full-torso swim panels with an "
            "inner shelf bra and ADJUSTABLE ring-and-slider straps, high-cut legs on a lined "
            "gusset. The adjustable straps and real shelf bra are the structure that "
            "distinguishes it from the FC-100 pull-on maillot.",
        "hardware": "rings + sliders via Yantra4D (notion.hardware_ref -> bra-ring-slider); "
            "strap_w drives BOTH the drafted strap's cut width (the strap_edge interface) and "
            "the ring/slider channel — the dimensional handshake.",
        "solved": {
            "bust_finished_mm": round(BUST_FIN, 1),
            "underbust_finished_mm": round(UNDERBUST_FIN, 1),
            "hip_finished_mm": round(HIP_FIN, 1),
            "shelf_rise_mm": round(shelf_rise, 1),
            "leg_height_mm": round(leg_height, 1),
            "strap_w_mm": round(strap_w, 1),
            "leg_opening_mm": round(leg_opening, 1),
        },
        "drafting": "Made to measure to bust, underbust, waist and hip girths + "
            "shoulder-to-crotch length; negative-ease throughout, with an inner shelf bra and "
            "adjustable straps.",
    }
    return pattern


result = build()

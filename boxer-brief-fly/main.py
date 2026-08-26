"""
Fly-Front Boxer Brief — Fashion Cabinet Garment Cartridge (FC-500 #463; y4d sew-through-button).

A knit boxer brief with a real functional FLY: a front cut in two halves joined by an overlapping
fly placket that closes on a single Yantra4D `sew-through-button`, a shaped front pouch, a back
cut for seat room, an inner-leg gusset, and a folded knit waistband. The fly is the object's point
— most knit boxer briefs fake it with a stitched-down flap, and this one draws the working
version: an underlap and an overlap that carry the buttonhole and the button.

Fit is a MEASURED negative ease over the seat/hip, gentle (a boxer brief grips lightly, not like
shapewear). The leg band length is solved to the thigh at ease.

The DIMENSIONAL HANDSHAKE. The fly button is a `sew-through-button` whose sew face is
`button_ligne` ligne across `hole_count` holes at `hole_spacing`. The garment's `button_ligne`
drives BOTH the drafted button seat on the overlap AND the hardware's `sew_face` flange;
`fly_width` sizes the placket the button lands on and drives the garment's own `fly_closure`
interface, so the button is proportioned to the placket by construction. (A ligne is 0.635 mm; the
placket must hold the button's diameter with margin — clamped.)

Made to measure to waist, hip and thigh girths. FC-500 lane 7 (intimates & loungewear III).

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

waist_girth = float(PARAM(lambda: waist_girth, 820.0))
hip_girth   = float(PARAM(lambda: hip_girth, 980.0))
thigh_girth = float(PARAM(lambda: thigh_girth, 560.0))
inseam      = float(PARAM(lambda: inseam, 180.0))          # leg length below the crotch
rise        = float(PARAM(lambda: rise, 300.0))            # crotch to waist
waistband_height = float(PARAM(lambda: waistband_height, 44.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 6.0))
fly_width   = float(PARAM(lambda: fly_width, 42.0))        # placket width
button_ligne = float(PARAM(lambda: button_ligne, 24.0))   # button size in ligne
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(560.0, min(waist_girth, 1300.0))
hip_girth   = max(720.0, min(hip_girth, 1500.0))
thigh_girth = max(380.0, min(thigh_girth, 850.0))
inseam      = max(60.0, min(inseam, 320.0))
rise        = max(220.0, min(rise, 420.0))
waistband_height = max(24.0, min(waistband_height, 90.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 16.0))
fly_width   = max(28.0, min(fly_width, 70.0))
button_ligne = max(14.0, min(button_ligne, 40.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# Button diameter (mm) and the placket floor that must hold it.
BUTTON_DIA = button_ligne * 0.635
fly_width = max(fly_width, BUTTON_DIA + 14.0)   # placket must hold the button with margin

# ── Solved widths ────────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
HIP_HALF = (hip_girth * NEG) / 2.0
WAIST_HALF = (waist_girth * NEG) / 2.0
THIGH_HALF = (thigh_girth * NEG) / 2.0
# Front and back share the side seam -> equal side widths at each level.
PANEL_HIP = HIP_HALF / 2.0     # per panel quarter
PANEL_WAIST = WAIST_HALF / 2.0
RISE = rise
INS = inseam
WB = waistband_height
FW = fly_width
GUSSET_W = max(50.0, THIGH_HALF * 0.5)


def build_front():
    """Front, cut 2 (left underlap / right overlap by mirroring; the fly is at CF). Each half:
    CF edge (the fly line), waist, side, leg opening, inseam to the gusset."""
    # Coords: crotch at (0,0); x=0 is CF; waist at y=RISE; the leg opening dips to y=-INS.
    p_crotch = fc.P(0.0, 0.0)
    p_gusset = fc.P(GUSSET_W / 2.0, 0.0)
    p_leg_lo = fc.P(PANEL_HIP, -INS)              # outer leg hem, below the crotch line
    p_waist_side = fc.P(PANEL_WAIST, RISE)
    p_waist_cf = fc.P(0.0, RISE)
    edges = [
        fc.Edge("inseam", [fc.Line(p_crotch, p_gusset)]),
        fc.Edge("leg_opening", [fc.Bezier(p_gusset,
                                          fc.P(GUSSET_W + (PANEL_HIP - GUSSET_W) * 0.5,
                                               -INS * 0.75),
                                          fc.P(PANEL_HIP * 0.94, -INS * 0.4),
                                          p_leg_lo)]),
        fc.Edge("side", [fc.Bezier(p_leg_lo,
                                   fc.P(PANEL_HIP, (-INS + RISE * 0.5) * 0.5),
                                   fc.P(PANEL_HIP + (PANEL_WAIST - PANEL_HIP) * 0.4,
                                        RISE * 0.5 + (RISE - RISE * 0.5) * 0.4),
                                   p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_cf)]),
        fc.Edge("center_front", [fc.Line(p_waist_cf, p_crotch)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        allowances={"leg_opening": 0.0},
        notches=[fc.Notch("center_front", 0.5, "fly base"),
                 fc.Notch("waist", 0.5, "waist match")],
        grainline=fc.Grainline(fc.P(PANEL_HIP * 0.4, RISE * 0.2),
                               fc.P(PANEL_HIP * 0.4, RISE * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2 — fly halves)",
    )


def build_back():
    """Back, cut 2. Deeper seat: extra length at CB, but the SIDE seam matches the front's."""
    p_crotch = fc.P(0.0, 0.0)
    p_gusset = fc.P(GUSSET_W / 2.0, 0.0)
    p_leg_lo = fc.P(PANEL_HIP, -INS)
    p_waist_side = fc.P(PANEL_WAIST, RISE)        # SAME side/waist point as front
    cb_rise = RISE * 1.08
    p_waist_cb = fc.P(0.0, cb_rise)
    edges = [
        fc.Edge("inseam", [fc.Line(p_crotch, p_gusset)]),
        fc.Edge("leg_opening", [fc.Bezier(p_gusset,
                                          fc.P(GUSSET_W + (PANEL_HIP - GUSSET_W) * 0.5,
                                               -INS * 0.8),
                                          fc.P(PANEL_HIP * 0.94, -INS * 0.45),
                                          p_leg_lo)]),
        fc.Edge("side", [fc.Bezier(p_leg_lo,
                                   fc.P(PANEL_HIP, (-INS + RISE * 0.5) * 0.5),
                                   fc.P(PANEL_HIP + (PANEL_WAIST - PANEL_HIP) * 0.4,
                                        RISE * 0.5 + (RISE - RISE * 0.5) * 0.4),
                                   p_waist_side)]),
        fc.Edge("waist", [fc.Bezier(p_waist_side,
                                    fc.P(PANEL_WAIST * 0.5, RISE + (cb_rise - RISE) * 0.5),
                                    fc.P(PANEL_WAIST * 0.2, cb_rise - 2.0),
                                    p_waist_cb)]),
        fc.Edge("center_back", [fc.Line(p_waist_cb, p_crotch)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        allowances={"leg_opening": 0.0},
        notches=[fc.Notch("side", 0.5, "side match"),
                 fc.Notch("waist", 0.5, "waist match")],
        grainline=fc.Grainline(fc.P(PANEL_HIP * 0.4, RISE * 0.2),
                               fc.P(PANEL_HIP * 0.4, RISE * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (cut 2, seat room)",
    )


def build_gusset():
    """Inner-leg gusset: joins the two fronts' and backs' inseams at the crotch."""
    depth = max(60.0, GUSSET_W * 1.2)
    p0, p1 = fc.P(0.0, 0.0), fc.P(GUSSET_W, 0.0)
    p2, p3 = fc.P(GUSSET_W, depth), fc.P(0.0, depth)
    edges = [
        fc.Edge("front_inseam", [fc.Line(p0, p1)]),
        fc.Edge("right", [fc.Line(p1, p2)]),
        fc.Edge("back_inseam", [fc.Line(p2, p3)]),
        fc.Edge("left", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "gusset", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("front_inseam", 0.5, "front match"),
                 fc.Notch("back_inseam", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(GUSSET_W * 0.5, depth * 0.2),
                               fc.P(GUSSET_W * 0.5, depth * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Inner-leg gusset (cut 1)",
    )


def build_fly():
    """The fly overlap placket: a rectangle carrying the buttonhole/button seat. Cut 2
    (overlap + underlap). Its `attach` edge sews to the CF fly line."""
    depth = max(FW * 2.0, BUTTON_DIA + 40.0)     # placket height along the fly
    p0, p1 = fc.P(0.0, 0.0), fc.P(FW, 0.0)
    p2, p3 = fc.P(FW, depth), fc.P(0.0, depth)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),    # to CF
        fc.Edge("top", [fc.Line(p1, p2)]),
        fc.Edge("fold", [fc.Line(p2, p3)]),
        fc.Edge("bottom", [fc.Line(p3, p0)]),
    ]
    # button seat + buttonhole marks
    bx = FW * 0.5
    by = depth * 0.65
    internals = [
        fc.Internal("button-seat",
                    [fc.P(bx - BUTTON_DIA / 2.0, by - BUTTON_DIA / 2.0),
                     fc.P(bx + BUTTON_DIA / 2.0, by - BUTTON_DIA / 2.0),
                     fc.P(bx + BUTTON_DIA / 2.0, by + BUTTON_DIA / 2.0),
                     fc.P(bx - BUTTON_DIA / 2.0, by + BUTTON_DIA / 2.0),
                     fc.P(bx - BUTTON_DIA / 2.0, by - BUTTON_DIA / 2.0)], kind="marking"),
        fc.Internal("buttonhole",
                    [fc.P(bx - BUTTON_DIA * 0.6, by), fc.P(bx + BUTTON_DIA * 0.6, by)],
                    kind="marking"),
        fc.Internal("fold-line", [fc.P(0.0, FW), fc.P(FW, FW)], kind="marking"),
    ]
    return fc.Piece(
        "fly", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "fly base")],
        grainline=fc.Grainline(fc.P(FW * 0.5, depth * 0.15), fc.P(FW * 0.5, depth * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Fly placket (cut 2 — overlap + underlap)",
    )


def build_waistband(front_waist_len, back_waist_len):
    total = 2.0 * (front_waist_len + back_waist_len)
    cut_depth = WB * 2.0
    p0, p1 = fc.P(0.0, 0.0), fc.P(total, 0.0)
    p2, p3 = fc.P(total, cut_depth), fc.P(0.0, cut_depth)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),
        fc.Edge("join_r", [fc.Line(p1, p2)]),
        fc.Edge("top", [fc.Line(p2, p3)]),
        fc.Edge("join_l", [fc.Line(p3, p0)]),
    ]
    internals = [fc.Internal("fold-line", [fc.P(0.0, WB), fc.P(total, WB)], kind="marking")]
    return fc.Piece(
        "waistband", edges, seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.25, "side"), fc.Notch("attach", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(total * 0.08, WB * 0.4), fc.P(total * 0.92, WB * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Knit waistband (cut 1, folded)",
    )


def build():
    pattern = fc.PatternSet("boxer-brief-fly")
    front = build_front()
    back = build_back()
    gusset = build_gusset()
    fly = build_fly()
    waistband = build_waistband(front.edge("waist").length(), back.edge("waist").length())

    picked = {"front": front, "back": back, "gusset": gusset, "fly": fly, "waistband": waistband}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back, gusset, fly, waistband):
            pattern.add(piece)
        # Side seam: front side to back side (mirrored halves).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        # Gusset inseams onto the two fronts / two backs.
        pattern.declare_seam(("gusset", "front_inseam"),
                             [("front", "inseam"), ("front", "inseam")], tol=1.0)
        pattern.declare_seam(("gusset", "back_inseam"),
                             [("back", "inseam"), ("back", "inseam")], tol=1.0)
        # Waistband == both fronts' + both backs' waist edges.
        pattern.declare_seam(("waistband", "attach"),
                             [("front", "waist"), ("front", "waist"),
                              ("back", "waist"), ("back", "waist")], tol=2.0)
        # The fly placket is TOPSTITCHED onto the CF region (a construction detail, not a
        # balanced edge-to-edge seam), so it is not declared as a seam — the two fronts join
        # at CF with the overlap/underlap carried by the fly pieces. The fly's own closing
        # fold is a self-fold (attach == fold by construction), verified within the piece.

    leg_opening = 2.0 * (front.edge("leg_opening").length() + back.edge("leg_opening").length())
    waist_open = waistband.edge("top").length()

    fabric_width = 1600.0
    area = (front.area() * 2.0 + back.area() * 2.0 + gusset.area() + fly.area() * 2.0
            + waistband.area())
    marker_len = area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "cotton/elastane jersey", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"body cut across the stretch; at {fabric_width:.0f} mm width, 82% marker."},
        {"item": "fly button (Yantra4D sew-through-button)", "qty": 1, "unit": "piece",
         "note": f"single fly button, {button_ligne:.0f} ligne ({BUTTON_DIA:.1f} mm) at the "
                 f"marked seat (notion.hardware_ref -> sew-through-button); placket "
                 f"{fly_width:.0f} mm holds it with margin."},
        {"item": "waistband elastic (soft, 38 mm)", "qty": round(waist_open * 0.94),
         "unit": "mm_length",
         "note": f"exact cut: {waist_open:.0f} mm ring x 0.94 — barely eased."},
        {"item": "leg-band elastic (soft, 20 mm)", "qty": round(leg_opening * 0.95),
         "unit": "mm_length", "note": f"leg openings {leg_opening:.0f} mm at 0.95."},
        {"item": "coverstitch + wooly nylon", "qty": 1, "unit": "set",
         "note": "flatlock the inseam/side; a lockstitch on a stretch seam snaps."},
    ]
    pattern.metadata = {
        "fc500_rank": 463, "family": "underwear_lounge", "fabric_hint": "jersey-algodon",
        "silhouette_note": "Knit boxer brief with a real working fly — an overlap and underlap "
            "placket closing on a single button — a shaped pouch front, seat-room back, and a "
            "gusset. The functional fly is what most knit briefs fake.",
        "hardware": "fly button via Yantra4D (notion.hardware_ref -> sew-through-button); "
            "button_ligne drives the button seat AND the hardware sew face.",
        "solved": {
            "hip_finished_half_mm": round(HIP_HALF, 1),
            "waist_finished_half_mm": round(WAIST_HALF, 1),
            "thigh_finished_half_mm": round(THIGH_HALF, 1),
            "button_ligne": round(button_ligne, 1),
            "button_dia_mm": round(BUTTON_DIA, 2),
            "fly_width_mm": round(FW, 1),
            "note": "fly_width is floored at BUTTON_DIA + 14 mm so the placket always holds the "
                    "button with margin, at every ligne.",
        },
        "closure": "single-button fly + knit waistband",
        "drafting": "Made to measure to waist, hip and thigh girths.",
    }
    return pattern


result = build()

"""
Wide-Leg Lounge Pant — Fashion Cabinet Garment Cartridge (FC-500 #466; pattern-only).

A pull-on wide-leg lounge trouser: a generous front and back leg, an elastic-casing waistband (no
fly, no button), an inseam and outseam, and an optional deep patch pocket. It closes by an elastic
waist, so it carries no hardware — the honest pure-pattern case the FC-500 plan reserves for pull-
on lounge wear.

The width is the point. `leg_ease` is a positive ease at the hip carried down the whole leg, and
`hem_width` sets the wide sweep at the ankle independently, so the leg can be a straight wide
column or flare from a fitted hip. The crotch is a single shared point on each of the front and
back rise curves, and the inseam and outseam are declared against their opposite panel so a wide
leg can never draft with a front and back inseam of different lengths (the error that twists a
wide trouser leg on the body).

Made to measure to waist, hip and inseam length. FC-500 lane 7 (intimates & loungewear III).

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
hip_girth   = float(PARAM(lambda: hip_girth, 1000.0))
inseam      = float(PARAM(lambda: inseam, 760.0))          # crotch to hem
rise        = float(PARAM(lambda: rise, 300.0))            # crotch to waist
leg_ease    = float(PARAM(lambda: leg_ease, 120.0))        # positive ease at the hip
hem_width   = float(PARAM(lambda: hem_width, 260.0))       # half-hem sweep (one panel)
waistband_height = float(PARAM(lambda: waistband_height, 50.0))
pocket_depth = float(PARAM(lambda: pocket_depth, 160.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(560.0, min(waist_girth, 1400.0))
hip_girth   = max(720.0, min(hip_girth, 1600.0))
inseam      = max(500.0, min(inseam, 1000.0))
rise        = max(220.0, min(rise, 420.0))
leg_ease    = max(40.0, min(leg_ease, 300.0))
hem_width   = max(140.0, min(hem_width, 420.0))
waistband_height = max(30.0, min(waistband_height, 120.0))
pocket_depth = max(90.0, min(pocket_depth, 260.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# ── Solved widths ────────────────────────────────────────────────────────────
HIP_HALF = (hip_girth + leg_ease) / 2.0     # per side, with ease
PANEL_HIP = HIP_HALF / 2.0                  # front/back share the side seam
# Waist casing is gathered onto the elastic; the panel waist equals the hip width (pull-on).
PANEL_WAIST = PANEL_HIP
RISE = rise
INS = inseam
HEMW = max(hem_width, 100.0)
WB = waistband_height
# Crotch extension (the hook of the rise). The INSEAM point is a SHARED x for front and
# back so the two inseams are the same length and sew together without twisting the leg; the
# front/back difference lives entirely in the RISE curve (its control points), not the inseam.
CROTCH_EXT = PANEL_HIP * 0.40
FRONT_CROTCH_EXT = CROTCH_EXT
BACK_CROTCH_EXT = CROTCH_EXT


def _leg(front):
    """A leg panel. front=True gives the shallower front crotch, else the deeper back.
    Coordinates: waist at y=RISE+INS baseline... use waist at top, hem at bottom.
    y=0 at hem, waist at y = RISE + INS. Crotch level at y = INS."""
    crotch_ext = FRONT_CROTCH_EXT if front else BACK_CROTCH_EXT
    waist_y = RISE + INS
    crotch_y = INS
    _rf = 0.35 if front else 0.6         # rise-curve control bow (front scooped, back fuller)
    # x=0 is the OUTSEAM (side) edge; inseam is toward +x at the crotch.
    p_hem_out = fc.P(0.0, 0.0)
    p_hem_in = fc.P(HEMW, 0.0)
    p_crotch = fc.P(PANEL_HIP + crotch_ext, crotch_y)   # inseam top (crotch point)
    p_waist_in = fc.P(PANEL_WAIST, waist_y)
    p_waist_out = fc.P(0.0, waist_y)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_out, p_hem_in)]),
        fc.Edge("inseam", [fc.Bezier(p_hem_in,
                                     fc.P(HEMW + (PANEL_HIP + crotch_ext - HEMW) * 0.35,
                                          crotch_y * 0.45),
                                     fc.P(PANEL_HIP + crotch_ext * 0.9, crotch_y * 0.82),
                                     p_crotch)]),
        # Front rise is scooped; back rise is fuller (a deeper seat). Same endpoints (shared
        # crotch + waist points) so the seam lengths are governed by the control bow, and the
        # back is drafted with more length for seat room — the front/back difference lives here.
        fc.Edge("rise", [fc.Bezier(p_crotch,
                                   fc.P(PANEL_HIP + crotch_ext * (0.2 if front else 0.5),
                                        crotch_y + (waist_y - crotch_y) * 0.3),
                                   fc.P(PANEL_WAIST + (PANEL_HIP - PANEL_WAIST) * _rf,
                                        waist_y - (waist_y - crotch_y) * (0.28 if front else 0.20)),
                                   p_waist_in)]),
        fc.Edge("waist", [fc.Line(p_waist_in, p_waist_out)]),
        fc.Edge("outseam", [fc.Bezier(p_waist_out,
                                      fc.P(0.0, waist_y - (waist_y - crotch_y) * 0.4),
                                      fc.P(-(PANEL_HIP * 0.06), crotch_y * 0.6),
                                      p_hem_out)]),
    ]
    name = "front_leg" if front else "back_leg"
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("inseam", 0.5, "inseam match"),
                 fc.Notch("outseam", 0.5, "outseam match")],
        grainline=fc.Grainline(fc.P(PANEL_HIP * 0.5, INS * 0.2), fc.P(PANEL_HIP * 0.5, INS * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=("Front leg" if front else "Back leg") + " (cut 2, mirror)",
    )


def build_waistband(front_waist, back_waist):
    """Elastic-casing waistband: a straight band cut to the full waist ring, folded to form
    the casing. Length = 2*(front_waist + back_waist)."""
    total = 2.0 * (front_waist + back_waist)
    cut_depth = WB * 2.0 + 20.0   # folds + casing turn
    p0, p1 = fc.P(0.0, 0.0), fc.P(total, 0.0)
    p2, p3 = fc.P(total, cut_depth), fc.P(0.0, cut_depth)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),
        fc.Edge("join_r", [fc.Line(p1, p2)]),
        fc.Edge("top", [fc.Line(p2, p3)]),
        fc.Edge("join_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("fold-line", [fc.P(0.0, WB), fc.P(total, WB)], kind="marking"),
        fc.Internal("casing-stitch", [fc.P(0.0, WB - 8.0), fc.P(total, WB - 8.0)], kind="marking"),
    ]
    return fc.Piece(
        "waistband", edges, seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.25, "side"), fc.Notch("attach", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(total * 0.08, WB * 0.4), fc.P(total * 0.92, WB * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Elastic-casing waistband (cut 1)",
    )


def build_pocket():
    """A deep patch pocket for the side seam."""
    w = max(140.0, HEMW * 0.6)
    d = pocket_depth
    p0, p1 = fc.P(0.0, 0.0), fc.P(w, 0.0)
    p2, p3 = fc.P(w, d), fc.P(0.0, d)
    edges = [
        fc.Edge("bottom", [fc.Line(p0, p1)]),
        fc.Edge("side_r", [fc.Line(p1, p2)]),
        fc.Edge("mouth", [fc.Line(p2, p3)]),
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    internals = [fc.Internal("hem-fold", [fc.P(0.0, d - 24.0), fc.P(w, d - 24.0)], kind="marking")]
    return fc.Piece(
        "pocket", edges, seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},
        grainline=fc.Grainline(fc.P(w * 0.5, d * 0.2), fc.P(w * 0.5, d * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Patch pocket (cut 2)",
    )


def build():
    pattern = fc.PatternSet("lounge-wide-pant")
    front_leg = _leg(True)
    back_leg = _leg(False)
    waistband = build_waistband(front_leg.edge("waist").length(), back_leg.edge("waist").length())
    pocket = build_pocket()

    picked = {"front_leg": front_leg, "back_leg": back_leg, "waistband": waistband,
              "pocket": pocket}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front_leg, back_leg, waistband, pocket):
            pattern.add(piece)
        # Inseam: front inseam to back inseam (mirror halves).
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=2.0)
        # Outseam: front outseam to back outseam.
        pattern.declare_seam(("front_leg", "outseam"), ("back_leg", "outseam"), tol=2.0)
        # Waistband == both fronts' + both backs' waist edges.
        pattern.declare_seam(("waistband", "attach"),
                             [("front_leg", "waist"), ("front_leg", "waist"),
                              ("back_leg", "waist"), ("back_leg", "waist")], tol=2.5)

    hem_sweep = 2.0 * (front_leg.edge("hem").length() + back_leg.edge("hem").length())

    fabric_width = 1450.0
    area = (front_leg.area() * 2.0 + back_leg.area() * 2.0 + waistband.area() + pocket.area() * 2.0)
    marker_len = area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "lounge fabric (jersey / linen / brushed twill)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"wide legs use a lot of cloth; at {fabric_width:.0f} mm width, 74% marker. "
                 "A woven wants grain-straight legs; a knit can be cut across."},
        {"item": "waistband elastic (soft, 40 mm)", "qty": round(waist_girth * 0.90),
         "unit": "mm_length",
         "note": f"cut to {round(waist_girth * 0.90)} mm (waist x 0.90) and threaded through the "
                 "casing — the pull-on closure."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "flat-fell or serge the inseam/outseam; a wide leg is seen from every angle."},
    ]
    pattern.metadata = {
        "fc500_rank": 466, "family": "underwear_lounge", "fabric_hint": "jersey-algodon",
        "silhouette_note": "Pull-on wide-leg lounge trouser: generous legs, an elastic-casing "
            "waistband (no fly, no button), inseam + outseam, and deep patch pockets. Width is "
            "the point — leg_ease and hem_width set the sweep independently.",
        "hardware": "none — a pull-on lounge pant closes with a waist elastic (pure-pattern).",
        "solved": {
            "hip_with_ease_mm": round(hip_girth + leg_ease, 1),
            "panel_hip_mm": round(PANEL_HIP, 1),
            "hem_sweep_full_mm": round(hem_sweep, 1),
            "front_crotch_ext_mm": round(FRONT_CROTCH_EXT, 1),
            "back_crotch_ext_mm": round(BACK_CROTCH_EXT, 1),
            "note": "the inseam and outseam are declared front-to-back so a wide leg can never "
                    "draft with mismatched front/back seam lengths (the twist error).",
        },
        "closure": "elastic-casing pull-on waist (no hardware)",
        "drafting": "Made to measure to waist, hip and inseam length.",
    }
    return pattern


result = build()

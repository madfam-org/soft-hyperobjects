"""
High-Waist Shaping Brief — Fashion Cabinet Garment Cartridge (FC-500 #461; y4d hook-and-eye).

A high-waist compression brief (faja calzón): a front control panel and back panel cut at negative
ease over the hip and waist, a knit waistband that reaches to (or above) the natural waist, and a
gusset that opens at a Yantra4D `hook-and-eye` closure so the garment can be worn without full
removal — the practical detail that separates real shapewear from a tight brief.

Compression is a MEASURED negative ease, graduated: firmer at the waist (`waist_compression`),
gentler at the hip (`hip_compression`), with the waist figure clamped never to be gentler than the
hip's (an error-severity constraint mirrors this in the manifest). The panels are cut to the body
girth times (1 - compression) at each level, so the garment's grip is a number rather than a
fabric-and-hope guess.

The DIMENSIONAL HANDSHAKE. The gusset placket closes on a `hook-and-eye` tape whose sewn plate is
`size_mm` wide across `columns`. The garment's `gusset_width` drives the placket the hooks sew to
AND the garment's own `gusset_closure` interface; the params_map feeds the hardware's `columns`
from `round(gusset_width / hook_pitch)` so the number of hooks fits the placket width, and
`size_mm` from the hook pitch — the placket the hooks sew to is exactly as wide as the tape.

Made to measure to waist and hip girths. FC-500 lane 7 (intimates & loungewear III).

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

waist_girth = float(PARAM(lambda: waist_girth, 760.0))
hip_girth   = float(PARAM(lambda: hip_girth, 980.0))
rise        = float(PARAM(lambda: rise, 340.0))           # gusset to waistband top, front
waistband_height = float(PARAM(lambda: waistband_height, 60.0))  # high-waist band depth
waist_compression = float(PARAM(lambda: waist_compression, 0.14))
hip_compression   = float(PARAM(lambda: hip_compression, 0.08))
gusset_width = float(PARAM(lambda: gusset_width, 70.0))
hook_pitch   = float(PARAM(lambda: hook_pitch, 14.0))     # hook column pitch
leg_scoop    = float(PARAM(lambda: leg_scoop, 46.0))      # leg-opening scoop depth
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(560.0, min(waist_girth, 1300.0))
hip_girth   = max(720.0, min(hip_girth, 1500.0))
rise        = max(220.0, min(rise, 460.0))
waistband_height = max(30.0, min(waistband_height, 140.0))
waist_compression = max(0.04, min(waist_compression, 0.28))
hip_compression   = max(0.02, min(hip_compression, 0.22))
gusset_width = max(40.0, min(gusset_width, 130.0))
hook_pitch   = max(8.0, min(hook_pitch, 24.0))
leg_scoop    = max(20.0, min(leg_scoop, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# Waist must grip at least as firmly as the hip (graduated compression). Clamp, don't trust.
waist_compression = max(waist_compression, hip_compression)

# ── Solved panel widths (per-quarter: two side seams => front half + back half) ──
WAIST_HALF = (waist_girth * (1.0 - waist_compression)) / 2.0
HIP_HALF   = (hip_girth * (1.0 - hip_compression)) / 2.0
# Front and back share the side seam, so they carry EQUAL width at hip and waist (the
# side seam is one physical seam and must match to the millimetre). Front/back shaping
# differs in the leg scoop and the higher centre-back rise, not in the side width.
FRONT_FRAC = 0.50
FRONT_WAIST = max(60.0, WAIST_HALF * FRONT_FRAC)
BACK_WAIST  = max(60.0, WAIST_HALF * (1.0 - FRONT_FRAC))
FRONT_HIP   = max(80.0, HIP_HALF * FRONT_FRAC)
BACK_HIP    = max(80.0, HIP_HALF * (1.0 - FRONT_FRAC))
RISE = rise
WB = waistband_height
GW = gusset_width


def build_front():
    """Front control panel: waist (top) narrower than hip (mid), scooping to the gusset.
    Left edge is CF, right edge is the side seam. Built bottom (gusset) up."""
    # y=0 at gusset; up to RISE at the waist seam (waistband sews on above).
    cf_x = 0.0
    # side seam runs from hip width at mid down/in to gusset and up to waist.
    gusset_half = GW / 2.0
    p_gusset_l = fc.P(cf_x, 0.0)
    p_gusset_r = fc.P(gusset_half, 0.0)
    # leg scoop: side rises from gusset out to the hip line
    hip_y = RISE * 0.42
    p_hip = fc.P(FRONT_HIP, hip_y)
    p_waist = fc.P(FRONT_WAIST, RISE)
    p_cf_top = fc.P(cf_x, RISE)
    edges = [
        fc.Edge("gusset_seam", [fc.Line(p_gusset_l, p_gusset_r)]),
        fc.Edge("leg_opening", [fc.Bezier(p_gusset_r,
                                          fc.P(gusset_half + (FRONT_HIP - gusset_half) * 0.5,
                                               leg_scoop * 0.4),
                                          fc.P(FRONT_HIP * 0.92, hip_y - leg_scoop * 0.2),
                                          p_hip)]),
        fc.Edge("side_seam", [fc.Bezier(p_hip,
                                        fc.P(FRONT_HIP + (FRONT_WAIST - FRONT_HIP) * 0.3,
                                             hip_y + (RISE - hip_y) * 0.35),
                                        fc.P(FRONT_WAIST + (FRONT_HIP - FRONT_WAIST) * 0.2,
                                             RISE - (RISE - hip_y) * 0.30),
                                        p_waist)]),
        fc.Edge("waist_seam", [fc.Line(p_waist, p_cf_top)]),
        fc.Edge("center_front", [fc.Line(p_cf_top, p_gusset_l)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        allowances={"leg_opening": 0.0},
        notches=[fc.Notch("side_seam", 0.42, "hip level"),
                 fc.Notch("waist_seam", 0.5, "waist match")],
        grainline=fc.Grainline(fc.P(FRONT_HIP * 0.4, RISE * 0.2),
                               fc.P(FRONT_HIP * 0.4, RISE * 0.8)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_front"),
        label="Front control panel (cut 1 on fold)",
    )


def build_back():
    """Back panel: mirror logic, taller rise at CB, scooping to the gusset."""
    cb_x = 0.0
    gusset_half = GW / 2.0
    # The side seam must match the front's, so the SIDE point sits at the same rise/hip as
    # the front. Extra back length lives only at centre back (a higher CB scoop), added
    # after the side point — it never lengthens the side seam.
    hip_y = RISE * 0.42
    cb_rise = RISE * 1.06
    p_gusset_l = fc.P(cb_x, 0.0)
    p_gusset_r = fc.P(gusset_half, 0.0)
    p_hip = fc.P(BACK_HIP, hip_y)
    p_waist = fc.P(BACK_WAIST, RISE)          # side/waist point at the SAME rise as front
    p_cb_top = fc.P(cb_x, cb_rise)
    edges = [
        fc.Edge("gusset_seam", [fc.Line(p_gusset_l, p_gusset_r)]),
        fc.Edge("leg_opening", [fc.Bezier(p_gusset_r,
                                          fc.P(gusset_half + (BACK_HIP - gusset_half) * 0.5,
                                               leg_scoop * 0.5),
                                          fc.P(BACK_HIP * 0.92, hip_y - leg_scoop * 0.25),
                                          p_hip)]),
        fc.Edge("side_seam", [fc.Bezier(p_hip,
                                        fc.P(BACK_HIP + (BACK_WAIST - BACK_HIP) * 0.3,
                                             hip_y + (RISE - hip_y) * 0.35),
                                        fc.P(BACK_WAIST + (BACK_HIP - BACK_WAIST) * 0.2,
                                             RISE - (RISE - hip_y) * 0.30),
                                        p_waist)]),
        fc.Edge("waist_seam", [fc.Line(p_waist, p_cb_top)]),
        fc.Edge("center_back", [fc.Line(p_cb_top, p_gusset_l)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        allowances={"leg_opening": 0.0},
        notches=[fc.Notch("side_seam", 0.44, "hip level"),
                 fc.Notch("waist_seam", 0.5, "waist match")],
        grainline=fc.Grainline(fc.P(BACK_HIP * 0.4, cb_rise * 0.2),
                               fc.P(BACK_HIP * 0.4, cb_rise * 0.8)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back"),
        label="Back panel (cut 1 on fold)",
    )


def build_gusset():
    """The gusset with a hook-and-eye placket: a rectangle whose two long ends are the
    front/back gusset seams and whose `placket` edge carries the hook tape. Cut double."""
    depth = max(60.0, GW * 1.1)
    p0, p1 = fc.P(0.0, 0.0), fc.P(GW, 0.0)
    p2, p3 = fc.P(GW, depth), fc.P(0.0, depth)
    edges = [
        fc.Edge("front_seam", [fc.Line(p0, p1)]),
        fc.Edge("placket_r", [fc.Line(p1, p2)]),
        fc.Edge("back_seam", [fc.Line(p2, p3)]),
        fc.Edge("placket_l", [fc.Line(p3, p0)]),
    ]
    # hook column marks along the placket
    n_hooks = max(1, int(round(GW / hook_pitch)))
    internals = []
    for i in range(n_hooks):
        x = (i + 0.5) * (GW / n_hooks)
        internals.append(fc.Internal(f"hook-{i}", [fc.P(x, depth * 0.5 - 6.0),
                                                   fc.P(x, depth * 0.5 + 6.0)], kind="drill"))
    internals.append(fc.Internal("hook-tape-line",
                                 [fc.P(0.0, depth * 0.5), fc.P(GW, depth * 0.5)],
                                 kind="marking"))
    return fc.Piece(
        "gusset", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("front_seam", 0.5, "front match"),
                 fc.Notch("back_seam", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(GW * 0.5, depth * 0.2), fc.P(GW * 0.5, depth * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Gusset with hook-and-eye placket (cut 2)",
    )


def build_waistband(front_waist_len, back_waist_len):
    """The high-waist band: cut to the combined front+back waist seams, folded double at
    its depth, negative-ease at the waist."""
    total = 2.0 * (front_waist_len + back_waist_len)  # full ring (both sides)
    band_len = total
    cut_depth = WB * 2.0  # folds
    p0, p1 = fc.P(0.0, 0.0), fc.P(band_len, 0.0)
    p2, p3 = fc.P(band_len, cut_depth), fc.P(0.0, cut_depth)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),
        fc.Edge("join_r", [fc.Line(p1, p2)]),
        fc.Edge("top", [fc.Line(p2, p3)]),
        fc.Edge("join_l", [fc.Line(p3, p0)]),
    ]
    internals = [fc.Internal("fold-line", [fc.P(0.0, WB), fc.P(band_len, WB)], kind="marking")]
    return fc.Piece(
        "waistband", edges, seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.25, "side"), fc.Notch("attach", 0.5, "CB"),
                 fc.Notch("attach", 0.75, "side")],
        grainline=fc.Grainline(fc.P(band_len * 0.08, WB * 0.4), fc.P(band_len * 0.92, WB * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="High waistband (cut 1, folded)",
    )


def build():
    pattern = fc.PatternSet("high-waist-shaping-brief")
    front = build_front()
    back = build_back()
    gusset = build_gusset()
    waistband = build_waistband(front.edge("waist_seam").length(),
                                back.edge("waist_seam").length())

    picked = {"front": front, "back": back, "gusset": gusset, "waistband": waistband}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back, gusset, waistband):
            pattern.add(piece)
        # Side seams: front side + back side (both halves) — declare one pairing (mirrored).
        pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.5)
        # Gusset front/back seams onto the panels' gusset seams. The panels are cut ON
        # FOLD, so each panel's gusset_seam edge is HALF the body width; the gusset (cut
        # flat) spans the full width, so the panel edge is counted twice.
        pattern.declare_seam(("gusset", "front_seam"),
                             [("front", "gusset_seam"), ("front", "gusset_seam")], tol=1.0)
        pattern.declare_seam(("gusset", "back_seam"),
                             [("back", "gusset_seam"), ("back", "gusset_seam")], tol=1.0)
        # Waistband attach == both waist seams, full ring.
        pattern.declare_seam(("waistband", "attach"),
                             [("front", "waist_seam"), ("front", "waist_seam"),
                              ("back", "waist_seam"), ("back", "waist_seam")], tol=1.5)

    leg_opening = 2.0 * (front.edge("leg_opening").length() + back.edge("leg_opening").length())
    waist_open = waistband.edge("top").length()

    fabric_width = 1550.0
    area = (front.area() * 2.0 + back.area() * 2.0 + gusset.area() * 2.0 + waistband.area())
    marker_len = area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "power-net / compression knit (poly-elastane)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"panels cut on the high-stretch grain across the body; at {fabric_width:.0f} "
                 "mm width, 80% marker. The compression IS the fit — no lining."},
        {"item": "hook-and-eye gusset tape (Yantra4D hook-and-eye)", "qty": 1, "unit": "piece",
         "note": f"gusset placket closure, {max(1, int(round(gusset_width / hook_pitch)))} "
                 f"columns across {gusset_width:.0f} mm (notion.hardware_ref -> hook-and-eye); "
                 "lets the brief open at the gusset without full removal."},
        {"item": "waistband elastic (soft, 40 mm)", "qty": round(waist_open * 0.90),
         "unit": "mm_length",
         "note": f"exact cut: {waist_open:.0f} mm ring x 0.90 — the high band is cut short so "
                 "it stays up without rolling."},
        {"item": "leg-opening elastic (picot, 10 mm)", "qty": round(leg_opening * 0.92),
         "unit": "mm_length",
         "note": f"leg openings {leg_opening:.0f} mm at 0.92 — a light draw stops the leg riding."},
        {"item": "coverstitch + wooly nylon", "qty": 1, "unit": "set",
         "note": "flatlock/coverstitch throughout; a lockstitch on a compression seam snaps."},
    ]
    pattern.metadata = {
        "fc500_rank": 461, "family": "underwear_lounge", "fabric_hint": "nylon-elastano",
        "silhouette_note": "High-waist compression brief with a graduated squeeze — firmer at "
            "the waist, gentler at the hip — a front control panel, and a hook-and-eye gusset "
            "that opens without full removal.",
        "hardware": "gusset closure via Yantra4D (notion.hardware_ref -> hook-and-eye); "
            "gusset_width drives the placket the hooks sew to and the hook column count.",
        "solved": {
            "waist_compression": round(waist_compression, 3),
            "hip_compression": round(hip_compression, 3),
            "waist_finished_half_mm": round(WAIST_HALF, 1),
            "hip_finished_half_mm": round(HIP_HALF, 1),
            "gusset_width_mm": round(GW, 1),
            "hook_columns": max(1, int(round(gusset_width / hook_pitch))),
            "note": "panels cut to girth * (1 - compression) at each level; the waist figure "
                    "is clamped never gentler than the hip's (graduated compression).",
        },
        "closure": "hook-and-eye gusset placket",
        "drafting": "Made to measure to waist and hip girths.",
    }
    return pattern


result = build()

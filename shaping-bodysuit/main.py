"""
Shaping Bodysuit — Fashion Cabinet Garment Cartridge (FC-300 #226; y4d hook-and-eye).

A compression bodysuit shaped by PRINCESS SEAMS rather than by darts or by stretch
alone. That choice is the garment:

  - A dart takes fullness out at a POINT and leaves a bubble either side of it. A
    princess seam takes the same fullness out along a CONTINUOUS CURVE running from the
    armhole down over the bust, in to the waist and out over the hip — so the shaping is
    distributed the whole length of the body instead of concentrated at a tip. In a
    compression garment that matters twice over: a dart tip under tension is a stress
    riser that eventually blows out, and the seam itself, being a seam, is stiffer than
    the cloth — a princess line is therefore also a structural line, doing the job
    boning does in a corset without any boning at all.
  - The seams run through all three rings (bust, waist, hip), so the suit's shaping is
    made to measure to all three, and the waist nip is an explicit reduction rather than
    a consequence of how hard the fabric happens to squeeze.

Construction. Six panels around the body (centre-front, side-front, side-back all cut as
mirrored pairs), joined by four princess seams per side, plus a gusset that closes with
a HOOK-AND-EYE at the crotch — the standard bodysuit closure, and the reason this
cartridge consumes `hook-and-eye`. That fitting is POINT/SLOT: hooks and eyes engage
each other, they have no sewn flange whose length must match a garment edge, so the
manifest maps only the tape's column and row COUNTS (numeric literals) and no edge
coupling is required.

Every princess seam is built from ONE shared curve profile reused on both mating panels,
so all four seams balance to the micron by construction.

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

bust_girth   = float(PARAM(lambda: bust_girth, 940.0))
waist_girth  = float(PARAM(lambda: waist_girth, 760.0))
hip_girth    = float(PARAM(lambda: hip_girth, 990.0))
body_rise    = float(PARAM(lambda: body_rise, 285.0))
front_neck_to_waist = float(PARAM(lambda: front_neck_to_waist, 360.0))
waist_reduction = float(PARAM(lambda: waist_reduction, 40.0))
compression_pct = float(PARAM(lambda: compression_pct, 12.0))
gusset_w     = float(PARAM(lambda: gusset_w, 75.0))
strap_w      = float(PARAM(lambda: strap_w, 18.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
bust_girth   = max(640.0, min(bust_girth, 1500.0))
waist_girth  = max(520.0, min(waist_girth, 1400.0))
hip_girth    = max(620.0, min(hip_girth, 1700.0))
body_rise    = max(180.0, min(body_rise, 420.0))
front_neck_to_waist = max(240.0, min(front_neck_to_waist, 520.0))
waist_reduction = max(0.0, min(waist_reduction, 120.0))
compression_pct = max(0.0, min(compression_pct, 25.0))
gusset_w     = max(45.0, min(gusset_w, 140.0))
strap_w      = max(8.0, min(strap_w, 32.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# ── The shaping solver ───────────────────────────────────────────────────────
# Compression applies to every ring; the waist takes the extra explicit reduction on
# top of it (that is the "shaping" a shaping bodysuit is bought for).
NEG = 1.0 - compression_pct / 100.0
BUST_FIN = bust_girth * NEG
WAIST_FIN = waist_girth * NEG - waist_reduction
HIP_FIN = hip_girth * NEG

# Six panels around the body: cf, side_front, side_back each cut as a mirrored pair.
# Each panel therefore carries a sixth of every ring.
PANELS = 6.0
BUST_P = BUST_FIN / PANELS
WAIST_P = WAIST_FIN / PANELS
HIP_P = HIP_FIN / PANELS

BODICE_H = front_neck_to_waist          # waist line up to the neck/shoulder line
RISE = body_rise                        # waist line down to the crotch
WAIST_Y = RISE                          # waist sits at y = RISE in panel coordinates
TOTAL_H = RISE + BODICE_H


def _princess_profile(x_bust, x_waist, x_hip, sign):
    """The shared princess-seam curve, reused verbatim on BOTH mating panels.

    Runs bottom (crotch/hip) -> waist -> top (bust/shoulder), bowing out over the hip,
    in at the waist and out over the bust. Because the identical profile is used on the
    panel either side of every seam, all four princess seams balance exactly (delta 0).
    `sign` mirrors the profile for the panel's other edge.
    """
    return [
        fc.Bezier(fc.P(sign * x_hip, 0.0),
                  fc.P(sign * x_hip * 1.04, RISE * 0.34),
                  fc.P(sign * x_waist * 1.06, RISE * 0.74),
                  fc.P(sign * x_waist, WAIST_Y)),
        fc.Bezier(fc.P(sign * x_waist, WAIST_Y),
                  fc.P(sign * x_waist * 1.10, WAIST_Y + BODICE_H * 0.26),
                  fc.P(sign * x_bust * 1.02, WAIST_Y + BODICE_H * 0.62),
                  fc.P(sign * x_bust, TOTAL_H)),
    ]


def _panel(name, is_cf, is_back, label):
    """One bodysuit panel, shaped by princess seams on both vertical edges.

    All panels share the same bust/waist/hip sixths, so `seam_l` of one is congruent
    with `seam_r` of its neighbour and every princess seam balances by construction.
    The centre-front panel carries the neckline and strap tab; the back panel likewise.
    """
    xb, xw, xh = BUST_P / 2.0, WAIST_P / 2.0, HIP_P / 2.0
    # Left seam runs top -> bottom; right seam bottom -> top (CCW outline).
    left = [seg.reversed() for seg in reversed(_princess_profile(xb, xw, xh, -1.0))]
    right = _princess_profile(xb, xw, xh, 1.0)
    top_label = "shoulder" if is_cf or is_back else "armscye"
    edges = [
        fc.Edge("crotch" if is_cf or is_back else "hem",
                [fc.Line(fc.P(-xh, 0.0), fc.P(xh, 0.0))]),
        fc.Edge("seam_r", right),
        fc.Edge(top_label, [fc.Line(fc.P(xb, TOTAL_H), fc.P(-xb, TOTAL_H))]),
        fc.Edge("seam_l", left),
    ]
    internals = [
        fc.Internal("waist line", [fc.P(-xw, WAIST_Y), fc.P(xw, WAIST_Y)], kind="marking"),
    ]
    notches = [fc.Notch("seam_r", 0.5, "waist match"),
               fc.Notch("seam_l", 0.5, "waist match")]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={top_label: 0.0},   # elastic-finished neck/armhole edges
        notches=notches,
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, TOTAL_H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def build_cf():
    return _panel("cf_panel", True, False,
                  "Centre-front panel (cut 2 pairs, gusset closure below)")


def build_side_front():
    return _panel("side_front_panel", False, False, "Side-front panel (cut 2 pairs)")


def build_side_back():
    return _panel("side_back_panel", False, True, "Side-back panel (cut 2 pairs)")


def build_gusset(crotch_run):
    """The gusset: closes with a HOOK-AND-EYE tape at the crotch (point/slot).

    Its front end is built to the measured centre-front panel's crotch edge so that
    seam balances; the back end carries the hook tape and is a free finished edge — the
    hooks engage the eyes, there is no sewn flange to match.
    """
    w = crotch_run
    ln = gusset_w * 1.6
    edges = [
        fc.Edge("front_end", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_a", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
        fc.Edge("hook_end", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
        fc.Edge("side_b", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "gusset",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hook_end": 0.0},   # the hook tape finishes this edge
        notches=[fc.Notch("hook_end", 0.5, "hook tape centre"),
                 fc.Notch("front_end", 0.5, "centre-front match")],
        grainline=fc.Grainline(fc.P(w * 0.5, ln * 0.2), fc.P(w * 0.5, ln * 0.8)),
        cut=fc.CutSpec(quantity=2),
        label="Gusset (cut 2 — self + cotton lining, hook-and-eye crotch)",
    )


def build():
    pattern = fc.PatternSet("shaping-bodysuit")
    cf = build_cf()
    side_front = build_side_front()
    side_back = build_side_back()
    gusset = build_gusset(cf.edge("crotch").length())

    picked = {"cf_panel": cf, "side_front_panel": side_front,
              "side_back_panel": side_back, "gusset": gusset}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (cf, side_front, side_back, gusset):
            pattern.add(piece)
        # The princess seams: cf -> side_front -> side_back around the body. Every panel
        # shares the same profile, so all of these balance exactly.
        pattern.declare_seam(("cf_panel", "seam_r"), ("side_front_panel", "seam_l"),
                             tol=1.0)
        pattern.declare_seam(("side_front_panel", "seam_r"), ("side_back_panel", "seam_l"),
                             tol=1.0)
        # The gusset's front end sews to the centre-front panel's crotch edge; its hook
        # end is a FREE edge carrying the tape (point/slot — nothing to match).
        pattern.declare_seam(("gusset", "front_end"), ("cf_panel", "crotch"), tol=1.0)

    bust_ring = 6.0 * BUST_P
    waist_ring = 6.0 * WAIST_P
    hip_ring = 6.0 * HIP_P
    neck_arm_run = 2.0 * (cf.edge("shoulder").length()
                          + side_front.edge("armscye").length()
                          + side_back.edge("shoulder").length())

    fabric_width = 1500.0
    area = (cf.area() * 2.0 + side_front.area() * 2.0 + side_back.area() * 2.0
            + gusset.area() * 2.0)
    marker_len = area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "powernet / high-recovery shaping knit",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"panels at {fabric_width:.0f} mm width, 60% marker. Greatest stretch "
                 "HORIZONTAL. The princess seams are themselves structural — a seam is "
                 "stiffer than the cloth, so these lines do the job boning does in a "
                 "corset, without any boning."},
        {"item": "cotton jersey (gusset lining)", "qty": 1, "unit": "piece",
         "note": "the gusset is cut twice: self plus a cotton lining."},
        {"item": "hook-and-eye gusset tape (3 cols x 2 rows)", "qty": 1, "unit": "piece",
         "note": "the crotch closure — Yantra4D hook-and-eye (notion.hardware_ref). "
                 "POINT/SLOT: hooks engage eyes, there is no sewn flange whose length "
                 "must match a garment edge, so only the column and row counts cross "
                 "the bridge. Hardware, never modelled here."},
        {"item": "soft edge elastic 10 mm", "qty": round(neck_arm_run * 0.88),
         "unit": "mm_length",
         "note": f"neck, shoulder and armhole edges {neck_arm_run:.0f} mm x 0.88; these "
                 "are the edges that cut in if over-tightened, so keep the ratio soft."},
        {"item": "polyester stretch thread + ballpoint 75/11", "qty": 1, "unit": "set",
         "note": "4-thread overlock the princess seams; they must stretch as far as the "
                 "cloth or they pop on donning. Coverstitch the finished edges."},
    ]
    pattern.metadata = {
        "fc300_rank": 226, "family": "underwear_lounge", "fabric_hint": "powernet",
        "silhouette_note": "A compression bodysuit shaped by four princess seams per "
            "side running armhole -> bust -> waist -> hip. Distributed shaping instead "
            "of dart tips: no stress risers to blow out, and the seams themselves act "
            "as the structural lines boning would otherwise provide.",
        "hardware": "crotch closure via Yantra4D (notion.hardware_ref -> hook-and-eye), "
            "POINT/SLOT — the fitting has no sewn flange, so only the tape's column and "
            "row counts cross the bridge and no edge coupling is required.",
        "shaping": {
            "compression_pct": compression_pct,
            "waist_reduction_mm": round(waist_reduction, 1),
            "bust_body_mm": round(bust_girth, 1),
            "bust_finished_mm": round(bust_ring, 1),
            "waist_body_mm": round(waist_girth, 1),
            "waist_finished_mm": round(waist_ring, 1),
            "hip_body_mm": round(hip_girth, 1),
            "hip_finished_mm": round(hip_ring, 1),
            "note": "the waist takes the explicit reduction ON TOP of the all-over "
                    "compression — the shaping is stated, not left to the fabric.",
        },
        "solved": {
            "panels": int(PANELS),
            "princess_seams_per_side": 2,
            "panel_height_mm": round(TOTAL_H, 1),
            "waist_line_from_crotch_mm": round(WAIST_Y, 1),
            "princess_seam_len_mm": round(cf.edge("seam_r").length(), 2),
        },
        "closure": "hook-and-eye gusset (3 cols x 2 rows)",
        "drafting": "Made to measure to bust, waist and hip girths plus body rise and "
            "front neck-to-waist; shaping is princess-seam distributed, never darted.",
    }
    return pattern


result = build()

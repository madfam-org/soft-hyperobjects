"""
One-piece Swimsuit — FC-100 rank #54. Fashion Cabinet Garment Cartridge.

The hardest swim garment: a CONTINUOUS full-torso maillot drafted on negative
ease so the tricot grips the whole body. Front and back are fold-cut halves
(CF / CB on the fold) joined at the SHOULDER and SIDE seams and closed at the
crotch by a GUSSET (self + lining) whose front and back edges match the body
crotch edges BY CONSTRUCTION — the same proven-at-render trick as the bikini
panty. A separate FRONT LINING mirrors the front bust/torso (swimsuits are
front-lined). Neckline, armholes and leg openings are elastic-finished
(allowance 0, marked elastic zones) and the BOM emits exact-mm elastic cut
lengths from the measured openings.

The fit-critical dimension is the TORSO LOOP: the vertical girth running from
the shoulder down the front through the crotch and up the back must be drafted
SHORTER than the body (a length negative ease — "the swimsuit stretches to fit
torso length"). Front centre length + back centre length + the gusset span are
derived from that reduced torso girth and the loop is checked to close.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|front_lining|gusset|set

bust_girth        = float(PARAM(lambda: bust_girth, 900.0))
hip_girth         = float(PARAM(lambda: hip_girth, 940.0))
torso_girth       = float(PARAM(lambda: torso_girth, 1550.0))  # shoulder→crotch→shoulder loop
neck_girth        = float(PARAM(lambda: neck_girth, 380.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 14.0))     # girth (width) grip
torso_neg_ease_pct = float(PARAM(lambda: torso_neg_ease_pct, 8.0))    # vertical torso-length grip
back_style        = str(PARAM(lambda: back_style, "scoop"))           # scoop|racer
strap_width       = float(PARAM(lambda: strap_width, 34.0))
gusset_front_w    = float(PARAM(lambda: gusset_front_w, 34.0))
gusset_back_w     = float(PARAM(lambda: gusset_back_w, 40.0))
neck_elastic_ratio   = float(PARAM(lambda: neck_elastic_ratio, 0.90))
armhole_elastic_ratio = float(PARAM(lambda: armhole_elastic_ratio, 0.88))
leg_elastic_ratio    = float(PARAM(lambda: leg_elastic_ratio, 0.85))
seam_allowance    = float(PARAM(lambda: seam_allowance, 7.0))

# ── Clamps (mirror the manifest sliders) ─────────────────────────────────────
bust_girth = max(650.0, min(bust_girth, 1500.0))
hip_girth = max(650.0, min(hip_girth, 1600.0))
torso_girth = max(1200.0, min(torso_girth, 2000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
negative_ease_pct = max(8.0, min(negative_ease_pct, 20.0))
torso_neg_ease_pct = max(0.0, min(torso_neg_ease_pct, 15.0))
if back_style not in ("scoop", "racer"):
    back_style = "scoop"
strap_width = max(18.0, min(strap_width, 70.0))
gusset_front_w = max(24.0, min(gusset_front_w, 60.0))
gusset_back_w = max(24.0, min(gusset_back_w, 60.0))
neck_elastic_ratio = max(0.80, min(neck_elastic_ratio, 1.0))
armhole_elastic_ratio = max(0.80, min(armhole_elastic_ratio, 1.0))
leg_elastic_ratio = max(0.75, min(leg_elastic_ratio, 1.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# ── Derived draft constants ──────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0          # width (girth) reduction
TNEG = 1.0 - torso_neg_ease_pct / 100.0        # vertical torso-length reduction

# Half-widths per fold-cut piece (girth / 4), negative-eased.
BUSTW = bust_girth * NEG / 4.0                 # bust half-width (upper torso)
HIPW = hip_girth * NEG / 4.0                   # hip half-width (lower torso, at the leg corner)
GF = gusset_front_w / 2.0                      # gusset half-widths (gusset drafts on fold too,
GB = gusset_back_w / 2.0                       # so the crotch seams match the half-drafts)
NW = max(52.0, neck_girth / 5.0 - 6.0)         # neck half-width at the front HPS

# Torso loop → centre lengths. The loop girth (shoulder→crotch→shoulder) reduced
# by TNEG is split into a front centre run and a back centre run, plus the gusset
# span that bridges the two crotch edges. Front is a touch longer than back (the
# body is deeper in front through the bust), and the gusset eats the crotch span.
GUSSET_LEN = 78.0                              # crotch-seam to crotch-seam through the legs
loop_reduced = torso_girth * TNEG
centre_total = loop_reduced - GUSSET_LEN       # what the two centre seams must sum to
FRONT_CENTRE = centre_total * 0.52             # front torso centre run (CF fold height)
BACK_CENTRE = centre_total * 0.48              # back torso centre run (CB fold height)

# Shared torso landmarks (front and back share these so shoulder + side seams
# close by construction). y grows upward; the crotch corner sits at y = 0. Each
# CF/CB centre edge runs the full crotch→neckline height, so centre.length()
# equals the designed centre run exactly and the torso loop closes by
# construction. The HPS (high-point shoulder) rides a strap rise ABOVE the
# taller centre so both necklines dip below a common shoulder band; the strap
# bridges neckline→shoulder over the top and is not part of the fit loop.
HIP_Y = 0.0                                    # leg/side corner height (hip line)
STRAP_RISE = 95.0                              # neckline band → shoulder point rise
UNDERARM_Y = min(FRONT_CENTRE, BACK_CENTRE) * 0.60   # armhole depth landmark (shared)
HPS_Y = max(FRONT_CENTRE, BACK_CENTRE) + STRAP_RISE
STRAP_INNER = NW                               # x of the strap's neck side at the HPS
STRAP_OUTER = NW + strap_width                 # x of the strap's armhole side
ELASTIC_ZONE = 8.0                             # marked elastic application width (mm)


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic edge, ELASTIC_ZONE mm inside.

    Pieces here are authored CCW, so the inward normal at tangent t is
    (-t.y, t.x). The fraction window [t0, t1] keeps the trace off the corners.
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


def _leg_curve(gusset_half, coverage):
    """Leg opening from the gusset crotch corner up-and-out to the hip corner.

    `coverage` in [0, 1] bows the curve: low = high-cut (leg scooped high),
    high = fuller coverage. Mirrors the panties-bikini leg idiom scaled to the
    full-torso hip corner.
    """
    lift = HIP_Y  # both ends sit on y = 0..HIP_Y band; corner at (HIPW, HIP_Y)
    c0 = fc.P(gusset_half + 6.0, (UNDERARM_Y * 0.10) * (1.0 - coverage) + 6.0)
    c1 = fc.P(HIPW * (0.55 + 0.30 * coverage), HIP_Y + (UNDERARM_Y * 0.04))
    return fc.Bezier(fc.P(gusset_half, lift), c0, c1, fc.P(HIPW, HIP_Y))


def _torso_piece(name, centre_len, scoop, armhole_pinch, leg_coverage,
                 gusset_half, label, color_role):
    """A fold-cut torso half: crotch, leg, side, armhole, shoulder, neck, centre.

    The centre (CF/CB) edge is the fold, running the FULL crotch→neckline height,
    so centre.length() == centre_len exactly — this is the fit-critical torso
    run. The neckline meets CF at (0, centre_len) and sweeps up to the strap at
    the shared HPS; the strap bridges neckline→shoulder above and is common to
    front and back, so shoulder and side seams balance by construction. `scoop`
    (mm) is how far the neckline bows below the straight CF-top→strap chord — a
    deeper front scoop without changing the centre run.
    """
    neck_cf_y = centre_len            # neckline meets the CF/CB fold here
    crotch = fc.Edge("crotch",
                     [fc.Line(fc.P(0.0, HIP_Y), fc.P(gusset_half, HIP_Y))])
    leg = fc.Edge("leg", [_leg_curve(gusset_half, leg_coverage)])
    side = fc.Edge("side", [fc.Line(fc.P(HIPW, HIP_Y), fc.P(HIPW, UNDERARM_Y))])
    armhole = fc.Edge(
        "armhole",
        [fc.Bezier(fc.P(HIPW, UNDERARM_Y),
                   fc.P(HIPW - armhole_pinch * 0.30, UNDERARM_Y + (HPS_Y - UNDERARM_Y) * 0.40),
                   fc.P(STRAP_OUTER + armhole_pinch * 0.20, HPS_Y - 12.0),
                   fc.P(STRAP_OUTER, HPS_Y))],
    )
    shoulder = fc.Edge("shoulder",
                       [fc.Line(fc.P(STRAP_OUTER, HPS_Y), fc.P(STRAP_INNER, HPS_Y))])
    # Neckline: strap inner point (at HPS) → CF neck point (at centre_len). The
    # control points pull the curve down by `scoop` for the low swim neckline.
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(STRAP_INNER, HPS_Y),
                   fc.P(STRAP_INNER * 0.60, HPS_Y - scoop * 0.55),
                   fc.P(NW * 0.45, neck_cf_y + scoop * 0.20),
                   fc.P(0.0, neck_cf_y))],
    )
    centre = fc.Edge("centre", [fc.Line(fc.P(0.0, neck_cf_y), fc.P(0.0, HIP_Y))])

    return fc.Piece(
        name,
        [crotch, leg, side, armhole, shoulder, neck, centre],
        seam_allowance=seam_allowance,
        allowances={"leg": 0.0, "armhole": 0.0, "neck": 0.0},  # elastic-finished
        notches=[fc.Notch("crotch", 0.5, "gusset match"),
                 fc.Notch("side", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(HIPW * 0.5, HIP_Y + 30.0),
                               fc.P(HIPW * 0.5, centre_len - 30.0)),
        internals=[
            _elastic_zone(leg, "leg elastic zone", 0.08, 0.92),
            _elastic_zone(armhole, "armhole elastic zone", 0.06, 0.94),
            _elastic_zone(neck, "neck elastic zone", 0.08, 0.92),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="centre", mirror=True),
        label=label,
    )


# Neckline scoop depth (mm the curve bows below the CF-top→strap chord).
FRONT_SCOOP = 140.0                            # deep swim front neckline
BACK_SCOOP = 90.0 if back_style == "scoop" else 60.0


def build_front():
    """Front: deep neckline scoop, high-cut leg, longer centre run."""
    return _torso_piece("front", FRONT_CENTRE, FRONT_SCOOP,
                        armhole_pinch=30.0, leg_coverage=0.15,
                        gusset_half=GF, label="Front (self)", color_role="front")


def build_back():
    """Back: scoop or racer back, fuller-coverage leg, shorter centre run."""
    pinch = 30.0 if back_style == "scoop" else 64.0   # racer digs the armhole in
    return _torso_piece("back", BACK_CENTRE, BACK_SCOOP,
                        armhole_pinch=pinch, leg_coverage=0.45,
                        gusset_half=GB, label=f"Back ({back_style})", color_role="back")


def build_front_lining():
    """Front lining: mirrors the front outline, cut in shell/mesh.

    Swimsuits are front-lined; the lining shares the front outline so every mated
    edge stays identical. It is a distinct piece (own colour) so the catalog can
    show the front self + lining pair.
    """
    return _torso_piece("front_lining", FRONT_CENTRE, FRONT_SCOOP,
                        armhole_pinch=30.0, leg_coverage=0.15,
                        gusset_half=GF, label="Front lining", color_role="lining")


def build_gusset():
    """Half-trapezoid crotch gusset on fold; cut 2 = self + lining.

    Front edge = GF wide, back edge = GB wide — identical to the body crotch
    edges by construction. The side (leg) edge is caught under the leg elastic.
    """
    center = fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, GUSSET_LEN))])
    front_edge = fc.Edge("front_edge",
                        [fc.Line(fc.P(0.0, GUSSET_LEN), fc.P(GF, GUSSET_LEN))])
    side = fc.Edge(
        "side",
        [fc.Bezier(fc.P(GF, GUSSET_LEN), fc.P(GF - 2.5, GUSSET_LEN * 0.62),
                   fc.P(GB - 4.5, GUSSET_LEN * 0.30), fc.P(GB, 0.0))],
    )
    back_edge = fc.Edge("back_edge", [fc.Line(fc.P(GB, 0.0), fc.P(0.0, 0.0))])
    return fc.Piece(
        "gusset",
        [center, front_edge, side, back_edge],
        seam_allowance=seam_allowance,
        allowances={"side": 0.0},  # caught under the leg elastic, never turned
        notches=[fc.Notch("front_edge", 0.5, "front match"),
                 fc.Notch("back_edge", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(7.0, GUSSET_LEN * 0.18),
                               fc.P(7.0, GUSSET_LEN * 0.82)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="center", mirror=True),
        label="Gusset (self + lining)",
    )


def build():
    pattern = fc.PatternSet("one-piece-swimsuit")
    front = build_front()
    back = build_back()
    front_lining = build_front_lining()
    gusset = build_gusset()
    picked = {"front": front, "back": back,
              "front_lining": front_lining, "gusset": gusset}

    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # "set"
        for piece in (front, back, front_lining, gusset):
            pattern.add(piece)
        # Crotch closes through the gusset (matched by construction, like the
        # bikini panty): gusset front_edge ↔ front crotch, back_edge ↔ back crotch.
        pattern.declare_seam(("gusset", "front_edge"), ("front", "crotch"), tol=1.0)
        pattern.declare_seam(("gusset", "back_edge"), ("back", "crotch"), tol=1.0)
        # Front and back join at the shoulder and side seams.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)

    # ── Torso-loop closure check (the fit-critical dimension) ─────────────────
    # The loop runs down the front centre, through the gusset span, up the back
    # centre. Its drafted length must equal the target girth reduced by TNEG.
    front_centre_len = front.edge("centre").length()
    back_centre_len = back.edge("centre").length()
    loop_drafted = front_centre_len + back_centre_len + GUSSET_LEN
    loop_target = torso_girth * TNEG
    loop_delta = loop_drafted - loop_target
    if abs(loop_delta) > 2.0:
        raise ValueError(
            f"torso loop does not close: drafted {loop_drafted:.1f} mm vs "
            f"target {loop_target:.1f} mm (delta {loop_delta:+.1f})"
        )

    # ── Elastic accounting (exact-mm cut lengths from measured openings) ──────
    neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
    armhole_opening = front.edge("armhole").length() + back.edge("armhole").length()  # per side
    leg_opening = front.edge("leg").length() + back.edge("leg").length()              # per leg
    neck_elastic = round(neck_opening * neck_elastic_ratio)
    armhole_elastic = round(armhole_opening * armhole_elastic_ratio)                  # per armhole
    leg_elastic = round(leg_opening * leg_elastic_ratio)                              # per leg

    fabric_width = 1500.0  # tricot-nylon-elastano card width
    area = sum(p.area() * p.cut.quantity * 2.0
               for p in (front, back, front_lining, gusset))  # ×2: fold-cut halves
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "tricot-nylon-elastano", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"swim shell: front+back+front lining+gusset (self+lining) at "
                 f"{fabric_width:.0f} mm width, 62% marker efficiency; greatest "
                 "stretch weft (around the body)"},
        {"item": "clear swim elastic 8 mm (neckline)", "qty": neck_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {neck_opening:.0f} mm opening x {neck_elastic_ratio:.2f}; "
                 "join in a ring, quarter-mark, zigzag then coverstitch the marked zone"},
        {"item": "clear swim elastic 8 mm (armholes)", "qty": 2 * armhole_elastic,
         "unit": "mm_length",
         "note": f"two armholes x {armhole_elastic} mm each ({armhole_opening:.0f} mm "
                 f"opening x {armhole_elastic_ratio:.2f})"},
        {"item": "clear swim elastic 8 mm (legs)", "qty": 2 * leg_elastic,
         "unit": "mm_length",
         "note": f"two legs x {leg_elastic} mm each ({leg_opening:.0f} mm opening x "
                 f"{leg_elastic_ratio:.2f}); the gusset side edges are caught underneath"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; stretch/overlock every seam, coverstitch "
                 "the elastic edges. No hardware — pull-on maillot"},
    ]
    pattern.metadata = {
        "fc100_rank": 54,
        "fabric_hint": "tricot-nylon-elastano",
        "stretch_note": "cut with greatest stretch weft (around the body); "
                        "chlorine-resistant grade for pool use",
        "negative_ease_pct": negative_ease_pct,
        "torso_neg_ease_pct": torso_neg_ease_pct,
        "back_style": back_style,
        "bust_half_width_mm": round(BUSTW, 1),
        "hip_half_width_mm": round(HIPW, 1),
        "front_centre_len_mm": round(front_centre_len, 1),
        "back_centre_len_mm": round(back_centre_len, 1),
        "gusset_span_mm": round(GUSSET_LEN, 1),
        "torso_loop_drafted_mm": round(loop_drafted, 1),
        "torso_loop_target_mm": round(loop_target, 1),
        "torso_loop_delta_mm": round(loop_delta, 2),
        "neck_opening_mm": round(neck_opening, 1),
        "neck_elastic_mm": neck_elastic,
        "armhole_opening_each_mm": round(armhole_opening, 1),
        "armhole_elastic_each_mm": armhole_elastic,
        "leg_opening_each_mm": round(leg_opening, 1),
        "leg_elastic_each_mm": leg_elastic,
        "drafting": "front-lined negative-ease one-piece; torso-length negative "
                    "ease is the fit-critical dimension. Front/back fold-cut halves "
                    "join at shoulder + side; crotch closes through a self+lining "
                    "gusset matched by construction; the torso loop (front centre + "
                    "back centre + gusset span) is checked to close to the reduced "
                    "torso girth. Teaching-grade: bust/waist shaping darts are "
                    "omitted (the 4-way stretch tricot molds them out).",
    }
    return pattern


result = build()

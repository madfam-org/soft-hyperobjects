"""
Running Shorts — FC-100 rank #52. Fashion Cabinet Garment Cartridge.

A runner's short: a RELAXED outer short with a scooped/split curved side hem
(the hem edge is a bezier that sweeps UP toward the side seam for stride
clearance) worn over a FITTED compression LINER brief. One elastic waistband
casing catches both layers; the liner attaches only at the waist and hangs
free at the leg.

Three seam-matching techniques from the commons converge here:
  • the outer BACK hem width is solved analytically so the straight outer
    inseams match exactly (rank #18 athletic-shorts idiom), and the same
    solve is applied to the liner;
  • the liner waist width is PINNED to the outer waist width so both layers
    meet the waistband at one length (waist seam delta ≈ 0 by construction);
  • the liner is cut with negative ease at the hip and leg (rank #7 leggings /
    rank #45 panties idiom) while its leg opening is elastic-finished with an
    exact-mm elastic cut length in the BOM.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
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
# target: outer_front|outer_back|liner_front|liner_back|waistband|set
target_piece = str(PARAM(lambda: target_piece, "set"))

hip_girth      = float(PARAM(lambda: hip_girth, 1000.0))
outer_inseam   = float(PARAM(lambda: outer_inseam, 130.0))   # outer short inseam (mm)
liner_inseam   = float(PARAM(lambda: liner_inseam, 55.0))    # short compression liner
front_rise     = float(PARAM(lambda: front_rise, 260.0))
back_rise      = float(PARAM(lambda: back_rise, 295.0))
sport_ease     = float(PARAM(lambda: sport_ease, 140.0))     # relaxed outer ease
outer_hem_width = float(PARAM(lambda: outer_hem_width, 250.0))  # front half-hem, flat
side_scoop     = float(PARAM(lambda: side_scoop, 55.0))      # side-hem rise (split hem)
liner_neg_ease = float(PARAM(lambda: liner_neg_ease, 10.0))  # liner negative ease (%)
elastic_width  = float(PARAM(lambda: elastic_width, 35.0))
waist_elastic_ratio = float(PARAM(lambda: waist_elastic_ratio, 0.90))
leg_elastic_ratio   = float(PARAM(lambda: leg_elastic_ratio, 0.88))
drawcord_ratio = float(PARAM(lambda: drawcord_ratio, 1.30))  # drawcord/waist length
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 18.0))

# ── Clamps (mirror the manifest slider ranges) ───────────────────────────────
hip_girth = max(650.0, min(hip_girth, 1800.0))
outer_inseam = max(70.0, min(outer_inseam, 250.0))
liner_inseam = max(20.0, min(liner_inseam, 140.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 80.0))
sport_ease = max(80.0, min(sport_ease, 360.0))
outer_hem_width = max(170.0, min(outer_hem_width, 360.0))
side_scoop = max(0.0, min(side_scoop, 120.0))
liner_neg_ease = max(0.0, min(liner_neg_ease, 18.0))
elastic_width = max(20.0, min(elastic_width, 60.0))
waist_elastic_ratio = max(0.80, min(waist_elastic_ratio, 1.0))
leg_elastic_ratio = max(0.75, min(leg_elastic_ratio, 1.0))
drawcord_ratio = max(1.0, min(drawcord_ratio, 1.6))
seam_allowance = max(0.0, min(seam_allowance, 15.0))
hem_allowance = max(0.0, min(hem_allowance, 40.0))

# ── Outer geometry (relaxed short, curved/split side hem) ────────────────────
HIP_E = hip_girth + sport_ease
CROTCH_Y = outer_inseam
WAIST_Y = outer_inseam + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0, HIP_E / 12.0
HEM_DROP = 0.0                       # hem lowest point (at the inseam corner)
OF_WAIST_IN = FW * 0.92              # outer waist inner x (front)
OB_WAIST_IN = BW * 0.92              # outer waist inner x (back)
ELASTIC_ZONE = 8.0                   # marked elastic application width (mm)


def _outer_back_hem():
    """Solve the outer back hem half-width so the straight inseams match."""
    f_tip_x = FW + FORK_F
    b_tip_x = BW + FORK_B
    dy = CROTCH_Y - HEM_DROP
    front_len = math.hypot(f_tip_x - outer_hem_width, dy)
    run = math.sqrt(max(front_len ** 2 - dy ** 2, 25.0))
    bhw = b_tip_x - run
    if bhw < 100.0:
        raise ValueError("solved outer back hem width degenerate; widen outer_hem_width")
    return bhw


def _outer_piece(name, width, tip_x, hem_w, cb_y, waist_in, label):
    """Relaxed outer short half: vertical side (scooped) + bezier curved hem."""
    edges = [
        # side/outseam: vertical, starting at the scooped hem corner
        fc.Edge("side", [fc.Line(fc.P(0.0, side_scoop), fc.P(0.0, WAIST_Y))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
        fc.Edge(
            "crotch",
            [fc.Bezier(fc.P(waist_in, cb_y),
                       fc.P(width - 4.0, cb_y - front_rise * 0.45),
                       fc.P(width + (tip_x - width) * 0.35, CROTCH_Y + 40.0),
                       fc.P(tip_x, CROTCH_Y))],
        ),
        fc.Edge("inseam", [fc.Line(fc.P(tip_x, CROTCH_Y), fc.P(hem_w, HEM_DROP))]),
        # curved/split hem: bezier sweeping UP from the hem corner to the side scoop
        fc.Edge(
            "hem",
            [fc.Bezier(fc.P(hem_w, HEM_DROP),
                       fc.P(hem_w * 0.55, HEM_DROP - 6.0),
                       fc.P(hem_w * 0.22, side_scoop * 0.35),
                       fc.P(0.0, side_scoop))],
        ),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(width * 0.45, WAIST_Y * 0.15),
                               fc.P(width * 0.45, WAIST_Y * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def build_outer():
    bhw = _outer_back_hem()
    front = _outer_piece("outer_front", FW, FW + FORK_F, outer_hem_width, WAIST_Y,
                         OF_WAIST_IN, "Outer Front")
    back = _outer_piece("outer_back", BW, BW + FORK_B, bhw,
                        WAIST_Y + (back_rise - front_rise), OB_WAIST_IN, "Outer Back")
    return front, back


# ── Liner geometry (fitted compression brief, negative ease) ─────────────────
NEG = 1.0 - liner_neg_ease / 100.0
LCROTCH_Y = liner_inseam
LWAIST_Y = liner_inseam + front_rise
LFW = (hip_girth * NEG) / 4.0 - 8.0
LBW = (hip_girth * NEG) / 4.0 + 8.0
LFORK_F, LFORK_B = (hip_girth * NEG) / 16.0, (hip_girth * NEG) / 12.0


def _liner_back_hem():
    """Solve the liner back hem half-width so the liner inseams match."""
    lf_tip_x = LFW + LFORK_F
    lb_tip_x = LBW + LFORK_B
    ldy = LCROTCH_Y
    lhem_f = LFW * 0.86
    lfront_len = math.hypot(lf_tip_x - lhem_f, ldy)
    lrun = math.sqrt(max(lfront_len ** 2 - ldy ** 2, 25.0))
    lhem_b = lb_tip_x - lrun
    if lhem_b < 60.0:
        raise ValueError("solved liner back hem width degenerate; raise liner_inseam")
    return lhem_f, lhem_b


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic edge, ELASTIC_ZONE mm inside.

    Pieces here are authored CCW; the inward normal at tangent t is (-t.y, t.x).
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


def _liner_piece(name, waist_in, tip_x, hem_w, cb_y, hipw, label):
    """Compression liner half: waist pinned to outer waist; leg elastic-finished."""
    hem = fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))])
    edges = [
        fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, LWAIST_Y))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, LWAIST_Y), fc.P(waist_in, cb_y))]),
        fc.Edge(
            "crotch",
            [fc.Bezier(fc.P(waist_in, cb_y),
                       fc.P(hipw - 4.0, cb_y - front_rise * 0.42),
                       fc.P(hipw + (tip_x - hipw) * 0.35, LCROTCH_Y + 30.0),
                       fc.P(tip_x, LCROTCH_Y))],
        ),
        fc.Edge("inseam", [fc.Line(fc.P(tip_x, LCROTCH_Y), fc.P(hem_w, 0.0))]),
        hem,
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 0.0},  # leg opening is elastic-finished, not turned
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(hipw * 0.4, LWAIST_Y * 0.2),
                               fc.P(hipw * 0.4, LWAIST_Y * 0.8)),
        internals=[_elastic_zone(hem, "leg elastic zone", 0.08, 0.92)],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def build_liner():
    lhem_f, lhem_b = _liner_back_hem()
    front = _liner_piece("liner_front", OF_WAIST_IN, LFW + LFORK_F, lhem_f, LWAIST_Y,
                         LFW, "Liner Front (compression)")
    back = _liner_piece("liner_back", OB_WAIST_IN, LBW + LFORK_B, lhem_b,
                        LWAIST_Y + (back_rise - front_rise), LBW,
                        "Liner Back (compression)")
    return front, back


# ── Waistband (one elastic casing catching both layers) ──────────────────────
def build_waistband(outer_front, outer_back):
    """Fold-over casing. Bottom edge = the outer waist opening exactly, so the
    band ↔ outer-waist seam balances; the elastic inside is shorter (BOM)."""
    circ = 2.0 * (outer_front.edge("waist").length() + outer_back.edge("waist").length())
    length = circ
    band_h = 2.0 * (elastic_width + seam_allowance)
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)]),
            fc.Internal("drawcord channel",
                        [fc.P(length * 0.30, band_h * 0.30), fc.P(length * 0.70, band_h * 0.30)]),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Waistband Casing",
    )


# ── Assembly ─────────────────────────────────────────────────────────────────
def build():
    pattern = fc.PatternSet("running-shorts")
    outer_front, outer_back = build_outer()
    liner_front, liner_back = build_liner()
    waistband = build_waistband(outer_front, outer_back)

    picked = {
        "outer_front": outer_front,
        "outer_back": outer_back,
        "liner_front": liner_front,
        "liner_back": liner_back,
        "waistband": waistband,
    }
    everything = target_piece == "set"
    if everything:
        for piece in (outer_front, outer_back, liner_front, liner_back, waistband):
            pattern.add(piece)
    elif target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # unknown target → build the full set
        for piece in (outer_front, outer_back, liner_front, liner_back, waistband):
            pattern.add(piece)
        everything = True

    if everything:
        # Outer short seams (curved side + straight inseam, both matched)
        pattern.declare_seam(("outer_front", "side"), ("outer_back", "side"), tol=1.5)
        pattern.declare_seam(("outer_front", "inseam"), ("outer_back", "inseam"), tol=1.5)
        # Liner brief seams
        pattern.declare_seam(("liner_front", "side"), ("liner_back", "side"), tol=1.5)
        pattern.declare_seam(("liner_front", "inseam"), ("liner_back", "inseam"), tol=1.5)
        # Liner attaches to the outer AT THE WAIST (stacked), and the waistband
        # catches that stack — both length-match the outer waist opening.
        pattern.declare_seam(
            [("liner_front", "waist"), ("liner_front", "waist"),
             ("liner_back", "waist"), ("liner_back", "waist")],
            [("outer_front", "waist"), ("outer_front", "waist"),
             ("outer_back", "waist"), ("outer_back", "waist")],
            tol=1.5,
        )
        pattern.declare_seam(
            ("waistband", "bottom"),
            [("outer_front", "waist"), ("outer_front", "waist"),
             ("outer_back", "waist"), ("outer_back", "waist")],
            tol=1.5,
        )

    # ── BOM: exact fabric + exact-mm elastics + drawcord + thread ────────────
    waist_opening = 2.0 * (outer_front.edge("waist").length()
                           + outer_back.edge("waist").length())
    leg_opening = liner_front.edge("hem").length() + liner_back.edge("hem").length()
    waist_elastic = round(waist_opening * waist_elastic_ratio)
    leg_elastic = round(leg_opening * leg_elastic_ratio)          # per leg
    drawcord_len = round(waist_opening * drawcord_ratio)

    outer_width = 1550.0   # poliester-elastano-compresion card width
    liner_width = 1500.0   # tricot-nylon-elastano card width
    outer_area = sum(p.area() * p.cut.quantity for p in (outer_front, outer_back))
    liner_area = sum(p.area() * p.cut.quantity for p in (liner_front, liner_back))
    outer_marker = outer_area / (outer_width * 0.62)
    liner_marker = liner_area / (liner_width * 0.60)

    pattern.bom = [
        {"item": "poliester-elastano-compresion", "qty": round(outer_marker / 10.0) * 10,
         "unit": "mm_length",
         "note": f"outer short shell at {outer_width:.0f} mm width, 62% marker "
                 "efficiency; greatest stretch (weft) horizontal around the body"},
        {"item": "tricot-nylon-elastano", "qty": round(liner_marker / 10.0) * 10,
         "unit": "mm_length",
         "note": f"compression liner brief at {liner_width:.0f} mm width, 60% marker "
                 "efficiency; a lighter liner fabric than the outer shell"},
        {"item": "plush-back waist elastic 35 mm", "qty": waist_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {waist_opening:.0f} mm opening x {waist_elastic_ratio:.2f}; "
                 "join in a ring, quarter-mark, enclose in the casing catching both layers"},
        {"item": "clear/knit leg elastic 6 mm", "qty": 2 * leg_elastic,
         "unit": "mm_length",
         "note": f"two liner legs x {leg_elastic} mm each ({leg_opening:.0f} mm opening x "
                 f"{leg_elastic_ratio:.2f}); coverstitch into the marked leg zone"},
        {"item": "flat drawcord 4 mm", "qty": drawcord_len,
         "unit": "mm_length",
         "note": f"internal drawcord: {waist_opening:.0f} mm opening x {drawcord_ratio:.2f}; "
                 "threaded through the casing drawcord channel; cord stops/tips are a "
                 "Yantra4D notion reference, not modelled here"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; flatlock/coverstitch or 4-thread overlock "
                 "every seam to avoid chafe. No hardware."},
    ]

    pattern.metadata = {
        "fc100_rank": 52,
        "fabric_hint": "poliester-elastano-compresion",
        "liner_fabric_hint": "tricot-nylon-elastano",
        "construction": "relaxed outer short with a scooped/split curved side hem over a "
                        "fitted compression liner; one elastic casing catches both layers",
        "curved_hem_note": "the outer hem edge is a bezier that sweeps up "
                           f"{side_scoop:.0f} mm at the side seam (split-hem stride clearance)",
        "built_in_liner_note": "liner attaches at the waist only and hangs free at the leg; "
                               "its leg opening is elastic-finished",
        "liner_negative_ease_pct": liner_neg_ease,
        "waist_opening_mm": round(waist_opening, 1),
        "waist_elastic_mm": waist_elastic,
        "leg_opening_each_mm": round(leg_opening, 1),
        "leg_elastic_each_mm": leg_elastic,
        "drawcord_mm": drawcord_len,
        "outer_back_hem_solved": "back hem width solved so straight outer inseams match",
        "liner_waist_pinned": "liner waist width pinned to the outer waist so the waist "
                              "seam balances (delta ~ 0)",
        "drafting": "teaching-grade: outer and liner share one waistband; both back hems "
                    "solved analytically; the liner is drafted with negative ease while its "
                    "waist is pinned to the outer waist so all waist-stack seams balance.",
    }
    return pattern


result = build()
